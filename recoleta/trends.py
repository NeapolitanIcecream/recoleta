from __future__ import annotations

import json
import math
import os
import time
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from typing import Any, Protocol

from loguru import logger
from pydantic import BaseModel, Field, ValidationError

from recoleta.storage import Repository
from recoleta.types import sha256_hex

embedding: Any | None = None
completion: Any | None = None


def _get_embedding() -> Any:
    global embedding  # noqa: PLW0603
    if embedding is None:
        from litellm import embedding as _embedding

        embedding = _embedding
    return embedding


def _get_completion() -> Any:
    global completion  # noqa: PLW0603
    if completion is None:
        from litellm import completion as _completion

        completion = _completion
    return completion


def _iter_embedding_batches(
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


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        return 0.0
    dot = 0.0
    norm_a = 0.0
    norm_b = 0.0
    for x, y in zip(a, b):
        fx = float(x)
        fy = float(y)
        dot += fx * fy
        norm_a += fx * fx
        norm_b += fy * fy
    if norm_a <= 0.0 or norm_b <= 0.0:
        return 0.0
    return dot / (math.sqrt(norm_a) * math.sqrt(norm_b))


def _bounded_cosine_similarity(a: list[float], b: list[float]) -> float:
    cosine = _cosine_similarity(a, b)
    if not math.isfinite(cosine):
        return 0.0
    return max(0.0, min(1.0, cosine))


def _extract_embeddings(response: object) -> list[list[float]]:
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


def _extract_usage(response: object) -> dict[str, Any] | None:
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
        vectors = _extract_embeddings(response)
        usage = _extract_usage(response)
        debug: dict[str, Any] = {
            "model": model,
            "inputs_total": len(inputs),
            "dimensions": dimensions,
            "elapsed_ms": elapsed_ms,
            "usage": usage,
        }
        return vectors, debug


@dataclass(slots=True)
class SemanticSearchHit:
    chunk_id: int
    doc_id: int
    chunk_index: int
    score: float
    text_preview: str


def ensure_summary_embeddings_for_period(
    *,
    repository: Repository,
    run_id: str,
    doc_type: str,
    period_start: datetime,
    period_end: datetime,
    embedding_model: str,
    embedding_dimensions: int | None,
    max_batch_inputs: int,
    max_batch_chars: int,
    limit: int = 500,
) -> dict[str, Any]:
    """Ensure summary chunks in period have embeddings persisted (idempotent by text_hash)."""
    log = logger.bind(module="trends.semantic_index", run_id=run_id, doc_type=doc_type)
    normalized_model = str(embedding_model or "").strip()
    if not normalized_model:
        raise ValueError("embedding_model must not be empty")

    chunks = repository.list_summary_chunks_in_period(
        doc_type=doc_type,
        period_start=period_start,
        period_end=period_end,
        limit=limit,
    )
    if not chunks:
        return {
            "chunks_total": 0,
            "embedded_total": 0,
            "skipped_total": 0,
            "embedding_calls_total": 0,
            "embedding_errors_total": 0,
        }

    chunk_ids: list[int] = []
    chunk_texts: dict[int, str] = {}
    chunk_hashes: dict[int, str] = {}
    for chunk in chunks:
        raw_id = getattr(chunk, "id", None)
        if raw_id is None:
            continue
        cid = int(raw_id)
        if cid <= 0:
            continue
        text_value = str(getattr(chunk, "text", "") or "").strip()
        if not text_value:
            continue
        chunk_ids.append(cid)
        chunk_texts[cid] = text_value
        chunk_hashes[cid] = str(getattr(chunk, "text_hash", "") or "") or sha256_hex(
            text_value
        )

    existing = repository.list_chunk_embeddings(
        chunk_ids=chunk_ids, model=normalized_model
    )

    to_embed_ids: list[int] = []
    to_embed_texts: list[str] = []
    skipped_total = 0
    for cid in chunk_ids:
        row = existing.get(cid)
        row_hash = str(getattr(row, "text_hash", "") or "") if row is not None else ""
        row_dims = getattr(row, "dimensions", None) if row is not None else None
        dims_match = (row_dims is None and embedding_dimensions is None) or (
            row_dims is not None
            and embedding_dimensions is not None
            and int(row_dims) == int(embedding_dimensions)
        )
        if row is not None and row_hash == chunk_hashes[cid] and dims_match:
            skipped_total += 1
            continue
        to_embed_ids.append(cid)
        to_embed_texts.append(chunk_texts[cid])

    embedded_total = 0
    embedding_calls_total = 0
    embedding_errors_total = 0

    if not to_embed_ids:
        return {
            "chunks_total": len(chunk_ids),
            "embedded_total": 0,
            "skipped_total": skipped_total,
            "embedding_calls_total": 0,
            "embedding_errors_total": 0,
        }

    embedder = LiteLLMEmbedder()
    idx = 0
    for batch in _iter_embedding_batches(
        to_embed_texts,
        max_batch_inputs=max_batch_inputs,
        max_batch_chars=max_batch_chars,
    ):
        batch_ids = to_embed_ids[idx : idx + len(batch)]
        idx += len(batch)
        debug: dict[str, Any] | None = None
        try:
            embedding_calls_total += 1
            vectors, debug = embedder.embed(
                model=normalized_model, inputs=batch, dimensions=embedding_dimensions
            )
            if len(vectors) != len(batch):
                raise ValueError("embedding output size mismatch")
            for cid, vec in zip(batch_ids, vectors, strict=True):
                repository.upsert_chunk_embedding(
                    chunk_id=cid,
                    model=normalized_model,
                    dimensions=embedding_dimensions,
                    text_hash=chunk_hashes[cid],
                    vector=vec,
                )
                embedded_total += 1
        except Exception as exc:  # noqa: BLE001
            embedding_errors_total += 1
            log.warning(
                "Summary embedding batch failed embedded_so_far={} error_type={} error={}",
                embedded_total,
                type(exc).__name__,
                str(exc),
            )

    return {
        "chunks_total": len(chunk_ids),
        "embedded_total": embedded_total,
        "skipped_total": skipped_total,
        "embedding_calls_total": embedding_calls_total,
        "embedding_errors_total": embedding_errors_total,
    }


def semantic_search_summaries_in_period(
    *,
    repository: Repository,
    run_id: str,
    doc_type: str,
    period_start: datetime,
    period_end: datetime,
    query: str,
    embedding_model: str,
    embedding_dimensions: int | None,
    max_batch_inputs: int,
    max_batch_chars: int,
    limit: int = 10,
    corpus_limit: int = 500,
) -> list[SemanticSearchHit]:
    log = logger.bind(module="trends.semantic_search", run_id=run_id, doc_type=doc_type)
    normalized_query = str(query or "").strip()
    if not normalized_query:
        return []

    index_stats = ensure_summary_embeddings_for_period(
        repository=repository,
        run_id=run_id,
        doc_type=doc_type,
        period_start=period_start,
        period_end=period_end,
        embedding_model=embedding_model,
        embedding_dimensions=embedding_dimensions,
        max_batch_inputs=max_batch_inputs,
        max_batch_chars=max_batch_chars,
        limit=corpus_limit,
    )

    embedder = LiteLLMEmbedder()
    query_vecs, _ = embedder.embed(
        model=str(embedding_model).strip(),
        inputs=[f"Query: {normalized_query}"],
        dimensions=embedding_dimensions,
    )
    if len(query_vecs) != 1:
        raise ValueError("query embedding output size mismatch")
    query_vec = query_vecs[0]

    chunks = repository.list_summary_chunks_in_period(
        doc_type=doc_type,
        period_start=period_start,
        period_end=period_end,
        limit=corpus_limit,
    )
    chunk_ids: list[int] = []
    meta_by_id: dict[int, tuple[int, int, str]] = {}
    for chunk in chunks:
        raw_id = getattr(chunk, "id", None)
        if raw_id is None:
            continue
        cid = int(raw_id)
        if cid <= 0:
            continue
        doc_id = int(getattr(chunk, "doc_id"))
        chunk_index = int(getattr(chunk, "chunk_index"))
        text_value = str(getattr(chunk, "text", "") or "").strip()
        preview = text_value[:240] + ("..." if len(text_value) > 240 else "")
        chunk_ids.append(cid)
        meta_by_id[cid] = (doc_id, chunk_index, preview)

    embeddings = repository.list_chunk_embeddings(
        chunk_ids=chunk_ids, model=str(embedding_model).strip()
    )

    scored: list[SemanticSearchHit] = []
    missing = 0
    for cid in chunk_ids:
        row = embeddings.get(cid)
        if row is None:
            missing += 1
            continue
        try:
            vec = json.loads(str(getattr(row, "vector_json") or "[]"))
        except Exception:
            continue
        if not isinstance(vec, list) or not vec:
            continue
        score = _bounded_cosine_similarity(query_vec, [float(v) for v in vec])
        doc_id, chunk_index, preview = meta_by_id[cid]
        scored.append(
            SemanticSearchHit(
                chunk_id=cid,
                doc_id=doc_id,
                chunk_index=chunk_index,
                score=score,
                text_preview=preview,
            )
        )

    scored_sorted = sorted(scored, key=lambda h: h.score, reverse=True)
    log.info(
        "Semantic search done hits={} missing_embeddings={} index_stats={}",
        len(scored_sorted),
        missing,
        {
            "chunks_total": index_stats.get("chunks_total"),
            "embedded_total": index_stats.get("embedded_total"),
            "skipped_total": index_stats.get("skipped_total"),
            "embedding_calls_total": index_stats.get("embedding_calls_total"),
            "embedding_errors_total": index_stats.get("embedding_errors_total"),
        },
    )
    return scored_sorted[: max(1, min(int(limit), 50))]


class TrendCluster(BaseModel):
    name: str
    description: str
    representative_doc_ids: list[int] = Field(default_factory=list)
    representative_chunks: list[dict[str, Any]] = Field(default_factory=list)


class TrendPayload(BaseModel):
    title: str
    granularity: str  # day|week|month
    period_start: str  # ISO datetime (UTC)
    period_end: str  # ISO datetime (UTC)
    overview_md: str
    topics: list[str] = Field(default_factory=list)
    clusters: list[TrendCluster] = Field(default_factory=list)
    highlights: list[str] = Field(default_factory=list)


def _response_message(response: object) -> Any:
    if isinstance(response, dict):
        return (response.get("choices") or [])[0].get("message")
    choices = getattr(response, "choices")
    return choices[0].message


def _message_content(message: object) -> str:
    if isinstance(message, dict):
        return str(message.get("content") or "")
    return str(getattr(message, "content", "") or "")


def _message_tool_calls(message: object) -> list[dict[str, Any]]:
    tool_calls: Any
    if isinstance(message, dict):
        tool_calls = message.get("tool_calls")
    else:
        tool_calls = getattr(message, "tool_calls", None)
    if not isinstance(tool_calls, list):
        return []
    out: list[dict[str, Any]] = []
    for call in tool_calls:
        if isinstance(call, dict):
            out.append(call)
            continue
        fn = getattr(call, "function", None)
        out.append(
            {
                "id": getattr(call, "id", None),
                "type": getattr(call, "type", "function"),
                "function": {
                    "name": getattr(fn, "name", None) if fn is not None else None,
                    "arguments": getattr(fn, "arguments", None)
                    if fn is not None
                    else None,
                },
            }
        )
    return out


def _tool_schemas() -> list[dict[str, Any]]:
    return [
        {
            "type": "function",
            "function": {
                "name": "list_docs",
                "description": "List documents in the target period, ordered by time. Use this to navigate by position.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "doc_type": {"type": "string", "enum": ["item", "trend"]},
                        "granularity": {
                            "type": "string",
                            "enum": ["day", "week", "month"],
                        },
                        "order_by": {
                            "type": "string",
                            "enum": ["event_desc", "event_asc"],
                        },
                        "offset": {"type": "integer", "minimum": 0},
                        "limit": {"type": "integer", "minimum": 1, "maximum": 200},
                    },
                    "required": ["doc_type"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_doc",
                "description": "Get document metadata by doc_id (no chunk text).",
                "parameters": {
                    "type": "object",
                    "properties": {"doc_id": {"type": "integer", "minimum": 1}},
                    "required": ["doc_id"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "read_chunk",
                "description": "Read a chunk of a document by (doc_id, chunk_index). Use this like reading code by chunk position.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "doc_id": {"type": "integer", "minimum": 1},
                        "chunk_index": {"type": "integer", "minimum": 0},
                    },
                    "required": ["doc_id", "chunk_index"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "search_text",
                "description": "Full-text search (FTS5) over indexed chunks in the target period.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "minLength": 1},
                        "doc_type": {"type": "string", "enum": ["item", "trend"]},
                        "limit": {"type": "integer", "minimum": 1, "maximum": 50},
                    },
                    "required": ["query", "doc_type"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "search_semantic",
                "description": "Semantic search over summary chunks in the target period (embeddings + cosine similarity).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "minLength": 1},
                        "doc_type": {"type": "string", "enum": ["item", "trend"]},
                        "limit": {"type": "integer", "minimum": 1, "maximum": 50},
                    },
                    "required": ["query", "doc_type"],
                },
            },
        },
    ]


def _litellm_mock_response_from_env() -> str | None:
    raw = str(os.getenv("RECOLETA_LITELLM_MOCK_RESPONSE", "")).strip()
    return raw or None


def _chunk_text_segments(
    text_value: str, *, chunk_chars: int
) -> list[tuple[int, int, str]]:
    normalized = str(text_value or "")
    size = max(200, int(chunk_chars))
    if not normalized.strip():
        return []
    segments: list[tuple[int, int, str]] = []
    start = 0
    end = len(normalized)
    while start < end:
        seg_end = min(end, start + size)
        seg = normalized[start:seg_end]
        segments.append((start, seg_end, seg))
        start = seg_end
    return segments


def index_items_as_documents(
    *,
    repository: Repository,
    run_id: str,
    period_start: datetime,
    period_end: datetime,
    limit: int = 2000,
    content_chunk_chars: int = 1200,
    max_content_chunks_per_item: int = 8,
) -> dict[str, Any]:
    """Index analyzed items into documents + chunks (summary first, content optional)."""
    log = logger.bind(module="trends.index_items", run_id=run_id)
    started = time.perf_counter()
    pairs = repository.list_analyzed_items_in_period(
        period_start=period_start, period_end=period_end, limit=limit
    )
    docs_upserted = 0
    chunks_upserted = 0
    content_chunks_upserted = 0

    content_types = [
        "pdf_text",
        "html_maintext",
        "html_document_md",
        "html_document",
        "latex_source",
    ]
    for item, analysis in pairs:
        try:
            doc = repository.upsert_document_for_item(item=item)
            docs_upserted += 1
            doc_id = int(getattr(doc, "id"))
            repository.upsert_document_chunk(
                doc_id=doc_id,
                chunk_index=0,
                kind="summary",
                text_value=str(getattr(analysis, "summary", "") or "").strip(),
                start_char=0,
                end_char=None,
                source_content_type="analysis_summary",
            )
            chunks_upserted += 1

            chosen: str | None = None
            chosen_type: str | None = None
            texts = repository.get_latest_content_texts(
                item_id=int(getattr(item, "id")), content_types=content_types
            )
            for ctype in content_types:
                candidate = texts.get(ctype)
                if isinstance(candidate, str) and candidate.strip():
                    chosen = candidate
                    chosen_type = ctype
                    break
            if not chosen or chosen_type is None:
                continue

            segments = _chunk_text_segments(chosen, chunk_chars=content_chunk_chars)
            for seg_idx, (start_char, end_char, seg) in enumerate(
                segments[: max(0, int(max_content_chunks_per_item))],
                start=1,
            ):
                repository.upsert_document_chunk(
                    doc_id=doc_id,
                    chunk_index=seg_idx,
                    kind="content",
                    text_value=seg,
                    start_char=start_char,
                    end_char=end_char,
                    source_content_type=chosen_type,
                )
                chunks_upserted += 1
                content_chunks_upserted += 1
        except Exception as exc:  # noqa: BLE001
            log.bind(item_id=getattr(item, "id", None)).warning(
                "Index item failed error_type={} error={}",
                type(exc).__name__,
                str(exc),
            )

    elapsed_ms = int((time.perf_counter() - started) * 1000)
    stats = {
        "items_total": len(pairs),
        "docs_upserted": docs_upserted,
        "chunks_upserted": chunks_upserted,
        "content_chunks_upserted": content_chunks_upserted,
        "duration_ms": elapsed_ms,
    }
    log.info("Index items done stats={}", stats)
    return stats


def generate_trend_via_tools(
    *,
    repository: Repository,
    run_id: str,
    llm_model: str,
    embedding_model: str,
    embedding_dimensions: int | None,
    embedding_batch_max_inputs: int,
    embedding_batch_max_chars: int,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
    corpus_doc_type: str,
    corpus_granularity: str | None = None,
    max_steps: int = 10,
    include_debug: bool = False,
) -> tuple[TrendPayload, dict[str, Any] | None]:
    log = logger.bind(module="trends.orchestrator", run_id=run_id)

    tools = _tool_schemas()

    def list_docs_tool(args: dict[str, Any]) -> dict[str, Any]:
        doc_type = str(args.get("doc_type") or "").strip().lower()
        order_by = str(args.get("order_by") or "event_desc").strip()
        offset = int(args.get("offset") or 0)
        limit = int(args.get("limit") or 50)
        gran = args.get("granularity")
        granularity_arg = str(gran).strip().lower() if isinstance(gran, str) else None
        docs = repository.list_documents(
            doc_type=doc_type,
            period_start=period_start,
            period_end=period_end,
            granularity=granularity_arg,
            order_by=order_by,
            offset=offset,
            limit=limit,
        )
        out = []
        for doc in docs:
            published_at = getattr(doc, "published_at", None)
            period_start_value = getattr(doc, "period_start", None)
            period_end_value = getattr(doc, "period_end", None)
            out.append(
                {
                    "doc_id": int(getattr(doc, "id")),
                    "doc_type": str(getattr(doc, "doc_type") or ""),
                    "title": str(getattr(doc, "title") or ""),
                    "item_id": getattr(doc, "item_id", None),
                    "source": str(getattr(doc, "source") or ""),
                    "canonical_url": str(getattr(doc, "canonical_url") or ""),
                    "published_at": published_at.isoformat()
                    if isinstance(published_at, datetime)
                    else None,
                    "granularity": str(getattr(doc, "granularity") or ""),
                    "period_start": period_start_value.isoformat()
                    if isinstance(period_start_value, datetime)
                    else None,
                    "period_end": period_end_value.isoformat()
                    if isinstance(period_end_value, datetime)
                    else None,
                }
            )
        return {"docs": out, "returned": len(out)}

    def get_doc_tool(args: dict[str, Any]) -> dict[str, Any]:
        doc_id = int(args.get("doc_id") or 0)
        doc = repository.get_document(doc_id=doc_id)
        if doc is None:
            return {"doc": None}
        published_at = getattr(doc, "published_at", None)
        period_start_value = getattr(doc, "period_start", None)
        period_end_value = getattr(doc, "period_end", None)
        return {
            "doc": {
                "doc_id": int(getattr(doc, "id")),
                "doc_type": str(getattr(doc, "doc_type") or ""),
                "title": str(getattr(doc, "title") or ""),
                "item_id": getattr(doc, "item_id", None),
                "source": str(getattr(doc, "source") or ""),
                "canonical_url": str(getattr(doc, "canonical_url") or ""),
                "published_at": published_at.isoformat()
                if isinstance(published_at, datetime)
                else None,
                "granularity": str(getattr(doc, "granularity") or ""),
                "period_start": period_start_value.isoformat()
                if isinstance(period_start_value, datetime)
                else None,
                "period_end": period_end_value.isoformat()
                if isinstance(period_end_value, datetime)
                else None,
            }
        }

    def read_chunk_tool(args: dict[str, Any]) -> dict[str, Any]:
        doc_id = int(args.get("doc_id") or 0)
        chunk_index = int(args.get("chunk_index") or 0)
        chunk = repository.read_document_chunk(doc_id=doc_id, chunk_index=chunk_index)
        if chunk is None:
            return {"chunk": None}
        return {
            "chunk": {
                "chunk_id": int(getattr(chunk, "id")),
                "doc_id": int(getattr(chunk, "doc_id")),
                "chunk_index": int(getattr(chunk, "chunk_index")),
                "kind": str(getattr(chunk, "kind") or ""),
                "start_char": getattr(chunk, "start_char", None),
                "end_char": getattr(chunk, "end_char", None),
                "source_content_type": str(getattr(chunk, "source_content_type") or ""),
                "text": str(getattr(chunk, "text") or ""),
            }
        }

    def search_text_tool(args: dict[str, Any]) -> dict[str, Any]:
        query = str(args.get("query") or "")
        doc_type = str(args.get("doc_type") or "").strip().lower()
        limit = int(args.get("limit") or 10)
        hits = repository.search_chunks_text(
            query=query,
            doc_type=doc_type,
            period_start=period_start,
            period_end=period_end,
            limit=limit,
        )
        return {"hits": hits, "returned": len(hits)}

    def search_semantic_tool(args: dict[str, Any]) -> dict[str, Any]:
        query = str(args.get("query") or "")
        doc_type = str(args.get("doc_type") or "").strip().lower()
        limit = int(args.get("limit") or 10)
        hits = semantic_search_summaries_in_period(
            repository=repository,
            run_id=run_id,
            doc_type=doc_type,
            period_start=period_start,
            period_end=period_end,
            query=query,
            embedding_model=embedding_model,
            embedding_dimensions=embedding_dimensions,
            max_batch_inputs=embedding_batch_max_inputs,
            max_batch_chars=embedding_batch_max_chars,
            limit=limit,
        )
        rows = [
            {
                "chunk_id": h.chunk_id,
                "doc_id": h.doc_id,
                "chunk_index": h.chunk_index,
                "score": round(float(h.score), 6),
                "text_preview": h.text_preview,
            }
            for h in hits
        ]
        return {"hits": rows, "returned": len(rows)}

    tool_funcs = {
        "list_docs": list_docs_tool,
        "get_doc": get_doc_tool,
        "read_chunk": read_chunk_tool,
        "search_text": search_text_tool,
        "search_semantic": search_semantic_tool,
    }

    system_message = (
        "You are a research trend analyst. You can explore a local document corpus using tools. "
        "Prefer summary chunks (chunk_index=0) for speed. If needed, inspect content chunks by position. "
        "When you are ready, return a single strict JSON object matching the required schema."
    )
    user_message = json.dumps(
        {
            "task": "Generate research trends for the period.",
            "granularity": granularity,
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat(),
            "corpus": {
                "doc_type": corpus_doc_type,
                "granularity": corpus_granularity,
            },
            "required_json_schema": TrendPayload.model_json_schema(),
            "notes": [
                "Use tools to cite representative doc_id/chunk_index in clusters.",
                "Return JSON only. No markdown outside JSON. No extra keys.",
            ],
        },
        ensure_ascii=False,
        separators=(",", ":"),
    )
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]

    trace: dict[str, Any] | None = {"steps": []} if include_debug else None
    tool_calls_total = 0

    for step in range(max(1, int(max_steps))):
        kwargs: dict[str, Any] = {
            "model": llm_model,
            "messages": messages,
            "tools": tools,
            "tool_choice": "auto",
        }
        mock_response = _litellm_mock_response_from_env()
        if mock_response is not None:
            kwargs["mock_response"] = mock_response
        response = _get_completion()(**kwargs)
        message = _response_message(response)
        content = _message_content(message)
        tool_calls = _message_tool_calls(message)
        assistant_msg: dict[str, Any] = {"role": "assistant", "content": content}
        if tool_calls:
            assistant_msg["tool_calls"] = tool_calls
        messages.append(assistant_msg)
        if trace is not None:
            trace["steps"].append(
                {
                    "step": step,
                    "assistant": {
                        "content_preview": (content[:400] + "...")
                        if len(content) > 400
                        else content,
                        "tool_calls_total": len(tool_calls),
                    },
                }
            )

        if not tool_calls:
            break

        for call in tool_calls:
            fn = call.get("function") or {}
            name = str(fn.get("name") or "").strip()
            raw_args = fn.get("arguments")
            tool_call_id = str(call.get("id") or "")
            tool_calls_total += 1
            try:
                parsed_args = json.loads(raw_args) if isinstance(raw_args, str) else {}
                if not isinstance(parsed_args, dict):
                    parsed_args = {}
            except Exception:
                parsed_args = {}
            func = tool_funcs.get(name)
            if func is None:
                result = {"error": f"unknown_tool:{name}"}
            else:
                try:
                    result = func(parsed_args)
                except Exception as exc:  # noqa: BLE001
                    result = {"error": type(exc).__name__, "message": str(exc)}
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "name": name,
                    "content": json.dumps(
                        result, ensure_ascii=False, separators=(",", ":")
                    ),
                }
            )

    # Finalize with JSON mode if needed.
    last_content = str(messages[-1].get("content") or "")
    decoded: Any | None = None
    try:
        decoded = json.loads(last_content)
    except Exception:
        decoded = None
    if not isinstance(decoded, dict):
        kwargs = {
            "model": llm_model,
            "messages": messages
            + [
                {
                    "role": "system",
                    "content": "Return strict JSON only. No markdown, no extra keys.",
                }
            ],
            "response_format": {"type": "json_object"},
        }
        mock_response = _litellm_mock_response_from_env()
        if mock_response is not None:
            kwargs["mock_response"] = mock_response
        finalize = _get_completion()(**kwargs)
        final_message = _response_message(finalize)
        decoded = json.loads(_message_content(final_message))

    try:
        payload = TrendPayload.model_validate(decoded)
    except ValidationError as exc:
        log.warning("Trend payload validation failed error={}", str(exc))
        raise

    debug = None
    if trace is not None:
        debug = {"trace": trace, "tool_calls_total": tool_calls_total}
    log.info(
        "Trend generation completed tool_calls_total={} debug={}",
        tool_calls_total,
        bool(debug),
    )
    return payload, debug


