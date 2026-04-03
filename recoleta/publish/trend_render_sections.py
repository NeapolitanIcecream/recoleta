from __future__ import annotations

import html
import re
from typing import Callable

from bs4 import BeautifulSoup, Tag
from slugify import slugify

from recoleta.publish.trend_render_models import TrendPdfSection

_OVERVIEW_HEADING_PATTERN = re.compile(
    r"^\s{0,3}#{1,6}\s*(overview|总览|概览|日度概览|周度概览|月度概览)\s*$",
    re.IGNORECASE,
)
_TOP_N_HEADING_PATTERN = re.compile(
    r"^(?P<heading>\s{0,3}#{1,6})\s+Top[- ]?(?P<count>\d+)(?P<suffix>\b.*)$",
    re.IGNORECASE,
)
_ORDERED_LIST_ITEM_PATTERN = re.compile(r"^\s{0,3}\d+\.\s+")
_REPRESENTATIVE_SNIPPET_PATTERN = re.compile(
    r"(?:[。.;；]\s*)?"
    r"(?:代表片段|Representative snippet|Representative excerpt)\s*[:：].*$",
    re.IGNORECASE,
)
_STANDALONE_REPRESENTATIVE_SNIPPET_LINE_PATTERN = re.compile(
    r"^\s*(?:[-*]\s*)?"
    r"(?:代表片段|Representative snippet|Representative excerpt)\s*[:：].*$",
    re.IGNORECASE,
)
_REDUNDANT_REFERENCE_BULLET_PATTERN = re.compile(
    r"^\s*-\s*(?:参考|Reference|Link)\s*[:：]",
    re.IGNORECASE,
)
_MARKDOWN_LINK_PATTERN = re.compile(r"\[[^\]]+\]\((?P<url>[^)]+)\)")
_TRAILING_PARENTHESES_LINK_PATTERN = re.compile(
    r"\s*[（(]\[[^\]]+\]\((?P<url>[^)]+)\)[）)]\s*$"
)


def _clean_overview_line(line: str) -> str:
    if _REDUNDANT_REFERENCE_BULLET_PATTERN.match(line):
        return ""
    if _STANDALONE_REPRESENTATIVE_SNIPPET_LINE_PATTERN.match(line):
        return ""
    if not _ORDERED_LIST_ITEM_PATTERN.match(line):
        return line

    cleaned = _REPRESENTATIVE_SNIPPET_PATTERN.sub("", line).rstrip()
    first_link = _MARKDOWN_LINK_PATTERN.search(cleaned)
    trailing_link = _TRAILING_PARENTHESES_LINK_PATTERN.search(cleaned)
    if (
        first_link is not None
        and trailing_link is not None
        and first_link.group("url").strip() == trailing_link.group("url").strip()
        and first_link.start() < trailing_link.start()
    ):
        return cleaned[: trailing_link.start()].rstrip()
    return cleaned


def _drop_leading_overview_heading(lines: list[str]) -> list[str]:
    remaining = list(lines)
    while remaining and not remaining[0].strip():
        remaining.pop(0)
    while remaining and _OVERVIEW_HEADING_PATTERN.match(remaining[0].strip()):
        remaining.pop(0)
        while remaining and not remaining[0].strip():
            remaining.pop(0)
    return remaining


def _normalize_top_heading(lines: list[str], *, start: int) -> int:
    match = _TOP_N_HEADING_PATTERN.match(lines[start])
    if match is None:
        return start + 1
    item_total = 0
    look_ahead = start + 1
    while look_ahead < len(lines):
        current = lines[look_ahead]
        if re.match(r"^\s{0,3}#{1,6}\s+", current):
            break
        if _ORDERED_LIST_ITEM_PATTERN.match(current):
            item_total += 1
        look_ahead += 1
    if item_total > 0:
        lines[start] = f"{match.group('heading')} Top-{item_total} 必读"
    return look_ahead


