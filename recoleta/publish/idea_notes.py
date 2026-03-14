from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

import yaml

from recoleta.publish.item_notes import resolve_item_note_href
from recoleta.publish.trend_notes import resolve_trend_note_href
from recoleta.publish.trend_render_shared import _trend_date_token

if TYPE_CHECKING:
    from recoleta.passes.trend_ideas import TrendIdeasPayload

__all__ = [
    "resolve_ideas_note_path",
    "write_markdown_ideas_note",
]


def resolve_ideas_note_path(
    *,
    note_dir: Path,
    granularity: str,
    period_start: datetime,
) -> Path:
    token = _trend_date_token(granularity=granularity, period_start=period_start)
    return note_dir / f"{granularity}--{token}--ideas.md"


def _format_evidence_ref(
    *,
    repository: Any,
    output_dir: Path,
    note_dir: Path,
    ref: Any,
) -> str:
    try:
        doc_id = int(getattr(ref, "doc_id"))
        chunk_index = int(getattr(ref, "chunk_index"))
    except Exception:
        return "Unknown evidence"
    doc = repository.get_document(doc_id=doc_id)
    reason = str(getattr(ref, "reason", "") or "").strip()
    suffix = f" (chunk {chunk_index})" if chunk_index > 0 else ""
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
                note_dir=output_dir / "Inbox",
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
                note_dir=output_dir / "Trends",
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


def write_markdown_ideas_note(
    *,
    repository: Any,
    output_dir: Path,
    pass_output_id: int,
    upstream_pass_output_id: int | None,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
    run_id: str,
    status: str,
    payload: TrendIdeasPayload,
    scope: str,
    topics: list[str] | None = None,
) -> Path:
    note_dir = output_dir / "Ideas"
    note_dir.mkdir(parents=True, exist_ok=True)
    note_path = resolve_ideas_note_path(
        note_dir=note_dir,
        granularity=granularity,
        period_start=period_start,
    )
    frontmatter = {
        "kind": "ideas",
        "pass_output_id": int(pass_output_id),
        "trend_pass_output_id": (
            int(upstream_pass_output_id) if upstream_pass_output_id is not None else None
        ),
        "granularity": granularity,
        "period_start": period_start.isoformat(),
        "period_end": period_end.isoformat(),
        "run_id": run_id,
        "status": status,
        "stream": scope,
        "topics": [str(topic).strip() for topic in list(topics or []) if str(topic).strip()],
        "tags": ["recoleta/ideas"],
    }

    lines: list[str] = [
        "---",
        yaml.safe_dump(frontmatter, sort_keys=False).strip(),
        "---",
        "",
        f"# {str(payload.title or '').strip() or 'Ideas'}",
        "",
        "## Summary",
        str(payload.summary_md or "").strip() or "(empty)",
    ]

    if payload.ideas:
        lines.extend(["", "## Opportunities"])
        for idea in payload.ideas:
            lines.extend(
                [
                    "",
                    f"### {idea.title}",
                    f"- Kind: {idea.kind}",
                    f"- Time horizon: {idea.time_horizon}",
                    f"- User/job: {idea.user_or_job}",
                    "",
                    f"**Thesis.** {idea.thesis}",
                    "",
                    f"**Why now.** {idea.why_now}",
                    "",
                    f"**What changed.** {idea.what_changed}",
                    "",
                    f"**Validation next step.** {idea.validation_next_step}",
                ]
            )
            if idea.evidence_refs:
                lines.extend(["", "#### Evidence"])
                for ref in idea.evidence_refs:
                    lines.append(
                        "- "
                        + _format_evidence_ref(
                            repository=repository,
                            output_dir=output_dir,
                            note_dir=note_dir,
                            ref=ref,
                        )
                    )

    note_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return note_path
