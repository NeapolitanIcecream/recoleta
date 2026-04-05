from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, cast

from sqlalchemy import desc, func, text
from sqlmodel import Session, select

from recoleta.models import (
    Item,
    Run,
    WorkspaceLease,
    ITEM_STATE_ANALYZED,
    ITEM_STATE_ENRICHED,
    ITEM_STATE_FAILED,
    ITEM_STATE_INGESTED,
    ITEM_STATE_PUBLISHED,
    ITEM_STATE_RETRYABLE_FAILED,
    ITEM_STATE_TRIAGED,
    RUN_STATUS_FAILED,
    RUN_STATUS_RUNNING,
    RUN_STATUS_SUCCEEDED,
)
from recoleta.storage_common import (
    WORKSPACE_LEASE_NAME,
    WorkspaceLeaseHeldError,
    WorkspaceLeaseLostError,
    WorkspaceStatsResult,
)
from recoleta.types import utc_now


@dataclass(frozen=True, slots=True)
class AcquireWorkspaceLeaseRequest:
    owner_token: str
    command: str
    lease_timeout_seconds: int
    run_id: str | None = None
    hostname: str | None = None
    pid: int | None = None
    name: str = WORKSPACE_LEASE_NAME
    now: datetime | None = None


class WorkspaceLeaseStoreMixin:
    engine: Any

    def acquire_workspace_lease(
        self,
        request: AcquireWorkspaceLeaseRequest | None = None,
        **legacy_kwargs: Any,
    ) -> WorkspaceLease:
        resolved_request = request or AcquireWorkspaceLeaseRequest(
            owner_token=str(legacy_kwargs["owner_token"]),
            command=str(legacy_kwargs["command"]),
            lease_timeout_seconds=int(legacy_kwargs["lease_timeout_seconds"]),
            run_id=legacy_kwargs.get("run_id"),
            hostname=legacy_kwargs.get("hostname"),
            pid=legacy_kwargs.get("pid"),
            name=str(legacy_kwargs.get("name") or WORKSPACE_LEASE_NAME),
            now=legacy_kwargs.get("now"),
        )
        acquired_at, expires_at = _lease_window(request=resolved_request)
        with self.engine.begin() as conn:
            result = conn.execute(
                _workspace_lease_upsert_statement(),
                _workspace_lease_upsert_params(
                    request=resolved_request,
                    acquired_at=acquired_at,
                    expires_at=expires_at,
                ),
            )
        return _acquired_workspace_lease(
            store=self,
            request=resolved_request,
            rowcount=int(result.rowcount or 0),
        )

    def renew_workspace_lease(
        self,
        *,
        owner_token: str,
        lease_timeout_seconds: int,
        name: str = WORKSPACE_LEASE_NAME,
        now: datetime | None = None,
    ) -> WorkspaceLease:
        heartbeat_at = now or utc_now()
        expires_at = heartbeat_at + timedelta(seconds=max(1, int(lease_timeout_seconds)))
        statement = text(
            """
            UPDATE workspace_leases
            SET heartbeat_at = :heartbeat_at,
                expires_at = :expires_at
            WHERE name = :name
              AND owner_token = :owner_token;
            """
        )
        with self.engine.begin() as conn:
            result = conn.execute(
                statement,
                {
                    "heartbeat_at": heartbeat_at,
                    "expires_at": expires_at,
                    "name": name,
                    "owner_token": owner_token,
                },
            )
        if int(result.rowcount or 0) <= 0:
            raise WorkspaceLeaseLostError(
                lease_name=name,
                owner_token=owner_token,
            )
        lease = self.get_workspace_lease(name=name)
        if lease is None:
            raise WorkspaceLeaseLostError(
                lease_name=name,
                owner_token=owner_token,
            )
        return lease

    def release_workspace_lease(
        self,
        *,
        owner_token: str,
        name: str = WORKSPACE_LEASE_NAME,
    ) -> bool:
        statement = text(
            """
            DELETE FROM workspace_leases
            WHERE name = :name
              AND owner_token = :owner_token;
            """
        )
        with self.engine.begin() as conn:
            result = conn.execute(
                statement,
                {
                    "name": name,
                    "owner_token": owner_token,
                },
            )
        return int(result.rowcount or 0) > 0

    def get_workspace_lease(
        self, *, name: str = WORKSPACE_LEASE_NAME
    ) -> WorkspaceLease | None:
        with Session(self.engine) as session:
            return session.get(WorkspaceLease, name)

    def collect_workspace_stats(
        self,
        *,
        stale_after_seconds: int,
        now: datetime | None = None,
    ) -> WorkspaceStatsResult:
        reference_now = now or utc_now()
        cutoff = reference_now - timedelta(seconds=max(1, int(stale_after_seconds)))
        item_state_counts = {
            ITEM_STATE_INGESTED: 0,
            ITEM_STATE_ENRICHED: 0,
            ITEM_STATE_TRIAGED: 0,
            ITEM_STATE_ANALYZED: 0,
            ITEM_STATE_PUBLISHED: 0,
            ITEM_STATE_RETRYABLE_FAILED: 0,
            ITEM_STATE_FAILED: 0,
        }
        run_status_counts = {
            RUN_STATUS_RUNNING: 0,
            RUN_STATUS_SUCCEEDED: 0,
            RUN_STATUS_FAILED: 0,
        }

        with Session(self.engine) as session:
            item_counts_statement = select(
                Item.state,
                func.count(cast(Any, Item.id)),
            ).group_by(Item.state)
            for state, count in session.exec(item_counts_statement):
                normalized_state = str(state or "").strip()
                if not normalized_state:
                    continue
                item_state_counts[normalized_state] = int(count or 0)

            oldest_unfinished_statement = select(func.min(cast(Any, Item.created_at))).where(
                ~cast(Any, Item.state).in_([ITEM_STATE_PUBLISHED, ITEM_STATE_FAILED])
            )
            oldest_unfinished_at = session.exec(oldest_unfinished_statement).one()

            run_counts_statement = select(
                Run.status,
                func.count(cast(Any, Run.id)),
            ).group_by(Run.status)
            for status, count in session.exec(run_counts_statement):
                normalized_status = str(status or "").strip()
                if not normalized_status:
                    continue
                run_status_counts[normalized_status] = int(count or 0)

            stale_running_statement = select(func.count(cast(Any, Run.id))).where(
                Run.status == RUN_STATUS_RUNNING,
                func.coalesce(Run.heartbeat_at, Run.started_at) < cutoff,
            )
            stale_running_runs = int(session.exec(stale_running_statement).one())

            latest_successful_statement = (
                select(Run)
                .where(Run.status == RUN_STATUS_SUCCEEDED)
                .order_by(
                    desc(cast(Any, Run.finished_at)),
                    desc(cast(Any, Run.started_at)),
                    desc(cast(Any, Run.id)),
                )
                .limit(1)
            )
            latest_successful_run = session.exec(latest_successful_statement).first()

        unfinished_total = sum(
            count
            for state, count in item_state_counts.items()
            if state not in {ITEM_STATE_PUBLISHED, ITEM_STATE_FAILED}
        )
        latest_successful_run_at = None
        latest_successful_run_id = None
        if latest_successful_run is not None:
            latest_successful_run_id = latest_successful_run.id
            latest_successful_run_at = (
                latest_successful_run.finished_at
                or latest_successful_run.heartbeat_at
                or latest_successful_run.started_at
            )

        return WorkspaceStatsResult(
            item_state_counts=item_state_counts,
            unfinished_total=unfinished_total,
            oldest_unfinished_at=oldest_unfinished_at,
            run_status_counts=run_status_counts,
            stale_running_runs=stale_running_runs,
            latest_successful_run_id=latest_successful_run_id,
            latest_successful_run_at=latest_successful_run_at,
        )

    def _workspace_lease_held_error(
        self,
        *,
        name: str,
        requested_run_id: str | None,
    ) -> WorkspaceLeaseHeldError:
        lease = self.get_workspace_lease(name=name)
        return WorkspaceLeaseHeldError(
            lease_name=name,
            holder_run_id=(lease.run_id if lease is not None else None),
            holder_command=(lease.command if lease is not None else None),
            holder_hostname=(lease.hostname if lease is not None else None),
            holder_pid=(lease.pid if lease is not None else None),
            expires_at=(lease.expires_at if lease is not None else None),
            requested_run_id=requested_run_id,
        )


