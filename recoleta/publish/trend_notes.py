from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from slugify import slugify

from recoleta.publish.trend_render_shared import _trend_date_token

__all__ = [
    "write_markdown_run_index",
    "write_markdown_stream_index",
    "write_markdown_trend_note",
    "write_obsidian_trend_note",
]


def _single_line(value: str, *, fallback: str) -> str:
    cleaned = " ".join(str(value or "").split()).strip()
    return cleaned if cleaned else fallback


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


def _format_author_suffix(authors: list[str], *, max_authors: int = 6) -> str:
    cleaned = [str(a).strip() for a in (authors or []) if str(a).strip()]
    if not cleaned:
        return ""
    limit = max(0, int(max_authors))
    if limit > 0 and len(cleaned) > limit:
        return f" — {'; '.join(cleaned[:limit])}; …"
    return f" — {'; '.join(cleaned)}"


def _render_trend_note_lines(
    *,
    title: str,
    trend_doc_id: int,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
    run_id: str,
    overview_md: str,
    topics: list[str],
    clusters: list[dict[str, Any]] | None,
    highlights: list[str] | None,
) -> list[str]:
    _ = highlights
    tags = ["recoleta/trend"]
    for topic in topics or []:
        normalized = _sanitize_obsidian_tag(topic)
        if normalized:
            tags.append(f"topic/{normalized}")
    seen_tags: set[str] = set()
    tags = [t for t in tags if not (t in seen_tags or seen_tags.add(t))]

    frontmatter = {
        "kind": "trend",
        "trend_doc_id": int(trend_doc_id),
        "granularity": str(granularity),
        "period_start": period_start.isoformat(),
        "period_end": period_end.isoformat(),
        "topics": topics,
        "run_id": run_id,
        "aliases": [f"recoleta-trend-{int(trend_doc_id)}"],
        "tags": tags,
    }

    lines: list[str] = [
        "---",
        yaml.safe_dump(frontmatter, sort_keys=False).strip(),
        "---",
        "",
        f"# {title}",
        "",
    ]
    lines.extend(
        [
            "## Overview",
            (overview_md or "").strip(),
            "",
            "## Topics",
        ]
    )
    if topics:
        lines.extend([f"- {t}" for t in topics])
    else:
        lines.append("- (none)")

    lines.extend(["", "## Clusters"])
    clusters = clusters or []
    if clusters:
        for cluster in clusters:
            name = _single_line(str(cluster.get("name") or ""), fallback="Cluster")
            desc = str(cluster.get("description") or "").strip()
            lines.extend(["", f"### {name}", ""])
            if desc:
                lines.append(desc)
                lines.append("")
            reps = cluster.get("representative_chunks") or []
            if isinstance(reps, list) and reps:
                lines.append("#### Representative papers")
                for rep in reps[:6]:
                    if not isinstance(rep, dict):
                        continue
                    rep_title = str(rep.get("title") or "").strip()
                    if not rep_title:
                        continue
                    url = str(rep.get("url") or "").strip()
                    authors_raw = rep.get("authors")
                    authors: list[str] = []
                    if isinstance(authors_raw, list):
                        authors = [
                            str(a).strip() for a in authors_raw if str(a).strip()
                        ]
                    author_suffix = _format_author_suffix(authors, max_authors=6)
                    if url:
                        lines.append(f"- [{rep_title}]({url}){author_suffix}")
                    else:
                        lines.append(f"- {rep_title}{author_suffix}")
                lines.append("")
    else:
        lines.append("- (none)")

    return lines


