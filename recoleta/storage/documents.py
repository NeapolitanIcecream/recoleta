from __future__ import annotations

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


class DocumentStoreMixin:
    engine: Any

    def _commit(self, session: Session) -> None: ...

    def upsert_document_for_item(self, *, item: Item) -> Document:
        raw_item_id = getattr(item, "id", None)
        if raw_item_id is None:
            raise ValueError("item must have an id")
        item_id = int(raw_item_id)
        if item_id <= 0:
            raise ValueError("item_id must be > 0")
        event_at = item.published_at or item.created_at
        with Session(self.engine) as session:
            existing = session.exec(
                select(Document).where(
                    Document.doc_type == "item",
                    Document.item_id == item_id,
                )
            ).first()
            if existing is None:
                doc = Document(
                    doc_type="item",
                    item_id=item_id,
                    source=str(getattr(item, "source", "") or "").strip() or None,
                    canonical_url=str(getattr(item, "canonical_url", "") or "").strip()
                    or None,
                    title=str(getattr(item, "title", "") or "").strip() or None,
                    published_at=event_at,
                )
                session.add(doc)
                self._commit(session)
                session.refresh(doc)
                return doc

            existing.source = str(getattr(item, "source", "") or "").strip() or None
            existing.canonical_url = (
                str(getattr(item, "canonical_url", "") or "").strip() or None
            )
            existing.title = str(getattr(item, "title", "") or "").strip() or None
            existing.published_at = event_at
            existing.updated_at = utc_now()
            session.add(existing)
            self._commit(session)
            session.refresh(existing)
            return existing

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
        doc_type: str,
        granularity: str,
        period_start: datetime,
        period_end: datetime,
        title: str,
    ) -> Document:
        normalized_granularity = str(granularity or "").strip().lower()
        if normalized_granularity not in {"day", "week", "month"}:
            raise ValueError("unsupported granularity")
        normalized_doc_type = str(doc_type or "").strip().lower()
        if normalized_doc_type not in {"trend", "idea"}:
            raise ValueError("unsupported doc_type")
        fallback_title = "Idea" if normalized_doc_type == "idea" else "Trend"
        normalized_title = str(title or "").strip() or fallback_title
        with Session(self.engine) as session:
            existing = session.exec(
                select(Document).where(
                    Document.doc_type == normalized_doc_type,
                    Document.granularity == normalized_granularity,
                    Document.period_start == period_start,
                    Document.period_end == period_end,
                )
            ).first()
            if existing is None:
                doc = Document(
                    doc_type=normalized_doc_type,
                    granularity=normalized_granularity,
                    period_start=period_start,
                    period_end=period_end,
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
        doc_id: int,
        chunk_index: int,
        kind: str,
        text_value: str,
        start_char: int | None = None,
        end_char: int | None = None,
        source_content_type: str | None = None,
    ) -> tuple[DocumentChunk, bool]:
        spec = normalize_chunk_upsert(
            ChunkUpsertRequest(
                doc_id=doc_id,
                chunk_index=chunk_index,
                kind=kind,
                text_value=text_value,
                start_char=start_char,
                end_char=end_char,
                source_content_type=source_content_type,
            )
        )

        inserted = False
        with Session(self.engine) as session:
            existing = _load_existing_document_chunk(
                session,
                doc_id=spec.doc_id,
                chunk_index=spec.chunk_index,
            )
            if existing is None:
                chunk = _build_document_chunk(spec=spec)
                session.add(chunk)
                self._commit(session)
                session.refresh(chunk)
                inserted = True
            else:
                if str(getattr(existing, "text_hash", "") or "") == spec.text_hash:
                    return existing, False
                existing = _update_document_chunk(existing=existing, spec=spec)
                session.add(existing)
                self._commit(session)
                session.refresh(existing)
                chunk = existing

        chunk_id = getattr(chunk, "id", None)
        if chunk_id is not None:
            self._sync_chunk_fts(
                chunk_id=int(chunk_id),
                doc_id=spec.doc_id,
                chunk_index=spec.chunk_index,
                kind=spec.kind,
                text_value=spec.text,
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
        chunk_id: int,
        doc_id: int,
        chunk_index: int,
        kind: str,
        text_value: str,
    ) -> None:
        normalized_chunk_id = int(chunk_id)
        normalized_doc_id = int(doc_id)
        if normalized_chunk_id <= 0 or normalized_doc_id <= 0:
            return
        payload = {
            "rowid": normalized_chunk_id,
            "text": str(text_value),
            "doc_id": normalized_doc_id,
            "chunk_index": int(chunk_index),
            "kind": str(kind),
        }
        with self.engine.begin() as conn:
            conn.execute(
                text("DELETE FROM chunk_fts WHERE rowid = :rowid"),
                {"rowid": normalized_chunk_id},
            )
            if str(kind or "").strip().lower() == "meta":
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
        doc_type: str,
        period_start: datetime,
        period_end: datetime,
        granularity: str | None = None,
        order_by: str = "event_desc",
        offset: int = 0,
        limit: int = 50,
    ) -> list[Document]:
        normalized_type = normalize_doc_type(doc_type)
        normalized_limit, normalized_offset = normalize_limit_offset(
            limit=limit,
            offset=offset,
        )
        if normalized_limit <= 0:
            return []
        with Session(self.engine) as session:
            statement = build_document_list_statement(
                normalized_type=normalized_type,
                period_start=period_start,
                period_end=period_end,
                granularity=granularity,
                order_by=order_by,
            )
            statement = statement.offset(normalized_offset).limit(normalized_limit)
            return list(session.exec(statement))

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
        query: str,
        doc_type: str,
        granularity: str | None = None,
        period_start: datetime,
        period_end: datetime,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        search_spec = build_chunk_search(
            ChunkSearchRequest(
                query=query,
                doc_type=doc_type,
                granularity=granularity,
                period_start=period_start,
                period_end=period_end,
                limit=limit,
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
        doc_type: str,
        period_start: datetime,
        period_end: datetime,
        limit: int = 500,
        offset: int = 0,
    ) -> list[DocumentChunk]:
        normalized_type = str(doc_type or "").strip().lower()
        normalized_limit = max(0, int(limit))
        normalized_offset = max(0, int(offset))
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
                    cast(Any, Document.published_at) >= period_start,
                    cast(Any, Document.published_at) < period_end,
                )
            elif normalized_type in {"trend", "idea"}:
                statement = statement.where(
                    cast(Any, Document.period_start).is_not(None),
                    cast(Any, Document.period_end).is_not(None),
                    cast(Any, Document.period_start) < period_end,
                    cast(Any, Document.period_end) > period_start,
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
        doc_type: str,
        granularity: str | None = None,
        period_start: datetime,
        period_end: datetime,
        limit: int = 500,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        normalized_type = normalize_doc_type(doc_type)
        normalized_limit, normalized_offset = normalize_limit_offset(
            limit=limit,
            offset=offset,
        )
        if normalized_limit <= 0:
            return []

        with Session(self.engine) as session:
            statement = build_summary_chunk_statement(
                normalized_type=normalized_type,
                period_start=period_start,
                period_end=period_end,
                granularity=granularity,
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
        chunk_id: int,
        model: str,
        dimensions: int | None,
        text_hash: str,
        vector: list[float],
    ) -> ChunkEmbedding:
        normalized_chunk_id = int(chunk_id)
        normalized_model = str(model or "").strip()
        normalized_text_hash = str(text_hash or "").strip()
        if normalized_chunk_id <= 0:
            raise ValueError("chunk_id must be > 0")
        if not normalized_model:
            raise ValueError("model must not be empty")
        if not normalized_text_hash:
            raise ValueError("text_hash must not be empty")
        if not isinstance(vector, list) or not vector:
            raise ValueError("vector must be a non-empty list")
        normalized_dims = int(dimensions) if dimensions is not None else None
        if normalized_dims is not None and normalized_dims <= 0:
            raise ValueError("dimensions must be positive")
        normalized_vector = [float(v) for v in vector]
        vector_json = _to_json(normalized_vector)

        with Session(self.engine) as session:
            existing = session.exec(
                select(ChunkEmbedding).where(
                    ChunkEmbedding.chunk_id == normalized_chunk_id,
                    ChunkEmbedding.model == normalized_model,
                )
            ).first()
            if existing is None:
                row = ChunkEmbedding(
                    chunk_id=normalized_chunk_id,
                    model=normalized_model,
                    dimensions=normalized_dims,
                    vector_json=vector_json,
                    text_hash=normalized_text_hash,
                )
                session.add(row)
                self._commit(session)
                session.refresh(row)
                return row

            if (
                str(getattr(existing, "text_hash", "") or "") == normalized_text_hash
                and str(getattr(existing, "vector_json", "") or "") == vector_json
            ):
                return existing
            existing.dimensions = normalized_dims
            existing.vector_json = vector_json
            existing.text_hash = normalized_text_hash
            session.add(existing)
            self._commit(session)
            session.refresh(existing)
            return existing
