from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, cast

from loguru import logger

from recoleta.item_summary import extract_item_summary_sections
from recoleta.llm_connection import LLMConnectionConfig
from recoleta.ports import TrendRepositoryPort
from recoleta.rag.semantic_search import semantic_search_summaries_in_period
from recoleta.rag.vector_store import LanceVectorStore
from recoleta.types import DEFAULT_TOPIC_STREAM

_SEARCH_TEXT_TOKEN_RE = re.compile(r"\w+", flags=re.UNICODE)
_SEARCH_TEXT_BACKOFF_MAX_CANDIDATES = 24
_INLINE_SUMMARY_SECTION_RE = re.compile(
    r"(?is)(summary|problem|approach|results)\s*[:：]\s*(.*?)(?=(summary|problem|approach|results)\s*[:：]|$)"
)


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
        inline_sections = {
            key: "" for key in ("summary", "problem", "approach", "results")
        }
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


@dataclass(slots=True)
class CorpusSource:
    doc_type: str
    granularity: str | None = None

    def normalized_key(self) -> tuple[str, str | None]:
        normalized_doc_type = str(self.doc_type or "").strip().lower()
        normalized_granularity = (
            str(self.granularity or "").strip().lower() or None
            if self.granularity is not None
            else None
        )
        if normalized_doc_type == "item":
            normalized_granularity = None
        return normalized_doc_type, normalized_granularity


@dataclass(slots=True)
class CorpusSpec:
    sources: list[CorpusSource] = field(default_factory=list)

    @classmethod
    def from_rag_sources(
        cls, rag_sources: list[dict[str, Any]] | None
    ) -> "CorpusSpec":
        normalized: list[CorpusSource] = []
        seen: set[tuple[str, str | None]] = set()
        for source in rag_sources or []:
            if not isinstance(source, dict):
                continue
            candidate = CorpusSource(
                doc_type=str(source.get("doc_type") or ""),
                granularity=(
                    str(source.get("granularity") or "")
                    if source.get("granularity") is not None
                    else None
                ),
            )
            key = candidate.normalized_key()
            if key[0] not in {"item", "trend", "idea"} or key in seen:
                continue
            seen.add(key)
            normalized.append(candidate)
        return cls(sources=normalized)

    def resolve_sources(
        self,
        *,
        doc_type: str,
        granularity: str | None = None,
    ) -> list[tuple[str, str | None]]:
        normalized_type = str(doc_type or "").strip().lower()
        if normalized_type not in {"item", "trend", "idea"}:
            return []
        normalized_granularity = (
            str(granularity or "").strip().lower() if granularity is not None else ""
        )
        normalized_sources = [source.normalized_key() for source in self.sources]
        if not normalized_sources:
            if normalized_type == "item":
                return [("item", None)]
            return [(normalized_type, normalized_granularity or None)]
        allowed_sources = [
            source for source in normalized_sources if source[0] == normalized_type
        ]
        if not allowed_sources:
            return []
        if normalized_type == "item":
            return [("item", None)]
        if normalized_granularity:
            requested = (normalized_type, normalized_granularity)
            return [requested] if requested in allowed_sources else []
        return allowed_sources


def resolve_corpus_query_sources(
    *,
    doc_type: str,
    granularity: str | None,
    rag_sources: list[dict[str, Any]] | None,
) -> list[tuple[str, str | None]]:
    spec = CorpusSpec.from_rag_sources(rag_sources)
    return spec.resolve_sources(doc_type=doc_type, granularity=granularity)


def _coerce_utc_datetime(value: Any) -> datetime | None:
    if not isinstance(value, datetime):
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value


def _document_source_key(doc: Any) -> tuple[str, str | None] | None:
    normalized_doc_type = str(getattr(doc, "doc_type", "") or "").strip().lower()
    if normalized_doc_type not in {"item", "trend", "idea"}:
        return None
    if normalized_doc_type == "item":
        return normalized_doc_type, None
    normalized_granularity = (
        str(getattr(doc, "granularity", "") or "").strip().lower() or None
    )
    return normalized_doc_type, normalized_granularity


