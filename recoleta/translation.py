from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
import json
from pathlib import Path
import time
from typing import Any, cast

from loguru import logger
from pydantic import BaseModel, ValidationError
from sqlalchemy import desc, func
from sqlmodel import Session, select

from recoleta.analyzer import (
    _extract_content,
    _extract_token_counts,
    _extract_usage_dict,
    _get_completion,
    _resolve_response_cost_usd,
)
from recoleta.config import LocalizationConfig, Settings
from recoleta.llm_connection import LLMConnectionConfig
from recoleta.models import Analysis, Document, DocumentChunk, Item, PassOutput
from recoleta.passes.trend_ideas import TrendIdeasPayload
from recoleta.presentation import (
    PRESENTATION_SCHEMA_VERSION,
    PRESENTATION_SCHEMA_VERSION_V1,
    presentation_sidecar_path,
    validate_presentation,
)
from recoleta.prompt_style import reader_facing_ai_tropes_prompt
from recoleta.provenance import build_projection_provenance, inject_projection_provenance
from recoleta.publish.idea_notes import resolve_ideas_note_path
from recoleta.publish.trend_notes import resolve_trend_note_path
from recoleta.rag.corpus_tools import CorpusSpec, SearchService
from recoleta.rag.vector_store import LanceVectorStore, embedding_table_name
from recoleta.storage.common import _to_json
from recoleta.trends import TrendPayload
from recoleta.types import sha256_hex

TRANSLATION_CONTEXT_ASSIST_VALUES = {"none", "direct", "hybrid"}
TRANSLATION_INCLUDE_VALUES = {"items", "trends", "ideas"}
_PROVIDER_FAILURE_ERROR_TYPES = {
    "APIConnectionError",
    "APIError",
    "AuthenticationError",
    "RateLimitError",
    "ServiceUnavailableError",
    "Timeout",
}
_PROVIDER_FAILURE_ABORT_THRESHOLD = 5
_DEFAULT_TRANSLATION_PARALLELISM = 4

_ITEM_CONTENT_TYPES = (
    "html_maintext",
    "markdown",
    "html_document",
    "pdf_text",
    "text",
)


class _AnalysisTranslationPayload(BaseModel):
    summary: str


@dataclass(frozen=True, slots=True)
class TranslationTarget:
    code: str
    llm_label: str


@dataclass(frozen=True, slots=True)
class TranslationCandidate:
    source_kind: str
    source_record_id: int
    payload: dict[str, Any]
    payload_model: type[BaseModel] | None
    canonical_language_code: str | None
    item_id: int | None = None
    document_id: int | None = None
    granularity: str | None = None
    period_start: datetime | None = None
    period_end: datetime | None = None


@dataclass(slots=True)
class TranslationRunResult:
    scanned_total: int = 0
    translated_total: int = 0
    mirrored_total: int = 0
    skipped_total: int = 0
    failed_total: int = 0
    aborted: bool = False
    abort_reason: str | None = None


@dataclass(frozen=True, slots=True)
class _PreparedTranslationTask:
    candidate: TranslationCandidate
    target: TranslationTarget
    source_hash: str
    context: dict[str, Any]


@dataclass(frozen=True, slots=True)
class _CompletedTranslationTask:
    translated_payload: dict[str, Any]
    debug: dict[str, Any]
    duration_ms: int


@dataclass(slots=True)
class _ProviderFailureTracker:
    last_signature: tuple[str, str] | None = None
    consecutive_count: int = 0

    def record(self, exc: Exception) -> str | None:
        signature = _provider_failure_signature(exc)
        if signature is None:
            self.last_signature = None
            self.consecutive_count = 0
            return None
        if signature == self.last_signature:
            self.consecutive_count += 1
        else:
            self.last_signature = signature
            self.consecutive_count = 1
        if self.consecutive_count < _PROVIDER_FAILURE_ABORT_THRESHOLD:
            return None
        error_type, message = signature
        return (
            "aborting after "
            f"{self.consecutive_count} consecutive provider failures "
            f"({error_type}: {message})"
        )

    def reset(self) -> None:
        self.last_signature = None
        self.consecutive_count = 0


def normalize_context_assist(value: str | None) -> str:
    normalized = str(value or "").strip().lower() or "direct"
    if normalized not in TRANSLATION_CONTEXT_ASSIST_VALUES:
        allowed = ", ".join(sorted(TRANSLATION_CONTEXT_ASSIST_VALUES))
        raise ValueError(f"context_assist must be one of: {allowed}")
    return normalized


def normalize_include(value: str | list[str] | None) -> set[str]:
    if value is None:
        return set(TRANSLATION_INCLUDE_VALUES)
    raw_values: list[str]
    if isinstance(value, str):
        raw_values = [part.strip().lower() for part in value.split(",")]
    else:
        raw_values = [str(part).strip().lower() for part in value]
    normalized = {part for part in raw_values if part}
    unknown = sorted(normalized - TRANSLATION_INCLUDE_VALUES)
    if unknown:
        allowed = ", ".join(sorted(TRANSLATION_INCLUDE_VALUES))
        raise ValueError(f"include must only contain: {allowed}")
    return normalized or set(TRANSLATION_INCLUDE_VALUES)


def language_slug(value: str) -> str:
    return str(value or "").strip().lower().replace("_", "-")


def _payload_hash(payload: dict[str, Any]) -> str:
    return sha256_hex(_to_json(payload))


def _provider_failure_signature(exc: Exception) -> tuple[str, str] | None:
    error_type = type(exc).__name__
    if error_type not in _PROVIDER_FAILURE_ERROR_TYPES:
        return None
    message = " ".join(str(exc).strip().split()).lower()
    if not message:
        message = error_type.lower()
    if len(message) > 240:
        message = message[:240]
    return error_type, message


def _normalize_utc_datetime(value: datetime | None) -> datetime | None:
    if not isinstance(value, datetime):
        return None
    if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def _periods_overlap(
    *,
    candidate_start: datetime | None,
    candidate_end: datetime | None,
    period_start: datetime | None,
    period_end: datetime | None,
) -> bool:
    normalized_candidate_start = _normalize_utc_datetime(candidate_start)
    normalized_candidate_end = _normalize_utc_datetime(candidate_end)
    normalized_period_start = _normalize_utc_datetime(period_start)
    normalized_period_end = _normalize_utc_datetime(period_end)
    if normalized_candidate_start is None or normalized_candidate_end is None:
        return False
    if (
        normalized_period_start is not None
        and normalized_candidate_end <= normalized_period_start
    ):
        return False
    if (
        normalized_period_end is not None
        and normalized_candidate_start >= normalized_period_end
    ):
        return False
    return True


def _coerce_payload_dict(
    payload: BaseModel | dict[str, Any] | Any,
    *,
    payload_model: type[BaseModel] | None,
) -> dict[str, Any]:
    if isinstance(payload, BaseModel):
        return payload.model_dump(mode="json")
    if payload_model is not None:
        return payload_model.model_validate(payload).model_dump(mode="json")
    if not isinstance(payload, dict):
        raise ValueError("translated payload must be a JSON object")
    return payload


