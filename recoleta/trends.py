from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta
from enum import StrEnum
from typing import Any, cast

from pydantic import BaseModel, Field, field_validator
from sqlmodel import Session, select

from recoleta.models import Document
from recoleta.ports import TrendRepositoryPort
from recoleta.provenance import (
    build_projection_provenance,
    inject_projection_provenance,
)
from recoleta.publish.trend_render_shared import (
    clamp_trend_overview_markdown,
    sanitize_trend_title,
)


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
    request: Any | None = None,
    **legacy_kwargs: Any,
) -> list[SemanticSearchHit]:
    from recoleta.trends_corpus import (
        coerce_semantic_search_request,
        semantic_search_summaries_in_period_impl,
    )

    normalized_request = coerce_semantic_search_request(
        request=request,
        legacy_kwargs=legacy_kwargs,
    )
    return cast(
        list[SemanticSearchHit],
        semantic_search_summaries_in_period_impl(request=normalized_request),
    )


class TrendCluster(BaseModel):
    name: str
    description: str
    representative_doc_ids: list[int] = Field(default_factory=list)

    class RepresentativeChunk(BaseModel):
        doc_id: int
        chunk_index: int
        score: float | None = None

    representative_chunks: list[RepresentativeChunk] = Field(default_factory=list)


class TrendEvolutionChangeType(StrEnum):
    CONTINUING = "continuing"
    EMERGING = "emerging"
    FADING = "fading"
    SHIFTING = "shifting"
    POLARIZING = "polarizing"


TREND_EVOLUTION_CHANGE_TYPE_VALUES = tuple(
    change_type.value for change_type in TrendEvolutionChangeType
)

_TREND_EVOLUTION_CHANGE_TYPE_ALIASES: dict[str, TrendEvolutionChangeType] = {
    change_type.value: change_type for change_type in TrendEvolutionChangeType
}
_TREND_EVOLUTION_CHANGE_TYPE_ALIASES.update(
    {
        "continue": TrendEvolutionChangeType.CONTINUING,
        "continued": TrendEvolutionChangeType.CONTINUING,
        "continuation": TrendEvolutionChangeType.CONTINUING,
        "ongoing": TrendEvolutionChangeType.CONTINUING,
        "persistent": TrendEvolutionChangeType.CONTINUING,
        "persisting": TrendEvolutionChangeType.CONTINUING,
        "stable": TrendEvolutionChangeType.CONTINUING,
        "strengthening": TrendEvolutionChangeType.CONTINUING,
        "sustained": TrendEvolutionChangeType.CONTINUING,
        "sustaining": TrendEvolutionChangeType.CONTINUING,
        "延续": TrendEvolutionChangeType.CONTINUING,
        "持续": TrendEvolutionChangeType.CONTINUING,
        "继续": TrendEvolutionChangeType.CONTINUING,
        "emerge": TrendEvolutionChangeType.EMERGING,
        "emerged": TrendEvolutionChangeType.EMERGING,
        "emergent": TrendEvolutionChangeType.EMERGING,
        "new": TrendEvolutionChangeType.EMERGING,
        "newly_emerging": TrendEvolutionChangeType.EMERGING,
        "rising": TrendEvolutionChangeType.EMERGING,
        "appearing": TrendEvolutionChangeType.EMERGING,
        "涌现": TrendEvolutionChangeType.EMERGING,
        "新出现": TrendEvolutionChangeType.EMERGING,
        "新兴": TrendEvolutionChangeType.EMERGING,
        "faded": TrendEvolutionChangeType.FADING,
        "declining": TrendEvolutionChangeType.FADING,
        "cooling": TrendEvolutionChangeType.FADING,
        "waning": TrendEvolutionChangeType.FADING,
        "disappearing": TrendEvolutionChangeType.FADING,
        "降温": TrendEvolutionChangeType.FADING,
        "消退": TrendEvolutionChangeType.FADING,
        "淡出": TrendEvolutionChangeType.FADING,
        "shifted": TrendEvolutionChangeType.SHIFTING,
        "shifting_focus": TrendEvolutionChangeType.SHIFTING,
        "evolving": TrendEvolutionChangeType.SHIFTING,
        "reframing": TrendEvolutionChangeType.SHIFTING,
        "reframed": TrendEvolutionChangeType.SHIFTING,
        "diversifying": TrendEvolutionChangeType.SHIFTING,
        "转向": TrendEvolutionChangeType.SHIFTING,
        "变化": TrendEvolutionChangeType.SHIFTING,
        "迁移": TrendEvolutionChangeType.SHIFTING,
        "polarized": TrendEvolutionChangeType.POLARIZING,
        "polarising": TrendEvolutionChangeType.POLARIZING,
        "polarizing_more": TrendEvolutionChangeType.POLARIZING,
        "diverging": TrendEvolutionChangeType.POLARIZING,
        "divergent": TrendEvolutionChangeType.POLARIZING,
        "contested": TrendEvolutionChangeType.POLARIZING,
        "debated": TrendEvolutionChangeType.POLARIZING,
        "分化": TrendEvolutionChangeType.POLARIZING,
        "分歧": TrendEvolutionChangeType.POLARIZING,
        "两极化": TrendEvolutionChangeType.POLARIZING,
    }
)


