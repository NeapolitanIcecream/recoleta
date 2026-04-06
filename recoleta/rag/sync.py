from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import time
from typing import Any

from loguru import logger

from recoleta.llm_connection import LLMConnectionConfig
from recoleta.ports import TrendRepositoryPort
from recoleta.rag.semantic_search import ensure_summary_vectors_for_period
from recoleta.rag.search_models import SummaryCorpusWindow, SummaryVectorSyncRequest
from recoleta.rag.vector_store import LanceVectorStore


def _int_with_default(value: Any, *, default: int) -> int:
    return default if value is None else int(value)


@dataclass(frozen=True, slots=True)
class SummaryVectorSyncRunRequest:
    repository: TrendRepositoryPort
    vector_store: LanceVectorStore
    run_id: str
    doc_type: str
    period_start: datetime
    period_end: datetime
    embedding_model: str
    embedding_dimensions: int | None
    max_batch_inputs: int
    max_batch_chars: int
    embedding_failure_mode: str = "continue"
    embedding_max_errors: int = 0
    page_size: int = 500
    max_pages: int = 10_000
    llm_connection: LLMConnectionConfig | None = None


def _coerce_summary_vector_sync_run_request(
    *,
    request: SummaryVectorSyncRunRequest | None = None,
    legacy_kwargs: dict[str, Any] | None = None,
) -> SummaryVectorSyncRunRequest:
    if request is not None:
        return request
    values = dict(legacy_kwargs or {})
    return SummaryVectorSyncRunRequest(
        repository=values["repository"],
        vector_store=values["vector_store"],
        run_id=str(values["run_id"]),
        doc_type=str(values["doc_type"]),
        period_start=values["period_start"],
        period_end=values["period_end"],
        embedding_model=str(values["embedding_model"]),
        embedding_dimensions=values.get("embedding_dimensions"),
        max_batch_inputs=int(values["max_batch_inputs"]),
        max_batch_chars=int(values["max_batch_chars"]),
        embedding_failure_mode=str(values.get("embedding_failure_mode") or "continue"),
        embedding_max_errors=int(values.get("embedding_max_errors") or 0),
        page_size=_int_with_default(values.get("page_size"), default=500),
        max_pages=_int_with_default(values.get("max_pages"), default=10_000),
        llm_connection=values.get("llm_connection"),
    )


def _empty_sync_totals() -> dict[str, float | int]:
    return {
        "chunks_total": 0,
        "embedded_total": 0,
        "skipped_total": 0,
        "embedding_calls_total": 0,
        "embedding_errors_total": 0,
        "embedding_prompt_tokens_total": 0,
        "embedding_prompt_tokens_missing_total": 0,
        "embedding_cost_usd_total": 0.0,
        "embedding_cost_missing_total": 0,
    }


def _accumulate_sync_totals(
    totals: dict[str, float | int],
    *,
    stats: dict[str, Any],
) -> int:
    page_chunks = int(stats.get("chunks_total") or 0)
    if page_chunks <= 0:
        return 0
    for key in (
        "chunks_total",
        "embedded_total",
        "skipped_total",
        "embedding_calls_total",
        "embedding_errors_total",
        "embedding_prompt_tokens_total",
        "embedding_prompt_tokens_missing_total",
        "embedding_cost_missing_total",
    ):
        totals[key] = int(totals.get(key) or 0) + int(stats.get(key) or 0)
    totals["embedding_cost_usd_total"] = float(
        totals.get("embedding_cost_usd_total") or 0.0
    ) + float(stats.get("embedding_cost_usd_total") or 0.0)
    return page_chunks


def _record_sync_metric(
    repository: TrendRepositoryPort,
    *,
    run_id: str,
    name: str,
    value: float,
    unit: str,
) -> None:
    repository.record_metric(run_id=run_id, name=name, value=value, unit=unit)


