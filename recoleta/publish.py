from __future__ import annotations

import base64
from dataclasses import dataclass
from datetime import datetime, timezone
import html
import json
import os
from pathlib import Path
import re
import shutil
import struct
import sys
from typing import Any, Callable
from urllib.parse import urlparse
import zlib

from bs4 import BeautifulSoup, Tag
import fitz
from loguru import logger
from markdown_it import MarkdownIt
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
) -> list[str]:
    frontmatter = {
        "source": source,
        "url": canonical_url,
        "published_at": published_at.isoformat() if published_at else None,
        "authors": authors,
        "topics": topics,
        "relevance_score": round(relevance_score, 4),
        "run_id": run_id,
    }
    return [
        "---",
        yaml.safe_dump(frontmatter, sort_keys=False).strip(),
        "---",
        "",
        f"# {title}",
        "",
        "## Summary",
        summary.strip(),
        "",
        "## Links",
        f"- Canonical: {canonical_url}",
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
    )


def _trend_date_token(*, granularity: str, period_start: datetime) -> str:
    normalized = str(granularity or "").strip().lower()
    if normalized == "day":
        return period_start.strftime("%Y-%m-%d")
    if normalized == "week":
        iso = period_start.isocalendar()
        return f"{iso.year}-W{iso.week:02d}"
    if normalized == "month":
        return period_start.strftime("%Y-%m")
    return period_start.strftime("%Y-%m-%d")


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


def _append_obsidian_callout(
    lines: list[str],
    *,
    callout_type: str,
    title: str,
    bullets: list[str],
    collapsed: bool,
) -> None:
    cleaned = [str(b).strip() for b in (bullets or []) if str(b).strip()]
    if not cleaned:
        return
    marker = f"[!{str(callout_type).strip()}]" + ("-" if collapsed else "")
    lines.append(f"> {marker} {str(title).strip()}")
    for b in cleaned:
        lines.append(f"> - {b}")
    lines.append("")


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


def _split_yaml_frontmatter_text(text: str) -> tuple[dict[str, Any], str]:
    normalized = str(text or "").replace("\r\n", "\n").replace("\r", "\n")
    lines = normalized.split("\n")
    if not lines or lines[0].strip() != "---":
        return {}, normalized

    end_idx: int | None = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_idx = idx
            break
    if end_idx is None:
        return {}, normalized

    raw = "\n".join(lines[1:end_idx]).strip()
    body = "\n".join(lines[end_idx + 1 :]).lstrip("\n")
    if not raw:
        return {}, body

    try:
        loaded = yaml.safe_load(raw)
    except Exception:
        return {}, body
    if isinstance(loaded, dict):
        return loaded, body
    return {}, body


def _normalize_obsidian_callouts_for_pdf(text: str) -> str:
    lines = str(text or "").splitlines()
    if not lines:
        return ""

    normalized: list[str] = []
    idx = 0
    while idx < len(lines):
        match = re.match(r"^\s*>\s*\[!([^\]]+)\][-+]?\s*(.*)$", lines[idx])
        if match is None:
            normalized.append(lines[idx])
            idx += 1
            continue

        callout_kind = str(match.group(1) or "").strip().replace("-", " ")
        title = str(match.group(2) or "").strip() or callout_kind.title()
        body_lines: list[str] = []
        idx += 1
        while idx < len(lines):
            current = lines[idx]
            if not current.lstrip().startswith(">"):
                break
            body_lines.append(re.sub(r"^\s*>\s?", "", current))
            idx += 1

        normalized.extend(["", f"## {title}", ""])
        normalized.extend(body_lines)
        if body_lines and body_lines[-1].strip():
            normalized.append("")
    return "\n".join(normalized).strip() + "\n"


def _trend_pdf_period_label(frontmatter: dict[str, Any]) -> str:
    granularity = str(frontmatter.get("granularity") or "").strip().lower()
    raw_period_start = str(frontmatter.get("period_start") or "").strip()
    raw_period_end = str(frontmatter.get("period_end") or "").strip()
    if granularity and raw_period_start:
        try:
            period_start = datetime.fromisoformat(raw_period_start)
            if period_start.tzinfo is None:
                period_start = period_start.replace(tzinfo=timezone.utc)
            token = _trend_date_token(
                granularity=granularity,
                period_start=period_start,
            )
            if raw_period_end:
                period_end = datetime.fromisoformat(raw_period_end)
                if period_end.tzinfo is None:
                    period_end = period_end.replace(tzinfo=timezone.utc)
                return (
                    f"{token} ({period_start.date().isoformat()} "
                    f"to {period_end.date().isoformat()})"
                )
            return token
        except Exception:
            return raw_period_start
    return raw_period_start or "Current window"


def _trend_pdf_topics_summary(frontmatter: dict[str, Any]) -> str:
    topics = frontmatter.get("topics")
    if not isinstance(topics, list) or not topics:
        return "No tracked topics"
    cleaned = [str(topic).strip() for topic in topics if str(topic).strip()]
    if not cleaned:
        return "No tracked topics"
    if len(cleaned) <= 3:
        return ", ".join(cleaned)
    return f"{len(cleaned)} tracked topics"


def _trend_pdf_meta_rows(frontmatter: dict[str, Any]) -> list[tuple[str, str]]:
    granularity = str(frontmatter.get("granularity") or "").strip().lower() or "trend"
    topics = frontmatter.get("topics")
    topic_count = 0
    if isinstance(topics, list):
        topic_count = len(
            [str(topic).strip() for topic in topics if str(topic).strip()]
        )
    return [
        ("Window", granularity.title()),
        ("Period", _trend_pdf_period_label(frontmatter)),
        ("Coverage", "Telegram-ready PDF brief"),
        ("Topics", str(topic_count) if topic_count > 0 else "None"),
    ]


def _trend_pdf_hero_dek(frontmatter: dict[str, Any]) -> str:
    granularity = str(frontmatter.get("granularity") or "").strip().lower() or "trend"
    return (
        f"{granularity.title()} brief tuned for quick scanning, stronger hierarchy, "
        f"and compact delivery in Telegram."
    )


@dataclass(slots=True)
class TrendPdfSection:
    heading: str
    slug: str
    inner_html: str


def _normalize_section_heading(heading: str) -> str:
    return str(heading or "").strip().lower()


def _section_matches(heading: str, *patterns: str) -> bool:
    normalized = _normalize_section_heading(heading)
    return any(pattern in normalized for pattern in patterns)


def _is_primary_trend_section_heading(heading: str) -> bool:
    return _section_matches(
        heading,
        "tl;dr",
        "summary",
        "overview",
        "must-read",
        "topics",
        "clusters",
        "highlight",
    )


def _build_topic_grid(soup: BeautifulSoup, topics: list[str]) -> Tag:
    table = soup.new_tag("table", attrs={"class": "topic-grid"})
    tbody = soup.new_tag("tbody")
    table.append(tbody)
    cleaned = [topic for topic in topics if topic]
    for idx in range(0, len(cleaned), 4):
        row = soup.new_tag("tr")
        for offset in range(4):
            cell = soup.new_tag("td")
            value = cleaned[idx + offset] if idx + offset < len(cleaned) else ""
            cell["class"] = "topic-cell topic-cell-empty" if not value else "topic-cell"
            cell.string = value
            row.append(cell)
        tbody.append(row)
    return table