def _normalize_evolution_token(value: Any) -> str:
    normalized = str(value or "").strip().lower()
    if not normalized:
        return ""
    normalized = normalized.replace("—", "-")
    normalized = re.sub(r"[\s\-]+", "_", normalized)
    return normalized.strip("_")


def normalize_trend_evolution_change_type(
    value: Any,
) -> TrendEvolutionChangeType | None:
    if isinstance(value, TrendEvolutionChangeType):
        return value
    normalized = _normalize_evolution_token(value)
    if not normalized:
        return None
    return _TREND_EVOLUTION_CHANGE_TYPE_ALIASES.get(normalized)


class TrendEvolutionSignal(BaseModel):
    theme: str
    change_type: TrendEvolutionChangeType
    summary: str
    history_windows: list[str] = Field(default_factory=list)

    @field_validator("change_type", mode="before")
    @classmethod
    def _normalize_change_type(cls, value: Any) -> TrendEvolutionChangeType:
        normalized = normalize_trend_evolution_change_type(value)
        if normalized is None:
            allowed = ", ".join(TREND_EVOLUTION_CHANGE_TYPE_VALUES)
            raise ValueError(f"change_type must be one of {allowed}")
        return normalized

    @field_validator("history_windows", mode="before")
    @classmethod
    def _normalize_history_windows(cls, value: Any) -> list[str]:
        if value is None:
            return []
        raw_values = value if isinstance(value, list) else [value]
        normalized: list[str] = []
        seen: set[str] = set()
        for raw in raw_values:
            candidate = " ".join(str(raw or "").split()).strip()
            if not candidate or candidate in seen:
                continue
            seen.add(candidate)
            normalized.append(candidate)
        return normalized


class TrendEvolutionSection(BaseModel):
    summary_md: str
    signals: list[TrendEvolutionSignal] = Field(default_factory=list)


class TrendCounterSignalEvidenceRef(BaseModel):
    doc_id: int
    chunk_index: int = 0
    reason: str | None = None

    @field_validator("doc_id")
    @classmethod
    def _validate_doc_id(cls, value: int) -> int:
        normalized = int(value)
        if normalized <= 0:
            raise ValueError("doc_id must be > 0")
        return normalized

    @field_validator("chunk_index")
    @classmethod
    def _validate_chunk_index(cls, value: int) -> int:
        normalized = int(value)
        if normalized < 0:
            raise ValueError("chunk_index must be >= 0")
        return normalized

    @field_validator("reason")
    @classmethod
    def _validate_optional_reason(cls, value: str | None) -> str | None:
        normalized = " ".join(str(value or "").split()).strip()
        return normalized or None


class TrendCounterSignal(BaseModel):
    title: str
    summary: str
    evidence_refs: list[TrendCounterSignalEvidenceRef] = Field(default_factory=list)

    @field_validator("title", "summary")
    @classmethod
    def _validate_required_text(cls, value: str) -> str:
        normalized = " ".join(str(value or "").split()).strip()
        if not normalized:
            raise ValueError("counter signal text fields must not be empty")
        return normalized


class TrendPayload(BaseModel):
    title: str
    granularity: str  # day|week|month
    period_start: str  # ISO datetime (UTC)
    period_end: str  # ISO datetime (UTC)
    overview_md: str
    topics: list[str] = Field(default_factory=list)
    clusters: list[TrendCluster] = Field(default_factory=list)
    highlights: list[str] = Field(default_factory=list)
    evolution: TrendEvolutionSection | None = None
    counter_signal: TrendCounterSignal | None = None


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
class TrendPeerHistoryWindow:
    window_id: str
    label: str
    period_start: datetime
    period_end: datetime


