from __future__ import annotations

from collections.abc import Iterator
from typing import Any


def _coerce_float(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if value is None:
        return None
    try:
        return float(value)
    except Exception:
        return None


def _get_value(obj: Any, key: str) -> Any:
    if isinstance(obj, dict):
        return obj.get(key)
    return getattr(obj, key, None)


def extract_measured_cost_usd(response: object) -> float | None:
    hidden = _get_value(response, "_hidden_params")
    hidden_cost = _coerce_float(_get_value(hidden, "response_cost"))
    if hidden_cost is not None:
        return hidden_cost

    usage = _get_value(response, "usage")
    usage_cost = _coerce_float(_get_value(usage, "cost"))
    if usage_cost is not None:
        return usage_cost

    cost_details = _get_value(usage, "cost_details")
    upstream_cost = _coerce_float(_get_value(cost_details, "upstream_inference_cost"))
    if upstream_cost is not None:
        return upstream_cost
    return None


def iter_pricing_model_candidates(
    *models: str | None,
    pricing_model_alias: str | None = None,
) -> Iterator[str]:
    yield from _iter_unique_pricing_candidates(
        _seed_pricing_model_candidates(
            models=models,
            pricing_model_alias=pricing_model_alias,
        )
    )


def _seed_pricing_model_candidates(
    *,
    models: tuple[str | None, ...],
    pricing_model_alias: str | None,
) -> list[str]:
    queue: list[str] = []
    if pricing_model_alias is not None:
        alias = str(pricing_model_alias).strip()
        if alias:
            queue.append(alias)
    for model in models:
        normalized = str(model or "").strip()
        if normalized:
            queue.append(normalized)
    return queue


def _iter_unique_pricing_candidates(queue: list[str]) -> Iterator[str]:
    seen: set[str] = set()
    pending = list(queue)
    while pending:
        candidate = pending.pop(0).strip()
        if not candidate or candidate in seen:
            continue
        seen.add(candidate)
        yield candidate
        expanded = _expand_pricing_model_candidate(candidate)
        if expanded is not None:
            pending.append(expanded)


def _expand_pricing_model_candidate(candidate: str) -> str | None:
    separator: str | None = None
    if ":" in candidate:
        separator = ":"
    elif "/" in candidate:
        separator = "/"
    if separator is None:
        return None
    _, rest = candidate.split(separator, 1)
    normalized = rest.strip()
    if not normalized or normalized == candidate:
        return None
    return normalized


def estimate_cost_usd_from_tokens(
    *,
    model: str | None,
    prompt_tokens: int | None,
    completion_tokens: int | None,
    pricing_model_alias: str | None = None,
) -> float | None:
    if prompt_tokens is None and completion_tokens is None:
        return None

    prompt = int(prompt_tokens or 0)
    completion = int(completion_tokens or 0)
    if prompt <= 0 and completion <= 0:
        return 0.0

    try:
        from litellm.cost_calculator import cost_per_token
    except Exception:
        return None

    for candidate in iter_pricing_model_candidates(
        model,
        pricing_model_alias=pricing_model_alias,
    ):
        try:
            prompt_cost, completion_cost = cost_per_token(
                model=candidate,
                prompt_tokens=prompt,
                completion_tokens=completion,
            )
            return float(prompt_cost) + float(completion_cost)
        except Exception:
            continue
    return None


def estimate_cost_usd_from_response(
    *,
    response: object,
    model: str | None,
    pricing_model_alias: str | None = None,
) -> float | None:
    try:
        from litellm.cost_calculator import completion_cost
    except Exception:
        return None

    for candidate in iter_pricing_model_candidates(
        model,
        pricing_model_alias=pricing_model_alias,
    ):
        try:
            return float(
                completion_cost(
                    completion_response=response,
                    model=candidate,
                )
            )
        except Exception:
            continue
    return None


def resolve_cost_usd(
    *,
    response: object,
    model: str | None,
    prompt_tokens: int | None,
    completion_tokens: int | None,
    pricing_model_alias: str | None = None,
) -> float | None:
    measured_cost = extract_measured_cost_usd(response)
    if measured_cost is not None:
        return measured_cost
    estimated_cost = estimate_cost_usd_from_response(
        response=response,
        model=model,
        pricing_model_alias=pricing_model_alias,
    )
    if estimated_cost is not None:
        return estimated_cost
    return estimate_cost_usd_from_tokens(
        model=model,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        pricing_model_alias=pricing_model_alias,
    )