def _extract_trend_pdf_sections(*, body_html: str) -> tuple[str, list[TrendPdfSection]]:
    soup = BeautifulSoup(body_html, "html.parser")
    title = "Trend"

    first_h1 = soup.find("h1")
    if first_h1 is not None:
        extracted_title = first_h1.get_text(" ", strip=True)
        if extracted_title:
            title = extracted_title
        first_h1.decompose()

    sections: list[TrendPdfSection] = []
    current_heading = "Preface"
    current_nodes: list[str] = []

    for node in list(soup.contents):
        extracted = node.extract()
        if not str(extracted).strip():
            continue
        if isinstance(extracted, Tag) and extracted.name == "h2":
            next_heading = extracted.get_text(" ", strip=True) or "Section"
            if (
                current_nodes == []
                and _is_primary_trend_section_heading(current_heading)
                and not _is_primary_trend_section_heading(next_heading)
            ):
                extracted.name = "h3"
                current_nodes.append(str(extracted))
                continue
            if current_nodes:
                sections.append(
                    TrendPdfSection(
                        heading=current_heading,
                        slug=slugify(current_heading) or "section",
                        inner_html="".join(current_nodes).strip(),
                    )
                )
            current_heading = next_heading
            current_nodes = []
            continue
        current_nodes.append(str(extracted))

    if current_nodes:
        sections.append(
            TrendPdfSection(
                heading=current_heading,
                slug=slugify(current_heading) or "section",
                inner_html="".join(current_nodes).strip(),
            )
        )

    return title, sections


def _render_section_label_html(heading: str) -> str:
    return (
        f"<h2 class='section-label'>{html.escape(heading)}</h2>"
    )


def _extract_topic_items(*, section: TrendPdfSection) -> list[str]:
    soup = BeautifulSoup(section.inner_html, "html.parser")
    bullet_list = soup.find("ul")
    if bullet_list is None:
        return []
    return [
        item.get_text(" ", strip=True)
        for item in bullet_list.find_all("li")
        if item.get_text(" ", strip=True)
    ]


def _extract_cluster_entries(*, section: TrendPdfSection) -> list[tuple[str, str]]:
    soup = BeautifulSoup(section.inner_html, "html.parser")
    clusters: list[tuple[str, str]] = []
    current_title: str | None = None
    current_nodes: list[str] = []

    for node in list(soup.contents):
        extracted = node.extract()
        if not str(extracted).strip():
            continue
        if isinstance(extracted, Tag) and extracted.name == "h3":
            if current_title is not None:
                clusters.append((current_title, "".join(current_nodes).strip()))
            current_title = extracted.get_text(" ", strip=True) or "Cluster"
            current_nodes = []
            continue
        current_nodes.append(str(extracted))

    if current_title is not None:
        clusters.append((current_title, "".join(current_nodes).strip()))
    return clusters


def _render_topics_section_html(*, section: TrendPdfSection) -> str:
    soup = BeautifulSoup(section.inner_html, "html.parser")
    topics = _extract_topic_items(section=section)
    grid = str(_build_topic_grid(soup, topics)) if topics else "<p>(none)</p>"
    return (
        "<section class='topics-section'>"
        f"{_render_section_label_html(section.heading)}"
        f"{grid}"
        "</section>"
    )


def _render_summary_panel_html(*, section: TrendPdfSection, modifier: str) -> str:
    return (
        f"<td class='summary-panel {modifier}'>"
        f"{_render_section_label_html(section.heading)}"
        f"<div class='summary-panel-body'>{section.inner_html}</div>"
        "</td>"
    )


def _render_cluster_grid_html(*, section: TrendPdfSection) -> str:
    clusters = _extract_cluster_entries(section=section)
    if not clusters:
        return (
            "<section class='clusters-section'>"
            f"{_render_section_label_html(section.heading)}"
            "<p>(none)</p>"
            "</section>"
        )

    rows: list[str] = []
    for idx in range(0, len(clusters), 2):
        row_cells: list[str] = []
        for offset in range(2):
            if idx + offset >= len(clusters):
                row_cells.append("<td class='cluster-cell cluster-cell-empty'></td>")
                continue
            cluster_title, cluster_html = clusters[idx + offset]
            row_cells.append(
                "<td class='cluster-cell'>"
                "<div class='cluster-card'>"
                f"<div class='cluster-title'>{html.escape(cluster_title)}</div>"
                f"<div class='cluster-body'>{cluster_html}</div>"
                "</div>"
                "</td>"
            )
        rows.append("<tr>" + "".join(row_cells) + "</tr>")

    return (
        "<section class='clusters-section'>"
        f"{_render_section_label_html(section.heading)}"
        "<table class='cluster-grid'>"
        + "".join(rows)
        + "</table>"
        "</section>"
    )


def _render_generic_section_html(*, section: TrendPdfSection, compact: bool = False) -> str:
    modifier = " section-compact" if compact else ""
    return (
        f"<section class='content-section{modifier} section-{section.slug}'>"
        f"{_render_section_label_html(section.heading)}"
        f"<div class='content-prose'>{section.inner_html}</div>"
        "</section>"
    )


def _decorate_trend_pdf_body_html(*, body_html: str) -> tuple[str, str]:
    title, sections = _extract_trend_pdf_sections(body_html=body_html)
    used: set[str] = set()
    rendered: list[str] = []

    summary_sections: list[tuple[TrendPdfSection, str]] = []
    for section in sections:
        if _section_matches(section.heading, "tl;dr", "summary"):
            summary_sections.append((section, "summary-primary"))
            used.add(section.slug)
        elif _section_matches(section.heading, "must-read"):
            summary_sections.append((section, "summary-secondary"))
            used.add(section.slug)

    if summary_sections:
        cells = "".join(
            _render_summary_panel_html(section=section, modifier=modifier)
            for section, modifier in summary_sections[:2]
        )
        rendered.append(
            "<section class='summary-grid-wrap'>"
            "<table class='summary-grid'><tr>"
            f"{cells}"
            "</tr></table>"
            "</section>"
        )

    for section in sections:
        if section.slug in used:
            continue
        if _section_matches(section.heading, "overview"):
            rendered.append(_render_generic_section_html(section=section))
            used.add(section.slug)
        elif _section_matches(section.heading, "topics"):
            rendered.append(_render_topics_section_html(section=section))
            used.add(section.slug)
        elif _section_matches(section.heading, "clusters"):
            rendered.append(_render_cluster_grid_html(section=section))
            used.add(section.slug)
        elif _section_matches(section.heading, "highlight"):
            rendered.append(_render_generic_section_html(section=section, compact=True))
            used.add(section.slug)

    for section in sections:
        if section.slug in used:
            continue
        rendered.append(_render_generic_section_html(section=section))

    return "<div class='brief-flow'>" + "".join(rendered) + "</div>", title


