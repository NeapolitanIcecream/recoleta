from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass
from datetime import datetime
from threading import Lock
from typing import Any

from loguru import logger

from recoleta.llm_connection import LLMConnectionConfig
from recoleta.ports import TrendRepositoryPort
from recoleta.rag.embeddings import LiteLLMEmbedder, iter_embedding_batches
from recoleta.rag.vector_store import LanceVectorStore, VectorRow
from recoleta.types import DEFAULT_TOPIC_STREAM


@dataclass(slots=True)
class SemanticSearchHit:
    chunk_id: int
    doc_id: int
    chunk_index: int
    score: float
    text_preview: str


@dataclass(frozen=True, slots=True)
class _SummaryCorpusCacheKey:
    run_id: str
    doc_type: str
    granularity: str
    period_start: str
    period_end: str
    embedding_model: str
    embedding_dimensions: int | None
    max_batch_inputs: int
    max_batch_chars: int
    embedding_failure_mode: str
    embedding_max_errors: int
    limit: int
    offset: int
    scope: str
    vector_store_dir: str
    vector_store_table: str


_SUMMARY_CORPUS_CACHE_MAX_KEYS = 64
_summary_corpus_cache_lock = Lock()
# Cache only within a run-local search context; the indexed corpus is expected
# to be stable for a given trends run_id once indexing has finished.
_summary_corpus_cache: OrderedDict[_SummaryCorpusCacheKey, dict[str, Any]] = OrderedDict()


def _sanitize_where_string(value: str) -> str:
    # Minimal single-quote escaping for SQL-like filters.
    return str(value).replace("'", "''")


def _summary_corpus_cache_key(
    *,
    vector_store: LanceVectorStore,
    run_id: str,
    doc_type: str,
    granularity: str | None,
    period_start: datetime,
    period_end: datetime,
    embedding_model: str,
    embedding_dimensions: int | None,
    max_batch_inputs: int,
    max_batch_chars: int,
    embedding_failure_mode: str,
    embedding_max_errors: int,
    limit: int,
    offset: int,
    scope: str,
) -> _SummaryCorpusCacheKey:
    return _SummaryCorpusCacheKey(
        run_id=str(run_id or "").strip(),
        doc_type=str(doc_type or "").strip().lower(),
        granularity=str(granularity or "").strip().lower(),
        period_start=period_start.isoformat(),
        period_end=period_end.isoformat(),
        embedding_model=str(embedding_model or "").strip(),
        embedding_dimensions=(
            int(embedding_dimensions) if embedding_dimensions is not None else None
        ),
        max_batch_inputs=int(max_batch_inputs),
        max_batch_chars=int(max_batch_chars),
        embedding_failure_mode=str(embedding_failure_mode or "").strip().lower(),
        embedding_max_errors=int(embedding_max_errors or 0),
        limit=int(limit),
        offset=int(offset),
        scope=str(scope or "").strip(),
        vector_store_dir=str(getattr(vector_store, "db_dir", "")),
        vector_store_table=str(getattr(vector_store, "table_name", "")),
    )


def _clone_summary_index_stats(
    stats: dict[str, Any],
    *,
    cache_hit: bool,
) -> dict[str, Any]:
    cloned = dict(stats)
    candidate_chunk_ids = list(cloned.get("candidate_chunk_ids") or [])
    chunks_total = int(cloned.get("chunks_total") or len(candidate_chunk_ids))
    cloned["candidate_chunk_ids"] = candidate_chunk_ids
    cloned["corpus_cache_hit"] = cache_hit
    if cache_hit:
        cloned["embedded_total"] = 0
        cloned["skipped_total"] = chunks_total
        cloned["embedding_calls_total"] = 0
        cloned["embedding_errors_total"] = 0
        cloned["embedding_prompt_tokens_total"] = 0
        cloned["embedding_prompt_tokens_missing_total"] = 0
        cloned["embedding_cost_usd_total"] = 0.0
        cloned["embedding_cost_missing_total"] = 0
    return cloned


def _should_cache_summary_index_stats(stats: dict[str, Any]) -> bool:
    return int(stats.get("embedding_errors_total") or 0) <= 0


