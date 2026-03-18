from __future__ import annotations

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


def summarize_artifact_payload(
    *,
    kind: str,
    payload: dict[str, Any],
) -> dict[str, Any] | None:
    source: dict[str, Any] | None = payload if isinstance(payload, dict) else None
    if str(kind or "").strip() == "pass_output_failure":
        nested = payload.get("failure") if isinstance(payload, dict) else None
        source = nested if isinstance(nested, dict) else None
    if not source:
        return None

    summary: dict[str, Any] = {}
    error_type = str(source.get("error_type") or "").strip()
    if error_type:
        summary["error_type"] = error_type
    error_category = str(source.get("error_category") or "").strip()
    if error_category:
        summary["error_category"] = error_category
    retryable = source.get("retryable")
    if isinstance(retryable, bool):
        summary["retryable"] = retryable
    http_status = source.get("http_status")
    if isinstance(http_status, int) and http_status > 0:
        summary["http_status"] = http_status
    message_excerpt = _message_excerpt(source.get("error_message"))
    if message_excerpt is not None:
        summary["message_excerpt"] = message_excerpt
    return summary or None


def write_debug_artifact(
    *,
    settings: Any,
    scrub_secrets_values: tuple[str, ...],
    run_id: str,
    item_id: int | None,
    kind: str,
    payload: dict[str, Any],
) -> Path | None:
    if not settings.write_debug_artifacts or settings.artifacts_dir is None:
        return None
    try:

        def sanitize_segment(
            value: str, *, max_len: int = 72, fallback: str = "unknown"
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

        safe_run_id = sanitize_segment(run_id, fallback="run")
        safe_kind = sanitize_segment(kind, fallback="artifact")
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
        relative_path = Path(safe_run_id) / item_segment / file_name

        base_dir = settings.artifacts_dir.expanduser().resolve()
        absolute_path = (base_dir / relative_path).resolve()
        if not absolute_path.is_relative_to(base_dir):
            raise ValueError("Debug artifact path escapes artifacts_dir")
        absolute_path.parent.mkdir(parents=True, exist_ok=True)

        raw_json = orjson.dumps(payload, option=orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS)
        scrubbed = scrub_secrets(
            raw_json.decode("utf-8"),
            secrets=scrub_secrets_values,
        )
        absolute_path.write_text(scrubbed + "\n", encoding="utf-8")
        return absolute_path.relative_to(base_dir)
    except Exception as exc:
        logger.bind(module="pipeline.artifacts", run_id=run_id, item_id=item_id).warning(
            "Debug artifact write failed: {}",
            sanitize_error_message(message=str(exc), secrets=scrub_secrets_values),
        )
        return None
