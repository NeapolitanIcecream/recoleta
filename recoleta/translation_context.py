from __future__ import annotations

from dataclasses import dataclass
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from loguru import logger
from sqlmodel import Session, select

from recoleta.config import Settings
from recoleta.models import Document, Item
from recoleta.presentation import (
    PRESENTATION_SCHEMA_VERSION,
    PRESENTATION_SCHEMA_VERSION_V1,
    presentation_sidecar_path,
    validate_presentation,
)
from recoleta.publish.idea_notes import resolve_ideas_note_path
from recoleta.publish.trend_notes import resolve_trend_note_path
from recoleta.rag.corpus_tools import CorpusSpec, SearchService
from recoleta.rag.vector_store import LanceVectorStore, embedding_table_name

_ITEM_CONTENT_TYPES = (
    "html_maintext",
    "markdown",
    "html_document",
    "pdf_text",
    "text",
)


@dataclass(frozen=True, slots=True)
class TranslationSearchServiceRequest:
    repository: Any
    settings: Settings
    run_id: str | None
    period_start: datetime
    period_end: datetime
    doc_type: str
    granularity: str | None = None


@dataclass(frozen=True, slots=True)
class HybridContextRequest:
    repository: Any
    settings: Settings
    run_id: str | None
    period_start: datetime | None
    period_end: datetime | None
    doc_type: str
    granularity: str | None
    query: str
    bundle_limit: int = 2


@dataclass(frozen=True, slots=True)
class ItemContextRequest:
    repository: Any
    settings: Settings
    run_id: str | None
    item: Item
    summary_text: str | None
    context_assist: str


@dataclass(frozen=True, slots=True)
class TrendContextRequest:
    repository: Any
    settings: Settings
    run_id: str | None
    payload: dict[str, Any]
    granularity: str | None
    period_start: datetime | None
    period_end: datetime | None
    context_assist: str


@dataclass(frozen=True, slots=True)
class IdeaContextRequest:
    repository: Any
    settings: Settings
    run_id: str | None
    payload: dict[str, Any]
    granularity: str | None
    period_start: datetime | None
    period_end: datetime | None
    context_assist: str


def first_nonempty_content_text(*, repository: Any, item_id: int) -> str | None:
    texts = repository.get_latest_content_texts(
        item_id=item_id,
        content_types=list(_ITEM_CONTENT_TYPES),
    )
    for content_type in _ITEM_CONTENT_TYPES:
        value = str(texts.get(content_type) or "").strip()
        if value:
            return value[:2000]
    return None


def doc_summary_text(*, repository: Any, doc_id: int) -> str | None:
    chunk = repository.read_document_chunk(doc_id=doc_id, chunk_index=0)
    if chunk is None:
        return None
    text = str(getattr(chunk, "text", "") or "").strip()
    return text or None


def doc_bundle_for_translation(
    *, repository: Any, doc_id: int
) -> dict[str, Any] | None:
    document = repository.get_document(doc_id=doc_id)
    if document is None:
        return None
    return {
        "doc_id": int(getattr(document, "id") or 0),
        "doc_type": str(getattr(document, "doc_type", "") or "").strip(),
        "title": str(getattr(document, "title", "") or "").strip(),
        "canonical_url": str(getattr(document, "canonical_url", "") or "").strip(),
        "summary": doc_summary_text(repository=repository, doc_id=doc_id),
    }


def translation_search_service(
    request: TranslationSearchServiceRequest,
) -> SearchService:
    return SearchService(
        repository=request.repository,
        vector_store=LanceVectorStore(
            db_dir=request.settings.rag_lancedb_dir,
            table_name=embedding_table_name(
                embedding_model=request.settings.trends_embedding_model,
                embedding_dimensions=request.settings.trends_embedding_dimensions,
            ),
        ),
        run_id=str(request.run_id or "").strip(),
        period_start=request.period_start,
        period_end=request.period_end,
        corpus_spec=CorpusSpec.from_rag_sources(
            [{"doc_type": request.doc_type, "granularity": request.granularity}]
        ),
        embedding_model=request.settings.trends_embedding_model,
        embedding_dimensions=request.settings.trends_embedding_dimensions,
        embedding_batch_max_inputs=request.settings.trends_embedding_batch_max_inputs,
        embedding_batch_max_chars=request.settings.trends_embedding_batch_max_chars,
        metric_namespace=_translation_metric_namespace(request.run_id),
        embedding_failure_mode=request.settings.trends_embedding_failure_mode,
        embedding_max_errors=request.settings.trends_embedding_max_errors,
        llm_connection=request.settings.llm_connection_config(),
        auto_sync_vectors=False,
    )


