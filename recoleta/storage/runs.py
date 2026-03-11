from __future__ import annotations

from datetime import datetime, timedelta
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
