from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, cast
from uuid import uuid4

from sqlalchemy import desc, func, text
from sqlmodel import Session, select

from recoleta.models import (
    Item,
    Metric,
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


class RuntimeStoreMixin:
    engine: Any

    def _commit(self, session: Session) -> None: ...

    def create_run(self, config_fingerprint: str, run_id: str | None = None) -> Run:
        now = utc_now()
        run = Run(
            id=run_id or str(uuid4()),
            started_at=now,
            heartbeat_at=now,
            status=RUN_STATUS_RUNNING,
            config_fingerprint=config_fingerprint,
        )
        with Session(self.engine) as session:
            session.add(run)
            self._commit(session)
            session.refresh(run)
            return run

    def finish_run(self, run_id: str, success: bool) -> None:
        final_status = RUN_STATUS_SUCCEEDED if success else RUN_STATUS_FAILED
        finished_at = utc_now()
        with Session(self.engine) as session:
            run = session.get(Run, run_id)
            if run is None:
                return
            run.status = final_status
            run.finished_at = finished_at
            run.heartbeat_at = finished_at
            session.add(run)
            self._commit(session)

    def heartbeat_run(self, run_id: str, *, now: datetime | None = None) -> None:
        heartbeat_at = now or utc_now()
        statement = text(
            """
            UPDATE runs
            SET heartbeat_at = :heartbeat_at
            WHERE id = :run_id
              AND status = :running_status;
            """
        )
        with self.engine.begin() as conn:
            conn.execute(
                statement,
                {
                    "heartbeat_at": heartbeat_at,
                    "run_id": run_id,
                    "running_status": RUN_STATUS_RUNNING,
                },
            )

    def mark_stale_runs_failed(
        self,
        *,
        stale_after_seconds: int,
        now: datetime | None = None,
    ) -> int:
        reference_now = now or utc_now()
        cutoff = reference_now - timedelta(seconds=max(1, int(stale_after_seconds)))
        statement = text(
            """
            UPDATE runs
            SET status = :failed_status,
                finished_at = :finished_at,
                heartbeat_at = :finished_at
            WHERE status = :running_status
              AND COALESCE(heartbeat_at, started_at) < :cutoff;
            """
        )
        with self.engine.begin() as conn:
            result = conn.execute(
                statement,
                {
                    "failed_status": RUN_STATUS_FAILED,
                    "finished_at": reference_now,
                    "running_status": RUN_STATUS_RUNNING,
                    "cutoff": cutoff,
                },
            )
        return int(result.rowcount or 0)

    def acquire_workspace_lease(
        self,
        *,
        owner_token: str,
        command: str,
        lease_timeout_seconds: int,
        run_id: str | None = None,
        hostname: str | None = None,
        pid: int | None = None,
        name: str = WORKSPACE_LEASE_NAME,
        now: datetime | None = None,
    ) -> WorkspaceLease:
        acquired_at = now or utc_now()
        expires_at = acquired_at + timedelta(seconds=max(1, int(lease_timeout_seconds)))
        statement = text(
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
        with self.engine.begin() as conn:
            result = conn.execute(
                statement,
                {
                    "name": name,
                    "owner_token": owner_token,
                    "run_id": run_id,
                    "pid": pid,
                    "hostname": hostname,
                    "command": command,
                    "acquired_at": acquired_at,
                    "heartbeat_at": acquired_at,
                    "expires_at": expires_at,
                },
            )
        lease = self.get_workspace_lease(name=name)
        if int(result.rowcount or 0) <= 0 or lease is None:
            raise self._workspace_lease_held_error(
                name=name,
                requested_run_id=run_id,
            )
        return lease

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

    def list_recent_runs(self, *, limit: int = 5) -> list[Run]:
        normalized_limit = max(0, int(limit))
        if normalized_limit <= 0:
            return []
        with Session(self.engine) as session:
            statement = (
                select(Run)
                .order_by(
                    desc(cast(Any, Run.started_at)),
                    desc(cast(Any, Run.id)),
                )
                .limit(normalized_limit)
            )
            return list(session.exec(statement))

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

    def record_metric(
        self, *, run_id: str, name: str, value: float, unit: str | None = None
    ) -> None:
        metric = Metric(run_id=run_id, name=name, value=value, unit=unit)
        with Session(self.engine) as session:
            session.add(metric)
            self._commit(session)

    def list_metrics(self, *, run_id: str) -> list[Metric]:
        with Session(self.engine) as session:
            statement = (
                select(Metric)
                .where(Metric.run_id == run_id)
                .order_by(cast(Any, Metric.id))
            )
            return list(session.exec(statement))
