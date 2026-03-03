from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from loguru import logger

from recoleta.rag.embeddings import LiteLLMEmbedder, iter_embedding_batches
from recoleta.rag.vector_store import LanceVectorStore, VectorRow
from recoleta.storage import Repository


@dataclass(slots=True)
class SemanticSearchHit:
    chunk_id: int
    doc_id: int
    chunk_index: int
    score: float
    text_preview: str


def _sanitize_where_string(value: str) -> str:
    # Minimal single-quote escaping for SQL-like filters.
    return str(value).replace("'", "''")


def ensure_summary_vectors_for_period(
    *,
    repository: Repository,
    vector_store: LanceVectorStore,
    run_id: str,
    doc_type: str,
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
        period_start=period_start,
        period_end=period_end,
        limit=limit,
        offset=offset,
    )
    if not rows:
        return {
            "chunks_total": 0,
            "embedded_total": 0,
            "skipped_total": 0,
            "embedding_calls_total": 0,
            "embedding_errors_total": 0,
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
            "embedded_total": 0,
            "skipped_total": skipped_total,
            "embedding_calls_total": 0,
            "embedding_errors_total": 0,
            "embedding_failure_mode": normalized_failure_mode,
            "embedding_max_errors": normalized_max_errors,
        }

    embedder = LiteLLMEmbedder()
    embedding_calls_total = 0
    embedding_errors_total = 0
    embedded_total = 0

    texts = [str(r["text"]) for r in to_embed_rows]
    idx = 0
    for batch in iter_embedding_batches(
        texts, max_batch_inputs=max_batch_inputs, max_batch_chars=max_batch_chars
    ):
        batch_rows = to_embed_rows[idx : idx + len(batch)]
        idx += len(batch)
        try:
            embedding_calls_total += 1
            vectors, _ = embedder.embed(
                model=normalized_model, inputs=batch, dimensions=embedding_dimensions
            )
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
        "embedded_total": embedded_total,
        "skipped_total": skipped_total,
        "embedding_calls_total": embedding_calls_total,
        "embedding_errors_total": embedding_errors_total,
        "embedding_failure_mode": normalized_failure_mode,
        "embedding_max_errors": normalized_max_errors,
    }
    log.info("Vector sync done stats={}", stats)
    return stats


def semantic_search_summaries_in_period(
    *,
    repository: Repository,
    vector_store: LanceVectorStore,
    run_id: str,
    doc_type: str,
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
) -> list[SemanticSearchHit]:
    log = logger.bind(module="rag.semantic_search", run_id=run_id, doc_type=doc_type)
    normalized_query = str(query or "").strip()
    if not normalized_query:
        return []

    index_stats = ensure_summary_vectors_for_period(
        repository=repository,
        vector_store=vector_store,
        run_id=run_id,
        doc_type=doc_type,
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

    start_ts = float(period_start.timestamp())
    end_ts = float(period_end.timestamp())
    where = (
        "kind = 'summary' "
        f"AND doc_type = '{_sanitize_where_string(str(doc_type).strip().lower())}' "
        f"AND event_start_ts < {end_ts} AND event_end_ts >= {start_ts}"
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
        },
    )
    return hits