def ensure_summary_vectors_for_period(
    *,
    repository: TrendRepositoryPort,
    vector_store: LanceVectorStore,
    run_id: str,
    doc_type: str,
    granularity: str | None = None,
    period_start: datetime,
    period_end: datetime,
    embedding_model: str,
    embedding_dimensions: int | None,
    max_batch_inputs: int,
    max_batch_chars: int,
    embedding_failure_mode: str = "continue",
    embedding_max_errors: int = 0,
    limit: int = 500,
    offset: int = 0,
    scope: str = DEFAULT_TOPIC_STREAM,
    llm_connection: LLMConnectionConfig | None = None,
) -> dict[str, Any]:
    """Ensure summary chunks in period have vectors in LanceDB (idempotent by text_hash)."""

    log = logger.bind(module="rag.semantic_index", run_id=run_id, doc_type=doc_type)
    normalized_model = str(embedding_model or "").strip()
    if not normalized_model:
        raise ValueError("embedding_model must not be empty")

    normalized_failure_mode = str(embedding_failure_mode or "").strip().lower()
    if not normalized_failure_mode:
        normalized_failure_mode = "continue"
    if normalized_failure_mode not in {"continue", "fail_fast", "threshold"}:
        raise ValueError(
            "embedding_failure_mode must be one of: continue, fail_fast, threshold"
        )
    normalized_max_errors = max(0, int(embedding_max_errors or 0))
    if normalized_failure_mode == "threshold" and normalized_max_errors <= 0:
        raise ValueError(
            "embedding_max_errors must be a positive integer when embedding_failure_mode=threshold"
        )

    rows = repository.list_summary_chunk_index_rows_in_period(
        doc_type=doc_type,
        granularity=granularity,
        period_start=period_start,
        period_end=period_end,
        scope=scope,
        limit=limit,
        offset=offset,
    )
    if not rows:
        return {
            "chunks_total": 0,
            "candidate_chunk_ids": [],
            "embedded_total": 0,
            "skipped_total": 0,
            "embedding_calls_total": 0,
            "embedding_errors_total": 0,
            "embedding_prompt_tokens_total": 0,
            "embedding_prompt_tokens_missing_total": 0,
            "embedding_cost_usd_total": 0.0,
            "embedding_cost_missing_total": 0,
            "embedding_failure_mode": normalized_failure_mode,
            "embedding_max_errors": normalized_max_errors,
        }

    chunk_ids = [int(r["chunk_id"]) for r in rows if int(r.get("chunk_id") or 0) > 0]
    existing_hashes = vector_store.fetch_existing_hashes(chunk_ids=chunk_ids)

    to_embed_rows: list[dict[str, Any]] = []
    skipped_total = 0
    for r in rows:
        cid = int(r.get("chunk_id") or 0)
        if cid <= 0:
            continue
        text = str(r.get("text") or "").strip()
        if not text:
            continue
        text_hash = str(r.get("text_hash") or "").strip()
        if existing_hashes.get(cid) == text_hash:
            skipped_total += 1
            continue
        to_embed_rows.append(r)

    if not to_embed_rows:
        return {
            "chunks_total": len(chunk_ids),
            "candidate_chunk_ids": chunk_ids,
            "embedded_total": 0,
            "skipped_total": skipped_total,
            "embedding_calls_total": 0,
            "embedding_errors_total": 0,
            "embedding_prompt_tokens_total": 0,
            "embedding_prompt_tokens_missing_total": 0,
            "embedding_cost_usd_total": 0.0,
            "embedding_cost_missing_total": 0,
            "embedding_failure_mode": normalized_failure_mode,
            "embedding_max_errors": normalized_max_errors,
        }

    embedder = LiteLLMEmbedder(llm_connection=llm_connection)
    embedding_calls_total = 0
    embedding_errors_total = 0
    embedded_total = 0
    embedding_prompt_tokens_total = 0
    embedding_prompt_tokens_missing_total = 0
    embedding_cost_usd_total = 0.0
    embedding_cost_missing_total = 0

    texts = [str(r["text"]) for r in to_embed_rows]
    idx = 0
    for batch in iter_embedding_batches(
        texts, max_batch_inputs=max_batch_inputs, max_batch_chars=max_batch_chars
    ):
        batch_rows = to_embed_rows[idx : idx + len(batch)]
        idx += len(batch)
        try:
            embedding_calls_total += 1
            vectors, embed_debug = embedder.embed(
                model=normalized_model, inputs=batch, dimensions=embedding_dimensions
            )
            if isinstance(embed_debug, dict):
                raw_prompt = embed_debug.get("prompt_tokens")
                if raw_prompt is None:
                    raw_prompt = embed_debug.get("total_tokens")
                if isinstance(raw_prompt, (int, float)):
                    embedding_prompt_tokens_total += int(raw_prompt)
                else:
                    embedding_prompt_tokens_missing_total += 1
                raw_cost = embed_debug.get("cost_usd")
                if isinstance(raw_cost, (int, float)):
                    embedding_cost_usd_total += float(raw_cost)
                else:
                    embedding_cost_missing_total += 1
            else:
                embedding_prompt_tokens_missing_total += 1
                embedding_cost_missing_total += 1
            if len(vectors) != len(batch):
                raise ValueError("embedding output size mismatch")
            upserts: list[VectorRow] = []
            for r, vec in zip(batch_rows, vectors, strict=True):
                text_preview = str(r.get("text_preview") or "")
                upserts.append(
                    VectorRow(
                        chunk_id=int(r["chunk_id"]),
                        doc_id=int(r["doc_id"]),
                        doc_type=str(r["doc_type"]),
                        chunk_index=int(r["chunk_index"]),
                        kind=str(r["kind"]),
                        text_hash=str(r["text_hash"]),
                        text_preview=text_preview,
                        event_start_ts=float(r["event_start_ts"]),
                        event_end_ts=float(r["event_end_ts"]),
                        vector=[float(v) for v in vec],
                    )
                )
            vector_store.upsert_rows(rows=upserts)
            embedded_total += len(upserts)
        except Exception as exc:  # noqa: BLE001
            embedding_errors_total += 1
            log.warning(
                "Vector sync batch failed embedded_so_far={} error_type={} error={}",
                embedded_total,
                type(exc).__name__,
                str(exc),
            )
            if normalized_failure_mode == "fail_fast":
                log.warning(
                    "Vector sync aborting (fail_fast) calls={} errors={}",
                    embedding_calls_total,
                    embedding_errors_total,
                )
                raise
            if (
                normalized_failure_mode == "threshold"
                and normalized_max_errors > 0
                and embedding_errors_total >= normalized_max_errors
            ):
                log.warning(
                    "Vector sync aborting (threshold) calls={} errors={} max_errors={}",
                    embedding_calls_total,
                    embedding_errors_total,
                    normalized_max_errors,
                )
                raise

    if (
        normalized_failure_mode == "threshold"
        and embedding_calls_total > 0
        and embedded_total <= 0
        and embedding_errors_total >= embedding_calls_total
    ):
        log.warning(
            "Vector sync aborted (all batches failed) calls={} errors={}",
            embedding_calls_total,
            embedding_errors_total,
        )
        raise RuntimeError("vector sync failed: all embedding batches failed")

    stats = {
        "chunks_total": len(chunk_ids),
        "candidate_chunk_ids": chunk_ids,
        "embedded_total": embedded_total,
        "skipped_total": skipped_total,
        "embedding_calls_total": embedding_calls_total,
        "embedding_errors_total": embedding_errors_total,
        "embedding_prompt_tokens_total": embedding_prompt_tokens_total,
        "embedding_prompt_tokens_missing_total": embedding_prompt_tokens_missing_total,
        "embedding_cost_usd_total": embedding_cost_usd_total,
        "embedding_cost_missing_total": embedding_cost_missing_total,
        "embedding_failure_mode": normalized_failure_mode,
        "embedding_max_errors": normalized_max_errors,
    }
    log.info("Vector sync done stats={}", stats)
    return stats


