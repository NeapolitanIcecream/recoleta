from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime
from threading import Event, Thread
import time
from typing import Any

from loguru import logger
from pydantic_ai import Agent, RunContext

from recoleta.item_summary import extract_item_summary_sections
from recoleta.llm_costs import estimate_cost_usd_from_tokens as estimate_llm_cost_usd_from_tokens
from recoleta.llm_connection import LLMConnectionConfig
from recoleta.ports import TrendRepositoryPort
from recoleta.rag.corpus_tools import (
    CorpusSpec,
    SearchService,
    _reciprocal_rank_fuse_search_hits as _shared_reciprocal_rank_fuse_search_hits,
    resolve_corpus_query_sources,
    serialize_document as _serialize_corpus_document,
)
from recoleta.rag.semantic_search import semantic_search_summaries_in_period
from recoleta.rag.vector_store import LanceVectorStore
from recoleta.trends import (
    TREND_EVOLUTION_CHANGE_TYPE_VALUES,
    TrendCluster,
    TrendPayload,
)


@dataclass(slots=True)
class TrendAgentDeps:
    repository: TrendRepositoryPort
    vector_store: LanceVectorStore
    run_id: str
    period_start: datetime
    period_end: datetime
    rag_sources: list[dict[str, Any]] | None
    embedding_model: str
    embedding_dimensions: int | None
    embedding_batch_max_inputs: int
    embedding_batch_max_chars: int
    metric_namespace: str = "pipeline.trends"
    embedding_failure_mode: str = "continue"
    embedding_max_errors: int = 0
    llm_connection: LLMConnectionConfig | None = None


def _search_service_from_deps(deps: TrendAgentDeps) -> SearchService:
    return SearchService(
        repository=deps.repository,
        vector_store=deps.vector_store,
        run_id=deps.run_id,
        period_start=deps.period_start,
        period_end=deps.period_end,
        corpus_spec=CorpusSpec.from_rag_sources(deps.rag_sources),
        embedding_model=deps.embedding_model,
        embedding_dimensions=deps.embedding_dimensions,
        embedding_batch_max_inputs=deps.embedding_batch_max_inputs,
        embedding_batch_max_chars=deps.embedding_batch_max_chars,
        metric_namespace=deps.metric_namespace,
        embedding_failure_mode=str(deps.embedding_failure_mode or "continue"),
        embedding_max_errors=int(deps.embedding_max_errors or 0),
        llm_connection=deps.llm_connection,
    )


_SEARCH_TEXT_TOKEN_RE = re.compile(r"\w+", flags=re.UNICODE)
_SEARCH_TEXT_BACKOFF_MAX_CANDIDATES = 24
_RAW_TOOL_TRACE_MAX_EVENTS = 64
_RAW_TOOL_TRACE_MAX_ITEMS = 12
_RAW_TOOL_TRACE_MAX_DEPTH = 4
_RAW_TOOL_TRACE_MAX_TEXT_CHARS = 600
_TREND_AGENT_HEARTBEAT_INTERVAL_SECONDS = 15.0
_INLINE_SUMMARY_SECTION_RE = re.compile(
    r"(?is)(summary|problem|approach|results)\s*[:：]\s*(.*?)(?=(summary|problem|approach|results)\s*[:：]|$)"
)


def _build_trend_instructions(*, output_language: str | None) -> str:
    base = (
        "You are a research trend analyst. Use tools to explore the local corpus. "
        "Prefer summary chunks (chunk_index=0) first. "
        "When ready, return a TrendPayload with grounded, readable content."
    )
    base += (
        " Start with search_hybrid when you need to discover themes quickly, "
        "then use get_doc_bundle to inspect promising evidence bundles before falling back to get_doc or read_chunk."
    )
    base += (
        " When available, use trend documents (doc_type=trend) for synthesis and higher-level themes, "
        "and use item documents (doc_type=item) for concrete citations and grounded evidence. "
        "Do not force a Top-N must-read section; that workflow is legacy and should only appear if the prompt explicitly requires it."
    )
    base += (
        " Tools only access the active target period. "
        "If historical same-granularity context is provided, it comes through history_pack_md in the prompt rather than tool calls. "
        "If no usable history is provided, leave evolution as null instead of guessing."
    )
    change_types = ", ".join(TREND_EVOLUTION_CHANGE_TYPE_VALUES)
    base += (
        " If you emit evolution.signals[].change_type, it must use one of these English enum values: "
        f"{change_types}. "
        "If you emit evolution.signals[].history_windows, cite only prev_n window_id values from history_pack_md sections that are not marked missing. "
        "Do not emit raw dates, ISO week/month tokens, or the current period token there."
    )
    base += (
        " Treat evolution as an evidence-first section rather than a generic summary. "
        "Each signal should name at least one concrete paper, benchmark, or system and include a specific factual detail or metric whenever the corpus provides one. "
        "When comparing against history, anchor the contrast to a named historical title, cluster, or representative system from history_pack_md instead of saying only that 'previous windows emphasized X'. "
        "If you mention a history window in prose, refer to it with the exact prev_n token so the renderer can convert it into a link. "
        "Use tools to inspect current-window evidence before writing evolution, and prefer fewer signals over vague ones. "
        "Do not simply restate the overview; focus on what persisted, appeared, faded, or changed across windows."
    )
    base += (
        " In overview_md, write body content only: do not add an extra Overview/总览 heading because the publisher adds it. "
        "The opening overview prose must stay under 200 Chinese characters or 200 words before any later sub-sections. "
        "Keep topics only in the topics field; do not add a Topics/主题 section inside overview_md. "
        "Make the title direct and specific to the content; do not prepend dates or generic labels such as Daily Trend/研究趋势日报/每日趋势. "
        "Inside any optional ranked reading list, do not append 'representative snippet' / '代表片段' text after a title or link."
    )
    base += (
        " Prioritize readability over compression: use short sentences, avoid long multi-clause lines, "
        "and avoid stacking many technical terms in a single sentence. "
        "Introduce acronyms once with a brief explanation in the output language, then reuse them. "
        "Avoid repetitive phrasing across overview, clusters, and highlights; each section should add new value."
    )
    base += (
        " For clusters[].representative_chunks, either omit the entry or provide an object "
        "with required integer fields doc_id and chunk_index, and optional float score. "
        "Never output null for doc_id/chunk_index."
    )
    if not output_language:
        return base
    return (
        f"{base} Use {output_language} for all natural language fields "
        "(title, overview_md, clusters[].name, clusters[].description, highlights). "
        "Keep all JSON keys in English and keep topics as concise English tags."
    )