def _build_trend_pdf_html(
    *,
    body_html: str,
    frontmatter: dict[str, Any],
    title: str,
) -> str:
    meta_rows = _trend_pdf_meta_rows(frontmatter)
    meta_cells = []
    for label, value in meta_rows:
        meta_cells.append(
            "<td>"
            f"<div class='meta-label'>{html.escape(label)}</div>"
            f"<div class='meta-value'>{html.escape(value)}</div>"
            "</td>"
        )

    meta_rows_html = "<tr>" + "".join(meta_cells) + "</tr>"

    return (
        "<html>"
        "<body>"
        "<div class='page-shell'>"
        "<div class='hero'>"
        "<div class='hero-kicker'>Recoleta Trend Brief</div>"
        f"<div class='hero-title'>{html.escape(title)}</div>"
        f"<div class='hero-dek'>{html.escape(_trend_pdf_hero_dek(frontmatter))}</div>"
        f"<div class='hero-summary'>{html.escape(_trend_pdf_topics_summary(frontmatter))}</div>"
        "<table class='meta-grid'>"
        f"{meta_rows_html}"
        "</table>"
        "</div>"
        f"<div class='content'>{body_html}</div>"
        "</div>"
        "</body>"
        "</html>"
    )


def _render_browser_section_label_html(heading: str) -> str:
    return f"<h2 class='section-label'>{html.escape(heading)}</h2>"


def _render_browser_content_card_html(
    *,
    heading: str,
    inner_html: str,
    card_classes: str = "surface-card section-card",
    prose_class: str = "prose",
) -> str:
    return (
        f"<section class='{card_classes}'>"
        f"{_render_browser_section_label_html(heading)}"
        f"<div class='{prose_class}'>{inner_html}</div>"
        "</section>"
    )


def _render_browser_topics_section_html(*, section: TrendPdfSection) -> str:
    topics = _extract_topic_items(section=section)
    if not topics:
        return _render_browser_content_card_html(
            heading=section.heading,
            inner_html="<p>(none)</p>",
        )

    pills = "".join(
        f"<span class='topic-pill'>{html.escape(topic)}</span>" for topic in topics
    )
    return (
        "<section class='surface-card section-card topics-card'>"
        f"{_render_browser_section_label_html(section.heading)}"
        f"<div class='topic-grid'>{pills}</div>"
        "</section>"
    )


def _render_browser_clusters_section_html(*, section: TrendPdfSection) -> str:
    clusters = _extract_cluster_entries(section=section)
    if not clusters:
        return _render_browser_content_card_html(
            heading=section.heading,
            inner_html="<p>(none)</p>",
        )

    cards = "".join(
        "<article class='cluster-card'>"
        f"<h3>{html.escape(cluster_title)}</h3>"
        f"<div class='cluster-body'>{cluster_html}</div>"
        "</article>"
        for cluster_title, cluster_html in clusters
    )
    return (
        "<section class='surface-card section-card cluster-section'>"
        f"{_render_browser_section_label_html(section.heading)}"
        f"<div class='cluster-columns'>{cards}</div>"
        "</section>"
    )


def _build_trend_browser_body_html(*, sections: list[TrendPdfSection]) -> str:
    used: set[str] = set()
    rendered: list[str] = []

    summary_cards: list[str] = []
    for section in sections:
        if _section_matches(section.heading, "tl;dr", "summary"):
            summary_cards.append(
                _render_browser_content_card_html(
                    heading=section.heading,
                    inner_html=section.inner_html,
                    card_classes="surface-card section-card summary-card summary-card-primary",
                )
            )
            used.add(section.slug)
        elif _section_matches(section.heading, "must-read"):
            summary_cards.append(
                _render_browser_content_card_html(
                    heading=section.heading,
                    inner_html=section.inner_html,
                    card_classes="surface-card section-card summary-card summary-card-secondary",
                )
            )
            used.add(section.slug)

    if summary_cards:
        rendered.append(
            "<section class='summary-grid'>"
            + "".join(summary_cards[:2])
            + "</section>"
        )

    for section in sections:
        if section.slug in used:
            continue
        if _section_matches(section.heading, "overview"):
            rendered.append(
                _render_browser_content_card_html(
                    heading=section.heading,
                    inner_html=section.inner_html,
                )
            )
            used.add(section.slug)
        elif _section_matches(section.heading, "topics"):
            rendered.append(_render_browser_topics_section_html(section=section))
            used.add(section.slug)
        elif _section_matches(section.heading, "clusters"):
            rendered.append(_render_browser_clusters_section_html(section=section))
            used.add(section.slug)
        elif _section_matches(section.heading, "highlight"):
            rendered.append(
                _render_browser_content_card_html(
                    heading=section.heading,
                    inner_html=section.inner_html,
                    card_classes="surface-card section-card highlight-card",
                )
            )
            used.add(section.slug)

    for section in sections:
        if section.slug in used:
            continue
        rendered.append(
            _render_browser_content_card_html(
                heading=section.heading,
                inner_html=section.inner_html,
            )
        )

    return "<div class='document-flow'>" + "".join(rendered) + "</div>"


def _build_trend_browser_pdf_html(
    *,
    frontmatter: dict[str, Any],
    title: str,
    sections: list[TrendPdfSection],
) -> str:
    meta_items = "".join(
        "<div class='meta-item'>"
        f"<div class='meta-label'>{html.escape(label)}</div>"
        f"<div class='meta-value'>{html.escape(value)}</div>"
        "</div>"
        for label, value in _trend_pdf_meta_rows(frontmatter)
    )
    body_html = _build_trend_browser_body_html(sections=sections)
    return (
        "<!doctype html>"
        "<html lang='zh-CN'>"
        "<head>"
        "<meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width, initial-scale=1'>"
        f"<title>{html.escape(title)}</title>"
        "</head>"
        "<body>"
        "<main class='page-shell'>"
        "<section class='hero'>"
        "<div class='hero-grid'>"
        "<div class='hero-main'>"
        "<div class='hero-kicker'>Recoleta Trend Brief</div>"
        f"<h1 class='hero-title'>{html.escape(title)}</h1>"
        f"<p class='hero-dek'>{html.escape(_trend_pdf_hero_dek(frontmatter))}</p>"
        f"<div class='hero-summary'>{html.escape(_trend_pdf_topics_summary(frontmatter))}</div>"
        "</div>"
        "<div class='hero-meta'>"
        f"{meta_items}"
        "</div>"
        "</div>"
        "</section>"
        f"{body_html}"
        "</main>"
        "</body>"
        "</html>"
    )


def _normalize_trend_pdf_page_mode(page_mode: str) -> str:
    normalized = str(page_mode or "").strip().lower() or "a4"
    if normalized not in {"a4", "continuous"}:
        raise ValueError(
            "Trend PDF page_mode must be one of: a4, continuous"
        )
    return normalized


