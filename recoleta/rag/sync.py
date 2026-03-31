from __future__ import annotations

from datetime import datetime
import time
from typing import Any

from loguru import logger

from recoleta.llm_connection import LLMConnectionConfig
from recoleta.ports import TrendRepositoryPort
from recoleta.rag.semantic_search import ensure_summary_vectors_for_period
from recoleta.rag.vector_store import LanceVectorStore


def sync_summary_vectors_in_period(
    *,
    repository: TrendRepositoryPort,
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
    page_size: int = 500,
    max_pages: int = 10_000,
    llm_connection: LLMConnectionConfig | None = None,
) -> dict[str, Any]:
    """Rebuild/sync vectors by paging through the SQLite corpus window."""

    log = logger.bind(module="rag.sync", run_id=run_id, doc_type=doc_type)
    started = time.perf_counter()
    normalized_page = max(1, min(int(page_size), 5000))
    normalized_max_pages = max(1, int(max_pages))

    embedded_total = 0
    skipped_total = 0
    embedding_calls_total = 0
    embedding_errors_total = 0
    embedding_prompt_tokens_total = 0
    embedding_prompt_tokens_missing_total = 0
    embedding_cost_usd_total = 0.0
    embedding_cost_missing_total = 0
    chunks_total = 0

    for page in range(normalized_max_pages):
        offset = page * normalized_page
        stats = ensure_summary_vectors_for_period(
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
            limit=normalized_page,
            offset=offset,
            llm_connection=llm_connection,
        )
        page_chunks = int(stats.get("chunks_total") or 0)
        if page_chunks <= 0:
            break
        chunks_total += page_chunks
        embedded_total += int(stats.get("embedded_total") or 0)
        skipped_total += int(stats.get("skipped_total") or 0)
        embedding_calls_total += int(stats.get("embedding_calls_total") or 0)
        embedding_errors_total += int(stats.get("embedding_errors_total") or 0)
        embedding_prompt_tokens_total += int(
            stats.get("embedding_prompt_tokens_total") or 0
        )
        embedding_prompt_tokens_missing_total += int(
            stats.get("embedding_prompt_tokens_missing_total") or 0
        )
        embedding_cost_usd_total += float(stats.get("embedding_cost_usd_total") or 0.0)
        embedding_cost_missing_total += int(
            stats.get("embedding_cost_missing_total") or 0
        )

        # Heuristic: if fewer rows returned than page_size, we're at the end.
        if page_chunks < normalized_page:
            break

    repository.record_metric(
        run_id=run_id,
        name="pipeline.rag.sync.embedding_calls_total",
        value=float(embedding_calls_total),
        unit="count",
    )
    repository.record_metric(
        run_id=run_id,
        name="pipeline.rag.sync.embedding_errors_total",
        value=float(embedding_errors_total),
        unit="count",
    )
    if embedding_prompt_tokens_total > 0:
        repository.record_metric(
            run_id=run_id,
            name="pipeline.rag.sync.embedding_prompt_tokens_total",
            value=float(embedding_prompt_tokens_total),
            unit="count",
        )
    if embedding_cost_usd_total > 0.0:
        repository.record_metric(
            run_id=run_id,
            name="pipeline.rag.sync.embedding_estimated_cost_usd",
            value=float(embedding_cost_usd_total),
            unit="usd",
        )
    if embedding_prompt_tokens_missing_total > 0:
        repository.record_metric(
            run_id=run_id,
            name="pipeline.rag.sync.embedding_prompt_tokens_missing_total",
            value=float(embedding_prompt_tokens_missing_total),
            unit="count",
        )
    if embedding_cost_missing_total > 0:
        repository.record_metric(
            run_id=run_id,
            name="pipeline.rag.sync.embedding_cost_missing_total",
            value=float(embedding_cost_missing_total),
            unit="count",
        )
    repository.record_metric(
        run_id=run_id,
        name="pipeline.rag.sync.duration_ms",
        value=float(int((time.perf_counter() - started) * 1000)),
        unit="ms",
    )

    out = {
        "chunks_total": chunks_total,
        "embedded_total": embedded_total,
        "skipped_total": skipped_total,
        "embedding_calls_total": embedding_calls_total,
        "embedding_errors_total": embedding_errors_total,
        "embedding_prompt_tokens_total": embedding_prompt_tokens_total,
        "embedding_prompt_tokens_missing_total": embedding_prompt_tokens_missing_total,
        "embedding_cost_usd_total": embedding_cost_usd_total,
        "embedding_cost_missing_total": embedding_cost_missing_total,
        "embedding_failure_mode": str(embedding_failure_mode or "").strip().lower()
        or "continue",
        "embedding_max_errors": max(0, int(embedding_max_errors or 0)),
        "page_size": normalized_page,
    }
    log.info("Vector sync finished stats={}", out)
    return out