def hybrid_query(*parts: Any, max_chars: int = 280) -> str:
    tokens: list[str] = []
    for part in parts:
        if isinstance(part, str):
            candidate = part.strip()
            if candidate:
                tokens.append(candidate)
            continue
        if isinstance(part, list):
            for item in part:
                candidate = str(item or "").strip()
                if candidate:
                    tokens.append(candidate)
    joined = " | ".join(dict.fromkeys(tokens))
    return joined[:max_chars].strip()


def hybrid_context_for_query(request: HybridContextRequest) -> dict[str, Any]:
    normalized_query = str(request.query or "").strip()
    if not normalized_query:
        return _hybrid_context_payload(status="no_query")
    if not _has_hybrid_window(request):
        return _hybrid_context_payload(status="no_window")
    service = translation_search_service(_search_service_request(request))
    try:
        search_result = service.search_hybrid(
            query=normalized_query,
            doc_type=request.doc_type,
            granularity=request.granularity,
            limit=max(1, int(request.bundle_limit)),
        )
    except Exception as exc:  # noqa: BLE001
        _hybrid_failure_logger(request).warning(
            "Hybrid translation assist failed open error_type={} error={}",
            type(exc).__name__,
            str(exc),
        )
        return _hybrid_context_payload(
            status="failed_open",
            query=normalized_query,
            hybrid_error_type=type(exc).__name__,
        )
    bundles = _hybrid_match_bundles(
        service=service,
        search_result=search_result,
        bundle_limit=request.bundle_limit,
    )
    context = _hybrid_context_payload(
        status="ok" if bundles else "no_hits",
        query=normalized_query,
        hybrid_source_returned=dict(search_result.get("source_returned") or {}),
    )
    if bundles:
        context["hybrid_matches"] = bundles
    return context


def item_translation_context(request: ItemContextRequest) -> dict[str, Any]:
    if request.context_assist == "none":
        return {}
    item_id = int(getattr(request.item, "id") or 0)
    context: dict[str, Any] = {"item": _item_payload(request.item, item_id=item_id)}
    content_text = first_nonempty_content_text(
        repository=request.repository,
        item_id=item_id,
    )
    if content_text:
        context["item"]["content_excerpt"] = content_text
    if request.context_assist != "hybrid":
        return context
    period_start, period_end = _item_hybrid_window(request.item)
    context.update(
        hybrid_context_for_query(
            HybridContextRequest(
                repository=request.repository,
                settings=request.settings,
                run_id=request.run_id,
                period_start=period_start,
                period_end=period_end,
                doc_type="item",
                granularity=None,
                query=hybrid_query(
                    getattr(request.item, "title", None),
                    request.summary_text,
                    context["item"].get("content_excerpt"),
                ),
            )
        )
    )
    return context


def trend_translation_context(request: TrendContextRequest) -> dict[str, Any]:
    if request.context_assist == "none":
        return {}
    context: dict[str, Any] = {}
    representative_docs = _doc_bundles(
        repository=request.repository,
        doc_ids=_trend_representative_doc_ids(request.payload),
        limit=6,
    )
    if representative_docs:
        context["representative_docs"] = representative_docs
    if request.context_assist == "hybrid":
        context.update(
            hybrid_context_for_query(
                HybridContextRequest(
                    repository=request.repository,
                    settings=request.settings,
                    run_id=request.run_id,
                    period_start=request.period_start,
                    period_end=request.period_end,
                    doc_type="item",
                    granularity=None,
                    query=hybrid_query(
                        request.payload.get("title"),
                        request.payload.get("topics"),
                        list(request.payload.get("highlights") or [])[:2],
                    ),
                )
            )
        )
    return context


