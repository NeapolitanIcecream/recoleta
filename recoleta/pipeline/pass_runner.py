from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Sequence, TypeVar

from recoleta.passes.base import PassOutputEnvelope
from recoleta.pipeline.projections import run_projection_target

T = TypeVar("T")


@dataclass(slots=True)
class ProjectionSpec:
    name: str
    enabled: bool
    metric_base: str
    log: Any
    failure_message: str
    execute: Callable[[], Any]
    warning_context: dict[str, Any] = field(default_factory=dict)
    sanitize_error: Callable[[str], str] | None = None
    reraise: bool = True


def run_projection_specs(
    *,
    specs: Sequence[ProjectionSpec],
    record_metric: Callable[..., None],
) -> dict[str, Any | None]:
    results: dict[str, Any | None] = {}
    for spec in specs:
        results[spec.name] = run_projection_target(
            enabled=spec.enabled,
            metric_base=spec.metric_base,
            record_metric=record_metric,
            log=spec.log,
            failure_message=spec.failure_message,
            execute=spec.execute,
            warning_context=spec.warning_context,
            sanitize_error=spec.sanitize_error,
            reraise=spec.reraise,
        )
    return results


def persist_pass_output_envelope(
    *,
    repository: Any,
    envelope: PassOutputEnvelope,
    period_start: datetime | None,
    period_end: datetime | None,
    record_metric: Callable[..., None],
    log: Any,
    failure_message: str,
    warning_context: dict[str, Any] | None = None,
    sanitize_error: Callable[[str], str] | None = None,
    on_failure: Callable[[BaseException], None] | None = None,
    failed_metric_name: str = "pipeline.trends.pass_outputs.persist_failed_total",
    persisted_metric_name: str | None = None,
    reraise: bool = True,
) -> int | None:
    try:
        row = repository.create_pass_output(
            run_id=envelope.run_id,
            pass_kind=envelope.pass_kind,
            status=envelope.status.value,
            scope=envelope.scope,
            granularity=envelope.granularity,
            period_start=period_start,
            period_end=period_end,
            schema_version=envelope.schema_version,
            payload=envelope.payload,
            diagnostics=envelope.diagnostics,
            input_refs=[ref.model_dump(mode="json") for ref in envelope.input_refs],
        )
        pass_output_id = int(getattr(row, "id") or 0)
        if pass_output_id <= 0:
            raise RuntimeError("pass output persistence returned an empty id")
    except Exception as exc:  # noqa: BLE001
        if callable(on_failure):
            on_failure(exc)
        if str(failed_metric_name or "").strip():
            record_metric(name=failed_metric_name, value=1, unit="count")
        log.warning(
            failure_message,
            **{
                **(warning_context or {}),
                "pass_kind": envelope.pass_kind,
                "error_type": type(exc).__name__,
                "error": (
                    sanitize_error(str(exc))
                    if callable(sanitize_error)
                    else str(exc)
                ),
            },
        )
        if reraise:
            raise
        return None

    if str(persisted_metric_name or "").strip():
        record_metric(name=str(persisted_metric_name), value=1, unit="count")
    return pass_output_id


__all__ = [
    "ProjectionSpec",
    "persist_pass_output_envelope",
    "run_projection_specs",
]