def translate_structured_payload(
    *,
    model: str,
    source_kind: str,
    payload: dict[str, Any],
    source_language_code: str,
    target_language_code: str,
    source_language_label: str | None = None,
    target_language_label: str | None = None,
    context: dict[str, Any] | None = None,
    payload_model: type[BaseModel] | None = None,
    llm_connection: LLMConnectionConfig | None = None,
    return_debug: bool = False,
) -> dict[str, Any] | tuple[dict[str, Any], dict[str, Any]]:
    translated_payload, debug = _translate_structured_payload_with_debug(
        model=model,
        source_kind=source_kind,
        payload=payload,
        source_language_code=source_language_code,
        target_language_code=target_language_code,
        source_language_label=source_language_label,
        target_language_label=target_language_label,
        context=context,
        payload_model=payload_model,
        llm_connection=llm_connection,
    )
    if return_debug:
        return translated_payload, debug
    return translated_payload


def _translate_structured_payload_with_debug(
    *,
    model: str,
    source_kind: str,
    payload: dict[str, Any],
    source_language_code: str,
    target_language_code: str,
    source_language_label: str | None = None,
    target_language_label: str | None = None,
    context: dict[str, Any] | None = None,
    payload_model: type[BaseModel] | None = None,
    llm_connection: LLMConnectionConfig | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    normalized_model = str(model or "").strip()
    if not normalized_model:
        raise ValueError("model must not be empty")

    normalized_payload = _coerce_payload_dict(payload, payload_model=payload_model)
    connection = llm_connection or LLMConnectionConfig()
    source_label = str(source_language_label or source_language_code).strip()
    target_label = str(target_language_label or target_language_code).strip()
    context_payload = context if isinstance(context, dict) else {}

    system_message = _build_translation_system_message()
    user_message = (
        f"Translate this {source_kind} payload from {source_label} to {target_label}.\n\n"
        "Rules:\n"
        "- Keep markdown structure valid inside translated string values.\n"
        "- Preserve topics/tags/kind/time_horizon/change_type/doc_id/chunk_index values unless they are clearly prose.\n"
        "- Keep JSON keys in English exactly as provided.\n"
        "- Return one JSON object only.\n\n"
        "Context JSON:\n"
        f"{json.dumps(context_payload, ensure_ascii=False, sort_keys=True)}\n\n"
        "Payload JSON:\n"
        f"{json.dumps(normalized_payload, ensure_ascii=False, sort_keys=True)}"
    )

    response = _get_completion()(
        model=normalized_model,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        response_format={"type": "json_object"},
        **connection.litellm_completion_kwargs(),
    )
    usage = _extract_usage_dict(response)
    prompt_tokens, completion_tokens, total_tokens = _extract_token_counts(usage)
    cost_usd = _resolve_response_cost_usd(
        response=response,
        model=normalized_model,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
    )
    raw_content = _extract_content(response)
    try:
        decoded = json.loads(raw_content)
    except json.JSONDecodeError as exc:
        raise ValueError(f"translation LLM returned invalid JSON: {exc.msg}") from exc

    if payload_model is not None:
        try:
            translated_payload = payload_model.model_validate(decoded).model_dump(
                mode="json"
            )
        except ValidationError as exc:
            raise ValueError(
                f"translation LLM returned JSON with invalid schema: {type(exc).__name__}"
            ) from exc
    elif not isinstance(decoded, dict):
        raise ValueError("translation LLM returned a non-object JSON payload")
    else:
        translated_payload = decoded
    debug_usage: dict[str, Any] = {"requests": 1}
    if prompt_tokens is not None:
        debug_usage["input_tokens"] = prompt_tokens
    if completion_tokens is not None:
        debug_usage["output_tokens"] = completion_tokens
    if total_tokens is not None:
        debug_usage["total_tokens"] = total_tokens
    if isinstance(usage, dict):
        if "cost" in usage:
            debug_usage["cost"] = usage["cost"]
        if "cost_details" in usage and isinstance(usage["cost_details"], dict):
            debug_usage["cost_details"] = usage["cost_details"]
    return translated_payload, {
        "usage": debug_usage,
        "estimated_cost_usd": cost_usd,
    }


def _build_translation_system_message() -> str:
    base = (
        "You translate structured Recoleta research outputs between languages. "
        "Return strict JSON only. Preserve the input JSON shape exactly. "
        "Do not add or remove keys, do not reorder arrays unnecessarily, and do not invent facts. "
        "Translate only natural-language prose. Preserve URLs, markdown link targets, ids, timestamps, "
        "topic slugs, enum-like tokens, doc references, and evidence refs exactly."
    )
    guardrail = (
        "When multiple target-language phrasings are equally faithful, choose the most direct, "
        "least rhetorical, least templated phrasing. Do not use this freedom to change claims, "
        "add or remove facts, reorder arrays, or alter JSON structure."
    )
    return "\n\n".join(
        [
            base,
            reader_facing_ai_tropes_prompt(),
            guardrail,
        ]
    )


def _latest_meta_chunk_for_doc(
    session: Session,
    *,
    doc_id: int,
    source_content_type: str | None = None,
) -> DocumentChunk | None:
    statement = select(DocumentChunk).where(
        DocumentChunk.doc_id == int(doc_id),
        DocumentChunk.kind == "meta",
    )
    if source_content_type is not None:
        statement = statement.where(
            DocumentChunk.source_content_type == str(source_content_type).strip()
        )
    statement = statement.order_by(
        desc(cast(Any, DocumentChunk.chunk_index)),
        desc(cast(Any, DocumentChunk.id)),
    )
    return session.exec(statement).first()


def _first_nonempty_content_text(*, repository: Any, item_id: int) -> str | None:
    texts = repository.get_latest_content_texts(
        item_id=item_id,
        content_types=list(_ITEM_CONTENT_TYPES),
    )
    for content_type in _ITEM_CONTENT_TYPES:
        value = str(texts.get(content_type) or "").strip()
        if value:
            return value[:2000]
    return None


def _doc_summary_text(*, repository: Any, doc_id: int) -> str | None:
    chunk = repository.read_document_chunk(doc_id=doc_id, chunk_index=0)
    if chunk is None:
        return None
    text = str(getattr(chunk, "text", "") or "").strip()
    return text or None


def _doc_bundle_for_translation(*, repository: Any, doc_id: int) -> dict[str, Any] | None:
    document = repository.get_document(doc_id=doc_id)
    if document is None:
        return None
    return {
        "doc_id": int(getattr(document, "id") or 0),
        "doc_type": str(getattr(document, "doc_type", "") or "").strip(),
        "title": str(getattr(document, "title", "") or "").strip(),
        "canonical_url": str(getattr(document, "canonical_url", "") or "").strip(),
        "summary": _doc_summary_text(repository=repository, doc_id=doc_id),
    }


def _translation_search_service(
    *,
    repository: Any,
    settings: Settings,
    run_id: str | None,
    period_start: datetime,
    period_end: datetime,
    doc_type: str,
    granularity: str | None = None,
) -> SearchService:
    return SearchService(
        repository=repository,
        vector_store=LanceVectorStore(
            db_dir=settings.rag_lancedb_dir,
            table_name=embedding_table_name(
                embedding_model=settings.trends_embedding_model,
                embedding_dimensions=settings.trends_embedding_dimensions,
            ),
        ),
        run_id=str(run_id or "").strip(),
        period_start=period_start,
        period_end=period_end,
        corpus_spec=CorpusSpec.from_rag_sources(
            [{"doc_type": doc_type, "granularity": granularity}]
        ),
        embedding_model=settings.trends_embedding_model,
        embedding_dimensions=settings.trends_embedding_dimensions,
        embedding_batch_max_inputs=settings.trends_embedding_batch_max_inputs,
        embedding_batch_max_chars=settings.trends_embedding_batch_max_chars,
        metric_namespace=(
            "pipeline.translate.context" if str(run_id or "").strip() else None
        ),
        embedding_failure_mode=settings.trends_embedding_failure_mode,
        embedding_max_errors=settings.trends_embedding_max_errors,
        llm_connection=settings.llm_connection_config(),
        auto_sync_vectors=False,
    )


def _hybrid_query(*parts: Any, max_chars: int = 280) -> str:
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


def _hybrid_context_for_query(
    *,
    repository: Any,
    settings: Settings,
    run_id: str | None,
    period_start: datetime | None,
    period_end: datetime | None,
    doc_type: str,
    granularity: str | None,
    query: str,
    bundle_limit: int = 2,
) -> dict[str, Any]:
    normalized_query = str(query or "").strip()
    if not normalized_query:
        return {"assist_mode": "hybrid", "hybrid_status": "no_query"}
    if not isinstance(period_start, datetime) or not isinstance(period_end, datetime):
        return {"assist_mode": "hybrid", "hybrid_status": "no_window"}

    service = _translation_search_service(
        repository=repository,
        settings=settings,
        run_id=run_id,
        period_start=period_start,
        period_end=period_end,
        doc_type=doc_type,
        granularity=granularity,
    )
    log = logger.bind(
        module="translation.context",
        doc_type=doc_type,
        granularity=granularity,
    )
    try:
        search_result = service.search_hybrid(
            query=normalized_query,
            doc_type=doc_type,
            granularity=granularity,
            limit=max(1, int(bundle_limit)),
        )
    except Exception as exc:  # noqa: BLE001
        log.warning(
            "Hybrid translation assist failed open error_type={} error={}",
            type(exc).__name__,
            str(exc),
        )
        return {
            "assist_mode": "hybrid",
            "hybrid_status": "failed_open",
            "hybrid_query": normalized_query,
            "hybrid_error_type": type(exc).__name__,
        }

    bundles: list[dict[str, Any]] = []
    seen_doc_ids: set[int] = set()
    for hit in list(search_result.get("hits") or []):
        if not isinstance(hit, dict):
            continue
        try:
            doc_id = int(hit.get("doc_id") or 0)
        except Exception:
            doc_id = 0
        if doc_id <= 0 or doc_id in seen_doc_ids:
            continue
        seen_doc_ids.add(doc_id)
        bundle_result = service.get_doc_bundle(
            doc_id=doc_id,
            content_limit=1,
            content_chars=500,
        )
        bundle = bundle_result.get("bundle") if isinstance(bundle_result, dict) else None
        if isinstance(bundle, dict):
            bundles.append(bundle)
        if len(bundles) >= bundle_limit:
            break

    context = {
        "assist_mode": "hybrid",
        "hybrid_status": "ok" if bundles else "no_hits",
        "hybrid_query": normalized_query,
        "hybrid_source_returned": dict(search_result.get("source_returned") or {}),
    }
    if bundles:
        context["hybrid_matches"] = bundles
    return context


def _item_translation_context(
    *,
    repository: Any,
    settings: Settings,
    run_id: str | None,
    item: Item,
    summary_text: str | None,
    context_assist: str,
) -> dict[str, Any]:
    if context_assist == "none":
        return {}
    item_id = int(getattr(item, "id") or 0)
    context: dict[str, Any] = {
        "item": {
            "item_id": item_id,
            "title": str(getattr(item, "title", "") or "").strip(),
            "canonical_url": str(getattr(item, "canonical_url", "") or "").strip(),
            "source": str(getattr(item, "source", "") or "").strip(),
        }
    }
    if content_text := _first_nonempty_content_text(repository=repository, item_id=item_id):
        context["item"]["content_excerpt"] = content_text
    if context_assist == "hybrid":
        published_at = getattr(item, "published_at", None)
        period_start = (
            published_at - timedelta(days=30)
            if isinstance(published_at, datetime)
            else None
        )
        period_end = (
            published_at + timedelta(days=1)
            if isinstance(published_at, datetime)
            else None
        )
        context.update(
            _hybrid_context_for_query(
                repository=repository,
                settings=settings,
                run_id=run_id,
                period_start=period_start,
                period_end=period_end,
                doc_type="item",
                granularity=None,
                query=_hybrid_query(
                    getattr(item, "title", None),
                    summary_text,
                    context["item"].get("content_excerpt"),
                ),
            )
        )
    return context


def _trend_translation_context(
    *,
    repository: Any,
    settings: Settings,
    run_id: str | None,
    payload: dict[str, Any],
    granularity: str | None,
    period_start: datetime | None,
    period_end: datetime | None,
    context_assist: str,
) -> dict[str, Any]:
    if context_assist == "none":
        return {}
    context: dict[str, Any] = {}
    representative_docs: list[dict[str, Any]] = []
    for cluster in list(payload.get("clusters") or [])[:3]:
        if not isinstance(cluster, dict):
            continue
        for ref in list(cluster.get("representative_chunks") or [])[:4]:
            if not isinstance(ref, dict):
                continue
            try:
                doc_id = int(ref.get("doc_id") or 0)
            except Exception:
                doc_id = 0
            if doc_id <= 0:
                continue
            if bundle := _doc_bundle_for_translation(repository=repository, doc_id=doc_id):
                representative_docs.append(bundle)
        if len(representative_docs) >= 6:
            break
    if representative_docs:
        context["representative_docs"] = representative_docs[:6]
    if context_assist == "hybrid":
        context.update(
            _hybrid_context_for_query(
                repository=repository,
                settings=settings,
                run_id=run_id,
                period_start=period_start,
                period_end=period_end,
                doc_type="item",
                granularity=None,
                query=_hybrid_query(
                    payload.get("title"),
                    payload.get("topics"),
                    list(payload.get("highlights") or [])[:2],
                ),
            )
        )
    return context


def _idea_translation_context(
    *,
    repository: Any,
    settings: Settings,
    run_id: str | None,
    payload: dict[str, Any],
    granularity: str | None,
    period_start: datetime | None,
    period_end: datetime | None,
    context_assist: str,
) -> dict[str, Any]:
    if context_assist == "none":
        return {}
    context: dict[str, Any] = {}
    evidence_docs: list[dict[str, Any]] = []
    for idea in list(payload.get("ideas") or [])[:4]:
        if not isinstance(idea, dict):
            continue
        for ref in list(idea.get("evidence_refs") or [])[:4]:
            if not isinstance(ref, dict):
                continue
            try:
                doc_id = int(ref.get("doc_id") or 0)
            except Exception:
                doc_id = 0
            if doc_id <= 0:
                continue
            if bundle := _doc_bundle_for_translation(repository=repository, doc_id=doc_id):
                evidence_docs.append(bundle)
        if len(evidence_docs) >= 6:
            break
    if evidence_docs:
        context["evidence_docs"] = evidence_docs[:6]

    if (
        isinstance(period_start, datetime)
        and isinstance(period_end, datetime)
        and granularity is not None
    ):
        with Session(repository.engine) as session:
            trend_doc = session.exec(
                select(Document).where(
                    Document.doc_type == "trend",
                    Document.granularity == granularity,
                    Document.period_start == period_start,
                    Document.period_end == period_end,
                )
            ).first()
        if trend_doc is not None:
            trend_doc_id = int(getattr(trend_doc, "id") or 0)
            if trend_doc_id > 0:
                context["upstream_trend"] = _doc_bundle_for_translation(
                    repository=repository,
                    doc_id=trend_doc_id,
                )

    if context_assist == "hybrid":
        idea_titles = [
            str(idea.get("title") or "").strip()
            for idea in list(payload.get("ideas") or [])[:3]
            if isinstance(idea, dict) and str(idea.get("title") or "").strip()
        ]
        context.update(
            _hybrid_context_for_query(
                repository=repository,
                settings=settings,
                run_id=run_id,
                period_start=period_start,
                period_end=period_end,
                doc_type="item",
                granularity=None,
                query=_hybrid_query(
                    payload.get("title"),
                    payload.get("summary_md"),
                    idea_titles,
                ),
            )
        )
    return context


def _load_item_candidates(
    *,
    repository: Any,
    limit: int | None,
    period_start: datetime | None = None,
    period_end: datetime | None = None,
    all_history: bool = True,
) -> list[tuple[Analysis, Item]]:
    normalized_limit = None if limit is None else max(1, int(limit))
    with Session(repository.engine) as session:
        event_at = func.coalesce(cast(Any, Item.published_at), cast(Any, Item.created_at))
        statement = (
            select(Analysis, Item)
            .join(Item, cast(Any, Analysis.item_id) == cast(Any, Item.id))
            .order_by(desc(cast(Any, Analysis.id)))
        )
        if not all_history:
            if period_start is not None:
                statement = statement.where(event_at >= period_start)
            if period_end is not None:
                statement = statement.where(event_at < period_end)
        if normalized_limit is not None:
            statement = statement.limit(normalized_limit)
        return list(session.exec(statement))


def _latest_pass_output_payload(
    *,
    repository: Any,
    pass_kind: str,
    granularity: str | None,
    period_start: datetime | None,
    period_end: datetime | None,
    payload_model: type[BaseModel],
) -> dict[str, Any] | None:
    row = repository.get_latest_pass_output(
        pass_kind=pass_kind,
        status="succeeded",
        granularity=granularity,
        period_start=period_start,
        period_end=period_end,
    )
    if row is None:
        return None
    try:
        return payload_model.model_validate(
            json.loads(str(getattr(row, "payload_json", "") or "{}"))
        ).model_dump(mode="json")
    except Exception:
        return None


def _limit_documents_for_backfill(
    *,
    documents: list[Document],
    all_history: bool,
    limit: int | None,
) -> list[Document]:
    selected = documents
    if not all_history:
        latest_by_granularity: set[str | None] = set()
        selected = []
        for document in documents:
            key = str(getattr(document, "granularity", "") or "").strip().lower() or None
            if key in latest_by_granularity:
                continue
            latest_by_granularity.add(key)
            selected.append(document)
    normalized_limit = None if limit is None else max(1, int(limit))
    if normalized_limit is not None:
        return selected[:normalized_limit]
    return selected


def _load_trend_candidates(
    *,
    repository: Any,
    granularity: str | None,
    limit: int | None,
    period_start: datetime | None = None,
    period_end: datetime | None = None,
    all_history: bool = True,
) -> list[tuple[Document, dict[str, Any]]]:
    with Session(repository.engine) as session:
        statement = (
            select(Document)
            .where(Document.doc_type == "trend")
            .order_by(
                desc(cast(Any, Document.period_start)),
                desc(cast(Any, Document.id)),
            )
        )
        if granularity is not None:
            statement = statement.where(Document.granularity == granularity)
        documents = list(session.exec(statement))
        if not all_history and (period_start is not None or period_end is not None):
            filtered: list[Document] = []
            for document in documents:
                if not _periods_overlap(
                    candidate_start=getattr(document, "period_start", None),
                    candidate_end=getattr(document, "period_end", None),
                    period_start=period_start,
                    period_end=period_end,
                ):
                    continue
                filtered.append(document)
            documents = filtered
            normalized_limit = None if limit is None else max(1, int(limit))
            if normalized_limit is not None:
                documents = documents[:normalized_limit]
        else:
            documents = _limit_documents_for_backfill(
                documents=documents,
                all_history=all_history,
                limit=limit,
            )

        candidates: list[tuple[Document, dict[str, Any]]] = []
        for document in documents:
            doc_id = int(getattr(document, "id") or 0)
            if doc_id <= 0:
                continue
            payload = _latest_pass_output_payload(
                repository=repository,
                pass_kind="trend_synthesis",
                granularity=str(getattr(document, "granularity", "") or "").strip() or None,
                period_start=getattr(document, "period_start", None),
                period_end=getattr(document, "period_end", None),
                payload_model=TrendPayload,
            )
            if payload is None:
                meta_chunk = _latest_meta_chunk_for_doc(
                    session,
                    doc_id=doc_id,
                    source_content_type="trend_payload_json",
                )
                if meta_chunk is None:
                    continue
                try:
                    payload = TrendPayload.model_validate(
                        json.loads(str(meta_chunk.text or "{}"))
                    ).model_dump(mode="json")
                except Exception:
                    continue
            candidates.append((document, payload))
        return candidates


def _load_idea_candidates(
    *,
    repository: Any,
    granularity: str | None,
    limit: int | None,
    period_start: datetime | None = None,
    period_end: datetime | None = None,
    all_history: bool = True,
) -> list[tuple[Document, dict[str, Any]]]:
    def _render_idea_document_chunk_text(idea: Any) -> str:
        evidence_reasons = [
            str(getattr(ref, "reason", "") or "").strip()
            for ref in list(getattr(idea, "evidence_refs", []) or [])
            if str(getattr(ref, "reason", "") or "").strip()
        ]
        lines = [
            f"Title: {str(getattr(idea, 'title', '') or '').strip()}",
            f"Kind: {str(getattr(idea, 'kind', '') or '').strip()}",
            f"Time horizon: {str(getattr(idea, 'time_horizon', '') or '').strip()}",
            f"User/job: {str(getattr(idea, 'user_or_job', '') or '').strip()}",
            f"Thesis: {str(getattr(idea, 'thesis', '') or '').strip()}",
            (
                "Anti-thesis: "
                + str(getattr(idea, "anti_thesis", "") or "").strip()
            ),
            f"Why now: {str(getattr(idea, 'why_now', '') or '').strip()}",
            f"What changed: {str(getattr(idea, 'what_changed', '') or '').strip()}",
            (
                "Validation next step: "
                + str(getattr(idea, "validation_next_step", "") or "").strip()
            ),
        ]
        if evidence_reasons:
            lines.append("Evidence: " + " | ".join(evidence_reasons))
        return "\n".join(line for line in lines if str(line).strip()).strip()

    def _ideas_upstream_pass_output_id(*, row: PassOutput) -> int | None:
        try:
            input_refs = json.loads(str(row.input_refs_json or "[]"))
        except Exception:
            return None
        if not isinstance(input_refs, list):
            return None
        for ref in input_refs:
            if not isinstance(ref, dict):
                continue
            raw_pass_output_id = ref.get("pass_output_id")
            if raw_pass_output_id is None:
                continue
            try:
                pass_output_id = int(raw_pass_output_id)
            except Exception:
                continue
            if pass_output_id > 0:
                return pass_output_id
        return None

    def _latest_idea_pass_outputs() -> list[PassOutput]:
        with Session(repository.engine) as session:
            statement = select(PassOutput).where(
                PassOutput.pass_kind == "trend_ideas",
                cast(Any, PassOutput.status) == "succeeded",
            )
            if granularity is not None:
                statement = statement.where(PassOutput.granularity == granularity)
            statement = statement.order_by(
                desc(cast(Any, PassOutput.created_at)),
                desc(cast(Any, PassOutput.id)),
            )
            rows = list(session.exec(statement))

        selected: list[PassOutput] = []
        seen_windows: set[tuple[str | None, datetime | None, datetime | None]] = set()
        for row in rows:
            key = (row.granularity, row.period_start, row.period_end)
            if key in seen_windows:
                continue
            seen_windows.add(key)
            selected.append(row)
        if not all_history and (period_start is not None or period_end is not None):
            filtered: list[PassOutput] = []
            for row in selected:
                if not _periods_overlap(
                    candidate_start=getattr(row, "period_start", None),
                    candidate_end=getattr(row, "period_end", None),
                    period_start=period_start,
                    period_end=period_end,
                ):
                    continue
                filtered.append(row)
            selected = filtered
        elif not all_history:
            latest_only: list[PassOutput] = []
            latest_by_granularity: set[str | None] = set()
            for row in selected:
                key = str(getattr(row, "granularity", "") or "").strip().lower() or None
                if key in latest_by_granularity:
                    continue
                latest_by_granularity.add(key)
                latest_only.append(row)
            selected = latest_only
        normalized_limit = None if limit is None else max(1, int(limit))
        if normalized_limit is not None:
            selected = selected[:normalized_limit]
        return selected

    def _ensure_idea_document_projection(
        *,
        row: PassOutput,
        payload: TrendIdeasPayload,
    ) -> Document | None:
        period_start = getattr(row, "period_start", None)
        period_end = getattr(row, "period_end", None)
        granularity_value = str(getattr(row, "granularity", "") or "").strip() or "day"
        if not isinstance(period_start, datetime) or not isinstance(period_end, datetime):
            return None
        doc = repository.upsert_document_for_idea(
            granularity=granularity_value,
            period_start=period_start,
            period_end=period_end,
            title=str(payload.title or "").strip() or "Ideas",
        )
        doc_id = int(getattr(doc, "id") or 0)
        if doc_id <= 0:
            return None
        repository.upsert_document_chunk(
            doc_id=doc_id,
            chunk_index=0,
            kind="summary",
            text_value=str(payload.summary_md or "").strip() or "(empty)",
            start_char=0,
            end_char=None,
            source_content_type="trend_ideas_summary",
        )
        next_chunk_index = 1
        for idea in list(payload.ideas or []):
            text_value = _render_idea_document_chunk_text(idea)
            if not text_value:
                continue
            repository.upsert_document_chunk(
                doc_id=doc_id,
                chunk_index=next_chunk_index,
                kind="content",
                text_value=text_value,
                start_char=0,
                end_char=None,
                source_content_type="trend_idea",
            )
            next_chunk_index += 1
        repository.upsert_document_chunk(
            doc_id=doc_id,
            chunk_index=next_chunk_index,
            kind="meta",
            text_value=json.dumps(
                inject_projection_provenance(
                    payload=payload.model_dump(mode="json"),
                    provenance=build_projection_provenance(
                        pass_output_id=int(getattr(row, "id") or 0),
                        pass_kind="trend_ideas",
                        upstream_pass_output_id=_ideas_upstream_pass_output_id(row=row),
                        upstream_pass_kind="trend_synthesis",
                    ),
                ),
                ensure_ascii=False,
                separators=(",", ":"),
            ),
            start_char=0,
            end_char=None,
            source_content_type="trend_ideas_payload_json",
        )
        repository.delete_document_chunks(doc_id=doc_id, chunk_index_gte=next_chunk_index + 1)
        persisted = repository.get_document(doc_id=doc_id)
        return persisted if persisted is not None else doc

    with Session(repository.engine) as session:
        statement = (
            select(Document)
            .where(Document.doc_type == "idea")
            .order_by(
                desc(cast(Any, Document.period_start)),
                desc(cast(Any, Document.id)),
            )
        )
        if granularity is not None:
            statement = statement.where(Document.granularity == granularity)
        documents = list(session.exec(statement))
        if not all_history and (period_start is not None or period_end is not None):
            filtered: list[Document] = []
            for document in documents:
                if not _periods_overlap(
                    candidate_start=getattr(document, "period_start", None),
                    candidate_end=getattr(document, "period_end", None),
                    period_start=period_start,
                    period_end=period_end,
                ):
                    continue
                filtered.append(document)
            documents = filtered
            normalized_limit = None if limit is None else max(1, int(limit))
            if normalized_limit is not None:
                documents = documents[:normalized_limit]
        else:
            documents = _limit_documents_for_backfill(
                documents=documents,
                all_history=all_history,
                limit=limit,
            )

        candidates: list[tuple[Document, dict[str, Any]]] = []
        seen_windows: set[tuple[str | None, datetime | None, datetime | None]] = set()
        for document in documents:
            doc_id = int(getattr(document, "id") or 0)
            if doc_id <= 0:
                continue
            payload = _latest_pass_output_payload(
                repository=repository,
                pass_kind="trend_ideas",
                granularity=str(getattr(document, "granularity", "") or "").strip() or None,
                period_start=getattr(document, "period_start", None),
                period_end=getattr(document, "period_end", None),
                payload_model=TrendIdeasPayload,
            )
            if payload is None:
                meta_chunk = _latest_meta_chunk_for_doc(
                    session,
                    doc_id=doc_id,
                    source_content_type="trend_ideas_payload_json",
                )
                if meta_chunk is None:
                    continue
                try:
                    payload = TrendIdeasPayload.model_validate(
                        json.loads(str(meta_chunk.text or "{}"))
                    ).model_dump(mode="json")
                except Exception:
                    continue
            seen_windows.add(
                (
                    getattr(document, "granularity", None),
                    getattr(document, "period_start", None),
                    getattr(document, "period_end", None),
                )
            )
            candidates.append((document, payload))

        for row in _latest_idea_pass_outputs():
            window_key = (row.granularity, row.period_start, row.period_end)
            if window_key in seen_windows:
                continue
            if limit is not None and len(candidates) >= max(1, int(limit)):
                break
            try:
                payload_model = TrendIdeasPayload.model_validate(
                    json.loads(str(getattr(row, "payload_json", "") or "{}"))
                )
            except Exception:
                continue
            period_start = getattr(row, "period_start", None)
            period_end = getattr(row, "period_end", None)
            granularity_value = str(getattr(row, "granularity", "") or "").strip() or None
            if not isinstance(period_start, datetime) or not isinstance(period_end, datetime):
                continue
            document = session.exec(
                select(Document)
                .where(
                    Document.doc_type == "idea",
                    Document.granularity == granularity_value,
                    Document.period_start == period_start,
                    Document.period_end == period_end,
                )
                .order_by(desc(cast(Any, Document.id)))
            ).first()
            if document is None:
                document = _ensure_idea_document_projection(
                    row=row,
                    payload=payload_model,
                )
            if document is None:
                continue
            payload = payload_model.model_dump(mode="json")
            candidates.append((document, payload))
            seen_windows.add(window_key)
        return candidates


def _incremental_candidates(
    *,
    repository: Any,
    granularity: str | None,
    include: set[str],
    limit: int | None,
    source_language_code: str,
    period_start: datetime | None = None,
    period_end: datetime | None = None,
    all_history: bool = True,
) -> list[TranslationCandidate]:
    candidates: list[TranslationCandidate] = []

    if "items" in include:
        for analysis, item in _load_item_candidates(
            repository=repository,
            limit=limit,
            period_start=period_start,
            period_end=period_end,
            all_history=all_history,
        ):
            analysis_id = int(getattr(analysis, "id") or 0)
            item_id = int(getattr(item, "id") or 0)
            if analysis_id <= 0 or item_id <= 0:
                continue
            payload = _AnalysisTranslationPayload(
                summary=str(getattr(analysis, "summary", "") or "").strip() or "(empty)"
            ).model_dump(mode="json")
            candidates.append(
                TranslationCandidate(
                    source_kind="analysis",
                    source_record_id=analysis_id,
                    payload=payload,
                    payload_model=_AnalysisTranslationPayload,
                    canonical_language_code=source_language_code,
                    item_id=item_id,
                )
            )

    if "trends" in include:
        for document, payload in _load_trend_candidates(
            repository=repository,
            granularity=granularity,
            limit=limit,
            period_start=period_start,
            period_end=period_end,
            all_history=all_history,
        ):
            doc_id = int(getattr(document, "id") or 0)
            if doc_id <= 0:
                continue
            candidates.append(
                TranslationCandidate(
                    source_kind="trend_synthesis",
                    source_record_id=doc_id,
                    payload=payload,
                    payload_model=TrendPayload,
                    canonical_language_code=source_language_code,
                    document_id=doc_id,
                    granularity=str(getattr(document, "granularity", "") or "").strip() or None,
                    period_start=getattr(document, "period_start", None),
                    period_end=getattr(document, "period_end", None),
                )
            )

    if "ideas" in include:
        for document, payload in _load_idea_candidates(
            repository=repository,
            granularity=granularity,
            limit=limit,
            period_start=period_start,
            period_end=period_end,
            all_history=all_history,
        ):
            doc_id = int(getattr(document, "id") or 0)
            if doc_id <= 0:
                continue
            candidates.append(
                TranslationCandidate(
                    source_kind="trend_ideas",
                    source_record_id=doc_id,
                    payload=payload,
                    payload_model=TrendIdeasPayload,
                    canonical_language_code=source_language_code,
                    document_id=doc_id,
                    granularity=str(getattr(document, "granularity", "") or "").strip() or None,
                    period_start=getattr(document, "period_start", None),
                    period_end=getattr(document, "period_end", None),
                )
            )

    return candidates


def _candidate_context(
    *,
    repository: Any,
    settings: Settings,
    candidate: TranslationCandidate,
    context_assist: str,
    run_id: str | None,
) -> dict[str, Any]:
    if context_assist == "none":
        return {}
    note_context = _canonical_note_context(settings=settings, candidate=candidate)
    if candidate.source_kind == "analysis" and candidate.item_id is not None:
        item = repository.get_item(item_id=candidate.item_id)
        if item is None:
            return note_context
        return {
            **note_context,
            **_item_translation_context(
                repository=repository,
                settings=settings,
                run_id=run_id,
                item=item,
                summary_text=str(candidate.payload.get("summary") or "").strip() or None,
                context_assist=context_assist,
            ),
        }
    if candidate.source_kind == "trend_synthesis":
        return {
            **note_context,
            **_trend_translation_context(
                repository=repository,
                settings=settings,
                run_id=run_id,
                payload=candidate.payload,
                granularity=candidate.granularity,
                period_start=candidate.period_start,
                period_end=candidate.period_end,
                context_assist=context_assist,
            ),
        }
    if candidate.source_kind == "trend_ideas":
        return {
            **note_context,
            **_idea_translation_context(
                repository=repository,
                settings=settings,
                run_id=run_id,
                payload=candidate.payload,
                granularity=candidate.granularity,
                period_start=candidate.period_start,
                period_end=candidate.period_end,
                context_assist=context_assist,
            ),
        }
    return note_context


def _canonical_note_path(
    *,
    settings: Settings,
    candidate: TranslationCandidate,
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


def _canonical_note_context(
    *,
    settings: Settings,
    candidate: TranslationCandidate,
) -> dict[str, Any]:
    note_path = _canonical_note_path(settings=settings, candidate=candidate)
    if note_path is None or not note_path.exists() or not note_path.is_file():
        return {}
    sidecar_path = presentation_sidecar_path(note_path=note_path)
    if sidecar_path.exists() and sidecar_path.is_file():
        try:
            payload = json.loads(sidecar_path.read_text(encoding="utf-8"))
        except Exception:
            payload = None
        try:
            schema_version = (
                int(payload.get("presentation_schema_version") or 0)
                if isinstance(payload, dict)
                else 0
            )
        except Exception:
            schema_version = 0
        if isinstance(payload, dict) and schema_version in {
            PRESENTATION_SCHEMA_VERSION_V1,
            PRESENTATION_SCHEMA_VERSION,
        }:
            if validate_presentation(payload):
                payload = None
            else:
                return {
                    "canonical_note": {
                        "path": str(note_path),
                        "sidecar_path": str(sidecar_path),
                    },
                    "presentation": payload,
                }
    try:
        markdown_text = note_path.read_text(encoding="utf-8")
    except Exception:
        return {}
    lines = [line.rstrip() for line in markdown_text.splitlines()]
    title = ""
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            title = stripped[2:].strip()
            break
    body_excerpt = "\n".join(lines[:80]).strip()
    return {
        "canonical_note": {
            "path": str(note_path),
            "title": title or note_path.stem,
            "markdown_excerpt": body_excerpt[:4000],
        }
    }


def _target_language_label(
    *,
    language_code: str,
    localization: LocalizationConfig,
    fallback: str | None,
) -> str:
    if language_code == localization.source_language_code and fallback:
        return str(fallback).strip()
    for target in localization.targets:
        if target.code == language_code:
            return str(target.llm_label).strip()
    return language_code


def _translation_parallelism(task_total: int) -> int:
    if task_total <= 1:
        return 1
    return max(1, min(_DEFAULT_TRANSLATION_PARALLELISM, int(task_total)))


def _prepare_translation_task(
    *,
    repository: Any,
    settings: Settings,
    candidate: TranslationCandidate,
    target: TranslationTarget,
    context_assist: str,
    force: bool,
    run_id: str | None = None,
) -> tuple[str, _PreparedTranslationTask | None]:
    source_hash = _payload_hash(candidate.payload)
    existing = repository.get_localized_output(
        source_kind=candidate.source_kind,
        source_record_id=candidate.source_record_id,
        language_code=target.code,
    )
    if (
        existing is not None
        and str(getattr(existing, "source_hash", "") or "") == source_hash
        and not force
    ):
        return "skipped", None

    context = _candidate_context(
        repository=repository,
        settings=settings,
        candidate=candidate,
        context_assist=context_assist,
        run_id=run_id,
    )
    return (
        "pending",
        _PreparedTranslationTask(
            candidate=candidate,
            target=target,
            source_hash=source_hash,
            context=context,
        ),
    )


def _execute_prepared_translation_task(
    *,
    task: _PreparedTranslationTask,
    llm_model: str,
    source_language_code: str,
    source_language_label: str,
    llm_connection: LLMConnectionConfig,
) -> _CompletedTranslationTask:
    started = time.perf_counter()
    translated_result = translate_structured_payload(
        model=llm_model,
        source_kind=task.candidate.source_kind,
        payload=task.candidate.payload,
        source_language_code=source_language_code,
        target_language_code=task.target.code,
        source_language_label=source_language_label,
        target_language_label=task.target.llm_label,
        context=task.context,
        payload_model=task.candidate.payload_model,
        llm_connection=llm_connection,
        return_debug=True,
    )
    if (
        isinstance(translated_result, tuple)
        and len(translated_result) == 2
        and isinstance(translated_result[0], dict)
        and isinstance(translated_result[1], dict)
    ):
        translated_payload, debug = translated_result
    else:
        translated_payload = cast(dict[str, Any], translated_result)
        debug = {}
    return _CompletedTranslationTask(
        translated_payload=translated_payload,
        debug=debug,
        duration_ms=int((time.perf_counter() - started) * 1000),
    )


def _persist_completed_translation_task(
    *,
    repository: Any,
    task: _PreparedTranslationTask,
    completed: _CompletedTranslationTask,
    context_assist: str,
    source_language_code: str,
    run_id: str | None = None,
) -> None:
    if str(run_id or "").strip():
        _record_translation_llm_metrics(
            repository=repository,
            run_id=str(run_id),
            debug=completed.debug,
            duration_ms=completed.duration_ms,
        )
    repository.upsert_localized_output(
        source_kind=task.candidate.source_kind,
        source_record_id=task.candidate.source_record_id,
        language_code=task.target.code,
        status="succeeded",
        source_hash=task.source_hash,
        payload=completed.translated_payload,
        diagnostics={
            "context_assist": context_assist,
            "source_language_code": source_language_code,
            "target_language_code": task.target.code,
            "translated_at": datetime.now(tz=UTC).isoformat(),
            "context_keys": sorted(task.context.keys()),
            "hybrid_status": task.context.get("hybrid_status"),
            "hybrid_query": task.context.get("hybrid_query"),
        },
        variant_role="translation",
    )


def _translate_candidate_into_language(
    *,
    repository: Any,
    settings: Settings,
    candidate: TranslationCandidate,
    target: TranslationTarget,
    llm_model: str,
    source_language_code: str,
    source_language_label: str,
    context_assist: str,
    llm_connection: LLMConnectionConfig,
    force: bool,
    run_id: str | None = None,
) -> tuple[str, bool]:
    status, prepared = _prepare_translation_task(
        repository=repository,
        settings=settings,
        candidate=candidate,
        target=target,
        context_assist=context_assist,
        force=force,
        run_id=run_id,
    )
    if status == "skipped" or prepared is None:
        return "skipped", False
    completed = _execute_prepared_translation_task(
        task=prepared,
        llm_model=llm_model,
        source_language_code=source_language_code,
        source_language_label=source_language_label,
        llm_connection=llm_connection,
    )
    _persist_completed_translation_task(
        repository=repository,
        task=prepared,
        completed=completed,
        context_assist=context_assist,
        source_language_code=source_language_code,
        run_id=run_id,
    )
    return "translated", True


def _record_translation_llm_metrics(
    *,
    repository: Any,
    run_id: str,
    debug: dict[str, Any] | None,
    duration_ms: int,
) -> None:
    usage = debug.get("usage") if isinstance(debug, dict) else None
    if isinstance(usage, dict):
        requests = usage.get("requests")
        input_tokens = usage.get("input_tokens")
        output_tokens = usage.get("output_tokens")
        if isinstance(requests, (int, float)):
            repository.record_metric(
                run_id=run_id,
                name="pipeline.translate.llm_requests_total",
                value=float(requests),
                unit="count",
            )
        if isinstance(input_tokens, (int, float)):
            repository.record_metric(
                run_id=run_id,
                name="pipeline.translate.llm_input_tokens_total",
                value=float(input_tokens),
                unit="count",
            )
        if isinstance(output_tokens, (int, float)):
            repository.record_metric(
                run_id=run_id,
                name="pipeline.translate.llm_output_tokens_total",
                value=float(output_tokens),
                unit="count",
            )
    cost_usd = debug.get("estimated_cost_usd") if isinstance(debug, dict) else None
    if isinstance(cost_usd, (int, float)):
        repository.record_metric(
            run_id=run_id,
            name="pipeline.translate.estimated_cost_usd",
            value=float(cost_usd),
            unit="usd",
        )
    else:
        repository.record_metric(
            run_id=run_id,
            name="pipeline.translate.cost_missing_total",
            value=1,
            unit="count",
        )
    repository.record_metric(
        run_id=run_id,
        name="pipeline.translate.duration_ms",
        value=float(max(0, int(duration_ms))),
        unit="ms",
    )


def _mirror_candidate_into_language(
    *,
    repository: Any,
    candidate: TranslationCandidate,
    language_code: str,
    force: bool,
) -> tuple[str, bool]:
    source_hash = _payload_hash(candidate.payload)
    existing = repository.get_localized_output(
        source_kind=candidate.source_kind,
        source_record_id=candidate.source_record_id,
        language_code=language_code,
    )
    if (
        existing is not None
        and str(getattr(existing, "source_hash", "") or "") == source_hash
        and not force
    ):
        return "skipped", False
    repository.upsert_localized_output(
        source_kind=candidate.source_kind,
        source_record_id=candidate.source_record_id,
        language_code=language_code,
        status="succeeded",
        source_hash=source_hash,
        payload=candidate.payload,
        diagnostics={
            "mirrored_at": datetime.now(tz=UTC).isoformat(),
        },
        variant_role="mirror",
    )
    return "mirrored", True


def run_translation(
    *,
    repository: Any,
    settings: Settings,
    granularity: str | None = None,
    include: str | list[str] | None = None,
    limit: int | None = None,
    period_start: datetime | None = None,
    period_end: datetime | None = None,
    all_history: bool = True,
    force: bool = False,
    context_assist: str = "direct",
    run_id: str | None = None,
) -> TranslationRunResult:
    localization = settings.localization
    if localization is None or not localization.targets:
        raise ValueError("localization.targets must be configured for translation")

    normalized_granularity = (
        str(granularity or "").strip().lower() or None if granularity is not None else None
    )
    normalized_include = normalize_include(include)
    normalized_context_assist = normalize_context_assist(context_assist)
    llm_model = str(settings.llm_model or "").strip()
    if not llm_model:
        raise ValueError("llm_model must not be empty")
    llm_connection = settings.llm_connection_config()
    source_language_code = str(localization.source_language_code).strip()
    source_language_label = str(settings.llm_output_language or source_language_code).strip()
    targets = [
        TranslationTarget(code=target.code, llm_label=target.llm_label)
        for target in localization.targets
    ]

    result = TranslationRunResult()
    provider_failures = _ProviderFailureTracker()
    candidates = _incremental_candidates(
        repository=repository,
        granularity=normalized_granularity,
        include=normalized_include,
        limit=limit,
        source_language_code=source_language_code,
        period_start=period_start,
        period_end=period_end,
        all_history=all_history,
    )
    log = logger.bind(module="translation.run")
    prepared_tasks: list[_PreparedTranslationTask] = []
    for candidate in candidates:
        for target in targets:
            result.scanned_total += 1
            try:
                status, prepared = _prepare_translation_task(
                    repository=repository,
                    settings=settings,
                    candidate=candidate,
                    target=target,
                    context_assist=normalized_context_assist,
                    force=force,
                    run_id=run_id,
                )
            except Exception as exc:  # noqa: BLE001
                result.failed_total += 1
                log.bind(
                    source_kind=candidate.source_kind,
                    source_record_id=candidate.source_record_id,
                    target_language_code=target.code,
                ).warning(
                    "translation failed error_type={} error={}",
                    type(exc).__name__,
                    str(exc),
                )
                abort_reason = provider_failures.record(exc)
                if abort_reason is not None:
                    result.aborted = True
                    result.abort_reason = abort_reason
                    log.warning(abort_reason)
                    return result
                continue
            if status == "skipped":
                result.skipped_total += 1
                provider_failures.reset()
                continue
            if prepared is not None:
                prepared_tasks.append(prepared)

    parallelism = _translation_parallelism(len(prepared_tasks))
    if parallelism <= 1:
        for task in prepared_tasks:
            try:
                completed = _execute_prepared_translation_task(
                    task=task,
                    llm_model=llm_model,
                    source_language_code=source_language_code,
                    source_language_label=source_language_label,
                    llm_connection=llm_connection,
                )
            except Exception as exc:  # noqa: BLE001
                result.failed_total += 1
                log.bind(
                    source_kind=task.candidate.source_kind,
                    source_record_id=task.candidate.source_record_id,
                    target_language_code=task.target.code,
                ).warning(
                    "translation failed error_type={} error={}",
                    type(exc).__name__,
                    str(exc),
                )
                abort_reason = provider_failures.record(exc)
                if abort_reason is not None:
                    result.aborted = True
                    result.abort_reason = abort_reason
                    log.warning(abort_reason)
                    return result
                continue
            provider_failures.reset()
            _persist_completed_translation_task(
                repository=repository,
                task=task,
                completed=completed,
                context_assist=normalized_context_assist,
                source_language_code=source_language_code,
                run_id=run_id,
            )
            result.translated_total += 1
        return result

    with ThreadPoolExecutor(max_workers=parallelism) as executor:
        in_flight: list[tuple[_PreparedTranslationTask, Any]] = []
        next_task_index = 0

        while next_task_index < len(prepared_tasks) and len(in_flight) < parallelism:
            task = prepared_tasks[next_task_index]
            next_task_index += 1
            future = executor.submit(
                _execute_prepared_translation_task,
                task=task,
                llm_model=llm_model,
                source_language_code=source_language_code,
                source_language_label=source_language_label,
                llm_connection=llm_connection,
            )
            in_flight.append((task, future))

        while in_flight:
            task, future = in_flight.pop(0)
            try:
                completed = future.result()
            except Exception as exc:  # noqa: BLE001
                result.failed_total += 1
                log.bind(
                    source_kind=task.candidate.source_kind,
                    source_record_id=task.candidate.source_record_id,
                    target_language_code=task.target.code,
                ).warning(
                    "translation failed error_type={} error={}",
                    type(exc).__name__,
                    str(exc),
                )
                abort_reason = provider_failures.record(exc)
                if abort_reason is not None:
                    result.aborted = True
                    result.abort_reason = abort_reason
                    log.warning(abort_reason)
                    return result
            else:
                provider_failures.reset()
                _persist_completed_translation_task(
                    repository=repository,
                    task=task,
                    completed=completed,
                    context_assist=normalized_context_assist,
                    source_language_code=source_language_code,
                    run_id=run_id,
                )
                result.translated_total += 1

            if next_task_index < len(prepared_tasks):
                next_task = prepared_tasks[next_task_index]
                next_task_index += 1
                next_future = executor.submit(
                    _execute_prepared_translation_task,
                    task=next_task,
                    llm_model=llm_model,
                    source_language_code=source_language_code,
                    source_language_label=source_language_label,
                    llm_connection=llm_connection,
                )
                in_flight.append((next_task, next_future))
    return result


def run_translation_backfill(
    *,
    repository: Any,
    settings: Settings,
    granularity: str | None = None,
    include: str | list[str] | None = None,
    limit: int | None = None,
    force: bool = False,
    context_assist: str = "direct",
    legacy_source_language: str | None = None,
    emit_mirror_targets: bool = False,
    all_history: bool = False,  # noqa: ARG001
    run_id: str | None = None,
) -> TranslationRunResult:
    localization = settings.localization
    if localization is None:
        raise ValueError("localization must be configured for translation backfill")

    normalized_granularity = (
        str(granularity or "").strip().lower() or None if granularity is not None else None
    )
    normalized_include = normalize_include(include)
    normalized_context_assist = normalize_context_assist(context_assist)
    llm_model = str(settings.llm_model or "").strip()
    if not llm_model:
        raise ValueError("llm_model must not be empty")
    llm_connection = settings.llm_connection_config()

    source_language_code = (
        str(
            legacy_source_language or localization.legacy_backfill_source_language_code or ""
        ).strip()
    )
    if not source_language_code:
        raise ValueError(
            "legacy_source_language or localization.legacy_backfill_source_language_code is required for translation backfill"
        )
    target_language_code = str(localization.source_language_code).strip()
    target_language_label = _target_language_label(
        language_code=target_language_code,
        localization=localization,
        fallback=settings.llm_output_language,
    )
    source_language_label = _target_language_label(
        language_code=source_language_code,
        localization=localization,
        fallback=None,
    )

    result = TranslationRunResult()
    provider_failures = _ProviderFailureTracker()
    candidates = _incremental_candidates(
        repository=repository,
        granularity=normalized_granularity,
        include=normalized_include,
        limit=limit,
        source_language_code=source_language_code,
        all_history=all_history,
    )
    log = logger.bind(module="translation.backfill")

    translation_target = TranslationTarget(
        code=target_language_code,
        llm_label=target_language_label,
    )

    for candidate in candidates:
        result.scanned_total += 1
        try:
            status, changed = _translate_candidate_into_language(
                repository=repository,
                settings=settings,
                candidate=candidate,
                target=translation_target,
                llm_model=llm_model,
                source_language_code=source_language_code,
                source_language_label=source_language_label,
                context_assist=normalized_context_assist,
                llm_connection=llm_connection,
                force=force,
                run_id=run_id,
            )
        except Exception as exc:  # noqa: BLE001
            result.failed_total += 1
            log.bind(
                source_kind=candidate.source_kind,
                source_record_id=candidate.source_record_id,
                target_language_code=translation_target.code,
            ).warning(
                "backfill translation failed error_type={} error={}",
                type(exc).__name__,
                str(exc),
            )
            abort_reason = provider_failures.record(exc)
            if abort_reason is not None:
                result.aborted = True
                result.abort_reason = abort_reason
                log.warning(abort_reason)
                return result
            continue
        provider_failures.reset()
        if status == "skipped":
            result.skipped_total += 1
        elif changed:
            result.translated_total += 1

        if not emit_mirror_targets:
            continue
        mirror_language_codes = {
            target.code
            for target in localization.targets
            if target.code == source_language_code
        }
        for mirror_language_code in sorted(mirror_language_codes):
            try:
                mirror_status, mirror_changed = _mirror_candidate_into_language(
                    repository=repository,
                    candidate=candidate,
                    language_code=mirror_language_code,
                    force=force,
                )
            except Exception as exc:  # noqa: BLE001
                result.failed_total += 1
                log.bind(
                    source_kind=candidate.source_kind,
                    source_record_id=candidate.source_record_id,
                    mirror_language_code=mirror_language_code,
                ).warning(
                    "backfill mirror failed error_type={} error={}",
                    type(exc).__name__,
                    str(exc),
                )
                continue
            if mirror_status == "skipped":
                result.skipped_total += 1
            elif mirror_changed:
                result.mirrored_total += 1
    return result


def materialize_localized_languages(
    *,
    repository: Any,
    localization: LocalizationConfig,
) -> list[str]:
    _ = repository
    languages = [target.code for target in localization.targets]
    ordered = []
    seen: set[str] = set()
    for language in languages:
        if language in seen:
            continue
        seen.add(language)
        ordered.append(language)
    return ordered


def localized_language_root(*, output_dir: Path, language_code: str) -> Path:
    return output_dir / "Localized" / language_slug(language_code)
