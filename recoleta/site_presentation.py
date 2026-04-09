from __future__ import annotations

from dataclasses import dataclass
import html
from typing import Any, Callable

from bs4 import BeautifulSoup, Tag

from recoleta.site_models import IdeaBodyRenderResult


@dataclass(frozen=True, slots=True)
class IdeaBrowserBodyDeps:
    extract_trend_pdf_sections: Callable[..., tuple[str, list[Any]]]
    build_item_browser_body_html: Callable[..., str]
    idea_heading_matches: Callable[..., bool]
    render_browser_content_card_html: Callable[..., str]


def _entry_title(entry: dict[str, Any]) -> str:
    title = str(entry.get("title") or "").strip()
    if title:
        return title
    doc_id = entry.get("doc_id")
    try:
        doc_id_int = int(doc_id) if doc_id is not None else 0
    except Exception:
        doc_id_int = 0
    return f"Document {doc_id_int}" if doc_id_int > 0 else ""


def _entry_meta_parts(
    *,
    entry: dict[str, Any],
    labels: dict[str, str],
    humanize_source_type: Callable[[str], str],
    humanize_confidence: Callable[[str], str],
) -> list[str]:
    meta_parts: list[str] = []
    authors = [
        str(author).strip()
        for author in list(entry.get("authors") or [])
        if str(author).strip()
    ]
    if authors:
        meta_parts.append(html.escape(", ".join(authors)))

    source_type = str(entry.get("source_type") or "").strip()
    if source_type:
        meta_parts.append(
            f"{html.escape(labels.get('source_type', 'Source type'))}: "
            f"{html.escape(humanize_source_type(source_type))}"
        )

    confidence = str(entry.get("confidence") or "").strip()
    if confidence:
        meta_parts.append(
            f"{html.escape(labels.get('confidence', 'Confidence'))}: "
            f"{html.escape(humanize_confidence(confidence))}"
        )
    return meta_parts


def render_presentation_source_list(
    *,
    entries: list[dict[str, Any]],
    labels: dict[str, str],
    humanize_source_type: Callable[[str], str],
    humanize_confidence: Callable[[str], str],
) -> str:
    items: list[str] = []
    seen_targets: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        title = _entry_title(entry)
        href = str(entry.get("href") or entry.get("url") or "").strip()
        target = href or title
        if not title or target in seen_targets:
            continue
        seen_targets.add(target)
        title_html = (
            f"<a href='{html.escape(href, quote=True)}'>{html.escape(title)}</a>"
            if href
            else html.escape(title)
        )
        meta_parts = _entry_meta_parts(
            entry=entry,
            labels=labels,
            humanize_source_type=humanize_source_type,
            humanize_confidence=humanize_confidence,
        )
        meta_html = ""
        if meta_parts:
            meta_html = f"<div class='source-list-meta'>{' · '.join(meta_parts)}</div>"
        items.append(
            "<li class='source-list-item'>"
            f"<div class='source-list-title'>{title_html}</div>"
            f"{meta_html}"
            "</li>"
        )
    if not items:
        return "<p>(none)</p>"
    return "<ul class='source-list'>" + "".join(items) + "</ul>"


def build_item_browser_body_html(
    *,
    body_html: str,
    extract_trend_pdf_sections: Callable[..., tuple[str, list[Any]]],
    build_trend_browser_body_html: Callable[..., str],
) -> str:
    _title, sections = extract_trend_pdf_sections(body_html=body_html)
    if not sections:
        fallback_html = body_html.strip() or "<p>(empty)</p>"
        return (
            "<div class='document-flow'>"
            "<section class='surface-card section-card'>"
            "<h2 class='section-label'>Note</h2>"
            f"<div class='prose'>{fallback_html}</div>"
            "</section>"
            "</div>"
        )

    browser_body_html = build_trend_browser_body_html(sections=sections)
    soup = BeautifulSoup(browser_body_html, "html.parser")
    summary_grid = soup.select_one("section.summary-grid")
    if summary_grid is None:
        return str(soup)
    summary_cards = summary_grid.find_all("section", recursive=False)
    if len(summary_cards) != 1:
        return str(soup)
    raw_classes = summary_grid.get("class")
    classes = (
        [str(class_name) for class_name in raw_classes]
        if isinstance(raw_classes, list)
        else str(raw_classes or "").split()
    )
    if "summary-grid-single" not in classes:
        classes.append("summary-grid-single")
    summary_grid["class"] = " ".join(classes)
    return str(soup)

def _count_evidence_links(
    *,
    inner_html: str,
    idea_heading_matches: Callable[..., bool],
) -> int:
    soup = BeautifulSoup(inner_html, "html.parser")
    children = [node for node in soup.contents if str(node).strip()]
    evidence_count = 0
    collecting = False
    for child in children:
        if isinstance(child, Tag) and child.name in {"h3", "h4", "h5"}:
            collecting = idea_heading_matches(
                child.get_text(" ", strip=True),
                "evidence",
            )
            continue
        if not collecting:
            continue
        if isinstance(child, Tag) and child.name in {"ul", "ol"}:
            evidence_count += sum(
                1 for item in child.find_all("li") if item.find_parent("li") is None
            )
    return evidence_count


def build_idea_browser_body_html(
    *,
    body_html: str,
    deps: IdeaBrowserBodyDeps,
) -> IdeaBodyRenderResult:
    _title, sections = deps.extract_trend_pdf_sections(body_html=body_html)
    if not sections:
        return IdeaBodyRenderResult(
            body_html=deps.build_item_browser_body_html(body_html=body_html),
            opportunity_count=0,
            evidence_count=0,
        )

    rendered: list[str] = []
    summary_cards: list[str] = []
    opportunity_count = 0
    evidence_count = 0
    for section in sections:
        if deps.idea_heading_matches(section.heading, "summary", "overview"):
            summary_cards.append(
                deps.render_browser_content_card_html(
                    heading=section.heading,
                    inner_html=section.inner_html,
                    card_classes="surface-card section-card summary-card summary-card-primary",
                )
            )
            continue
        opportunity_count += 1
        evidence_count += _count_evidence_links(
            inner_html=section.inner_html,
            idea_heading_matches=deps.idea_heading_matches,
        )
        rendered.append(
            deps.render_browser_content_card_html(
                heading=section.heading,
                inner_html=section.inner_html,
            )
        )

    if summary_cards:
        summary_classes = (
            "summary-grid summary-grid-single"
            if len(summary_cards) == 1
            else "summary-grid"
        )
        rendered.insert(
            0,
            f"<section class='{summary_classes}'>{''.join(summary_cards[:2])}</section>",
        )
    return IdeaBodyRenderResult(
        body_html="<div class='document-flow'>" + "".join(rendered) + "</div>",
        opportunity_count=opportunity_count,
        evidence_count=evidence_count,
    )


__all__ = [
    "IdeaBrowserBodyDeps",
    "build_idea_browser_body_html",
    "build_item_browser_body_html",
    "render_presentation_source_list",
]
