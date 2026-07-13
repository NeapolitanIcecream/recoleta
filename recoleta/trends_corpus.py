from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import time
from typing import Any, cast

from loguru import logger
from sqlalchemy import select as sa_select
from sqlalchemy import text
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlmodel import Session

from recoleta.models import Document, DocumentChunk
from recoleta.types import sha256_hex, utc_now


@dataclass(slots=True)
class SemanticSearchRequest:
    repository: Any
    lancedb_dir: Path
    run_id: str
    doc_type: str
    granularity: str | None
    period_start: datetime
    period_end: datetime
    query: str
    embedding_model: str
    embedding_dimensions: int | None
    max_batch_inputs: int
    max_batch_chars: int
    embedding_failure_mode: str = "continue"
    embedding_max_errors: int = 0
    limit: int = 10
    corpus_limit: int = 500
    metric_namespace: str | None = None
    llm_connection: Any | None = None


@dataclass(slots=True)
class IndexItemsAsDocumentsRequest:
    repository: Any
    run_id: str
    period_start: datetime
    period_end: datetime
    limit: int = 2000
    content_chunk_chars: int = 1200
    max_content_chunks_per_item: int = 8
    min_relevance_score: float = 0.0
    llm_model: str | None = None


@dataclass(slots=True)
class GenerateTrendRequest:
    repository: Any
    run_id: str
    llm_model: str
    output_language: str | None
    embedding_model: str
    embedding_dimensions: int | None
    embedding_batch_max_inputs: int
    embedding_batch_max_chars: int
    embedding_failure_mode: str
    embedding_max_errors: int
    lancedb_dir: Path
    granularity: str
    period_start: datetime
    period_end: datetime
    corpus_doc_type: str
    corpus_granularity: str | None
    overview_pack_md: str | None
    history_pack_md: str | None
    rag_sources: list[dict[str, str | None]] | None
    ranking_n: int | None
    rep_source_doc_type: str | None
    evolution_max_signals: int | None
    include_debug: bool
    metric_namespace: str
    llm_connection: Any | None


@dataclass(frozen=True, slots=True)
class _TargetRowsForPairsRequest:
    trends_module: Any
    pairs: list[tuple[Any, Any]]
    doc_ids_by_item_id: dict[int, int]
    texts_by_item_id: dict[int, dict[str, str | None]]
    content_types: list[str]
    content_chunk_chars: int
    max_content_chunks_per_item: int


@dataclass(frozen=True, slots=True)
class _ContentSegmentRowsRequest:
    trends_module: Any
    doc_id: int
    chosen: str
    chosen_type: str
    content_chunk_chars: int
    max_content_chunks_per_item: int


@dataclass(frozen=True, slots=True)
class _TargetRowsForPairRequest:
    trends_module: Any
    item: Any
    analysis: Any
    doc_ids_by_item_id: dict[int, int]
    texts_by_item_id: dict[int, dict[str, str | None]]
    content_types: list[str]
    content_chunk_chars: int
    max_content_chunks_per_item: int


@dataclass(frozen=True, slots=True)
class _ExistingChunk:
    id: int
    doc_id: int
    chunk_index: int
    kind: str
    text_hash: str


def coerce_semantic_search_request(
    *, request: SemanticSearchRequest | None = None, legacy_kwargs: dict[str, Any]
) -> SemanticSearchRequest:
    if request is not None:
        return request
    return SemanticSearchRequest(
        repository=legacy_kwargs["repository"],
        lancedb_dir=Path(legacy_kwargs["lancedb_dir"]),
        run_id=str(legacy_kwargs["run_id"]),
        doc_type=str(legacy_kwargs["doc_type"]),
        granularity=legacy_kwargs.get("granularity"),
        period_start=legacy_kwargs["period_start"],
        period_end=legacy_kwargs["period_end"],
        query=str(legacy_kwargs["query"]),
        embedding_model=str(legacy_kwargs["embedding_model"]),
        embedding_dimensions=legacy_kwargs.get("embedding_dimensions"),
        max_batch_inputs=int(legacy_kwargs["max_batch_inputs"]),
        max_batch_chars=int(legacy_kwargs["max_batch_chars"]),
        embedding_failure_mode=str(
            legacy_kwargs.get("embedding_failure_mode", "continue")
        ),
        embedding_max_errors=int(legacy_kwargs.get("embedding_max_errors", 0)),
        limit=int(legacy_kwargs.get("limit", 10)),
        corpus_limit=int(legacy_kwargs.get("corpus_limit", 500)),
        metric_namespace=legacy_kwargs.get("metric_namespace"),
        llm_connection=legacy_kwargs.get("llm_connection"),
    )


