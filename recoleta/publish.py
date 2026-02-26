from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from slugify import slugify


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
        frontmatter = _read_yaml_frontmatter(note_path) or {}
        existing_url = str(frontmatter.get("url") or "").strip()
        if existing_url != canonical_url.strip():
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
    insight: str,
    ideas: list[str],
) -> Path:
    output_dir = output_dir.expanduser().resolve()
    if output_dir.exists() and not output_dir.is_dir():
        raise ValueError("MARKDOWN_OUTPUT_DIR must be a directory")

    note_dir = output_dir / "Inbox"
    note_dir.mkdir(parents=True, exist_ok=True)
    date_prefix = (published_at or datetime.now(timezone.utc)).strftime("%Y-%m-%d")
    slug = slugify(title, lowercase=True) or "untitled-item"
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


def write_markdown_run_index(
    *,
    output_dir: Path,
    run_id: str,
    generated_at: datetime,
    notes: list[tuple[str, Path]],
) -> Path:
    output_dir = output_dir.expanduser().resolve()
    if output_dir.exists() and not output_dir.is_dir():
        raise ValueError("MARKDOWN_OUTPUT_DIR must be a directory")
    output_dir.mkdir(parents=True, exist_ok=True)

    def sanitize_segment(value: str, *, max_len: int = 72, fallback: str = "unknown") -> str:
        cleaned = str(value).strip()
        normalized = "".join(ch if (ch.isalnum() or ch in {"-", "_"}) else "_" for ch in cleaned)
        while "__" in normalized:
            normalized = normalized.replace("__", "_")
        normalized = normalized.strip("_")
        if not normalized:
            return fallback
        return normalized[:max_len]

    safe_run_id = sanitize_segment(run_id, fallback="run")
    runs_dir = output_dir / "Runs"
    runs_dir.mkdir(parents=True, exist_ok=True)
    run_index_path = runs_dir / f"{safe_run_id}.md"
    latest_path = output_dir / "latest.md"

    lines: list[str] = [
        "# Recoleta publish output",
        "",
        f"- Run ID: `{run_id}`",
        f"- Generated at (UTC): `{generated_at.astimezone(timezone.utc).isoformat()}`",
        "",
        "## Notes",
    ]
    if not notes:
        lines.extend(["", "_No items published in this run._", ""])
    else:
        for title, note_path in notes:
            rel: str
            try:
                rel = str(note_path.resolve().relative_to(output_dir))
            except Exception:
                rel = str(note_path)
            lines.append(f"- [{title}]({rel})")
        lines.append("")

    payload = "\n".join(lines).strip() + "\n"
    run_index_path.write_text(payload, encoding="utf-8")
    latest_path.write_text(payload, encoding="utf-8")
    return latest_path


def build_telegram_message(*, title: str, summary: str, insight: str, url: str) -> str:
    return (
        f"{title}\n\n"
        f"Summary: {summary.strip()}\n\n"
        f"Why it matters: {insight.strip()}\n\n"
        f"Link: {url}"
    )
