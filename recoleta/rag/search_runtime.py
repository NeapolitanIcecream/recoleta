from __future__ import annotations

from collections import OrderedDict
import time
from threading import Lock
from typing import Any

from loguru import logger

from recoleta.rag.embeddings import LiteLLMEmbedder, iter_embedding_batches
from recoleta.rag.search_models import (
    SemanticSearchHit,
    SummarySearchRequest,
    SummaryVectorSyncRequest,
)
from recoleta.rag.vector_store import VectorRow

_SUMMARY_CORPUS_CACHE_MAX_KEYS = 64
_summary_corpus_cache_lock = Lock()
_summary_corpus_cache: OrderedDict[tuple[Any, ...], dict[str, Any]] = OrderedDict()


def _duration_ms(started: float) -> int:
    return int((time.perf_counter() - started) * 1000)


def _normalize_embedding_model(value: str) -> str:
    normalized = str(value or "").strip()
    if not normalized:
        raise ValueError("embedding_model must not be empty")
    return normalized


def _normalize_failure_mode(value: str | None) -> str:
    normalized = str(value or "").strip().lower() or "continue"
    if normalized not in {"continue", "fail_fast", "threshold"}:
        raise ValueError(
            "embedding_failure_mode must be one of: continue, fail_fast, threshold"
        )
    return normalized


def _normalize_max_errors(*, failure_mode: str, raw_value: int) -> int:
    normalized = max(0, int(raw_value or 0))
    if failure_mode == "threshold" and normalized <= 0:
        raise ValueError(
            "embedding_max_errors must be a positive integer when embedding_failure_mode=threshold"
        )
    return normalized


def _sync_stats(
    *,
    candidate_chunk_ids: list[int],
    skipped_total: int,
    failure_mode: str,
    max_errors: int,
    duration_ms: int,
) -> dict[str, Any]:
    return {
        "chunks_total": len(candidate_chunk_ids),
        "candidate_chunk_ids": candidate_chunk_ids,
        "embedded_total": 0,
        "skipped_total": skipped_total,
        "embedding_calls_total": 0,
        "embedding_errors_total": 0,
        "embedding_prompt_tokens_total": 0,
        "embedding_prompt_tokens_missing_total": 0,
        "embedding_cost_usd_total": 0.0,
        "embedding_cost_missing_total": 0,
        "embedding_failure_mode": failure_mode,
        "embedding_max_errors": max_errors,
        "duration_ms": duration_ms,
    }


def _candidate_rows(request: SummaryVectorSyncRequest) -> list[dict[str, Any]]:
    return request.window.repository.list_summary_chunk_index_rows_in_period(
        doc_type=request.window.doc_type,
        granularity=request.window.granularity,
        period_start=request.window.period_start,
        period_end=request.window.period_end,
        limit=request.limit,
        offset=request.offset,
    )


def _candidate_chunk_ids(rows: list[dict[str, Any]]) -> list[int]:
    return [int(row["chunk_id"]) for row in rows if int(row.get("chunk_id") or 0) > 0]


def _rows_to_embed(
    *,
    rows: list[dict[str, Any]],
    existing_hashes: dict[int, str],
) -> tuple[list[dict[str, Any]], int]:
    to_embed_rows: list[dict[str, Any]] = []
    skipped_total = 0
    for row in rows:
        chunk_id = int(row.get("chunk_id") or 0)
        if chunk_id <= 0:
            continue
        text = str(row.get("text") or "").strip()
        if not text:
            continue
        text_hash = str(row.get("text_hash") or "").strip()
        if existing_hashes.get(chunk_id) == text_hash:
            skipped_total += 1
            continue
        to_embed_rows.append(row)
    return to_embed_rows, skipped_total