def coerce_index_items_request(
    *,
    request: IndexItemsAsDocumentsRequest | None = None,
    legacy_kwargs: dict[str, Any],
) -> IndexItemsAsDocumentsRequest:
    if request is not None:
        return request
    return IndexItemsAsDocumentsRequest(
        repository=legacy_kwargs["repository"],
        run_id=str(legacy_kwargs["run_id"]),
        period_start=legacy_kwargs["period_start"],
        period_end=legacy_kwargs["period_end"],
        limit=int(legacy_kwargs.get("limit", 2000)),
        content_chunk_chars=int(legacy_kwargs.get("content_chunk_chars", 1200)),
        max_content_chunks_per_item=int(
            legacy_kwargs.get("max_content_chunks_per_item", 8)
        ),
        min_relevance_score=float(legacy_kwargs.get("min_relevance_score", 0.0)),
        llm_model=legacy_kwargs.get("llm_model"),
    )


def coerce_generate_trend_request(
    *, request: GenerateTrendRequest | None = None, legacy_kwargs: dict[str, Any]
) -> GenerateTrendRequest:
    if request is not None:
        return request
    return GenerateTrendRequest(
        repository=legacy_kwargs["repository"],
        run_id=str(legacy_kwargs["run_id"]),
        llm_model=str(legacy_kwargs["llm_model"]),
        output_language=legacy_kwargs.get("output_language"),
        embedding_model=str(legacy_kwargs["embedding_model"]),
        embedding_dimensions=legacy_kwargs.get("embedding_dimensions"),
        embedding_batch_max_inputs=int(legacy_kwargs["embedding_batch_max_inputs"]),
        embedding_batch_max_chars=int(legacy_kwargs["embedding_batch_max_chars"]),
        embedding_failure_mode=str(
            legacy_kwargs.get("embedding_failure_mode", "continue")
        ),
        embedding_max_errors=int(legacy_kwargs.get("embedding_max_errors", 0)),
        lancedb_dir=Path(legacy_kwargs["lancedb_dir"]),
        granularity=str(legacy_kwargs["granularity"]),
        period_start=legacy_kwargs["period_start"],
        period_end=legacy_kwargs["period_end"],
        corpus_doc_type=str(legacy_kwargs["corpus_doc_type"]),
        corpus_granularity=legacy_kwargs.get("corpus_granularity"),
        overview_pack_md=legacy_kwargs.get("overview_pack_md"),
        history_pack_md=legacy_kwargs.get("history_pack_md"),
        rag_sources=legacy_kwargs.get("rag_sources"),
        ranking_n=legacy_kwargs.get("ranking_n"),
        rep_source_doc_type=legacy_kwargs.get("rep_source_doc_type"),
        evolution_max_signals=legacy_kwargs.get("evolution_max_signals"),
        include_debug=bool(legacy_kwargs.get("include_debug", False)),
        metric_namespace=str(legacy_kwargs.get("metric_namespace", "pipeline.trends")),
        llm_connection=legacy_kwargs.get("llm_connection"),
    )


def _normalize_item_ids(item_ids: list[int]) -> list[int]:
    normalized_ids: list[int] = []
    seen_ids: set[int] = set()
    for raw_item_id in item_ids:
        try:
            item_id = int(raw_item_id)
        except Exception:
            continue
        if item_id <= 0 or item_id in seen_ids:
            continue
        seen_ids.add(item_id)
        normalized_ids.append(item_id)
    return normalized_ids


def _normalize_content_types(content_types: list[str]) -> list[str]:
    normalized_types = [
        str(content_type or "").strip() for content_type in content_types
    ]
    return [content_type for content_type in normalized_types if content_type]


