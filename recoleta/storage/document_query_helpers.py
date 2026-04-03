from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, cast

from sqlalchemy import desc, text
from sqlmodel import Session, select

from recoleta.models import Document, DocumentChunk
from recoleta.storage_common import _to_fts5_query
from recoleta.types import sha256_hex


@dataclass(frozen=True, slots=True)
class ChunkUpsertSpec:
    doc_id: int
    chunk_index: int
    kind: str
    text: str
    text_hash: str
    start_char: int | None
    end_char: int | None
    source_content_type: str | None


@dataclass(frozen=True, slots=True)
class ChunkDeleteSpec:
    doc_id: int
    kind: str | None
    chunk_index_gte: int | None


@dataclass(frozen=True, slots=True)
class ChunkUpsertRequest:
    doc_id: int
    chunk_index: int
    kind: str
    text_value: str
    start_char: int | None
    end_char: int | None
    source_content_type: str | None


@dataclass(frozen=True, slots=True)
class ChunkSearchRequest:
    query: str
    doc_type: str
    granularity: str | None
    period_start: datetime
    period_end: datetime
    limit: int


def normalize_doc_type(doc_type: str) -> str:
    return str(doc_type or "").strip().lower()


def normalize_granularity(granularity: str | None) -> str:
    return str(granularity or "").strip().lower()


def normalize_limit_offset(*, limit: int, offset: int = 0) -> tuple[int, int]:
    return max(0, int(limit)), max(0, int(offset))


def normalize_chunk_upsert(request: ChunkUpsertRequest) -> ChunkUpsertSpec:
    normalized_doc_id = int(request.doc_id)
    if normalized_doc_id <= 0:
        raise ValueError("doc_id must be > 0")
    normalized_index = int(request.chunk_index)
    if normalized_index < 0:
        raise ValueError("chunk_index must be >= 0")
    normalized_kind = str(request.kind or "").strip().lower()
    if normalized_kind not in {"summary", "content", "meta"}:
        raise ValueError("unsupported chunk kind")
    normalized_text = str(request.text_value or "").strip()
    if not normalized_text:
        raise ValueError("chunk text must not be empty")
    normalized_source_content_type = (
        str(request.source_content_type).strip()
        if isinstance(request.source_content_type, str)
        and str(request.source_content_type).strip()
        else None
    )
    return ChunkUpsertSpec(
        doc_id=normalized_doc_id,
        chunk_index=normalized_index,
        kind=normalized_kind,
        text=normalized_text,
        text_hash=sha256_hex(normalized_text),
        start_char=request.start_char,
        end_char=request.end_char,
        source_content_type=normalized_source_content_type,
    )


def normalize_chunk_delete(
    *,
    doc_id: int,
    kind: str | None,
    chunk_index_gte: int | None,
) -> ChunkDeleteSpec:
    normalized_doc_id = int(doc_id)
    if normalized_doc_id <= 0:
        raise ValueError("doc_id must be > 0")
    normalized_kind: str | None = None
    if kind is not None:
        candidate = str(kind or "").strip().lower()
        if candidate:
            if candidate not in {"summary", "content", "meta"}:
                raise ValueError("unsupported chunk kind")
            normalized_kind = candidate
    normalized_index_gte: int | None = None
    if chunk_index_gte is not None:
        normalized_index_gte = int(chunk_index_gte)
        if normalized_index_gte < 0:
            raise ValueError("chunk_index_gte must be >= 0")
    return ChunkDeleteSpec(
        doc_id=normalized_doc_id,
        kind=normalized_kind,
        chunk_index_gte=normalized_index_gte,
    )


def build_document_list_statement(
    *,
    normalized_type: str,
    period_start: datetime,
    period_end: datetime,
    granularity: str | None,
    order_by: str,
) -> Any:
    statement = select(Document).where(Document.doc_type == normalized_type)
    if normalized_type == "item":
        return _item_document_statement(
            statement=statement,
            period_start=period_start,
            period_end=period_end,
            order_by=order_by,
        )
    if normalized_type in {"trend", "idea"}:
        return _period_document_statement(
            statement=statement,
            period_start=period_start,
            period_end=period_end,
            granularity=granularity,
            order_by=order_by,
        )
    raise ValueError("unsupported doc_type")


