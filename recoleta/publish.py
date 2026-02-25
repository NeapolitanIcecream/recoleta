from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import yaml
from slugify import slugify


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
    insight: str,
    ideas: list[str],
) -> Path:
    note_dir = vault_path / base_folder / "Inbox"
    note_dir.mkdir(parents=True, exist_ok=True)
    date_prefix = (published_at or datetime.now(timezone.utc)).strftime("%Y-%m-%d")
    slug = slugify(title, lowercase=True) or "untitled-item"
    note_path = note_dir / f"{date_prefix}--{slug}.md"
    if note_path.exists():
        note_path = note_dir / f"{date_prefix}--{slug}--{item_id}.md"

    frontmatter = {
        "source": source,
        "url": canonical_url,
        "published_at": published_at.isoformat() if published_at else None,
        "authors": authors,
        "topics": topics,
        "relevance_score": round(relevance_score, 4),
        "run_id": run_id,
    }

    lines = [
        "---",
        yaml.safe_dump(frontmatter, sort_keys=False).strip(),
        "---",
        "",
        f"# {title}",
        "",
        "## Summary",
        summary.strip(),
        "",
        "## Insight",
        insight.strip(),
        "",
        "## Ideas",
    ]
    lines.extend(f"- {idea.strip()}" for idea in ideas if idea.strip())
    lines.extend(
        [
            "",
            "## Links",
            f"- Canonical: {canonical_url}",
            "",
        ]
    )
    note_path.write_text("\n".join(lines), encoding="utf-8")
    return note_path


def build_telegram_message(*, title: str, summary: str, insight: str, url: str) -> str:
    return (
        f"{title}\n\n"
        f"Summary: {summary.strip()}\n\n"
        f"Why it matters: {insight.strip()}\n\n"
        f"Link: {url}"
    )
