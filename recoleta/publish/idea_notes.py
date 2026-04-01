from __future__ import annotations

from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from typing import TYPE_CHECKING, Any

import yaml

from recoleta.presentation import (
    build_idea_presentation_v1,
    idea_display_labels,
    presentation_sidecar_path,
    resolve_presentation_language_code,
    write_presentation_sidecar,
)
from recoleta.publish.item_notes import resolve_item_note_href
from recoleta.publish.trend_notes import resolve_trend_note_href
from recoleta.publish.trend_render_shared import _trend_date_token
from recoleta.provenance import build_projection_provenance

if TYPE_CHECKING:
    from recoleta.passes.trend_ideas import TrendIdeasPayload

__all__ = [
    "resolve_ideas_note_path",
    "write_markdown_ideas_note",
    "write_obsidian_ideas_note",
]


def resolve_ideas_note_path(
    *,
    note_dir: Path,
    granularity: str,
    period_start: datetime,
) -> Path:
    token = _trend_date_token(granularity=granularity, period_start=period_start)
    return note_dir / f"{granularity}--{token}--ideas.md"


def _sanitize_obsidian_tag(value: str) -> str:
    raw = str(value or "").strip()
    if not raw:
        return ""
    normalized = "".join(
        ch if (ch.isalnum() or ch in {"-", "_", "/"}) else "-" for ch in raw
    )
    while "--" in normalized:
        normalized = normalized.replace("--", "-")
    normalized = normalized.strip("-")
    return normalized.lower()


def _format_evidence_ref(
    *,
    repository: Any,
    root_dir: Path,
    note_dir: Path,
    ref: Any,
    show_chunk_index: bool = False,
) -> str:
    try:
        doc_id = int(getattr(ref, "doc_id"))
    except Exception:
        return "Unknown evidence"
    chunk_index = 0
    if show_chunk_index:
        try:
            chunk_index = int(getattr(ref, "chunk_index"))
        except Exception:
            return "Unknown evidence"
    doc = repository.get_document(doc_id=doc_id)
    reason = str(getattr(ref, "reason", "") or "").strip()
    suffix = f" (chunk {chunk_index})" if show_chunk_index and chunk_index > 0 else ""
    if doc is None:
        base = f"Document {doc_id}{suffix}"
        return f"{base}: {reason}" if reason else base

    title = str(getattr(doc, "title", "") or "").strip() or f"Document {doc_id}"
    href: str | None = None
    doc_type = str(getattr(doc, "doc_type", "") or "").strip().lower()
    if doc_type == "item":
        raw_item_id = getattr(doc, "item_id", None)
        try:
            item_id = int(raw_item_id) if raw_item_id is not None else 0
        except Exception:
            item_id = 0
        item = repository.get_item(item_id=item_id) if item_id > 0 else None
        if item is not None:
            href = resolve_item_note_href(
                note_dir=root_dir / "Inbox",
                from_dir=note_dir,
                item_id=item_id,
                title=str(getattr(item, "title", "") or ""),
                canonical_url=str(getattr(item, "canonical_url", "") or ""),
                published_at=getattr(item, "published_at", None),
            )
    elif doc_type == "trend":
        raw_granularity = str(getattr(doc, "granularity", "") or "").strip().lower()
        period_start = getattr(doc, "period_start", None)
        if raw_granularity and isinstance(period_start, datetime):
            href = resolve_trend_note_href(
                note_dir=root_dir / "Trends",
                from_dir=note_dir,
                trend_doc_id=doc_id,
                granularity=raw_granularity,
                period_start=period_start,
            )
    if href is None:
        raw_url = str(getattr(doc, "canonical_url", "") or "").strip()
        if raw_url:
            href = raw_url

    rendered = f"[{title}]({href}){suffix}" if href else f"{title}{suffix}"
    return f"{rendered}: {reason}" if reason else rendered


def _merge_evidence_reasons(refs: list[Any]) -> list[str]:
    seen_reasons: set[str] = set()
    merged_reasons: list[str] = []
    for ref in refs:
        reason = " ".join(str(getattr(ref, "reason", "") or "").split()).strip()
        if not reason or reason in seen_reasons:
            continue
        seen_reasons.add(reason)
        merged_reasons.append(reason)
    return merged_reasons


