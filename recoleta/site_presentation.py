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
    render_idea_opportunities_section: Callable[..., tuple[str, int, int]]


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


def _idea_evidence_block(*, evidence_nodes: list[str]) -> tuple[str, int]:
    evidence_soup = BeautifulSoup("".join(evidence_nodes), "html.parser")
    evidence_count = sum(
        1 for item in evidence_soup.find_all("li") if item.find_parent("li") is None
    )
    evidence_html = "".join(evidence_nodes).strip() or "<p>(none)</p>"
    return (
        "<section class='idea-opportunity-block idea-opportunity-block-evidence'>"
        "<div class='idea-opportunity-label'>Evidence</div>"
        f"<div class='idea-opportunity-copy prose idea-evidence-list'>{evidence_html}</div>"
        "</section>",
        evidence_count,
    )


def _collect_evidence_nodes(
    *, children: list[Any], start_index: int
) -> tuple[list[str], int]:
    evidence_nodes: list[str] = []
    look_ahead = start_index + 1
    while look_ahead < len(children):
        candidate = children[look_ahead]
        if isinstance(candidate, Tag) and candidate.name in {"h3", "h4", "h5"}:
            break
        if str(candidate).strip():
            evidence_nodes.append(str(candidate))
        look_ahead += 1
    return evidence_nodes, look_ahead


def _consume_opportunity_meta_sections(
    *,
    child: Tag,
    meta_row_html: str,
    extract_meta_sections: Callable[[Tag], tuple[str | None, str | None] | None],
) -> tuple[str, str | None] | None:
    if meta_row_html:
        return None
    meta_sections = extract_meta_sections(child)
    if meta_sections is None:
        return None
    extracted_meta_html, role_html = meta_sections
    return extracted_meta_html or meta_row_html, role_html


def _consume_opportunity_evidence_section(
    *,
    child: Tag,
    children: list[Any],
    index: int,
    idea_heading_matches: Callable[..., bool],
) -> tuple[str, int, int] | None:
    if child.name not in {"h4", "h5"}:
        return None
    if not idea_heading_matches(child.get_text(" ", strip=True), "evidence"):
        return None
    evidence_nodes, next_index = _collect_evidence_nodes(
        children=children,
        start_index=index,
    )
    evidence_block, evidence_count = _idea_evidence_block(evidence_nodes=evidence_nodes)
    return evidence_block, evidence_count, next_index


def _render_labeled_opportunity_block(*, label: str, value_html: str) -> str:
    return (
        "<section class='idea-opportunity-block'>"
        f"<div class='idea-opportunity-label'>{html.escape(label)}</div>"
        f"<div class='idea-opportunity-copy prose'><p>{value_html}</p></div>"
        "</section>"
    )


def _render_generic_opportunity_block(*, nodes: list[str]) -> str:
    return (
        "<section class='idea-opportunity-block'>"
        "<div class='idea-opportunity-copy prose'>"
        f"{''.join(nodes)}"
        "</div>"
        "</section>"
    )


def render_idea_opportunity_card(
    *,
    title: str,
    inner_html: str,
    extract_meta_sections: Callable[[Tag], tuple[str | None, str | None] | None],
    idea_heading_matches: Callable[..., bool],
    extract_labeled_paragraph: Callable[[Tag], tuple[str, str] | None],
) -> tuple[str, int]:
    soup = BeautifulSoup(inner_html, "html.parser")
    meta_row_html = ""
    content_blocks: list[str] = []
    evidence_count = 0
    generic_nodes: list[str] = []
    children = [node for node in soup.contents if str(node).strip()]
    index = 0
    while index < len(children):
        child = children[index]
        if not isinstance(child, Tag):
            generic_nodes.append(str(child))
            index += 1
            continue

        meta_sections = _consume_opportunity_meta_sections(
            child=child,
            meta_row_html=meta_row_html,
            extract_meta_sections=extract_meta_sections,
        )
        if meta_sections is not None:
            meta_row_html, role_html = meta_sections
            if role_html is not None:
                content_blocks.append(role_html)
            index += 1
            continue

        evidence_section = _consume_opportunity_evidence_section(
            child=child,
            children=children,
            index=index,
            idea_heading_matches=idea_heading_matches,
        )
        if evidence_section is not None:
            evidence_block, block_evidence_count, index = evidence_section
            evidence_count += block_evidence_count
            content_blocks.append(evidence_block)
            continue

        labeled = extract_labeled_paragraph(child)
        if labeled is not None:
            label, value_html = labeled
            content_blocks.append(
                _render_labeled_opportunity_block(label=label, value_html=value_html)
            )
            index += 1
            continue

        generic_nodes.append(str(child))
        index += 1

    if generic_nodes:
        content_blocks.insert(0, _render_generic_opportunity_block(nodes=generic_nodes))

    return (
        "<article class='idea-opportunity-card'>"
        "<div class='idea-opportunity-head'>"
        f"<h3 class='idea-opportunity-title'>{html.escape(title)}</h3>"
        f"{meta_row_html}"
        "</div>"
        f"<div class='idea-opportunity-body'>{''.join(content_blocks)}</div>"
        "</article>",
        evidence_count,
    )


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