def load_latest_content_texts_for_items_impl(
    *,
    repository: Any,
    item_ids: list[int],
    content_types: list[str],
) -> dict[int, dict[str, str | None]]:
    normalized_ids = _normalize_item_ids(item_ids)
    normalized_types = _normalize_content_types(content_types)
    if not normalized_ids or not normalized_types:
        return {}
    out: dict[int, dict[str, str | None]] = {
        item_id: {content_type: None for content_type in normalized_types}
        for item_id in normalized_ids
    }
    batch_text_getter = getattr(repository, "get_latest_content_texts_for_items", None)
    if callable(batch_text_getter):
        return cast(
            dict[int, dict[str, str | None]],
            batch_text_getter(item_ids=normalized_ids, content_types=normalized_types),
        )
    batch_getter = getattr(repository, "get_latest_contents", None)
    if callable(batch_getter):
        for content_type in normalized_types:
            contents = cast(
                dict[int, Any],
                batch_getter(item_ids=normalized_ids, content_type=content_type),
            )
            for item_id, content in contents.items():
                text_value = getattr(content, "text", None)
                bucket = out.setdefault(
                    item_id, {ctype: None for ctype in normalized_types}
                )
                bucket[content_type] = (
                    text_value
                    if isinstance(text_value, str) and text_value.strip()
                    else None
                )
        return out
    for item_id in normalized_ids:
        out[item_id] = repository.get_latest_content_texts(
            item_id=item_id,
            content_types=normalized_types,
        )
    return out


def _item_ids_from_pairs(pairs: list[tuple[Any, Any]]) -> list[int]:
    return [
        int(raw_id)
        for item, _analysis in pairs
        if (raw_id := getattr(item, "id", None)) is not None and int(raw_id) > 0
    ]


def _upsert_item_documents(
    *,
    session: Any,
    pairs: list[tuple[Any, Any]],
) -> tuple[dict[int, int], int]:
    table = cast(Any, Document).__table__
    now = utc_now()
    rows: list[dict[str, Any]] = []
    docs_upserted = 0
    for item, _analysis in pairs:
        item_id = _item_id_value(item)
        if item_id <= 0:
            continue
        rows.append(
            {
                "doc_type": "item",
                "item_id": item_id,
                "source": str(getattr(item, "source", "") or "").strip() or None,
                "canonical_url": (
                    str(getattr(item, "canonical_url", "") or "").strip() or None
                ),
                "title": str(getattr(item, "title", "") or "").strip() or None,
                "published_at": _item_event_at(item),
                "created_at": now,
                "updated_at": now,
            }
        )
        docs_upserted += 1
    if not rows:
        return {}, 0

    insert_statement = sqlite_insert(table)
    session.connection().execute(
        insert_statement.on_conflict_do_update(
            index_elements=[table.c.doc_type, table.c.item_id],
            set_={
                "source": insert_statement.excluded.source,
                "canonical_url": insert_statement.excluded.canonical_url,
                "title": insert_statement.excluded.title,
                "published_at": insert_statement.excluded.published_at,
                "updated_at": insert_statement.excluded.updated_at,
            },
        ),
        rows,
    )
    item_ids = list(dict.fromkeys(int(row["item_id"]) for row in rows))
    result = session.connection().execute(
        sa_select(table.c.id, table.c.item_id).where(
            table.c.doc_type == "item",
            table.c.item_id.in_(item_ids),
        )
    )
    doc_ids_by_item_id = {
        int(item_id): int(doc_id)
        for doc_id, item_id in result
        if doc_id is not None and item_id is not None
    }
    return doc_ids_by_item_id, docs_upserted


def _item_id_value(item: Any) -> int:
    raw_item_id = getattr(item, "id", None)
    return int(raw_item_id) if raw_item_id is not None else 0


def _item_event_at(item: Any) -> Any:
    return getattr(item, "published_at", None) or getattr(item, "created_at", None)