def persist_trend_payload(
    *,
    repository: Repository,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
    payload: TrendPayload,
) -> int:
    title = str(payload.title or "").strip() or "Trend"
    doc = repository.upsert_document_for_trend(
        granularity=granularity,
        period_start=period_start,
        period_end=period_end,
        title=title,
    )
    doc_id = int(getattr(doc, "id"))

    repository.upsert_document_chunk(
        doc_id=doc_id,
        chunk_index=0,
        kind="summary",
        text_value=str(payload.overview_md or "").strip() or "(empty)",
        start_char=0,
        end_char=None,
        source_content_type="trend_overview",
    )
    repository.upsert_document_chunk(
        doc_id=doc_id,
        chunk_index=1,
        kind="meta",
        text_value=json.dumps(
            payload.model_dump(mode="json"), ensure_ascii=False, separators=(",", ":")
        ),
        start_char=0,
        end_char=None,
        source_content_type="trend_payload_json",
    )
    return doc_id


def day_period_bounds(anchor: date) -> tuple[datetime, datetime]:
    start = datetime(anchor.year, anchor.month, anchor.day, tzinfo=UTC)
    return start, start + timedelta(days=1)


def week_period_bounds(anchor: date) -> tuple[datetime, datetime]:
    # ISO week: Monday start.
    weekday = anchor.isoweekday()  # 1..7
    start_day = anchor - timedelta(days=weekday - 1)
    start = datetime(start_day.year, start_day.month, start_day.day, tzinfo=UTC)
    return start, start + timedelta(days=7)


def month_period_bounds(anchor: date) -> tuple[datetime, datetime]:
    start = datetime(anchor.year, anchor.month, 1, tzinfo=UTC)
    if anchor.month == 12:
        end = datetime(anchor.year + 1, 1, 1, tzinfo=UTC)
    else:
        end = datetime(anchor.year, anchor.month + 1, 1, tzinfo=UTC)
    return start, end
