from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Callable

from pydantic import BaseModel, ValidationError

from recoleta.analyzer import (
    _extract_token_counts,
    _extract_usage_dict,
    _get_completion,
    _resolve_response_cost_usd,
)
from recoleta.llm_connection import LLMConnectionConfig
from recoleta.prompt_style import reader_facing_ai_tropes_prompt

_TRANSLATION_LLM_MAX_ATTEMPTS = 3


class TranslationLLMOutputError(ValueError):
    def __init__(
        self,
        message: str,
        *,
        reason: str,
        finish_reason: str | None = None,
    ) -> None:
        super().__init__(message)
        self.reason = str(reason or "").strip().lower() or "unexpected"
        self.finish_reason = str(finish_reason or "").strip().lower() or None


@dataclass(frozen=True, slots=True)
class TranslationLLMRequest:
    model: str
    source_kind: str
    payload: dict[str, Any]
    source_language_code: str
    target_language_code: str
    source_language_label: str | None = None
    target_language_label: str | None = None
    context: dict[str, Any] | None = None
    payload_model: type[BaseModel] | None = None
    llm_connection: LLMConnectionConfig | None = None


@dataclass(frozen=True, slots=True)
class TranslationLLMDeps:
    completion_factory: Callable[[], Any] | None = None
    extract_usage_dict_fn: Callable[[object], dict[str, Any] | None] | None = None
    extract_token_counts_fn: (
        Callable[[dict[str, Any] | None], tuple[int | None, int | None, int | None]]
        | None
    ) = None
    extract_content_fn: Callable[[object], Any] | None = None
    resolve_response_cost_usd_fn: Callable[..., float | None] | None = None


def coerce_payload_dict(
    payload: BaseModel | dict[str, Any] | Any,
    *,
    payload_model: type[BaseModel] | None,
) -> dict[str, Any]:
    if isinstance(payload, BaseModel):
        return payload.model_dump(mode="json")
    if payload_model is not None:
        return payload_model.model_validate(payload).model_dump(mode="json")
    if not isinstance(payload, dict):
        raise ValueError("translated payload must be a JSON object")
    return payload


def build_translation_system_message() -> str:
    base = (
        "You translate structured Recoleta research outputs between languages. "
        "Return strict JSON only. Preserve the input JSON shape exactly. "
        "Do not add or remove keys, do not reorder arrays unnecessarily, and do not invent facts. "
        "Translate only natural-language prose. Preserve URLs, markdown link targets, ids, timestamps, "
        "topic slugs, enum-like tokens, doc references, and evidence refs exactly."
    )
    guardrail = (
        "When multiple target-language phrasings are equally faithful, choose the most direct, "
        "least rhetorical, least templated phrasing. Do not use this freedom to change claims, "
        "add or remove facts, reorder arrays, or alter JSON structure."
    )
    return "\n\n".join([base, reader_facing_ai_tropes_prompt(), guardrail])