def _existing_chunks_by_key(
    *, session: Any, doc_ids: list[int]
) -> tuple[list[_ExistingChunk], dict[tuple[int, int], _ExistingChunk]]:
    table = cast(Any, DocumentChunk).__table__
    if not doc_ids:
        return [], {}
    rows = session.connection().execute(
        sa_select(
            table.c.id,
            table.c.doc_id,
            table.c.chunk_index,
            table.c.kind,
            table.c.text_hash,
        ).where(
            table.c.doc_id.in_(doc_ids),
            table.c.kind.in_(["summary", "content", "meta"]),
        )
    )
    existing_chunks = [
        _ExistingChunk(
            id=int(chunk_id),
            doc_id=int(doc_id),
            chunk_index=int(chunk_index),
            kind=str(kind),
            text_hash=str(text_hash or ""),
        )
        for chunk_id, doc_id, chunk_index, kind, text_hash in rows
        if chunk_id is not None and doc_id is not None and chunk_index is not None
    ]
    existing_chunks_by_key = {
        (chunk.doc_id, chunk.chunk_index): chunk for chunk in existing_chunks
    }
    return existing_chunks, existing_chunks_by_key


def _resolved_pair_doc_id(
    *,
    item: Any,
    doc_ids_by_item_id: dict[int, int],
) -> int | None:
    raw_item_id = getattr(item, "id", None)
    if raw_item_id is None:
        return None
    doc_id = doc_ids_by_item_id.get(int(raw_item_id))
    if doc_id is None:
        return None
    return int(doc_id)


def _target_rows_for_pairs(
    *,
    request: _TargetRowsForPairsRequest,
) -> tuple[dict[tuple[int, int], dict[str, Any]], dict[int, int | None], int]:
    target_rows: dict[tuple[int, int], dict[str, Any]] = {}
    content_cutoffs: dict[int, int | None] = {}
    content_chunks_upserted = 0
    for item, analysis in request.pairs:
        pair_rows = _target_rows_for_pair(
            request=_TargetRowsForPairRequest(
                trends_module=request.trends_module,
                item=item,
                analysis=analysis,
                doc_ids_by_item_id=request.doc_ids_by_item_id,
                texts_by_item_id=request.texts_by_item_id,
                content_types=request.content_types,
                content_chunk_chars=request.content_chunk_chars,
                max_content_chunks_per_item=request.max_content_chunks_per_item,
            )
        )
        if pair_rows is None:
            continue
        doc_id, content_rows, max_written_index, added_chunks = pair_rows
        target_rows[(doc_id, 0)] = _summary_target_row(doc_id=doc_id, analysis=analysis)
        target_rows[(doc_id, request.trends_module._ITEM_META_CHUNK_INDEX)] = (
            _meta_target_row(
                trends_module=request.trends_module,
                doc_id=doc_id,
                item=item,
                analysis=analysis,
            )
        )
        target_rows.update(content_rows)
        content_chunks_upserted += added_chunks
        content_cutoffs[doc_id] = max_written_index
    return target_rows, content_cutoffs, content_chunks_upserted


def _summary_target_row(*, doc_id: int, analysis: Any) -> dict[str, Any]:
    summary_text = str(getattr(analysis, "summary", "") or "").strip()
    if not summary_text:
        raise ValueError("chunk text must not be empty")
    return {
        "doc_id": doc_id,
        "chunk_index": 0,
        "kind": "summary",
        "text": summary_text,
        "start_char": 0,
        "end_char": None,
        "text_hash": sha256_hex(summary_text),
        "source_content_type": "analysis_summary",
    }


def _meta_target_row(
    *,
    trends_module: Any,
    doc_id: int,
    item: Any,
    analysis: Any,
) -> dict[str, Any]:
    meta_text = trends_module._item_meta_chunk_text(item=item, analysis=analysis)
    return {
        "doc_id": doc_id,
        "chunk_index": trends_module._ITEM_META_CHUNK_INDEX,
        "kind": "meta",
        "text": meta_text,
        "start_char": 0,
        "end_char": None,
        "text_hash": sha256_hex(meta_text),
        "source_content_type": "analysis_meta_json",
    }


def _chosen_content_text(
    *,
    item_id: int,
    texts_by_item_id: dict[int, dict[str, str | None]],
    content_types: list[str],
) -> tuple[str | None, str | None]:
    texts = texts_by_item_id.get(item_id, {})
    for content_type in content_types:
        candidate = texts.get(content_type)
        if isinstance(candidate, str) and candidate.strip():
            return candidate, content_type
    return None, None


