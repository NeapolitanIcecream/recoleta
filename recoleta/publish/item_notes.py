from __future__ import annotations

from datetime import datetime, timezone
import os
from pathlib import Path
from typing import Any

import yaml
from slugify import slugify

from recoleta.item_summary import normalize_item_summary_markdown

__all__ = [
    "resolve_item_note_path",
    "resolve_item_note_href",
    "write_markdown_note",
    "write_obsidian_note",
]


def _read_yaml_frontmatter(path: Path) -> dict[str, Any] | None:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception:
        return None

    if not lines or lines[0].strip() != "---":
        return None

    end_idx: int | None = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_idx = idx
            break
    if end_idx is None:
        return None

    raw = "\n".join(lines[1:end_idx]).strip()
    if not raw:
        return None

    try:
        loaded = yaml.safe_load(raw)
    except Exception:
        return None
    return loaded if isinstance(loaded, dict) else None


def _item_note_path(
    *,
    note_dir: Path,
    item_id: int,
    title: str,
    canonical_url: str,
    published_at: datetime | None,
) -> Path:
    date_prefix = (published_at or datetime.now(timezone.utc)).strftime("%Y-%m-%d")
    slug = slugify(title, lowercase=True) or "untitled-item"
    note_path = note_dir / f"{date_prefix}--{slug}.md"
    if note_path.exists():
        frontmatter = _read_yaml_frontmatter(note_path) or {}
        existing_url = str(frontmatter.get("url") or "").strip()
        if existing_url != canonical_url.strip():
            note_path = note_dir / f"{date_prefix}--{slug}--{item_id}.md"
    return note_path


def resolve_item_note_path(
    *,
    note_dir: Path,
    item_id: int,
    title: str,
    canonical_url: str,
    published_at: datetime | None,
) -> Path:
    return _item_note_path(
        note_dir=note_dir,
        item_id=item_id,
        title=title,
        canonical_url=canonical_url,
        published_at=published_at,
    )


def resolve_item_note_href(
    *,
    note_dir: Path,
    from_dir: Path,
    item_id: int,
    title: str,
    canonical_url: str,
    published_at: datetime | None,
) -> str:
    note_path = resolve_item_note_path(
        note_dir=note_dir,
        item_id=item_id,
        title=title,
        canonical_url=canonical_url,
        published_at=published_at,
    )
    relative = Path(os.path.relpath(note_path, start=from_dir))
    return relative.as_posix()


def _render_item_note_lines(
    *,
    title: str,
    source: str,
    canonical_url: str,
    published_at: datetime | None,
    authors: list[str],
    topics: list[str],
    relevance_score: float,
    run_id: str,
    summary: str,
    language_code: str | None,
) -> list[str]:
    normalized_summary = normalize_item_summary_markdown(summary)
    frontmatter = {
        "source": source,
        "url": canonical_url,
        "published_at": published_at.isoformat() if published_at else None,
        "authors": authors,
        "topics": topics,
        "relevance_score": round(relevance_score, 4),
        "run_id": run_id,
    }
    normalized_language_code = str(language_code or "").strip()
    if normalized_language_code:
        frontmatter["language_code"] = normalized_language_code
    return [
        "---",
        yaml.safe_dump(frontmatter, sort_keys=False).strip(),
        "---",
        "",
        f"# {title}",
        "",
        normalized_summary,
        "",
        "## Link",
        f"- [{canonical_url}]({canonical_url})",
        "",
    ]


def _write_item_note(
    *,
    note_dir: Path,
    item_id: int,
    title: str,
    source: str,
    canonical_url: str,
    published_at: datetime | None,
    authors: list[str],
    topics: list[str],
    relevance_score: float,
    run_id: str,
    summary: str,
    language_code: str | None = None,
) -> Path:
    note_dir.mkdir(parents=True, exist_ok=True)
    note_path = _item_note_path(
        note_dir=note_dir,
        item_id=item_id,
        title=title,
        canonical_url=canonical_url,
        published_at=published_at,
    )
    lines = _render_item_note_lines(
        title=title,
        source=source,
        canonical_url=canonical_url,
        published_at=published_at,
        authors=authors,
        topics=topics,
        relevance_score=relevance_score,
        run_id=run_id,
        summary=summary,
        language_code=language_code,
    )
    note_path.write_text("\n".join(lines), encoding="utf-8")
    return note_path


def write_obsidian_note(
    *,
    vault_path: Path,
    base_folder: str,
    item_id: int,
    title: str,
    source: str,
    canonical_url: str,
    published_at: datetime | None,
    authors: list[str],
    topics: list[str],
    relevance_score: float,
    run_id: str,
    summary: str,
    language_code: str | None = None,
) -> Path:
    note_dir = vault_path / base_folder / "Inbox"
    return _write_item_note(
        note_dir=note_dir,
        item_id=item_id,
        title=title,
        source=source,
        canonical_url=canonical_url,
        published_at=published_at,
        authors=authors,
        topics=topics,
        relevance_score=relevance_score,
        run_id=run_id,
        summary=summary,
        language_code=language_code,
    )


def write_markdown_note(
    *,
    output_dir: Path,
    item_id: int,
    title: str,
    source: str,
    canonical_url: str,
    published_at: datetime | None,
    authors: list[str],
    topics: list[str],
    relevance_score: float,
    run_id: str,
    summary: str,
    language_code: str | None = None,
) -> Path:
    output_dir = output_dir.expanduser().resolve()
    if output_dir.exists() and not output_dir.is_dir():
        raise ValueError("MARKDOWN_OUTPUT_DIR must be a directory")

    note_dir = output_dir / "Inbox"
    return _write_item_note(
        note_dir=note_dir,
        item_id=item_id,
        title=title,
        source=source,
        canonical_url=canonical_url,
        published_at=published_at,
        authors=authors,
        topics=topics,
        relevance_score=relevance_score,
        run_id=run_id,
        summary=summary,
        language_code=language_code,
    )