_TREND_PDF_CSS = """
body {
  font-family: "PingFang SC", "Hiragino Sans GB", "Helvetica Neue", Arial, sans-serif;
  font-size: 10.9pt;
  line-height: 1.64;
  color: #1d2733;
  background: #f5f7fb;
}
.page-shell {
  padding: 0;
}
.hero {
  margin-bottom: 16pt;
  padding: 18pt 18pt 16pt 18pt;
  border-radius: 20pt;
  background: #eef3fa;
  border: 1pt solid #d8e2ef;
  color: #1d2d35;
}
.hero-kicker {
  margin-bottom: 7pt;
  font-size: 8.4pt;
  font-weight: bold;
  letter-spacing: 1.8pt;
  text-transform: uppercase;
  color: #4f6a8d;
}
.hero-title {
  margin: 0 0 6pt 0;
  font-family: "Songti SC", "STSong", Georgia, serif;
  font-size: 22pt;
  line-height: 1.16;
  font-weight: bold;
  color: #112234;
}
.hero-dek {
  margin: 0 0 10pt 0;
  color: #536478;
  font-size: 9.7pt;
}
.hero-summary {
  margin: 0 0 10pt 0;
  color: #1664c0;
  font-size: 9.2pt;
  font-weight: bold;
}
.meta-grid {
  width: 100%;
  margin: 0;
  border-collapse: separate;
  border-spacing: 6pt;
}
.meta-grid td {
  width: 25%;
  padding: 8pt 9pt;
  vertical-align: top;
  border: 1pt solid #d9e3ef;
  border-radius: 12pt;
  background: #f9fbfe;
}
.meta-label {
  margin-bottom: 2pt;
  font-size: 7.8pt;
  letter-spacing: 1.2pt;
  text-transform: uppercase;
  color: #6f8096;
}
.meta-value {
  font-size: 9.8pt;
  line-height: 1.4;
  color: #223243;
}
.content {
  margin: 0;
}
.brief-flow {
  margin: 0;
}
.summary-grid-wrap {
  margin: 0 0 12pt 0;
}
.summary-grid {
  width: 100%;
  margin: 0;
  border-collapse: separate;
  border-spacing: 8pt;
}
.summary-panel {
  width: 50%;
  padding: 12pt 13pt;
  vertical-align: top;
  border: 1pt solid #dbe4ef;
  border-radius: 16pt;
  background: #ffffff;
}
.summary-primary {
  background: #edf5ff;
  border-color: #cfe0f7;
}
.summary-secondary {
  background: #f8fbff;
}
.summary-panel-body {
  font-size: 10pt;
}
.content-section,
.topics-section,
.clusters-section {
  margin: 0 0 12pt 0;
}
.content-section {
  padding: 0;
}
.section-compact {
  padding: 10pt 12pt;
  border: 1pt solid #dbe4ef;
  border-radius: 14pt;
  background: #fbfdff;
}
.section-label {
  margin: 0 0 7pt 0;
  font-size: 8.2pt;
  line-height: 1.2;
  color: #6a7f99;
  text-transform: uppercase;
  letter-spacing: 1.5pt;
}
.content-prose {
  margin: 0;
}
h1 {
  margin: 0 0 12pt 0;
  font-size: 23pt;
  line-height: 1.2;
  color: #102a37;
}
h2 {
  margin: 0;
  padding: 0;
  font-size: 8.9pt;
  line-height: 1.25;
  color: #7d5b42;
  text-transform: uppercase;
  letter-spacing: 1.6pt;
  border: 0;
}
h3 {
  margin: 12pt 0 5pt 0;
  font-size: 13.2pt;
  color: #15395a;
  font-family: "Songti SC", "STSong", Georgia, serif;
}
h4, h5, h6 {
  margin: 10pt 0 5pt 0;
  font-size: 8.7pt;
  color: #5d7492;
  text-transform: uppercase;
  letter-spacing: 1.1pt;
}
p {
  margin: 0 0 7pt 0;
}
ul, ol {
  margin: 0 0 8pt 14pt;
}
li {
  margin: 0 0 4pt 0;
}
blockquote {
  margin: 0 0 10pt 0;
  padding: 10pt 11pt;
  border-left: 3pt solid #3390ec;
  background: #eff7ff;
  color: #36536e;
  border-radius: 12pt;
}
pre {
  margin: 0 0 14pt 0;
  padding: 12pt;
  border-radius: 12pt;
  background: #16212b;
  color: #f8fafc;
  font-size: 9pt;
  line-height: 1.45;
  white-space: pre-wrap;
}
code {
  padding: 1pt 4pt;
  border-radius: 6pt;
  background: #eef3f8;
  border: 1pt solid #d9e3ef;
  font-size: 9.5pt;
}
a {
  color: #1d6fd3;
  text-decoration: underline;
}
hr {
  margin: 18pt 0;
  border: 0;
  border-top: 1pt solid #dbe4ef;
}
table {
  width: 100%;
  margin: 0 0 14pt 0;
  border-collapse: collapse;
}
th, td {
  padding: 6pt 8pt;
  border: 1pt solid #eadfce;
}
th {
  background: #f7f0e4;
}
strong {
  color: #162a34;
}
.topic-grid {
  width: 100%;
  margin: 0;
  border-collapse: separate;
  border-spacing: 6pt;
}
.topic-grid td {
  width: 25%;
  padding: 6pt 8pt;
  border: 1pt solid #dbe4ef;
  border-radius: 999pt;
  background: #f8fbff;
  font-size: 8.9pt;
  color: #425a73;
}
.topic-grid .topic-cell-empty {
  background: transparent;
  border-color: transparent;
}
.cluster-grid {
  width: 100%;
  margin: 0;
  border-collapse: separate;
  border-spacing: 8pt;
}
.cluster-cell {
  width: 50%;
  vertical-align: top;
  border: 0;
  padding: 0;
}
.cluster-cell-empty {
  background: transparent;
}
.cluster-card {
  padding: 11pt 12pt 9pt 12pt;
  border: 1pt solid #dbe4ef;
  border-radius: 14pt;
  background: #ffffff;
  page-break-inside: avoid;
}
.cluster-title {
  margin: 0 0 7pt 0;
  font-family: "Songti SC", "STSong", Georgia, serif;
  font-size: 12.3pt;
  line-height: 1.28;
  color: #13395f;
}
.cluster-body {
  margin: 0;
}
.content-prose ul:last-child,
.content-prose ol:last-child,
.content-prose p:last-child,
.summary-panel-body ul:last-child,
.summary-panel-body ol:last-child,
.summary-panel-body p:last-child,
.cluster-body ul:last-child,
.cluster-body ol:last-child,
.cluster-body p:last-child {
  margin-bottom: 0;
}
"""


def _png_chunk(kind: bytes, data: bytes) -> bytes:
    return (
        struct.pack(">I", len(data))
        + kind
        + data
        + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    )


def _build_vertical_gradient_png_data_uri(
    start_rgb: tuple[int, int, int],
    end_rgb: tuple[int, int, int],
    *,
    width: int = 8,
    height: int = 256,
) -> str:
    rows: list[bytes] = []
    for y in range(height):
        t = 0.0 if height <= 1 else y / (height - 1)
        r = round(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * t)
        g = round(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * t)
        b = round(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * t)
        pixel = bytes((r, g, b, 255))
        rows.append(b"\x00" + pixel * width)

    payload = b"".join(rows)
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    png = (
        b"\x89PNG\r\n\x1a\n"
        + _png_chunk(b"IHDR", ihdr)
        + _png_chunk(b"IDAT", zlib.compress(payload, level=9))
        + _png_chunk(b"IEND", b"")
    )
    encoded = base64.b64encode(png).decode("ascii")
    return f"data:image/png;base64,{encoded}"