def _content_segment_rows(
    *,
    request: _ContentSegmentRowsRequest,
) -> tuple[dict[tuple[int, int], dict[str, Any]], int | None, int]:
    rows: dict[tuple[int, int], dict[str, Any]] = {}
    max_written_index: int | None = None
    for seg_idx, (start_char, end_char, seg) in enumerate(
        request.trends_module._chunk_text_segments(
            request.chosen,
            chunk_chars=request.content_chunk_chars,
            max_segments=request.max_content_chunks_per_item,
        ),
        start=1,
    ):
        rows[(request.doc_id, seg_idx)] = {
            "doc_id": request.doc_id,
            "chunk_index": seg_idx,
            "kind": "content",
            "text": seg,
            "start_char": start_char,
            "end_char": end_char,
            "text_hash": sha256_hex(seg),
            "source_content_type": request.chosen_type,
        }
        max_written_index = seg_idx
    return rows, max_written_index, len(rows)


def _target_rows_for_pair(
    *,
    request: _TargetRowsForPairRequest,
) -> tuple[int, dict[tuple[int, int], dict[str, Any]], int | None, int] | None:
    doc_id = _resolved_pair_doc_id(
        item=request.item,
        doc_ids_by_item_id=request.doc_ids_by_item_id,
    )
    if doc_id is None:
        return None
    chosen, chosen_type = _chosen_content_text(
        item_id=int(getattr(request.item, "id")),
        texts_by_item_id=request.texts_by_item_id,
        content_types=request.content_types,
    )
    if not chosen or chosen_type is None:
        return doc_id, {}, None, 0
    content_rows, max_written_index, added_chunks = _content_segment_rows(
        request=_ContentSegmentRowsRequest(
            trends_module=request.trends_module,
            doc_id=doc_id,
            chosen=chosen,
            chosen_type=chosen_type,
            content_chunk_chars=request.content_chunk_chars,
            max_content_chunks_per_item=request.max_content_chunks_per_item,
        )
    )
    return doc_id, content_rows, max_written_index, added_chunks


def _changed_chunks(
    *,
    existing_chunks_by_key: dict[tuple[int, int], _ExistingChunk],
    target_rows: dict[tuple[int, int], dict[str, Any]],
) -> list[dict[str, Any]]:
    changed_chunks: list[dict[str, Any]] = []
    for (doc_id, chunk_index), payload in target_rows.items():
        existing = existing_chunks_by_key.get((doc_id, chunk_index))
        if existing is not None and existing.text_hash == str(payload["text_hash"]):
            continue
        changed_chunks.append(payload)
    return changed_chunks


def _stale_content_chunks(
    *,
    existing_chunks: list[_ExistingChunk],
    content_cutoffs: dict[int, int | None],
) -> list[_ExistingChunk]:
    stale_chunks: list[_ExistingChunk] = []
    for chunk in existing_chunks:
        if chunk.kind.strip().lower() != "content":
            continue
        max_written_index = content_cutoffs.get(chunk.doc_id)
        threshold = 1 if max_written_index is None else max_written_index + 1
        if chunk.chunk_index >= threshold:
            stale_chunks.append(chunk)
    return stale_chunks


def _sync_chunk_indexes(
    *,
    session: Any,
    changed_chunks: list[dict[str, Any]],
    stale_chunks: list[_ExistingChunk],
) -> None:
    conn = session.connection()
    _upsert_changed_chunks(conn=conn, changed_chunks=changed_chunks)
    changed_chunk_ids = _chunk_ids_by_key(
        conn=conn,
        changed_keys=[
            (int(chunk["doc_id"]), int(chunk["chunk_index"]))
            for chunk in changed_chunks
        ],
    )
    changed_fts_rows = _changed_fts_rows(
        changed_chunks=changed_chunks,
        chunk_ids_by_key=changed_chunk_ids,
    )
    _replace_changed_chunk_fts_rows(conn=conn, changed_fts_rows=changed_fts_rows)
    stale_ids = _stale_chunk_ids(stale_chunks)
    _delete_stale_chunk_side_tables(conn=conn, stale_ids=stale_ids)
    _delete_stale_chunks(conn=conn, stale_ids=stale_ids)


