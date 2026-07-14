from __future__ import annotations

from dataclasses import dataclass
import json
from datetime import UTC, datetime
from typing import Any, cast

from pydantic import BaseModel
from sqlalchemy import desc, func
from sqlmodel import Session, select

from recoleta.idea_projection import (
    IdeaProjectionRequest,
    persist_idea_document_projection,
)
from recoleta.models import Analysis, Document, DocumentChunk, Item, PassOutput
from recoleta.pass_output_selection import (
    CANONICAL_PASS_OUTPUT_STATUSES,
    is_suppressed_pass_output,
    latest_canonical_pass_outputs_by_window,
    latest_idea_pass_output_states_by_window,
    pass_output_window_key,
)
from recoleta.passes.trend_ideas import TrendIdeasPayload
from recoleta.trends import TrendPayload

type WindowKey = tuple[str | None, datetime | None, datetime | None]


@dataclass(frozen=True, slots=True)
class CandidateWindowRequest:
    repository: Any
    granularity: str | None
    limit: int | None
    period_start: datetime | None = None
    period_end: datetime | None = None
    all_history: bool = True
    materialize_missing_idea_projections: bool = True


@dataclass(frozen=True, slots=True)
class DocumentPayloadSpec:
    pass_kind: str
    payload_model: type[BaseModel]
    meta_source_content_type: str


@dataclass(frozen=True, slots=True)
class IncrementalCandidatesRequest:
    repository: Any
    granularity: str | None
    include: set[str]
    limit: int | None
    source_language_code: str
    candidate_factory: Any
    analysis_payload_model: type[BaseModel]
    period_start: datetime | None = None
    period_end: datetime | None = None
    all_history: bool = True
    materialize_missing_idea_projections: bool = True


def normalize_utc_datetime(value: datetime | None) -> datetime | None:
    if not isinstance(value, datetime):
        return None
    if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def periods_overlap(
    *,
    candidate_start: datetime | None,
    candidate_end: datetime | None,
    period_start: datetime | None,
    period_end: datetime | None,
) -> bool:
    normalized_candidate_start = normalize_utc_datetime(candidate_start)
    normalized_candidate_end = normalize_utc_datetime(candidate_end)
    normalized_period_start = normalize_utc_datetime(period_start)
    normalized_period_end = normalize_utc_datetime(period_end)
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