def _merge_embedding_debug(stats: dict[str, Any], embed_debug: Any) -> None:
    if isinstance(embed_debug, dict):
        raw_prompt = embed_debug.get("prompt_tokens")
        if raw_prompt is None:
            raw_prompt = embed_debug.get("total_tokens")
        if isinstance(raw_prompt, (int, float)):
            stats["embedding_prompt_tokens_total"] += int(raw_prompt)
        else:
            stats["embedding_prompt_tokens_missing_total"] += 1
        raw_cost = embed_debug.get("cost_usd")
        if isinstance(raw_cost, (int, float)):
            stats["embedding_cost_usd_total"] += float(raw_cost)
        else:
            stats["embedding_cost_missing_total"] += 1
        return
    stats["embedding_prompt_tokens_missing_total"] += 1
    stats["embedding_cost_missing_total"] += 1


def _embedding_stats() -> dict[str, Any]:
    return {
        "embedding_calls_total": 0,
        "embedding_errors_total": 0,
        "embedded_total": 0,
        "embedding_prompt_tokens_total": 0,
        "embedding_prompt_tokens_missing_total": 0,
        "embedding_cost_usd_total": 0.0,
        "embedding_cost_missing_total": 0,
    }


def _should_raise_embedding_error(
    *,
    failure_mode: str,
    errors_total: int,
    max_errors: int,
) -> bool:
    if failure_mode == "fail_fast":
        return True
    return failure_mode == "threshold" and max_errors > 0 and errors_total >= max_errors


def _vector_rows(batch_rows: list[dict[str, Any]], vectors: list[list[float]]) -> list[VectorRow]:
    out: list[VectorRow] = []
    for row, vector in zip(batch_rows, vectors, strict=True):
        out.append(
            VectorRow(
                chunk_id=int(row["chunk_id"]),
                doc_id=int(row["doc_id"]),
                doc_type=str(row["doc_type"]),
                chunk_index=int(row["chunk_index"]),
                kind=str(row["kind"]),
                text_hash=str(row["text_hash"]),
                text_preview=str(row.get("text_preview") or ""),
                event_start_ts=float(row["event_start_ts"]),
                event_end_ts=float(row["event_end_ts"]),
                vector=[float(value) for value in vector],
            )
        )
    return out


def _upsert_embedded_batch(
    *,
    embedder: LiteLLMEmbedder,
    request: SummaryVectorSyncRequest,
    batch_rows: list[dict[str, Any]],
    model: str,
    stats: dict[str, Any],
) -> int:
    batch = [str(row["text"]) for row in batch_rows]
    vectors, embed_debug = embedder.embed(
        model=model,
        inputs=batch,
        dimensions=request.embedding_dimensions,
    )
    _merge_embedding_debug(stats, embed_debug)
    if len(vectors) != len(batch):
        raise ValueError("embedding output size mismatch")
    return request.window.vector_store.upsert_rows(rows=_vector_rows(batch_rows, vectors))


def _handle_embedding_batch_failure(
    *,
    log: Any,
    stats: dict[str, Any],
    exc: Exception,
    failure_mode: str,
    max_errors: int,
) -> None:
    stats["embedding_errors_total"] += 1
    log.warning(
        "Vector sync batch failed embedded_so_far={} error_type={} error={}",
        int(stats["embedded_total"]),
        type(exc).__name__,
        str(exc),
    )
    if not _should_raise_embedding_error(
        failure_mode=failure_mode,
        errors_total=int(stats["embedding_errors_total"]),
        max_errors=max_errors,
    ):
        return
    log.warning(
        "Vector sync aborting ({}) calls={} errors={}{}",
        failure_mode,
        int(stats["embedding_calls_total"]),
        int(stats["embedding_errors_total"]),
        f" max_errors={max_errors}" if failure_mode == "threshold" else "",
    )
    raise exc


