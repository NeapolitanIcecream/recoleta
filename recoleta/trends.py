from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any, cast

from loguru import logger
from pydantic import BaseModel, Field

from recoleta.llm_connection import LLMConnectionConfig
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
    llm_connection: LLMConnectionConfig | None = None,
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
        granularity=granularity,
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
        llm_connection=llm_connection,
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

    class RepresentativeChunk(BaseModel):
        doc_id: int
        chunk_index: int
        score: float | None = None

    representative_chunks: list[RepresentativeChunk] = Field(default_factory=list)


class TrendPayload(BaseModel):
    title: str
    granularity: str  # day|week|month
    period_start: str  # ISO datetime (UTC)
    period_end: str  # ISO datetime (UTC)
    overview_md: str
    topics: list[str] = Field(default_factory=list)
    clusters: list[TrendCluster] = Field(default_factory=list)
    highlights: list[str] = Field(default_factory=list)


def prev_level_for_granularity(granularity: str) -> str:
    normalized = str(granularity or "").strip().lower()
    mapping = {
        "day": "item",
        "week": "day",
        "month": "week",
    }
    if normalized in mapping:
        return mapping[normalized]
    raise ValueError("unsupported granularity")


def rag_sources_for_granularity(granularity: str) -> list[dict[str, str | None]]:
    normalized = str(granularity or "").strip().lower()
    if normalized == "day":
        return [{"doc_type": "item", "granularity": None}]
    if normalized == "week":
        return [
            {"doc_type": "item", "granularity": None},
            {"doc_type": "trend", "granularity": "day"},
        ]
    if normalized == "month":
        return [
            {"doc_type": "item", "granularity": None},
            {"doc_type": "trend", "granularity": "day"},
            {"doc_type": "trend", "granularity": "week"},
        ]
    raise ValueError("unsupported granularity")


@dataclass(slots=True)
class TrendGenerationPlan:
    target_granularity: str
    period_start: datetime
    period_end: datetime
    prev_level: str = field(init=False)
    overview_pack_strategy: str = field(init=False)
    rag_sources: list[dict[str, str | None]] = field(init=False)
    rep_source_doc_type: str = field(default="item", init=False)

    def __post_init__(self) -> None:
        normalized = str(self.target_granularity or "").strip().lower()
        if not normalized:
            raise ValueError("target_granularity must not be empty")
        self.target_granularity = normalized
        self.prev_level = prev_level_for_granularity(normalized)
        self.overview_pack_strategy = (
            "item_top_k" if self.prev_level == "item" else "trend_overviews"
        )
        self.rag_sources = rag_sources_for_granularity(normalized)


