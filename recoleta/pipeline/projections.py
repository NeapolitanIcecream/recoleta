from __future__ import annotations

from typing import Any, Callable, TypeVar

T = TypeVar("T")


def run_projection_target(
    *,
    enabled: bool,
    metric_base: str,
    record_metric: Callable[..., None],
    log: Any,
    failure_message: str,
    execute: Callable[[], T],
    warning_context: dict[str, Any] | None = None,
    sanitize_error: Callable[[str], str] | None = None,
) -> T | None:
    if not enabled:
        return None
    try:
        result = execute()
    except Exception as exc:  # noqa: BLE001
        record_metric(name=f"{metric_base}.failed_total", value=1, unit="count")
        log.warning(
            failure_message,
            **{
                **(warning_context or {}),
                "error_type": type(exc).__name__,
                "error": (
                    sanitize_error(str(exc))
                    if callable(sanitize_error)
                    else str(exc)
                ),
            },
        )
        raise
    record_metric(name=f"{metric_base}.emitted_total", value=1, unit="count")
    return result


__all__ = ["run_projection_target"]