def resolve_rag_query_sources(
    *,
    doc_type: str,
    granularity: str | None,
    rag_sources: list[dict[str, Any]] | None,
) -> list[tuple[str, str | None]]:
    return resolve_corpus_query_sources(
        doc_type=doc_type,
        granularity=granularity,
        rag_sources=rag_sources,
    )


def _doc_event_sort_key(doc: Any) -> tuple[float, int]:
    raw_event = getattr(doc, "published_at", None)
    if not isinstance(raw_event, datetime):
        raw_event = getattr(doc, "period_start", None)
    event_ts = raw_event.timestamp() if isinstance(raw_event, datetime) else 0.0
    try:
        doc_id = int(getattr(doc, "id") or 0)
    except Exception:
        doc_id = 0
    return event_ts, doc_id


def _decode_item_authors(
    *, repository: TrendRepositoryPort, item_id: int | None
) -> list[str]:
    if item_id is None:
        return []
    try:
        normalized_item_id = int(item_id)
    except Exception:
        return []
    if normalized_item_id <= 0:
        return []
    item = repository.get_item(item_id=normalized_item_id)
    if item is None:
        return []
    raw_authors = getattr(item, "authors", None)
    if isinstance(raw_authors, list):
        return [str(author).strip() for author in raw_authors if str(author).strip()]
    decode_list = getattr(repository, "decode_list", None)
    if callable(decode_list):
        try:
            decoded = decode_list(raw_authors)
            if not isinstance(decoded, list):
                return []
            return [
                str(author).strip()
                for author in decoded
                if str(author).strip()
            ]
        except Exception:
            return []
    if isinstance(raw_authors, str) and raw_authors.strip():
        return [raw_authors.strip()]
    return []


def _serialize_document(
    *,
    repository: TrendRepositoryPort,
    doc: Any,
) -> dict[str, Any]:
    return _serialize_corpus_document(repository=repository, doc=doc)


def _truncate_text(value: str, *, max_chars: int) -> str:
    normalized = str(value or "").strip()
    cap = max(0, int(max_chars))
    if cap <= 0 or len(normalized) <= cap:
        return normalized
    return normalized[:cap].rstrip()


def _clean_summary_section_value(value: str) -> str:
    normalized = str(value or "").strip()
    if normalized.startswith("- "):
        return normalized[2:].strip()
    if normalized.startswith("* "):
        return normalized[2:].strip()
    return normalized


def _normalize_summary_sections(value: str) -> dict[str, str]:
    sections = extract_item_summary_sections(value)
    if (
        str(sections.get("summary") or "").strip()
        and not str(sections.get("problem") or "").strip()
        and not str(sections.get("approach") or "").strip()
        and not str(sections.get("results") or "").strip()
    ):
        inline_sections = {key: "" for key in ("summary", "problem", "approach", "results")}
        matches = list(_INLINE_SUMMARY_SECTION_RE.finditer(str(value or "")))
        if matches:
            for match in matches:
                key = str(match.group(1) or "").strip().lower()
                body = _clean_summary_section_value(str(match.group(2) or "").strip())
                if key in inline_sections and body:
                    inline_sections[key] = body
            if any(
                str(inline_sections.get(key) or "").strip()
                for key in ("problem", "approach", "results")
            ):
                return inline_sections
    return {
        key: _clean_summary_section_value(section_value)
        for key, section_value in sections.items()
    }