def _document_visible_in_corpus(
    *,
    doc: Any,
    scope: str,
    period_start: datetime,
    period_end: datetime,
    corpus_spec: CorpusSpec,
) -> bool:
    source_key = _document_source_key(doc)
    if source_key is None:
        return False

    normalized_scope = str(getattr(doc, "scope", "") or "").strip() or DEFAULT_TOPIC_STREAM
    if normalized_scope != (str(scope or "").strip() or DEFAULT_TOPIC_STREAM):
        return False

    active_period_start = _coerce_utc_datetime(period_start)
    active_period_end = _coerce_utc_datetime(period_end)
    if active_period_start is None or active_period_end is None:
        return False

    allowed_sources = set(
        corpus_spec.resolve_sources(
            doc_type=source_key[0],
            granularity=source_key[1],
        )
    )
    if source_key not in allowed_sources:
        return False

    if source_key[0] == "item":
        published_at = _coerce_utc_datetime(getattr(doc, "published_at", None))
        return (
            published_at is not None
            and active_period_start <= published_at < active_period_end
        )

    doc_period_start = _coerce_utc_datetime(getattr(doc, "period_start", None))
    doc_period_end = _coerce_utc_datetime(getattr(doc, "period_end", None))
    return (
        doc_period_start is not None
        and doc_period_end is not None
        and doc_period_start < active_period_end
        and doc_period_end > active_period_start
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
                str(author).strip() for author in decoded if str(author).strip()
            ]
        except Exception:
            return []
    if isinstance(raw_authors, str) and raw_authors.strip():
        return [raw_authors.strip()]
    return []


