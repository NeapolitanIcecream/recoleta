from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta
from enum import StrEnum
from pathlib import Path
from typing import Any, cast

from loguru import logger
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import text
from sqlmodel import Session, select

from recoleta.llm_connection import LLMConnectionConfig
from recoleta.item_summary import extract_item_summary_sections
from recoleta.models import Document, DocumentChunk
from recoleta.ports import TrendRepositoryPort
from recoleta.provenance import (
    build_projection_provenance,
    inject_projection_provenance,
)
from recoleta.publish.trend_render_shared import (
    clamp_trend_overview_markdown,
    sanitize_trend_title,
)
from recoleta.types import sha256_hex, utc_now


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
    repository: TrendRepositoryPort,
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
    metric_namespace: str | None = None,
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
        metric_namespace=metric_namespace,
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
    stats = {
        "history_windows_normalized_total": 0,
        "history_windows_dropped_total": 0,
        "signals_dropped_total": 0,
    }
    if evolution is None:
        return None, stats

    all_windows = list(history_windows or [])
    alias_to_window_id: dict[str, str] = {}
    allowed_window_ids = {
        str(window.window_id).strip()
        for window in all_windows
        if str(window.window_id).strip()
    }
    if available_window_ids is not None:
        allowed_window_ids &= {
            str(window_id).strip()
            for window_id in available_window_ids
            if str(window_id).strip()
        }

    for window in all_windows:
        window_id = str(window.window_id).strip()
        if not window_id:
            continue
        for alias in {window_id, window.label}:
            normalized_alias = _normalize_history_window_alias(alias)
            if normalized_alias:
                alias_to_window_id.setdefault(normalized_alias, window_id)

    current_period_token = _normalize_history_window_alias(
        _period_token_for_granularity(granularity, period_start)
    )

    normalized_signals: list[TrendEvolutionSignal] = []
    for signal in evolution.signals or []:
        normalized_history_windows: list[str] = []
        seen_history_windows: set[str] = set()
        for candidate in _split_history_window_candidates(
            list(signal.history_windows or [])
        ):
            normalized_candidate = _normalize_history_window_alias(
                _trim_history_window_candidate(candidate)
            )
            if not normalized_candidate:
                continue
            if normalized_candidate == current_period_token:
                stats["history_windows_dropped_total"] += 1
                continue

            mapped_window_id: str | None = None
            direct_match = _HISTORY_WINDOW_ID_RE.search(normalized_candidate)
            if direct_match is not None:
                candidate_window_id = direct_match.group(0).lower()
                if candidate_window_id in allowed_window_ids:
                    mapped_window_id = candidate_window_id
            else:
                candidate_window_id = alias_to_window_id.get(normalized_candidate)
                if (
                    candidate_window_id is not None
                    and candidate_window_id in allowed_window_ids
                ):
                    mapped_window_id = candidate_window_id
                    if candidate_window_id != normalized_candidate:
                        stats["history_windows_normalized_total"] += 1

            if mapped_window_id is None:
                stats["history_windows_dropped_total"] += 1
                continue
            if mapped_window_id in seen_history_windows:
                continue
            seen_history_windows.add(mapped_window_id)
            normalized_history_windows.append(mapped_window_id)

        if allowed_window_ids and not normalized_history_windows:
            stats["signals_dropped_total"] += 1
            continue

        normalized_signals.append(
            TrendEvolutionSignal(
                theme=str(signal.theme or "").strip(),
                change_type=signal.change_type,
                summary=str(signal.summary or "").strip(),
                history_windows=normalized_history_windows,
            )
        )

    summary_md = str(evolution.summary_md or "").strip()
    if not summary_md and not normalized_signals:
        return None, stats
    return (
        TrendEvolutionSection(summary_md=summary_md, signals=normalized_signals),
        stats,
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
    doc_id = int(getattr(doc, "id", 0) or 0)
    heading = f"### {entry_label} {token}"
    if doc_id <= 0:
        return [heading, "- status=missing"]

    meta_chunk = repository.read_document_chunk(doc_id=doc_id, chunk_index=1)
    if meta_chunk is not None:
        try:
            payload = json.loads(str(getattr(meta_chunk, "text", "") or ""))
        except Exception:
            payload = None
        if isinstance(payload, dict):
            title = sanitize_trend_title(
                str(payload.get("title") or getattr(doc, "title", "") or "").strip(),
                fallback="Trend",
            )
            overview_md = clamp_trend_overview_markdown(
                str(payload.get("overview_md") or "").strip()
            )
            clusters = payload.get("clusters") or []
            representative_links: list[str] = []
            cluster_names: list[str] = []
            if isinstance(clusters, list):
                for cluster in clusters:
                    if not isinstance(cluster, dict):
                        continue
                    cluster_name = _sanitize_inline_text(
                        str(cluster.get("name") or "").strip()
                    )
                    if cluster_name and cluster_name not in cluster_names:
                        cluster_names.append(cluster_name)
                    reps = cluster.get("representative_chunks") or []
                    if not isinstance(reps, list):
                        continue
                    for rep in reps:
                        if not isinstance(rep, dict):
                            continue
                        try:
                            rep_doc_id = int(rep.get("doc_id") or 0)
                        except Exception:
                            continue
                        if rep_doc_id <= 0:
                            continue
                        rep_doc = repository.get_document(doc_id=rep_doc_id)
                        if rep_doc is None:
                            continue
                        rep_title = str(getattr(rep_doc, "title", "") or "").strip()
                        rep_url = str(getattr(rep_doc, "canonical_url", "") or "").strip()
                        if not rep_title or not rep_url:
                            continue
                        representative_links.append(f"[{rep_title}]({rep_url})")
            lines = [heading, "- status=ok", f"- title={_sanitize_inline_text(title)}"]
            if overview_md:
                overview_text, _ = _truncate_chars(
                    _sanitize_inline_text(overview_md),
                    max_chars=280,
                )
                lines.append(
                    f"- overview={overview_text}"
                )
            for link in _extract_markdown_links(overview_md, limit=3):
                lines.append(f"- must_read={link}")
            for cluster_name in cluster_names[:3]:
                lines.append(f"- cluster={cluster_name}")
            seen_representatives: set[str] = set()
            for representative_link in representative_links:
                if representative_link in seen_representatives:
                    continue
                seen_representatives.add(representative_link)
                lines.append(f"- representative={representative_link}")
                if len(seen_representatives) >= 3:
                    break
            return lines

    chunk = repository.read_document_chunk(doc_id=doc_id, chunk_index=0)
    if chunk is None:
        return [heading, "- status=missing_chunk"]
    overview = _sanitize_inline_text(str(getattr(chunk, "text", "") or ""))
    if not overview:
        return [heading, "- status=empty"]
    return [
        heading,
        "- status=summary_fallback",
        f"- title={_sanitize_inline_text(sanitize_trend_title(str(getattr(doc, 'title', '') or '').strip(), fallback='Trend'))}",
        f"- overview={overview}",
    ]


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
    repository: TrendRepositoryPort,
    plan: TrendGenerationPlan,
    *,
    overview_pack_max_chars: int,
    item_overview_top_k: int,
    item_overview_item_max_chars: int,
    min_relevance_score: float = 0.0,
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
                    lines.extend([f"### day {token}", "- status=missing"])
                    continue
                lines.extend(
                    _trend_payload_summary_lines(
                        repository=repository,
                        doc=doc,
                        token=token,
                        entry_label="day",
                    )
                )
        else:
            for doc in docs:
                raw_start = getattr(doc, "period_start", None)
                start = (
                    _to_utc_datetime(raw_start)
                    if isinstance(raw_start, datetime)
                    else None
                )
                token = start.date().isoformat() if isinstance(start, datetime) else "-"
                lines.extend(
                    _trend_payload_summary_lines(
                        repository=repository,
                        doc=doc,
                        token=token,
                        entry_label=prev_level or "trend",
                    )
                )
            if not docs:
                lines.extend([f"### {prev_level or 'trend'} -", "- status=missing"])

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
            pairs, filtered_out_total = _filter_pairs_by_min_relevance(
                pairs,
                min_relevance_score=min_relevance_score,
            )
            stats["filtered_out_total"] = filtered_out_total

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
                    -_analysis_relevance_score(pair[1]),
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
                sections = extract_item_summary_sections(
                    str(getattr(analysis, "summary", "") or "")
                )
                lines.extend(
                    [
                        f"### item rank={rank}",
                        f"- title={title}",
                        f"- url={url}",
                        f"- summary={_summary_field_line(sections, field_name='summary', max_chars=item_max_chars)}",
                        f"- problem={_summary_field_line(sections, field_name='problem', max_chars=item_max_chars)}",
                        f"- approach={_summary_field_line(sections, field_name='approach', max_chars=item_max_chars)}",
                        f"- results={_summary_field_line(sections, field_name='results', max_chars=item_max_chars)}",
                    ]
                )

    else:
        lines.append(f"- unsupported_strategy={strategy or '(empty)'}")

    md = "\n".join(lines).rstrip() + "\n"
    md, truncated = _truncate_chars(md, max_chars=int(overview_pack_max_chars))
    stats["truncated"] = bool(truncated)
    stats["chars"] = len(md)
    stats["max_chars"] = int(overview_pack_max_chars)
    return md, stats


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
    normalized_ids: list[int] = []
    seen_ids: set[int] = set()
    for raw_item_id in item_ids:
        try:
            item_id = int(raw_item_id)
        except Exception:
            continue
        if item_id <= 0 or item_id in seen_ids:
            continue
        seen_ids.add(item_id)
        normalized_ids.append(item_id)

    normalized_types = [str(content_type or "").strip() for content_type in content_types]
    normalized_types = [content_type for content_type in normalized_types if content_type]
    if not normalized_ids or not normalized_types:
        return {}

    out: dict[int, dict[str, str | None]] = {
        item_id: {content_type: None for content_type in normalized_types}
        for item_id in normalized_ids
    }
    batch_text_getter = getattr(repository, "get_latest_content_texts_for_items", None)
    if callable(batch_text_getter):
        return cast(
            dict[int, dict[str, str | None]],
            batch_text_getter(item_ids=normalized_ids, content_types=normalized_types),
        )

    batch_getter = getattr(repository, "get_latest_contents", None)
    if callable(batch_getter):
        for content_type in normalized_types:
            contents = cast(
                dict[int, Any],
                batch_getter(item_ids=normalized_ids, content_type=content_type),
            )
            for item_id, content in contents.items():
                text_value = getattr(content, "text", None)
                bucket = out.setdefault(
                    item_id,
                    {ctype: None for ctype in normalized_types},
                )
                bucket[content_type] = (
                    text_value
                    if isinstance(text_value, str) and text_value.strip()
                    else None
                )
        return out

    for item_id in normalized_ids:
        out[item_id] = repository.get_latest_content_texts(
            item_id=item_id,
            content_types=normalized_types,
        )
    return out


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
    item_ids = [
        int(raw_id)
        for item, _analysis in pairs
        if (raw_id := getattr(item, "id", None)) is not None and int(raw_id) > 0
    ]
    if not item_ids:
        return {
            "docs_upserted": 0,
            "chunks_upserted": 0,
            "content_chunks_upserted": 0,
            "content_chunks_deleted": 0,
        }

    texts_by_item_id = _load_latest_content_texts_for_items(
        repository=repository,
        item_ids=item_ids,
        content_types=content_types,
    )

    with Session(repository.engine) as session:
        existing_docs = list(
            session.exec(
                select(Document).where(
                    Document.doc_type == "item",
                    cast(Any, Document.item_id).in_(item_ids),
                )
            )
        )
        docs_by_item_id: dict[int, Document] = {}
        for doc in existing_docs:
            raw_item_id = getattr(doc, "item_id", None)
            if raw_item_id is None:
                continue
            item_id = int(raw_item_id)
            if item_id > 0:
                docs_by_item_id[item_id] = doc

        docs_upserted = 0
        for item, _analysis in pairs:
            raw_item_id = getattr(item, "id", None)
            if raw_item_id is None:
                continue
            item_id = int(raw_item_id)
            if item_id <= 0:
                continue
            event_at = getattr(item, "published_at", None) or getattr(
                item, "created_at", None
            )
            existing = docs_by_item_id.get(item_id)
            if existing is None:
                existing = Document(
                    doc_type="item",
                    item_id=item_id,
                    source=str(getattr(item, "source", "") or "").strip() or None,
                    canonical_url=(
                        str(getattr(item, "canonical_url", "") or "").strip() or None
                    ),
                    title=str(getattr(item, "title", "") or "").strip() or None,
                    published_at=event_at,
                )
                session.add(existing)
                docs_by_item_id[item_id] = existing
            else:
                existing.source = (
                    str(getattr(item, "source", "") or "").strip() or None
                )
                existing.canonical_url = (
                    str(getattr(item, "canonical_url", "") or "").strip() or None
                )
                existing.title = str(getattr(item, "title", "") or "").strip() or None
                existing.published_at = event_at
                existing.updated_at = utc_now()
                session.add(existing)
            docs_upserted += 1

        session.flush()

        doc_ids = [
            int(raw_doc_id)
            for raw_doc_id in (getattr(doc, "id", None) for doc in docs_by_item_id.values())
            if raw_doc_id is not None and int(raw_doc_id) > 0
        ]
        existing_chunks = (
            list(
                session.exec(
                    select(DocumentChunk).where(
                        cast(Any, DocumentChunk.doc_id).in_(doc_ids),
                        cast(Any, DocumentChunk.kind).in_(["summary", "content"]),
                    )
                )
            )
            if doc_ids
            else []
        )
        existing_chunks_by_key: dict[tuple[int, int], DocumentChunk] = {}
        for chunk in existing_chunks:
            existing_chunks_by_key[
                (int(getattr(chunk, "doc_id")), int(getattr(chunk, "chunk_index")))
            ] = chunk

        target_rows: dict[tuple[int, int], dict[str, Any]] = {}
        content_cutoffs: dict[int, int | None] = {}
        content_chunks_upserted = 0
        for item, analysis in pairs:
            raw_item_id = getattr(item, "id", None)
            if raw_item_id is None:
                continue
            item_id = int(raw_item_id)
            doc = docs_by_item_id.get(item_id)
            if doc is None or getattr(doc, "id", None) is None:
                continue
            doc_id = int(getattr(doc, "id"))
            summary_text = str(getattr(analysis, "summary", "") or "").strip()
            if not summary_text:
                raise ValueError("chunk text must not be empty")
            target_rows[(doc_id, 0)] = {
                "doc_id": doc_id,
                "chunk_index": 0,
                "kind": "summary",
                "text": summary_text,
                "start_char": 0,
                "end_char": None,
                "text_hash": sha256_hex(summary_text),
                "source_content_type": "analysis_summary",
            }

            chosen: str | None = None
            chosen_type: str | None = None
            texts = texts_by_item_id.get(item_id, {})
            for content_type in content_types:
                candidate = texts.get(content_type)
                if isinstance(candidate, str) and candidate.strip():
                    chosen = candidate
                    chosen_type = content_type
                    break
            if not chosen or chosen_type is None:
                content_cutoffs[doc_id] = None
                continue

            max_written_index: int | None = None
            for seg_idx, (start_char, end_char, seg) in enumerate(
                _chunk_text_segments(
                    chosen,
                    chunk_chars=content_chunk_chars,
                    max_segments=max_content_chunks_per_item,
                ),
                start=1,
            ):
                target_rows[(doc_id, seg_idx)] = {
                    "doc_id": doc_id,
                    "chunk_index": seg_idx,
                    "kind": "content",
                    "text": seg,
                    "start_char": start_char,
                    "end_char": end_char,
                    "text_hash": sha256_hex(seg),
                    "source_content_type": chosen_type,
                }
                content_chunks_upserted += 1
                max_written_index = seg_idx
            content_cutoffs[doc_id] = max_written_index

        changed_chunks: list[DocumentChunk] = []
        for (doc_id, chunk_index), payload in target_rows.items():
            existing = existing_chunks_by_key.get((doc_id, chunk_index))
            if existing is None:
                chunk = DocumentChunk(
                    doc_id=doc_id,
                    chunk_index=chunk_index,
                    kind=str(payload["kind"]),
                    text=str(payload["text"]),
                    start_char=payload["start_char"],
                    end_char=payload["end_char"],
                    text_hash=str(payload["text_hash"]),
                    source_content_type=(
                        str(payload["source_content_type"]).strip()
                        if payload.get("source_content_type")
                        else None
                    ),
                )
                session.add(chunk)
                changed_chunks.append(chunk)
                continue

            if str(getattr(existing, "text_hash", "") or "") == str(
                payload["text_hash"]
            ):
                continue
            existing.kind = str(payload["kind"])
            existing.text = str(payload["text"])
            existing.start_char = payload["start_char"]
            existing.end_char = payload["end_char"]
            existing.text_hash = str(payload["text_hash"])
            existing.source_content_type = (
                str(payload["source_content_type"]).strip()
                if payload.get("source_content_type")
                else None
            )
            session.add(existing)
            changed_chunks.append(existing)

        stale_chunks: list[DocumentChunk] = []
        for chunk in existing_chunks:
            if str(getattr(chunk, "kind", "") or "").strip().lower() != "content":
                continue
            doc_id = int(getattr(chunk, "doc_id"))
            max_written_index = content_cutoffs.get(doc_id)
            threshold = 1 if max_written_index is None else max_written_index + 1
            if int(getattr(chunk, "chunk_index")) >= threshold:
                stale_chunks.append(chunk)

        session.flush()
        conn = session.connection()

        changed_fts_rows = [
            {
                "rowid": int(raw_chunk_id),
                "text": str(getattr(chunk, "text")),
                "doc_id": int(getattr(chunk, "doc_id")),
                "chunk_index": int(getattr(chunk, "chunk_index")),
                "kind": str(getattr(chunk, "kind")),
            }
            for chunk in changed_chunks
            if (raw_chunk_id := getattr(chunk, "id", None)) is not None
            and int(raw_chunk_id) > 0
        ]
        if changed_fts_rows:
            conn.execute(
                text("DELETE FROM chunk_fts WHERE rowid = :rowid"),
                [{"rowid": row["rowid"]} for row in changed_fts_rows],
            )
            conn.execute(
                text(
                    "INSERT INTO chunk_fts(rowid, text, doc_id, chunk_index, kind) "
                    "VALUES(:rowid, :text, :doc_id, :chunk_index, :kind)"
                ),
                changed_fts_rows,
            )

        stale_ids = [
            int(raw_chunk_id)
            for raw_chunk_id in (getattr(chunk, "id", None) for chunk in stale_chunks)
            if raw_chunk_id is not None and int(raw_chunk_id) > 0
        ]
        if stale_ids:
            conn.execute(
                text("DELETE FROM chunk_embeddings WHERE chunk_id = :chunk_id"),
                [{"chunk_id": chunk_id} for chunk_id in stale_ids],
            )
            conn.execute(
                text("DELETE FROM chunk_fts WHERE rowid = :rowid"),
                [{"rowid": chunk_id} for chunk_id in stale_ids],
            )
        for chunk in stale_chunks:
            session.delete(chunk)

        _commit_trend_session(repository=repository, session=session)
        return {
            "docs_upserted": docs_upserted,
            "chunks_upserted": len(target_rows),
            "content_chunks_upserted": content_chunks_upserted,
            "content_chunks_deleted": len(stale_chunks),
        }


def index_items_as_documents(
    *,
    repository: TrendRepositoryPort,
    run_id: str,
    period_start: datetime,
    period_end: datetime,
    limit: int = 2000,
    content_chunk_chars: int = 1200,
    max_content_chunks_per_item: int = 8,
    min_relevance_score: float = 0.0,
) -> dict[str, Any]:
    """Index analyzed items into documents + chunks (summary first, content optional)."""
    log = logger.bind(module="trends.index_items", run_id=run_id)
    started = time.perf_counter()
    pairs = repository.list_analyzed_items_in_period(
        period_start=period_start,
        period_end=period_end,
        limit=limit,
    )
    pairs, filtered_out_total = _filter_pairs_by_min_relevance(
        pairs,
        min_relevance_score=min_relevance_score,
    )
    keep_item_ids = {
        int(getattr(item, "id") or 0)
        for item, _analysis in pairs
        if getattr(item, "id", None) is not None
    }
    docs_deleted = _prune_item_documents_for_period(
        repository=repository,
        period_start=period_start,
        period_end=period_end,
        keep_item_ids=keep_item_ids,
    )

    content_types = [
        "pdf_text",
        "html_maintext",
        "html_document_md",
        "html_document",
        "latex_source",
    ]
    write_mode = "batched"
    try:
        write_stats = _index_items_as_documents_batched(
            repository=repository,
            pairs=pairs,
            content_types=content_types,
            content_chunk_chars=content_chunk_chars,
            max_content_chunks_per_item=max_content_chunks_per_item,
        )
    except Exception as exc:  # noqa: BLE001
        write_mode = "itemwise_fallback"
        log.warning(
            "Batch document indexing failed; falling back to itemwise writes "
            "error_type={} error={}",
            type(exc).__name__,
            str(exc),
        )
        write_stats = _index_items_as_documents_itemwise(
            repository=repository,
            pairs=pairs,
            content_types=content_types,
            content_chunk_chars=content_chunk_chars,
            max_content_chunks_per_item=max_content_chunks_per_item,
            log=log,
        )

    elapsed_ms = int((time.perf_counter() - started) * 1000)
    stats = {
        "items_total": len(pairs),
        "items_filtered_out": filtered_out_total,
        "docs_upserted": write_stats["docs_upserted"],
        "docs_deleted": docs_deleted,
        "chunks_upserted": write_stats["chunks_upserted"],
        "content_chunks_upserted": write_stats["content_chunks_upserted"],
        "content_chunks_deleted": write_stats["content_chunks_deleted"],
        "write_mode": write_mode,
        "duration_ms": elapsed_ms,
    }
    log.info("Index items done stats={}", stats)
    return stats


def generate_trend_via_tools(
    *,
    repository: TrendRepositoryPort,
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
    history_pack_md: str | None = None,
    rag_sources: list[dict[str, str | None]] | None = None,
    ranking_n: int | None = None,
    rep_source_doc_type: str | None = None,
    evolution_max_signals: int | None = None,
    include_debug: bool = False,
    metric_namespace: str = "pipeline.trends",
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
        history_pack_md=history_pack_md,
        rag_sources=rag_sources,
        ranking_n=ranking_n,
        rep_source_doc_type=rep_source_doc_type,
        evolution_max_signals=evolution_max_signals,
        include_debug=include_debug,
        metric_namespace=metric_namespace,
        llm_connection=llm_connection,
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