def _to_utc_datetime(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def _sanitize_inline_text(value: str) -> str:
    normalized = str(value or "")
    normalized = normalized.replace("\r\n", "\n").replace("\r", "\n")
    normalized = normalized.replace("\n", " ").strip()
    if not normalized:
        return ""
    normalized = " ".join(normalized.split())
    return normalized.replace("|", "\\|")


def _truncate_chars(value: str, *, max_chars: int) -> tuple[str, bool]:
    cap = int(max_chars)
    if cap <= 0:
        return "", bool(value)
    if len(value) <= cap:
        return value, False
    return value[:cap], True


def build_overview_pack_md(
    repository: Repository,
    plan: TrendGenerationPlan,
    *,
    overview_pack_max_chars: int,
    item_overview_top_k: int,
    item_overview_item_max_chars: int,
) -> tuple[str, dict[str, Any]]:
    strategy = str(getattr(plan, "overview_pack_strategy", "") or "").strip().lower()
    stats: dict[str, Any] = {"strategy": strategy, "truncated": False}

    lines: list[str] = []
    period_start = _to_utc_datetime(plan.period_start)
    period_end = _to_utc_datetime(plan.period_end)
    lines.append(f"## Overview pack (strategy={strategy})")
    lines.append(
        f"- period_start={period_start.isoformat()} | period_end={period_end.isoformat()}"
    )

    if strategy == "trend_overviews":
        prev_level = str(getattr(plan, "prev_level", "") or "").strip().lower()
        lines.append(f"- prev_level={prev_level}")
        docs = repository.list_documents(
            doc_type="trend",
            granularity=prev_level or None,
            period_start=period_start,
            period_end=period_end,
            order_by="event_asc",
            limit=500,
        )
        docs_by_start: dict[datetime, Any] = {}
        for doc in docs:
            raw_start = getattr(doc, "period_start", None)
            if not isinstance(raw_start, datetime):
                continue
            docs_by_start[_to_utc_datetime(raw_start)] = doc

        if (
            str(getattr(plan, "target_granularity", "") or "").strip().lower() == "week"
            and prev_level == "day"
        ):
            for i in range(7):
                day_start = _to_utc_datetime(period_start + timedelta(days=i))
                token = day_start.date().isoformat()
                doc = docs_by_start.get(day_start)
                if doc is None:
                    lines.append(f"- day {token} | missing | (missing)")
                    continue

                doc_id = int(getattr(doc, "id", 0) or 0)
                chunk = repository.read_document_chunk(doc_id=doc_id, chunk_index=0)
                if chunk is None:
                    lines.append(f"- day {token} | missing_chunk | (missing chunk)")
                    continue
                overview = _sanitize_inline_text(str(getattr(chunk, "text", "") or ""))
                status = "ok"
                if not overview:
                    overview = "(empty)"
                    status = "empty"
                lines.append(f"- day {token} | {status} | {overview}")
        else:
            for doc in docs:
                raw_start = getattr(doc, "period_start", None)
                start = (
                    _to_utc_datetime(raw_start)
                    if isinstance(raw_start, datetime)
                    else None
                )
                token = start.date().isoformat() if isinstance(start, datetime) else "-"
                doc_id = int(getattr(doc, "id", 0) or 0)
                chunk = repository.read_document_chunk(doc_id=doc_id, chunk_index=0)
                if chunk is None:
                    lines.append(f"- {prev_level} {token} | missing_chunk | (missing chunk)")
                    continue
                overview = _sanitize_inline_text(str(getattr(chunk, "text", "") or ""))
                status = "ok"
                if not overview:
                    overview = "(empty)"
                    status = "empty"
                lines.append(f"- {prev_level} {token} | {status} | {overview}")
            if not docs:
                lines.append(f"- {prev_level or 'trend'} - | missing | (no docs)")

    elif strategy == "item_top_k":
        top_k = max(0, int(item_overview_top_k))
        item_max_chars = max(0, int(item_overview_item_max_chars))
        candidate_limit = max(0, min(2000, max(50, top_k * 25)))
        if top_k <= 0:
            lines.append("- items_total=0 | selected=0")
        else:
            pairs = repository.list_analyzed_items_in_period(
                period_start=period_start,
                period_end=period_end,
                limit=candidate_limit,
            )

            def event_at_ts(item: Any) -> float:
                raw = getattr(item, "published_at", None) or getattr(
                    item, "created_at", None
                )
                if isinstance(raw, datetime):
                    return float(_to_utc_datetime(raw).timestamp())
                return 0.0

            def novelty_score(analysis: Any) -> float:
                raw = getattr(analysis, "novelty_score", None)
                if raw is None:
                    return -1.0
                try:
                    return float(raw)
                except Exception:
                    return -1.0

            def relevance_score(analysis: Any) -> float:
                raw = getattr(analysis, "relevance_score", 0.0)
                try:
                    return float(raw)
                except Exception:
                    return 0.0

            def item_id_value(item: Any) -> int:
                raw = getattr(item, "id", 0)
                try:
                    return int(raw or 0)
                except Exception:
                    return 0

            def selection_key(item: Any) -> tuple[str, str]:
                url = str(getattr(item, "canonical_url", "") or "").strip()
                if url:
                    return ("url", url)
                return ("item_id", str(item_id_value(item)))

            sorted_pairs = sorted(
                pairs,
                key=lambda pair: (
                    -relevance_score(pair[1]),
                    -novelty_score(pair[1]),
                    -event_at_ts(pair[0]),
                    -item_id_value(pair[0]),
                ),
            )
            selected: list[tuple[Any, Any]] = []
            seen_selection_keys: set[tuple[str, str]] = set()
            for item, analysis in sorted_pairs:
                key = selection_key(item)
                if key in seen_selection_keys:
                    continue
                seen_selection_keys.add(key)
                selected.append((item, analysis))
                if len(selected) >= top_k:
                    break
            lines.append(
                f"- items_total={len(pairs)} | selected={len(selected)} | top_k={top_k}"
            )
            for rank, (item, analysis) in enumerate(selected, start=1):
                title = (
                    _sanitize_inline_text(str(getattr(item, "title", "") or ""))
                    or "(untitled)"
                )
                url = (
                    _sanitize_inline_text(str(getattr(item, "canonical_url", "") or ""))
                    or "-"
                )
                summary_raw = _sanitize_inline_text(
                    str(getattr(analysis, "summary", "") or "")
                )
                summary = summary_raw[:item_max_chars] if item_max_chars > 0 else ""
                lines.append(
                    f"- rank={rank} | title={title} | url={url} | summary={summary}"
                )

    else:
        lines.append(f"- unsupported_strategy={strategy or '(empty)'}")

    md = "\n".join(lines).rstrip() + "\n"
    md, truncated = _truncate_chars(md, max_chars=int(overview_pack_max_chars))
    stats["truncated"] = bool(truncated)
    stats["chars"] = len(md)
    stats["max_chars"] = int(overview_pack_max_chars)
    return md, stats


def _is_chinese_output_language(output_language: str | None) -> bool:
    normalized = str(output_language or "").strip()
    if not normalized:
        return False
    lowered = normalized.lower()
    return lowered.startswith("zh") or "chinese" in lowered or "中文" in normalized


def build_empty_trend_payload(
    *,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
    output_language: str | None = None,
) -> TrendPayload:
    normalized_granularity = str(granularity or "").strip().lower() or "day"
    if _is_chinese_output_language(output_language):
        title_map = {
            "day": "每日趋势",
            "week": "每周趋势",
            "month": "每月趋势",
        }
        title = title_map.get(normalized_granularity, "趋势")
        overview_md = "- 该周期没有可用文档。"
    else:
        title_map = {
            "day": "Daily Trend",
            "week": "Weekly Trend",
            "month": "Monthly Trend",
        }
        title = title_map.get(normalized_granularity, "Trend")
        overview_md = "- No documents available for this period."
    return TrendPayload(
        title=title,
        granularity=normalized_granularity,
        period_start=period_start.isoformat(),
        period_end=period_end.isoformat(),
        overview_md=overview_md,
        topics=[],
        clusters=[],
        highlights=[],
    )


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
    output_language: str | None = None,
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
    overview_pack_md: str | None = None,
    rag_sources: list[dict[str, str | None]] | None = None,
    ranking_n: int | None = None,
    rep_source_doc_type: str | None = None,
    include_debug: bool = False,
    llm_connection: LLMConnectionConfig | None = None,
) -> tuple[TrendPayload, dict[str, Any] | None]:
    from recoleta.rag.agent import generate_trend_payload
    from recoleta.rag.vector_store import LanceVectorStore, embedding_table_name

    store = LanceVectorStore(
        db_dir=Path(lancedb_dir),
        table_name=embedding_table_name(
            embedding_model=embedding_model, embedding_dimensions=embedding_dimensions
        ),
    )
    generate_trend_payload_any = cast(Any, generate_trend_payload)
    return generate_trend_payload_any(
        repository=repository,
        vector_store=store,
        run_id=run_id,
        llm_model=llm_model,
        output_language=output_language,
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
        overview_pack_md=overview_pack_md,
        rag_sources=rag_sources,
        ranking_n=ranking_n,
        rep_source_doc_type=rep_source_doc_type,
        include_debug=include_debug,
        llm_connection=llm_connection,
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
