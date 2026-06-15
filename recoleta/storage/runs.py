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
    WorkflowStepReceipt,
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

    def get_run_source_diagnostics(self, *, run_id: str) -> dict[str, Any]:
        normalized_run_id = str(run_id or "").strip()
        if not normalized_run_id:
            return {}
        with Session(self.engine) as session:
            run = session.get(Run, normalized_run_id)
            if run is None:
                return {}
            return _source_diagnostics_payload(run.source_diagnostics_json)

    def merge_run_source_diagnostics(
        self,
        *,
        run_id: str,
        diagnostics: list[dict[str, Any]],
    ) -> None:
        normalized_run_id = str(run_id or "").strip()
        if not normalized_run_id or not diagnostics:
            return
        with Session(self.engine) as session:
            run = session.get(Run, normalized_run_id)
            if run is None:
                return
            payload = _source_diagnostics_payload(run.source_diagnostics_json)
            _merge_window_diagnostics(payload=payload, diagnostics=diagnostics)
            run.source_diagnostics_json = _normalized_json(payload) or "{}"
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

    def record_metrics_batch(self, *, run_id: str, metrics: list[MetricPoint]) -> int:
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

    def record_workflow_step_receipt(
        self,
        *,
        request: WorkflowStepReceiptWriteRequest | None = None,
        **legacy_kwargs: Any,
    ) -> WorkflowStepReceipt | None:
        normalized_request = coerce_workflow_step_receipt_write_request(
            request=request,
            legacy_kwargs=legacy_kwargs,
        )
        receipt = workflow_step_receipt_from_write_request(normalized_request)
        if receipt is None:
            return None
        with Session(self.engine) as session:
            session.add(receipt)
            self._commit(session)
            session.refresh(receipt)
            return receipt

    def get_latest_workflow_step_receipt(
        self,
        *,
        request: WorkflowStepReceiptQuery | None = None,
        **legacy_kwargs: Any,
    ) -> WorkflowStepReceipt | None:
        query = coerce_workflow_step_receipt_query(
            request=request,
            legacy_kwargs=legacy_kwargs,
        )
        normalized_step_id = str(query.step_id or "").strip()
        normalized_config_fingerprint = str(query.config_fingerprint or "").strip()
        if not normalized_step_id or not normalized_config_fingerprint:
            return None
        with Session(self.engine) as session:
            statement = (
                select(WorkflowStepReceipt)
                .where(
                    WorkflowStepReceipt.step_id == normalized_step_id,
                    WorkflowStepReceipt.granularity
                    == _normalized_optional_text(query.granularity),
                    WorkflowStepReceipt.period_start == query.period_start,
                    WorkflowStepReceipt.period_end == query.period_end,
                    WorkflowStepReceipt.config_fingerprint
                    == normalized_config_fingerprint,
                    WorkflowStepReceipt.status
                    == (_normalized_optional_text(query.status) or "succeeded"),
                    WorkflowStepReceipt.selected_total
                    >= _nonnegative_int(query.min_selected_total),
                )
                .order_by(
                    desc(cast(Any, WorkflowStepReceipt.created_at)),
                    desc(cast(Any, WorkflowStepReceipt.id)),
                )
                .limit(1)
            )
            return session.exec(statement).first()


@dataclass(frozen=True, slots=True)
class WorkflowStepReceiptWriteRequest:
    run_id: str
    step_id: str
    granularity: str | None
    period_start: datetime | None
    period_end: datetime | None
    config_fingerprint: str
    requested_limit: int | None
    selected_total: int
    processed_total: int
    failed_total: int
    status: str = "succeeded"
    details: dict[str, Any] | None = None


@dataclass(frozen=True, slots=True)
class WorkflowStepReceiptQuery:
    step_id: str
    granularity: str | None
    period_start: datetime | None
    period_end: datetime | None
    config_fingerprint: str
    min_selected_total: int = 0
    status: str = "succeeded"


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
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True)
        if value is not None
        else None
    )


def _source_diagnostics_payload(value: str | None) -> dict[str, Any]:
    if not value:
        return {"sources": {}}
    try:
        loaded = json.loads(value)
    except Exception:
        return {"sources": {}}
    if not isinstance(loaded, dict):
        return {"sources": {}}
    sources = loaded.get("sources")
    if not isinstance(sources, dict):
        loaded["sources"] = {}
    return loaded


