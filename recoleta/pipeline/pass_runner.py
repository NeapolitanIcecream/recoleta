from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Generic, Sequence, TypeVar

from recoleta.passes.base import PassOutputEnvelope
from recoleta.pipeline.projections import run_projection_target

T = TypeVar("T")
S = TypeVar("S")


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


@dataclass(slots=True)
class PassPersistSpec:
    envelope: PassOutputEnvelope
    period_start: datetime | None
    period_end: datetime | None
    log: Any
    failure_message: str
    warning_context: dict[str, Any] = field(default_factory=dict)
    sanitize_error: Callable[[str], str] | None = None
    on_failure: Callable[[BaseException], None] | None = None
    failed_metric_name: str = "pipeline.trends.pass_outputs.persist_failed_total"
    persisted_metric_name: str | None = None
    reraise: bool = True


@dataclass(slots=True)
class PassDefinition(Generic[S]):
    persist: PassPersistSpec
    prepare_projection_state: Callable[[int | None], S] | None = None
    build_projection_specs: Callable[
        [int | None, S | None], Sequence[ProjectionSpec]
    ] | None = None
    should_project: bool | Callable[[int | None, S | None], bool] = True
    allow_projection_without_pass_output: bool = False


@dataclass(slots=True)
class PassExecutionResult(Generic[S]):
    pass_output_id: int | None
    projection_state: S | None = None
    projection_results: dict[str, Any | None] = field(default_factory=dict)


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


def run_pass_definition(
    *,
    repository: Any,
    record_metric: Callable[..., None],
    definition: PassDefinition[S],
) -> PassExecutionResult[S]:
    persist = definition.persist
    pass_output_id = persist_pass_output_envelope(
        repository=repository,
        envelope=persist.envelope,
        period_start=persist.period_start,
        period_end=persist.period_end,
        record_metric=record_metric,
        log=persist.log,
        failure_message=persist.failure_message,
        warning_context=persist.warning_context,
        sanitize_error=persist.sanitize_error,
        on_failure=persist.on_failure,
        failed_metric_name=persist.failed_metric_name,
        persisted_metric_name=persist.persisted_metric_name,
        reraise=persist.reraise,
    )

    projection_state = (
        definition.prepare_projection_state(pass_output_id)
        if callable(definition.prepare_projection_state)
        else None
    )

    if callable(definition.should_project):
        should_project = bool(definition.should_project(pass_output_id, projection_state))
    else:
        should_project = bool(definition.should_project)
    can_project = bool(
        pass_output_id is not None or definition.allow_projection_without_pass_output
    )
    if not should_project or not can_project or not callable(definition.build_projection_specs):
        return PassExecutionResult(
            pass_output_id=pass_output_id,
            projection_state=projection_state,
        )

    projection_results = run_projection_specs(
        record_metric=record_metric,
        specs=definition.build_projection_specs(pass_output_id, projection_state),
    )
    return PassExecutionResult(
        pass_output_id=pass_output_id,
        projection_state=projection_state,
        projection_results=projection_results,
    )


__all__ = [
    "PassDefinition",
    "PassExecutionResult",
    "PassPersistSpec",
    "ProjectionSpec",
    "persist_pass_output_envelope",
    "run_pass_definition",
    "run_projection_specs",
]
