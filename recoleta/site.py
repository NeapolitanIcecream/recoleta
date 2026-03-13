from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
import html
import json
import os
from pathlib import Path
import re
import shutil
from typing import Any
from urllib.parse import quote, urlparse

from bs4 import BeautifulSoup
from loguru import logger
from markdown_it import MarkdownIt
from slugify import slugify

from recoleta.publish.trend_render_shared import (
    _build_trend_browser_body_html,
    _extract_trend_pdf_sections,
    _normalize_obsidian_callouts_for_pdf,
    _split_yaml_frontmatter_text,
    _trend_date_token,
    _trend_pdf_hero_dek,
    _trend_pdf_meta_rows,
    _trend_pdf_topics_summary,
    sanitize_trend_title,
)


@dataclass(slots=True)
class TrendSiteDocument:
    markdown_path: Path
    markdown_asset_path: Path
    pdf_asset_path: Path | None
    page_path: Path
    stem: str
    title: str
    granularity: str
    period_token: str
    period_start: datetime | None
    period_end: datetime | None
    topics: list[str]
    stream: str | None
    body_html: str
    excerpt: str
    frontmatter: dict[str, Any]


@dataclass(slots=True)
class TrendSiteInputDirectory:
    path: Path
    root_path: Path
    inbox_path: Path | None
    stream: str | None


@dataclass(slots=True)
class TrendSiteSourceDocument:
    markdown_path: Path
    pdf_path: Path | None
    stem: str
    frontmatter: dict[str, Any]
    markdown_body: str
    granularity: str
    period_start: datetime | None
    period_end: datetime | None
    topics: list[str]
    stream: str | None


@dataclass(slots=True)
class ItemSiteSourceDocument:
    markdown_path: Path
    stem: str
    frontmatter: dict[str, Any]
    markdown_body: str
    title: str
    canonical_url: str
    source: str
    published_at: datetime | None
    authors: list[str]
    topics: list[str]
    relevance_score: float | None
    stream: str | None


@dataclass(slots=True)
class ItemSiteDocument:
    markdown_path: Path
    markdown_asset_path: Path
    page_path: Path
    stem: str
    title: str
    canonical_url: str
    source: str
    published_at: datetime | None
    authors: list[str]
    topics: list[str]
    stream: str | None
    relevance_score: float | None
    body_html: str
    excerpt: str
    frontmatter: dict[str, Any]


