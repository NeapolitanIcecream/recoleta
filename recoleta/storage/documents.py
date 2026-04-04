from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, cast

from sqlalchemy import desc, text
from sqlmodel import Session, select

from recoleta.models import ChunkEmbedding, Document, DocumentChunk, Item
from recoleta.storage.document_query_helpers import (
    ChunkSearchRequest,
    ChunkUpsertRequest,
    build_chunk_search,
    build_document_list_statement,
    build_summary_chunk_statement,
    collect_chunk_ids,
    decode_search_hit_row,
    delete_chunk_side_tables,
    load_chunks_for_delete,
    normalize_chunk_delete,
    normalize_chunk_upsert,
    normalize_doc_type,
    normalize_limit_offset,
    summary_chunk_index_row,
)
from recoleta.storage_common import _to_json
from recoleta.types import utc_now


@dataclass(frozen=True, slots=True)
class ItemDocumentUpsertRequest:
    item: Item


@dataclass(frozen=True, slots=True)
class PeriodDocumentUpsertRequest:
    doc_type: str
    granularity: str
    period_start: datetime
    period_end: datetime
    title: str


@dataclass(frozen=True, slots=True)
class ChunkFtsSyncRequest:
    chunk_id: int
    doc_id: int
    chunk_index: int
    kind: str
    text_value: str


@dataclass(frozen=True, slots=True)
class DocumentListRequest:
    doc_type: str
    period_start: datetime
    period_end: datetime
    granularity: str | None = None
    order_by: str = "event_desc"
    offset: int = 0
    limit: int = 50


@dataclass(frozen=True, slots=True)
class SummaryChunkListRequest:
    doc_type: str
    period_start: datetime
    period_end: datetime
    limit: int = 500
    offset: int = 0


@dataclass(frozen=True, slots=True)
class SummaryChunkIndexListRequest:
    doc_type: str
    period_start: datetime
    period_end: datetime
    granularity: str | None = None
    limit: int = 500
    offset: int = 0


@dataclass(frozen=True, slots=True)
class ChunkEmbeddingUpsertRequest:
    chunk_id: int
    model: str
    dimensions: int | None
    text_hash: str
    vector: list[float]


@dataclass(frozen=True, slots=True)
class _NormalizedChunkEmbeddingValues:
    chunk_id: int
    model: str
    dimensions: int | None
    text_hash: str
    vector_json: str


def _load_existing_document_chunk(
    session: Session,
    *,
    doc_id: int,
    chunk_index: int,
) -> DocumentChunk | None:
    statement = select(DocumentChunk).where(
        DocumentChunk.doc_id == doc_id,
        DocumentChunk.chunk_index == chunk_index,
    )
    return session.exec(statement).first()


def _build_document_chunk(*, spec: Any) -> DocumentChunk:
    return DocumentChunk(
        doc_id=spec.doc_id,
        chunk_index=spec.chunk_index,
        kind=spec.kind,
        text=spec.text,
        start_char=spec.start_char,
        end_char=spec.end_char,
        text_hash=spec.text_hash,
        source_content_type=spec.source_content_type,
    )


def _update_document_chunk(*, existing: DocumentChunk, spec: Any) -> DocumentChunk:
    existing.kind = spec.kind
    existing.text = spec.text
    existing.start_char = spec.start_char
    existing.end_char = spec.end_char
    existing.text_hash = spec.text_hash
    existing.source_content_type = spec.source_content_type
    return existing


def _persist_new_document_chunk(
    *,
    store: Any,
    session: Session,
    spec: Any,
) -> tuple[DocumentChunk, bool]:
    chunk = _build_document_chunk(spec=spec)
    session.add(chunk)
    store._commit(session)
    session.refresh(chunk)
    return chunk, True


def _persist_existing_document_chunk(
    *,
    store: Any,
    session: Session,
    existing: DocumentChunk,
    spec: Any,
) -> tuple[DocumentChunk, bool, bool]:
    if str(getattr(existing, "text_hash", "") or "") == spec.text_hash:
        return existing, False, False
    chunk = _update_document_chunk(existing=existing, spec=spec)
    session.add(chunk)
    store._commit(session)
    session.refresh(chunk)
    return chunk, False, True


def _stored_document_chunk(
    *,
    store: Any,
    session: Session,
    existing: DocumentChunk | None,
    spec: Any,
) -> tuple[DocumentChunk, bool, bool]:
    if existing is None:
        chunk, inserted = _persist_new_document_chunk(
            store=store,
            session=session,
            spec=spec,
        )
        return chunk, inserted, True
    return _persist_existing_document_chunk(
        store=store,
        session=session,
        existing=existing,
        spec=spec,
    )