def _period_token_for_granularity(granularity: str, period_start: datetime) -> str:
    normalized = str(granularity or "").strip().lower()
    start = _to_utc_datetime(period_start)
    if normalized == "day":
        return start.date().isoformat()
    if normalized == "week":
        iso = start.date().isocalendar()
        return f"{iso.year}-W{iso.week:02d}"
    if normalized == "month":
        return f"{start.year:04d}-{start.month:02d}"
    raise ValueError("unsupported granularity")


def _shift_month_start(period_start: datetime, *, months: int) -> datetime:
    start = _to_utc_datetime(period_start)
    month_index = (start.year * 12 + (start.month - 1)) + int(months)
    year = month_index // 12
    month = month_index % 12 + 1
    return datetime(year, month, 1, tzinfo=UTC)


def peer_history_windows_for_period(
    *, granularity: str, period_start: datetime, window_count: int
) -> list[TrendPeerHistoryWindow]:
    normalized = str(granularity or "").strip().lower()
    count = max(0, int(window_count or 0))
    if count <= 0:
        return []

    anchor_start = _to_utc_datetime(period_start)
    windows: list[TrendPeerHistoryWindow] = []
    for idx in range(1, count + 1):
        if normalized == "day":
            start = anchor_start - timedelta(days=idx)
            end = start + timedelta(days=1)
        elif normalized == "week":
            start = anchor_start - timedelta(days=7 * idx)
            end = start + timedelta(days=7)
        elif normalized == "month":
            start = _shift_month_start(anchor_start, months=-idx)
            end = _shift_month_start(anchor_start, months=-(idx - 1))
        else:
            raise ValueError("unsupported granularity")
        windows.append(
            TrendPeerHistoryWindow(
                window_id=f"prev_{idx}",
                label=_period_token_for_granularity(normalized, start),
                period_start=start,
                period_end=end,
            )
        )
    return windows


@dataclass(slots=True)
class TrendGenerationPlan:
    target_granularity: str
    period_start: datetime
    period_end: datetime
    peer_history_window_count: int = 0
    prev_level: str = field(init=False)
    overview_pack_strategy: str = field(init=False)
    rag_sources: list[dict[str, str | None]] = field(init=False)
    rep_source_doc_type: str = field(default="item", init=False)
    peer_history_windows: list[TrendPeerHistoryWindow] = field(
        default_factory=list, init=False
    )

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
        self.peer_history_window_count = max(0, int(self.peer_history_window_count or 0))
        self.peer_history_windows = peer_history_windows_for_period(
            granularity=normalized,
            period_start=self.period_start,
            window_count=self.peer_history_window_count,
        )


_HISTORY_WINDOW_ID_RE = re.compile(r"\bprev_\d+\b", flags=re.IGNORECASE)
_HISTORY_WINDOW_TRIM_CHARS = " \t\r\n()[]{}<>.,;:!?\"'`，；：。！？"


def _normalize_history_window_alias(value: Any) -> str:
    return " ".join(str(value or "").split()).strip().lower()


def _trim_history_window_candidate(value: Any) -> str:
    return str(value or "").strip(_HISTORY_WINDOW_TRIM_CHARS)


def _split_history_window_candidates(raw_values: list[str]) -> list[str]:
    candidates: list[str] = []
    for raw in raw_values:
        normalized = " ".join(str(raw or "").split()).strip()
        if not normalized:
            continue
        parts = re.split(r"[,/|;，；]+", normalized)
        if len(parts) == 1:
            candidates.append(normalized)
            continue
        for part in parts:
            candidate = part.strip()
            if candidate:
                candidates.append(candidate)
    return candidates


def normalize_trend_evolution(
    evolution: TrendEvolutionSection | None,
    *,
    granularity: str,
    period_start: datetime,
    history_windows: list[TrendPeerHistoryWindow] | None,
    available_window_ids: set[str] | None = None,
) -> tuple[TrendEvolutionSection | None, dict[str, int]]:
    from recoleta.trends_overview import normalize_trend_evolution_impl

    return cast(
        tuple[TrendEvolutionSection | None, dict[str, int]],
        normalize_trend_evolution_impl(
            evolution,
            granularity=granularity,
            period_start=period_start,
            history_windows=history_windows,
            available_window_ids=available_window_ids,
        ),
    )


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