_TREND_BROWSER_BASE_CARD_GRADIENT = _build_vertical_gradient_png_data_uri(
    (255, 255, 255),
    (244, 248, 252),
)
_TREND_BROWSER_SUMMARY_PRIMARY_GRADIENT = _build_vertical_gradient_png_data_uri(
    (235, 243, 253),
    (248, 251, 254),
)
_TREND_BROWSER_SUMMARY_SECONDARY_GRADIENT = _build_vertical_gradient_png_data_uri(
    (247, 250, 254),
    (251, 252, 254),
)
_TREND_BROWSER_HIGHLIGHT_GRADIENT = _build_vertical_gradient_png_data_uri(
    (247, 250, 254),
    (241, 247, 253),
)
_TREND_BROWSER_CLUSTER_GRADIENT = _build_vertical_gradient_png_data_uri(
    (255, 255, 255),
    (246, 249, 253),
)


_TREND_BROWSER_PDF_CSS = """
:root {
  color-scheme: light;
  --page-bg-top: #dbe7f4;
  --page-bg-mid: #eef4f8;
  --page-bg-bottom: #fafcfd;
  --line: rgba(20, 41, 67, 0.12);
  --line-strong: rgba(15, 35, 58, 0.18);
  --text: #142133;
  --muted: #5d7188;
  --accent: #1764c2;
  --accent-soft: #e7effa;
  --hero-start: #10273f;
  --hero-end: #2b5f96;
  --radius-xl: 28px;
  --radius-lg: 22px;
  --radius-md: 18px;
}
* {
  box-sizing: border-box;
}
html {
  margin: 0;
  background: linear-gradient(
    180deg,
    var(--page-bg-top) 0%,
    var(--page-bg-mid) 40%,
    var(--page-bg-bottom) 100%
  );
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}
@page {
  margin: 0;
}
body {
  margin: 0;
  color: var(--text);
  background:
    radial-gradient(circle at top left, rgba(255, 255, 255, 0.74), transparent 34%),
    radial-gradient(circle at top right, rgba(23, 100, 194, 0.10), transparent 28%),
    linear-gradient(
      180deg,
      var(--page-bg-top) 0%,
      var(--page-bg-mid) 40%,
      var(--page-bg-bottom) 100%
    );
  font-family: "PingFang SC", "Hiragino Sans GB", "Helvetica Neue", "Segoe UI", Arial, sans-serif;
}
.page-shell {
  width: 100%;
  min-height: 100vh;
  padding: 12.5mm 12.5mm 14mm;
}
.hero {
  padding: 18px 20px 18px;
  border-radius: var(--radius-xl);
  border: 1px solid rgba(255, 255, 255, 0.16);
  background:
    radial-gradient(circle at top right, rgba(255, 255, 255, 0.18), transparent 30%),
    linear-gradient(135deg, var(--hero-start) 0%, var(--hero-end) 100%);
  color: #f7fbff;
}
.hero-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.55fr) minmax(220px, 0.9fr);
  gap: 16px;
  align-items: end;
}
.hero-main,
.hero-meta,
.document-flow,
.summary-grid,
.cluster-columns {
  min-width: 0;
}
.hero-kicker {
  margin-bottom: 8px;
  color: rgba(233, 242, 255, 0.92);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}
.hero-title {
  margin: 0 0 10px;
  font-size: 27px;
  line-height: 1.1;
  letter-spacing: -0.035em;
  font-weight: 760;
}
.hero-dek {
  margin: 0 0 14px;
  color: rgba(236, 243, 251, 0.82);
  font-size: 13.5px;
  line-height: 1.46;
}
.hero-summary {
  display: inline-flex;
  align-items: center;
  min-height: 30px;
  padding: 0 12px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: #eff5ff;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.04em;
}
.hero-meta {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}
.meta-item {
  min-height: 76px;
  padding: 12px 13px 11px;
  border-radius: var(--radius-md);
  border: 1px solid rgba(255, 255, 255, 0.16);
  background: rgba(244, 248, 255, 0.14);
}
.meta-label {
  margin-bottom: 6px;
  color: rgba(226, 236, 248, 0.76);
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.10em;
  text-transform: uppercase;
}
.meta-value {
  color: #f9fbff;
  font-size: 13px;
  line-height: 1.34;
  font-weight: 560;
  word-break: break-word;
}
.document-flow {
  margin-top: 12px;
}
.summary-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}
.surface-card {
  margin-top: 12px;
  padding: 14px 15px;
  border-radius: var(--radius-lg);
  border: 1px solid var(--line);
  background:
    url("__TREND_BROWSER_BASE_CARD_GRADIENT__") center/100% 100% no-repeat,
    #f7fafc;
  break-inside: avoid;
  page-break-inside: avoid;
}
.summary-grid .surface-card {
  margin-top: 0;
}
.summary-card-primary {
  border-color: rgba(28, 79, 138, 0.18);
  background:
    url("__TREND_BROWSER_SUMMARY_PRIMARY_GRADIENT__") center/100% 100% no-repeat,
    #f3f8fd;
}
.summary-card-secondary {
  background:
    url("__TREND_BROWSER_SUMMARY_SECONDARY_GRADIENT__") center/100% 100% no-repeat,
    #f8fbfe;
}
.highlight-card {
  background:
    url("__TREND_BROWSER_HIGHLIGHT_GRADIENT__") center/100% 100% no-repeat,
    #f5f9fd;
}
.section-label {
  margin: 0 0 10px;
  color: #6c8197;
  font-size: 10px;
  line-height: 1.2;
  font-weight: 700;
  letter-spacing: 0.10em;
  text-transform: uppercase;
}
.prose,
.cluster-body {
  font-size: 13.4px;
  line-height: 1.58;
}
.prose > *:first-child,
.cluster-body > *:first-child {
  margin-top: 0;
}
.prose > *:last-child,
.cluster-body > *:last-child {
  margin-bottom: 0;
}
.prose p,
.cluster-body p {
  margin: 0 0 9px;
}
.prose h3,
.cluster-card h3 {
  margin: 14px 0 8px;
  color: #15395d;
  font-family: "Songti SC", "STSong", Georgia, serif;
  font-size: 20px;
  line-height: 1.18;
  letter-spacing: -0.03em;
  font-weight: 720;
}
.cluster-card h3 {
  margin-top: 0;
  font-size: 18px;
}
.prose h4,
.cluster-body h4 {
  margin: 12px 0 7px;
  color: #6d8198;
  font-size: 10px;
  line-height: 1.2;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}
.prose ul,
.prose ol,
.cluster-body ul,
.cluster-body ol {
  margin: 7px 0 9px;
  padding-inline-start: 1.05em;
}
.prose li,
.cluster-body li {
  margin: 0 0 6px;
  padding-left: 0.12em;
}
.prose li::marker,
.cluster-body li::marker {
  color: #7a8fa7;
}
.prose a,
.cluster-body a {
  color: var(--accent);
  text-decoration: none;
}
.prose strong,
.cluster-body strong {
  color: #122238;
}
.prose blockquote,
.cluster-body blockquote {
  margin: 10px 0;
  padding: 12px 14px;
  border-left: 3px solid rgba(23, 100, 194, 0.45);
  border-radius: 14px;
  background: var(--accent-soft);
  color: #27496d;
}
.prose pre,
.cluster-body pre {
  margin: 10px 0;
  padding: 12px 14px;
  border-radius: 16px;
  background: #16212b;
  color: #f8fafc;
  font-size: 12px;
  line-height: 1.5;
  white-space: pre-wrap;
}
.prose code,
.cluster-body code {
  padding: 1px 5px;
  border-radius: 8px;
  background: #eef3f8;
  border: 1px solid #d9e3ef;
  font-size: 12px;
}
.prose table,
.cluster-body table {
  width: 100%;
  margin: 10px 0 12px;
  border-collapse: collapse;
}
.prose th,
.prose td,
.cluster-body th,
.cluster-body td {
  padding: 7px 8px;
  border: 1px solid #dbe4ef;
  text-align: left;
  vertical-align: top;
}
.prose th,
.cluster-body th {
  background: #f4f7fb;
}
.topics-card {
  padding-bottom: 15px;
}
.topic-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 8px;
}
.topic-pill {
  display: block;
  min-height: 38px;
  padding: 9px 12px;
  border-radius: 999px;
  border: 1px solid #dbe4ef;
  background: rgba(248, 251, 255, 0.98);
  color: #425a74;
  font-size: 11px;
  line-height: 1.3;
  font-weight: 560;
}
.cluster-section {
  padding-bottom: 4px;
}
.cluster-columns {
  column-count: 2;
  column-gap: 12px;
}
.cluster-card {
  display: inline-block;
  width: 100%;
  margin: 0 0 12px;
  padding: 14px 14px 12px;
  border-radius: 18px;
  border: 1px solid var(--line-strong);
  background:
    url("__TREND_BROWSER_CLUSTER_GRADIENT__") center/100% 100% no-repeat,
    #f8fbfd;
  break-inside: avoid;
  page-break-inside: avoid;
}
"""