def _sync_document_chunk_fts(
    *,
    store: Any,
    chunk: DocumentChunk,
    spec: Any,
) -> None:
    chunk_id = getattr(chunk, "id", None)
    if chunk_id is None:
        return
    store._sync_chunk_fts(
        request=ChunkFtsSyncRequest(
            chunk_id=int(chunk_id),
            doc_id=spec.doc_id,
            chunk_index=spec.chunk_index,
            kind=spec.kind,
            text_value=spec.text,
        )
    )


def _item_document_values(*, item: Item, event_at: datetime | None) -> dict[str, Any]:
    return {
        "source": str(getattr(item, "source", "") or "").strip() or None,
        "canonical_url": str(getattr(item, "canonical_url", "") or "").strip() or None,
        "title": str(getattr(item, "title", "") or "").strip() or None,
        "published_at": event_at,
    }


def _stored_item_document(
    *,
    session: Session,
    item_id: int,
    values: dict[str, Any],
) -> Document:
    existing = session.exec(
        select(Document).where(
            Document.doc_type == "item",
            Document.item_id == item_id,
        )
    ).first()
    if existing is None:
        return Document(doc_type="item", item_id=item_id, **values)
    existing.source = values["source"]
    existing.canonical_url = values["canonical_url"]
    existing.title = values["title"]
    existing.published_at = values["published_at"]
    existing.updated_at = utc_now()
    return existing


def _normalized_embedding_values(
    request: ChunkEmbeddingUpsertRequest,
) -> _NormalizedChunkEmbeddingValues:
    normalized_chunk_id = int(request.chunk_id)
    normalized_model = str(request.model or "").strip()
    normalized_text_hash = str(request.text_hash or "").strip()
    if normalized_chunk_id <= 0:
        raise ValueError("chunk_id must be > 0")
    if not normalized_model:
        raise ValueError("model must not be empty")
    if not normalized_text_hash:
        raise ValueError("text_hash must not be empty")
    if not isinstance(request.vector, list) or not request.vector:
        raise ValueError("vector must be a non-empty list")
    normalized_dims = int(request.dimensions) if request.dimensions is not None else None
    if normalized_dims is not None and normalized_dims <= 0:
        raise ValueError("dimensions must be positive")
    normalized_vector = [float(value) for value in request.vector]
    return _NormalizedChunkEmbeddingValues(
        chunk_id=normalized_chunk_id,
        model=normalized_model,
        dimensions=normalized_dims,
        text_hash=normalized_text_hash,
        vector_json=_to_json(normalized_vector),
    )


def _existing_chunk_embedding(
    *,
    session: Session,
    chunk_id: int,
    model: str,
) -> ChunkEmbedding | None:
    return session.exec(
        select(ChunkEmbedding).where(
            ChunkEmbedding.chunk_id == chunk_id,
            ChunkEmbedding.model == model,
        )
    ).first()


def _stored_chunk_embedding(
    *,
    existing: ChunkEmbedding | None,
    values: _NormalizedChunkEmbeddingValues,
) -> ChunkEmbedding:
    if existing is None:
        return ChunkEmbedding(
            chunk_id=values.chunk_id,
            model=values.model,
            dimensions=values.dimensions,
            vector_json=values.vector_json,
            text_hash=values.text_hash,
        )
    if (
        str(getattr(existing, "text_hash", "") or "") == values.text_hash
        and str(getattr(existing, "vector_json", "") or "") == values.vector_json
    ):
        return existing
    existing.dimensions = values.dimensions
    existing.vector_json = values.vector_json
    existing.text_hash = values.text_hash
    return existing


def coerce_item_document_request(
    *,
    request: ItemDocumentUpsertRequest | None = None,
    legacy_kwargs: dict[str, Any],
) -> ItemDocumentUpsertRequest:
    if request is not None:
        return request
    return ItemDocumentUpsertRequest(item=legacy_kwargs["item"])


def coerce_period_document_request(
    *,
    request: PeriodDocumentUpsertRequest | None = None,
    legacy_kwargs: dict[str, Any],
) -> PeriodDocumentUpsertRequest:
    if request is not None:
        return request
    return PeriodDocumentUpsertRequest(
        doc_type=legacy_kwargs["doc_type"],
        granularity=legacy_kwargs["granularity"],
        period_start=legacy_kwargs["period_start"],
        period_end=legacy_kwargs["period_end"],
        title=legacy_kwargs["title"],
    )