def _parse_site_datetime(value: Any) -> datetime | None:
    raw = str(value or "").strip()
    if not raw:
        return None
    try:
        parsed = datetime.fromisoformat(raw)
    except Exception:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def _parse_site_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _safe_excerpt(value: str, *, limit: int = 220) -> str:
    collapsed = " ".join(str(value or "").split()).strip()
    collapsed = re.sub(r"\s+([,.;:!?])", r"\1", collapsed)
    collapsed = re.sub(r"\s+([，。；：！？）】》])", r"\1", collapsed)
    if len(collapsed) <= limit:
        return collapsed
    boundary = collapsed.rfind(" ", 0, limit)
    if boundary < max(80, limit // 2):
        boundary = limit
    return collapsed[:boundary].rstrip() + "…"


def _section_excerpt(sections: list[Any]) -> str:
    preferred_html = ""
    for section in sections:
        heading = str(getattr(section, "heading", "") or "").strip().lower()
        if "overview" in heading or "summary" in heading or "tl;dr" in heading:
            preferred_html = str(getattr(section, "inner_html", "") or "")
            break
    if not preferred_html and sections:
        preferred_html = str(getattr(sections[0], "inner_html", "") or "")
    text = BeautifulSoup(preferred_html, "html.parser").get_text(" ", strip=True)
    return _safe_excerpt(text, limit=220)


def _site_href(*, from_page: Path, to_page: Path) -> str:
    relative = Path(os.path.relpath(to_page, start=from_page.parent))
    return "/".join(
        part if part in {".", ".."} else quote(part) for part in relative.parts
    )


def _host_matches(*, host: str, domain: str) -> bool:
    normalized_host = str(host or "").strip().lower().rstrip(".")
    normalized_domain = str(domain or "").strip().lower().rstrip(".")
    if not normalized_host or not normalized_domain:
        return False
    return normalized_host == normalized_domain or normalized_host.endswith(
        f".{normalized_domain}"
    )


def _item_action_label(*, source: str | None, canonical_url: str) -> str:
    normalized_source = str(source or "").strip().lower()
    host = (urlparse(str(canonical_url or "")).hostname or "").lower()
    if _host_matches(host=host, domain="arxiv.org") or normalized_source == "arxiv":
        return "Open arXiv"
    if _host_matches(host=host, domain="openreview.net") or normalized_source == "openreview":
        return "Open OpenReview"
    if _host_matches(host=host, domain="github.com"):
        return "Open GitHub"
    return "Open original"


def _topic_slug(topic: str) -> str:
    return slugify(str(topic or "").strip(), lowercase=True) or "topic"


def _stream_slug(stream: str) -> str:
    return slugify(str(stream or "").strip(), lowercase=True) or "stream"


def _paths_overlap(path_a: Path, path_b: Path) -> bool:
    return path_a == path_b or path_a in path_b.parents or path_b in path_a.parents


_TREND_GRANULARITY_SORT_PRIORITY = {
    "month": 3,
    "week": 2,
    "day": 1,
}


def _trend_site_sort_key(
    document: TrendSiteSourceDocument,
) -> tuple[datetime, int, datetime, str]:
    floor = datetime.min.replace(tzinfo=timezone.utc)
    return (
        document.period_end or document.period_start or floor,
        _TREND_GRANULARITY_SORT_PRIORITY.get(document.granularity, 0),
        document.period_start or floor,
        document.stem,
    )


def _reset_directory(path: Path) -> None:
    if path.exists():
        if not path.is_dir():
            raise ValueError(f"Output path must be a directory: {path}")
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def _remove_managed_stage_path(path: Path) -> None:
    if not path.exists():
        return
    if path.is_dir():
        shutil.rmtree(path)
        return
    path.unlink()


def _reset_stage_output_root(*, stage_root: Path, trends_output_dir: Path) -> None:
    if stage_root == trends_output_dir:
        _reset_directory(trends_output_dir)
        return
    _remove_managed_stage_path(trends_output_dir)
    _remove_managed_stage_path(stage_root / "Inbox")
    _remove_managed_stage_path(stage_root / "Streams")
    trends_output_dir.mkdir(parents=True, exist_ok=True)


def _coerce_site_input_paths(input_dir: Path | Sequence[Path]) -> list[Path]:
    raw_inputs = [input_dir] if isinstance(input_dir, Path) else list(input_dir)
    if not raw_inputs:
        raise ValueError("Trend input directory list must not be empty")

    resolved_inputs: list[Path] = []
    for raw_input in raw_inputs:
        resolved_input = raw_input.expanduser().resolve()
        if not resolved_input.exists() or not resolved_input.is_dir():
            raise ValueError(f"Trend input directory must exist: {resolved_input}")
        resolved_inputs.append(resolved_input)
    return resolved_inputs


def _infer_stream_name_from_trends_dir(path: Path) -> str | None:
    if path.name != "Trends":
        return None
    if len(path.parts) < 3:
        return None
    if path.parent.parent.name != "Streams":
        return None
    return path.parent.name


def _discover_trend_site_input_dirs(
    raw_inputs: Sequence[Path],
) -> list[TrendSiteInputDirectory]:
    discovered: list[TrendSiteInputDirectory] = []
    seen_paths: set[Path] = set()

    def add_candidate(candidate: Path) -> None:
        resolved_candidate = candidate.expanduser().resolve()
        if not resolved_candidate.exists() or not resolved_candidate.is_dir():
            return
        if resolved_candidate in seen_paths:
            return
        seen_paths.add(resolved_candidate)
        root_path = (
            resolved_candidate.parent
            if resolved_candidate.name == "Trends"
            else resolved_candidate
        )
        inbox_path = root_path / "Inbox"
        discovered.append(
            TrendSiteInputDirectory(
                path=resolved_candidate,
                root_path=root_path,
                inbox_path=inbox_path if inbox_path.exists() and inbox_path.is_dir() else None,
                stream=_infer_stream_name_from_trends_dir(resolved_candidate),
            )
        )

    for raw_input in raw_inputs:
        candidates: list[Path] = []
        if raw_input.name == "Trends":
            candidates.append(raw_input)

        direct_trends_dir = raw_input / "Trends"
        if direct_trends_dir.exists() and direct_trends_dir.is_dir():
            candidates.append(direct_trends_dir)

        streams_root = raw_input if raw_input.name == "Streams" else raw_input / "Streams"
        if streams_root.exists() and streams_root.is_dir():
            candidates.extend(
                path
                for path in sorted(streams_root.glob("*/Trends"))
                if path.is_dir()
            )

        if not candidates:
            candidates.append(raw_input)

        for candidate in candidates:
            add_candidate(candidate)

    return discovered


def _render_topic_link_pills(
    *,
    topics: list[str],
    from_page: Path,
    topic_pages: dict[str, Path],
) -> str:
    if not topics:
        return "<span class='meta-pill subdued'>No tracked topics</span>"
    pills: list[str] = []
    seen: set[str] = set()
    for topic in topics:
        cleaned = str(topic).strip()
        if not cleaned:
            continue
        slug = _topic_slug(cleaned)
        if slug in seen:
            continue
        seen.add(slug)
        topic_page = topic_pages.get(slug)
        if topic_page is None:
            pills.append(f"<span class='topic-pill'>{html.escape(cleaned)}</span>")
            continue
        href = _site_href(from_page=from_page, to_page=topic_page)
        pills.append(
            f"<a class='topic-pill topic-pill-link' href='{href}'>{html.escape(cleaned)}</a>"
        )
    return "".join(pills) if pills else "<span class='meta-pill subdued'>No tracked topics</span>"


def _render_stream_link_pill(
    *,
    stream: str | None,
    from_page: Path,
    stream_pages: dict[str, Path],
) -> str:
    cleaned = str(stream or "").strip()
    if not cleaned:
        return ""
    slug = _stream_slug(cleaned)
    page_path = stream_pages.get(slug)
    if page_path is None:
        return f"<span class='meta-pill stream-pill'>{html.escape(cleaned)}</span>"
    href = _site_href(from_page=from_page, to_page=page_path)
    return (
        "<a class='meta-pill stream-pill stream-pill-link' href='{}'>{}</a>".format(
            href,
            html.escape(cleaned),
        )
    )


def _site_page_shell(
    *,
    title: str,
    page_path: Path,
    output_dir: Path,
    page_heading: str,
    page_subtitle: str,
    body_class: str,
    active_nav: str,
    content_html: str,
    show_page_hero: bool = False,
) -> str:
    stylesheet_path = output_dir / "assets" / "site.css"
    stylesheet_href = _site_href(from_page=page_path, to_page=stylesheet_path)
    index_href = _site_href(from_page=page_path, to_page=output_dir / "index.html")
    archive_href = _site_href(from_page=page_path, to_page=output_dir / "archive.html")
    topics_href = _site_href(from_page=page_path, to_page=output_dir / "topics" / "index.html")
    streams_href = _site_href(
        from_page=page_path,
        to_page=output_dir / "streams" / "index.html",
    )

    def nav_link(label: str, href: str, key: str) -> str:
        class_name = "nav-link is-active" if key == active_nav else "nav-link"
        return f"<a class='{class_name}' href='{href}'>{label}</a>"

    nav_caption_html = (
        f"<div class='nav-caption'>{html.escape(page_subtitle)}</div>"
        if page_subtitle
        else ""
    )
    page_hero_html = (
        "<section class='page-hero'>"
        f"<div class='hero-kicker'>{html.escape(page_subtitle)}</div>"
        f"<h1 class='page-title'>{html.escape(page_heading)}</h1>"
        "</section>"
        if show_page_hero
        else ""
    )

    return (
        "<!doctype html>"
        "<html lang='zh-CN'>"
        "<head>"
        "<meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width, initial-scale=1'>"
        f"<title>{html.escape(title)}</title>"
        "<meta name='theme-color' content='#10273f'>"
        f"<link rel='stylesheet' href='{stylesheet_href}'>"
        "</head>"
        f"<body class='{body_class}'>"
        "<div class='site-bg'></div>"
        "<div class='site-shell'>"
        "<header class='site-header'>"
        "<div class='nav-brand-wrap'>"
        f"<a class='nav-brand' href='{index_href}'>Recoleta Trends</a>"
        f"{nav_caption_html}"
        "</div>"
        "<nav class='nav-links'>"
        f"{nav_link('Home', index_href, 'home')}"
        f"{nav_link('Archive', archive_href, 'archive')}"
        f"{nav_link('Topics', topics_href, 'topics')}"
        f"{nav_link('Streams', streams_href, 'streams')}"
        "</nav>"
        "</header>"
        "<main class='site-main'>"
        f"{page_hero_html}"
        f"{content_html}"
        "</main>"
        "</div>"
        "</body>"
        "</html>"
    )


def _render_trend_card(
    *,
    document: TrendSiteDocument,
    from_page: Path,
    topic_pages: dict[str, Path],
    stream_pages: dict[str, Path],
) -> str:
    trend_href = _site_href(from_page=from_page, to_page=document.page_path)
    pdf_href = (
        _site_href(from_page=from_page, to_page=document.pdf_asset_path)
        if document.pdf_asset_path is not None
        else None
    )
    markdown_href = _site_href(from_page=from_page, to_page=document.markdown_asset_path)
    topic_links = _render_topic_link_pills(
        topics=document.topics[:4],
        from_page=from_page,
        topic_pages=topic_pages,
    )
    stream_link = _render_stream_link_pill(
        stream=document.stream,
        from_page=from_page,
        stream_pages=stream_pages,
    )
    meta_pills = [f"<span class='meta-pill'>{html.escape(document.granularity.title())}</span>"]
    if stream_link:
        meta_pills.append(stream_link)
    actions = [
        f"<a class='action-link' href='{trend_href}'>Open brief</a>",
        f"<a class='action-link secondary' href='{markdown_href}'>Markdown</a>",
    ]
    if pdf_href is not None:
        actions.insert(1, f"<a class='action-link secondary' href='{pdf_href}'>PDF</a>")
    return (
        "<article class='trend-card'>"
        "<div class='card-meta-row'>"
        f"<div class='card-pill-row'>{''.join(meta_pills)}</div>"
        f"<span class='meta-date'>{html.escape(document.period_token)}</span>"
        "</div>"
        f"<h2 class='card-title'><a href='{trend_href}'>{html.escape(document.title)}</a></h2>"
        f"<p class='card-excerpt'>{html.escape(document.excerpt)}</p>"
        f"<div class='topic-pill-row'>{topic_links}</div>"
        f"<div class='card-actions'>{''.join(actions)}</div>"
        "</article>"
    )


def _render_topic_card(
    *,
    topic: str,
    count: int,
    latest_token: str,
    page_path: Path,
    topic_page_path: Path,
) -> str:
    href = _site_href(from_page=page_path, to_page=topic_page_path)
    return (
        "<article class='topic-card'>"
        f"<h2 class='topic-card-title'><a href='{href}'>{html.escape(topic)}</a></h2>"
        f"<div class='topic-card-meta'>{count} briefs · latest {html.escape(latest_token)}</div>"
        "</article>"
    )


def _render_stream_card(
    *,
    stream: str,
    count: int,
    latest_token: str,
    page_path: Path,
    stream_page_path: Path,
) -> str:
    href = _site_href(from_page=page_path, to_page=stream_page_path)
    return (
        "<article class='topic-card'>"
        f"<h2 class='topic-card-title'><a href='{href}'>{html.escape(stream)}</a></h2>"
        f"<div class='topic-card-meta'>{count} briefs · latest {html.escape(latest_token)}</div>"
        "</article>"
    )


def _render_archive_rows(*, documents: list[TrendSiteDocument], from_page: Path) -> str:
    rows: list[str] = []
    grouped: dict[str, list[TrendSiteDocument]] = defaultdict(list)
    for document in documents:
        period_start = document.period_start
        month_key = (
            period_start.astimezone(timezone.utc).strftime("%Y-%m")
            if period_start is not None
            else "Unknown"
        )
        grouped[month_key].append(document)

    for month_key in sorted(grouped.keys(), reverse=True):
        month_documents = grouped[month_key]
        items = "".join(
            "<li class='archive-item'>"
            f"<a href='{_site_href(from_page=from_page, to_page=document.page_path)}'>{html.escape(document.title)}</a>"
            f"<span>{html.escape(document.granularity.title())} · {html.escape(document.period_token)}"
            + (
                f" · {html.escape(document.stream)}"
                if document.stream
                else ""
            )
            + "</span>"
            "</li>"
            for document in month_documents
        )
        rows.append(
            "<section class='archive-block'>"
            f"<h2 class='section-title'>{html.escape(month_key)}</h2>"
            f"<ul class='archive-list'>{items}</ul>"
            "</section>"
        )
    return "".join(rows)


def _render_detail_page(
    *,
    document: TrendSiteDocument,
    output_dir: Path,
    topic_pages: dict[str, Path],
    stream_pages: dict[str, Path],
    previous_document: TrendSiteDocument | None,
    next_document: TrendSiteDocument | None,
) -> str:
    breadcrumb_home = _site_href(from_page=document.page_path, to_page=output_dir / "index.html")
    breadcrumb_archive = _site_href(from_page=document.page_path, to_page=output_dir / "archive.html")
    markdown_href = _site_href(
        from_page=document.page_path,
        to_page=document.markdown_asset_path,
    )
    pdf_href = (
        _site_href(from_page=document.page_path, to_page=document.pdf_asset_path)
        if document.pdf_asset_path is not None
        else None
    )
    topic_links = _render_topic_link_pills(
        topics=document.topics,
        from_page=document.page_path,
        topic_pages=topic_pages,
    )
    stream_link = _render_stream_link_pill(
        stream=document.stream,
        from_page=document.page_path,
        stream_pages=stream_pages,
    )
    meta_items = "".join(
        "<div class='meta-panel'>"
        f"<div class='meta-panel-label'>{html.escape(label)}</div>"
        f"<div class='meta-panel-value'>{html.escape(value)}</div>"
        "</div>"
        for label, value in _trend_pdf_meta_rows(document.frontmatter)
    )

    pager_items: list[str] = []
    if previous_document is not None:
        previous_href = _site_href(
            from_page=document.page_path,
            to_page=previous_document.page_path,
        )
        pager_items.append(
            "<a class='pager-card' href='{}'><span>Newer</span><strong>{}</strong></a>".format(
                previous_href, html.escape(previous_document.title)
            )
        )
    if next_document is not None:
        next_href = _site_href(from_page=document.page_path, to_page=next_document.page_path)
        pager_items.append(
            "<a class='pager-card' href='{}'><span>Older</span><strong>{}</strong></a>".format(
                next_href, html.escape(next_document.title)
            )
        )

    action_links = [
        f"<a class='action-link' href='{markdown_href}'>Source markdown</a>",
    ]
    if pdf_href is not None:
        action_links.insert(0, f"<a class='action-link' href='{pdf_href}'>Download PDF</a>")

    detail_stream_html = (
        f"<div class='detail-stream-row'>{stream_link}</div>" if stream_link else ""
    )
    pager_html = (
        f"<section class='pager-row'>{''.join(pager_items)}</section>"
        if pager_items
        else ""
    )
    content_html = (
        "<nav class='breadcrumbs'>"
        f"<a href='{breadcrumb_home}'>Home</a>"
        "<span>/</span>"
        f"<a href='{breadcrumb_archive}'>Archive</a>"
        "<span>/</span>"
        f"<span>{html.escape(document.period_token)}</span>"
        "</nav>"
        "<section class='detail-hero'>"
        "<div class='detail-hero-main'>"
        f"<div class='hero-kicker'>{html.escape(document.granularity.title())} · {html.escape(document.period_token)}</div>"
        f"<h1 class='detail-title'>{html.escape(document.title)}</h1>"
        f"<p class='detail-dek'>{html.escape(document.excerpt or _trend_pdf_hero_dek(document.frontmatter))}</p>"
        f"<div class='detail-summary'>{html.escape(_trend_pdf_topics_summary(document.frontmatter))}</div>"
        f"{detail_stream_html}"
        f"<div class='topic-pill-row'>{topic_links}</div>"
        f"<div class='card-actions detail-actions'>{''.join(action_links)}</div>"
        "</div>"
        "<aside class='detail-hero-side'>"
        f"{meta_items}"
        "</aside>"
        "</section>"
        f"<section class='detail-content'>{document.body_html}</section>"
        f"{pager_html}"
    )

    return _site_page_shell(
        title=document.title,
        page_path=document.page_path,
        output_dir=output_dir,
        page_heading=document.title,
        page_subtitle="",
        body_class="page-detail",
        active_nav="archive",
        content_html=content_html,
    )


def _render_item_page(
    *,
    document: ItemSiteDocument,
    output_dir: Path,
    topic_pages: dict[str, Path],
    stream_pages: dict[str, Path],
) -> str:
    breadcrumb_home = _site_href(from_page=document.page_path, to_page=output_dir / "index.html")
    markdown_href = _site_href(
        from_page=document.page_path,
        to_page=document.markdown_asset_path,
    )
    topic_links = _render_topic_link_pills(
        topics=document.topics,
        from_page=document.page_path,
        topic_pages=topic_pages,
    )
    stream_link = _render_stream_link_pill(
        stream=document.stream,
        from_page=document.page_path,
        stream_pages=stream_pages,
    )
    meta_rows: list[tuple[str, str]] = [
        ("Source", document.source or "Item"),
        (
            "Published",
            document.published_at.astimezone(timezone.utc).date().isoformat()
            if document.published_at is not None
            else "Unknown",
        ),
    ]
    if document.relevance_score is not None:
        meta_rows.append(("Relevance", f"{document.relevance_score:.2f}"))
    if document.authors:
        authors_value = "; ".join(document.authors[:6])
        if len(document.authors) > 6:
            authors_value += "; …"
        meta_rows.append(("Authors", authors_value))
    meta_items = "".join(
        "<div class='meta-panel'>"
        f"<div class='meta-panel-label'>{html.escape(label)}</div>"
        f"<div class='meta-panel-value'>{html.escape(value)}</div>"
        "</div>"
        for label, value in meta_rows
    )
    action_links = [f"<a class='action-link' href='{markdown_href}'>Source markdown</a>"]
    if document.canonical_url:
        action_links.insert(
            0,
            "<a class='action-link' href='{}'>{}</a>".format(
                html.escape(document.canonical_url, quote=True),
                html.escape(
                    _item_action_label(
                        source=document.source,
                        canonical_url=document.canonical_url,
                    )
                ),
            ),
        )
    detail_stream_html = (
        f"<div class='detail-stream-row'>{stream_link}</div>" if stream_link else ""
    )
    content_html = (
        "<nav class='breadcrumbs'>"
        f"<a href='{breadcrumb_home}'>Home</a>"
        "<span>/</span>"
        "<span>Item</span>"
        "</nav>"
        "<section class='detail-hero'>"
        "<div class='detail-hero-main'>"
        "<div class='hero-kicker'>Recoleta Item Note</div>"
        f"<h1 class='detail-title'>{html.escape(document.title)}</h1>"
        f"<p class='detail-dek'>{html.escape(document.excerpt or 'Curated item note with summary and source metadata.')}</p>"
        f"{detail_stream_html}"
        f"<div class='topic-pill-row'>{topic_links}</div>"
        f"<div class='card-actions detail-actions'>{''.join(action_links)}</div>"
        "</div>"
        "<aside class='detail-hero-side'>"
        f"{meta_items}"
        "</aside>"
        "</section>"
        f"<section class='detail-content'>{document.body_html}</section>"
    )
    return _site_page_shell(
        title=f"{document.title} · Recoleta",
        page_path=document.page_path,
        output_dir=output_dir,
        page_heading=document.title,
        page_subtitle="",
        body_class="page-item",
        active_nav="archive",
        content_html=content_html,
    )


def _render_home_page(
    *,
    documents: list[TrendSiteDocument],
    output_dir: Path,
    topic_pages: dict[str, Path],
    stream_pages: dict[str, Path],
) -> str:
    page_path = output_dir / "index.html"
    latest_cards = "".join(
        _render_trend_card(
            document=document,
            from_page=page_path,
            topic_pages=topic_pages,
            stream_pages=stream_pages,
        )
        for document in documents[:6]
    )

    topic_counter: Counter[str] = Counter()
    latest_by_topic: dict[str, TrendSiteDocument] = {}
    label_by_slug: dict[str, str] = {}
    for document in documents:
        for topic in document.topics:
            cleaned = str(topic).strip()
            if not cleaned:
                continue
            slug = _topic_slug(cleaned)
            topic_counter[slug] += 1
            label_by_slug.setdefault(slug, cleaned)
            latest_by_topic.setdefault(slug, document)

    topic_cards = "".join(
        _render_topic_card(
            topic=label_by_slug[slug],
            count=topic_counter[slug],
            latest_token=latest_by_topic[slug].period_token,
            page_path=page_path,
            topic_page_path=topic_pages[slug],
        )
        for slug, _count in topic_counter.most_common(12)
        if slug in topic_pages
    )

    stream_counter: Counter[str] = Counter()
    latest_by_stream: dict[str, TrendSiteDocument] = {}
    for document in documents:
        cleaned_stream = str(document.stream or "").strip()
        if not cleaned_stream:
            continue
        slug = _stream_slug(cleaned_stream)
        stream_counter[slug] += 1
        latest_by_stream.setdefault(slug, document)

    stream_cards = "".join(
        _render_stream_card(
            stream=latest_by_stream[slug].stream or slug,
            count=stream_counter[slug],
            latest_token=latest_by_stream[slug].period_token,
            page_path=page_path,
            stream_page_path=stream_pages[slug],
        )
        for slug, _count in stream_counter.most_common(12)
        if slug in stream_pages
    )

    archive_preview = "".join(
        "<li class='timeline-item'>"
        f"<a href='{_site_href(from_page=page_path, to_page=document.page_path)}'>{html.escape(document.title)}</a>"
        f"<span>{html.escape(document.period_token)}</span>"
        "</li>"
        for document in documents[:8]
    )

    generated_span = ""
    if documents:
        newest = documents[0].period_token
        oldest = documents[-1].period_token
        generated_span = f"{oldest} to {newest}"

    stream_section_html = (
        "<section class='home-section'>"
        "<div class='section-heading-row'>"
        "<h2 class='section-title'>Topic streams</h2>"
        "</div>"
        f"<div class='topic-card-grid'>{stream_cards}</div>"
        "</section>"
        if stream_cards
        else ""
    )
    content_html = (
        "<section class='home-hero-card'>"
        "<div class='home-hero-copy'>"
        "<div class='hero-kicker'>Browse trend briefs</div>"
        "<h1 class='home-title'>Latest research trends</h1>"
        "<p class='home-dek'>"
        "Scan recent briefs, jump by topic or stream, and open the full note when"
        " needed."
        "</p>"
        "<div class='hero-actions'>"
        f"<a class='action-link' href='{_site_href(from_page=page_path, to_page=output_dir / 'archive.html')}'>Open archive</a>"
        f"<a class='action-link secondary' href='{_site_href(from_page=page_path, to_page=output_dir / 'topics' / 'index.html')}'>Browse topics</a>"
        "</div>"
        "</div>"
        "<div class='hero-stats'>"
        f"<div class='meta-panel'><div class='meta-panel-label'>Briefs</div><div class='meta-panel-value'>{len(documents)}</div></div>"
        f"<div class='meta-panel'><div class='meta-panel-label'>Topics</div><div class='meta-panel-value'>{len(topic_pages)}</div></div>"
        f"<div class='meta-panel'><div class='meta-panel-label'>Window</div><div class='meta-panel-value'>{html.escape(generated_span or 'n/a')}</div></div>"
        "</div>"
        "</section>"
        "<section class='home-section'>"
        "<div class='section-heading-row'>"
        "<h2 class='section-title'>Latest briefs</h2>"
        "</div>"
        f"<div class='trend-grid'>{latest_cards or '<div class=\"empty-card\">No trend notes available yet.</div>'}</div>"
        "</section>"
        f"{stream_section_html}"
        "<section class='home-section split-layout'>"
        "<div>"
        "<h2 class='section-title'>Topic radar</h2>"
        f"<div class='topic-card-grid'>{topic_cards or '<div class=\"empty-card\">No topics available yet.</div>'}</div>"
        "</div>"
        "<div>"
        "<h2 class='section-title'>Archive preview</h2>"
        f"<ul class='timeline-list'>{archive_preview or '<li class=\"timeline-item empty\">No archive entries yet.</li>'}</ul>"
        "</div>"
        "</section>"
    )

    return _site_page_shell(
        title="Recoleta Trends",
        page_path=page_path,
        output_dir=output_dir,
        page_heading="Recoleta Trends",
        page_subtitle="",
        body_class="page-home",
        active_nav="home",
        content_html=content_html,
    )


def _render_topics_index_page(
    *,
    documents: list[TrendSiteDocument],
    output_dir: Path,
    topic_pages: dict[str, Path],
) -> str:
    page_path = output_dir / "topics" / "index.html"
    topic_counter: Counter[str] = Counter()
    latest_by_topic: dict[str, TrendSiteDocument] = {}
    label_by_slug: dict[str, str] = {}

    for document in documents:
        for topic in document.topics:
            cleaned = str(topic).strip()
            if not cleaned:
                continue
            slug = _topic_slug(cleaned)
            topic_counter[slug] += 1
            label_by_slug.setdefault(slug, cleaned)
            latest_by_topic.setdefault(slug, document)

    cards = "".join(
        _render_topic_card(
            topic=label_by_slug[slug],
            count=topic_counter[slug],
            latest_token=latest_by_topic[slug].period_token,
            page_path=page_path,
            topic_page_path=topic_pages[slug],
        )
        for slug, _count in topic_counter.most_common()
        if slug in topic_pages
    )

    content_html = (
        "<section class='home-section'>"
        "<h1 class='section-title page-section-title'>All tracked topics</h1>"
        f"<div class='topic-card-grid'>{cards or '<div class=\"empty-card\">No topics available yet.</div>'}</div>"
        "</section>"
    )

    return _site_page_shell(
        title="Topics · Recoleta Trends",
        page_path=page_path,
        output_dir=output_dir,
        page_heading="Topics",
        page_subtitle="",
        body_class="page-topics",
        active_nav="topics",
        content_html=content_html,
    )


def _render_streams_index_page(
    *,
    documents: list[TrendSiteDocument],
    output_dir: Path,
    stream_pages: dict[str, Path],
) -> str:
    page_path = output_dir / "streams" / "index.html"
    stream_counter: Counter[str] = Counter()
    latest_by_stream: dict[str, TrendSiteDocument] = {}

    for document in documents:
        cleaned_stream = str(document.stream or "").strip()
        if not cleaned_stream:
            continue
        slug = _stream_slug(cleaned_stream)
        stream_counter[slug] += 1
        latest_by_stream.setdefault(slug, document)

    cards = "".join(
        _render_stream_card(
            stream=latest_by_stream[slug].stream or slug,
            count=stream_counter[slug],
            latest_token=latest_by_stream[slug].period_token,
            page_path=page_path,
            stream_page_path=stream_pages[slug],
        )
        for slug, _count in stream_counter.most_common()
        if slug in stream_pages
    )

    content_html = (
        "<section class='home-section'>"
        "<h1 class='section-title page-section-title'>Topic streams</h1>"
        f"<div class='topic-card-grid'>{cards or '<div class=\"empty-card\">No topic streams available yet.</div>'}</div>"
        "</section>"
    )

    return _site_page_shell(
        title="Streams · Recoleta Trends",
        page_path=page_path,
        output_dir=output_dir,
        page_heading="Streams",
        page_subtitle="",
        body_class="page-streams",
        active_nav="streams",
        content_html=content_html,
    )


def _render_topic_page(
    *,
    topic: str,
    topic_slug: str,
    documents: list[TrendSiteDocument],
    output_dir: Path,
    topic_pages: dict[str, Path],
    stream_pages: dict[str, Path],
) -> str:
    page_path = topic_pages[topic_slug]
    cards = "".join(
        _render_trend_card(
            document=document,
            from_page=page_path,
            topic_pages=topic_pages,
            stream_pages=stream_pages,
        )
        for document in documents
    )
    content_html = (
        "<section class='home-section'>"
        "<div class='section-heading-row'>"
        f"<h1 class='section-title page-section-title'>{html.escape(topic)}</h1>"
        f"<span class='meta-date'>{len(documents)} briefs</span>"
        "</div>"
        f"<div class='trend-grid'>{cards}</div>"
        "</section>"
    )
    return _site_page_shell(
        title=f"{topic} · Recoleta Trends",
        page_path=page_path,
        output_dir=output_dir,
        page_heading=topic,
        page_subtitle="",
        body_class="page-topic",
        active_nav="topics",
        content_html=content_html,
    )


def _render_stream_page(
    *,
    stream: str,
    stream_slug: str,
    documents: list[TrendSiteDocument],
    output_dir: Path,
    topic_pages: dict[str, Path],
    stream_pages: dict[str, Path],
) -> str:
    page_path = stream_pages[stream_slug]
    cards = "".join(
        _render_trend_card(
            document=document,
            from_page=page_path,
            topic_pages=topic_pages,
            stream_pages=stream_pages,
        )
        for document in documents
    )
    content_html = (
        "<section class='home-section'>"
        "<div class='section-heading-row'>"
        f"<h1 class='section-title page-section-title'>{html.escape(stream)}</h1>"
        f"<span class='meta-date'>{len(documents)} briefs</span>"
        "</div>"
        f"<div class='trend-grid'>{cards}</div>"
        "</section>"
    )
    return _site_page_shell(
        title=f"{stream} · Recoleta Trends",
        page_path=page_path,
        output_dir=output_dir,
        page_heading=stream,
        page_subtitle="",
        body_class="page-stream",
        active_nav="streams",
        content_html=content_html,
    )


def _render_archive_page(*, documents: list[TrendSiteDocument], output_dir: Path) -> str:
    page_path = output_dir / "archive.html"
    content_html = (
        "<section class='home-section'>"
        "<h1 class='section-title page-section-title'>Archive</h1>"
        f"{_render_archive_rows(documents=documents, from_page=page_path)}"
        "</section>"
    )
    return _site_page_shell(
        title="Archive · Recoleta Trends",
        page_path=page_path,
        output_dir=output_dir,
        page_heading="Archive",
        page_subtitle="",
        body_class="page-archive",
        active_nav="archive",
        content_html=content_html,
    )


_SITE_CSS = """
:root {
  --bg-top: #dce7f2;
  --bg-bottom: #f7fafc;
  --panel: rgba(255, 255, 255, 0.82);
  --panel-strong: rgba(250, 252, 255, 0.94);
  --line: rgba(17, 41, 71, 0.10);
  --text: #162235;
  --muted: #60748a;
  --accent: #1d67c2;
  --accent-soft: #eaf2fb;
  --hero-start: #10273f;
  --hero-end: #2a5f95;
  --radius-xl: 30px;
  --radius-lg: 22px;
  --radius-md: 16px;
  --shadow-lg: 0 22px 60px rgba(22, 40, 69, 0.10);
  --shadow-md: 0 14px 36px rgba(22, 40, 69, 0.08);
}
* {
  box-sizing: border-box;
}
html, body {
  margin: 0;
  min-height: 100%;
}
body {
  color: var(--text);
  background:
    radial-gradient(circle at top left, rgba(255, 255, 255, 0.68), transparent 28%),
    radial-gradient(circle at top right, rgba(29, 103, 194, 0.10), transparent 24%),
    linear-gradient(180deg, var(--bg-top) 0%, #eaf1f7 35%, var(--bg-bottom) 100%);
  font-family: "PingFang SC", "Hiragino Sans GB", "Helvetica Neue", "Segoe UI", sans-serif;
  overflow-x: hidden;
}
a {
  color: var(--accent);
  text-decoration: none;
}
img,
svg,
video,
iframe {
  max-width: 100%;
  height: auto;
}
.site-shell {
  position: relative;
  width: min(1240px, calc(100% - 32px));
  margin: 0 auto;
  padding: 22px 0 48px;
}
.site-header {
  position: sticky;
  top: 12px;
  z-index: 20;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 20px;
  padding: 16px 18px;
  border: 1px solid rgba(255, 255, 255, 0.42);
  border-radius: 999px;
  background: rgba(245, 248, 252, 0.72);
  backdrop-filter: blur(18px);
  box-shadow: var(--shadow-md);
}
.nav-brand-wrap {
  min-width: 0;
}
.nav-brand {
  display: inline-block;
  color: #10273f;
  font-family: "Songti SC", "STSong", Georgia, serif;
  font-size: 24px;
  letter-spacing: -0.03em;
  font-weight: 700;
}
.nav-caption {
  color: var(--muted);
  font-size: 12px;
}
.nav-links {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  min-width: 0;
}
.nav-link {
  padding: 10px 14px;
  border-radius: 999px;
  color: #2f4b69;
  font-size: 13px;
  font-weight: 600;
}
.nav-link.is-active {
  background: rgba(29, 103, 194, 0.12);
  color: #164e94;
}
.site-main {
  display: grid;
  gap: 18px;
}
.page-hero,
.home-hero-card,
.detail-hero {
  position: relative;
  overflow: hidden;
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
}
.page-hero {
  padding: 28px 30px 26px;
  border: 1px solid rgba(255, 255, 255, 0.20);
  background:
    radial-gradient(circle at top right, rgba(255, 255, 255, 0.18), transparent 34%),
    linear-gradient(135deg, var(--hero-start) 0%, var(--hero-end) 100%);
  color: #f5fbff;
}
.hero-kicker {
  margin-bottom: 8px;
  color: rgba(235, 242, 252, 0.82);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}
.page-title,
.home-title,
.detail-title {
  margin: 0;
  font-family: "Songti SC", "STSong", Georgia, serif;
  font-size: clamp(34px, 5vw, 54px);
  line-height: 0.98;
  letter-spacing: -0.04em;
}
.home-hero-card,
.detail-hero,
.home-section,
.detail-content,
.pager-row,
.archive-block {
  border: 1px solid rgba(255, 255, 255, 0.34);
  background: var(--panel);
  backdrop-filter: blur(16px);
}
.home-hero-card {
  display: grid;
  grid-template-columns: minmax(0, 1.5fr) minmax(260px, 0.9fr);
  gap: 20px;
  padding: 24px;
}
.home-dek,
.detail-dek {
  max-width: 70ch;
  color: var(--muted);
  font-size: 16px;
  line-height: 1.6;
}
.hero-actions,
.card-actions,
.detail-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.home-hero-copy,
.hero-stats,
.detail-hero-main,
.detail-hero-side,
.trend-card,
.topic-card,
.pager-card {
  min-width: 0;
}
.hero-actions {
  margin-top: 18px;
}
.hero-stats,
.detail-hero-side {
  display: grid;
  gap: 10px;
}
.detail-hero-main {
  display: grid;
  align-content: start;
}
.detail-stream-row {
  margin-bottom: 10px;
}
.meta-panel {
  padding: 14px 16px;
  border: 1px solid rgba(255, 255, 255, 0.46);
  border-radius: var(--radius-md);
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.62), rgba(245, 249, 253, 0.86));
}
.meta-panel-label {
  margin-bottom: 6px;
  color: #7187a0;
  font-size: 11px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}
.meta-panel-value {
  color: #1f3248;
  font-size: 16px;
  line-height: 1.35;
  font-weight: 600;
}
.home-section,
.detail-content,
.archive-block {
  padding: 20px;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
}
.split-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) minmax(320px, 0.9fr);
  gap: 18px;
}
.section-heading-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 14px;
  flex-wrap: wrap;
}
.section-title {
  margin: 0 0 12px;
  color: #183453;
  font-family: "Songti SC", "STSong", Georgia, serif;
  font-size: 28px;
  letter-spacing: -0.03em;
  overflow-wrap: anywhere;
  word-break: break-word;
}
.page-section-title {
  margin-bottom: 18px;
}
.trend-grid,
.topic-card-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}
.trend-card,
.topic-card,
.pager-card {
  display: grid;
  padding: 18px;
  border: 1px solid var(--line);
  border-radius: 20px;
  background:
    linear-gradient(180deg, var(--panel-strong) 0%, rgba(245, 249, 253, 0.92) 100%);
}
.card-meta-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}
.card-pill-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.meta-pill,
.topic-pill {
  display: inline-flex;
  align-items: center;
  min-height: 32px;
  padding: 0 12px;
  border-radius: 999px;
  border: 1px solid rgba(29, 103, 194, 0.14);
  background: rgba(29, 103, 194, 0.08);
  color: #225693;
  font-size: 12px;
  font-weight: 600;
}
.nav-link,
.meta-pill,
.topic-pill,
.action-link,
.detail-summary {
  max-width: 100%;
  overflow-wrap: anywhere;
  word-break: break-word;
  white-space: normal;
}
.stream-pill {
  border-color: rgba(21, 98, 76, 0.16);
  background: rgba(21, 98, 76, 0.08);
  color: #1e6a55;
}
.meta-pill.subdued {
  border-color: rgba(17, 41, 71, 0.08);
  background: rgba(255, 255, 255, 0.65);
  color: var(--muted);
}
.topic-pill-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 16px;
}
.topic-pill-link:hover,
.stream-pill-link:hover,
.action-link:hover,
.trend-card a:hover,
.topic-card a:hover {
  opacity: 0.85;
}
.meta-date {
  color: #6e849d;
  font-size: 13px;
  overflow-wrap: anywhere;
  word-break: break-word;
}
.card-title,
.topic-card-title {
  margin: 14px 0 10px;
  color: #15253a;
  font-family: "Songti SC", "STSong", Georgia, serif;
  font-size: 26px;
  line-height: 1.08;
  letter-spacing: -0.03em;
  overflow-wrap: anywhere;
  word-break: break-word;
}
.card-title a,
.topic-card-title a {
  color: inherit;
}
.card-excerpt {
  margin: 0 0 14px;
  color: #4f647a;
  line-height: 1.62;
}
.trend-card .card-actions,
.detail-actions {
  margin-top: 16px;
  padding-top: 14px;
  border-top: 1px solid var(--line);
}
.action-link {
  display: inline-flex;
  align-items: center;
  min-height: 38px;
  padding: 0 14px;
  border-radius: 999px;
  background: #1d67c2;
  color: white;
  font-size: 13px;
  font-weight: 700;
}
.action-link.secondary {
  background: rgba(29, 103, 194, 0.10);
  color: #1b579d;
}
.breadcrumbs {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
  margin-bottom: 8px;
  color: #7489a1;
  font-size: 13px;
}
.detail-hero {
  display: grid;
  grid-template-columns: minmax(0, 1.45fr) minmax(260px, 0.9fr);
  gap: 18px;
  padding: 22px;
}
.detail-summary {
  display: inline-flex;
  align-items: center;
  min-height: 34px;
  margin-bottom: 6px;
  padding: 0 12px;
  border-radius: 999px;
  background: rgba(29, 103, 194, 0.09);
  color: #1c5da8;
  font-size: 13px;
  font-weight: 700;
}
.detail-content {
  padding: 0;
}
.detail-content .document-flow {
  padding: 16px;
}
.detail-content .summary-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}
.detail-content .summary-grid.summary-grid-single {
  grid-template-columns: minmax(0, 1fr);
}
.detail-content .surface-card {
  margin-top: 14px;
  padding: 16px;
  border: 1px solid var(--line);
  border-radius: 20px;
  background:
    linear-gradient(180deg, var(--panel-strong), rgba(244, 248, 252, 0.92));
}
.detail-content .summary-grid .surface-card {
  margin-top: 0;
}
.detail-content .summary-card-primary {
  background:
    linear-gradient(180deg, rgba(235, 243, 253, 0.95), rgba(248, 251, 254, 0.96));
}
.detail-content .summary-card-secondary {
  background:
    linear-gradient(180deg, rgba(247, 250, 254, 0.95), rgba(251, 252, 254, 0.96));
}
.detail-content .highlight-card {
  background:
    linear-gradient(180deg, rgba(247, 250, 254, 0.95), rgba(241, 247, 253, 0.96));
}
.detail-content .section-label {
  margin: 0 0 10px;
  color: #6a8098;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}
.detail-content .prose,
.detail-content .cluster-body {
  color: #213246;
  font-size: 15px;
  line-height: 1.66;
}
.detail-content .prose p,
.detail-content .cluster-body p {
  margin: 0 0 10px;
}
.detail-content .prose h3,
.detail-content .cluster-card h3 {
  margin: 14px 0 8px;
  color: #16395c;
  font-family: "Songti SC", "STSong", Georgia, serif;
  font-size: 24px;
  line-height: 1.08;
}
.detail-content .prose h4,
.detail-content .cluster-body h4 {
  margin: 12px 0 7px;
  color: #6e849d;
  font-size: 11px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}
.detail-content .prose ul,
.detail-content .prose ol,
.detail-content .cluster-body ul,
.detail-content .cluster-body ol {
  margin: 8px 0 10px;
  padding-inline-start: 1.08em;
}
.detail-content .prose li,
.detail-content .cluster-body li {
  margin: 0 0 7px;
  padding-left: 0.12em;
}
.detail-content .prose blockquote,
.detail-content .cluster-body blockquote {
  margin: 12px 0;
  padding: 12px 14px;
  border-left: 3px solid rgba(29, 103, 194, 0.42);
  border-radius: 14px;
  background: var(--accent-soft);
  color: #24476d;
}
.detail-content .prose table,
.detail-content .cluster-body table {
  display: block;
  max-width: 100%;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  width: 100%;
  margin: 12px 0;
  border-collapse: collapse;
}
.detail-content .prose pre,
.detail-content .cluster-body pre {
  max-width: 100%;
  overflow-x: auto;
}
.detail-content .prose th,
.detail-content .prose td,
.detail-content .cluster-body th,
.detail-content .cluster-body td {
  padding: 8px;
  border: 1px solid #d8e1eb;
  text-align: left;
  vertical-align: top;
}
.detail-content .prose th,
.detail-content .cluster-body th {
  background: #eff5fa;
}
.detail-content .topic-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 8px;
}
.detail-content .topic-pill {
  justify-content: center;
  min-height: 40px;
  background: rgba(248, 251, 255, 0.98);
  border: 1px solid #dbe4ef;
  color: #425a74;
}
.detail-content .cluster-columns {
  column-count: 2;
  column-gap: 14px;
}
.detail-content .cluster-card {
  display: inline-block;
  width: 100%;
  margin: 0 0 14px;
  padding: 16px;
  border: 1px solid var(--line);
  border-radius: 18px;
  background: rgba(251, 253, 255, 0.96);
  break-inside: avoid;
}
.pager-row {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
  padding: 16px;
}
.pager-card span {
  display: block;
  margin-bottom: 8px;
  color: #6f859d;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}
.pager-card strong {
  color: #16304f;
  font-size: 18px;
  line-height: 1.32;
}
.timeline-list,
.archive-list {
  display: grid;
  gap: 10px;
  margin: 0;
  padding: 0;
  list-style: none;
}
.timeline-item,
.archive-item {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding: 14px 16px;
  border: 1px solid var(--line);
  border-radius: 16px;
  background: rgba(251, 253, 255, 0.86);
}
.timeline-item a,
.archive-item a {
  color: #162f4d;
  font-weight: 600;
  overflow-wrap: anywhere;
  word-break: break-word;
}
.timeline-item span,
.archive-item span,
.topic-card-meta {
  color: #6b8098;
  font-size: 13px;
  overflow-wrap: anywhere;
  word-break: break-word;
}
.empty-card {
  padding: 24px;
  border: 1px dashed rgba(17, 41, 71, 0.16);
  border-radius: 18px;
  color: var(--muted);
}
@media (max-width: 1080px) {
  .home-hero-card,
  .detail-hero,
  .split-layout {
    grid-template-columns: 1fr;
  }
  .trend-grid,
  .topic-card-grid,
  .detail-content .summary-grid,
  .pager-row {
    grid-template-columns: 1fr;
  }
}
@media (max-width: 760px) {
  .site-shell {
    width: calc(100% - 16px);
    max-width: 100%;
    padding-top: 12px;
  }
  .site-header {
    position: static;
    flex-direction: column;
    align-items: stretch;
    border-radius: 24px;
    padding: 16px;
  }
  .nav-links {
    width: 100%;
  }
  .nav-link {
    flex: 1 1 calc(50% - 5px);
    justify-content: center;
    text-align: center;
  }
  .page-hero,
  .home-hero-card,
  .home-section,
  .detail-hero,
  .detail-content,
  .archive-block {
    padding-left: 16px;
    padding-right: 16px;
  }
  .detail-content .document-flow {
    padding: 12px 0 0;
  }
  .section-heading-row {
    align-items: flex-start;
  }
  .hero-actions .action-link,
  .card-actions .action-link,
  .detail-actions .action-link {
    flex: 1 1 100%;
    justify-content: center;
  }
  .detail-summary {
    width: 100%;
  }
  .detail-content .topic-grid,
  .detail-content .cluster-columns {
    grid-template-columns: 1fr;
    column-count: 1;
  }
  .timeline-item,
  .archive-item {
    flex-direction: column;
  }
}
"""


def _load_trend_source_documents(
    *,
    input_dirs: Sequence[TrendSiteInputDirectory],
    limit: int | None = None,
) -> list[TrendSiteSourceDocument]:
    source_documents: list[TrendSiteSourceDocument] = []
    for input_info in input_dirs:
        markdown_paths = sorted(input_info.path.glob("*.md"))
        for markdown_path in markdown_paths:
            raw_markdown = markdown_path.read_text(encoding="utf-8")
            frontmatter, markdown_body = _split_yaml_frontmatter_text(raw_markdown)
            if str(frontmatter.get("kind") or "").strip().lower() != "trend":
                continue

            period_start = _parse_site_datetime(frontmatter.get("period_start"))
            period_end = _parse_site_datetime(frontmatter.get("period_end"))
            granularity = (
                str(frontmatter.get("granularity") or "trend").strip().lower()
                or "trend"
            )
            topics = _parse_site_string_list(frontmatter.get("topics"))

            stream = str(frontmatter.get("stream") or input_info.stream or "").strip() or None
            source_pdf_path = markdown_path.with_suffix(".pdf")
            pdf_path = (
                source_pdf_path
                if source_pdf_path.exists() and source_pdf_path.is_file()
                else None
            )
            source_documents.append(
                TrendSiteSourceDocument(
                    markdown_path=markdown_path,
                    pdf_path=pdf_path,
                    stem=markdown_path.stem,
                    frontmatter=frontmatter,
                    markdown_body=markdown_body,
                    granularity=granularity,
                    period_start=period_start,
                    period_end=period_end,
                    topics=topics,
                    stream=stream,
                )
            )

    source_documents.sort(key=_trend_site_sort_key, reverse=True)
    return source_documents[:limit] if limit is not None else source_documents


def _item_site_page_stem(*, stem: str, stream: str | None) -> str:
    cleaned_stream = str(stream or "").strip()
    if not cleaned_stream:
        return stem
    return f"{_stream_slug(cleaned_stream)}--{stem}"


def _item_site_asset_name(*, name: str, stream: str | None) -> str:
    cleaned_stream = str(stream or "").strip()
    if not cleaned_stream:
        return name
    return f"{_stream_slug(cleaned_stream)}--{name}"


def _extract_markdown_h1(markdown_body: str, *, fallback: str) -> str:
    for line in str(markdown_body or "").splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("# "):
            title = stripped[2:].strip()
            return title or fallback
        break
    return fallback


def _resolve_site_local_markdown_target(
    *,
    source_markdown_path: Path,
    href: str,
) -> Path | None:
    raw_href = str(href or "").strip()
    if (
        not raw_href
        or raw_href.startswith("#")
        or "://" in raw_href
        or raw_href.startswith("mailto:")
        or raw_href.startswith("tel:")
    ):
        return None
    candidate = raw_href.split("#", 1)[0].split("?", 1)[0].strip()
    if not candidate or not candidate.endswith(".md"):
        return None
    return (source_markdown_path.parent / candidate).resolve()


def _rewrite_site_markdown_links(
    *,
    html_text: str,
    source_markdown_path: Path,
    from_page: Path,
    page_by_markdown_path: dict[Path, Path],
) -> str:
    soup = BeautifulSoup(html_text, "html.parser")
    rewritten = False
    for anchor in soup.find_all("a", href=True):
        target_path = _resolve_site_local_markdown_target(
            source_markdown_path=source_markdown_path,
            href=str(anchor.get("href") or ""),
        )
        if target_path is None:
            continue
        target_page_path = page_by_markdown_path.get(target_path)
        if target_page_path is None:
            continue
        anchor["href"] = _site_href(from_page=from_page, to_page=target_page_path)
        rewritten = True
    return str(soup) if rewritten else html_text


def _load_item_source_documents(
    *,
    input_dirs: Sequence[TrendSiteInputDirectory],
) -> list[ItemSiteSourceDocument]:
    source_documents: list[ItemSiteSourceDocument] = []
    seen_paths: set[Path] = set()
    for input_info in input_dirs:
        if input_info.inbox_path is None:
            continue
        for markdown_path in sorted(input_info.inbox_path.glob("*.md")):
            resolved_markdown_path = markdown_path.resolve()
            if resolved_markdown_path in seen_paths:
                continue
            seen_paths.add(resolved_markdown_path)
            raw_markdown = resolved_markdown_path.read_text(encoding="utf-8")
            frontmatter, markdown_body = _split_yaml_frontmatter_text(raw_markdown)
            title = _extract_markdown_h1(
                markdown_body,
                fallback=resolved_markdown_path.stem,
            )
            raw_relevance = frontmatter.get("relevance_score")
            relevance_score: float | None = None
            if raw_relevance is not None:
                try:
                    relevance_score = float(raw_relevance)
                except Exception:
                    relevance_score = None
            source_documents.append(
                ItemSiteSourceDocument(
                    markdown_path=resolved_markdown_path,
                    stem=resolved_markdown_path.stem,
                    frontmatter=frontmatter,
                    markdown_body=markdown_body,
                    title=title,
                    canonical_url=str(frontmatter.get("url") or "").strip(),
                    source=str(frontmatter.get("source") or "").strip(),
                    published_at=_parse_site_datetime(frontmatter.get("published_at")),
                    authors=_parse_site_string_list(frontmatter.get("authors")),
                    topics=_parse_site_string_list(frontmatter.get("topics")),
                    relevance_score=relevance_score,
                    stream=input_info.stream,
                )
            )

    source_documents.sort(
        key=lambda document: (
            document.published_at or datetime.min.replace(tzinfo=timezone.utc),
            document.stem,
        ),
        reverse=True,
    )
    return source_documents


def _extract_item_body_html(*, body_html: str) -> tuple[str, str, str]:
    soup = BeautifulSoup(body_html, "html.parser")
    title = "Item"
    first_h1 = soup.find("h1")
    if first_h1 is not None:
        extracted_title = first_h1.get_text(" ", strip=True)
        if extracted_title:
            title = extracted_title
        first_h1.decompose()
    normalized_html = str(soup).strip()
    _section_title, sections = _extract_trend_pdf_sections(body_html=normalized_html)
    excerpt = _section_excerpt(sections) if sections else ""
    if not excerpt:
        excerpt = _safe_excerpt(soup.get_text(" ", strip=True), limit=220)
    return title, normalized_html, excerpt


def _build_item_browser_body_html(*, body_html: str) -> str:
    _title, sections = _extract_trend_pdf_sections(body_html=body_html)
    if sections:
        browser_body_html = _build_trend_browser_body_html(sections=sections)
        soup = BeautifulSoup(browser_body_html, "html.parser")
        summary_grid = soup.select_one("section.summary-grid")
        if summary_grid is not None:
            summary_cards = summary_grid.find_all("section", recursive=False)
            if len(summary_cards) == 1:
                raw_classes = summary_grid.get("class")
                if isinstance(raw_classes, list):
                    classes = [str(class_name) for class_name in raw_classes]
                else:
                    classes = str(raw_classes or "").split()
                if "summary-grid-single" not in classes:
                    classes.append("summary-grid-single")
                summary_grid["class"] = " ".join(classes)
        return str(soup)
    fallback_html = body_html.strip() or "<p>(empty)</p>"
    return (
        "<div class='document-flow'>"
        "<section class='surface-card section-card'>"
        "<h2 class='section-label'>Note</h2>"
        f"<div class='prose'>{fallback_html}</div>"
        "</section>"
        "</div>"
    )


def _load_item_site_documents(
    *,
    input_dirs: Sequence[TrendSiteInputDirectory],
    output_dir: Path,
) -> tuple[list[ItemSiteDocument], dict[Path, Path]]:
    markdown = MarkdownIt("commonmark", {"html": True, "typographer": True})
    source_documents = _load_item_source_documents(input_dirs=input_dirs)
    items_dir = output_dir / "items"
    item_artifacts_dir = output_dir / "artifacts" / "items"
    items_dir.mkdir(parents=True, exist_ok=True)
    item_artifacts_dir.mkdir(parents=True, exist_ok=True)

    documents: list[ItemSiteDocument] = []
    page_by_markdown_path: dict[Path, Path] = {}
    for source_document in source_documents:
        normalized_markdown = source_document.markdown_body.strip() or "# Item\n"
        rendered_html = markdown.render(normalized_markdown)
        title, raw_body_html, excerpt = _extract_item_body_html(body_html=rendered_html)
        body_html = _build_item_browser_body_html(body_html=raw_body_html)
        page_stem = _item_site_page_stem(
            stem=source_document.stem,
            stream=source_document.stream,
        )
        page_path = items_dir / f"{page_stem}.html"
        markdown_asset_path = item_artifacts_dir / _item_site_asset_name(
            name=source_document.markdown_path.name,
            stream=source_document.stream,
        )
        shutil.copy2(source_document.markdown_path, markdown_asset_path)
        documents.append(
            ItemSiteDocument(
                markdown_path=source_document.markdown_path,
                markdown_asset_path=markdown_asset_path,
                page_path=page_path,
                stem=source_document.stem,
                title=title,
                canonical_url=source_document.canonical_url,
                source=source_document.source,
                published_at=source_document.published_at,
                authors=source_document.authors,
                topics=source_document.topics,
                stream=source_document.stream,
                relevance_score=source_document.relevance_score,
                body_html=body_html,
                excerpt=excerpt,
                frontmatter=source_document.frontmatter,
            )
        )
        page_by_markdown_path[source_document.markdown_path.resolve()] = page_path
    return documents, page_by_markdown_path


def _load_trend_site_documents(
    *,
    input_dirs: Sequence[TrendSiteInputDirectory],
    output_dir: Path,
    item_pages_by_markdown_path: dict[Path, Path],
    limit: int | None = None,
) -> list[TrendSiteDocument]:
    markdown = MarkdownIt("commonmark", {"html": True, "typographer": True})
    documents: list[TrendSiteDocument] = []
    source_documents = _load_trend_source_documents(input_dirs=input_dirs, limit=limit)

    artifacts_dir = output_dir / "artifacts"
    trends_dir = output_dir / "trends"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    trends_dir.mkdir(parents=True, exist_ok=True)

    trend_pages_by_markdown_path = {
        source_document.markdown_path.resolve(): (
            trends_dir / f"{source_document.stem}.html"
        )
        for source_document in source_documents
    }
    linked_page_by_markdown_path = dict(item_pages_by_markdown_path)
    linked_page_by_markdown_path.update(trend_pages_by_markdown_path)

    for source_document in source_documents:
        normalized_markdown = _normalize_obsidian_callouts_for_pdf(
            source_document.markdown_body
        ).strip()
        if not normalized_markdown:
            normalized_markdown = "# Trend\n"
        body_html = markdown.render(normalized_markdown)
        title, sections = _extract_trend_pdf_sections(body_html=body_html)
        title = sanitize_trend_title(title, fallback="Trend")
        excerpt = _section_excerpt(sections)
        page_path = trend_pages_by_markdown_path[source_document.markdown_path.resolve()]
        browser_body_html = _rewrite_site_markdown_links(
            html_text=_build_trend_browser_body_html(sections=sections),
            source_markdown_path=source_document.markdown_path,
            from_page=page_path,
            page_by_markdown_path=linked_page_by_markdown_path,
        )

        period_token = (
            _trend_date_token(
                granularity=source_document.granularity,
                period_start=source_document.period_start,
            )
            if source_document.period_start is not None
            else source_document.stem
        )

        markdown_asset_path = artifacts_dir / source_document.markdown_path.name
        shutil.copy2(source_document.markdown_path, markdown_asset_path)

        pdf_asset_path: Path | None = None
        if source_document.pdf_path is not None:
            pdf_asset_path = artifacts_dir / source_document.pdf_path.name
            shutil.copy2(source_document.pdf_path, pdf_asset_path)

        documents.append(
            TrendSiteDocument(
                markdown_path=source_document.markdown_path,
                markdown_asset_path=markdown_asset_path,
                pdf_asset_path=pdf_asset_path,
                page_path=page_path,
                stem=source_document.stem,
                title=title,
                granularity=source_document.granularity,
                period_token=period_token,
                period_start=source_document.period_start,
                period_end=source_document.period_end,
                topics=source_document.topics,
                stream=source_document.stream,
                body_html=browser_body_html,
                excerpt=excerpt,
                frontmatter=source_document.frontmatter,
            )
        )

    return documents


def export_trend_static_site(
    *,
    input_dir: Path | Sequence[Path],
    output_dir: Path,
    limit: int | None = None,
) -> Path:
    resolved_input_roots = _coerce_site_input_paths(input_dir)
    resolved_input_dirs = _discover_trend_site_input_dirs(resolved_input_roots)
    resolved_output_dir = output_dir.expanduser().resolve()
    for input_info in resolved_input_dirs:
        if _paths_overlap(input_info.path, resolved_output_dir):
            raise ValueError(
                "Trend site output directory must not overlap the input directory"
            )
    _reset_directory(resolved_output_dir)
    (resolved_output_dir / "assets").mkdir(parents=True, exist_ok=True)
    (resolved_output_dir / "items").mkdir(parents=True, exist_ok=True)
    (resolved_output_dir / "topics").mkdir(parents=True, exist_ok=True)
    (resolved_output_dir / "streams").mkdir(parents=True, exist_ok=True)

    item_documents, item_pages_by_markdown_path = _load_item_site_documents(
        input_dirs=resolved_input_dirs,
        output_dir=resolved_output_dir,
    )
    documents = _load_trend_site_documents(
        input_dirs=resolved_input_dirs,
        output_dir=resolved_output_dir,
        item_pages_by_markdown_path=item_pages_by_markdown_path,
        limit=limit,
    )

    label_by_topic_slug: dict[str, str] = {}
    topic_documents: dict[str, list[TrendSiteDocument]] = defaultdict(list)
    for document in documents:
        for topic in document.topics:
            slug = _topic_slug(topic)
            label_by_topic_slug.setdefault(slug, topic)
            topic_documents[slug].append(document)

    topic_pages = {
        slug: resolved_output_dir / "topics" / f"{slug}.html"
        for slug in sorted(topic_documents.keys())
    }
    label_by_stream_slug: dict[str, str] = {}
    stream_documents: dict[str, list[TrendSiteDocument]] = defaultdict(list)
    for document in documents:
        cleaned_stream = str(document.stream or "").strip()
        if not cleaned_stream:
            continue
        slug = _stream_slug(cleaned_stream)
        label_by_stream_slug.setdefault(slug, cleaned_stream)
        stream_documents[slug].append(document)

    stream_pages = {
        slug: resolved_output_dir / "streams" / f"{slug}.html"
        for slug in sorted(stream_documents.keys())
    }

    (resolved_output_dir / "assets" / "site.css").write_text(
        _SITE_CSS.strip() + "\n",
        encoding="utf-8",
    )
    (resolved_output_dir / ".nojekyll").write_text("", encoding="utf-8")

    (resolved_output_dir / "index.html").write_text(
        _render_home_page(
            documents=documents,
            output_dir=resolved_output_dir,
            topic_pages=topic_pages,
            stream_pages=stream_pages,
        ),
        encoding="utf-8",
    )
    (resolved_output_dir / "archive.html").write_text(
        _render_archive_page(
            documents=documents,
            output_dir=resolved_output_dir,
        ),
        encoding="utf-8",
    )
    (resolved_output_dir / "topics" / "index.html").write_text(
        _render_topics_index_page(
            documents=documents,
            output_dir=resolved_output_dir,
            topic_pages=topic_pages,
        ),
        encoding="utf-8",
    )
    (resolved_output_dir / "streams" / "index.html").write_text(
        _render_streams_index_page(
            documents=documents,
            output_dir=resolved_output_dir,
            stream_pages=stream_pages,
        ),
        encoding="utf-8",
    )

    for idx, document in enumerate(documents):
        previous_document = documents[idx - 1] if idx > 0 else None
        next_document = documents[idx + 1] if idx + 1 < len(documents) else None
        document.page_path.write_text(
            _render_detail_page(
                document=document,
                output_dir=resolved_output_dir,
                topic_pages=topic_pages,
                stream_pages=stream_pages,
                previous_document=previous_document,
                next_document=next_document,
            ),
            encoding="utf-8",
        )

    for document in item_documents:
        document.page_path.write_text(
            _render_item_page(
                document=document,
                output_dir=resolved_output_dir,
                topic_pages=topic_pages,
                stream_pages=stream_pages,
            ),
            encoding="utf-8",
        )

    for slug, page_path in topic_pages.items():
        page_path.write_text(
            _render_topic_page(
                topic=label_by_topic_slug[slug],
                topic_slug=slug,
                documents=topic_documents[slug],
                output_dir=resolved_output_dir,
                topic_pages=topic_pages,
                stream_pages=stream_pages,
            ),
            encoding="utf-8",
        )

    for slug, page_path in stream_pages.items():
        page_path.write_text(
            _render_stream_page(
                stream=label_by_stream_slug[slug],
                stream_slug=slug,
                documents=stream_documents[slug],
                output_dir=resolved_output_dir,
                topic_pages=topic_pages,
                stream_pages=stream_pages,
            ),
            encoding="utf-8",
        )

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "input_dir": (
            str(resolved_input_roots[0])
            if len(resolved_input_roots) == 1
            else [str(path) for path in resolved_input_roots]
        ),
        "input_dirs": [
            {
                "path": str(input_info.path),
                "stream": input_info.stream,
            }
            for input_info in resolved_input_dirs
        ],
        "output_dir": str(resolved_output_dir),
        "trends_total": len(documents),
        "items_total": len(item_documents),
        "topics_total": len(topic_pages),
        "streams_total": len(stream_pages),
        "files": {
            "index": "index.html",
            "archive": "archive.html",
            "nojekyll": ".nojekyll",
            "topics_index": "topics/index.html",
            "streams_index": "streams/index.html",
            "stylesheet": "assets/site.css",
            "trend_pages": [
                str(document.page_path.relative_to(resolved_output_dir))
                for document in documents
            ],
            "item_pages": [
                str(document.page_path.relative_to(resolved_output_dir))
                for document in item_documents
            ],
            "topic_pages": [
                str(path.relative_to(resolved_output_dir))
                for path in topic_pages.values()
            ],
            "stream_pages": [
                str(path.relative_to(resolved_output_dir))
                for path in stream_pages.values()
            ],
        },
    }
    manifest_path = resolved_output_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    logger.bind(
        module="site.build",
        output_dir=str(resolved_output_dir),
        trends_total=len(documents),
        items_total=len(item_documents),
        topics_total=len(topic_pages),
        streams_total=len(stream_pages),
    ).info("Trend static site export completed")
    return manifest_path