def _merge_window_diagnostics(
    *, payload: dict[str, Any], diagnostics: list[dict[str, Any]]
) -> None:
    for diagnostic in diagnostics:
        if not isinstance(diagnostic, dict):
            continue
        if str(diagnostic.get("kind") or "") != "pool_window_readiness":
            continue
        source_name = str(diagnostic.get("source") or "").strip().lower()
        if not source_name:
            source_name = "unknown"
        sources = payload.setdefault("sources", {})
        if not isinstance(sources, dict):
            sources = {}
            payload["sources"] = sources
        source_payload = sources.setdefault(source_name, {})
        if not isinstance(source_payload, dict):
            source_payload = {}
            sources[source_name] = source_payload
        ingest_payload = source_payload.setdefault("ingest", {})
        if not isinstance(ingest_payload, dict):
            ingest_payload = {}
            source_payload["ingest"] = ingest_payload
        _upsert_window_diagnostic(
            ingest_payload=ingest_payload,
            diagnostic=dict(diagnostic),
        )


def _upsert_window_diagnostic(
    *, ingest_payload: dict[str, Any], diagnostic: dict[str, Any]
) -> None:
    existing = ingest_payload.get("window_diagnostics")
    existing_entries = existing if isinstance(existing, list) else []
    by_key: dict[tuple[str, str, str, str, str, int], dict[str, Any]] = {}
    order: list[tuple[str, str, str, str, str, int]] = []
    for entry in existing_entries:
        if not isinstance(entry, dict):
            continue
        key = _window_diagnostic_identity(entry)
        if key is None:
            continue
        if key not in by_key:
            order.append(key)
        by_key[key] = dict(entry)
    key = _window_diagnostic_identity(diagnostic)
    if key is None:
        return
    if key not in by_key:
        order.append(key)
    by_key[key] = diagnostic
    ingest_payload["window_diagnostics"] = [by_key[key] for key in order]


def _window_diagnostic_identity(
    entry: dict[str, Any],
) -> tuple[str, str, str, str, str, int] | None:
    try:
        return (
            str(entry["source"]),
            str(entry["kind"]),
            str(entry["query_text"]),
            str(entry["period_start"]),
            str(entry["period_end"]),
            int(entry["max_results"]),
        )
    except Exception:
        return None


def coerce_workflow_step_receipt_write_request(
    *,
    request: WorkflowStepReceiptWriteRequest | None = None,
    legacy_kwargs: dict[str, Any],
) -> WorkflowStepReceiptWriteRequest:
    if request is not None:
        return request
    return WorkflowStepReceiptWriteRequest(
        run_id=legacy_kwargs["run_id"],
        step_id=legacy_kwargs["step_id"],
        granularity=legacy_kwargs["granularity"],
        period_start=legacy_kwargs["period_start"],
        period_end=legacy_kwargs["period_end"],
        config_fingerprint=legacy_kwargs["config_fingerprint"],
        requested_limit=legacy_kwargs["requested_limit"],
        selected_total=legacy_kwargs["selected_total"],
        processed_total=legacy_kwargs["processed_total"],
        failed_total=legacy_kwargs["failed_total"],
        status=legacy_kwargs.get("status", "succeeded"),
        details=legacy_kwargs.get("details"),
    )


def workflow_step_receipt_from_write_request(
    request: WorkflowStepReceiptWriteRequest,
) -> WorkflowStepReceipt | None:
    normalized_run_id = str(request.run_id or "").strip()
    normalized_step_id = str(request.step_id or "").strip()
    normalized_config_fingerprint = str(request.config_fingerprint or "").strip()
    if not normalized_run_id or not normalized_step_id or not normalized_config_fingerprint:
        return None
    return WorkflowStepReceipt(
        run_id=normalized_run_id,
        step_id=normalized_step_id,
        granularity=_normalized_optional_text(request.granularity),
        period_start=request.period_start,
        period_end=request.period_end,
        config_fingerprint=normalized_config_fingerprint,
        requested_limit=_optional_int(request.requested_limit),
        selected_total=_nonnegative_int(request.selected_total),
        processed_total=_nonnegative_int(request.processed_total),
        failed_total=_nonnegative_int(request.failed_total),
        status=_normalized_optional_text(request.status) or "succeeded",
        details_json=_normalized_json(
            request.details if isinstance(request.details, dict) else {}
        )
        or "{}",
    )


def coerce_workflow_step_receipt_query(
    *,
    request: WorkflowStepReceiptQuery | None = None,
    legacy_kwargs: dict[str, Any],
) -> WorkflowStepReceiptQuery:
    if request is not None:
        return request
    return WorkflowStepReceiptQuery(
        step_id=legacy_kwargs["step_id"],
        granularity=legacy_kwargs["granularity"],
        period_start=legacy_kwargs["period_start"],
        period_end=legacy_kwargs["period_end"],
        config_fingerprint=legacy_kwargs["config_fingerprint"],
        min_selected_total=legacy_kwargs.get("min_selected_total", 0),
        status=legacy_kwargs.get("status", "succeeded"),
    )


def _optional_int(value: int | None) -> int | None:
    return int(value) if value is not None else None


def _nonnegative_int(value: int | None) -> int:
    return max(0, int(value or 0))


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


def _run_context_updates(
    request: UpdateRunContextRequest,
) -> tuple[tuple[str, Any], ...]:
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