def _upsert_changed_chunks(*, conn: Any, changed_chunks: list[dict[str, Any]]) -> None:
    if not changed_chunks:
        return
    table = cast(Any, DocumentChunk).__table__
    now = utc_now()
    rows = [dict(chunk, created_at=now) for chunk in changed_chunks]
    insert_statement = sqlite_insert(table)
    conn.execute(
        insert_statement.on_conflict_do_update(
            index_elements=[table.c.doc_id, table.c.chunk_index],
            set_={
                "kind": insert_statement.excluded.kind,
                "text": insert_statement.excluded.text,
                "start_char": insert_statement.excluded.start_char,
                "end_char": insert_statement.excluded.end_char,
                "text_hash": insert_statement.excluded.text_hash,
                "source_content_type": insert_statement.excluded.source_content_type,
            },
        ),
        rows,
    )


def _chunk_ids_by_key(
    *, conn: Any, changed_keys: list[tuple[int, int]]
) -> dict[tuple[int, int], int]:
    if not changed_keys:
        return {}
    table = cast(Any, DocumentChunk).__table__
    doc_ids = list(dict.fromkeys(doc_id for doc_id, _chunk_index in changed_keys))
    changed_key_set = set(changed_keys)
    rows = conn.execute(
        sa_select(table.c.id, table.c.doc_id, table.c.chunk_index).where(
            table.c.doc_id.in_(doc_ids)
        )
    )
    return {
        (int(doc_id), int(chunk_index)): int(chunk_id)
        for chunk_id, doc_id, chunk_index in rows
        if chunk_id is not None
        and doc_id is not None
        and chunk_index is not None
        and (int(doc_id), int(chunk_index)) in changed_key_set
    }