def stage_trend_site_source(
    *,
    input_dir: Path | Sequence[Path],
    output_dir: Path,
    limit: int | None = None,
) -> Path:
    resolved_input_roots = _coerce_site_input_paths(input_dir)
    resolved_input_dirs = _discover_trend_site_input_dirs(resolved_input_roots)
    resolved_output_dir = output_dir.expanduser().resolve()
    stage_root = (
        resolved_output_dir.parent
        if resolved_output_dir.name == "Trends"
        else resolved_output_dir
    )
    for input_info in resolved_input_dirs:
        if _paths_overlap(input_info.path, stage_root):
            raise ValueError(
                "Trend site stage output directory must not overlap the input directory"
            )
    _reset_stage_output_root(
        stage_root=stage_root,
        trends_output_dir=resolved_output_dir,
    )

    source_documents = _load_trend_source_documents(
        input_dirs=resolved_input_dirs,
        limit=limit,
    )
    item_source_documents = _load_item_source_documents(input_dirs=resolved_input_dirs)
    has_stream_documents = any(
        bool(source_document.stream) for source_document in source_documents
    )
    staged_markdown_files: list[str] = []
    staged_pdf_files: list[str] = []
    staged_item_files: list[str] = []

    def relative_to_stage_root(path: Path) -> str:
        return str(path.relative_to(stage_root))

    for source_document in source_documents:
        target_dir = (
            stage_root / "Streams" / source_document.stream / "Trends"
            if source_document.stream
            else (
                stage_root / "Trends"
                if has_stream_documents
                else resolved_output_dir
            )
        )
        target_dir.mkdir(parents=True, exist_ok=True)
        staged_markdown_path = target_dir / source_document.markdown_path.name
        shutil.copy2(source_document.markdown_path, staged_markdown_path)
        staged_markdown_files.append(relative_to_stage_root(staged_markdown_path))

        if source_document.pdf_path is None:
            continue
        staged_pdf_path = target_dir / source_document.pdf_path.name
        shutil.copy2(source_document.pdf_path, staged_pdf_path)
        staged_pdf_files.append(relative_to_stage_root(staged_pdf_path))

    for source_document in item_source_documents:
        target_dir = (
            stage_root / "Streams" / source_document.stream / "Inbox"
            if source_document.stream
            else stage_root / "Inbox"
        )
        target_dir.mkdir(parents=True, exist_ok=True)
        staged_item_path = target_dir / source_document.markdown_path.name
        shutil.copy2(source_document.markdown_path, staged_item_path)
        staged_item_files.append(relative_to_stage_root(staged_item_path))

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "input_dir": (
            str(resolved_input_roots[0])
            if len(resolved_input_roots) == 1
            else [str(path) for path in resolved_input_roots]
        ),
        "input_dirs": [
            {
                "path": str(input_info.path),
                "stream": input_info.stream,
            }
            for input_info in resolved_input_dirs
        ],
        "output_dir": str(resolved_output_dir),
        "trends_total": len(source_documents),
        "items_total": len(item_source_documents),
        "pdf_total": len(staged_pdf_files),
        "streams_total": len(
            {
                source_document.stream
                for source_document in source_documents
                if source_document.stream
            }
        ),
        "files": {
            "markdown": staged_markdown_files,
            "items_markdown": staged_item_files,
            "pdf": staged_pdf_files,
        },
    }
    manifest_path = resolved_output_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    logger.bind(
        module="site.stage",
        output_dir=str(resolved_output_dir),
        trends_total=len(source_documents),
        items_total=len(item_source_documents),
        pdf_total=len(staged_pdf_files),
        streams_total=manifest["streams_total"],
    ).info("Trend site source staging completed")
    return manifest_path