def coerce_document_chunk_request(
    *,
    request: ChunkUpsertRequest | None = None,
    legacy_kwargs: dict[str, Any],
) -> ChunkUpsertRequest:
    if request is not None:
        return request
    return ChunkUpsertRequest(
        doc_id=legacy_kwargs["doc_id"],
        chunk_index=legacy_kwargs["chunk_index"],
        kind=legacy_kwargs["kind"],
        text_value=legacy_kwargs["text_value"],
        start_char=legacy_kwargs.get("start_char"),
        end_char=legacy_kwargs.get("end_char"),
        source_content_type=legacy_kwargs.get("source_content_type"),
    )


def coerce_chunk_fts_sync_request(
    *,
    request: ChunkFtsSyncRequest | None = None,
    legacy_kwargs: dict[str, Any],
) -> ChunkFtsSyncRequest:
    if request is not None:
        return request
    return ChunkFtsSyncRequest(
        chunk_id=legacy_kwargs["chunk_id"],
        doc_id=legacy_kwargs["doc_id"],
        chunk_index=legacy_kwargs["chunk_index"],
        kind=legacy_kwargs["kind"],
        text_value=legacy_kwargs["text_value"],
    )


def coerce_document_list_request(
    *,
    request: DocumentListRequest | None = None,
    legacy_kwargs: dict[str, Any],
) -> DocumentListRequest:
    if request is not None:
        return request
    return DocumentListRequest(
        doc_type=legacy_kwargs["doc_type"],
        period_start=legacy_kwargs["period_start"],
        period_end=legacy_kwargs["period_end"],
        granularity=legacy_kwargs.get("granularity"),
        order_by=legacy_kwargs.get("order_by", "event_desc"),
        offset=int(legacy_kwargs.get("offset", 0)),
        limit=int(legacy_kwargs.get("limit", 50)),
    )


def coerce_chunk_search_request(
    *,
    request: ChunkSearchRequest | None = None,
    legacy_kwargs: dict[str, Any],
) -> ChunkSearchRequest:
    if request is not None:
        return request
    return ChunkSearchRequest(
        query=legacy_kwargs["query"],
        doc_type=legacy_kwargs["doc_type"],
        granularity=legacy_kwargs.get("granularity"),
        period_start=legacy_kwargs["period_start"],
        period_end=legacy_kwargs["period_end"],
        limit=int(legacy_kwargs.get("limit", 10)),
    )


def coerce_summary_chunk_list_request(
    *,
    request: SummaryChunkListRequest | None = None,
    legacy_kwargs: dict[str, Any],
) -> SummaryChunkListRequest:
    if request is not None:
        return request
    return SummaryChunkListRequest(
        doc_type=legacy_kwargs["doc_type"],
        period_start=legacy_kwargs["period_start"],
        period_end=legacy_kwargs["period_end"],
        limit=int(legacy_kwargs.get("limit", 500)),
        offset=int(legacy_kwargs.get("offset", 0)),
    )


def coerce_summary_chunk_index_request(
    *,
    request: SummaryChunkIndexListRequest | None = None,
    legacy_kwargs: dict[str, Any],
) -> SummaryChunkIndexListRequest:
    if request is not None:
        return request
    return SummaryChunkIndexListRequest(
        doc_type=legacy_kwargs["doc_type"],
        period_start=legacy_kwargs["period_start"],
        period_end=legacy_kwargs["period_end"],
        granularity=legacy_kwargs.get("granularity"),
        limit=int(legacy_kwargs.get("limit", 500)),
        offset=int(legacy_kwargs.get("offset", 0)),
    )


def coerce_chunk_embedding_request(
    *,
    request: ChunkEmbeddingUpsertRequest | None = None,
    legacy_kwargs: dict[str, Any],
) -> ChunkEmbeddingUpsertRequest:
    if request is not None:
        return request
    return ChunkEmbeddingUpsertRequest(
        chunk_id=legacy_kwargs["chunk_id"],
        model=legacy_kwargs["model"],
        dimensions=legacy_kwargs.get("dimensions"),
        text_hash=legacy_kwargs["text_hash"],
        vector=list(legacy_kwargs["vector"]),
    )