def _embed_summary_rows(
    *,
    request: SummaryVectorSyncRequest,
    rows: list[dict[str, Any]],
    model: str,
    failure_policy: tuple[str, int],
    log: Any,
) -> dict[str, Any]:
    stats = _embedding_stats()
    embedder = LiteLLMEmbedder(llm_connection=request.llm_connection)
    failure_mode, max_errors = failure_policy
    texts = [str(row["text"]) for row in rows]
    index = 0
    for batch in iter_embedding_batches(
        texts,
        max_batch_inputs=request.max_batch_inputs,
        max_batch_chars=request.max_batch_chars,
    ):
        batch_rows = rows[index : index + len(batch)]
        index += len(batch)
        try:
            stats["embedding_calls_total"] += 1
            stats["embedded_total"] += _upsert_embedded_batch(
                embedder=embedder,
                request=request,
                batch_rows=batch_rows,
                model=model,
                stats=stats,
            )
        except Exception as exc:
            _handle_embedding_batch_failure(
                log=log,
                stats=stats,
                exc=exc,
                failure_mode=failure_mode,
                max_errors=max_errors,
            )
    return stats


def _raise_if_all_batches_failed(
    *,
    failure_mode: str,
    stats: dict[str, Any],
    log: Any,
) -> None:
    if failure_mode != "threshold":
        return
    if int(stats.get("embedding_calls_total") or 0) <= 0:
        return
    if int(stats.get("embedded_total") or 0) > 0:
        return
    if int(stats.get("embedding_errors_total") or 0) < int(
        stats.get("embedding_calls_total") or 0
    ):
        return
    log.warning(
        "Vector sync aborted (all batches failed) calls={} errors={}",
        int(stats.get("embedding_calls_total") or 0),
        int(stats.get("embedding_errors_total") or 0),
    )
    raise RuntimeError("vector sync failed: all embedding batches failed")


def _finalize_sync_stats(
    *,
    base: dict[str, Any],
    embedded_stats: dict[str, Any],
    duration_ms: int,
) -> dict[str, Any]:
    out = dict(base)
    out.update(embedded_stats)
    out["duration_ms"] = duration_ms
    return out