def _summary_field_line(
    sections: dict[str, str],
    *,
    field_name: str,
    max_chars: int,
) -> str:
    raw = _sanitize_inline_text(str(sections.get(field_name) or ""))
    if max_chars > 0:
        raw = raw[:max_chars]
    return raw


def _extract_markdown_links(value: str, *, limit: int) -> list[str]:
    links: list[str] = []
    seen: set[str] = set()
    for title, url in re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", str(value or "")):
        normalized = f"[{title}]({url})"
        if normalized in seen:
            continue
        seen.add(normalized)
        links.append(normalized)
        if len(links) >= limit:
            break
    return links


def _trend_payload_summary_lines(
    *,
    repository: TrendRepositoryPort,
    doc: Any,
    token: str,
    entry_label: str,
) -> list[str]:
    from recoleta.trends_overview import trend_payload_summary_lines_impl

    return trend_payload_summary_lines_impl(
        repository=repository,
        doc=doc,
        token=token,
        entry_label=entry_label,
    )


def _truncate_chars(value: str, *, max_chars: int) -> tuple[str, bool]:
    cap = int(max_chars)
    if cap <= 0:
        return "", bool(value)
    if len(value) <= cap:
        return value, False
    return value[:cap], True


def _analysis_relevance_score(analysis: Any) -> float:
    raw = getattr(analysis, "relevance_score", 0.0)
    try:
        return float(raw)
    except Exception:
        return 0.0


def _filter_pairs_by_min_relevance(
    pairs: list[tuple[Any, Any]],
    *,
    min_relevance_score: float,
) -> tuple[list[tuple[Any, Any]], int]:
    threshold = float(min_relevance_score or 0.0)
    if threshold <= 0.0:
        return pairs, 0
    kept = [
        (item, analysis)
        for item, analysis in pairs
        if _analysis_relevance_score(analysis) >= threshold
    ]
    return kept, max(0, len(pairs) - len(kept))


def _prune_item_documents_for_period(
    *,
    repository: TrendRepositoryPort,
    period_start: datetime,
    period_end: datetime,
    keep_item_ids: set[int],
) -> int:
    with Session(repository.engine) as session:
        docs = list(
            session.exec(
                select(Document).where(
                    Document.doc_type == "item",
                    cast(Any, Document.published_at).is_not(None),
                    cast(Any, Document.published_at) >= period_start,
                    cast(Any, Document.published_at) < period_end,
                )
            )
        )
        stale_docs: list[Document] = []
        for doc in docs:
            raw_item_id = getattr(doc, "item_id", None)
            try:
                item_id = int(raw_item_id) if raw_item_id is not None else 0
            except Exception:
                item_id = 0
            if item_id > 0 and item_id in keep_item_ids:
                continue
            stale_docs.append(doc)

        if not stale_docs:
            return 0

        for doc in stale_docs:
            raw_doc_id = getattr(doc, "id", None)
            try:
                doc_id = int(raw_doc_id) if raw_doc_id is not None else 0
            except Exception:
                doc_id = 0
            if doc_id > 0:
                repository.delete_document_chunks(doc_id=doc_id)

        for doc in stale_docs:
            session.delete(doc)
        session.commit()
        return len(stale_docs)


def build_overview_pack_md(
    repository: TrendRepositoryPort | None = None,
    plan: TrendGenerationPlan | None = None,
    *,
    request: Any | None = None,
    **legacy_kwargs: Any,
) -> tuple[str, dict[str, Any]]:
    from recoleta.trends_overview import (
        build_overview_pack_md_impl,
        coerce_build_overview_pack_request,
    )

    normalized_request = coerce_build_overview_pack_request(
        request=request,
        legacy_kwargs={
            "repository": repository if repository is not None else legacy_kwargs["repository"],
            "plan": plan if plan is not None else legacy_kwargs["plan"],
            **legacy_kwargs,
        },
    )
    return build_overview_pack_md_impl(request=normalized_request)


