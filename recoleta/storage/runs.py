from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
import json
from typing import Any, cast
from uuid import uuid4

from sqlalchemy import desc, text
from sqlmodel import Session, select

from recoleta.models import (
    Metric,
    Run,
    RUN_STATUS_FAILED,
    RUN_STATUS_RUNNING,
    RUN_STATUS_SUCCEEDED,
    RUN_TERMINAL_STATE_FAILED,
    RUN_TERMINAL_STATE_SUCCEEDED_CLEAN,
)
from recoleta.types import MetricPoint, utc_now


class RunStoreMixin:
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

    def finish_run(
        self,
        run_id: str,
        success: bool,
        *,
        terminal_state: str | None = None,
    ) -> None:
        final_status = RUN_STATUS_SUCCEEDED if success else RUN_STATUS_FAILED
        resolved_terminal_state = (
            terminal_state
            if terminal_state is not None
            else (
                RUN_TERMINAL_STATE_SUCCEEDED_CLEAN
                if success
                else RUN_TERMINAL_STATE_FAILED
            )
        )
        finished_at = utc_now()
        with Session(self.engine) as session:
            run = session.get(Run, run_id)
            if run is None:
                return
            run.status = final_status
            run.terminal_state = resolved_terminal_state
            run.finished_at = finished_at
            run.heartbeat_at = finished_at
            session.add(run)
            self._commit(session)

    def update_run_context(
        self,
        *,
        request: UpdateRunContextRequest | None = None,
        **legacy_kwargs: Any,
    ) -> None:
        normalized_request = coerce_update_run_context_request(
            request=request,
            legacy_kwargs=legacy_kwargs,
        )
        if not normalized_request.run_id:
            return
        with Session(self.engine) as session:
            run = session.get(Run, normalized_request.run_id)
            if run is None:
                return
            changed = False
            for name, value in _run_context_updates(normalized_request):
                if value is None or getattr(run, name, None) == value:
                    continue
                setattr(run, name, value)
                changed = True
            if not changed:
                return
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

    def get_run(self, *, run_id: str) -> Run | None:
        normalized_run_id = str(run_id or "").strip()
        if not normalized_run_id:
            return None
        with Session(self.engine) as session:
            return session.get(Run, normalized_run_id)

    def record_metric(
        self, *, run_id: str, name: str, value: float, unit: str | None = None
    ) -> None:
        metric = Metric(run_id=run_id, name=name, value=value, unit=unit)
        with Session(self.engine) as session:
            session.add(metric)
            self._commit(session)

    def record_metrics_batch(
        self, *, run_id: str, metrics: list[MetricPoint]
    ) -> int:
        normalized: list[Metric] = []
        for metric in metrics:
            name = str(metric.name or "").strip()
            if not name:
                continue
            normalized.append(
                Metric(
                    run_id=run_id,
                    name=name,
                    value=float(metric.value),
                    unit=metric.unit,
                )
            )
        if not normalized:
            return 0
        with Session(self.engine) as session:
            session.add_all(normalized)
            self._commit(session)
        return len(normalized)

    def list_metrics(self, *, run_id: str) -> list[Metric]:
        with Session(self.engine) as session:
            statement = (
                select(Metric)
                .where(Metric.run_id == run_id)
                .order_by(cast(Any, Metric.id))
            )
            return list(session.exec(statement))


@dataclass(frozen=True, slots=True)
class UpdateRunContextRequest:
    run_id: str
    command: str | None = None
    operation_kind: str | None = None
    scope: str | None = None
    granularity: str | None = None
    period_start: datetime | None = None
    period_end: datetime | None = None
    target_granularity: str | None = None
    target_period_start: datetime | None = None
    target_period_end: datetime | None = None
    requested_steps: list[str] | None = None
    executed_steps: list[str] | None = None
    skipped_steps: list[str] | None = None
    billing_by_step: dict[str, Any] | None = None


def _normalized_optional_text(value: str | None) -> str | None:
    return str(value or "").strip() or None


def _normalized_json(value: Any) -> str | None:
    return json.dumps(value, ensure_ascii=False, sort_keys=True) if value is not None else None


def coerce_update_run_context_request(
    *,
    request: UpdateRunContextRequest | None = None,
    legacy_kwargs: dict[str, Any],
) -> UpdateRunContextRequest:
    if request is not None:
        return request
    return UpdateRunContextRequest(
        run_id=str(legacy_kwargs["run_id"] or "").strip(),
        command=legacy_kwargs.get("command"),
        operation_kind=legacy_kwargs.get("operation_kind"),
        scope=legacy_kwargs.get("scope"),
        granularity=legacy_kwargs.get("granularity"),
        period_start=legacy_kwargs.get("period_start"),
        period_end=legacy_kwargs.get("period_end"),
        target_granularity=legacy_kwargs.get("target_granularity"),
        target_period_start=legacy_kwargs.get("target_period_start"),
        target_period_end=legacy_kwargs.get("target_period_end"),
        requested_steps=legacy_kwargs.get("requested_steps"),
        executed_steps=legacy_kwargs.get("executed_steps"),
        skipped_steps=legacy_kwargs.get("skipped_steps"),
        billing_by_step=legacy_kwargs.get("billing_by_step"),
    )


def _run_context_updates(request: UpdateRunContextRequest) -> tuple[tuple[str, Any], ...]:
    return (
        ("command", _normalized_optional_text(request.command)),
        ("operation_kind", _normalized_optional_text(request.operation_kind)),
        ("scope", _normalized_optional_text(request.scope)),
        ("granularity", _normalized_optional_text(request.granularity)),
        ("period_start", request.period_start),
        ("period_end", request.period_end),
        ("target_granularity", _normalized_optional_text(request.target_granularity)),
        ("target_period_start", request.target_period_start),
        ("target_period_end", request.target_period_end),
        ("requested_steps_json", _normalized_json(request.requested_steps)),
        ("executed_steps_json", _normalized_json(request.executed_steps)),
        ("skipped_steps_json", _normalized_json(request.skipped_steps)),
        ("billing_by_step_json", _normalized_json(request.billing_by_step)),
    )