def _summary_corpus_cache_key(request: SummarySearchRequest) -> tuple[Any, ...]:
    window = request.window
    return (
        str(window.run_id or "").strip(),
        str(window.doc_type or "").strip().lower(),
        str(window.granularity or "").strip().lower(),
        window.period_start.isoformat(),
        window.period_end.isoformat(),
        str(request.embedding_model or "").strip(),
        int(request.embedding_dimensions) if request.embedding_dimensions is not None else None,
        int(request.max_batch_inputs),
        int(request.max_batch_chars),
        str(request.embedding_failure_mode or "").strip().lower(),
        int(request.embedding_max_errors or 0),
        int(request.corpus_limit),
        0,
        str(getattr(window.vector_store, "db_dir", "")),
        str(getattr(window.vector_store, "table_name", "")),
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
        cloned["duration_ms"] = 0
    return cloned


def _should_cache_summary_index_stats(stats: dict[str, Any]) -> bool:
    return int(stats.get("embedding_errors_total") or 0) <= 0


def ensure_summary_vectors_for_period(request: SummaryVectorSyncRequest) -> dict[str, Any]:
    started = time.perf_counter()
    log = logger.bind(
        module="rag.semantic_index",
        run_id=request.window.run_id,
        doc_type=request.window.doc_type,
    )
    normalized_model = _normalize_embedding_model(request.embedding_model)
    failure_mode = _normalize_failure_mode(request.embedding_failure_mode)
    max_errors = _normalize_max_errors(
        failure_mode=failure_mode,
        raw_value=request.embedding_max_errors,
    )
    rows = _candidate_rows(request)
    if not rows:
        return _sync_stats(
            candidate_chunk_ids=[],
            skipped_total=0,
            failure_mode=failure_mode,
            max_errors=max_errors,
            duration_ms=_duration_ms(started),
        )
    chunk_ids = _candidate_chunk_ids(rows)
    existing_hashes = request.window.vector_store.fetch_existing_hashes(chunk_ids=chunk_ids)
    to_embed_rows, skipped_total = _rows_to_embed(rows=rows, existing_hashes=existing_hashes)
    base = _sync_stats(
        candidate_chunk_ids=chunk_ids,
        skipped_total=skipped_total,
        failure_mode=failure_mode,
        max_errors=max_errors,
        duration_ms=_duration_ms(started),
    )
    if not to_embed_rows:
        return base
    embedded_stats = _embed_summary_rows(
        request=request,
        rows=to_embed_rows,
        model=normalized_model,
        failure_policy=(failure_mode, max_errors),
        log=log,
    )
    _raise_if_all_batches_failed(
        failure_mode=failure_mode,
        stats=embedded_stats,
        log=log,
    )
    return _finalize_sync_stats(
        base=base,
        embedded_stats=embedded_stats,
        duration_ms=_duration_ms(started),
    )


def _candidate_chunk_ids_from_rows(rows: list[dict[str, Any]]) -> list[int]:
    return [int(row.get("chunk_id") or 0) for row in rows if int(row.get("chunk_id") or 0) > 0]


def _uncached_index_stats(request: SummarySearchRequest) -> dict[str, Any]:
    candidate_rows = request.window.repository.list_summary_chunk_index_rows_in_period(
        doc_type=request.window.doc_type,
        granularity=request.window.granularity,
        period_start=request.window.period_start,
        period_end=request.window.period_end,
        limit=request.corpus_limit,
        offset=0,
    )
    candidate_chunk_ids = _candidate_chunk_ids_from_rows(candidate_rows)
    return {
        "chunks_total": len(candidate_chunk_ids),
        "candidate_chunk_ids": candidate_chunk_ids,
        "embedded_total": 0,
        "skipped_total": len(candidate_chunk_ids),
        "embedding_calls_total": 0,
        "embedding_errors_total": 0,
        "embedding_prompt_tokens_total": 0,
        "embedding_prompt_tokens_missing_total": 0,
        "embedding_cost_usd_total": 0.0,
        "embedding_cost_missing_total": 0,
        "embedding_failure_mode": str(request.embedding_failure_mode or "").strip().lower()
        or "continue",
        "embedding_max_errors": int(request.embedding_max_errors or 0),
        "corpus_cache_hit": False,
    }


def _warm_index_stats(request: SummarySearchRequest) -> dict[str, Any]:
    cache_key = _summary_corpus_cache_key(request)
    cached_stats: dict[str, Any] | None = None
    with _summary_corpus_cache_lock:
        cached_stats = _summary_corpus_cache.get(cache_key)
        if cached_stats is not None:
            _summary_corpus_cache.move_to_end(cache_key)
    if cached_stats is not None:
        return _clone_summary_index_stats(cached_stats, cache_hit=True)
    from recoleta.rag import semantic_search as rag_semantic

    fresh_index_stats = rag_semantic.ensure_summary_vectors_for_period(
        repository=request.window.repository,
        vector_store=request.window.vector_store,
        run_id=request.window.run_id,
        doc_type=request.window.doc_type,
        granularity=request.window.granularity,
        period_start=request.window.period_start,
        period_end=request.window.period_end,
        embedding_model=request.embedding_model,
        embedding_dimensions=request.embedding_dimensions,
        max_batch_inputs=request.max_batch_inputs,
        max_batch_chars=request.max_batch_chars,
        embedding_failure_mode=request.embedding_failure_mode,
        embedding_max_errors=request.embedding_max_errors,
        limit=request.corpus_limit,
        offset=0,
        llm_connection=request.llm_connection,
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
    return _clone_summary_index_stats(fresh_index_stats, cache_hit=False)


def _record_search_duration_metric(
    *,
    request: SummarySearchRequest,
    normalized_doc_type: str,
    duration_ms: int,
) -> None:
    if request.metric_namespace is None or not str(request.metric_namespace).strip():
        return
    request.window.repository.record_metric(
        run_id=request.window.run_id,
        name=(
            f"{str(request.metric_namespace).strip()}.semantic_search."
            f"{normalized_doc_type}.duration_ms"
        ),
        value=duration_ms,
        unit="ms",
    )


def _query_vector(request: SummarySearchRequest) -> tuple[list[float], Any]:
    embedder = LiteLLMEmbedder(llm_connection=request.llm_connection)
    query_vectors, query_debug = embedder.embed(
        model=_normalize_embedding_model(request.embedding_model),
        inputs=[f"Query: {str(request.query or '').strip()}"],
        dimensions=request.embedding_dimensions,
    )
    if len(query_vectors) != 1:
        raise ValueError("query embedding output size mismatch")
    return query_vectors[0], query_debug


def _sanitize_where_string(value: str) -> str:
    return str(value).replace("'", "''")


def _candidate_where_clause(
    request: SummarySearchRequest,
    *,
    candidate_chunk_ids: list[int],
) -> str:
    start_ts = float(request.window.period_start.timestamp())
    end_ts = float(request.window.period_end.timestamp())
    return (
        "kind = 'summary' "
        f"AND doc_type = '{_sanitize_where_string(str(request.window.doc_type).strip().lower())}' "
        f"AND event_start_ts < {end_ts} AND event_end_ts >= {start_ts} "
        f"AND chunk_id IN ({', '.join(str(chunk_id) for chunk_id in candidate_chunk_ids)})"
    )


def _rows_to_hits(rows: list[dict[str, Any]]) -> list[SemanticSearchHit]:
    hits: list[SemanticSearchHit] = []
    for row in rows:
        raw_distance = row.get("_distance")
        try:
            distance = float(raw_distance) if raw_distance is not None else 1.0
        except Exception:
            distance = 1.0
        hits.append(
            SemanticSearchHit(
                chunk_id=int(row.get("chunk_id") or 0),
                doc_id=int(row.get("doc_id") or 0),
                chunk_index=int(row.get("chunk_index") or 0),
                score=max(0.0, min(1.0, 1.0 - distance)),
                text_preview=str(row.get("text_preview") or ""),
            )
        )
    return hits


def _metric_totals(index_stats: dict[str, Any], query_debug: Any) -> dict[str, float | int | bool]:
    prompt_tokens_total = int(index_stats.get("embedding_prompt_tokens_total") or 0)
    prompt_tokens_missing_total = int(index_stats.get("embedding_prompt_tokens_missing_total") or 0)
    cost_usd_total = float(index_stats.get("embedding_cost_usd_total") or 0.0)
    cost_missing_total = int(index_stats.get("embedding_cost_missing_total") or 0)
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
    return {
        "calls_total": int(index_stats.get("embedding_calls_total") or 0) + 1,
        "errors_total": int(index_stats.get("embedding_errors_total") or 0),
        "prompt_tokens_total": prompt_tokens_total,
        "prompt_tokens_missing_total": prompt_tokens_missing_total,
        "cost_usd_total": cost_usd_total,
        "cost_missing_total": cost_missing_total,
        "cache_hit": bool(index_stats.get("corpus_cache_hit")),
    }


def _record_search_metrics(
    *,
    request: SummarySearchRequest,
    normalized_doc_type: str,
    index_stats: dict[str, Any],
    query_debug: Any,
) -> None:
    if request.metric_namespace is None or not str(request.metric_namespace).strip():
        return
    repository = request.window.repository
    prefix = str(request.metric_namespace).strip()
    totals = _metric_totals(index_stats, query_debug)
    repository.record_metric(
        run_id=request.window.run_id,
        name=f"{prefix}.embedding_calls_total",
        value=float(totals["calls_total"]),
        unit="count",
    )
    repository.record_metric(
        run_id=request.window.run_id,
        name=f"{prefix}.embedding_errors_total",
        value=float(totals["errors_total"]),
        unit="count",
    )
    repository.record_metric(
        run_id=request.window.run_id,
        name=(
            f"{prefix}.corpus_cache_hits_total"
            if totals["cache_hit"]
            else f"{prefix}.corpus_cache_misses_total"
        ),
        value=1,
        unit="count",
    )
    repository.record_metric(
        run_id=request.window.run_id,
        name=f"{prefix}.semantic_index.{normalized_doc_type}.duration_ms",
        value=float(int(index_stats.get("duration_ms") or 0)),
        unit="ms",
    )
    if int(totals["prompt_tokens_total"]) > 0:
        repository.record_metric(
            run_id=request.window.run_id,
            name=f"{prefix}.embedding_prompt_tokens_total",
            value=float(totals["prompt_tokens_total"]),
            unit="count",
        )
    if float(totals["cost_usd_total"]) > 0.0:
        repository.record_metric(
            run_id=request.window.run_id,
            name=f"{prefix}.embedding_estimated_cost_usd",
            value=float(totals["cost_usd_total"]),
            unit="usd",
        )
    if int(totals["prompt_tokens_missing_total"]) > 0:
        repository.record_metric(
            run_id=request.window.run_id,
            name=f"{prefix}.embedding_prompt_tokens_missing_total",
            value=float(totals["prompt_tokens_missing_total"]),
            unit="count",
        )
    if int(totals["cost_missing_total"]) > 0:
        repository.record_metric(
            run_id=request.window.run_id,
            name=f"{prefix}.embedding_cost_missing_total",
            value=float(totals["cost_missing_total"]),
            unit="count",
        )


def semantic_search_summaries_in_period(
    request: SummarySearchRequest,
) -> list[SemanticSearchHit]:
    log = logger.bind(
        module="rag.semantic_search",
        run_id=request.window.run_id,
        doc_type=request.window.doc_type,
    )
    started = time.perf_counter()
    normalized_doc_type = str(request.window.doc_type or "").strip().lower() or "unknown"
    normalized_query = str(request.query or "").strip()
    if not normalized_query:
        _record_search_duration_metric(
            request=request,
            normalized_doc_type=normalized_doc_type,
            duration_ms=_duration_ms(started),
        )
        return []
    index_stats = (
        _warm_index_stats(request)
        if request.auto_sync_vectors
        else _uncached_index_stats(request)
    )
    candidate_chunk_ids = [
        int(chunk_id)
        for chunk_id in list(index_stats.get("candidate_chunk_ids") or [])
        if int(chunk_id or 0) > 0
    ]
    if not candidate_chunk_ids:
        log.info("Semantic search skipped: empty candidate corpus")
        _record_search_duration_metric(
            request=request,
            normalized_doc_type=normalized_doc_type,
            duration_ms=_duration_ms(started),
        )
        return []
    if not request.auto_sync_vectors and request.window.vector_store.try_open_table() is None:
        log.info("Semantic search skipped: vector table missing and auto_sync_vectors=false")
        _record_search_duration_metric(
            request=request,
            normalized_doc_type=normalized_doc_type,
            duration_ms=_duration_ms(started),
        )
        return []
    query_vector, query_debug = _query_vector(request)
    rows = request.window.vector_store.search(
        query_vector=query_vector,
        where=_candidate_where_clause(request, candidate_chunk_ids=candidate_chunk_ids),
        limit=request.limit,
        metric="cosine",
        select_columns=["chunk_id", "doc_id", "chunk_index", "text_preview", "_distance"],
    )
    hits = _rows_to_hits(rows)
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
    _record_search_metrics(
        request=request,
        normalized_doc_type=normalized_doc_type,
        index_stats=index_stats,
        query_debug=query_debug,
    )
    _record_search_duration_metric(
        request=request,
        normalized_doc_type=normalized_doc_type,
        duration_ms=_duration_ms(started),
    )
    return hits
