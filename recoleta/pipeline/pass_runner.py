from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Generic, Sequence, TypeVar

from recoleta.passes.base import PassOutputEnvelope
from recoleta.pipeline.projections import ProjectionSpec, run_projection_target

T = TypeVar("T")
S = TypeVar("S")


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
    build_projection_specs: (
        Callable[[int | None, S | None], Sequence[ProjectionSpec]] | None
    ) = None
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
            spec=spec,
            record_metric=record_metric,
        )
    return results


def persist_pass_output_envelope(
    *,
    repository: Any,
    record_metric: Callable[..., None],
    spec: PassPersistSpec,
) -> int | None:
    try:
        row = repository.create_pass_output(
            run_id=spec.envelope.run_id,
            pass_kind=spec.envelope.pass_kind,
            status=spec.envelope.status.value,
            granularity=spec.envelope.granularity,
            period_start=spec.period_start,
            period_end=spec.period_end,
            schema_version=spec.envelope.schema_version,
            payload=spec.envelope.payload,
            diagnostics=spec.envelope.diagnostics,
            input_refs=[
                ref.model_dump(mode="json") for ref in spec.envelope.input_refs
            ],
        )
        pass_output_id = int(getattr(row, "id") or 0)
        if pass_output_id <= 0:
            raise RuntimeError("pass output persistence returned an empty id")
    except Exception as exc:  # noqa: BLE001
        if callable(spec.on_failure):
            spec.on_failure(exc)
        if str(spec.failed_metric_name or "").strip():
            record_metric(name=spec.failed_metric_name, value=1, unit="count")
        spec.log.warning(
            spec.failure_message,
            **_pass_persist_warning_payload(spec=spec, exc=exc),
        )
        if spec.reraise:
            raise
        return None

    if str(spec.persisted_metric_name or "").strip():
        record_metric(name=str(spec.persisted_metric_name), value=1, unit="count")
    return pass_output_id


def _pass_persist_warning_payload(
    *,
    spec: PassPersistSpec,
    exc: BaseException,
) -> dict[str, Any]:
    return {
        **spec.warning_context,
        "pass_kind": spec.envelope.pass_kind,
        "error_type": type(exc).__name__,
        "error": (
            spec.sanitize_error(str(exc)) if callable(spec.sanitize_error) else str(exc)
        ),
    }


def run_pass_definition(
    *,
    repository: Any,
    record_metric: Callable[..., None],
    definition: PassDefinition[S],
) -> PassExecutionResult[S]:
    persist = definition.persist
    pass_output_id = persist_pass_output_envelope(
        repository=repository,
        record_metric=record_metric,
        spec=persist,
    )

    projection_state = (
        definition.prepare_projection_state(pass_output_id)
        if callable(definition.prepare_projection_state)
        else None
    )

    if callable(definition.should_project):
        should_project = bool(
            definition.should_project(pass_output_id, projection_state)
        )
    else:
        should_project = bool(definition.should_project)
    can_project = bool(
        pass_output_id is not None or definition.allow_projection_without_pass_output
    )
    if (
        not should_project
        or not can_project
        or not callable(definition.build_projection_specs)
    ):
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