def build_history_pack_md(
    repository: TrendRepositoryPort,
    plan: TrendGenerationPlan,
    *,
    history_pack_max_chars: int,
) -> tuple[str, dict[str, Any]]:
    windows = list(getattr(plan, "peer_history_windows", []) or [])
    current_period_token = _period_token_for_granularity(
        plan.target_granularity, plan.period_start
    )
    stats: dict[str, Any] = {
        "requested_windows": len(windows),
        "available_windows": 0,
        "missing_windows": 0,
        "requested_window_ids": [window.window_id for window in windows],
        "available_window_ids": [],
        "missing_window_ids": [],
        "current_period_token": current_period_token,
        "truncated": False,
    }
    period_start = _to_utc_datetime(plan.period_start)
    period_end = _to_utc_datetime(plan.period_end)
    summary_lines: list[str] = [
        f"## History pack (granularity={plan.target_granularity})",
        f"- current_period_start={period_start.isoformat()} | current_period_end={period_end.isoformat()}",
        f"- current_period_token={current_period_token}",
        f"- requested_windows={len(windows)}",
        (
            "- requested_window_ids="
            + ", ".join(str(window.window_id).strip() for window in windows)
            if windows
            else "- requested_window_ids=-"
        ),
    ]
    if not windows:
        summary_lines.append("- status=disabled")
        md = "\n".join(summary_lines).strip() + "\n"
        md, truncated = _truncate_chars(md, max_chars=int(history_pack_max_chars))
        stats["truncated"] = bool(truncated)
        stats["max_chars"] = int(history_pack_max_chars)
        return md, stats

    section_lines: list[str] = []
    for window in windows:
        section_lines.append(f"### {plan.target_granularity} {window.window_id}")
        section_lines.append(f"- window_id={window.window_id}")
        section_lines.append(f"- period_token={window.label}")
        docs = repository.list_documents(
            doc_type="trend",
            granularity=plan.target_granularity,
            period_start=window.period_start,
            period_end=window.period_end,
            order_by="event_desc",
            limit=1,
        )
        doc = docs[0] if docs else None
        if doc is None:
            stats["missing_windows"] = int(stats["missing_windows"]) + 1
            stats["missing_window_ids"].append(window.window_id)
            section_lines.append("- status=missing")
            continue
        stats["available_windows"] = int(stats["available_windows"]) + 1
        stats["available_window_ids"].append(window.window_id)
        doc_lines = _trend_payload_summary_lines(
            repository=repository,
            doc=doc,
            token=window.window_id,
            entry_label=plan.target_granularity,
        )
        section_lines.extend(doc_lines[1:] if len(doc_lines) > 1 else doc_lines)

    summary_lines.extend(
        [
            (
                "- available_window_ids="
                + ", ".join(str(window_id) for window_id in stats["available_window_ids"])
                if stats["available_window_ids"]
                else "- available_window_ids=-"
            ),
            (
                "- missing_window_ids="
                + ", ".join(str(window_id) for window_id in stats["missing_window_ids"])
                if stats["missing_window_ids"]
                else "- missing_window_ids=-"
            ),
        ]
    )

    md = "\n".join(summary_lines + section_lines).strip() + "\n"
    md, truncated = _truncate_chars(md, max_chars=int(history_pack_max_chars))
    stats["truncated"] = bool(truncated)
    stats["max_chars"] = int(history_pack_max_chars)
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
        title = "本期暂无可发布研究趋势"
        overview_md = "- 该周期没有可用文档。"
    else:
        title = "No publishable research trend for this period"
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


def is_empty_trend_payload(payload: TrendPayload) -> bool:
    if list(payload.topics or []) or list(payload.clusters or []) or list(payload.highlights or []):
        return False
    title = str(payload.title or "").strip()
    overview = str(payload.overview_md or "").strip()
    return (title, overview) in {
        (
            "本期暂无可发布研究趋势",
            "- 该周期没有可用文档。",
        ),
        (
            "No publishable research trend for this period",
            "- No documents available for this period.",
        ),
        (
            "No research trends available for publication this period",
            "- No documents were available during this period.",
        ),
        (
            "No research trends available for publication this period",
            "- No documents are available for this period.",
        ),
    }


def _chunk_text_segments(
    text_value: str, *, chunk_chars: int, max_segments: int | None = None
) -> list[tuple[int, int, str]]:
    normalized = str(text_value or "")
    size = max(200, int(chunk_chars))
    if not normalized.strip():
        return []
    segment_limit = None if max_segments is None else max(0, int(max_segments))
    if segment_limit == 0:
        return []
    segments: list[tuple[int, int, str]] = []
    start = 0
    end = len(normalized)
    while start < end:
        if segment_limit is not None and len(segments) >= segment_limit:
            break
        seg_end = min(end, start + size)
        seg = normalized[start:seg_end]
        segments.append((start, seg_end, seg))
        start = seg_end
    return segments