def sanitize_trend_overview_markdown(value: str) -> str:
    normalized = str(value or "").replace("\r\n", "\n").replace("\r", "\n")
    if not normalized.strip():
        return ""

    lines = _drop_leading_overview_heading(normalized.split("\n"))
    for idx, line in enumerate(lines):
        lines[idx] = _clean_overview_line(line)

    idx = 0
    while idx < len(lines):
        idx = _normalize_top_heading(lines, start=idx)
    return "\n".join(lines).strip()


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
            value = cleaned[idx + offset] if idx + offset < len(cleaned) else ""
            cell = soup.new_tag("td")
            cell["class"] = "topic-cell topic-cell-empty" if not value else "topic-cell"
            if value:
                cell.append(value)
            row.append(cell)
        tbody.append(row)
    return table


def _append_section(
    *,
    sections: list[TrendPdfSection],
    heading: str,
    current_nodes: list[str],
) -> None:
    if not current_nodes:
        return
    sections.append(
        TrendPdfSection(
            heading=heading,
            slug=slugify(heading) or "section",
            inner_html="".join(current_nodes).strip(),
        )
    )


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
                not current_nodes
                and _is_primary_trend_section_heading(current_heading)
                and not _is_primary_trend_section_heading(next_heading)
            ):
                extracted.name = "h3"
                current_nodes.append(str(extracted))
                continue
            _append_section(
                sections=sections,
                heading=current_heading,
                current_nodes=current_nodes,
            )
            current_heading = next_heading
            current_nodes = []
            continue
        current_nodes.append(str(extracted))

    _append_section(
        sections=sections,
        heading=current_heading,
        current_nodes=current_nodes,
    )
    return title, sections


def _render_section_label_html(heading: str) -> str:
    return f"<h2 class='section-label'>{html.escape(heading)}</h2>"


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
        "<table class='cluster-grid'>" + "".join(rows) + "</table>"
        "</section>"
    )


def _render_generic_section_html(
    *,
    section: TrendPdfSection,
    compact: bool = False,
) -> str:
    modifier = " section-compact" if compact else ""
    return (
        f"<section class='content-section{modifier} section-{section.slug}'>"
        f"{_render_section_label_html(section.heading)}"
        f"<div class='content-prose'>{section.inner_html}</div>"
        "</section>"
    )


def _render_pdf_summary_grid(sections: list[TrendPdfSection]) -> tuple[str, set[str]]:
    summary_sections: list[tuple[TrendPdfSection, str]] = []
    used: set[str] = set()
    for section in sections:
        if _section_matches(section.heading, "tl;dr", "summary"):
            summary_sections.append((section, "summary-primary"))
            used.add(section.slug)
        elif _section_matches(section.heading, "must-read"):
            summary_sections.append((section, "summary-secondary"))
            used.add(section.slug)
    if not summary_sections:
        return "", used
    cells = "".join(
        _render_summary_panel_html(section=section, modifier=modifier)
        for section, modifier in summary_sections[:2]
    )
    return (
        "<section class='summary-grid-wrap'>"
        "<table class='summary-grid'><tr>"
        f"{cells}"
        "</tr></table>"
        "</section>"
    ), used


def decorate_trend_pdf_body_html(*, body_html: str) -> tuple[str, str]:
    title, sections = _extract_trend_pdf_sections(body_html=body_html)
    rendered: list[str] = []
    summary_grid, used = _render_pdf_summary_grid(sections)
    if summary_grid:
        rendered.append(summary_grid)

    for section in sections:
        if section.slug in used:
            continue
        if _section_matches(section.heading, "overview"):
            rendered.append(_render_generic_section_html(section=section))
            used.add(section.slug)
        elif _section_matches(section.heading, "topics"):
            used.add(section.slug)
        elif _section_matches(section.heading, "clusters"):
            rendered.append(_render_cluster_grid_html(section=section))
            used.add(section.slug)
        elif _section_matches(section.heading, "highlight"):
            rendered.append(_render_generic_section_html(section=section, compact=True))
            used.add(section.slug)

    for section in sections:
        if section.slug not in used:
            rendered.append(_render_generic_section_html(section=section))
    return "<div class='brief-flow'>" + "".join(rendered) + "</div>", title


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


