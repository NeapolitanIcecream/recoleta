from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from recoleta.publish.item_notes import resolve_item_note_href
from recoleta.publish.trend_notes import resolve_trend_note_href


@dataclass(frozen=True, slots=True)
class IdeasEvidenceContext:
    repository: Any
    root_dir: Path
    note_dir: Path


def _int_or_zero(value: Any) -> int:
    try:
        return int(value)
    except Exception:
        return 0


def _build_item_href(*, ctx: IdeasEvidenceContext, doc: Any) -> tuple[str | None, list[str], str | None]:
    item_id = _int_or_zero(getattr(doc, "item_id", None))
    if item_id <= 0:
        return None, [], None
    item = ctx.repository.get_item(item_id=item_id)
    if item is None:
        return None, [], None
    href = resolve_item_note_href(
        note_dir=ctx.root_dir / "Inbox",
        from_dir=ctx.note_dir,
        item_id=item_id,
        title=str(getattr(item, "title", "") or ""),
        canonical_url=str(getattr(item, "canonical_url", "") or ""),
        published_at=getattr(item, "published_at", None),
    )
    authors = [
        str(author).strip()
        for author in list(getattr(item, "authors", []) or [])
        if str(author).strip()
    ]
    source = str(getattr(item, "source", "") or "").strip() or None
    return href, authors, source


def _build_trend_href(*, ctx: IdeasEvidenceContext, doc: Any, doc_id: int) -> str | None:
    granularity = str(getattr(doc, "granularity", "") or "").strip().lower()
    period_start = getattr(doc, "period_start", None)
    if not granularity or not isinstance(period_start, datetime):
        return None
    return resolve_trend_note_href(
        note_dir=ctx.root_dir / "Trends",
        from_dir=ctx.note_dir,
        trend_doc_id=doc_id,
        granularity=granularity,
        period_start=period_start,
    )


def _resolve_doc_details(*, ctx: IdeasEvidenceContext, doc_id: int) -> tuple[Any | None, str | None]:
    if doc_id <= 0:
        return None, None
    doc = ctx.repository.get_document(doc_id=doc_id)
    if doc is None:
        return None, None
    title = str(getattr(doc, "title", "") or "").strip() or None
    return doc, title


def _resolve_href_and_metadata(
    *,
    ctx: IdeasEvidenceContext,
    doc: Any,
    doc_id: int,
) -> tuple[str | None, list[str], str | None]:
    doc_type = str(getattr(doc, "doc_type", "") or "").strip().lower()
    if doc_type == "item":
        return _build_item_href(ctx=ctx, doc=doc)
    if doc_type == "trend":
        return _build_trend_href(ctx=ctx, doc=doc, doc_id=doc_id), [], None
    href = str(getattr(doc, "canonical_url", "") or "").strip() or None
    return href, [], None


def format_evidence_ref(
    *,
    repository: Any,
    root_dir: Path,
    note_dir: Path,
    ref: Any,
    show_chunk_index: bool = False,
) -> str:
    ctx = IdeasEvidenceContext(repository=repository, root_dir=root_dir, note_dir=note_dir)
    doc_id = _int_or_zero(getattr(ref, "doc_id", None))
    if doc_id <= 0:
        return "Unknown evidence"

    chunk_index = _int_or_zero(getattr(ref, "chunk_index", 0)) if show_chunk_index else 0
    suffix = f" (chunk {chunk_index})" if chunk_index > 0 else ""
    reason = str(getattr(ref, "reason", "") or "").strip()
    doc, title = _resolve_doc_details(ctx=ctx, doc_id=doc_id)
    if doc is None:
        base = f"Document {doc_id}{suffix}"
        return f"{base}: {reason}" if reason else base

    href, _authors, _source = _resolve_href_and_metadata(ctx=ctx, doc=doc, doc_id=doc_id)
    rendered_title = title or f"Document {doc_id}"
    rendered = f"[{rendered_title}]({href}){suffix}" if href else f"{rendered_title}{suffix}"
    return f"{rendered}: {reason}" if reason else rendered


def enrich_evidence_ref(
    *,
    repository: Any,
    root_dir: Path,
    note_dir: Path,
    ref: Any,
) -> Any:
    ctx = IdeasEvidenceContext(repository=repository, root_dir=root_dir, note_dir=note_dir)
    doc_id = _int_or_zero(getattr(ref, "doc_id", None))
    chunk_index = _int_or_zero(getattr(ref, "chunk_index", 0))
    title = getattr(ref, "title", None)
    href = getattr(ref, "href", None)
    authors = list(getattr(ref, "authors", []) or [])
    source = getattr(ref, "source", None)

    doc, resolved_title = _resolve_doc_details(ctx=ctx, doc_id=doc_id)
    if resolved_title:
        title = resolved_title
    if doc is not None:
        resolved_href, resolved_authors, resolved_source = _resolve_href_and_metadata(
            ctx=ctx,
            doc=doc,
            doc_id=doc_id,
        )
        href = resolved_href or href
        if resolved_authors:
            authors = resolved_authors
        if resolved_source:
            source = resolved_source

    return SimpleNamespace(
        doc_id=doc_id,
        chunk_index=chunk_index,
        reason=getattr(ref, "reason", None),
        title=title,
        href=href,
        authors=authors,
        source=source,
        score=getattr(ref, "score", None),
    )


__all__ = ["IdeasEvidenceContext", "enrich_evidence_ref", "format_evidence_ref"]