def build_summary_chunk_statement(
    *,
    normalized_type: str,
    period_start: datetime,
    period_end: datetime,
    granularity: str | None,
    include_document: bool,
) -> Any:
    statement = (
        select(DocumentChunk, Document)
        if include_document
        else select(DocumentChunk)
    )
    statement = statement.join(
        Document,
        cast(Any, Document.id) == cast(Any, DocumentChunk.doc_id),
    ).where(
        Document.doc_type == normalized_type,
        DocumentChunk.kind == "summary",
    )
    if normalized_type == "item":
        return statement.where(
            cast(Any, Document.published_at).is_not(None),
            cast(Any, Document.published_at) >= period_start,
            cast(Any, Document.published_at) < period_end,
        )
    if normalized_type in {"trend", "idea"}:
        statement = statement.where(
            cast(Any, Document.period_start).is_not(None),
            cast(Any, Document.period_end).is_not(None),
            cast(Any, Document.period_start) < period_end,
            cast(Any, Document.period_end) > period_start,
        )
        normalized_granularity = normalize_granularity(granularity)
        if normalized_granularity:
            statement = statement.where(Document.granularity == normalized_granularity)
        return statement
    raise ValueError("unsupported doc_type")


def load_chunks_for_delete(*, session: Session, spec: ChunkDeleteSpec) -> list[DocumentChunk]:
    statement = select(DocumentChunk).where(DocumentChunk.doc_id == spec.doc_id)
    if spec.kind is not None:
        statement = statement.where(DocumentChunk.kind == spec.kind)
    if spec.chunk_index_gte is not None:
        statement = statement.where(DocumentChunk.chunk_index >= spec.chunk_index_gte)
    return list(session.exec(statement))


def collect_chunk_ids(rows: list[DocumentChunk]) -> list[int]:
    chunk_ids: list[int] = []
    for row in rows:
        raw_id = getattr(row, "id", None)
        if raw_id is None:
            continue
        try:
            chunk_id = int(raw_id)
        except Exception:
            continue
        if chunk_id > 0:
            chunk_ids.append(chunk_id)
    return chunk_ids


def delete_chunk_side_tables(*, engine: Any, chunk_ids: list[int]) -> None:
    if not chunk_ids:
        return
    with engine.begin() as conn:
        for chunk_id in chunk_ids:
            conn.execute(
                text("DELETE FROM chunk_embeddings WHERE chunk_id = :chunk_id"),
                {"chunk_id": chunk_id},
            )
            conn.execute(
                text("DELETE FROM chunk_fts WHERE rowid = :rowid"),
                {"rowid": chunk_id},
            )