def _changed_fts_rows(
    *,
    changed_chunks: list[dict[str, Any]],
    chunk_ids_by_key: dict[tuple[int, int], int],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for chunk in changed_chunks:
        doc_id = int(chunk["doc_id"])
        chunk_index = int(chunk["chunk_index"])
        chunk_id = chunk_ids_by_key.get((doc_id, chunk_index))
        if chunk_id is None or _chunk_is_meta(chunk):
            continue
        rows.append(
            {
                "rowid": chunk_id,
                "text": str(chunk["text"]),
                "doc_id": doc_id,
                "chunk_index": chunk_index,
                "kind": str(chunk["kind"]),
            }
        )
    return rows


def _chunk_is_meta(chunk: dict[str, Any]) -> bool:
    return str(chunk.get("kind") or "").strip().lower() == "meta"


def _replace_changed_chunk_fts_rows(
    *,
    conn: Any,
    changed_fts_rows: list[dict[str, Any]],
) -> None:
    if not changed_fts_rows:
        return
    conn.execute(
        text("DELETE FROM chunk_fts WHERE rowid = :rowid"),
        [{"rowid": row["rowid"]} for row in changed_fts_rows],
    )
    conn.execute(
        text(
            "INSERT INTO chunk_fts(rowid, text, doc_id, chunk_index, kind) "
            "VALUES(:rowid, :text, :doc_id, :chunk_index, :kind)"
        ),
        changed_fts_rows,
    )


def _stale_chunk_ids(stale_chunks: list[_ExistingChunk]) -> list[int]:
    return [chunk.id for chunk in stale_chunks if chunk.id > 0]


def _delete_stale_chunk_side_tables(*, conn: Any, stale_ids: list[int]) -> None:
    if not stale_ids:
        return
    conn.execute(
        text("DELETE FROM chunk_embeddings WHERE chunk_id = :chunk_id"),
        [{"chunk_id": chunk_id} for chunk_id in stale_ids],
    )
    conn.execute(
        text("DELETE FROM chunk_fts WHERE rowid = :rowid"),
        [{"rowid": chunk_id} for chunk_id in stale_ids],
    )


def _delete_stale_chunks(*, conn: Any, stale_ids: list[int]) -> None:
    if not stale_ids:
        return
    conn.execute(
        text("DELETE FROM document_chunks WHERE id = :chunk_id"),
        [{"chunk_id": chunk_id} for chunk_id in stale_ids],
    )


def index_items_as_documents_batched_impl(
    *,
    repository: Any,
    pairs: list[tuple[Any, Any]],
    content_types: list[str],
    content_chunk_chars: int,
    max_content_chunks_per_item: int,
) -> dict[str, int]:
    from recoleta import trends as trends_module

    item_ids = _item_ids_from_pairs(pairs)
    if not item_ids:
        return {
            "docs_upserted": 0,
            "chunks_upserted": 0,
            "content_chunks_upserted": 0,
            "content_chunks_deleted": 0,
        }
    texts_by_item_id = trends_module._load_latest_content_texts_for_items(
        repository=repository,
        item_ids=item_ids,
        content_types=content_types,
    )
    with Session(repository.engine) as session:
        doc_ids_by_item_id, docs_upserted = _upsert_item_documents(
            session=session,
            pairs=pairs,
        )
        doc_ids = list(doc_ids_by_item_id.values())
        existing_chunks, existing_chunks_by_key = _existing_chunks_by_key(
            session=session,
            doc_ids=doc_ids,
        )
        target_rows, content_cutoffs, content_chunks_upserted = _target_rows_for_pairs(
            request=_TargetRowsForPairsRequest(
                trends_module=trends_module,
                pairs=pairs,
                doc_ids_by_item_id=doc_ids_by_item_id,
                texts_by_item_id=texts_by_item_id,
                content_types=content_types,
                content_chunk_chars=content_chunk_chars,
                max_content_chunks_per_item=max_content_chunks_per_item,
            )
        )
        changed_chunks = _changed_chunks(
            existing_chunks_by_key=existing_chunks_by_key,
            target_rows=target_rows,
        )
        stale_chunks = _stale_content_chunks(
            existing_chunks=existing_chunks,
            content_cutoffs=content_cutoffs,
        )
        _sync_chunk_indexes(
            session=session,
            changed_chunks=changed_chunks,
            stale_chunks=stale_chunks,
        )
        trends_module._commit_trend_session(repository=repository, session=session)
        return {
            "docs_upserted": docs_upserted,
            "chunks_upserted": len(target_rows),
            "content_chunks_upserted": content_chunks_upserted,
            "content_chunks_deleted": len(stale_chunks),
        }


def index_items_as_documents_impl(
    *, request: IndexItemsAsDocumentsRequest
) -> dict[str, Any]:
    from recoleta import trends as trends_module

    log = logger.bind(module="trends.index_items", run_id=request.run_id)
    started = time.perf_counter()
    pairs = request.repository.list_analyzed_items_in_period(
        period_start=request.period_start,
        period_end=request.period_end,
        limit=request.limit,
        llm_model=request.llm_model,
    )
    pairs, filtered_out_total = trends_module._filter_pairs_by_min_relevance(
        pairs,
        min_relevance_score=request.min_relevance_score,
    )
    keep_item_ids = {
        int(getattr(item, "id") or 0)
        for item, _analysis in pairs
        if getattr(item, "id", None) is not None
    }
    docs_deleted = trends_module._prune_item_documents_for_period(
        repository=request.repository,
        period_start=request.period_start,
        period_end=request.period_end,
        keep_item_ids=keep_item_ids,
    )
    content_types = [
        "pdf_text",
        "html_maintext",
        "html_document_md",
        "html_document",
        "latex_source",
    ]
    write_mode = "batched"
    try:
        write_stats = trends_module._index_items_as_documents_batched(
            repository=request.repository,
            pairs=pairs,
            content_types=content_types,
            content_chunk_chars=request.content_chunk_chars,
            max_content_chunks_per_item=request.max_content_chunks_per_item,
        )
    except Exception as exc:  # noqa: BLE001
        write_mode = "itemwise_fallback"
        log.warning(
            "Batch document indexing failed; falling back to itemwise writes "
            "error_type={} error={}",
            type(exc).__name__,
            str(exc),
        )
        write_stats = trends_module._index_items_as_documents_itemwise(
            repository=request.repository,
            pairs=pairs,
            content_types=content_types,
            content_chunk_chars=request.content_chunk_chars,
            max_content_chunks_per_item=request.max_content_chunks_per_item,
            log=log,
        )
    elapsed_ms = int((time.perf_counter() - started) * 1000)
    stats = {
        "items_total": len(pairs),
        "items_filtered_out": filtered_out_total,
        "docs_upserted": write_stats["docs_upserted"],
        "docs_deleted": docs_deleted,
        "chunks_upserted": write_stats["chunks_upserted"],
        "content_chunks_upserted": write_stats["content_chunks_upserted"],
        "content_chunks_deleted": write_stats["content_chunks_deleted"],
        "write_mode": write_mode,
        "duration_ms": elapsed_ms,
    }
    log.info("Index items done stats={}", stats)
    return stats


def semantic_search_summaries_in_period_impl(
    *, request: SemanticSearchRequest
) -> list[Any]:
    from recoleta import trends as trends_module
    from recoleta.rag.semantic_search import (
        semantic_search_summaries_in_period as _semantic_search,
    )
    from recoleta.rag.vector_store import LanceVectorStore, embedding_table_name

    store = LanceVectorStore(
        db_dir=Path(request.lancedb_dir),
        table_name=embedding_table_name(
            embedding_model=request.embedding_model,
            embedding_dimensions=request.embedding_dimensions,
        ),
    )
    hits = _semantic_search(
        repository=request.repository,
        vector_store=store,
        run_id=request.run_id,
        doc_type=request.doc_type,
        granularity=request.granularity,
        period_start=request.period_start,
        period_end=request.period_end,
        query=request.query,
        embedding_model=request.embedding_model,
        embedding_dimensions=request.embedding_dimensions,
        max_batch_inputs=request.max_batch_inputs,
        max_batch_chars=request.max_batch_chars,
        embedding_failure_mode=request.embedding_failure_mode,
        embedding_max_errors=request.embedding_max_errors,
        limit=request.limit,
        corpus_limit=request.corpus_limit,
        metric_namespace=request.metric_namespace,
        llm_connection=request.llm_connection,
    )
    return [
        trends_module.SemanticSearchHit(
            chunk_id=hit.chunk_id,
            doc_id=hit.doc_id,
            chunk_index=hit.chunk_index,
            score=hit.score,
            text_preview=hit.text_preview,
        )
        for hit in hits
    ]


def generate_trend_via_tools_impl(
    *, request: GenerateTrendRequest
) -> tuple[Any, dict[str, Any] | None]:
    from recoleta.rag.agent import generate_trend_payload
    from recoleta.rag.vector_store import LanceVectorStore, embedding_table_name

    store = LanceVectorStore(
        db_dir=Path(request.lancedb_dir),
        table_name=embedding_table_name(
            embedding_model=request.embedding_model,
            embedding_dimensions=request.embedding_dimensions,
        ),
    )
    generate_trend_payload_any = cast(Any, generate_trend_payload)
    return generate_trend_payload_any(
        repository=request.repository,
        vector_store=store,
        run_id=request.run_id,
        llm_model=request.llm_model,
        output_language=request.output_language,
        embedding_model=request.embedding_model,
        embedding_dimensions=request.embedding_dimensions,
        embedding_batch_max_inputs=request.embedding_batch_max_inputs,
        embedding_batch_max_chars=request.embedding_batch_max_chars,
        embedding_failure_mode=request.embedding_failure_mode,
        embedding_max_errors=request.embedding_max_errors,
        granularity=request.granularity,
        period_start=request.period_start,
        period_end=request.period_end,
        corpus_doc_type=request.corpus_doc_type,
        corpus_granularity=request.corpus_granularity,
        overview_pack_md=request.overview_pack_md,
        history_pack_md=request.history_pack_md,
        rag_sources=request.rag_sources,
        ranking_n=request.ranking_n,
        rep_source_doc_type=request.rep_source_doc_type,
        evolution_max_signals=request.evolution_max_signals,
        include_debug=request.include_debug,
        metric_namespace=request.metric_namespace,
        llm_connection=request.llm_connection,
    )