def latest_meta_chunk_for_doc(
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


def load_item_candidates(
    request: CandidateWindowRequest,
) -> list[tuple[Analysis, Item]]:
    normalized_limit = _normalized_limit(request.limit)
    with Session(request.repository.engine) as session:
        event_at = func.coalesce(
            cast(Any, Item.published_at), cast(Any, Item.created_at)
        )
        statement = (
            select(Analysis, Item)
            .join(Item, cast(Any, Analysis.item_id) == cast(Any, Item.id))
            .order_by(desc(cast(Any, Analysis.id)))
        )
        if not request.all_history:
            if request.period_start is not None:
                statement = statement.where(event_at >= request.period_start)
            if request.period_end is not None:
                statement = statement.where(event_at < request.period_end)
        if normalized_limit is not None:
            statement = statement.limit(normalized_limit)
        return list(session.exec(statement))


def _canonical_pass_output_payload(
    *, row: Any, payload_model: type[BaseModel]
) -> dict[str, Any] | None:
    if is_suppressed_pass_output(row):
        return None
    try:
        return payload_model.model_validate(
            json.loads(str(getattr(row, "payload_json", "") or "{}"))
        ).model_dump(mode="json")
    except Exception:
        return None


def limit_documents_for_backfill(
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
            key = _normalized_granularity(getattr(document, "granularity", None))
            if key in latest_by_granularity:
                continue
            latest_by_granularity.add(key)
            selected.append(document)
    normalized_limit = _normalized_limit(limit)
    return selected if normalized_limit is None else selected[:normalized_limit]


def load_trend_candidates(
    request: CandidateWindowRequest,
) -> list[tuple[Document, dict[str, Any]]]:
    with Session(request.repository.engine) as session:
        documents = _load_candidate_documents(
            session=session,
            doc_type="trend",
            request=request,
        )
        candidates = _document_candidates(
            session=session,
            repository=request.repository,
            documents=documents,
            spec=DocumentPayloadSpec(
                pass_kind="trend_synthesis",
                payload_model=TrendPayload,
                meta_source_content_type="trend_payload_json",
            ),
        )
    normalized_limit = _normalized_limit(request.limit)
    return candidates if normalized_limit is None else candidates[:normalized_limit]


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


def _latest_idea_pass_outputs(request: CandidateWindowRequest) -> list[PassOutput]:
    rows = _idea_pass_output_rows(request)
    unique_rows = _unique_windowed_rows(rows)
    filtered_rows = _filtered_pass_output_rows(unique_rows, request)
    states_by_window = latest_idea_pass_output_states_by_window(
        repository=request.repository,
        windows=(pass_output_window_key(row) for row in filtered_rows),
    )
    return [
        row
        for row in filtered_rows
        if (state := states_by_window.get(pass_output_window_key(row))) is not None
        and state.active
    ]


def _ensure_idea_document_projection(
    *,
    repository: Any,
    row: PassOutput,
    payload: TrendIdeasPayload,
) -> Document | None:
    period_start = getattr(row, "period_start", None)
    period_end = getattr(row, "period_end", None)
    granularity_value = str(getattr(row, "granularity", "") or "").strip() or "day"
    normalized_granularity = _normalized_granularity(granularity_value) or "day"
    if not isinstance(period_start, datetime) or not isinstance(period_end, datetime):
        return None
    persist_idea_document_projection(
        IdeaProjectionRequest(
            repository=repository,
            pass_output_id=int(getattr(row, "id") or 0),
            upstream_pass_output_id=_ideas_upstream_pass_output_id(row=row),
            granularity=normalized_granularity,
            period_start=period_start,
            period_end=period_end,
            payload=payload,
        )
    )
    with Session(repository.engine) as session:
        return session.exec(
            select(Document)
            .where(
                Document.doc_type == "idea",
                Document.granularity == normalized_granularity,
                Document.period_start == period_start,
                Document.period_end == period_end,
            )
            .order_by(desc(cast(Any, Document.id)))
        ).first()


def load_idea_candidates(
    request: CandidateWindowRequest,
) -> list[tuple[Document, dict[str, Any]]]:
    with Session(request.repository.engine) as session:
        documents = _load_candidate_documents(
            session=session,
            doc_type="idea",
            request=request,
        )
        candidates, seen_windows = _existing_idea_candidates(
            session=session,
            repository=request.repository,
            documents=documents,
        )
    return _ranked_idea_candidates(
        candidates=candidates,
        seen_windows=seen_windows,
        request=request,
    )


def incremental_candidates(
    request: IncrementalCandidatesRequest,
) -> list[Any]:
    candidates: list[Any] = []
    if "items" in request.include:
        candidates.extend(_item_translation_candidates(request))
    if "trends" in request.include:
        candidates.extend(_trend_translation_candidates(request))
    if "ideas" in request.include:
        candidates.extend(_idea_translation_candidates(request))
    return candidates


def _normalized_limit(limit: int | None) -> int | None:
    return None if limit is None else max(1, int(limit))


def _normalized_granularity(value: Any) -> str | None:
    return str(value or "").strip().lower() or None


def _window_key(record: Any) -> WindowKey:
    return (
        _normalized_granularity(getattr(record, "granularity", None)),
        getattr(record, "period_start", None),
        getattr(record, "period_end", None),
    )


def _window_request(request: IncrementalCandidatesRequest) -> CandidateWindowRequest:
    return CandidateWindowRequest(
        repository=request.repository,
        granularity=request.granularity,
        limit=request.limit,
        period_start=request.period_start,
        period_end=request.period_end,
        all_history=request.all_history,
        materialize_missing_idea_projections=(
            request.materialize_missing_idea_projections
        ),
    )


def _load_candidate_documents(
    *,
    session: Session,
    doc_type: str,
    request: CandidateWindowRequest,
) -> list[Document]:
    statement = (
        select(Document)
        .where(Document.doc_type == doc_type)
        .order_by(
            desc(cast(Any, Document.period_start)),
            desc(cast(Any, Document.id)),
        )
    )
    if request.granularity is not None:
        statement = statement.where(Document.granularity == request.granularity)
    documents = list(session.exec(statement))
    if not request.all_history and (
        request.period_start is not None or request.period_end is not None
    ):
        return _window_filtered_documents(documents, request)
    return limit_documents_for_backfill(
        documents=documents,
        all_history=request.all_history,
        limit=None,
    )


def _window_filtered_documents(
    documents: list[Document],
    request: CandidateWindowRequest,
) -> list[Document]:
    selected = [
        document
        for document in documents
        if periods_overlap(
            candidate_start=getattr(document, "period_start", None),
            candidate_end=getattr(document, "period_end", None),
            period_start=request.period_start,
            period_end=request.period_end,
        )
    ]
    return selected


def _document_candidates(
    *,
    session: Session,
    repository: Any,
    documents: list[Document],
    spec: DocumentPayloadSpec,
) -> list[tuple[Document, dict[str, Any]]]:
    candidates: list[tuple[Document, dict[str, Any]]] = []
    canonical_by_window = latest_canonical_pass_outputs_by_window(
        repository=repository,
        pass_kind=spec.pass_kind,
        windows=(pass_output_window_key(document) for document in documents),
    )
    for document in documents:
        payload = _payload_for_document(
            session=session,
            document=document,
            spec=spec,
            canonical_row=canonical_by_window.get(pass_output_window_key(document)),
        )
        if payload is not None:
            candidates.append((document, payload))
    return candidates


def _payload_for_document(
    *,
    session: Session,
    document: Document,
    spec: DocumentPayloadSpec,
    canonical_row: Any | None,
) -> dict[str, Any] | None:
    doc_id = int(getattr(document, "id") or 0)
    if doc_id <= 0:
        return None
    if canonical_row is not None:
        return _canonical_pass_output_payload(
            row=canonical_row,
            payload_model=spec.payload_model,
        )
    return _meta_chunk_payload(
        session=session,
        doc_id=doc_id,
        payload_model=spec.payload_model,
        source_content_type=spec.meta_source_content_type,
    )


def _meta_chunk_payload(
    *,
    session: Session,
    doc_id: int,
    payload_model: type[BaseModel],
    source_content_type: str,
) -> dict[str, Any] | None:
    meta_chunk = latest_meta_chunk_for_doc(
        session,
        doc_id=doc_id,
        source_content_type=source_content_type,
    )
    if meta_chunk is None:
        return None
    try:
        return payload_model.model_validate(
            json.loads(str(meta_chunk.text or "{}"))
        ).model_dump(mode="json")
    except Exception:
        return None


def _idea_pass_output_rows(request: CandidateWindowRequest) -> list[PassOutput]:
    with Session(request.repository.engine) as session:
        statement = select(PassOutput).where(
            PassOutput.pass_kind == "trend_ideas",
            cast(Any, PassOutput.status).in_(CANONICAL_PASS_OUTPUT_STATUSES),
        )
        if request.granularity is not None:
            statement = statement.where(PassOutput.granularity == request.granularity)
        statement = statement.order_by(
            desc(cast(Any, PassOutput.created_at)),
            desc(cast(Any, PassOutput.id)),
        )
        return list(session.exec(statement))


def _unique_windowed_rows(rows: list[PassOutput]) -> list[PassOutput]:
    selected: list[PassOutput] = []
    seen_windows: set[WindowKey] = set()
    for row in rows:
        key = _window_key(row)
        if key in seen_windows:
            continue
        seen_windows.add(key)
        selected.append(row)
    return selected


def _filtered_pass_output_rows(
    rows: list[PassOutput],
    request: CandidateWindowRequest,
) -> list[PassOutput]:
    if request.all_history:
        return rows
    if request.period_start is not None or request.period_end is not None:
        return [
            row
            for row in rows
            if periods_overlap(
                candidate_start=getattr(row, "period_start", None),
                candidate_end=getattr(row, "period_end", None),
                period_start=request.period_start,
                period_end=request.period_end,
            )
        ]
    return _latest_rows_by_granularity(rows)


def _latest_rows_by_granularity(rows: list[PassOutput]) -> list[PassOutput]:
    latest_only: list[PassOutput] = []
    seen_granularities: set[str | None] = set()
    for row in rows:
        key = _normalized_granularity(getattr(row, "granularity", None))
        if key in seen_granularities:
            continue
        seen_granularities.add(key)
        latest_only.append(row)
    return latest_only


def _existing_idea_candidates(
    *,
    session: Session,
    repository: Any,
    documents: list[Document],
) -> tuple[list[tuple[Document, dict[str, Any]]], set[WindowKey]]:
    states_by_window = latest_idea_pass_output_states_by_window(
        repository=repository,
        windows=(pass_output_window_key(document) for document in documents),
    )
    candidates: list[tuple[Document, dict[str, Any]]] = []
    for document in documents:
        state = states_by_window.get(pass_output_window_key(document))
        payload = _idea_document_payload(
            session=session,
            document=document,
            state=state,
        )
        if payload is not None:
            candidates.append((document, payload))
    return candidates, {_window_key(document) for document, _payload in candidates}


def _idea_document_payload(
    *, session: Session, document: Document, state: Any | None
) -> dict[str, Any] | None:
    if state is not None:
        if not state.active:
            return None
        return _canonical_pass_output_payload(
            row=state.row,
            payload_model=TrendIdeasPayload,
        )
    return _meta_chunk_payload(
        session=session,
        doc_id=int(getattr(document, "id") or 0),
        payload_model=TrendIdeasPayload,
        source_content_type="trend_ideas_payload_json",
    )


def _ranked_idea_candidates(
    *,
    candidates: list[tuple[Document, dict[str, Any]]],
    seen_windows: set[WindowKey],
    request: CandidateWindowRequest,
) -> list[tuple[Document, dict[str, Any]]]:
    ranked: list[tuple[tuple[float, int], str, Any]] = [
        (_document_candidate_recency_key(candidate), "existing", candidate)
        for candidate in candidates
    ]
    if request.materialize_missing_idea_projections:
        ranked.extend(
            (
                _pass_output_recency_key(row),
                "backfill",
                row,
            )
            for row in _latest_idea_pass_outputs(request)
            if _window_key(row) not in seen_windows
        )
    ranked.sort(key=lambda entry: entry[0], reverse=True)
    normalized_limit = _normalized_limit(request.limit)
    selected: list[tuple[Document, dict[str, Any]]] = []
    for _recency, kind, value in ranked:
        candidate = (
            value
            if kind == "existing"
            else _backfilled_idea_candidate(
                repository=request.repository,
                row=value,
            )
        )
        if candidate is None:
            continue
        selected.append(candidate)
        if normalized_limit is not None and len(selected) >= normalized_limit:
            break
    return selected


def _document_candidate_recency_key(
    candidate: tuple[Document, dict[str, Any]],
) -> tuple[float, int]:
    document, _payload = candidate
    period_start = normalize_utc_datetime(getattr(document, "period_start", None))
    return (
        period_start.timestamp() if period_start is not None else 0.0,
        int(getattr(document, "id", 0) or 0),
    )


def _pass_output_recency_key(row: PassOutput) -> tuple[float, int]:
    period_start = normalize_utc_datetime(getattr(row, "period_start", None))
    return (
        period_start.timestamp() if period_start is not None else 0.0,
        int(getattr(row, "id", 0) or 0),
    )


def _backfilled_idea_candidate(
    *,
    repository: Any,
    row: PassOutput,
) -> tuple[Document, dict[str, Any]] | None:
    if is_suppressed_pass_output(row):
        return None
    try:
        payload_model = TrendIdeasPayload.model_validate(
            json.loads(str(getattr(row, "payload_json", "") or "{}"))
        )
    except Exception:
        return None
    document = _ensure_idea_document_projection(
        repository=repository,
        row=row,
        payload=payload_model,
    )
    if document is None:
        return None
    return document, payload_model.model_dump(mode="json")


def _item_translation_candidates(request: IncrementalCandidatesRequest) -> list[Any]:
    candidates: list[Any] = []
    for analysis, item in load_item_candidates(_window_request(request)):
        analysis_id = int(getattr(analysis, "id") or 0)
        item_id = int(getattr(item, "id") or 0)
        if analysis_id <= 0 or item_id <= 0:
            continue
        payload = request.analysis_payload_model(
            summary=str(getattr(analysis, "summary", "") or "").strip() or "(empty)"
        ).model_dump(mode="json")
        candidates.append(
            request.candidate_factory(
                source_kind="analysis",
                source_record_id=analysis_id,
                payload=payload,
                payload_model=request.analysis_payload_model,
                canonical_language_code=request.source_language_code,
                item_id=item_id,
            )
        )
    return candidates


def _trend_translation_candidates(request: IncrementalCandidatesRequest) -> list[Any]:
    candidates: list[Any] = []
    for document, payload in load_trend_candidates(_window_request(request)):
        doc_id = int(getattr(document, "id") or 0)
        if doc_id <= 0:
            continue
        candidates.append(
            request.candidate_factory(
                source_kind="trend_synthesis",
                source_record_id=doc_id,
                payload=payload,
                payload_model=TrendPayload,
                canonical_language_code=request.source_language_code,
                document_id=doc_id,
                granularity=_normalized_granularity(
                    getattr(document, "granularity", None)
                ),
                period_start=getattr(document, "period_start", None),
                period_end=getattr(document, "period_end", None),
            )
        )
    return candidates


def _idea_translation_candidates(request: IncrementalCandidatesRequest) -> list[Any]:
    candidates: list[Any] = []
    for document, payload in load_idea_candidates(_window_request(request)):
        doc_id = int(getattr(document, "id") or 0)
        if doc_id <= 0:
            continue
        candidates.append(
            request.candidate_factory(
                source_kind="trend_ideas",
                source_record_id=doc_id,
                payload=payload,
                payload_model=TrendIdeasPayload,
                canonical_language_code=request.source_language_code,
                document_id=doc_id,
                granularity=_normalized_granularity(
                    getattr(document, "granularity", None)
                ),
                period_start=getattr(document, "period_start", None),
                period_end=getattr(document, "period_end", None),
            )
        )
    return candidates