def idea_translation_context(request: IdeaContextRequest) -> dict[str, Any]:
    if request.context_assist == "none":
        return {}
    context: dict[str, Any] = {}
    evidence_docs = _doc_bundles(
        repository=request.repository,
        doc_ids=_idea_evidence_doc_ids(request.payload),
        limit=6,
    )
    if evidence_docs:
        context["evidence_docs"] = evidence_docs
    upstream_trend = _upstream_trend_bundle(
        repository=request.repository,
        granularity=request.granularity,
        period_start=request.period_start,
        period_end=request.period_end,
    )
    if upstream_trend is not None:
        context["upstream_trend"] = upstream_trend
    if request.context_assist == "hybrid":
        context.update(
            hybrid_context_for_query(
                HybridContextRequest(
                    repository=request.repository,
                    settings=request.settings,
                    run_id=request.run_id,
                    period_start=request.period_start,
                    period_end=request.period_end,
                    doc_type="item",
                    granularity=None,
                    query=hybrid_query(
                        request.payload.get("title"),
                        request.payload.get("summary_md"),
                        _idea_titles(request.payload),
                    ),
                )
            )
        )
    return context


def canonical_note_path(
    *,
    settings: Settings,
    candidate: Any,
) -> Path | None:
    root = Path(settings.markdown_output_dir).expanduser().resolve()
    if candidate.source_kind == "trend_synthesis":
        if candidate.granularity is None or candidate.period_start is None:
            return None
        return resolve_trend_note_path(
            note_dir=root / "Trends",
            trend_doc_id=candidate.source_record_id,
            granularity=candidate.granularity,
            period_start=candidate.period_start,
        )
    if candidate.source_kind == "trend_ideas":
        if candidate.granularity is None or candidate.period_start is None:
            return None
        return resolve_ideas_note_path(
            note_dir=root / "Ideas",
            granularity=candidate.granularity,
            period_start=candidate.period_start,
        )
    return None


def canonical_note_presentation_context(
    *,
    note_path: Path,
    sidecar_path: Path,
) -> dict[str, Any] | None:
    if not sidecar_path.exists() or not sidecar_path.is_file():
        return None
    try:
        payload = json.loads(sidecar_path.read_text(encoding="utf-8"))
    except Exception:
        return None
    try:
        schema_version = (
            int(payload.get("presentation_schema_version") or 0)
            if isinstance(payload, dict)
            else 0
        )
    except Exception:
        schema_version = 0
    if not isinstance(payload, dict) or schema_version not in {
        PRESENTATION_SCHEMA_VERSION_V1,
        PRESENTATION_SCHEMA_VERSION,
    }:
        return None
    if validate_presentation(payload):
        return None
    return {
        "canonical_note": {
            "path": str(note_path),
            "sidecar_path": str(sidecar_path),
        },
        "presentation": payload,
    }


def canonical_markdown_note_context(*, note_path: Path) -> dict[str, Any]:
    try:
        markdown_text = note_path.read_text(encoding="utf-8")
    except Exception:
        return {}
    lines = [line.rstrip() for line in markdown_text.splitlines()]
    title = next(
        (
            stripped[2:].strip()
            for line in lines
            if (stripped := line.strip()).startswith("# ")
        ),
        "",
    )
    body_excerpt = "\n".join(lines[:80]).strip()
    return {
        "canonical_note": {
            "path": str(note_path),
            "title": title or note_path.stem,
            "markdown_excerpt": body_excerpt[:4000],
        }
    }


def canonical_note_context(
    *,
    settings: Settings,
    candidate: Any,
) -> dict[str, Any]:
    note_path = canonical_note_path(settings=settings, candidate=candidate)
    if note_path is None or not note_path.exists() or not note_path.is_file():
        return {}
    sidecar_path = presentation_sidecar_path(note_path=note_path)
    presentation_context = canonical_note_presentation_context(
        note_path=note_path,
        sidecar_path=sidecar_path,
    )
    if presentation_context is not None:
        return presentation_context
    return canonical_markdown_note_context(note_path=note_path)