def translate_structured_payload_with_debug(
    request: TranslationLLMRequest,
    deps: TranslationLLMDeps | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    normalized_model = str(request.model or "").strip()
    if not normalized_model:
        raise ValueError("model must not be empty")
    normalized_payload = coerce_payload_dict(
        request.payload,
        payload_model=request.payload_model,
    )
    aggregated_debug: dict[str, Any] = {}
    retry_attempts: list[dict[str, Any]] = []
    for attempt in range(1, _TRANSLATION_LLM_MAX_ATTEMPTS + 1):
        response = _invoke_translation_completion(
            request=request,
            normalized_model=normalized_model,
            normalized_payload=normalized_payload,
            deps=deps,
        )
        raw_content, attempt_debug = _extract_translation_response_payload(
            response=response,
            normalized_model=normalized_model,
            deps=deps,
        )
        _merge_translation_debug(aggregated=aggregated_debug, attempt=attempt_debug)
        try:
            decoded_payload = _decode_translation_content(
                raw_content=raw_content,
                finish_reason=(
                    str(attempt_debug.get("finish_reason") or "").strip().lower()
                    or None
                ),
            )
            translated_payload = _validated_translated_payload(
                decoded=decoded_payload,
                payload_model=request.payload_model,
                finish_reason=(
                    str(attempt_debug.get("finish_reason") or "").strip().lower()
                    or None
                ),
            )
        except ValueError as exc:
            if (
                _is_retryable_translation_output_error(exc)
                and attempt < _TRANSLATION_LLM_MAX_ATTEMPTS
            ):
                retry_attempts.append(
                    {
                        "attempt": attempt,
                        "error_type": type(exc).__name__,
                        "error": str(exc),
                        "reason": getattr(exc, "reason", None),
                        "finish_reason": getattr(exc, "finish_reason", None),
                    }
                )
                continue
            raise
        if retry_attempts:
            aggregated_debug["retry"] = {
                "attempts": retry_attempts,
                "attempts_total": len(retry_attempts) + 1,
            }
        return translated_payload, aggregated_debug
    raise RuntimeError("translation attempts exhausted unexpectedly")


def _invoke_translation_completion(
    *,
    request: TranslationLLMRequest,
    normalized_model: str,
    normalized_payload: dict[str, Any],
    deps: TranslationLLMDeps | None,
) -> Any:
    completion = (
        deps.completion_factory if deps is not None else None
    ) or _get_completion
    connection = request.llm_connection or LLMConnectionConfig()
    return completion()(
        model=normalized_model,
        messages=_translation_messages(
            request=request,
            normalized_payload=normalized_payload,
        ),
        response_format={"type": "json_object"},
        **connection.litellm_completion_kwargs(),
    )


def _translation_messages(
    *,
    request: TranslationLLMRequest,
    normalized_payload: dict[str, Any],
) -> list[dict[str, str]]:
    source_label = str(
        request.source_language_label or request.source_language_code
    ).strip()
    target_label = str(
        request.target_language_label or request.target_language_code
    ).strip()
    context_payload = request.context if isinstance(request.context, dict) else {}
    user_message = (
        f"Translate this {request.source_kind} payload from {source_label} to {target_label}.\n\n"
        "Rules:\n"
        "- Keep markdown structure valid inside translated string values.\n"
        "- Preserve topics/tags/kind/time_horizon/change_type/doc_id/chunk_index values unless they are clearly prose.\n"
        "- Keep JSON keys in English exactly as provided.\n"
        "- Return one JSON object only.\n\n"
        "Context JSON:\n"
        f"{json.dumps(context_payload, ensure_ascii=False, sort_keys=True)}\n\n"
        "Payload JSON:\n"
        f"{json.dumps(normalized_payload, ensure_ascii=False, sort_keys=True)}"
    )
    return [
        {"role": "system", "content": build_translation_system_message()},
        {"role": "user", "content": user_message},
    ]


def _extract_translation_response_payload(
    *,
    response: Any,
    normalized_model: str,
    deps: TranslationLLMDeps | None,
) -> tuple[Any, dict[str, Any]]:
    extract_usage_dict = (
        deps.extract_usage_dict_fn if deps is not None else None
    ) or _extract_usage_dict
    extract_token_counts = (
        deps.extract_token_counts_fn if deps is not None else None
    ) or _extract_token_counts
    extract_content = (
        deps.extract_content_fn if deps is not None else None
    ) or _extract_translation_message_content
    resolve_response_cost_usd = (
        deps.resolve_response_cost_usd_fn if deps is not None else None
    ) or _resolve_response_cost_usd
    usage = extract_usage_dict(response)
    prompt_tokens, completion_tokens, total_tokens = extract_token_counts(usage)
    cost_usd = resolve_response_cost_usd(
        response=response,
        model=normalized_model,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
    )
    raw_content = extract_content(response)
    return raw_content, {
        "usage": _debug_usage(
            usage=usage,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
        ),
        "estimated_cost_usd": cost_usd,
        "finish_reason": _extract_translation_finish_reason(response),
    }


def _decode_translation_content(
    *,
    raw_content: Any,
    finish_reason: str | None,
) -> Any:
    normalized_finish_reason = str(finish_reason or "").strip().lower() or None
    if normalized_finish_reason == "content_filter":
        raise TranslationLLMOutputError(
            "translation LLM response was content-filtered",
            reason="content_filter",
            finish_reason=normalized_finish_reason,
        )
    normalized_content = _normalized_translation_content_text(raw_content)
    if not normalized_content:
        raise TranslationLLMOutputError(
            "translation LLM returned empty content",
            reason="empty_content",
            finish_reason=normalized_finish_reason,
        )
    try:
        return json.loads(normalized_content)
    except json.JSONDecodeError as exc:
        raise TranslationLLMOutputError(
            f"translation LLM returned invalid JSON: {exc.msg}",
            reason="invalid_json",
            finish_reason=normalized_finish_reason,
        ) from exc


def _validated_translated_payload(
    *,
    decoded: Any,
    payload_model: type[BaseModel] | None,
    finish_reason: str | None,
) -> dict[str, Any]:
    normalized_finish_reason = str(finish_reason or "").strip().lower() or None
    if payload_model is not None:
        try:
            return payload_model.model_validate(decoded).model_dump(mode="json")
        except ValidationError as exc:
            raise TranslationLLMOutputError(
                f"translation LLM returned JSON with invalid schema: {type(exc).__name__}",
                reason="invalid_schema",
                finish_reason=normalized_finish_reason,
            ) from exc
    if not isinstance(decoded, dict):
        raise TranslationLLMOutputError(
            "translation LLM returned a non-object JSON payload",
            reason="non_object_json",
            finish_reason=normalized_finish_reason,
        )
    return decoded


def _is_retryable_translation_output_error(exc: ValueError) -> bool:
    if isinstance(exc, TranslationLLMOutputError):
        return True
    message = str(exc)
    return message.startswith("translation LLM returned ")


def _merge_translation_debug(
    *, aggregated: dict[str, Any], attempt: dict[str, Any]
) -> None:
    usage = attempt.get("usage")
    if isinstance(usage, dict):
        aggregated_usage = aggregated.setdefault("usage", {})
        if not isinstance(aggregated_usage, dict):
            aggregated_usage = {}
            aggregated["usage"] = aggregated_usage
        for key in ("requests", "input_tokens", "output_tokens", "total_tokens"):
            value = usage.get(key)
            if isinstance(value, (int, float)):
                aggregated_usage[key] = float(aggregated_usage.get(key) or 0) + float(
                    value
                )
        cost = usage.get("cost")
        if isinstance(cost, (int, float)):
            aggregated_usage["cost"] = float(aggregated_usage.get("cost") or 0) + float(
                cost
            )
        cost_details = usage.get("cost_details")
        if isinstance(cost_details, dict):
            aggregated_usage["cost_details"] = dict(cost_details)
    estimated_cost_usd = attempt.get("estimated_cost_usd")
    if isinstance(estimated_cost_usd, (int, float)):
        aggregated["estimated_cost_usd"] = float(
            aggregated.get("estimated_cost_usd") or 0.0
        ) + float(estimated_cost_usd)
    finish_reason = str(attempt.get("finish_reason") or "").strip().lower()
    if finish_reason:
        aggregated["finish_reason"] = finish_reason


def _debug_usage(
    *,
    usage: dict[str, Any] | None,
    prompt_tokens: int | None,
    completion_tokens: int | None,
    total_tokens: int | None,
) -> dict[str, Any]:
    debug_usage: dict[str, Any] = {"requests": 1}
    if prompt_tokens is not None:
        debug_usage["input_tokens"] = prompt_tokens
    if completion_tokens is not None:
        debug_usage["output_tokens"] = completion_tokens
    if total_tokens is not None:
        debug_usage["total_tokens"] = total_tokens
    if isinstance(usage, dict):
        if "cost" in usage:
            debug_usage["cost"] = usage["cost"]
        cost_details = usage.get("cost_details")
        if isinstance(cost_details, dict):
            debug_usage["cost_details"] = cost_details
    return debug_usage


def _extract_translation_message_content(response: object) -> Any:
    if isinstance(response, dict):
        choices = response.get("choices") or []
        if not choices:
            return None
        first_choice = choices[0] or {}
        message = first_choice.get("message") or {}
        if isinstance(message, dict):
            return message.get("content")
        return getattr(message, "content", None)
    choices = getattr(response, "choices")
    first_choice = choices[0]
    return getattr(first_choice.message, "content", None)


def _extract_translation_finish_reason(response: object) -> str | None:
    if isinstance(response, dict):
        choices = response.get("choices") or []
        if not choices:
            return None
        return str((choices[0] or {}).get("finish_reason") or "").strip() or None
    choices = getattr(response, "choices")
    first_choice = choices[0]
    return str(getattr(first_choice, "finish_reason", "") or "").strip() or None


def _normalized_translation_content_text(raw_content: Any) -> str | None:
    if raw_content is None:
        return None
    if isinstance(raw_content, str):
        normalized = raw_content.strip()
        return normalized or None
    if isinstance(raw_content, list):
        return _normalized_translation_content_list_text(raw_content)
    normalized = str(raw_content).strip()
    return normalized or None


def _normalized_translation_content_list_text(parts: list[Any]) -> str | None:
    normalized_parts = [
        normalized_part
        for part in parts
        if (normalized_part := _normalized_translation_content_part_text(part))
        is not None
    ]
    if not normalized_parts:
        return None
    joined = "".join(normalized_parts).strip()
    return joined or None


def _normalized_translation_content_part_text(part: Any) -> str | None:
    if not isinstance(part, dict):
        return None
    if part.get("type") != "output_text":
        return None
    text_value = part.get("text")
    if isinstance(text_value, str) and text_value:
        return text_value
    normalized = str(text_value or "").strip()
    return normalized or None
