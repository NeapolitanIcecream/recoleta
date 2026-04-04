from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable

import yaml

from recoleta.item_summary import normalize_item_summary_markdown


@dataclass(slots=True)
class ItemNoteSpec:
    item_id: int
    title: str
    source: str
    canonical_url: str
    published_at: datetime | None
    authors: list[str]
    topics: list[str]
    relevance_score: float
    run_id: str
    summary: str
    language_code: str | None = None


def render_item_note_lines(*, spec: ItemNoteSpec) -> list[str]:
    normalized_summary = normalize_item_summary_markdown(spec.summary)
    frontmatter = {
        "source": spec.source,
        "url": spec.canonical_url,
        "published_at": spec.published_at.isoformat() if spec.published_at else None,
        "authors": spec.authors,
        "topics": spec.topics,
        "relevance_score": round(spec.relevance_score, 4),
        "run_id": spec.run_id,
    }
    normalized_language_code = str(spec.language_code or "").strip()
    if normalized_language_code:
        frontmatter["language_code"] = normalized_language_code
    return [
        "---",
        yaml.safe_dump(frontmatter, sort_keys=False).strip(),
        "---",
        "",
        f"# {spec.title}",
        "",
        normalized_summary,
        "",
        "## Link",
        f"- [{spec.canonical_url}]({spec.canonical_url})",
        "",
    ]


def write_item_note(
    *,
    note_dir: Path,
    spec: ItemNoteSpec,
    resolve_note_path: Callable[..., Path],
    lines: list[str] | None = None,
) -> Path:
    note_dir.mkdir(parents=True, exist_ok=True)
    note_path = resolve_note_path(
        note_dir=note_dir,
        item_id=spec.item_id,
        title=spec.title,
        canonical_url=spec.canonical_url,
        published_at=spec.published_at,
    )
    rendered_lines = lines if lines is not None else render_item_note_lines(spec=spec)
    note_path.write_text("\n".join(rendered_lines), encoding="utf-8")
    return note_path
