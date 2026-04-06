from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, cast

from loguru import logger

from recoleta.llm_connection import LLMConnectionConfig
from recoleta.ports import TrendRepositoryPort
from recoleta.rag.semantic_search import semantic_search_summaries_in_period
from recoleta.rag.search_helpers import (
    attach_doc_metadata,
    collect_text_hits_with_backoff as _collect_text_hits_with_backoff_impl,
    document_event_sort_key,
    normalize_summary_sections,
    read_doc_content_chunks,
    search_hit_key,
    serialize_document,
)
from recoleta.rag.search_models import SummaryCorpusWindow, SummarySearchRequest
from recoleta.rag.vector_store import LanceVectorStore


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
    def from_rag_sources(cls, rag_sources: list[dict[str, Any]] | None) -> "CorpusSpec":
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
    period_start: datetime,
    period_end: datetime,
    corpus_spec: CorpusSpec,
) -> bool:
    source_key = _document_source_key(doc)
    if source_key is None:
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
            key = search_hit_key(row)
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


def _semantic_hit_key(hit: Any) -> tuple[int, int] | None:
    try:
        doc_id = int(getattr(hit, "doc_id"))
        chunk_index = int(getattr(hit, "chunk_index"))
    except Exception:
        return None
    if doc_id <= 0 or chunk_index < 0:
        return None
    return doc_id, chunk_index


def _dedupe_matched_queries(
    current: list[str],
    new_values: list[str],
) -> list[str]:
    out = list(current)
    for matched_query in new_values:
        if matched_query not in out:
            out.append(matched_query)
    return out


def _collect_text_hits_with_backoff(
    *,
    window: SummaryCorpusWindow | None = None,
    **legacy_kwargs: Any,
) -> tuple[list[dict[str, Any]], list[str]]:
    active_window = window
    if active_window is None:
        active_window = SummaryCorpusWindow(
            repository=legacy_kwargs["repository"],
            vector_store=cast(Any, legacy_kwargs.get("vector_store")),
            run_id=str(legacy_kwargs.get("run_id") or ""),
            doc_type=str(legacy_kwargs["doc_type"]),
            granularity=legacy_kwargs.get("granularity"),
            period_start=legacy_kwargs["period_start"],
            period_end=legacy_kwargs["period_end"],
        )
    return _collect_text_hits_with_backoff_impl(
        window=active_window,
        query=str(legacy_kwargs["query"]),
        limit=int(legacy_kwargs.get("limit") or 10),
    )


def _text_search_window(
    service: SearchService,
    *,
    doc_type: str,
    granularity: str | None,
) -> SummaryCorpusWindow:
    return SummaryCorpusWindow(
        repository=service.repository,
        vector_store=service.vector_store,
        run_id=service.run_id,
        doc_type=doc_type,
        granularity=granularity,
        period_start=service.period_start,
        period_end=service.period_end,
    )


def _collect_source_text_hits(
    service: SearchService,
    *,
    query: str,
    requested_sources: list[tuple[str, str | None]],
    limit: int,
) -> tuple[list[dict[str, Any]], list[str]]:
    hits: list[dict[str, Any]] = []
    seen_hits: set[tuple[int, int]] = set()
    matched_queries: list[str] = []
    for source_doc_type, source_granularity in requested_sources:
        source_hits, matched_for_source = _collect_text_hits_with_backoff(
            window=_text_search_window(
                service,
                doc_type=source_doc_type,
                granularity=source_granularity,
            ),
            query=query,
            limit=limit,
        )
        matched_queries = _dedupe_matched_queries(matched_queries, matched_for_source)
        for row in source_hits:
            key = search_hit_key(row)
            if key is None or key in seen_hits:
                continue
            seen_hits.add(key)
            hits.append(row)
    return hits, matched_queries


def _semantic_search_request(
    service: SearchService,
    *,
    query: str,
    doc_type: str,
    granularity: str | None,
    limit: int,
) -> SummarySearchRequest:
    return SummarySearchRequest(
        window=_text_search_window(
            service,
            doc_type=doc_type,
            granularity=granularity,
        ),
        query=query,
        embedding_model=service.embedding_model,
        embedding_dimensions=service.embedding_dimensions,
        max_batch_inputs=service.embedding_batch_max_inputs,
        max_batch_chars=service.embedding_batch_max_chars,
        embedding_failure_mode=str(service.embedding_failure_mode or "continue"),
        embedding_max_errors=int(service.embedding_max_errors or 0),
        limit=limit,
        metric_namespace=service.metric_namespace,
        llm_connection=service.llm_connection,
        auto_sync_vectors=bool(service.auto_sync_vectors),
    )


def _collect_semantic_hits(
    service: SearchService,
    *,
    query: str,
    requested_sources: list[tuple[str, str | None]],
    limit: int,
) -> list[Any]:
    hits: list[Any] = []
    seen_hits: set[tuple[int, int]] = set()
    for source_doc_type, source_granularity in requested_sources:
        source_hits = semantic_search_summaries_in_period(
            request=_semantic_search_request(
                service,
                query=query,
                doc_type=source_doc_type,
                granularity=source_granularity,
                limit=limit,
            )
        )
        for hit in source_hits:
            key = _semantic_hit_key(hit)
            if key is None or key in seen_hits:
                continue
            seen_hits.add(key)
            hits.append(hit)
    return hits


def _listed_source_docs(
    service: SearchService,
    *,
    requested_sources: list[tuple[str, str | None]],
    order_by: str,
    limit: int,
) -> list[Any]:
    docs: list[Any] = []
    seen_doc_ids: set[int] = set()
    for source_doc_type, source_granularity in requested_sources:
        rows = service.repository.list_documents(
            doc_type=source_doc_type,
            period_start=service.period_start,
            period_end=service.period_end,
            granularity=source_granularity,
            order_by=order_by,
            offset=0,
            limit=limit,
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
    return docs


def _serialize_docs(
    repository: TrendRepositoryPort,
    *,
    docs: list[Any],
) -> list[dict[str, Any]]:
    return [serialize_document(repository=repository, doc=doc) for doc in docs]


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
        docs = _listed_source_docs(
            self,
            requested_sources=requested_sources,
            order_by=normalized_order,
            limit=normalized_limit,
        )
        docs.sort(
            key=document_event_sort_key,
            reverse=normalized_order != "event_asc",
        )
        docs = docs[normalized_offset : normalized_offset + normalized_limit]
        out = _serialize_docs(self.repository, docs=docs)
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
        content_chunks = read_doc_content_chunks(
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
                "summary_sections": normalize_summary_sections(summary_text),
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

        hits, matched_queries = _collect_source_text_hits(
            self,
            query=str(query or ""),
            requested_sources=requested_sources,
            limit=normalized_limit,
        )
        hits.sort(
            key=lambda row: (
                int(row.get("backoff_depth") or 0),
                float(row.get("rank") or 0.0),
                int(row.get("doc_id") or 0),
                int(row.get("chunk_index") or 0),
            )
        )
        hits = attach_doc_metadata(
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

        hits = _collect_semantic_hits(
            self,
            query=str(query or ""),
            requested_sources=requested_sources,
            limit=normalized_limit,
        )
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
        rows = attach_doc_metadata(repository=self.repository, rows=rows)
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
    "_reciprocal_rank_fuse_search_hits",
]