def _append_idea_opportunity_card(
    *,
    cards: list[str],
    current_title: str | None,
    current_nodes: list[str],
    render_idea_opportunity_card: Callable[..., tuple[str, int]],
) -> int:
    if current_title is None:
        return 0
    card_html, evidence_count = render_idea_opportunity_card(
        title=current_title,
        inner_html="".join(current_nodes),
    )
    cards.append(card_html)
    return evidence_count


def _idea_opportunity_count_label(card_count: int) -> str:
    return f"{card_count} idea" if card_count == 1 else f"{card_count} ideas"


def render_idea_opportunities_section(
    *,
    heading: str,
    inner_html: str,
    render_idea_opportunity_card: Callable[..., tuple[str, int]],
    render_browser_content_card_html: Callable[..., str],
    render_browser_section_label_html: Callable[[str], str],
) -> tuple[str, int, int]:
    section_soup = BeautifulSoup(inner_html, "html.parser")
    cards: list[str] = []
    intro_nodes: list[str] = []
    evidence_count = 0
    current_title: str | None = None
    current_nodes: list[str] = []
    for node in [node for node in section_soup.contents if str(node).strip()]:
        if isinstance(node, Tag) and node.name == "h3":
            evidence_count += _append_idea_opportunity_card(
                cards=cards,
                current_title=current_title,
                current_nodes=current_nodes,
                render_idea_opportunity_card=render_idea_opportunity_card,
            )
            current_title = node.get_text(" ", strip=True) or "Idea"
            current_nodes = []
            continue
        if current_title is None:
            intro_nodes.append(str(node))
            continue
        current_nodes.append(str(node))

    evidence_count += _append_idea_opportunity_card(
        cards=cards,
        current_title=current_title,
        current_nodes=current_nodes,
        render_idea_opportunity_card=render_idea_opportunity_card,
    )
    if not cards:
        return (
            render_browser_content_card_html(heading=heading, inner_html=inner_html),
            0,
            evidence_count,
        )

    intro_html = (
        f"<div class='prose idea-section-intro'>{''.join(intro_nodes)}</div>"
        if "".join(intro_nodes).strip()
        else ""
    )
    return (
        "<section class='surface-card section-card idea-opportunities-section'>"
        "<div class='idea-section-head'>"
        f"{render_browser_section_label_html(heading)}"
        f"<span class='meta-date'>{html.escape(_idea_opportunity_count_label(len(cards)))}</span>"
        "</div>"
        f"{intro_html}"
        f"<div class='idea-opportunity-grid'>{''.join(cards)}</div>"
        "</section>",
        len(cards),
        evidence_count,
    )


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
        if deps.idea_heading_matches(section.heading, "opportunit"):
            section_html, section_opportunity_count, section_evidence_count = (
                deps.render_idea_opportunities_section(
                    heading=section.heading,
                    inner_html=section.inner_html,
                )
            )
            rendered.append(section_html)
            opportunity_count += section_opportunity_count
            evidence_count += section_evidence_count
            continue
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
    "render_idea_opportunities_section",
    "render_idea_opportunity_card",
    "render_presentation_source_list",
]