def build_candidate_context(
    *,
    repository: Any,
    settings: Settings,
    candidate: Any,
    context_assist: str,
    run_id: str | None,
) -> dict[str, Any]:
    if context_assist == "none":
        return {}
    note_context = canonical_note_context(settings=settings, candidate=candidate)
    if candidate.source_kind == "analysis" and candidate.item_id is not None:
        item = repository.get_item(item_id=candidate.item_id)
        if item is None:
            return note_context
        return {
            **note_context,
            **item_translation_context(
                ItemContextRequest(
                    repository=repository,
                    settings=settings,
                    run_id=run_id,
                    item=item,
                    summary_text=str(candidate.payload.get("summary") or "").strip()
                    or None,
                    context_assist=context_assist,
                )
            ),
        }
    if candidate.source_kind == "trend_synthesis":
        return {
            **note_context,
            **trend_translation_context(
                TrendContextRequest(
                    repository=repository,
                    settings=settings,
                    run_id=run_id,
                    payload=candidate.payload,
                    granularity=candidate.granularity,
                    period_start=candidate.period_start,
                    period_end=candidate.period_end,
                    context_assist=context_assist,
                )
            ),
        }
    if candidate.source_kind == "trend_ideas":
        return {
            **note_context,
            **idea_translation_context(
                IdeaContextRequest(
                    repository=repository,
                    settings=settings,
                    run_id=run_id,
                    payload=candidate.payload,
                    granularity=candidate.granularity,
                    period_start=candidate.period_start,
                    period_end=candidate.period_end,
                    context_assist=context_assist,
                )
            ),
        }
    return note_context


def _translation_metric_namespace(run_id: str | None) -> str | None:
    return "pipeline.translate.context" if str(run_id or "").strip() else None


def _search_service_request(
    request: HybridContextRequest,
) -> TranslationSearchServiceRequest:
    assert isinstance(request.period_start, datetime)
    assert isinstance(request.period_end, datetime)
    return TranslationSearchServiceRequest(
        repository=request.repository,
        settings=request.settings,
        run_id=request.run_id,
        period_start=request.period_start,
        period_end=request.period_end,
        doc_type=request.doc_type,
        granularity=request.granularity,
    )


def _has_hybrid_window(request: HybridContextRequest) -> bool:
    return isinstance(request.period_start, datetime) and isinstance(
        request.period_end,
        datetime,
    )


def _hybrid_failure_logger(request: HybridContextRequest) -> Any:
    return logger.bind(
        module="translation.context",
        doc_type=request.doc_type,
        granularity=request.granularity,
    )


def _hybrid_context_payload(
    *,
    status: str,
    query: str | None = None,
    hybrid_source_returned: dict[str, Any] | None = None,
    hybrid_error_type: str | None = None,
) -> dict[str, Any]:
    context: dict[str, Any] = {
        "assist_mode": "hybrid",
        "hybrid_status": status,
    }
    if query:
        context["hybrid_query"] = query
    if hybrid_source_returned is not None:
        context["hybrid_source_returned"] = hybrid_source_returned
    if hybrid_error_type is not None:
        context["hybrid_error_type"] = hybrid_error_type
    return context


def _hybrid_match_bundles(
    *,
    service: SearchService,
    search_result: dict[str, Any],
    bundle_limit: int,
) -> list[dict[str, Any]]:
    bundles: list[dict[str, Any]] = []
    seen_doc_ids: set[int] = set()
    for doc_id in _hybrid_doc_ids(search_result):
        if doc_id in seen_doc_ids:
            continue
        seen_doc_ids.add(doc_id)
        bundle_result = service.get_doc_bundle(
            doc_id=doc_id,
            content_limit=1,
            content_chars=500,
        )
        bundle = (
            bundle_result.get("bundle") if isinstance(bundle_result, dict) else None
        )
        if isinstance(bundle, dict):
            bundles.append(bundle)
        if len(bundles) >= bundle_limit:
            break
    return bundles


