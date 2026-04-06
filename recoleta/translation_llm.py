from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Callable

from pydantic import BaseModel, ValidationError

from recoleta.analyzer import (
    _extract_content,
    _extract_token_counts,
    _extract_usage_dict,
    _get_completion,
    _resolve_response_cost_usd,
)
from recoleta.llm_connection import LLMConnectionConfig
from recoleta.prompt_style import reader_facing_ai_tropes_prompt


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
    extract_content_fn: Callable[[object], str] | None = None
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
    response = _invoke_translation_completion(
        request=request,
        normalized_model=normalized_model,
        normalized_payload=normalized_payload,
        deps=deps,
    )
    decoded_payload, debug = _decode_translation_response(
        response=response,
        request=request,
        normalized_model=normalized_model,
        deps=deps,
    )
    return _validated_translated_payload(
        decoded=decoded_payload,
        payload_model=request.payload_model,
    ), debug


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


def _decode_translation_response(
    *,
    response: Any,
    request: TranslationLLMRequest,
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
    ) or _extract_content
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
    try:
        decoded = json.loads(raw_content)
    except json.JSONDecodeError as exc:
        raise ValueError(f"translation LLM returned invalid JSON: {exc.msg}") from exc
    return decoded, {
        "usage": _debug_usage(
            usage=usage,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
        ),
        "estimated_cost_usd": cost_usd,
    }


def _validated_translated_payload(
    *,
    decoded: Any,
    payload_model: type[BaseModel] | None,
) -> dict[str, Any]:
    if payload_model is not None:
        try:
            return payload_model.model_validate(decoded).model_dump(mode="json")
        except ValidationError as exc:
            raise ValueError(
                f"translation LLM returned JSON with invalid schema: {type(exc).__name__}"
            ) from exc
    if not isinstance(decoded, dict):
        raise ValueError("translation LLM returned a non-object JSON payload")
    return decoded


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
