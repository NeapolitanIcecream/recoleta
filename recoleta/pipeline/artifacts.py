from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx
import orjson
from loguru import logger

from recoleta.observability import scrub_secrets


def sanitize_error_message(*, message: str, secrets: tuple[str, ...]) -> str:
    return scrub_secrets(message, secrets=secrets)


def classify_exception(exc: BaseException) -> dict[str, Any]:
    if isinstance(exc, httpx.HTTPStatusError):
        status = int(getattr(getattr(exc, "response", None), "status_code", 0) or 0)
        if status in {401, 403}:
            return {
                "error_category": "auth",
                "retryable": True,
                "http_status": status,
            }
        return {
            "error_category": "http_status",
            "retryable": status >= 500 or status == 429,
            "http_status": status,
        }
    if isinstance(exc, httpx.RequestError):
        return {"error_category": "http_request", "retryable": True}
    if isinstance(exc, ValueError):
        return {"error_category": "validation", "retryable": False}
    return {"error_category": "unknown", "retryable": False}


def _message_excerpt(value: Any, *, max_len: int = 240) -> str | None:
    normalized = " ".join(str(value or "").split())
    if not normalized:
        return None
    if len(normalized) <= max_len:
        return normalized
    return normalized[: max_len - 3].rstrip() + "..."


@dataclass(frozen=True, slots=True)
class DebugArtifactWriteRequest:
    settings: Any
    scrub_secrets_values: tuple[str, ...]
    run_id: str
    item_id: int | None
    kind: str
    payload: dict[str, Any]


def _artifact_summary_source(
    *,
    kind: str,
    payload: dict[str, Any],
) -> dict[str, Any] | None:
    if not isinstance(payload, dict):
        return None
    if str(kind or "").strip() != "pass_output_failure":
        return payload
    nested = payload.get("failure")
    return nested if isinstance(nested, dict) else None


def _summary_text_value(source: dict[str, Any], *, key: str) -> str | None:
    normalized = str(source.get(key) or "").strip()
    return normalized or None


def _summary_positive_int(source: dict[str, Any], *, key: str) -> int | None:
    value = source.get(key)
    return value if isinstance(value, int) and value > 0 else None


def summarize_artifact_payload(
    *,
    kind: str,
    payload: dict[str, Any],
) -> dict[str, Any] | None:
    source = _artifact_summary_source(kind=kind, payload=payload)
    if not source:
        return None

    summary: dict[str, Any] = {}
    if error_type := _summary_text_value(source, key="error_type"):
        summary["error_type"] = error_type
    if error_category := _summary_text_value(source, key="error_category"):
        summary["error_category"] = error_category
    retryable = source.get("retryable")
    if isinstance(retryable, bool):
        summary["retryable"] = retryable
    if http_status := _summary_positive_int(source, key="http_status"):
        summary["http_status"] = http_status
    message_excerpt = _message_excerpt(source.get("error_message"))
    if message_excerpt is not None:
        summary["message_excerpt"] = message_excerpt
    return summary or None


def _coerce_debug_artifact_write_request(
    *,
    request: DebugArtifactWriteRequest | None = None,
    legacy_kwargs: dict[str, Any] | None = None,
) -> DebugArtifactWriteRequest:
    if request is not None:
        return request
    values = dict(legacy_kwargs or {})
    return DebugArtifactWriteRequest(
        settings=values["settings"],
        scrub_secrets_values=tuple(values["scrub_secrets_values"]),
        run_id=str(values["run_id"]),
        item_id=values.get("item_id"),
        kind=str(values["kind"]),
        payload=dict(values["payload"]),
    )


def _sanitize_artifact_segment(
    value: str,
    *,
    max_len: int = 72,
    fallback: str = "unknown",
) -> str:
    cleaned = value.strip()
    normalized = "".join(
        ch if (ch.isalnum() or ch in {"-", "_"}) else "_" for ch in cleaned
    )
    while "__" in normalized:
        normalized = normalized.replace("__", "_")
    normalized = normalized.strip("_")
    if not normalized:
        return fallback
    return normalized[:max_len]


def _artifact_relative_path(*, run_id: str, item_id: int | None, kind: str) -> Path:
    safe_run_id = _sanitize_artifact_segment(run_id, fallback="run")
    safe_kind = _sanitize_artifact_segment(kind, fallback="artifact")
    item_segment = str(item_id) if item_id is not None else "no-item"
    kind_to_name = {
        "error_context": "error-context.json",
        "llm_request": "llm-request.json",
        "llm_response": "llm-response.json",
        "embedding_request": "embedding-request.json",
        "embedding_response": "embedding-response.json",
        "triage_summary": "triage-summary.json",
    }
    file_name = kind_to_name.get(kind, f"{safe_kind.replace('_', '-')}.json")
    return Path(safe_run_id) / item_segment / file_name


def _resolve_artifact_output_path(*, settings: Any, relative_path: Path) -> Path:
    base_dir = settings.artifacts_dir.expanduser().resolve()
    absolute_path = (base_dir / relative_path).resolve()
    if not absolute_path.is_relative_to(base_dir):
        raise ValueError("Debug artifact path escapes artifacts_dir")
    absolute_path.parent.mkdir(parents=True, exist_ok=True)
    return absolute_path


def _scrubbed_artifact_json(
    *,
    payload: dict[str, Any],
    secrets: tuple[str, ...],
) -> str:
    raw_json = orjson.dumps(payload, option=orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS)
    return scrub_secrets(
        raw_json.decode("utf-8"),
        secrets=secrets,
    )


def write_debug_artifact(
    *,
    request: DebugArtifactWriteRequest | None = None,
    **legacy_kwargs: Any,
) -> Path | None:
    normalized_request = _coerce_debug_artifact_write_request(
        request=request,
        legacy_kwargs=legacy_kwargs,
    )
    settings = normalized_request.settings
    if not settings.write_debug_artifacts or settings.artifacts_dir is None:
        return None
    try:
        relative_path = _artifact_relative_path(
            run_id=normalized_request.run_id,
            item_id=normalized_request.item_id,
            kind=normalized_request.kind,
        )
        absolute_path = _resolve_artifact_output_path(
            settings=settings,
            relative_path=relative_path,
        )
        scrubbed = _scrubbed_artifact_json(
            payload=normalized_request.payload,
            secrets=normalized_request.scrub_secrets_values,
        )
        absolute_path.write_text(scrubbed + "\n", encoding="utf-8")
        return relative_path
    except Exception as exc:
        logger.bind(
            module="pipeline.artifacts",
            run_id=normalized_request.run_id,
            item_id=normalized_request.item_id,
        ).warning(
            "Debug artifact write failed: {}",
            sanitize_error_message(
                message=str(exc),
                secrets=normalized_request.scrub_secrets_values,
            ),
        )
        return None