def _record_sync_metrics(
    *,
    repository: TrendRepositoryPort,
    run_id: str,
    totals: dict[str, float | int],
    started: float,
) -> None:
    _record_sync_metric(
        repository,
        run_id=run_id,
        name="pipeline.rag.sync.embedding_calls_total",
        value=float(totals["embedding_calls_total"]),
        unit="count",
    )
    _record_sync_metric(
        repository,
        run_id=run_id,
        name="pipeline.rag.sync.embedding_errors_total",
        value=float(totals["embedding_errors_total"]),
        unit="count",
    )
    if int(totals["embedding_prompt_tokens_total"]) > 0:
        _record_sync_metric(
            repository,
            run_id=run_id,
            name="pipeline.rag.sync.embedding_prompt_tokens_total",
            value=float(totals["embedding_prompt_tokens_total"]),
            unit="count",
        )
    if float(totals["embedding_cost_usd_total"]) > 0.0:
        _record_sync_metric(
            repository,
            run_id=run_id,
            name="pipeline.rag.sync.embedding_estimated_cost_usd",
            value=float(totals["embedding_cost_usd_total"]),
            unit="usd",
        )
    if int(totals["embedding_prompt_tokens_missing_total"]) > 0:
        _record_sync_metric(
            repository,
            run_id=run_id,
            name="pipeline.rag.sync.embedding_prompt_tokens_missing_total",
            value=float(totals["embedding_prompt_tokens_missing_total"]),
            unit="count",
        )
    if int(totals["embedding_cost_missing_total"]) > 0:
        _record_sync_metric(
            repository,
            run_id=run_id,
            name="pipeline.rag.sync.embedding_cost_missing_total",
            value=float(totals["embedding_cost_missing_total"]),
            unit="count",
        )
    _record_sync_metric(
        repository,
        run_id=run_id,
        name="pipeline.rag.sync.duration_ms",
        value=float(int((time.perf_counter() - started) * 1000)),
        unit="ms",
    )


def sync_summary_vectors_in_period(
    request: SummaryVectorSyncRunRequest | None = None,
    **legacy_kwargs: Any,
) -> dict[str, Any]:
    """Rebuild/sync vectors by paging through the SQLite corpus window."""

    resolved_request = _coerce_summary_vector_sync_run_request(
        request=request,
        legacy_kwargs=legacy_kwargs,
    )
    log = logger.bind(
        module="rag.sync",
        run_id=resolved_request.run_id,
        doc_type=resolved_request.doc_type,
    )
    started = time.perf_counter()
    normalized_page = max(1, min(int(resolved_request.page_size), 5000))
    normalized_max_pages = max(1, int(resolved_request.max_pages))
    totals = _empty_sync_totals()
    window = SummaryCorpusWindow(
        repository=resolved_request.repository,
        vector_store=resolved_request.vector_store,
        run_id=resolved_request.run_id,
        doc_type=resolved_request.doc_type,
        period_start=resolved_request.period_start,
        period_end=resolved_request.period_end,
    )

    for page in range(normalized_max_pages):
        offset = page * normalized_page
        stats = ensure_summary_vectors_for_period(
            request=SummaryVectorSyncRequest(
                window=window,
                embedding_model=resolved_request.embedding_model,
                embedding_dimensions=resolved_request.embedding_dimensions,
                max_batch_inputs=resolved_request.max_batch_inputs,
                max_batch_chars=resolved_request.max_batch_chars,
                embedding_failure_mode=resolved_request.embedding_failure_mode,
                embedding_max_errors=resolved_request.embedding_max_errors,
                limit=normalized_page,
                offset=offset,
                llm_connection=resolved_request.llm_connection,
            )
        )
        page_chunks = _accumulate_sync_totals(totals, stats=stats)
        if page_chunks <= 0:
            break
        if page_chunks < normalized_page:
            break

    _record_sync_metrics(
        repository=resolved_request.repository,
        run_id=resolved_request.run_id,
        totals=totals,
        started=started,
    )

    out = {
        "chunks_total": int(totals["chunks_total"]),
        "embedded_total": int(totals["embedded_total"]),
        "skipped_total": int(totals["skipped_total"]),
        "embedding_calls_total": int(totals["embedding_calls_total"]),
        "embedding_errors_total": int(totals["embedding_errors_total"]),
        "embedding_prompt_tokens_total": int(totals["embedding_prompt_tokens_total"]),
        "embedding_prompt_tokens_missing_total": int(
            totals["embedding_prompt_tokens_missing_total"]
        ),
        "embedding_cost_usd_total": float(totals["embedding_cost_usd_total"]),
        "embedding_cost_missing_total": int(totals["embedding_cost_missing_total"]),
        "embedding_failure_mode": str(resolved_request.embedding_failure_mode or "")
        .strip()
        .lower()
        or "continue",
        "embedding_max_errors": max(0, int(resolved_request.embedding_max_errors or 0)),
        "page_size": normalized_page,
    }
    log.info("Vector sync finished stats={}", out)
    return out
