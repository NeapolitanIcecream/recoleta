from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, cast

from sqlalchemy import desc, text
from sqlmodel import Session, select

from recoleta.models import ChunkEmbedding, Document, DocumentChunk, Item
from recoleta.storage_common import _to_fts5_query, _to_json
from recoleta.types import DEFAULT_TOPIC_STREAM, sha256_hex, utc_now


class DocumentStoreMixin:
    engine: Any

    def _commit(self, session: Session) -> None: ...

    def upsert_document_for_item(
        self, *, item: Item, scope: str = DEFAULT_TOPIC_STREAM
    ) -> Document:
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
                    cast(Any, Document.scope) == scope,
                )
            ).first()
            if existing is None:
                doc = Document(
                    doc_type="item",
                    scope=scope,
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
        scope: str = DEFAULT_TOPIC_STREAM,
    ) -> Document:
        return self._upsert_period_document(
            doc_type="trend",
            granularity=granularity,
            period_start=period_start,
            period_end=period_end,
            title=title,
            scope=scope,
        )

    def upsert_document_for_idea(
        self,
        *,
        granularity: str,
        period_start: datetime,
        period_end: datetime,
        title: str,
        scope: str = DEFAULT_TOPIC_STREAM,
    ) -> Document:
        return self._upsert_period_document(
            doc_type="idea",
            granularity=granularity,
            period_start=period_start,
            period_end=period_end,
            title=title,
            scope=scope,
        )

    def _upsert_period_document(
        self,
        *,
        doc_type: str,
        granularity: str,
        period_start: datetime,
        period_end: datetime,
        title: str,
        scope: str = DEFAULT_TOPIC_STREAM,
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
                    cast(Any, Document.scope) == scope,
                    Document.granularity == normalized_granularity,
                    Document.period_start == period_start,
                    Document.period_end == period_end,
                )
            ).first()
            if existing is None:
                doc = Document(
                    doc_type=normalized_doc_type,
                    scope=scope,
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
        normalized_doc_id = int(doc_id)
        if normalized_doc_id <= 0:
            raise ValueError("doc_id must be > 0")
        normalized_index = int(chunk_index)
        if normalized_index < 0:
            raise ValueError("chunk_index must be >= 0")
        normalized_kind = str(kind or "").strip().lower()
        if normalized_kind not in {"summary", "content", "meta"}:
            raise ValueError("unsupported chunk kind")
        normalized_text = str(text_value or "").strip()
        if not normalized_text:
            raise ValueError("chunk text must not be empty")
        text_hash = sha256_hex(normalized_text)

        inserted = False
        with Session(self.engine) as session:
            existing = session.exec(
                select(DocumentChunk).where(
                    DocumentChunk.doc_id == normalized_doc_id,
                    DocumentChunk.chunk_index == normalized_index,
                )
            ).first()
            if existing is None:
                chunk = DocumentChunk(
                    doc_id=normalized_doc_id,
                    chunk_index=normalized_index,
                    kind=normalized_kind,
                    text=normalized_text,
                    start_char=start_char,
                    end_char=end_char,
                    text_hash=text_hash,
                    source_content_type=(
                        str(source_content_type).strip()
                        if isinstance(source_content_type, str)
                        and str(source_content_type).strip()
                        else None
                    ),
                )
                session.add(chunk)
                self._commit(session)
                session.refresh(chunk)
                inserted = True
            else:
                if str(getattr(existing, "text_hash", "") or "") == text_hash:
                    return existing, False
                existing.kind = normalized_kind
                existing.text = normalized_text
                existing.start_char = start_char
                existing.end_char = end_char
                existing.text_hash = text_hash
                existing.source_content_type = (
                    str(source_content_type).strip()
                    if isinstance(source_content_type, str)
                    and str(source_content_type).strip()
                    else None
                )
                session.add(existing)
                self._commit(session)
                session.refresh(existing)
                chunk = existing

        chunk_id = getattr(chunk, "id", None)
        if chunk_id is not None:
            self._sync_chunk_fts(
                chunk_id=int(chunk_id),
                doc_id=normalized_doc_id,
                chunk_index=normalized_index,
                kind=normalized_kind,
                text_value=normalized_text,
            )
        return chunk, inserted

    def delete_document_chunks(
        self,
        *,
        doc_id: int,
        kind: str | None = None,
        chunk_index_gte: int | None = None,
    ) -> int:
        normalized_doc_id = int(doc_id)
        if normalized_doc_id <= 0:
            raise ValueError("doc_id must be > 0")

        normalized_kind: str | None = None
        if kind is not None:
            candidate = str(kind or "").strip().lower()
            if not candidate:
                normalized_kind = None
            elif candidate not in {"summary", "content", "meta"}:
                raise ValueError("unsupported chunk kind")
            else:
                normalized_kind = candidate

        normalized_index_gte: int | None = None
        if chunk_index_gte is not None:
            normalized_index_gte = int(chunk_index_gte)
            if normalized_index_gte < 0:
                raise ValueError("chunk_index_gte must be >= 0")

        with Session(self.engine) as session:
            statement = select(DocumentChunk).where(
                DocumentChunk.doc_id == normalized_doc_id
            )
            if normalized_kind is not None:
                statement = statement.where(DocumentChunk.kind == normalized_kind)
            if normalized_index_gte is not None:
                statement = statement.where(
                    DocumentChunk.chunk_index >= normalized_index_gte
                )
            rows = list(session.exec(statement))
            if not rows:
                return 0

            chunk_ids: list[int] = []
            for row in rows:
                raw_id = getattr(row, "id", None)
                if raw_id is None:
                    continue
                try:
                    cid = int(raw_id)
                except Exception:
                    continue
                if cid > 0:
                    chunk_ids.append(cid)

            if chunk_ids:
                with self.engine.begin() as conn:
                    for cid in chunk_ids:
                        conn.execute(
                            text("DELETE FROM chunk_embeddings WHERE chunk_id = :chunk_id"),
                            {"chunk_id": cid},
                        )
                        conn.execute(
                            text("DELETE FROM chunk_fts WHERE rowid = :rowid"),
                            {"rowid": cid},
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
        scope: str = DEFAULT_TOPIC_STREAM,
        order_by: str = "event_desc",
        offset: int = 0,
        limit: int = 50,
    ) -> list[Document]:
        normalized_type = str(doc_type or "").strip().lower()
        normalized_limit = max(0, int(limit))
        normalized_offset = max(0, int(offset))
        if normalized_limit <= 0:
            return []
        with Session(self.engine) as session:
            statement = select(Document).where(
                Document.doc_type == normalized_type,
                cast(Any, Document.scope) == scope,
            )
            if normalized_type == "item":
                statement = statement.where(
                    cast(Any, Document.published_at).is_not(None),
                    cast(Any, Document.published_at) >= period_start,
                    cast(Any, Document.published_at) < period_end,
                )
                if order_by == "event_asc":
                    statement = statement.order_by(
                        cast(Any, Document.published_at), cast(Any, Document.id)
                    )
                else:
                    statement = statement.order_by(
                        desc(cast(Any, Document.published_at)),
                        desc(cast(Any, Document.id)),
                    )
            elif normalized_type in {"trend", "idea"}:
                statement = statement.where(
                    cast(Any, Document.period_start).is_not(None),
                    cast(Any, Document.period_end).is_not(None),
                    cast(Any, Document.period_start) < period_end,
                    cast(Any, Document.period_end) > period_start,
                )
                normalized_granularity = (
                    str(granularity or "").strip().lower()
                    if granularity is not None
                    else ""
                )
                if normalized_granularity:
                    statement = statement.where(
                        Document.granularity == normalized_granularity
                    )
                if order_by == "event_asc":
                    statement = statement.order_by(
                        cast(Any, Document.period_start), cast(Any, Document.id)
                    )
                else:
                    statement = statement.order_by(
                        desc(cast(Any, Document.period_start)),
                        desc(cast(Any, Document.id)),
                    )
            else:
                raise ValueError("unsupported doc_type")
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
        scope: str = DEFAULT_TOPIC_STREAM,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        normalized_query = str(query or "").strip()
        if not normalized_query:
            return []
        fts_query = _to_fts5_query(normalized_query)
        if not fts_query:
            return []
        normalized_type = str(doc_type or "").strip().lower()
        normalized_limit = max(1, min(int(limit), 50))

        if normalized_type == "item":
            period_pred = "d.published_at >= :period_start AND d.published_at < :period_end"
        elif normalized_type in {"trend", "idea"}:
            period_pred = "d.period_start < :period_end AND d.period_end > :period_start"
        else:
            raise ValueError("unsupported doc_type")

        extra_predicates: list[str] = []
        params = {
            "query": fts_query,
            "doc_type": normalized_type,
            "scope": scope,
            "period_start": period_start,
            "period_end": period_end,
            "limit": normalized_limit,
        }
        if normalized_type in {"trend", "idea"}:
            normalized_granularity = (
                str(granularity or "").strip().lower() if granularity is not None else ""
            )
            if normalized_granularity:
                extra_predicates.append("d.granularity = :granularity")
                params["granularity"] = normalized_granularity

        sql = f"""
        SELECT
            dc.id AS chunk_id,
            dc.doc_id AS doc_id,
            dc.chunk_index AS chunk_index,
            dc.kind AS kind,
            snippet(chunk_fts, 0, '[', ']', '…', 12) AS snippet,
            bm25(chunk_fts) AS rank
        FROM chunk_fts
        JOIN document_chunks dc ON dc.id = chunk_fts.rowid
        JOIN documents d ON d.id = dc.doc_id
        WHERE
            chunk_fts MATCH :query
            AND d.doc_type = :doc_type
            AND d.scope = :scope
            AND {period_pred}
            {"AND " + " AND ".join(extra_predicates) if extra_predicates else ""}
        ORDER BY rank ASC
        LIMIT :limit
        """
        with self.engine.begin() as conn:
            rows = conn.execute(text(sql), params).mappings().all()
        out: list[dict[str, Any]] = []
        for row in rows:
            raw_chunk_id = row.get("chunk_id")
            raw_doc_id = row.get("doc_id")
            raw_chunk_index = row.get("chunk_index")
            if raw_chunk_id is None or raw_doc_id is None or raw_chunk_index is None:
                continue
            try:
                chunk_id = int(raw_chunk_id)
                doc_id = int(raw_doc_id)
                chunk_index = int(raw_chunk_index)
            except Exception:
                continue
            if chunk_id <= 0 or doc_id <= 0 or chunk_index < 0:
                continue
            out.append(
                {
                    "chunk_id": chunk_id,
                    "doc_id": doc_id,
                    "chunk_index": chunk_index,
                    "kind": str(row.get("kind") or ""),
                    "snippet": str(row.get("snippet") or ""),
                    "rank": float(row.get("rank") or 0.0),
                }
            )
        return out

    def list_summary_chunks_in_period(
        self,
        *,
        doc_type: str,
        period_start: datetime,
        period_end: datetime,
        scope: str = DEFAULT_TOPIC_STREAM,
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
                    cast(Any, Document.scope) == scope,
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
        scope: str = DEFAULT_TOPIC_STREAM,
        limit: int = 500,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        normalized_type = str(doc_type or "").strip().lower()
        normalized_limit = max(0, int(limit))
        normalized_offset = max(0, int(offset))
        if normalized_limit <= 0:
            return []

        with Session(self.engine) as session:
            statement = (
                select(DocumentChunk, Document)
                .join(Document, cast(Any, Document.id) == cast(Any, DocumentChunk.doc_id))
                .where(
                    Document.doc_type == normalized_type,
                    cast(Any, Document.scope) == scope,
                    DocumentChunk.kind == "summary",
                )
            )
            if normalized_type == "item":
                statement = statement.where(
                    cast(Any, Document.published_at).is_not(None),
                    cast(Any, Document.published_at) >= period_start,
                    cast(Any, Document.published_at) < period_end,
                )
                statement = statement.order_by(desc(cast(Any, DocumentChunk.id)))
            elif normalized_type in {"trend", "idea"}:
                statement = statement.where(
                    cast(Any, Document.period_start).is_not(None),
                    cast(Any, Document.period_end).is_not(None),
                    cast(Any, Document.period_start) < period_end,
                    cast(Any, Document.period_end) > period_start,
                )
                normalized_granularity = (
                    str(granularity or "").strip().lower()
                    if granularity is not None
                    else ""
                )
                if normalized_granularity:
                    statement = statement.where(
                        Document.granularity == normalized_granularity
                    )
                statement = statement.order_by(desc(cast(Any, DocumentChunk.id)))
            else:
                raise ValueError("unsupported doc_type")

            statement = statement.offset(normalized_offset).limit(normalized_limit)
            rows = list(session.exec(statement))

        out: list[dict[str, Any]] = []
        for chunk, doc in rows:
            chunk_id = getattr(chunk, "id", None)
            doc_id = getattr(doc, "id", None)
            if chunk_id is None or doc_id is None:
                continue
            if normalized_type == "item":
                published_at = getattr(doc, "published_at", None)
                if not isinstance(published_at, datetime):
                    continue
                if published_at.tzinfo is None:
                    published_at = published_at.replace(tzinfo=UTC)
                event_start_ts = float(published_at.timestamp())
                event_end_ts = float(published_at.timestamp())
            else:
                dstart = getattr(doc, "period_start", None)
                dend = getattr(doc, "period_end", None)
                if not isinstance(dstart, datetime) or not isinstance(dend, datetime):
                    continue
                if dstart.tzinfo is None:
                    dstart = dstart.replace(tzinfo=UTC)
                if dend.tzinfo is None:
                    dend = dend.replace(tzinfo=UTC)
                event_start_ts = float(dstart.timestamp())
                event_end_ts = float(dend.timestamp())

            text_value = str(getattr(chunk, "text", "") or "")
            preview = text_value[:240] + ("..." if len(text_value) > 240 else "")
            out.append(
                {
                    "chunk_id": int(chunk_id),
                    "doc_id": int(doc_id),
                    "doc_type": normalized_type,
                    "granularity": str(getattr(doc, "granularity", "") or "") or None,
                    "chunk_index": int(getattr(chunk, "chunk_index")),
                    "kind": str(getattr(chunk, "kind") or ""),
                    "text": text_value,
                    "text_hash": str(getattr(chunk, "text_hash") or ""),
                    "text_preview": preview,
                    "event_start_ts": event_start_ts,
                    "event_end_ts": event_end_ts,
                }
            )
        return out

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