def _candidate_text_queries(query: str) -> list[tuple[str, int]]:
    tokens: list[str] = []
    seen_tokens: set[str] = set()
    for token in _SEARCH_TEXT_TOKEN_RE.findall(str(query or "")):
        normalized = str(token or "").strip()
        lowered = normalized.lower()
        if not lowered or lowered in seen_tokens:
            continue
        seen_tokens.add(lowered)
        tokens.append(normalized)
    if not tokens:
        return []

    candidates: list[tuple[str, int]] = []
    seen_queries: set[str] = set()
    total = len(tokens)
    for size in range(total, 0, -1):
        for start in range(0, total - size + 1):
            candidate = " ".join(tokens[start : start + size]).strip()
            if not candidate or candidate in seen_queries:
                continue
            seen_queries.add(candidate)
            candidates.append((candidate, total - size))

    longest_tokens = sorted(tokens, key=lambda token: (-len(token), token.lower()))
    for size in range(min(3, total), 0, -1):
        candidate = " ".join(longest_tokens[:size]).strip()
        if not candidate or candidate in seen_queries:
            continue
        seen_queries.add(candidate)
        candidates.append((candidate, total - size))
    if len(candidates) <= _SEARCH_TEXT_BACKOFF_MAX_CANDIDATES:
        return candidates

    capped_candidates: list[tuple[str, int]] = []
    max_index = len(candidates) - 1
    for ordinal in range(_SEARCH_TEXT_BACKOFF_MAX_CANDIDATES):
        if _SEARCH_TEXT_BACKOFF_MAX_CANDIDATES == 1:
            index = 0
        else:
            index = (ordinal * max_index) // (_SEARCH_TEXT_BACKOFF_MAX_CANDIDATES - 1)
        candidate = candidates[index]
        if candidate in capped_candidates:
            continue
        capped_candidates.append(candidate)
    return capped_candidates

def _read_doc_content_chunks(
    *,
    repository: TrendRepositoryPort,
    doc_id: int,
    limit: int,
    text_max_chars: int,
) -> list[dict[str, Any]]:
    normalized_limit = max(0, int(limit or 0))
    if normalized_limit <= 0:
        return []
    out: list[dict[str, Any]] = []
    consecutive_misses = 0
    chunk_index = 1
    while len(out) < normalized_limit and consecutive_misses < 2 and chunk_index <= 12:
        chunk = repository.read_document_chunk(doc_id=doc_id, chunk_index=chunk_index)
        if chunk is None:
            consecutive_misses += 1
            chunk_index += 1
            continue
        consecutive_misses = 0
        if str(getattr(chunk, "kind", "") or "").strip().lower() != "content":
            chunk_index += 1
            continue
        text_value = _truncate_text(str(getattr(chunk, "text", "") or ""), max_chars=text_max_chars)
        if not text_value:
            chunk_index += 1
            continue
        out.append(
            {
                "chunk_id": int(getattr(chunk, "id")),
                "doc_id": int(getattr(chunk, "doc_id")),
                "chunk_index": int(getattr(chunk, "chunk_index")),
                "kind": str(getattr(chunk, "kind") or ""),
                "start_char": getattr(chunk, "start_char", None),
                "end_char": getattr(chunk, "end_char", None),
                "source_content_type": str(getattr(chunk, "source_content_type") or ""),
                "text": text_value,
            }
        )
        chunk_index += 1
    return out