_TREND_BROWSER_PDF_CSS = (
    _TREND_BROWSER_PDF_CSS
    .replace(
        "__TREND_BROWSER_BASE_CARD_GRADIENT__",
        _TREND_BROWSER_BASE_CARD_GRADIENT,
    )
    .replace(
        "__TREND_BROWSER_SUMMARY_PRIMARY_GRADIENT__",
        _TREND_BROWSER_SUMMARY_PRIMARY_GRADIENT,
    )
    .replace(
        "__TREND_BROWSER_SUMMARY_SECONDARY_GRADIENT__",
        _TREND_BROWSER_SUMMARY_SECONDARY_GRADIENT,
    )
    .replace(
        "__TREND_BROWSER_HIGHLIGHT_GRADIENT__",
        _TREND_BROWSER_HIGHLIGHT_GRADIENT,
    )
    .replace(
        "__TREND_BROWSER_CLUSTER_GRADIENT__",
        _TREND_BROWSER_CLUSTER_GRADIENT,
    )
)


@dataclass(slots=True)
class TrendPdfRenderInputs:
    markdown_path: Path
    output_path: Path
    frontmatter: dict[str, Any]
    raw_markdown: str
    normalized_markdown: str
    title: str
    document_html: str
    css: str
    renderer: str
    page_mode: str


@dataclass(slots=True)
class TrendPdfRenderResult:
    path: Path
    prepared: TrendPdfRenderInputs


def _prepare_trend_pdf_render_inputs(
    *,
    markdown_path: Path,
    output_path: Path | None = None,
    backend: str = "story",
    page_mode: str = "a4",
) -> TrendPdfRenderInputs:
    resolved_markdown_path = markdown_path.expanduser().resolve()
    if not resolved_markdown_path.exists():
        raise ValueError(
            f"Trend markdown note does not exist: {resolved_markdown_path}"
        )
    if not resolved_markdown_path.is_file():
        raise ValueError(
            f"Trend markdown note must be a file: {resolved_markdown_path}"
        )

    resolved_output_path = (
        output_path.expanduser().resolve()
        if output_path is not None
        else resolved_markdown_path.with_suffix(".pdf")
    )
    resolved_output_path.parent.mkdir(parents=True, exist_ok=True)

    raw_markdown = resolved_markdown_path.read_text(encoding="utf-8")
    frontmatter, markdown_body = _split_yaml_frontmatter_text(raw_markdown)
    normalized_markdown = _normalize_obsidian_callouts_for_pdf(markdown_body).strip()
    if not normalized_markdown:
        normalized_markdown = "# Trend\n"

    normalized_backend = str(backend or "").strip().lower() or "story"
    normalized_page_mode = _normalize_trend_pdf_page_mode(page_mode)
    markdown = MarkdownIt("commonmark", {"html": True, "typographer": True})
    body_html = markdown.render(normalized_markdown)
    title, sections = _extract_trend_pdf_sections(body_html=body_html)

    if normalized_backend == "browser":
        document_html = _build_trend_browser_pdf_html(
            frontmatter=frontmatter,
            title=title,
            sections=sections,
        )
        css = _TREND_BROWSER_PDF_CSS
        actual_page_mode = normalized_page_mode
    else:
        decorated_body_html, decorated_title = _decorate_trend_pdf_body_html(
            body_html=body_html
        )
        title = decorated_title
        document_html = _build_trend_pdf_html(
            body_html=decorated_body_html,
            frontmatter=frontmatter,
            title=title,
        )
        css = _TREND_PDF_CSS
        actual_page_mode = "a4"

    return TrendPdfRenderInputs(
        markdown_path=resolved_markdown_path,
        output_path=resolved_output_path,
        frontmatter=frontmatter,
        raw_markdown=raw_markdown,
        normalized_markdown=normalized_markdown,
        title=title,
        document_html=document_html,
        css=css,
        renderer=normalized_backend,
        page_mode=actual_page_mode,
    )


