from __future__ import annotations

import time
from typing import Any, Protocol


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
        response = _get_embedding()(**kwargs)
        elapsed_ms = int((time.perf_counter() - started) * 1000)
        vectors = extract_embeddings(response)
        usage = extract_usage(response)
        debug: dict[str, Any] = {
            "model": model,
            "inputs_total": len(inputs),
            "dimensions": dimensions,
            "elapsed_ms": elapsed_ms,
            "usage": usage,
        }
        return vectors, debug