def _attach_doc_metadata(
    *,
    repository: TrendRepositoryPort,
    rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    if not rows:
        return []
    doc_cache: dict[int, dict[str, Any] | None] = {}
    out: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        try:
            doc_id = int(row.get("doc_id") or 0)
        except Exception:
            doc_id = 0
        metadata: dict[str, Any] | None = None
        if doc_id > 0:
            if doc_id not in doc_cache:
                doc = repository.get_document(doc_id=doc_id)
                doc_cache[doc_id] = (
                    _serialize_document(repository=repository, doc=doc)
                    if doc is not None
                    else None
                )
            metadata = doc_cache.get(doc_id)
        enriched = dict(row)
        if metadata is not None:
            for key, value in metadata.items():
                enriched.setdefault(key, value)
        out.append(enriched)
    return out


def _search_hit_key(row: dict[str, Any]) -> tuple[int, int] | None:
    try:
        raw_doc_id = row.get("doc_id")
        raw_chunk_index = row.get("chunk_index")
        doc_id = int(raw_doc_id) if raw_doc_id is not None else 0
        chunk_index = int(raw_chunk_index) if raw_chunk_index is not None else -1
    except Exception:
        return None
    if doc_id <= 0 or chunk_index < 0:
        return None
    return doc_id, chunk_index


def _reciprocal_rank_fuse_search_hits(
    *,
    text_hits: list[dict[str, Any]],
    semantic_hits: list[dict[str, Any]],
    limit: int,
) -> list[dict[str, Any]]:
    return _shared_reciprocal_rank_fuse_search_hits(
        text_hits=text_hits,
        semantic_hits=semantic_hits,
        limit=limit,
    )


def build_trend_agent(
    *,
    llm_model: str,
    output_language: str | None = None,
    llm_connection: LLMConnectionConfig | None = None,
) -> Agent[TrendAgentDeps, TrendPayload]:
    from recoleta.rag.pydantic_ai_model import build_pydantic_ai_model

    model = build_pydantic_ai_model(llm_model, llm_connection=llm_connection)
    agent: Agent[TrendAgentDeps, TrendPayload] = Agent(
        model,
        deps_type=TrendAgentDeps,
        output_type=TrendPayload,
        instructions=_build_trend_instructions(output_language=output_language),
        defer_model_check=True,
    )

    @agent.tool
    def list_docs(
        ctx: RunContext[TrendAgentDeps],
        doc_type: str,
        granularity: str | None = None,
        order_by: str = "event_desc",
        offset: int = 0,
        limit: int = 50,
    ) -> dict[str, Any]:
        """List documents in the active trend window.

        Args:
            doc_type: Use `item` for paper-level evidence and `trend` for lower-level trend summaries.
            This tool only accesses the active target period and not earlier windows.
            granularity: Optional trend granularity filter such as `day` or `week`.
            order_by: Event-time ordering, typically `event_desc` or `event_asc`.
            offset: Pagination offset for broad corpus scans.
            limit: Maximum number of documents to return.
        """
        return _search_service_from_deps(ctx.deps).list_docs(
            doc_type=doc_type,
            granularity=granularity,
            order_by=order_by,
            offset=offset,
            limit=limit,
        )

    @agent.tool
    def get_doc(ctx: RunContext[TrendAgentDeps], doc_id: int) -> dict[str, Any]:
        """Fetch one document with metadata.

        Args:
            doc_id: Document identifier returned by list/search tools.
        """
        return _search_service_from_deps(ctx.deps).get_doc(doc_id=doc_id)

    @agent.tool
    def get_doc_bundle(
        ctx: RunContext[TrendAgentDeps],
        doc_id: int,
        content_limit: int = 2,
        content_chars: int = 600,
    ) -> dict[str, Any]:
        """Fetch a compact evidence bundle for one document.

        Args:
            doc_id: Document identifier returned by list/search tools.
            content_limit: Maximum number of content chunks to include after the summary.
            content_chars: Maximum characters to keep per content chunk preview.
        """
        return _search_service_from_deps(ctx.deps).get_doc_bundle(
            doc_id=doc_id,
            content_limit=content_limit,
            content_chars=content_chars,
        )

    @agent.tool
    def read_chunk(
        ctx: RunContext[TrendAgentDeps], doc_id: int, chunk_index: int
    ) -> dict[str, Any]:
        """Read one indexed chunk from a document.

        Args:
            doc_id: Document identifier returned by list/search tools.
            chunk_index: Chunk number to inspect; `0` is usually the summary chunk.
        """
        return _search_service_from_deps(ctx.deps).read_chunk(
            doc_id=doc_id,
            chunk_index=chunk_index,
        )

    @agent.tool
    def search_text(
        ctx: RunContext[TrendAgentDeps],
        query: str,
        doc_type: str,
        granularity: str | None = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        """Search the corpus lexically via FTS.

        Args:
            query: Exact keywords, phrases, or jargon you expect to appear in the corpus.
            doc_type: Use `item` for papers and `trend` for lower-level trend notes.
            This tool only searches the active target period and not prior windows.
            granularity: Optional trend granularity filter such as `day` or `week`.
            limit: Maximum number of hits to return.
        """
        return _search_service_from_deps(ctx.deps).search_text(
            query=query,
            doc_type=doc_type,
            granularity=granularity,
            limit=limit,
        )

    @agent.tool
    def search_semantic(
        ctx: RunContext[TrendAgentDeps],
        query: str,
        doc_type: str,
        granularity: str | None = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        """Search the corpus semantically over summary chunks.

        Args:
            query: Conceptual query phrased in natural language.
            doc_type: Use `item` for papers and `trend` for lower-level trend notes.
            This tool only searches the active target period and not prior windows.
            granularity: Optional trend granularity filter such as `day` or `week`.
            limit: Maximum number of hits to return.
        """
        return _search_service_from_deps(ctx.deps).search_semantic(
            query=query,
            doc_type=doc_type,
            granularity=granularity,
            limit=limit,
        )

    @agent.tool
    def search_hybrid(
        ctx: RunContext[TrendAgentDeps],
        query: str,
        doc_type: str,
        granularity: str | None = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        """Blend lexical and semantic retrieval for theme discovery.

        Args:
            query: The concept, theme, or concrete phrase you want to investigate.
            doc_type: Use `item` for paper-level evidence and `trend` for synthesized lower-level trend docs.
            This tool only searches the active target period and not prior windows.
            granularity: Optional trend granularity filter such as `day` or `week`.
            limit: Maximum number of fused hits to return.
        """
        return _search_service_from_deps(ctx.deps).search_hybrid(
            query=query,
            doc_type=doc_type,
            granularity=granularity,
            limit=limit,
        )

    return agent


def ensure_trend_cluster_representatives(
    *,
    payload: TrendPayload,
    search,
    max_reps: int = 6,
) -> dict[str, int]:
    clusters_total = len(payload.clusters or [])
    clusters_backfilled_total = 0
    invalid_reps_dropped_total = 0
    reps_backfilled_total = 0

    normalized_max_reps = max(0, int(max_reps or 0))
    if normalized_max_reps <= 0 or not payload.clusters:
        return {
            "clusters_total": clusters_total,
            "clusters_backfilled_total": 0,
            "invalid_reps_dropped_total": 0,
            "reps_backfilled_total": 0,
        }

    for cluster in payload.clusters:
        raw_reps = cluster.representative_chunks or []
        cleaned: list[TrendCluster.RepresentativeChunk] = []
        for rep in raw_reps:
            try:
                doc_id = int(getattr(rep, "doc_id"))
                chunk_index = int(getattr(rep, "chunk_index"))
            except Exception:
                invalid_reps_dropped_total += 1
                continue
            if doc_id <= 0 or chunk_index < 0:
                invalid_reps_dropped_total += 1
                continue
            score_raw = getattr(rep, "score", None)
            rep_score: float | None = None
            if score_raw is not None:
                try:
                    rep_score = float(score_raw)  # type: ignore[arg-type]
                except Exception:
                    rep_score = None
            cleaned.append(
                TrendCluster.RepresentativeChunk(
                    doc_id=doc_id,
                    chunk_index=chunk_index,
                    score=round(rep_score, 6) if rep_score is not None else None,
                )
            )

        if cleaned:
            cluster.representative_chunks = cleaned[:normalized_max_reps]
            continue

        query = " ".join(
            [
                str(getattr(cluster, "name", "") or "").strip(),
                str(getattr(cluster, "description", "") or "").strip(),
            ]
        ).strip()
        backfilled: list[TrendCluster.RepresentativeChunk] = []
        if query:
            try:
                rows = search(query, normalized_max_reps) or []
            except Exception:
                rows = []
            for r in rows:
                if not isinstance(r, dict):
                    continue
                doc_id_raw = r.get("doc_id")
                chunk_index_raw = r.get("chunk_index")
                if doc_id_raw is None or chunk_index_raw is None:
                    continue
                try:
                    doc_id = int(doc_id_raw)
                    chunk_index = int(chunk_index_raw)
                except Exception:
                    continue
                if doc_id <= 0 or chunk_index < 0:
                    continue
                score_raw = r.get("score")
                hit_score: float | None
                if score_raw is None:
                    hit_score = None
                else:
                    try:
                        hit_score = float(score_raw)  # type: ignore[arg-type]
                    except Exception:
                        hit_score = None
                backfilled.append(
                    TrendCluster.RepresentativeChunk(
                        doc_id=doc_id,
                        chunk_index=chunk_index,
                        score=round(hit_score, 6) if hit_score is not None else None,
                    )
                )
                if len(backfilled) >= normalized_max_reps:
                    break

        if not backfilled:
            doc_ids = list(getattr(cluster, "representative_doc_ids", []) or [])
            for raw_doc_id in doc_ids:
                try:
                    doc_id = int(raw_doc_id)
                except Exception:
                    continue
                if doc_id <= 0:
                    continue
                backfilled.append(
                    TrendCluster.RepresentativeChunk(
                        doc_id=doc_id, chunk_index=0, score=None
                    )
                )
                if len(backfilled) >= normalized_max_reps:
                    break

        if backfilled:
            cluster.representative_chunks = backfilled
            clusters_backfilled_total += 1
            reps_backfilled_total += len(backfilled)
        else:
            cluster.representative_chunks = []

    return {
        "clusters_total": clusters_total,
        "clusters_backfilled_total": clusters_backfilled_total,
        "invalid_reps_dropped_total": invalid_reps_dropped_total,
        "reps_backfilled_total": reps_backfilled_total,
    }


def _summarize_tool_calls(messages: list[Any]) -> tuple[int, dict[str, int]]:
    total = 0
    breakdown: dict[str, int] = {}
    for msg in messages:
        parts = getattr(msg, "parts", None)
        if not isinstance(parts, list):
            continue
        for part in parts:
            if getattr(part, "part_kind", None) == "tool-call":
                total += 1
                tool_name = str(getattr(part, "tool_name", "") or "").strip()
                if tool_name:
                    breakdown[tool_name] = int(breakdown.get(tool_name, 0)) + 1
    return total, {name: breakdown[name] for name in sorted(breakdown)}


def _compact_tool_trace_value(value: Any, *, depth: int = 0) -> Any:
    if value is None or isinstance(value, (bool, int, float)):
        return value
    if isinstance(value, str):
        if len(value) <= _RAW_TOOL_TRACE_MAX_TEXT_CHARS:
            return value
        return value[:_RAW_TOOL_TRACE_MAX_TEXT_CHARS].rstrip()
    if depth >= _RAW_TOOL_TRACE_MAX_DEPTH:
        return _truncate_text(str(value), max_chars=_RAW_TOOL_TRACE_MAX_TEXT_CHARS)
    if isinstance(value, dict):
        compacted_dict: dict[str, Any] = {}
        items = list(value.items())
        for key, item_value in items[:_RAW_TOOL_TRACE_MAX_ITEMS]:
            compacted_dict[str(key)] = _compact_tool_trace_value(
                item_value, depth=depth + 1
            )
        if len(items) > _RAW_TOOL_TRACE_MAX_ITEMS:
            compacted_dict["__truncated_items__"] = (
                len(items) - _RAW_TOOL_TRACE_MAX_ITEMS
            )
        return compacted_dict
    if isinstance(value, (list, tuple)):
        compacted_list: list[Any] = [
            _compact_tool_trace_value(item, depth=depth + 1)
            for item in list(value)[:_RAW_TOOL_TRACE_MAX_ITEMS]
        ]
        if len(value) > _RAW_TOOL_TRACE_MAX_ITEMS:
            compacted_list.append(
                {"__truncated_items__": len(value) - _RAW_TOOL_TRACE_MAX_ITEMS}
            )
        return compacted_list
    model_dump = getattr(value, "model_dump", None)
    if callable(model_dump):
        try:
            return _compact_tool_trace_value(model_dump(mode="json"), depth=depth + 1)
        except Exception:
            pass
    return _truncate_text(str(value), max_chars=_RAW_TOOL_TRACE_MAX_TEXT_CHARS)


def _extract_raw_tool_trace(messages: list[Any]) -> dict[str, Any]:
    if not messages:
        return {
            "status": "unavailable",
            "events": [],
            "events_total": 0,
            "tool_calls_total": 0,
            "events_truncated": False,
        }

    events: list[dict[str, Any]] = []
    tool_calls_total = 0
    for message_index, msg in enumerate(messages):
        parts = getattr(msg, "parts", None)
        if not isinstance(parts, (list, tuple)):
            continue
        message_kind = str(getattr(msg, "kind", "") or "")
        for part_index, part in enumerate(parts):
            part_kind = str(getattr(part, "part_kind", "") or "").strip()
            if part_kind == "tool-call":
                tool_calls_total += 1
                events.append(
                    {
                        "event_index": len(events),
                        "message_index": message_index,
                        "message_kind": message_kind,
                        "part_index": part_index,
                        "kind": "tool-call",
                        "tool_name": str(getattr(part, "tool_name", "") or ""),
                        "tool_call_id": str(getattr(part, "tool_call_id", "") or ""),
                        "args": _compact_tool_trace_value(getattr(part, "args", None)),
                    }
                )
            elif part_kind == "tool-return":
                raw_content = getattr(part, "content", None)
                model_response_object = getattr(part, "model_response_object", None)
                if callable(model_response_object) and not isinstance(raw_content, str):
                    try:
                        raw_content = model_response_object()
                    except Exception:
                        raw_content = getattr(part, "content", None)
                events.append(
                    {
                        "event_index": len(events),
                        "message_index": message_index,
                        "message_kind": message_kind,
                        "part_index": part_index,
                        "kind": "tool-return",
                        "tool_name": str(getattr(part, "tool_name", "") or ""),
                        "tool_call_id": str(getattr(part, "tool_call_id", "") or ""),
                        "content": _compact_tool_trace_value(raw_content),
                    }
                )

    events_total = len(events)
    return {
        "status": "captured",
        "events": events[:_RAW_TOOL_TRACE_MAX_EVENTS],
        "events_total": events_total,
        "tool_calls_total": tool_calls_total,
        "events_truncated": events_total > _RAW_TOOL_TRACE_MAX_EVENTS,
    }


def _count_tool_calls(messages: list[Any]) -> int:
    total, _ = _summarize_tool_calls(messages)
    return total


def _estimate_cost_usd_from_tokens(
    *, model: str, input_tokens: int | None, output_tokens: int | None
) -> float | None:
    return estimate_llm_cost_usd_from_tokens(
        model=model,
        prompt_tokens=input_tokens,
        completion_tokens=output_tokens,
    )


def _record_metric(
    *,
    repository: TrendRepositoryPort,
    run_id: str,
    metric_namespace: str,
    name: str,
    value: float,
    unit: str | None = None,
) -> None:
    repository.record_metric(
        run_id=run_id,
        name=f"{metric_namespace}.{name}",
        value=value,
        unit=unit,
    )


def _start_trend_generation_heartbeat(
    *,
    log: Any,
    granularity: str,
    prompt_chars: int,
) -> tuple[Event, Thread]:
    stop_event = Event()
    started = time.perf_counter()
    interval_seconds = max(0.01, float(_TREND_AGENT_HEARTBEAT_INTERVAL_SECONDS))

    def _heartbeat() -> None:
        while not stop_event.wait(timeout=interval_seconds):
            elapsed_ms = int((time.perf_counter() - started) * 1000)
            log.info(
                "Trend generation heartbeat granularity={} elapsed_ms={} prompt_chars={} tool_calls_observed_total={}",
                granularity,
                elapsed_ms,
                prompt_chars,
                0,
            )

    thread = Thread(
        target=_heartbeat,
        name=f"recoleta-trend-heartbeat-{granularity}",
        daemon=True,
    )
    thread.start()
    return stop_event, thread


def build_trend_prompt_payload(
    *,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
    corpus_doc_type: str,
    corpus_granularity: str | None = None,
    overview_pack_md: str | None = None,
    history_pack_md: str | None = None,
    rag_sources: list[dict[str, Any]] | None = None,
    ranking_n: int | None = None,
    rep_source_doc_type: str | None = None,
    evolution_max_signals: int | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "task": "Generate research trends for the period.",
        "granularity": granularity,
        "period_start": period_start.isoformat(),
        "period_end": period_end.isoformat(),
        "corpus": {"doc_type": corpus_doc_type, "granularity": corpus_granularity},
        "notes": [
            "Use tools to cite representative doc_id/chunk_index in clusters.",
            "Optimize for readability: short sentences, minimal jargon pile-ups, no repetitive filler.",
            "Keep claims grounded in the local corpus.",
            "Keep the title specific and remove date/generic prefixes.",
            "Keep topics only in metadata, not in overview_md body sections.",
            "Tools only access the active target period; use history_pack_md for same-granularity historical context when present.",
            "Leave evolution null unless history_pack_md provides usable prior-window evidence.",
            (
                "If evolution is present, evolution.signals[].change_type must be one of "
                + ", ".join(TREND_EVOLUTION_CHANGE_TYPE_VALUES)
                + "."
            ),
            "If evolution is present, evolution.signals[].history_windows must use only prev_n window_id values from history_pack_md and must not repeat the current period token.",
            "Evolution must be evidence-dense: name concrete papers, benchmarks, or systems and include specific factual details or metrics whenever available.",
            "When comparing against history, ground the delta in concrete historical titles, clusters, or representative systems from history_pack_md rather than generic phrases.",
            "If you mention a historical window in prose, use the exact prev_n token so publishing can render it as a link, and do not manually repeat the linked historical title immediately next to that token.",
            "If you cannot ground an evolution signal concretely, emit fewer signals instead of generic prose.",
            "Do not repeat the overview inside evolution; explain the delta across windows.",
        ],
    }
    payload["evolution_change_types"] = list(TREND_EVOLUTION_CHANGE_TYPE_VALUES)
    payload["evolution_requirements"] = {
        "avoid_generic_summary": True,
        "prefer_concrete_titles": True,
        "prefer_named_history_anchors": True,
        "prefer_quantitative_details": True,
        "render_history_window_mentions": True,
        "use_fewer_signals_if_evidence_is_thin": True,
    }
    if overview_pack_md is not None:
        payload["overview_pack_md"] = str(overview_pack_md)
    if history_pack_md is not None:
        payload["history_pack_md"] = str(history_pack_md)
    if rag_sources is not None:
        payload["rag_sources"] = rag_sources
    if ranking_n is not None:
        payload["ranking_n"] = int(ranking_n)
        notes = payload.get("notes")
        if isinstance(notes, list):
            notes.append(
                "ranking_n is legacy compatibility metadata; do not force a Top-N section unless explicitly requested."
            )
    if rep_source_doc_type is not None:
        normalized = str(rep_source_doc_type).strip().lower()
        if normalized:
            payload["rep_source_doc_type"] = normalized
    if evolution_max_signals is not None:
        payload["evolution_max_signals"] = int(evolution_max_signals)
    return payload


def generate_trend_payload(
    *,
    repository: TrendRepositoryPort,
    vector_store: LanceVectorStore,
    run_id: str,
    llm_model: str,
    output_language: str | None = None,
    embedding_model: str,
    embedding_dimensions: int | None,
    embedding_batch_max_inputs: int,
    embedding_batch_max_chars: int,
    embedding_failure_mode: str = "continue",
    embedding_max_errors: int = 0,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
    corpus_doc_type: str,
    corpus_granularity: str | None = None,
    overview_pack_md: str | None = None,
    history_pack_md: str | None = None,
    rag_sources: list[dict[str, Any]] | None = None,
    ranking_n: int | None = None,
    rep_source_doc_type: str | None = None,
    evolution_max_signals: int | None = None,
    include_debug: bool = False,
    metric_namespace: str = "pipeline.trends",
    llm_connection: LLMConnectionConfig | None = None,
) -> tuple[TrendPayload, dict[str, Any] | None]:
    log = logger.bind(module="rag.trend_agent", run_id=run_id)
    agent_kwargs: dict[str, Any] = {
        "llm_model": llm_model,
        "output_language": output_language,
    }
    if llm_connection is not None:
        agent_kwargs["llm_connection"] = llm_connection
    agent = build_trend_agent(**agent_kwargs)
    deps = TrendAgentDeps(
        repository=repository,
        vector_store=vector_store,
        run_id=run_id,
        metric_namespace=metric_namespace,
        period_start=period_start,
        period_end=period_end,
        rag_sources=rag_sources,
        embedding_model=embedding_model,
        embedding_dimensions=embedding_dimensions,
        embedding_batch_max_inputs=embedding_batch_max_inputs,
        embedding_batch_max_chars=embedding_batch_max_chars,
        embedding_failure_mode=str(embedding_failure_mode or "continue"),
        embedding_max_errors=int(embedding_max_errors or 0),
        llm_connection=llm_connection,
    )

    prompt = json.dumps(
        build_trend_prompt_payload(
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
        ),
        ensure_ascii=False,
        separators=(",", ":"),
    )
    prompt_chars = len(prompt)
    log.info(
        "Trend generation started granularity={} prompt_chars={} corpus_doc_type={} corpus_granularity={}",
        granularity,
        prompt_chars,
        corpus_doc_type,
        corpus_granularity or "-",
    )
    agent_started = time.perf_counter()
    stop_event, heartbeat_thread = _start_trend_generation_heartbeat(
        log=log,
        granularity=granularity,
        prompt_chars=prompt_chars,
    )
    try:
        result = agent.run_sync(prompt, deps=deps)
    except Exception as exc:  # noqa: BLE001
        agent_duration_ms = int((time.perf_counter() - agent_started) * 1000)
        _record_metric(
            repository=repository,
            run_id=run_id,
            metric_namespace=metric_namespace,
            name="agent_run_sync.duration_ms",
            value=agent_duration_ms,
            unit="ms",
        )
        _record_metric(
            repository=repository,
            run_id=run_id,
            metric_namespace=metric_namespace,
            name="agent_run_sync.failed_total",
            value=1,
            unit="count",
        )
        log.warning(
            "Trend generation failed granularity={} elapsed_ms={} prompt_chars={} error_type={} error={}",
            granularity,
            agent_duration_ms,
            prompt_chars,
            type(exc).__name__,
            str(exc),
        )
        raise
    finally:
        stop_event.set()
        heartbeat_thread.join(timeout=1.0)
    agent_duration_ms = int((time.perf_counter() - agent_started) * 1000)
    _record_metric(
        repository=repository,
        run_id=run_id,
        metric_namespace=metric_namespace,
        name="agent_run_sync.duration_ms",
        value=agent_duration_ms,
        unit="ms",
    )
    _record_metric(
        repository=repository,
        run_id=run_id,
        metric_namespace=metric_namespace,
        name="agent_run_sync.failed_total",
        value=0,
        unit="count",
    )
    payload = result.output
    rep_doc_type_candidate = str(rep_source_doc_type or "").strip().lower()
    rep_doc_type = (
        rep_doc_type_candidate
        if rep_doc_type_candidate in {"item", "trend"}
        else "item"
    )
    rep_backfill_started = time.perf_counter()
    rep_stats = ensure_trend_cluster_representatives(
        payload=payload,
        search=lambda q, n: [
            {
                "doc_id": h.doc_id,
                "chunk_index": h.chunk_index,
                "score": round(float(h.score), 6),
            }
            for h in semantic_search_summaries_in_period(
                repository=repository,
                vector_store=vector_store,
                run_id=run_id,
                doc_type=rep_doc_type,
                period_start=period_start,
                period_end=period_end,
                query=q,
                embedding_model=embedding_model,
                embedding_dimensions=embedding_dimensions,
                max_batch_inputs=embedding_batch_max_inputs,
                max_batch_chars=embedding_batch_max_chars,
                embedding_failure_mode=str(embedding_failure_mode or "continue"),
                embedding_max_errors=int(embedding_max_errors or 0),
                limit=int(n),
                metric_namespace=metric_namespace,
                llm_connection=llm_connection,
            )
        ],
        max_reps=6,
    )
    rep_backfill_duration_ms = int((time.perf_counter() - rep_backfill_started) * 1000)
    _record_metric(
        repository=repository,
        run_id=run_id,
        metric_namespace=metric_namespace,
        name="rep_backfill.duration_ms",
        value=rep_backfill_duration_ms,
        unit="ms",
    )
    log.info(
        "Trend representative backfill done granularity={} duration_ms={} clusters_backfilled_total={} invalid_reps_dropped_total={} reps_backfilled_total={}",
        granularity,
        rep_backfill_duration_ms,
        int(rep_stats.get("clusters_backfilled_total") or 0),
        int(rep_stats.get("invalid_reps_dropped_total") or 0),
        int(rep_stats.get("reps_backfilled_total") or 0),
    )
    if rep_stats.get("invalid_reps_dropped_total", 0) or rep_stats.get(
        "clusters_backfilled_total", 0
    ):
        log.warning("Trend cluster representatives normalized stats={}", rep_stats)
        try:
            repository.record_metric(
                run_id=run_id,
                name=f"{metric_namespace}.cluster_representatives_backfilled_total",
                value=int(rep_stats.get("clusters_backfilled_total") or 0),
                unit="count",
            )
            repository.record_metric(
                run_id=run_id,
                name=f"{metric_namespace}.cluster_representatives_invalid_dropped_total",
                value=int(rep_stats.get("invalid_reps_dropped_total") or 0),
                unit="count",
            )
        except Exception as metric_exc:  # noqa: BLE001
            log.warning(
                "Trend representative metrics failed error_type={} error={}",
                type(metric_exc).__name__,
                str(metric_exc),
            )
    usage = result.usage()
    messages_getter = getattr(result, "all_messages", None)
    raw_messages = messages_getter() if callable(messages_getter) else None
    messages: list[Any] = raw_messages if isinstance(raw_messages, list) else []
    tool_calls_total, tool_call_breakdown = _summarize_tool_calls(messages)
    usage_dict = {
        "input_tokens": getattr(usage, "input_tokens", None),
        "output_tokens": getattr(usage, "output_tokens", None),
        "requests": getattr(usage, "requests", None),
    }
    estimated_cost_usd = _estimate_cost_usd_from_tokens(
        model=llm_model,
        input_tokens=getattr(usage, "input_tokens", None),
        output_tokens=getattr(usage, "output_tokens", None),
    )
    debug: dict[str, Any] = {
        "usage": usage_dict,
        "estimated_cost_usd": estimated_cost_usd,
        "tool_calls_total": tool_calls_total,
        "tool_call_breakdown": tool_call_breakdown,
        "raw_tool_trace": _extract_raw_tool_trace(messages),
        "prompt_chars": prompt_chars,
        "overview_pack_chars": len(str(overview_pack_md or "")),
        "history_pack_chars": len(str(history_pack_md or "")),
    }
    log.info(
        "Trend generation done granularity={} elapsed_ms={} include_debug={} cost_present={} tool_calls_total={}",
        granularity,
        agent_duration_ms,
        bool(include_debug),
        estimated_cost_usd is not None,
        tool_calls_total,
    )
    return payload, debug