def _lease_window(
    *,
    request: AcquireWorkspaceLeaseRequest,
) -> tuple[datetime, datetime]:
    acquired_at = request.now or utc_now()
    expires_at = acquired_at + timedelta(
        seconds=max(1, int(request.lease_timeout_seconds))
    )
    return acquired_at, expires_at


def _acquired_workspace_lease(
    *,
    store: Any,
    request: AcquireWorkspaceLeaseRequest,
    rowcount: int,
) -> WorkspaceLease:
    lease = store.get_workspace_lease(name=request.name)
    if rowcount <= 0 or lease is None:
        raise store._workspace_lease_held_error(
            name=request.name,
            requested_run_id=request.run_id,
        )
    return lease


def _workspace_lease_upsert_statement() -> Any:
    return text(
        """
        INSERT INTO workspace_leases (
            name,
            owner_token,
            run_id,
            pid,
            hostname,
            command,
            acquired_at,
            heartbeat_at,
            expires_at
        )
        VALUES (
            :name,
            :owner_token,
            :run_id,
            :pid,
            :hostname,
            :command,
            :acquired_at,
            :heartbeat_at,
            :expires_at
        )
        ON CONFLICT(name) DO UPDATE SET
            owner_token = excluded.owner_token,
            run_id = excluded.run_id,
            pid = excluded.pid,
            hostname = excluded.hostname,
            command = excluded.command,
            acquired_at = excluded.acquired_at,
            heartbeat_at = excluded.heartbeat_at,
            expires_at = excluded.expires_at
        WHERE workspace_leases.expires_at <= :acquired_at
           OR workspace_leases.owner_token = :owner_token;
        """
    )


def _workspace_lease_upsert_params(
    *,
    request: AcquireWorkspaceLeaseRequest,
    acquired_at: datetime,
    expires_at: datetime,
) -> dict[str, Any]:
    return {
        "name": request.name,
        "owner_token": request.owner_token,
        "run_id": request.run_id,
        "pid": request.pid,
        "hostname": request.hostname,
        "command": request.command,
        "acquired_at": acquired_at,
        "heartbeat_at": acquired_at,
        "expires_at": expires_at,
    }
