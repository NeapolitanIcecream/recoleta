from __future__ import annotations

import time
from typing import Any, Protocol

from recoleta.llm_connection import LLMConnectionConfig


def iter_embedding_batches(
    inputs: list[str],
    *,
    max_batch_inputs: int,
    max_batch_chars: int,
):
    normalized_max_inputs = max(1, int(max_batch_inputs))
    normalized_max_chars = max(1, int(max_batch_chars))
    batch: list[str] = []
    batch_chars = 0
    for text in inputs:
        text_chars = len(text)
        if not batch:
            batch = [text]
            batch_chars = text_chars
            continue
        would_exceed_inputs = len(batch) >= normalized_max_inputs
        would_exceed_chars = (batch_chars + text_chars) > normalized_max_chars
        if would_exceed_inputs or would_exceed_chars:
            yield batch
            batch = [text]
            batch_chars = text_chars
            continue
        batch.append(text)
        batch_chars += text_chars
    if batch:
        yield batch


def extract_embeddings(response: object) -> list[list[float]]:
    data: Any
    if isinstance(response, dict):
        data = response.get("data")
    else:
        data = getattr(response, "data", None)
    if not isinstance(data, list):
        raise ValueError("embedding response missing data list")
    vectors: list[list[float]] = []
    for entry in data:
        if isinstance(entry, dict):
            raw = entry.get("embedding")
        else:
            raw = getattr(entry, "embedding", None)
        if not isinstance(raw, list):
            raise ValueError("embedding entry missing embedding list")
        vectors.append([float(value) for value in raw])
    return vectors


def extract_usage(response: object) -> dict[str, Any] | None:
    usage: Any
    if isinstance(response, dict):
        usage = response.get("usage")
    else:
        usage = getattr(response, "usage", None)
    if isinstance(usage, dict):
        return usage
    return None


def _extract_response_cost_usd(response: object) -> float | None:
    hidden: Any | None
    if isinstance(response, dict):
        hidden = response.get("_hidden_params")
    else:
        hidden = getattr(response, "_hidden_params", None)
    if not isinstance(hidden, dict):
        return None
    raw = hidden.get("response_cost")
    if isinstance(raw, (int, float)):
        return float(raw)
    if raw is None:
        return None
    try:
        return float(raw)
    except Exception:
        return None


def _get_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return None


def _estimate_prompt_tokens(*, model: str, inputs: list[str]) -> int | None:
    normalized_model = str(model or "").strip()
    if not normalized_model:
        return None
    if not inputs:
        return 0
    try:
        from litellm.utils import token_counter
    except Exception:
        return None

    joined = "\n\n".join(str(v) for v in inputs if str(v))
    if not joined.strip():
        return 0
    messages = [{"role": "user", "content": joined}]
    try:
        return int(token_counter(model=normalized_model, messages=messages))
    except Exception:
        try:
            return int(token_counter(model="gpt-3.5-turbo", messages=messages))
        except Exception:
            return None


class Embedder(Protocol):
    def embed(
        self,
        *,
        model: str,
        inputs: list[str],
        dimensions: int | None = None,
    ) -> tuple[list[list[float]], dict[str, Any]]: ...


_embedding: Any | None = None


def _get_embedding() -> Any:
    global _embedding  # noqa: PLW0603
    if _embedding is None:
        from litellm import embedding as _litellm_embedding

        _embedding = _litellm_embedding
    return _embedding


class LiteLLMEmbedder:
    def __init__(self, *, llm_connection: LLMConnectionConfig | None = None) -> None:
        self.llm_connection = llm_connection or LLMConnectionConfig()

    def embed(
        self,
        *,
        model: str,
        inputs: list[str],
        dimensions: int | None = None,
    ) -> tuple[list[list[float]], dict[str, Any]]:
        started = time.perf_counter()
        kwargs: dict[str, Any] = {"model": model, "input": inputs}
        if dimensions is not None:
            kwargs["dimensions"] = int(dimensions)
        kwargs.update(self.llm_connection.litellm_embedding_kwargs())
        response = _get_embedding()(**kwargs)
        elapsed_ms = int((time.perf_counter() - started) * 1000)
        vectors = extract_embeddings(response)
        usage = extract_usage(response)
        prompt_tokens: int | None = None
        total_tokens: int | None = None
        if isinstance(usage, dict):
            prompt_tokens = _get_int(usage.get("prompt_tokens"))
            total_tokens = _get_int(usage.get("total_tokens"))
            if prompt_tokens is None:
                prompt_tokens = _get_int(usage.get("input_tokens"))
            if total_tokens is None and prompt_tokens is not None:
                total_tokens = prompt_tokens

        tokens_estimated = False
        if prompt_tokens is None:
            estimated = _estimate_prompt_tokens(model=model, inputs=inputs)
            if estimated is not None:
                prompt_tokens = int(estimated)
                total_tokens = int(estimated)
                tokens_estimated = True

        cost_usd = _extract_response_cost_usd(response)
        if cost_usd is None and prompt_tokens is not None:
            try:
                from litellm.cost_calculator import cost_per_token

                prompt_cost, completion_cost = cost_per_token(
                    model=str(model),
                    prompt_tokens=int(prompt_tokens),
                    completion_tokens=0,
                )
                cost_usd = float(prompt_cost) + float(completion_cost)
            except Exception:
                cost_usd = None
        debug: dict[str, Any] = {
            "model": model,
            "inputs_total": len(inputs),
            "dimensions": dimensions,
            "elapsed_ms": elapsed_ms,
            "usage": usage,
            "prompt_tokens": prompt_tokens,
            "total_tokens": total_tokens,
            "tokens_estimated": tokens_estimated,
            "cost_usd": cost_usd,
        }
        connection_overrides = self.llm_connection.debug_payload()
        if connection_overrides:
            debug["connection_overrides"] = connection_overrides
        return vectors, debug