def serialize_document(
    *,
    repository: TrendRepositoryPort,
    doc: Any,
) -> dict[str, Any]:
    published_at = getattr(doc, "published_at", None)
    period_start_value = getattr(doc, "period_start", None)
    period_end_value = getattr(doc, "period_end", None)
    raw_item_id = getattr(doc, "item_id", None)
    try:
        item_id = int(raw_item_id) if raw_item_id is not None else None
    except Exception:
        item_id = None
    return {
        "doc_id": int(getattr(doc, "id")),
        "doc_type": str(getattr(doc, "doc_type") or ""),
        "title": str(getattr(doc, "title") or ""),
        "item_id": item_id,
        "source": str(getattr(doc, "source") or ""),
        "canonical_url": str(getattr(doc, "canonical_url") or ""),
        "published_at": published_at.isoformat()
        if isinstance(published_at, datetime)
        else None,
        "granularity": str(getattr(doc, "granularity") or ""),
        "period_start": period_start_value.isoformat()
        if isinstance(period_start_value, datetime)
        else None,
        "period_end": period_end_value.isoformat()
        if isinstance(period_end_value, datetime)
        else None,
        "authors": _decode_item_authors(repository=repository, item_id=item_id),
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


def _collect_text_hits_with_backoff(
    *,
    repository: TrendRepositoryPort,
    query: str,
    doc_type: str,
    granularity: str | None,
    period_start: datetime,
    period_end: datetime,
    scope: str,
    limit: int,
) -> tuple[list[dict[str, Any]], list[str]]:
    normalized_limit = max(1, int(limit or 1))
    hits: list[dict[str, Any]] = []
    seen_hits: set[tuple[int, int]] = set()
    matched_queries: list[str] = []

    for candidate_query, backoff_depth in _candidate_text_queries(query):
        rows = repository.search_chunks_text(
            query=candidate_query,
            doc_type=doc_type,
            granularity=granularity,
            period_start=period_start,
            period_end=period_end,
            scope=scope,
            limit=normalized_limit,
        )
        matched_in_candidate = False
        for row in rows:
            if not isinstance(row, dict):
                continue
            key = _search_hit_key(row)
            if key is None or key in seen_hits:
                continue
            seen_hits.add(key)
            enriched = dict(row)
            enriched["matched_query"] = candidate_query
            enriched["backoff_depth"] = int(backoff_depth)
            hits.append(enriched)
            matched_in_candidate = True
            if len(hits) >= normalized_limit:
                break
        if matched_in_candidate:
            matched_queries.append(candidate_query)
        if len(hits) >= normalized_limit:
            break
    return hits, matched_queries


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
        text_value = _truncate_text(
            str(getattr(chunk, "text", "") or ""),
            max_chars=text_max_chars,
        )
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
                    serialize_document(repository=repository, doc=doc)
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


def _reciprocal_rank_fuse_search_hits(
    *,
    text_hits: list[dict[str, Any]],
    semantic_hits: list[dict[str, Any]],
    limit: int,
) -> list[dict[str, Any]]:
    normalized_limit = max(1, int(limit or 1))
    rrf_k = 60
    fused: dict[tuple[int, int], dict[str, Any]] = {}

    def _merge_source(source_name: str, hits: list[dict[str, Any]]) -> None:
        for rank, row in enumerate(hits, start=1):
            if not isinstance(row, dict):
                continue
            key = _search_hit_key(row)
            if key is None:
                continue
            entry = fused.setdefault(
                key,
                {
                    "doc_id": key[0],
                    "chunk_index": key[1],
                    "match_sources": [],
                    "rrf_score": 0.0,
                },
            )
            for field_name, field_value in row.items():
                if field_name in {"match_sources", "rrf_score"}:
                    continue
                existing = entry.get(field_name)
                if existing in (None, "", [], {}):
                    entry[field_name] = field_value
            entry["rrf_score"] = float(entry.get("rrf_score") or 0.0) + (
                1.0 / float(rrf_k + rank)
            )
            sources = cast(list[str], entry.setdefault("match_sources", []))
            if source_name not in sources:
                sources.append(source_name)
            entry[f"{source_name}_rank"] = rank

    _merge_source("text", text_hits)
    _merge_source("semantic", semantic_hits)

    rows = list(fused.values())
    rows.sort(
        key=lambda row: (
            -float(row.get("rrf_score") or 0.0),
            -len(cast(list[str], row.get("match_sources") or [])),
            int(row.get("doc_id") or 0),
            int(row.get("chunk_index") or 0),
        )
    )
    out: list[dict[str, Any]] = []
    for row in rows[:normalized_limit]:
        normalized = dict(row)
        normalized["rrf_score"] = round(float(row.get("rrf_score") or 0.0), 6)
        normalized["match_sources"] = list(row.get("match_sources") or [])
        out.append(normalized)
    return out


@dataclass(slots=True)
class SearchService:
    repository: TrendRepositoryPort
    vector_store: LanceVectorStore
    run_id: str
    period_start: datetime
    period_end: datetime
    corpus_spec: CorpusSpec
    embedding_model: str
    embedding_dimensions: int | None
    embedding_batch_max_inputs: int
    embedding_batch_max_chars: int
    scope: str = DEFAULT_TOPIC_STREAM
    metric_namespace: str | None = "pipeline.trends"
    embedding_failure_mode: str = "continue"
    embedding_max_errors: int = 0
    llm_connection: LLMConnectionConfig | None = None
    auto_sync_vectors: bool = True

    def _visible_document(self, *, doc_id: int) -> Any | None:
        normalized_doc_id = int(doc_id or 0)
        if normalized_doc_id <= 0:
            return None
        doc = self.repository.get_document(doc_id=normalized_doc_id)
        if doc is None:
            return None
        if not _document_visible_in_corpus(
            doc=doc,
            scope=self.scope,
            period_start=self.period_start,
            period_end=self.period_end,
            corpus_spec=self.corpus_spec,
        ):
            return None
        return doc

    def _visible_chunk(self, *, doc_id: int, chunk_index: int) -> Any | None:
        doc = self._visible_document(doc_id=doc_id)
        if doc is None:
            return None
        chunk = self.repository.read_document_chunk(
            doc_id=int(getattr(doc, "id") or 0),
            chunk_index=int(chunk_index or 0),
        )
        if chunk is None:
            return None
        normalized_kind = str(getattr(chunk, "kind", "") or "").strip().lower()
        if normalized_kind not in {"summary", "content"}:
            return None
        return chunk

    def list_docs(
        self,
        *,
        doc_type: str,
        granularity: str | None = None,
        order_by: str = "event_desc",
        offset: int = 0,
        limit: int = 50,
    ) -> dict[str, Any]:
        requested_sources = self.corpus_spec.resolve_sources(
            doc_type=doc_type,
            granularity=granularity,
        )
        normalized_order = str(order_by or "event_desc").strip()
        normalized_offset = max(0, int(offset or 0))
        normalized_limit = max(0, int(limit or 50))
        if not requested_sources or normalized_limit <= 0:
            return {"docs": [], "returned": 0}

        docs: list[Any] = []
        seen_doc_ids: set[int] = set()
        for source_doc_type, source_granularity in requested_sources:
            rows = self.repository.list_documents(
                doc_type=source_doc_type,
                period_start=self.period_start,
                period_end=self.period_end,
                granularity=source_granularity,
                scope=self.scope,
                order_by=normalized_order,
                offset=0,
                limit=normalized_limit,
            )
            for doc in rows:
                try:
                    doc_id = int(getattr(doc, "id") or 0)
                except Exception:
                    continue
                if doc_id <= 0 or doc_id in seen_doc_ids:
                    continue
                seen_doc_ids.add(doc_id)
                docs.append(doc)

        docs.sort(key=_doc_event_sort_key, reverse=normalized_order != "event_asc")
        docs = docs[normalized_offset : normalized_offset + normalized_limit]
        out = [serialize_document(repository=self.repository, doc=doc) for doc in docs]
        return {"docs": out, "returned": len(out)}

    def get_doc(self, *, doc_id: int) -> dict[str, Any]:
        doc = self._visible_document(doc_id=doc_id)
        if doc is None:
            return {"doc": None}
        return {"doc": serialize_document(repository=self.repository, doc=doc)}

    def get_doc_bundle(
        self,
        *,
        doc_id: int,
        content_limit: int = 2,
        content_chars: int = 600,
    ) -> dict[str, Any]:
        doc = self._visible_document(doc_id=doc_id)
        if doc is None:
            return {"bundle": None}

        normalized_doc_id = int(getattr(doc, "id"))
        summary_chunk = self.repository.read_document_chunk(
            doc_id=normalized_doc_id,
            chunk_index=0,
        )
        summary_text = str(getattr(summary_chunk, "text", "") or "").strip()
        content_chunks = _read_doc_content_chunks(
            repository=self.repository,
            doc_id=normalized_doc_id,
            limit=content_limit,
            text_max_chars=content_chars,
        )
        return {
            "bundle": {
                "doc": serialize_document(repository=self.repository, doc=doc),
                "summary": {
                    "chunk_id": int(getattr(summary_chunk, "id"))
                    if summary_chunk is not None
                    and getattr(summary_chunk, "id", None) is not None
                    else None,
                    "doc_id": normalized_doc_id,
                    "chunk_index": 0,
                    "kind": str(getattr(summary_chunk, "kind", "") or ""),
                    "source_content_type": str(
                        getattr(summary_chunk, "source_content_type", "") or ""
                    ),
                    "text": summary_text,
                },
                "summary_sections": _normalize_summary_sections(summary_text),
                "content_chunks": content_chunks,
            }
        }

    def read_chunk(self, *, doc_id: int, chunk_index: int) -> dict[str, Any]:
        chunk = self._visible_chunk(doc_id=doc_id, chunk_index=chunk_index)
        if chunk is None:
            return {"chunk": None}
        return {
            "chunk": {
                "chunk_id": int(getattr(chunk, "id")),
                "doc_id": int(getattr(chunk, "doc_id")),
                "chunk_index": int(getattr(chunk, "chunk_index")),
                "kind": str(getattr(chunk, "kind") or ""),
                "start_char": getattr(chunk, "start_char", None),
                "end_char": getattr(chunk, "end_char", None),
                "source_content_type": str(getattr(chunk, "source_content_type") or ""),
                "text": str(getattr(chunk, "text") or ""),
            }
        }

    def search_text(
        self,
        *,
        query: str,
        doc_type: str,
        granularity: str | None = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        requested_sources = self.corpus_spec.resolve_sources(
            doc_type=doc_type,
            granularity=granularity,
        )
        normalized_limit = max(1, int(limit or 10))
        if not requested_sources:
            return {"hits": [], "returned": 0, "matched_queries": []}

        hits: list[dict[str, Any]] = []
        seen_hits: set[tuple[int, int]] = set()
        matched_queries: list[str] = []
        for source_doc_type, source_granularity in requested_sources:
            rows, matched_for_source = _collect_text_hits_with_backoff(
                repository=self.repository,
                query=str(query or ""),
                doc_type=source_doc_type,
                granularity=source_granularity,
                period_start=self.period_start,
                period_end=self.period_end,
                scope=self.scope,
                limit=normalized_limit,
            )
            for matched_query in matched_for_source:
                if matched_query not in matched_queries:
                    matched_queries.append(matched_query)
            for row in rows:
                if not isinstance(row, dict):
                    continue
                key = _search_hit_key(row)
                if key is None or key in seen_hits:
                    continue
                seen_hits.add(key)
                hits.append(row)
        hits.sort(
            key=lambda row: (
                int(row.get("backoff_depth") or 0),
                float(row.get("rank") or 0.0),
                int(row.get("doc_id") or 0),
                int(row.get("chunk_index") or 0),
            )
        )
        hits = _attach_doc_metadata(
            repository=self.repository,
            rows=hits[:normalized_limit],
        )
        return {
            "hits": hits,
            "returned": len(hits),
            "matched_queries": matched_queries,
        }

    def search_semantic(
        self,
        *,
        query: str,
        doc_type: str,
        granularity: str | None = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        requested_sources = self.corpus_spec.resolve_sources(
            doc_type=doc_type,
            granularity=granularity,
        )
        normalized_limit = max(1, int(limit or 10))
        if not requested_sources:
            return {"hits": [], "returned": 0}

        hits: list[Any] = []
        seen_hits: set[tuple[int, int]] = set()
        for source_doc_type, source_granularity in requested_sources:
            rows = semantic_search_summaries_in_period(
                repository=self.repository,
                vector_store=self.vector_store,
                run_id=self.run_id,
                doc_type=source_doc_type,
                granularity=source_granularity,
                period_start=self.period_start,
                period_end=self.period_end,
                query=str(query or ""),
                embedding_model=self.embedding_model,
                embedding_dimensions=self.embedding_dimensions,
                max_batch_inputs=self.embedding_batch_max_inputs,
                max_batch_chars=self.embedding_batch_max_chars,
                embedding_failure_mode=str(self.embedding_failure_mode or "continue"),
                embedding_max_errors=int(self.embedding_max_errors or 0),
                limit=normalized_limit,
                scope=self.scope,
                metric_namespace=self.metric_namespace,
                llm_connection=self.llm_connection,
                auto_sync_vectors=bool(self.auto_sync_vectors),
            )
            for hit in rows:
                try:
                    key = (int(getattr(hit, "doc_id")), int(getattr(hit, "chunk_index")))
                except Exception:
                    continue
                if key[0] <= 0 or key[1] < 0 or key in seen_hits:
                    continue
                seen_hits.add(key)
                hits.append(hit)
        hits.sort(
            key=lambda hit: (
                -float(getattr(hit, "score", 0.0) or 0.0),
                int(getattr(hit, "doc_id") or 0),
                int(getattr(hit, "chunk_index") or 0),
            )
        )
        hits = hits[:normalized_limit]
        rows = [
            {
                "chunk_id": h.chunk_id,
                "doc_id": h.doc_id,
                "chunk_index": h.chunk_index,
                "score": round(float(h.score), 6),
                "text_preview": h.text_preview,
            }
            for h in hits
        ]
        rows = _attach_doc_metadata(repository=self.repository, rows=rows)
        return {"hits": rows, "returned": len(rows)}

    def search_hybrid(
        self,
        *,
        query: str,
        doc_type: str,
        granularity: str | None = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        normalized_limit = max(1, int(limit or 10))
        per_source_limit = min(50, max(10, normalized_limit * 3))
        log = logger.bind(module="rag.corpus_tools", run_id=self.run_id)

        text_hits: list[dict[str, Any]] = []
        semantic_hits: list[dict[str, Any]] = []

        try:
            text_result = self.search_text(
                query=query,
                doc_type=doc_type,
                granularity=granularity,
                limit=per_source_limit,
            )
            text_hits = list(text_result.get("hits") or [])
        except Exception as exc:  # noqa: BLE001
            log.warning(
                "Hybrid search text branch failed doc_type={} granularity={} error_type={} error={}",
                str(doc_type or "").strip(),
                str(granularity or "").strip(),
                type(exc).__name__,
                str(exc),
            )

        try:
            semantic_result = self.search_semantic(
                query=query,
                doc_type=doc_type,
                granularity=granularity,
                limit=per_source_limit,
            )
            semantic_hits = list(semantic_result.get("hits") or [])
        except Exception as exc:  # noqa: BLE001
            log.warning(
                "Hybrid search semantic branch failed doc_type={} granularity={} error_type={} error={}",
                str(doc_type or "").strip(),
                str(granularity or "").strip(),
                type(exc).__name__,
                str(exc),
            )

        hits = _reciprocal_rank_fuse_search_hits(
            text_hits=text_hits,
            semantic_hits=semantic_hits,
            limit=normalized_limit,
        )
        return {
            "hits": hits,
            "returned": len(hits),
            "source_returned": {
                "text": len(text_hits),
                "semantic": len(semantic_hits),
            },
        }


__all__ = [
    "CorpusSource",
    "CorpusSpec",
    "SearchService",
    "resolve_corpus_query_sources",
    "serialize_document",
    "_collect_text_hits_with_backoff",
    "_reciprocal_rank_fuse_search_hits",
]