def _write_trend_note(
    *,
    note_dir: Path,
    trend_doc_id: int,
    title: str,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
    run_id: str,
    overview_md: str,
    topics: list[str],
    clusters: list[dict[str, Any]] | None,
    highlights: list[str] | None,
) -> Path:
    note_dir.mkdir(parents=True, exist_ok=True)
    token = _trend_date_token(granularity=granularity, period_start=period_start)
    note_path = note_dir / f"{granularity}--{token}--trend--{trend_doc_id}.md"
    lines = _render_trend_note_lines(
        title=title,
        trend_doc_id=trend_doc_id,
        granularity=granularity,
        period_start=period_start,
        period_end=period_end,
        run_id=run_id,
        overview_md=overview_md,
        topics=topics,
        clusters=clusters,
        highlights=highlights,
    )
    note_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    return note_path


def write_obsidian_trend_note(
    *,
    vault_path: Path,
    base_folder: str,
    trend_doc_id: int,
    title: str,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
    run_id: str,
    overview_md: str,
    topics: list[str],
    clusters: list[dict[str, Any]] | None = None,
    highlights: list[str] | None = None,
) -> Path:
    note_dir = vault_path / base_folder / "Trends"
    return _write_trend_note(
        note_dir=note_dir,
        trend_doc_id=trend_doc_id,
        title=title,
        granularity=granularity,
        period_start=period_start,
        period_end=period_end,
        run_id=run_id,
        overview_md=overview_md,
        topics=topics,
        clusters=clusters,
        highlights=highlights,
    )


def write_markdown_trend_note(
    *,
    output_dir: Path,
    trend_doc_id: int,
    title: str,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
    run_id: str,
    overview_md: str,
    topics: list[str],
    clusters: list[dict[str, Any]] | None = None,
    highlights: list[str] | None = None,
) -> Path:
    output_dir = output_dir.expanduser().resolve()
    if output_dir.exists() and not output_dir.is_dir():
        raise ValueError("MARKDOWN_OUTPUT_DIR must be a directory")
    trends_dir = output_dir / "Trends"
    return _write_trend_note(
        note_dir=trends_dir,
        trend_doc_id=trend_doc_id,
        title=title,
        granularity=granularity,
        period_start=period_start,
        period_end=period_end,
        run_id=run_id,
        overview_md=overview_md,
        topics=topics,
        clusters=clusters,
        highlights=highlights,
    )


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

    def sanitize_segment(
        value: str, *, max_len: int = 72, fallback: str = "unknown"
    ) -> str:
        cleaned = str(value).strip()
        normalized = "".join(
            ch if (ch.isalnum() or ch in {"-", "_"}) else "_" for ch in cleaned
        )
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


def write_markdown_stream_index(
    *,
    output_dir: Path,
    run_id: str,
    generated_at: datetime,
    streams: list[tuple[str, Path]],
) -> Path:
    output_dir = output_dir.expanduser().resolve()
    if output_dir.exists() and not output_dir.is_dir():
        raise ValueError("MARKDOWN_OUTPUT_DIR must be a directory")
    output_dir.mkdir(parents=True, exist_ok=True)

    safe_run_id = slugify(run_id, lowercase=True) or "run"
    runs_dir = output_dir / "Runs"
    runs_dir.mkdir(parents=True, exist_ok=True)
    run_index_path = runs_dir / f"{safe_run_id}--streams.md"
    latest_path = output_dir / "latest.md"

    lines: list[str] = [
        "# Recoleta topic streams",
        "",
        f"- Run ID: `{run_id}`",
        f"- Generated at (UTC): `{generated_at.astimezone(timezone.utc).isoformat()}`",
        "",
        "## Streams",
    ]
    if not streams:
        lines.extend(["", "_No topic streams published in this run._", ""])
    else:
        for stream_name, latest_stream_path in streams:
            rel: str
            try:
                rel = str(latest_stream_path.resolve().relative_to(output_dir))
            except Exception:
                rel = str(latest_stream_path)
            lines.append(f"- [{stream_name}]({rel})")
        lines.append("")

    payload = "\n".join(lines).strip() + "\n"
    run_index_path.write_text(payload, encoding="utf-8")
    latest_path.write_text(payload, encoding="utf-8")
    return latest_path