def _commit_trend_session(*, repository: TrendRepositoryPort, session: Session) -> None:
    commit_fn = getattr(repository, "_commit", None)
    if callable(commit_fn):
        commit_fn(session)
        return
    session.commit()


def _load_latest_content_texts_for_items(
    *,
    repository: TrendRepositoryPort,
    item_ids: list[int],
    content_types: list[str],
) -> dict[int, dict[str, str | None]]:
    from recoleta.trends_corpus import load_latest_content_texts_for_items_impl

    return load_latest_content_texts_for_items_impl(
        repository=repository,
        item_ids=item_ids,
        content_types=content_types,
    )


def _index_items_as_documents_itemwise(
    *,
    repository: TrendRepositoryPort,
    pairs: list[tuple[Any, Any]],
    content_types: list[str],
    content_chunk_chars: int,
    max_content_chunks_per_item: int,
    log: Any,
) -> dict[str, int]:
    docs_upserted = 0
    chunks_upserted = 0
    content_chunks_upserted = 0
    content_chunks_deleted = 0

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
            for content_type in content_types:
                candidate = texts.get(content_type)
                if isinstance(candidate, str) and candidate.strip():
                    chosen = candidate
                    chosen_type = content_type
                    break
            if not chosen or chosen_type is None:
                content_chunks_deleted += repository.delete_document_chunks(
                    doc_id=doc_id,
                    kind="content",
                    chunk_index_gte=1,
                )
                continue

            segments = _chunk_text_segments(
                chosen,
                chunk_chars=content_chunk_chars,
                max_segments=max_content_chunks_per_item,
            )
            max_written_index: int | None = None
            for seg_idx, (start_char, end_char, seg) in enumerate(segments, start=1):
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

    return {
        "docs_upserted": docs_upserted,
        "chunks_upserted": chunks_upserted,
        "content_chunks_upserted": content_chunks_upserted,
        "content_chunks_deleted": content_chunks_deleted,
    }


def _index_items_as_documents_batched(
    *,
    repository: TrendRepositoryPort,
    pairs: list[tuple[Any, Any]],
    content_types: list[str],
    content_chunk_chars: int,
    max_content_chunks_per_item: int,
) -> dict[str, int]:
    from recoleta.trends_corpus import index_items_as_documents_batched_impl

    return index_items_as_documents_batched_impl(
        repository=repository,
        pairs=pairs,
        content_types=content_types,
        content_chunk_chars=content_chunk_chars,
        max_content_chunks_per_item=max_content_chunks_per_item,
    )


def index_items_as_documents(
    *,
    request: Any | None = None,
    **legacy_kwargs: Any,
) -> dict[str, Any]:
    from recoleta.trends_corpus import (
        coerce_index_items_request,
        index_items_as_documents_impl,
    )

    normalized_request = coerce_index_items_request(
        request=request,
        legacy_kwargs=legacy_kwargs,
    )
    return index_items_as_documents_impl(request=normalized_request)


def generate_trend_via_tools(
    *,
    request: Any | None = None,
    **legacy_kwargs: Any,
) -> tuple[TrendPayload, dict[str, Any] | None]:
    from recoleta.trends_corpus import (
        coerce_generate_trend_request,
        generate_trend_via_tools_impl,
    )

    normalized_request = coerce_generate_trend_request(
        request=request,
        legacy_kwargs=legacy_kwargs,
    )
    return cast(
        tuple[TrendPayload, dict[str, Any] | None],
        generate_trend_via_tools_impl(request=normalized_request),
    )


def persist_trend_payload(
    *,
    repository: TrendRepositoryPort,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
    payload: TrendPayload,
    pass_output_id: int | None = None,
    pass_kind: str | None = None,
) -> int:
    title = sanitize_trend_title(str(payload.title or "").strip(), fallback="Trend")
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
        text_value=clamp_trend_overview_markdown(str(payload.overview_md or "").strip())
        or "(empty)",
        start_char=0,
        end_char=None,
        source_content_type="trend_overview",
    )
    repository.upsert_document_chunk(
        doc_id=doc_id,
        chunk_index=1,
        kind="meta",
        text_value=json.dumps(
            inject_projection_provenance(
                payload=payload.model_dump(mode="json"),
                provenance=(
                    build_projection_provenance(
                        pass_output_id=pass_output_id,
                        pass_kind=str(pass_kind or "").strip() or "trend_synthesis",
                    )
                    if pass_output_id is not None
                    else None
                ),
            ),
            ensure_ascii=False,
            separators=(",", ":"),
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
