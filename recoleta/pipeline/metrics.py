from __future__ import annotations

from typing import Any

from recoleta.types import DEFAULT_TOPIC_STREAM


def metric_token(value: str, *, max_len: int = 48) -> str:
    lowered = value.lower().strip()
    if not lowered:
        return "unknown"
    normalized = "".join(ch if ch.isalnum() else "_" for ch in lowered)
    while "__" in normalized:
        normalized = normalized.replace("__", "_")
    normalized = normalized.strip("_")
    if not normalized:
        return "unknown"
    return normalized[:max_len]


def stream_metric_name(*, stage: str, stream: str, suffix: str) -> str:
    stream_token = metric_token(stream, max_len=32)
    return f"pipeline.{stage}.stream.{stream_token}.{suffix}"


def record_stream_metric(
    *,
    repository: Any,
    run_id: str,
    stage: str,
    stream: str,
    suffix: str,
    value: float,
    unit: str,
) -> None:
    repository.record_metric(
        run_id=run_id,
        name=stream_metric_name(stage=stage, stream=stream, suffix=suffix),
        value=value,
        unit=unit,
    )


def scoped_trends_metric_name(name: str, *, scope: str) -> str:
    normalized_name = str(name or "").strip()
    normalized_scope = str(scope or "").strip() or DEFAULT_TOPIC_STREAM
    if normalized_scope == DEFAULT_TOPIC_STREAM:
        return normalized_name
    stream_prefix = f"pipeline.trends.stream.{metric_token(normalized_scope, max_len=32)}"
    if normalized_name == "pipeline.trends":
        return stream_prefix
    if not normalized_name.startswith("pipeline.trends."):
        return normalized_name
    suffix = normalized_name.removeprefix("pipeline.trends.")
    return f"{stream_prefix}.{suffix}"