def build_chunk_search(request: ChunkSearchRequest) -> tuple[str, dict[str, Any]] | None:
    normalized_query = str(request.query or "").strip()
    if not normalized_query:
        return None
    fts_query = _to_fts5_query(normalized_query)
    if not fts_query:
        return None
    normalized_type = normalize_doc_type(request.doc_type)
    normalized_limit = max(1, min(int(request.limit), 50))
    period_predicate = _search_period_predicate(normalized_type)
    extra_predicates, params = _search_extra_predicates(
        doc_type=normalized_type,
        granularity=request.granularity,
    )
    params.update(
        {
            "query": fts_query,
            "doc_type": normalized_type,
            "period_start": request.period_start,
            "period_end": request.period_end,
            "limit": normalized_limit,
        }
    )
    extra_sql = f"AND {' AND '.join(extra_predicates)}" if extra_predicates else ""
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
            AND dc.kind IN ('summary', 'content')
            AND {period_predicate}
            {extra_sql}
        ORDER BY rank ASC
        LIMIT :limit
    """
    return sql, params


def decode_search_hit_row(row: Any) -> dict[str, Any] | None:
    raw_chunk_id = row.get("chunk_id")
    raw_doc_id = row.get("doc_id")
    raw_chunk_index = row.get("chunk_index")
    if raw_chunk_id is None or raw_doc_id is None or raw_chunk_index is None:
        return None
    try:
        chunk_id = int(raw_chunk_id)
        doc_id = int(raw_doc_id)
        chunk_index = int(raw_chunk_index)
    except Exception:
        return None
    if chunk_id <= 0 or doc_id <= 0 or chunk_index < 0:
        return None
    return {
        "chunk_id": chunk_id,
        "doc_id": doc_id,
        "chunk_index": chunk_index,
        "kind": str(row.get("kind") or ""),
        "snippet": str(row.get("snippet") or ""),
        "rank": float(row.get("rank") or 0.0),
    }


def summary_chunk_index_row(
    *,
    doc_type: str,
    chunk: DocumentChunk,
    document: Document,
) -> dict[str, Any] | None:
    timestamps = _document_event_timestamps(doc_type=doc_type, document=document)
    if timestamps is None:
        return None
    text_value = str(getattr(chunk, "text", "") or "")
    return {
        "chunk_id": int(getattr(chunk, "id")),
        "doc_id": int(getattr(document, "id")),
        "doc_type": doc_type,
        "granularity": str(getattr(document, "granularity", "") or "") or None,
        "chunk_index": int(getattr(chunk, "chunk_index")),
        "kind": str(getattr(chunk, "kind") or ""),
        "text": text_value,
        "text_hash": str(getattr(chunk, "text_hash") or ""),
        "text_preview": _text_preview(text_value),
        "event_start_ts": timestamps[0],
        "event_end_ts": timestamps[1],
    }


def _item_document_statement(
    *,
    statement: Any,
    period_start: datetime,
    period_end: datetime,
    order_by: str,
) -> Any:
    statement = statement.where(
        cast(Any, Document.published_at).is_not(None),
        cast(Any, Document.published_at) >= period_start,
        cast(Any, Document.published_at) < period_end,
    )
    if order_by == "event_asc":
        return statement.order_by(
            cast(Any, Document.published_at),
            cast(Any, Document.id),
        )
    return statement.order_by(
        desc(cast(Any, Document.published_at)),
        desc(cast(Any, Document.id)),
    )


def _period_document_statement(
    *,
    statement: Any,
    period_start: datetime,
    period_end: datetime,
    granularity: str | None,
    order_by: str,
) -> Any:
    statement = statement.where(
        cast(Any, Document.period_start).is_not(None),
        cast(Any, Document.period_end).is_not(None),
        cast(Any, Document.period_start) < period_end,
        cast(Any, Document.period_end) > period_start,
    )
    normalized_granularity = normalize_granularity(granularity)
    if normalized_granularity:
        statement = statement.where(Document.granularity == normalized_granularity)
    if order_by == "event_asc":
        return statement.order_by(
            cast(Any, Document.period_start),
            cast(Any, Document.id),
        )
    return statement.order_by(
        desc(cast(Any, Document.period_start)),
        desc(cast(Any, Document.id)),
    )


def _search_period_predicate(doc_type: str) -> str:
    if doc_type == "item":
        return "d.published_at >= :period_start AND d.published_at < :period_end"
    if doc_type in {"trend", "idea"}:
        return "d.period_start < :period_end AND d.period_end > :period_start"
    raise ValueError("unsupported doc_type")


def _search_extra_predicates(
    *,
    doc_type: str,
    granularity: str | None,
) -> tuple[list[str], dict[str, Any]]:
    if doc_type not in {"trend", "idea"}:
        return [], {}
    normalized_granularity = normalize_granularity(granularity)
    if not normalized_granularity:
        return [], {}
    return ["d.granularity = :granularity"], {"granularity": normalized_granularity}


def _document_event_timestamps(
    *,
    doc_type: str,
    document: Document,
) -> tuple[float, float] | None:
    if doc_type == "item":
        published_at = getattr(document, "published_at", None)
        if not isinstance(published_at, datetime):
            return None
        if published_at.tzinfo is None:
            published_at = published_at.replace(tzinfo=UTC)
        timestamp = float(published_at.timestamp())
        return timestamp, timestamp
    period_start = getattr(document, "period_start", None)
    period_end = getattr(document, "period_end", None)
    if not isinstance(period_start, datetime) or not isinstance(period_end, datetime):
        return None
    if period_start.tzinfo is None:
        period_start = period_start.replace(tzinfo=UTC)
    if period_end.tzinfo is None:
        period_end = period_end.replace(tzinfo=UTC)
    return float(period_start.timestamp()), float(period_end.timestamp())


def _text_preview(text_value: str, *, max_chars: int = 240) -> str:
    return text_value[:max_chars] + ("..." if len(text_value) > max_chars else "")
