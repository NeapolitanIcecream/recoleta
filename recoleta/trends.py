from __future__ import annotations

import json
import time
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

from loguru import logger
from pydantic import BaseModel, Field

from recoleta.storage import Repository


@dataclass(slots=True)
class SemanticSearchHit:
    chunk_id: int
    doc_id: int
    chunk_index: int
    score: float
    text_preview: str


def ensure_summary_embeddings_for_period(*_, **__: Any) -> dict[str, Any]:
    raise RuntimeError(
        "SQLite embedding persistence has been removed; use LanceDB vector sync instead."
    )


def semantic_search_summaries_in_period(
    *,
    repository: Repository,
    lancedb_dir: Path,
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
    from recoleta.rag.semantic_search import (
        semantic_search_summaries_in_period as _semantic_search,
    )
    from recoleta.rag.vector_store import LanceVectorStore, embedding_table_name

    store = LanceVectorStore(
        db_dir=Path(lancedb_dir),
        table_name=embedding_table_name(
            embedding_model=embedding_model, embedding_dimensions=embedding_dimensions
        ),
    )
    hits = _semantic_search(
        repository=repository,
        vector_store=store,
        run_id=run_id,
        doc_type=doc_type,
        period_start=period_start,
        period_end=period_end,
        query=query,
        embedding_model=embedding_model,
        embedding_dimensions=embedding_dimensions,
        max_batch_inputs=max_batch_inputs,
        max_batch_chars=max_batch_chars,
        embedding_failure_mode=embedding_failure_mode,
        embedding_max_errors=embedding_max_errors,
        limit=limit,
        corpus_limit=corpus_limit,
    )
    return [
        SemanticSearchHit(
            chunk_id=h.chunk_id,
            doc_id=h.doc_id,
            chunk_index=h.chunk_index,
            score=h.score,
            text_preview=h.text_preview,
        )
        for h in hits
    ]


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
    content_chunks_deleted = 0

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
                content_chunks_deleted += repository.delete_document_chunks(
                    doc_id=doc_id,
                    kind="content",
                    chunk_index_gte=1,
                )
                continue

            segments = _chunk_text_segments(chosen, chunk_chars=content_chunk_chars)
            max_written_index: int | None = None
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
                max_written_index = seg_idx

            if max_written_index is None:
                content_chunks_deleted += repository.delete_document_chunks(
                    doc_id=doc_id,
                    kind="content",
                    chunk_index_gte=1,
                )
            else:
                content_chunks_deleted += repository.delete_document_chunks(
                    doc_id=doc_id,
                    kind="content",
                    chunk_index_gte=max_written_index + 1,
                )
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
        "content_chunks_deleted": content_chunks_deleted,
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
    embedding_failure_mode: str = "continue",
    embedding_max_errors: int = 0,
    lancedb_dir: Path,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
    corpus_doc_type: str,
    corpus_granularity: str | None = None,
    include_debug: bool = False,
) -> tuple[TrendPayload, dict[str, Any] | None]:
    from recoleta.rag.agent import generate_trend_payload
    from recoleta.rag.vector_store import LanceVectorStore, embedding_table_name

    store = LanceVectorStore(
        db_dir=Path(lancedb_dir),
        table_name=embedding_table_name(
            embedding_model=embedding_model, embedding_dimensions=embedding_dimensions
        ),
    )
    return generate_trend_payload(
        repository=repository,
        vector_store=store,
        run_id=run_id,
        llm_model=llm_model,
        embedding_model=embedding_model,
        embedding_dimensions=embedding_dimensions,
        embedding_batch_max_inputs=embedding_batch_max_inputs,
        embedding_batch_max_chars=embedding_batch_max_chars,
        embedding_failure_mode=embedding_failure_mode,
        embedding_max_errors=embedding_max_errors,
        granularity=granularity,
        period_start=period_start,
        period_end=period_end,
        corpus_doc_type=corpus_doc_type,
        corpus_granularity=corpus_granularity,
        include_debug=include_debug,
    )


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