class DocumentStoreMixin:
    engine: Any

    def _commit(self, session: Session) -> None: ...

    def upsert_document_for_item(
        self,
        *,
        request: ItemDocumentUpsertRequest | None = None,
        **legacy_kwargs: Any,
    ) -> Document:
        normalized_request = coerce_item_document_request(
            request=request,
            legacy_kwargs=legacy_kwargs,
        )
        item = normalized_request.item
        raw_item_id = getattr(item, "id", None)
        if raw_item_id is None:
            raise ValueError("item must have an id")
        item_id = int(raw_item_id)
        if item_id <= 0:
            raise ValueError("item_id must be > 0")
        values = _item_document_values(
            item=item,
            event_at=item.published_at or item.created_at,
        )
        with Session(self.engine) as session:
            document = _stored_item_document(
                session=session,
                item_id=item_id,
                values=values,
            )
            session.add(document)
            self._commit(session)
            session.refresh(document)
            return document

    def upsert_document_for_trend(
        self,
        *,
        granularity: str,
        period_start: datetime,
        period_end: datetime,
        title: str,
    ) -> Document:
        return self._upsert_period_document(
            doc_type="trend",
            granularity=granularity,
            period_start=period_start,
            period_end=period_end,
            title=title,
        )

    def upsert_document_for_idea(
        self,
        *,
        granularity: str,
        period_start: datetime,
        period_end: datetime,
        title: str,
    ) -> Document:
        return self._upsert_period_document(
            doc_type="idea",
            granularity=granularity,
            period_start=period_start,
            period_end=period_end,
            title=title,
        )

    def _upsert_period_document(
        self,
        *,
        request: PeriodDocumentUpsertRequest | None = None,
        **legacy_kwargs: Any,
    ) -> Document:
        normalized_request = coerce_period_document_request(
            request=request,
            legacy_kwargs=legacy_kwargs,
        )
        normalized_granularity = str(normalized_request.granularity or "").strip().lower()
        if normalized_granularity not in {"day", "week", "month"}:
            raise ValueError("unsupported granularity")
        normalized_doc_type = str(normalized_request.doc_type or "").strip().lower()
        if normalized_doc_type not in {"trend", "idea"}:
            raise ValueError("unsupported doc_type")
        fallback_title = "Idea" if normalized_doc_type == "idea" else "Trend"
        normalized_title = str(normalized_request.title or "").strip() or fallback_title
        with Session(self.engine) as session:
            existing = session.exec(
                select(Document).where(
                    Document.doc_type == normalized_doc_type,
                    Document.granularity == normalized_granularity,
                    Document.period_start == normalized_request.period_start,
                    Document.period_end == normalized_request.period_end,
                )
            ).first()
            if existing is None:
                doc = Document(
                    doc_type=normalized_doc_type,
                    granularity=normalized_granularity,
                    period_start=normalized_request.period_start,
                    period_end=normalized_request.period_end,
                    title=normalized_title,
                )
                session.add(doc)
                self._commit(session)
                session.refresh(doc)
                return doc

            existing.title = normalized_title
            existing.updated_at = utc_now()
            session.add(existing)
            self._commit(session)
            session.refresh(existing)
            return existing

    def upsert_document_chunk(
        self,
        *,
        request: ChunkUpsertRequest | None = None,
        **legacy_kwargs: Any,
    ) -> tuple[DocumentChunk, bool]:
        spec = normalize_chunk_upsert(
            coerce_document_chunk_request(
                request=request,
                legacy_kwargs=legacy_kwargs,
            )
        )
        with Session(self.engine) as session:
            existing = _load_existing_document_chunk(
                session,
                doc_id=spec.doc_id,
                chunk_index=spec.chunk_index,
            )
            chunk, inserted, changed = _stored_document_chunk(
                store=self,
                session=session,
                existing=existing,
                spec=spec,
            )
            if not changed:
                return chunk, inserted

        _sync_document_chunk_fts(
            store=self,
            chunk=chunk,
            spec=spec,
        )
        return chunk, inserted

    def delete_document_chunks(
        self,
        *,
        doc_id: int,
        kind: str | None = None,
        chunk_index_gte: int | None = None,
    ) -> int:
        spec = normalize_chunk_delete(
            doc_id=doc_id,
            kind=kind,
            chunk_index_gte=chunk_index_gte,
        )
        with Session(self.engine) as session:
            rows = load_chunks_for_delete(session=session, spec=spec)
            if not rows:
                return 0
            delete_chunk_side_tables(
                engine=self.engine,
                chunk_ids=collect_chunk_ids(rows),
            )
            for row in rows:
                session.delete(row)
            self._commit(session)
            return len(rows)

    def _sync_chunk_fts(
        self,
        *,
        request: ChunkFtsSyncRequest | None = None,
        **legacy_kwargs: Any,
    ) -> None:
        normalized_request = coerce_chunk_fts_sync_request(
            request=request,
            legacy_kwargs=legacy_kwargs,
        )
        normalized_chunk_id = int(normalized_request.chunk_id)
        normalized_doc_id = int(normalized_request.doc_id)
        if normalized_chunk_id <= 0 or normalized_doc_id <= 0:
            return
        payload = {
            "rowid": normalized_chunk_id,
            "text": str(normalized_request.text_value),
            "doc_id": normalized_doc_id,
            "chunk_index": int(normalized_request.chunk_index),
            "kind": str(normalized_request.kind),
        }
        with self.engine.begin() as conn:
            conn.execute(
                text("DELETE FROM chunk_fts WHERE rowid = :rowid"),
                {"rowid": normalized_chunk_id},
            )
            if str(normalized_request.kind or "").strip().lower() == "meta":
                return
            conn.execute(
                text(
                    "INSERT INTO chunk_fts(rowid, text, doc_id, chunk_index, kind) "
                    "VALUES(:rowid, :text, :doc_id, :chunk_index, :kind)"
                ),
                payload,
            )

    def list_documents(
        self,
        *,
        request: DocumentListRequest | None = None,
        **legacy_kwargs: Any,
    ) -> list[Document]:
        normalized_request = coerce_document_list_request(
            request=request,
            legacy_kwargs=legacy_kwargs,
        )
        normalized_type = normalize_doc_type(normalized_request.doc_type)
        normalized_limit, normalized_offset = normalize_limit_offset(
            limit=normalized_request.limit,
            offset=normalized_request.offset,
        )
        if normalized_limit <= 0:
            return []
        with Session(self.engine) as session:
            return list(
                session.exec(
                    build_document_list_statement(
                        normalized_type=normalized_type,
                        period_start=normalized_request.period_start,
                        period_end=normalized_request.period_end,
                        granularity=normalized_request.granularity,
                        order_by=normalized_request.order_by,
                    )
                    .offset(normalized_offset)
                    .limit(normalized_limit)
                )
            )

    def get_document(self, *, doc_id: int) -> Document | None:
        normalized_id = int(doc_id)
        if normalized_id <= 0:
            return None
        with Session(self.engine) as session:
            return session.get(Document, normalized_id)

    def get_item(self, *, item_id: int) -> Item | None:
        normalized_id = int(item_id)
        if normalized_id <= 0:
            return None
        with Session(self.engine) as session:
            return session.get(Item, normalized_id)

    def read_document_chunk(
        self, *, doc_id: int, chunk_index: int
    ) -> DocumentChunk | None:
        normalized_doc_id = int(doc_id)
        normalized_index = int(chunk_index)
        if normalized_doc_id <= 0 or normalized_index < 0:
            return None
        with Session(self.engine) as session:
            statement = select(DocumentChunk).where(
                DocumentChunk.doc_id == normalized_doc_id,
                DocumentChunk.chunk_index == normalized_index,
            )
            return session.exec(statement).first()

    def search_chunks_text(
        self,
        *,
        request: ChunkSearchRequest | None = None,
        **legacy_kwargs: Any,
    ) -> list[dict[str, Any]]:
        search_spec = build_chunk_search(
            coerce_chunk_search_request(
                request=request,
                legacy_kwargs=legacy_kwargs,
            )
        )
        if search_spec is None:
            return []
        sql, params = search_spec
        with self.engine.begin() as conn:
            rows = conn.execute(text(sql), params).mappings().all()
        return [
            hit for row in rows if (hit := decode_search_hit_row(row)) is not None
        ]

    def list_summary_chunks_in_period(
        self,
        *,
        request: SummaryChunkListRequest | None = None,
        **legacy_kwargs: Any,
    ) -> list[DocumentChunk]:
        normalized_request = coerce_summary_chunk_list_request(
            request=request,
            legacy_kwargs=legacy_kwargs,
        )
        normalized_type = str(normalized_request.doc_type or "").strip().lower()
        normalized_limit = max(0, int(normalized_request.limit))
        normalized_offset = max(0, int(normalized_request.offset))
        if normalized_limit <= 0:
            return []

        with Session(self.engine) as session:
            statement = (
                select(DocumentChunk)
                .join(Document, cast(Any, Document.id) == cast(Any, DocumentChunk.doc_id))
                .where(
                    Document.doc_type == normalized_type,
                    DocumentChunk.kind == "summary",
                )
            )
            if normalized_type == "item":
                statement = statement.where(
                    cast(Any, Document.published_at).is_not(None),
                    cast(Any, Document.published_at) >= normalized_request.period_start,
                    cast(Any, Document.published_at) < normalized_request.period_end,
                )
            elif normalized_type in {"trend", "idea"}:
                statement = statement.where(
                    cast(Any, Document.period_start).is_not(None),
                    cast(Any, Document.period_end).is_not(None),
                    cast(Any, Document.period_start) < normalized_request.period_end,
                    cast(Any, Document.period_end) > normalized_request.period_start,
                )
            else:
                raise ValueError("unsupported doc_type")

            statement = (
                statement.order_by(desc(cast(Any, DocumentChunk.id)))
                .offset(normalized_offset)
                .limit(normalized_limit)
            )
            return list(session.exec(statement))

    def list_summary_chunk_index_rows_in_period(
        self,
        *,
        request: SummaryChunkIndexListRequest | None = None,
        **legacy_kwargs: Any,
    ) -> list[dict[str, Any]]:
        normalized_request = coerce_summary_chunk_index_request(
            request=request,
            legacy_kwargs=legacy_kwargs,
        )
        normalized_type = normalize_doc_type(normalized_request.doc_type)
        normalized_limit, normalized_offset = normalize_limit_offset(
            limit=normalized_request.limit,
            offset=normalized_request.offset,
        )
        if normalized_limit <= 0:
            return []

        with Session(self.engine) as session:
            statement = build_summary_chunk_statement(
                normalized_type=normalized_type,
                period_start=normalized_request.period_start,
                period_end=normalized_request.period_end,
                granularity=normalized_request.granularity,
                include_document=True,
            )
            statement = statement.order_by(desc(cast(Any, DocumentChunk.id))).offset(
                normalized_offset
            ).limit(normalized_limit)
            rows = list(session.exec(statement))
        return [
            row
            for chunk, doc in rows
            if (row := summary_chunk_index_row(
                doc_type=normalized_type,
                chunk=chunk,
                document=doc,
            ))
            is not None
        ]

    def get_chunk_embedding(
        self, *, chunk_id: int, model: str
    ) -> ChunkEmbedding | None:
        normalized_chunk_id = int(chunk_id)
        normalized_model = str(model or "").strip()
        if normalized_chunk_id <= 0 or not normalized_model:
            return None
        with Session(self.engine) as session:
            statement = select(ChunkEmbedding).where(
                ChunkEmbedding.chunk_id == normalized_chunk_id,
                ChunkEmbedding.model == normalized_model,
            )
            return session.exec(statement).first()

    def list_chunk_embeddings(
        self, *, chunk_ids: list[int], model: str
    ) -> dict[int, ChunkEmbedding]:
        normalized_model = str(model or "").strip()
        if not normalized_model:
            return {}
        normalized_ids: list[int] = []
        seen: set[int] = set()
        for raw in chunk_ids or []:
            try:
                cid = int(raw)
            except Exception:
                continue
            if cid <= 0 or cid in seen:
                continue
            seen.add(cid)
            normalized_ids.append(cid)
        if not normalized_ids:
            return {}
        with Session(self.engine) as session:
            statement = select(ChunkEmbedding).where(
                ChunkEmbedding.model == normalized_model,
                cast(Any, ChunkEmbedding.chunk_id).in_(normalized_ids),
            )
            rows = list(session.exec(statement))
            return {int(row.chunk_id): row for row in rows}

    def upsert_chunk_embedding(
        self,
        *,
        request: ChunkEmbeddingUpsertRequest | None = None,
        **legacy_kwargs: Any,
    ) -> ChunkEmbedding:
        normalized_request = coerce_chunk_embedding_request(
            request=request,
            legacy_kwargs=legacy_kwargs,
        )
        normalized_values = _normalized_embedding_values(normalized_request)

        with Session(self.engine) as session:
            row = _stored_chunk_embedding(
                existing=_existing_chunk_embedding(
                    session=session,
                    chunk_id=normalized_values.chunk_id,
                    model=normalized_values.model,
                ),
                values=normalized_values,
            )
            session.add(row)
            self._commit(session)
            session.refresh(row)
            return row