def export_trend_note_pdf_debug_bundle(
    *,
    markdown_path: Path,
    pdf_path: Path,
    debug_dir: Path,
    prepared: TrendPdfRenderInputs | None = None,
) -> Path:
    inputs = prepared or _prepare_trend_pdf_render_inputs(
        markdown_path=markdown_path,
        output_path=pdf_path,
    )
    resolved_debug_dir = debug_dir.expanduser().resolve()
    resolved_debug_dir.mkdir(parents=True, exist_ok=True)

    files = {
        "source": "source.md",
        "normalized": "normalized.md",
        "html": "document.html",
        "css": "styles.css",
    }
    (resolved_debug_dir / files["source"]).write_text(
        inputs.raw_markdown, encoding="utf-8"
    )
    (resolved_debug_dir / files["normalized"]).write_text(
        inputs.normalized_markdown + "\n", encoding="utf-8"
    )
    (resolved_debug_dir / files["html"]).write_text(
        inputs.document_html, encoding="utf-8"
    )
    (resolved_debug_dir / files["css"]).write_text(inputs.css, encoding="utf-8")

    previews: list[str] = []
    page_count = 0
    with fitz.open(pdf_path) as document:
        page_count = len(document)
        for page_number in range(page_count):
            preview_name = f"page-{page_number + 1}.png"
            page = document.load_page(page_number)
            page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False).save(
                resolved_debug_dir / preview_name
            )
            previews.append(preview_name)

    manifest = {
        "title": inputs.title,
        "renderer": inputs.renderer,
        "page_mode": inputs.page_mode,
        "markdown_path": str(inputs.markdown_path),
        "pdf_path": str(pdf_path.expanduser().resolve()),
        "page_count": page_count,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "frontmatter": inputs.frontmatter,
        "files": {
            "source_markdown": files["source"],
            "normalized_markdown": files["normalized"],
            "document_html": files["html"],
            "styles_css": files["css"],
            "page_previews": previews,
        },
    }
    manifest_path = resolved_debug_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest_path


def _render_trend_note_pdf_story(inputs: TrendPdfRenderInputs) -> None:
    page_rect = fitz.paper_rect("a4")
    content_rect = fitz.Rect(34, 38, page_rect.width - 34, page_rect.height - 38)

    def _rect_fn(
        rect_num: int,
        _filled: fitz.Rect,
    ) -> tuple[fitz.Rect, fitz.Rect, None]:
        _ = rect_num
        return page_rect, content_rect, None

    if inputs.output_path.exists():
        inputs.output_path.unlink()
    writer = fitz.DocumentWriter(str(inputs.output_path), "compress")
    try:
        fitz.Story(inputs.document_html, user_css=inputs.css, em=11).write(
            writer, _rect_fn
        )
    finally:
        writer.close()


def _get_playwright_sync_api() -> Callable[[], Any]:
    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(
            "Playwright is unavailable for browser-based trend PDF rendering."
        ) from exc
    return sync_playwright


def _trend_pdf_browser_launch_options() -> list[dict[str, Any]]:
    raw_candidates = [
        os.environ.get("RECOLETA_PLAYWRIGHT_EXECUTABLE_PATH"),
        os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH"),
        os.environ.get("GOOGLE_CHROME_BIN"),
        os.environ.get("CHROME_BIN"),
    ]
    if sys.platform == "darwin":
        raw_candidates.extend(
            [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/Applications/Chromium.app/Contents/MacOS/Chromium",
                "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
            ]
        )
    else:
        raw_candidates.extend(
            [
                shutil.which("google-chrome"),
                shutil.which("chromium"),
                shutil.which("chromium-browser"),
                shutil.which("microsoft-edge"),
                shutil.which("msedge"),
            ]
        )

    launch_options: list[dict[str, Any]] = []
    seen: set[str] = set()
    for candidate in raw_candidates:
        if not candidate:
            continue
        candidate_path = Path(candidate).expanduser()
        if not candidate_path.exists():
            continue
        resolved = str(candidate_path.resolve())
        if resolved in seen:
            continue
        launch_options.append({"headless": True, "executable_path": resolved})
        seen.add(resolved)
    launch_options.append({"headless": True})
    return launch_options


def _compose_trend_pdf_browser_html(*, inputs: TrendPdfRenderInputs) -> str:
    return inputs.document_html.replace(
        "</head>",
        f"<style>{inputs.css}</style></head>",
        1,
    )


def _render_trend_note_pdf_browser(inputs: TrendPdfRenderInputs) -> None:
    sync_playwright = _get_playwright_sync_api()
    viewport = {"width": 794, "height": 1123}
    last_error: Exception | None = None
    launch_options_list = _trend_pdf_browser_launch_options()
    if inputs.output_path.exists():
        inputs.output_path.unlink()

    with sync_playwright() as playwright:
        for launch_kwargs in launch_options_list:
            browser = None
            try:
                browser = playwright.chromium.launch(**launch_kwargs)
                page = browser.new_page(
                    viewport=viewport,
                    device_scale_factor=1,
                    color_scheme="light",
                )
                page.set_content(
                    _compose_trend_pdf_browser_html(inputs=inputs),
                    wait_until="load",
                )
                page.emulate_media(media="screen")
                if inputs.page_mode == "continuous":
                    height_px = int(
                        page.evaluate(
                            """async () => {
                              if (document.fonts && document.fonts.ready) {
                                await document.fonts.ready;
                              }
                              const root = document.documentElement;
                              const body = document.body;
                              return Math.ceil(Math.max(
                                root.scrollHeight,
                                root.offsetHeight,
                                body.scrollHeight,
                                body.offsetHeight,
                              ));
                            }"""
                        )
                    )
                    pdf_kwargs: dict[str, Any] = {
                        "path": str(inputs.output_path),
                        "width": "210mm",
                        "height": f"{max(height_px, viewport['height'])}px",
                        "print_background": True,
                        "margin": {"top": "0", "right": "0", "bottom": "0", "left": "0"},
                    }
                else:
                    pdf_kwargs = {
                        "path": str(inputs.output_path),
                        "format": "A4",
                        "print_background": True,
                        "margin": {"top": "0", "right": "0", "bottom": "0", "left": "0"},
                    }
                page.pdf(**pdf_kwargs)
                return
            except Exception as exc:  # noqa: BLE001
                last_error = exc
            finally:
                if browser is not None:
                    browser.close()

    raise RuntimeError(
        "Browser-based trend PDF rendering failed."
    ) from last_error


def render_trend_note_pdf_result(
    *,
    markdown_path: Path,
    output_path: Path | None = None,
    backend: str = "story",
    page_mode: str = "a4",
    debug_dir: Path | None = None,
) -> TrendPdfRenderResult:
    normalized_backend = str(backend or "").strip().lower() or "story"
    if normalized_backend not in {"story", "browser", "auto"}:
        raise ValueError(
            "Trend PDF backend must be one of: story, browser, auto"
        )

    prepared: TrendPdfRenderInputs | None = None
    if normalized_backend in {"browser", "auto"}:
        try:
            prepared = _prepare_trend_pdf_render_inputs(
                markdown_path=markdown_path,
                output_path=output_path,
                backend="browser",
                page_mode=page_mode,
            )
            _render_trend_note_pdf_browser(prepared)
        except Exception as exc:  # noqa: BLE001
            if normalized_backend == "browser":
                raise
            logger.bind(
                module="publish.trends.pdf",
                requested_backend=normalized_backend,
            ).warning(
                "Trend PDF browser render failed, falling back to story error_type={} error={}",
                type(exc).__name__,
                str(exc),
            )
            prepared = None

    if prepared is None:
        prepared = _prepare_trend_pdf_render_inputs(
            markdown_path=markdown_path,
            output_path=output_path,
            backend="story",
            page_mode="a4",
        )
        _render_trend_note_pdf_story(prepared)

    if debug_dir is not None:
        export_trend_note_pdf_debug_bundle(
            markdown_path=prepared.markdown_path,
            pdf_path=prepared.output_path,
            debug_dir=debug_dir,
            prepared=prepared,
        )
    return TrendPdfRenderResult(path=prepared.output_path, prepared=prepared)