def _render_browser_summary_cards(sections: list[TrendPdfSection]) -> tuple[list[str], set[str]]:
    rendered: list[str] = []
    used: set[str] = set()
    for section in sections:
        card_classes = None
        if _section_matches(section.heading, "tl;dr", "summary"):
            card_classes = "surface-card section-card summary-card summary-card-primary"
        elif _section_matches(section.heading, "must-read"):
            card_classes = "surface-card section-card summary-card summary-card-secondary"
        if card_classes is None:
            continue
        rendered.append(
            _render_browser_content_card_html(
                heading=section.heading,
                inner_html=section.inner_html,
                card_classes=card_classes,
            )
        )
        used.add(section.slug)
    return rendered, used


def _render_browser_section(
    *,
    section: TrendPdfSection,
    render_browser_evolution_section_html: Callable[..., str],
    allow_evolution_disclosure: bool,
) -> tuple[str | None, bool]:
    if _section_matches(section.heading, "overview"):
        return (
            _render_browser_content_card_html(
                heading=section.heading,
                inner_html=section.inner_html,
            ),
            True,
        )
    if _section_matches(section.heading, "evolution"):
        return (
            render_browser_evolution_section_html(
                section=section,
                allow_disclosure=allow_evolution_disclosure,
            ),
            True,
        )
    if _section_matches(section.heading, "topics"):
        return None, True
    if _section_matches(section.heading, "clusters"):
        return _render_browser_clusters_section_html(section=section), True
    if _section_matches(section.heading, "highlight"):
        return (
            _render_browser_content_card_html(
                heading=section.heading,
                inner_html=section.inner_html,
                card_classes="surface-card section-card highlight-card",
            ),
            True,
        )
    return None, False


def build_trend_browser_body_html(
    *,
    sections: list[TrendPdfSection],
    render_browser_evolution_section_html: Callable[..., str],
    allow_evolution_disclosure: bool = True,
) -> str:
    rendered: list[str] = []
    summary_cards, used = _render_browser_summary_cards(sections)
    if summary_cards:
        rendered.append(
            "<section class='summary-grid'>" + "".join(summary_cards[:2]) + "</section>"
        )

    for section in sections:
        if section.slug in used:
            continue
        section_html, handled = _render_browser_section(
            section=section,
            render_browser_evolution_section_html=render_browser_evolution_section_html,
            allow_evolution_disclosure=allow_evolution_disclosure,
        )
        if handled:
            used.add(section.slug)
        if section_html is not None:
            rendered.append(section_html)

    for section in sections:
        if section.slug not in used:
            rendered.append(
                _render_browser_content_card_html(
                    heading=section.heading,
                    inner_html=section.inner_html,
                )
            )
    return "<div class='document-flow'>" + "".join(rendered) + "</div>"


__all__ = [
    "_build_topic_grid",
    "_extract_cluster_entries",
    "_extract_topic_items",
    "_extract_trend_pdf_sections",
    "_is_primary_trend_section_heading",
    "_normalize_section_heading",
    "_render_browser_clusters_section_html",
    "_render_browser_content_card_html",
    "_render_browser_section_label_html",
    "_render_browser_topics_section_html",
    "_render_cluster_grid_html",
    "_render_generic_section_html",
    "_render_section_label_html",
    "_render_summary_panel_html",
    "_render_topics_section_html",
    "_section_matches",
    "build_trend_browser_body_html",
    "decorate_trend_pdf_body_html",
    "sanitize_trend_overview_markdown",
]