def semantic_search_summaries_in_period(
    *,
    repository: TrendRepositoryPort,
    vector_store: LanceVectorStore,
    run_id: str,
    doc_type: str,
    granularity: str | None = None,
    period_start: datetime,
    period_end: datetime,
    query: str,
    embedding_model: str,
    embedding_dimensions: int | None,
    max_batch_inputs: int,
    max_batch_chars: int,
    embedding_failure_mode: str = "continue",
    embedding_max_errors: int = 0,
    limit: int = 10,
    corpus_limit: int = 500,
    scope: str = DEFAULT_TOPIC_STREAM,
    metric_namespace: str | None = None,
    llm_connection: LLMConnectionConfig | None = None,
) -> list[SemanticSearchHit]:
    log = logger.bind(module="rag.semantic_search", run_id=run_id, doc_type=doc_type)
    normalized_query = str(query or "").strip()
    if not normalized_query:
        return []

    cache_key = _summary_corpus_cache_key(
        vector_store=vector_store,
        run_id=run_id,
        doc_type=doc_type,
        granularity=granularity,
        period_start=period_start,
        period_end=period_end,
        embedding_model=embedding_model,
        embedding_dimensions=embedding_dimensions,
        max_batch_inputs=max_batch_inputs,
        max_batch_chars=max_batch_chars,
        embedding_failure_mode=embedding_failure_mode,
        embedding_max_errors=embedding_max_errors,
        limit=corpus_limit,
        offset=0,
        scope=scope,
    )
    with _summary_corpus_cache_lock:
        cached_stats = _summary_corpus_cache.get(cache_key)
        if cached_stats is not None:
            _summary_corpus_cache.move_to_end(cache_key)
    if cached_stats is not None:
        index_stats = _clone_summary_index_stats(cached_stats, cache_hit=True)
    else:
        fresh_index_stats = ensure_summary_vectors_for_period(
            repository=repository,
            vector_store=vector_store,
            run_id=run_id,
            doc_type=doc_type,
            granularity=granularity,
            period_start=period_start,
            period_end=period_end,
            embedding_model=embedding_model,
            embedding_dimensions=embedding_dimensions,
            max_batch_inputs=max_batch_inputs,
            max_batch_chars=max_batch_chars,
            embedding_failure_mode=embedding_failure_mode,
            embedding_max_errors=embedding_max_errors,
            limit=corpus_limit,
            offset=0,
            scope=scope,
            llm_connection=llm_connection,
        )
        if _should_cache_summary_index_stats(fresh_index_stats):
            with _summary_corpus_cache_lock:
                _summary_corpus_cache[cache_key] = _clone_summary_index_stats(
                    fresh_index_stats,
                    cache_hit=False,
                )
                _summary_corpus_cache.move_to_end(cache_key)
                while len(_summary_corpus_cache) > _SUMMARY_CORPUS_CACHE_MAX_KEYS:
                    _summary_corpus_cache.popitem(last=False)
        index_stats = _clone_summary_index_stats(fresh_index_stats, cache_hit=False)
    candidate_chunk_ids = [
        int(raw_id)
        for raw_id in list(index_stats.get("candidate_chunk_ids") or [])
        if int(raw_id or 0) > 0
    ]
    if not candidate_chunk_ids:
        log.info("Semantic search skipped: empty candidate corpus")
        return []

    embedder = LiteLLMEmbedder(llm_connection=llm_connection)
    query_vecs, query_debug = embedder.embed(
        model=str(embedding_model).strip(),
        inputs=[f"Query: {normalized_query}"],
        dimensions=embedding_dimensions,
    )
    if len(query_vecs) != 1:
        raise ValueError("query embedding output size mismatch")
    query_vec = query_vecs[0]

    start_ts = float(period_start.timestamp())
    end_ts = float(period_end.timestamp())
    where = (
        "kind = 'summary' "
        f"AND doc_type = '{_sanitize_where_string(str(doc_type).strip().lower())}' "
        f"AND event_start_ts < {end_ts} AND event_end_ts >= {start_ts} "
        f"AND chunk_id IN ({', '.join(str(cid) for cid in candidate_chunk_ids)})"
    )
    rows = vector_store.search(
        query_vector=query_vec,
        where=where,
        limit=limit,
        metric="cosine",
        select_columns=[
            "chunk_id",
            "doc_id",
            "chunk_index",
            "text_preview",
            "_distance",
        ],
    )

    hits: list[SemanticSearchHit] = []
    for r in rows:
        raw_distance = r.get("_distance")
        if raw_distance is None:
            distance = 1.0
        else:
            try:
                distance = float(raw_distance)
            except Exception:
                distance = 1.0
        score = max(0.0, min(1.0, 1.0 - distance))
        hits.append(
            SemanticSearchHit(
                chunk_id=int(r.get("chunk_id") or 0),
                doc_id=int(r.get("doc_id") or 0),
                chunk_index=int(r.get("chunk_index") or 0),
                score=score,
                text_preview=str(r.get("text_preview") or ""),
            )
        )

    log.info(
        "Semantic search done hits={} index_stats={}",
        len(hits),
        {
            "chunks_total": index_stats.get("chunks_total"),
            "embedded_total": index_stats.get("embedded_total"),
            "skipped_total": index_stats.get("skipped_total"),
            "embedding_calls_total": index_stats.get("embedding_calls_total"),
            "embedding_errors_total": index_stats.get("embedding_errors_total"),
            "embedding_failure_mode": index_stats.get("embedding_failure_mode"),
            "embedding_max_errors": index_stats.get("embedding_max_errors"),
            "corpus_cache_hit": index_stats.get("corpus_cache_hit"),
        },
    )

    if metric_namespace is not None and str(metric_namespace).strip():
        prefix = str(metric_namespace).strip()
        calls_total = int(index_stats.get("embedding_calls_total") or 0) + 1
        errors_total = int(index_stats.get("embedding_errors_total") or 0)
        prompt_tokens_total = int(index_stats.get("embedding_prompt_tokens_total") or 0)
        prompt_tokens_missing_total = int(
            index_stats.get("embedding_prompt_tokens_missing_total") or 0
        )
        cost_usd_total = float(index_stats.get("embedding_cost_usd_total") or 0.0)
        cost_missing_total = int(index_stats.get("embedding_cost_missing_total") or 0)
        cache_hit = bool(index_stats.get("corpus_cache_hit"))

        if isinstance(query_debug, dict):
            raw_prompt = query_debug.get("prompt_tokens")
            if raw_prompt is None:
                raw_prompt = query_debug.get("total_tokens")
            if isinstance(raw_prompt, (int, float)):
                prompt_tokens_total += int(raw_prompt)
            else:
                prompt_tokens_missing_total += 1
            raw_cost = query_debug.get("cost_usd")
            if isinstance(raw_cost, (int, float)):
                cost_usd_total += float(raw_cost)
            else:
                cost_missing_total += 1
        else:
            prompt_tokens_missing_total += 1
            cost_missing_total += 1

        repository.record_metric(
            run_id=run_id,
            name=f"{prefix}.embedding_calls_total",
            value=calls_total,
            unit="count",
        )
        repository.record_metric(
            run_id=run_id,
            name=f"{prefix}.embedding_errors_total",
            value=errors_total,
            unit="count",
        )
        repository.record_metric(
            run_id=run_id,
            name=f"{prefix}.corpus_cache_hits_total"
            if cache_hit
            else f"{prefix}.corpus_cache_misses_total",
            value=1,
            unit="count",
        )
        if prompt_tokens_total > 0:
            repository.record_metric(
                run_id=run_id,
                name=f"{prefix}.embedding_prompt_tokens_total",
                value=prompt_tokens_total,
                unit="count",
            )
        if cost_usd_total > 0.0:
            repository.record_metric(
                run_id=run_id,
                name=f"{prefix}.embedding_estimated_cost_usd",
                value=cost_usd_total,
                unit="usd",
            )
        if prompt_tokens_missing_total > 0:
            repository.record_metric(
                run_id=run_id,
                name=f"{prefix}.embedding_prompt_tokens_missing_total",
                value=prompt_tokens_missing_total,
                unit="count",
            )
        if cost_missing_total > 0:
            repository.record_metric(
                run_id=run_id,
                name=f"{prefix}.embedding_cost_missing_total",
                value=cost_missing_total,
                unit="count",
            )
    return hits