def render_trend_note_pdf(
    *,
    markdown_path: Path,
    output_path: Path | None = None,
    backend: str = "story",
    page_mode: str = "a4",
    debug_dir: Path | None = None,
) -> Path:
    return render_trend_note_pdf_result(
        markdown_path=markdown_path,
        output_path=output_path,
        backend=backend,
        page_mode=page_mode,
        debug_dir=debug_dir,
    ).path


def _format_telegram_markdownish_html(text: str) -> str:
    raw = str(text or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    if not raw:
        return ""

    codeblocks: list[str] = []

    def _stash_codeblock(match: re.Match[str]) -> str:
        code = (match.group(1) or "").strip("\n")
        token = f"\x00CB{len(codeblocks)}\x00"
        codeblocks.append(f"<pre><code>{html.escape(code)}</code></pre>")
        return token

    raw = re.sub(r"```[^\n]*\n([\s\S]*?)```", _stash_codeblock, raw)

    codespans: list[str] = []

    def _inline_to_html(line: str) -> str:
        def _apply_outside_tags(value: str, transform: Any) -> str:
            parts = re.split(r"(<[^>]+>)", value)
            for idx in range(0, len(parts), 2):
                parts[idx] = transform(parts[idx])
            return "".join(parts)

        def _stash_codespan(match: re.Match[str]) -> str:
            code = match.group(1) or ""
            token = f"\x00CS{len(codespans)}\x00"
            codespans.append(f"<code>{html.escape(code)}</code>")
            return token

        protected = re.sub(r"`([^`\n]+)`", _stash_codespan, line)
        escaped = html.escape(protected, quote=True)

        def _replace_link(match: re.Match[str]) -> str:
            label = match.group(1) or ""
            url_escaped = match.group(2) or ""
            url_unescaped = html.unescape(url_escaped)
            try:
                parsed = urlparse(url_unescaped)
            except Exception:
                return match.group(0)
            if parsed.scheme and parsed.scheme not in {"http", "https"}:
                return f"{label} ({url_escaped})"
            safe_href = html.escape(url_unescaped, quote=True)
            return f'<a href="{safe_href}">{label}</a>'

        escaped = re.sub(r"\[([^\]\n]+)\]\(([^)\s\n]+)\)", _replace_link, escaped)
        escaped = _apply_outside_tags(
            escaped,
            lambda s: re.sub(r"\*\*([^\n]+?)\*\*", r"<b>\1</b>", s),
        )
        escaped = _apply_outside_tags(
            escaped,
            lambda s: re.sub(r"__([^\n]+?)__", r"<b>\1</b>", s),
        )
        escaped = _apply_outside_tags(
            escaped,
            lambda s: re.sub(r"(?<!\*)\*([^\n]+?)\*(?!\*)", r"<i>\1</i>", s),
        )
        escaped = _apply_outside_tags(
            escaped,
            lambda s: re.sub(r"(?<!_)_([^\n]+?)_(?!_)", r"<i>\1</i>", s),
        )

        for idx, html_snippet in enumerate(codespans):
            escaped = escaped.replace(f"\x00CS{idx}\x00", html_snippet)
        return escaped

    lines: list[str] = []
    for raw_line in raw.splitlines():
        stripped = raw_line.strip()
        cb = re.fullmatch(r"\x00CB(\d+)\x00", stripped)
        if cb:
            idx = int(cb.group(1))
            if 0 <= idx < len(codeblocks):
                lines.append(codeblocks[idx])
                continue

        if not stripped:
            lines.append("")
            continue

        heading = re.match(r"^\s*#{1,6}\s+(.*)$", raw_line)
        if heading:
            content = heading.group(1).strip()
            lines.append(f"<b>{_inline_to_html(content)}</b>")
            continue

        bullet = re.match(r"^\s*[-*]\s+(.*)$", raw_line)
        if bullet:
            content = bullet.group(1).strip()
            lines.append(f"• {_inline_to_html(content)}")
            continue

        lines.append(_inline_to_html(raw_line.strip()))

    rendered = "\n".join(lines).strip()
    while "\n\n\n" in rendered:
        rendered = rendered.replace("\n\n\n", "\n\n")
    return rendered


def _truncate_telegram_text(
    *,
    raw_text: str,
    max_chars: int,
    render: Callable[[str], str],
) -> str:
    message = render(raw_text)
    if len(message) <= max_chars:
        return message
    if not raw_text:
        return render("…")[:max_chars]

    lo = 0
    hi = len(raw_text)
    best = ""
    while lo <= hi:
        mid = (lo + hi) // 2
        candidate = raw_text[:mid].rstrip()
        if candidate.count("```") % 2 == 1:
            candidate = candidate.rsplit("```", 1)[0].rstrip()
        candidate_message = render(candidate + "…")
        if len(candidate_message) <= max_chars:
            best = candidate
            lo = mid + 1
        else:
            hi = mid - 1

    if best:
        boundary = max(best.rfind("\n"), best.rfind(" "))
        if boundary >= 120:
            best = best[:boundary].rstrip()
        return render(best + "…")
    return render("…")[:max_chars]


def _link_label(value: str) -> str:
    try:
        parsed = urlparse(value)
        if parsed.netloc:
            return parsed.netloc
    except Exception:
        pass
    return "Open"


def build_telegram_message(*, title: str, summary: str, url: str) -> str:
    title_raw = str(title or "").strip() or "Untitled"
    summary_raw = str(summary or "").strip()
    url_raw = str(url or "").strip()

    def _render(summary_text: str) -> str:
        safe_title = html.escape(title_raw)
        safe_summary = _format_telegram_markdownish_html(summary_text)
        safe_url_attr = html.escape(url_raw, quote=True)
        safe_label = html.escape(_link_label(url_raw))
        return "\n".join(
            [
                f"<b>{safe_title}</b>",
                "",
                "<b>Summary:</b>",
                safe_summary,
                "",
                f'<b>Link:</b> <a href="{safe_url_attr}">{safe_label}</a>',
            ]
        ).strip()

    return _truncate_telegram_text(raw_text=summary_raw, max_chars=4096, render=_render)


def build_telegram_trend_document_caption(
    *,
    title: str,
    overview_md: str,
    granularity: str,
    period_start: datetime,
) -> str:
    title_raw = str(title or "").strip() or "Trend"
    overview_raw = str(overview_md or "").strip()
    period_token = _trend_date_token(
        granularity=granularity,
        period_start=period_start,
    )
    period_label = f"{str(granularity or '').strip().title()} · {period_token}".strip(
        " ·"
    )

    def _render(overview_text: str) -> str:
        safe_title = html.escape(title_raw)
        safe_overview = _format_telegram_markdownish_html(overview_text)
        safe_period = html.escape(period_label)
        return "\n".join(
            [
                f"<b>{safe_title}</b>",
                "",
                "<b>Overview:</b>",
                safe_overview,
                "",
                f"<b>Period:</b> {safe_period}",
            ]
        ).strip()

    return _truncate_telegram_text(raw_text=overview_raw, max_chars=1024, render=_render)
