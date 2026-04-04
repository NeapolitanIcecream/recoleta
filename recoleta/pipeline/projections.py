from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

T = TypeVar("T")


@dataclass(slots=True)
class ProjectionSpec(Generic[T]):
    name: str
    enabled: bool
    metric_base: str
    log: Any
    failure_message: str
    execute: Callable[[], T]
    warning_context: dict[str, Any] = field(default_factory=dict)
    sanitize_error: Callable[[str], str] | None = None
    reraise: bool = True


def run_projection_target(
    *,
    spec: ProjectionSpec[T],
    record_metric: Callable[..., None],
) -> T | None:
    if not spec.enabled:
        return None
    try:
        result = spec.execute()
    except Exception as exc:  # noqa: BLE001
        record_metric(name=f"{spec.metric_base}.failed_total", value=1, unit="count")
        spec.log.warning(
            spec.failure_message,
            **_projection_warning_payload(spec=spec, exc=exc),
        )
        if spec.reraise:
            raise
        return None
    record_metric(name=f"{spec.metric_base}.emitted_total", value=1, unit="count")
    return result


def _projection_warning_payload(
    *,
    spec: ProjectionSpec[Any],
    exc: BaseException,
) -> dict[str, Any]:
    return {
        **spec.warning_context,
        "error_type": type(exc).__name__,
        "error": (
            spec.sanitize_error(str(exc))
            if callable(spec.sanitize_error)
            else str(exc)
        ),
    }


__all__ = ["ProjectionSpec", "run_projection_target"]