def _hybrid_doc_ids(search_result: dict[str, Any]) -> list[int]:
    doc_ids: list[int] = []
    for hit in list(search_result.get("hits") or []):
        try:
            doc_id = int(hit.get("doc_id") or 0) if isinstance(hit, dict) else 0
        except Exception:
            doc_id = 0
        if doc_id > 0:
            doc_ids.append(doc_id)
    return doc_ids


def _item_payload(item: Item, *, item_id: int) -> dict[str, Any]:
    return {
        "item_id": item_id,
        "title": str(getattr(item, "title", "") or "").strip(),
        "canonical_url": str(getattr(item, "canonical_url", "") or "").strip(),
        "source": str(getattr(item, "source", "") or "").strip(),
    }


def _item_hybrid_window(item: Item) -> tuple[datetime | None, datetime | None]:
    published_at = getattr(item, "published_at", None)
    if not isinstance(published_at, datetime):
        return None, None
    return published_at - timedelta(days=30), published_at + timedelta(days=1)


def _trend_representative_doc_ids(payload: dict[str, Any]) -> list[int]:
    doc_ids: list[int] = []
    for cluster in list(payload.get("clusters") or [])[:3]:
        if not isinstance(cluster, dict):
            continue
        for ref in list(cluster.get("representative_chunks") or [])[:4]:
            doc_id = _doc_id_from_ref(ref)
            if doc_id > 0:
                doc_ids.append(doc_id)
        if len(doc_ids) >= 6:
            return doc_ids[:6]
    return doc_ids[:6]


def _idea_evidence_doc_ids(payload: dict[str, Any]) -> list[int]:
    doc_ids: list[int] = []
    for idea in list(payload.get("ideas") or [])[:4]:
        if not isinstance(idea, dict):
            continue
        for ref in list(idea.get("evidence_refs") or [])[:4]:
            doc_id = _doc_id_from_ref(ref)
            if doc_id > 0:
                doc_ids.append(doc_id)
        if len(doc_ids) >= 6:
            return doc_ids[:6]
    return doc_ids[:6]


def _doc_id_from_ref(ref: Any) -> int:
    if not isinstance(ref, dict):
        return 0
    try:
        return int(ref.get("doc_id") or 0)
    except Exception:
        return 0


def _doc_bundles(
    *,
    repository: Any,
    doc_ids: list[int],
    limit: int,
) -> list[dict[str, Any]]:
    bundles: list[dict[str, Any]] = []
    seen_doc_ids: set[int] = set()
    for doc_id in doc_ids:
        if doc_id <= 0 or doc_id in seen_doc_ids:
            continue
        seen_doc_ids.add(doc_id)
        bundle = doc_bundle_for_translation(repository=repository, doc_id=doc_id)
        if bundle is not None:
            bundles.append(bundle)
        if len(bundles) >= limit:
            return bundles
    return bundles


def _upstream_trend_bundle(
    *,
    repository: Any,
    granularity: str | None,
    period_start: datetime | None,
    period_end: datetime | None,
) -> dict[str, Any] | None:
    if (
        not isinstance(period_start, datetime)
        or not isinstance(period_end, datetime)
        or granularity is None
    ):
        return None
    with Session(repository.engine) as session:
        trend_doc = session.exec(
            select(Document).where(
                Document.doc_type == "trend",
                Document.granularity == granularity,
                Document.period_start == period_start,
                Document.period_end == period_end,
            )
        ).first()
    trend_doc_id = int(getattr(trend_doc, "id") or 0) if trend_doc is not None else 0
    if trend_doc_id <= 0:
        return None
    return doc_bundle_for_translation(repository=repository, doc_id=trend_doc_id)


def _idea_titles(payload: dict[str, Any]) -> list[str]:
    return [
        str(idea.get("title") or "").strip()
        for idea in list(payload.get("ideas") or [])[:3]
        if isinstance(idea, dict) and str(idea.get("title") or "").strip()
    ]