def _display_evidence_refs(refs: list[Any]) -> list[tuple[Any, list[str]]]:
    ordered: list[tuple[str, Any]] = []
    grouped: dict[int, list[Any]] = {}
    for ref in refs:
        try:
            doc_id = int(getattr(ref, "doc_id"))
        except Exception:
            ordered.append(("raw", ref))
            continue
        if doc_id <= 0:
            ordered.append(("raw", ref))
            continue
        if doc_id not in grouped:
            grouped[doc_id] = []
            ordered.append(("doc", doc_id))
        grouped[doc_id].append(ref)

    display_refs: list[tuple[Any, list[str]]] = []
    for kind, value in ordered:
        if kind == "raw":
            display_refs.append((value, _merge_evidence_reasons([value])))
            continue
        refs_for_doc = grouped.get(int(value), [])
        if not refs_for_doc:
            continue
        display_refs.append(
            (
                SimpleNamespace(
                    doc_id=int(value),
                    chunk_index=0,
                    reason=None,
                ),
                _merge_evidence_reasons(refs_for_doc),
            )
        )
    return display_refs


def _render_evidence_ref_lines(
    *,
    repository: Any,
    root_dir: Path,
    note_dir: Path,
    ref: Any,
    reasons: list[str],
) -> list[str]:
    rendered = _format_evidence_ref(
        repository=repository,
        root_dir=root_dir,
        note_dir=note_dir,
        ref=ref,
        show_chunk_index=False,
    )
    if not reasons:
        return [f"- {rendered}"]
    if len(reasons) == 1:
        return [f"- {rendered}: {reasons[0]}"]
    lines = [f"- {rendered}"]
    lines.extend(f"  - {reason}" for reason in reasons)
    return lines


def _enrich_evidence_ref(
    *,
    repository: Any,
    root_dir: Path,
    note_dir: Path,
    ref: Any,
) -> Any:
    doc_id = getattr(ref, "doc_id", None)
    chunk_index = getattr(ref, "chunk_index", 0)
    reason = getattr(ref, "reason", None)
    title = getattr(ref, "title", None)
    href = getattr(ref, "href", None)
    authors = list(getattr(ref, "authors", []) or [])
    source = getattr(ref, "source", None)
    score = getattr(ref, "score", None)

    try:
        doc_id_int = int(doc_id) if doc_id is not None else 0
    except Exception:
        doc_id_int = 0
    try:
        chunk_index_int = int(chunk_index or 0)
    except Exception:
        chunk_index_int = 0

    doc = repository.get_document(doc_id=doc_id_int) if doc_id_int > 0 else None
    if doc is not None:
        resolved_title = str(getattr(doc, "title", "") or "").strip()
        if resolved_title:
            title = resolved_title
        doc_type = str(getattr(doc, "doc_type", "") or "").strip().lower()
        if doc_type == "item":
            raw_item_id = getattr(doc, "item_id", None)
            try:
                item_id = int(raw_item_id) if raw_item_id is not None else 0
            except Exception:
                item_id = 0
            item = repository.get_item(item_id=item_id) if item_id > 0 else None
            if item is not None:
                href = resolve_item_note_href(
                    note_dir=root_dir / "Inbox",
                    from_dir=note_dir,
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
                source = str(getattr(item, "source", "") or "").strip() or source
        elif doc_type == "trend":
            raw_granularity = str(getattr(doc, "granularity", "") or "").strip().lower()
            period_start = getattr(doc, "period_start", None)
            if raw_granularity and isinstance(period_start, datetime):
                href = resolve_trend_note_href(
                    note_dir=root_dir / "Trends",
                    from_dir=note_dir,
                    trend_doc_id=doc_id_int,
                    granularity=raw_granularity,
                    period_start=period_start,
                )
        if href is None:
            href = str(getattr(doc, "canonical_url", "") or "").strip() or href

    return SimpleNamespace(
        doc_id=doc_id_int,
        chunk_index=chunk_index_int,
        reason=reason,
        title=title,
        href=href,
        authors=authors,
        source=source,
        score=score,
    )


def _presentation_ready_ideas(
    *,
    repository: Any,
    root_dir: Path,
    note_dir: Path,
    payload: TrendIdeasPayload,
) -> list[Any]:
    prepared: list[Any] = []
    for idea in _normalized_payload_ideas(payload):
        prepared.append(
            SimpleNamespace(
                title=idea.title,
                kind=idea.kind,
                thesis=idea.thesis,
                why_now=idea.why_now,
                what_changed=idea.what_changed,
                user_or_job=idea.user_or_job,
                validation_next_step=idea.validation_next_step,
                time_horizon=idea.time_horizon,
                evidence_refs=[
                    _enrich_evidence_ref(
                        repository=repository,
                        root_dir=root_dir,
                        note_dir=note_dir,
                        ref=ref,
                    )
                    for ref in list(idea.evidence_refs or [])
                ],
            )
        )
    return prepared


def _format_presentation_evidence_line(entry: dict[str, Any]) -> str:
    title = str(entry.get("title") or "").strip()
    doc_id = entry.get("doc_id")
    if not title and doc_id is not None:
        title = f"Document {doc_id}"
    href = str(entry.get("href") or entry.get("url") or "").strip()
    if title and href:
        return f"[{title}]({href})"
    if title:
        return title
    return "Unknown evidence"


def _render_presentation_evidence_lines(entry: dict[str, Any]) -> list[str]:
    rendered = _format_presentation_evidence_line(entry)
    reasons = [
        " ".join(str(reason).split()).strip()
        for reason in list(entry.get("reasons") or [])
        if " ".join(str(reason).split()).strip()
    ]
    if not reasons:
        reason = " ".join(str(entry.get("reason") or "").split()).strip()
        if reason:
            reasons = [reason]
    if not reasons:
        return [f"- {rendered}"]
    if len(reasons) == 1:
        return [f"- {rendered}: {reasons[0]}"]
    return [f"- {rendered}", *[f"  - {reason}" for reason in reasons]]


def _normalized_payload_ideas(payload: TrendIdeasPayload, *, max_count: int = 3) -> list[Any]:
    return list(payload.ideas or [])[:max_count]


def _render_ideas_note_lines(
    *,
    pass_output_id: int | None,
    upstream_pass_output_id: int | None,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
    run_id: str,
    status: str,
    title: str,
    topics: list[str] | None = None,
    pass_kind: str = "trend_ideas",
    upstream_pass_kind: str | None = "trend_synthesis",
    language_code: str | None = None,
    display_language_code: str | None = None,
    presentation: dict[str, Any],
) -> list[str]:
    base_tags = ["recoleta/ideas"]
    for topic in list(topics or []):
        normalized = _sanitize_obsidian_tag(topic)
        if normalized:
            base_tags.append(f"topic/{normalized}")
    seen_tags: set[str] = set()
    tags = [tag for tag in base_tags if not (tag in seen_tags or seen_tags.add(tag))]
    frontmatter = {
        "kind": "ideas",
        "granularity": granularity,
        "period_start": period_start.isoformat(),
        "period_end": period_end.isoformat(),
        "run_id": run_id,
        "status": status,
        "topics": [str(topic).strip() for topic in list(topics or []) if str(topic).strip()],
        "tags": tags,
    }
    normalized_language_code = str(language_code or "").strip()
    if normalized_language_code:
        frontmatter["language_code"] = normalized_language_code
    if pass_output_id is not None:
        frontmatter.update(
            build_projection_provenance(
                pass_output_id=pass_output_id,
                pass_kind=str(pass_kind or "").strip() or "trend_ideas",
                upstream_pass_output_id=upstream_pass_output_id,
                upstream_pass_kind=(
                    str(upstream_pass_kind or "").strip() or None
                    if upstream_pass_output_id is not None
                    else None
                ),
            ).model_dump(mode="json", exclude_none=True)
        )

    lines: list[str] = [
        "---",
        yaml.safe_dump(frontmatter, sort_keys=False).strip(),
        "---",
        "",
        f"# {title or 'Ideas'}",
        "",
        f"## {presentation['display_labels']['summary']}",
        str(presentation["content"].get("summary") or "").strip() or "(empty)",
    ]

    opportunities = list(presentation["content"].get("opportunities") or [])
    labels = presentation["display_labels"]
    if display_language_code is not None:
        labels = idea_display_labels(language_code=display_language_code)
    if opportunities:
        lines.extend(["", f"## {labels['opportunities']}"])
        for opportunity in opportunities:
            tier_label = (
                labels["best_bet"]
                if str(opportunity.get("tier") or "").strip() == "best_bet"
                else labels["alternate"]
            )
            lines.extend(
                [
                    "",
                    f"### {tier_label}: {opportunity['title']}",
                    f"- {labels['type']}: {opportunity['display_kind']}",
                    f"- {labels['horizon']}: {opportunity['display_time_horizon']}",
                    f"- {labels['role']}: {opportunity['role']}",
                    "",
                    f"**{labels['thesis']}.** {opportunity['thesis']}",
                    "",
                    f"**{labels['why_now']}.** {opportunity['why_now']}",
                    "",
                    f"**{labels['what_changed']}.** {opportunity['what_changed']}",
                    "",
                    f"**{labels['validation_next_step']}.** {opportunity['validation_next_step']}",
                ]
            )
            evidence = list(opportunity.get("evidence") or [])
            if evidence:
                lines.extend(["", f"#### {labels['evidence']}"])
                for entry in evidence:
                    if not isinstance(entry, dict):
                        continue
                    lines.extend(_render_presentation_evidence_lines(entry))
    return lines


def _write_ideas_note(
    *,
    repository: Any,
    root_dir: Path,
    note_dir: Path,
    pass_output_id: int | None,
    upstream_pass_output_id: int | None,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
    run_id: str,
    status: str,
    payload: TrendIdeasPayload,
    topics: list[str] | None = None,
    pass_kind: str = "trend_ideas",
    upstream_pass_kind: str | None = "trend_synthesis",
    output_language: str | None = None,
    language_code: str | None = None,
    emit_presentation_sidecar: bool = False,
) -> Path:
    note_dir.mkdir(parents=True, exist_ok=True)
    resolved_language_code = resolve_presentation_language_code(
        language_code=language_code,
        output_language=output_language,
    )
    resolved_display_language_code = (
        resolve_presentation_language_code(language_code=language_code) or "en"
    )
    note_path = resolve_ideas_note_path(
        note_dir=note_dir,
        granularity=granularity,
        period_start=period_start,
    )
    presentation = build_idea_presentation_v1(
        source_markdown_path=f"{note_dir.name}/{note_path.name}",
        title=str(payload.title or "").strip(),
        summary_md=str(payload.summary_md or "").strip(),
        ideas=_presentation_ready_ideas(
            repository=repository,
            root_dir=root_dir,
            note_dir=note_dir,
            payload=payload,
        ),
        language_code=resolved_language_code,
        display_language_code=resolved_display_language_code,
    )
    lines = _render_ideas_note_lines(
        pass_output_id=pass_output_id,
        upstream_pass_output_id=upstream_pass_output_id,
        granularity=granularity,
        period_start=period_start,
        period_end=period_end,
        run_id=run_id,
        status=status,
        title=str(payload.title or "").strip(),
        topics=topics,
        pass_kind=pass_kind,
        upstream_pass_kind=upstream_pass_kind,
        language_code=resolved_language_code,
        display_language_code=resolved_display_language_code,
        presentation=presentation,
    )
    note_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    if emit_presentation_sidecar:
        try:
            write_presentation_sidecar(note_path=note_path, presentation=presentation)
        except Exception:
            note_path.unlink(missing_ok=True)
            presentation_sidecar_path(note_path=note_path).unlink(missing_ok=True)
            raise
    return note_path


def write_markdown_ideas_note(
    *,
    repository: Any,
    output_dir: Path,
    pass_output_id: int | None,
    upstream_pass_output_id: int | None,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
    run_id: str,
    status: str,
    payload: TrendIdeasPayload,
    topics: list[str] | None = None,
    pass_kind: str = "trend_ideas",
    upstream_pass_kind: str | None = "trend_synthesis",
    output_language: str | None = None,
    language_code: str | None = None,
) -> Path:
    root_dir = output_dir.expanduser().resolve()
    note_dir = root_dir / "Ideas"
    return _write_ideas_note(
        repository=repository,
        root_dir=root_dir,
        note_dir=note_dir,
        pass_output_id=pass_output_id,
        upstream_pass_output_id=upstream_pass_output_id,
        granularity=granularity,
        period_start=period_start,
        period_end=period_end,
        run_id=run_id,
        status=status,
        payload=payload,
        topics=topics,
        pass_kind=pass_kind,
        upstream_pass_kind=upstream_pass_kind,
        output_language=output_language,
        language_code=language_code,
        emit_presentation_sidecar=True,
    )


def write_obsidian_ideas_note(
    *,
    repository: Any,
    vault_path: Path,
    base_folder: str,
    pass_output_id: int | None,
    upstream_pass_output_id: int | None,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
    run_id: str,
    status: str,
    payload: TrendIdeasPayload,
    topics: list[str] | None = None,
    pass_kind: str = "trend_ideas",
    upstream_pass_kind: str | None = "trend_synthesis",
    output_language: str | None = None,
    language_code: str | None = None,
) -> Path:
    root_dir = vault_path / base_folder
    note_dir = root_dir / "Ideas"
    return _write_ideas_note(
        repository=repository,
        root_dir=root_dir,
        note_dir=note_dir,
        pass_output_id=pass_output_id,
        upstream_pass_output_id=upstream_pass_output_id,
        granularity=granularity,
        period_start=period_start,
        period_end=period_end,
        run_id=run_id,
        status=status,
        payload=payload,
        topics=topics,
        pass_kind=pass_kind,
        upstream_pass_kind=upstream_pass_kind,
        output_language=output_language,
        language_code=language_code,
        emit_presentation_sidecar=False,
    )
