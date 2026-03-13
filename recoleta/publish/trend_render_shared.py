from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import html
import re
from typing import Any

from bs4 import BeautifulSoup, Tag
from slugify import slugify
import yaml


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
_TREND_DATE_PREFIX_PATTERN = r"(?:\d{4}-\d{2}-\d{2}|\d{4}-W\d{2}|\d{4}-\d{2}(?!-\d{2}))"
_GENERIC_TREND_TITLE_PREFIX_RE = re.compile(
    r"^\s*(?:" + _TREND_DATE_PREFIX_PATTERN + r"\s*"
    r"(?:[|｜:：\-—]\s*)?"
    r")?"
    r"(?:"
    r"研究趋势日报|研究趋势周报|研究趋势月报|趋势日报|趋势周报|趋势月报|"
    r"每日趋势|每周趋势|每月趋势|"
    r"daily trend|weekly trend|monthly trend|trend brief|research trend(?:s)?"
    r")"
    r"\s*(?:[|｜:：\-—]\s*)*",
    re.IGNORECASE,
)
_DATE_ONLY_PREFIX_RE = re.compile(
    r"^\s*" + _TREND_DATE_PREFIX_PATTERN + r"\s*(?:[|｜:：\-—]\s*)+"
)
_TOP_LEVEL_H2_RE = re.compile(r"^\s{0,3}##\s+")
_MARKDOWN_STRIP_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_MARKDOWN_STRIP_DECORATION_RE = re.compile(r"[`*_>#]")


def sanitize_trend_overview_markdown(value: str) -> str:
    normalized = str(value or "").replace("\r\n", "\n").replace("\r", "\n")
    if not normalized.strip():
        return ""

    lines = normalized.split("\n")
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and _OVERVIEW_HEADING_PATTERN.match(lines[0].strip()):
        lines.pop(0)
        while lines and not lines[0].strip():
            lines.pop(0)

    for idx, line in enumerate(lines):
        if _REDUNDANT_REFERENCE_BULLET_PATTERN.match(line):
            lines[idx] = ""
            continue
        if _STANDALONE_REPRESENTATIVE_SNIPPET_LINE_PATTERN.match(line):
            lines[idx] = ""
            continue
        if not _ORDERED_LIST_ITEM_PATTERN.match(line):
            continue
        cleaned = _REPRESENTATIVE_SNIPPET_PATTERN.sub("", line).rstrip()
        first_link = _MARKDOWN_LINK_PATTERN.search(cleaned)
        trailing_link = _TRAILING_PARENTHESES_LINK_PATTERN.search(cleaned)
        if (
            first_link is not None
            and trailing_link is not None
            and first_link.group("url").strip() == trailing_link.group("url").strip()
            and first_link.start() < trailing_link.start()
        ):
            cleaned = cleaned[: trailing_link.start()].rstrip()
        lines[idx] = cleaned

    idx = 0
    while idx < len(lines):
        match = _TOP_N_HEADING_PATTERN.match(lines[idx])
        if match is None:
            idx += 1
            continue

        item_total = 0
        look_ahead = idx + 1
        while look_ahead < len(lines):
            current = lines[look_ahead]
            if re.match(r"^\s{0,3}#{1,6}\s+", current):
                break
            if _ORDERED_LIST_ITEM_PATTERN.match(current):
                item_total += 1
            look_ahead += 1
        if item_total > 0:
            lines[idx] = f"{match.group('heading')} Top-{item_total} 必读"
        idx = look_ahead

    sanitized = "\n".join(lines).strip()
    return sanitized


def sanitize_trend_title(value: str, *, fallback: str = "Trend") -> str:
    normalized = " ".join(str(value or "").split()).strip()
    if not normalized:
        return fallback
    cleaned = _DATE_ONLY_PREFIX_RE.sub("", normalized).strip()
    cleaned = _GENERIC_TREND_TITLE_PREFIX_RE.sub("", cleaned).strip()
    cleaned = re.sub(r"^[|｜:：\-—\s]+", "", cleaned).strip()
    cleaned = _markdownish_plain_text(cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned or fallback


def _split_trend_overview_prelude(value: str) -> tuple[str, str]:
    lines = str(value or "").splitlines()
    prelude: list[str] = []
    suffix: list[str] = []
    in_suffix = False
    for line in lines:
        if _TOP_LEVEL_H2_RE.match(line):
            in_suffix = True
        if in_suffix:
            suffix.append(line)
        else:
            prelude.append(line)
    return "\n".join(prelude).strip(), "\n".join(suffix).strip()


def _markdownish_plain_text(value: str) -> str:
    normalized = str(value or "")
    normalized = _MARKDOWN_STRIP_LINK_RE.sub(r"\1", normalized)
    normalized = _MARKDOWN_STRIP_DECORATION_RE.sub(" ", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


def _truncate_visible_text(value: str, *, chinese_output: bool) -> str:
    normalized = " ".join(str(value or "").split()).strip()
    if not normalized:
        return ""
    if chinese_output:
        compact = re.sub(r"\s+", "", normalized)
        if len(compact) <= 199:
            return compact
        boundary = 199
        for idx in range(0, min(len(compact), 199)):
            if compact[idx] in "。！？；.!?;":
                boundary = idx + 1
        return compact[:boundary].strip()

    words = normalized.split()
    if len(words) <= 199:
        return normalized
    candidate = " ".join(words[:199]).strip()
    boundary = max(candidate.rfind(". "), candidate.rfind("! "), candidate.rfind("? "))
    if boundary >= 80:
        candidate = candidate[: boundary + 1].strip()
    return candidate


def _visible_text_within_limit(value: str, *, chinese_output: bool) -> bool:
    normalized = " ".join(str(value or "").split()).strip()
    if not normalized:
        return True
    if chinese_output:
        compact = re.sub(r"\s+", "", normalized)
        return len(compact) <= 199
    return len(normalized.split()) <= 199


def clamp_trend_overview_markdown(
    value: str,
    *,
    output_language: str | None = None,
) -> str:
    sanitized = sanitize_trend_overview_markdown(value)
    if not sanitized:
        return ""
    prelude, suffix = _split_trend_overview_prelude(sanitized)
    if not prelude:
        return sanitized
    chinese_output = False
    normalized_language = str(output_language or "").strip().lower()
    if normalized_language:
        chinese_output = normalized_language.startswith("zh") or (
            "chinese" in normalized_language
        )
    visible_plain_text = _markdownish_plain_text(prelude)
    if _visible_text_within_limit(visible_plain_text, chinese_output=chinese_output):
        truncated_prelude = prelude.strip()
    else:
        truncated_prelude = _truncate_visible_text(
            visible_plain_text,
            chinese_output=chinese_output,
        )
    parts = [truncated_prelude.strip()] if truncated_prelude.strip() else []
    if suffix:
        parts.append(suffix)
    return "\n\n".join(part for part in parts if part).strip()


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
        ("Topics", str(topic_count) if topic_count > 0 else "None"),
    ]


def _trend_pdf_hero_dek(frontmatter: dict[str, Any]) -> str:
    granularity = str(frontmatter.get("granularity") or "").strip().lower() or "trend"
    return f"{granularity.title()} trend brief with overview, must-read papers, and cluster notes."


@dataclass(slots=True)
class TrendPdfSection:
    heading: str
    slug: str
    inner_html: str


@dataclass(slots=True)
class TrendEvolutionSignal:
    theme: str
    change_type: str
    change_tone: str
    history_labels: list[str]
    history_links: list[tuple[str, str]]
    summary_html: str


@dataclass(slots=True)
class TrendEvolutionSectionData:
    summary_html: str
    signals: list[TrendEvolutionSignal]


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
    *, section: TrendPdfSection, compact: bool = False
) -> str:
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


def _strip_labeled_value(value: str, *, labels: tuple[str, ...]) -> str | None:
    for label in labels:
        pattern = re.compile(
            rf"^\s*{re.escape(label)}\s*[:：]\s*(?P<value>.+?)\s*$",
            re.IGNORECASE,
        )
        match = pattern.match(str(value or ""))
        if match is not None:
            return str(match.group("value") or "").strip()
    return None


def _html_visible_text(value: str) -> str:
    return BeautifulSoup(str(value or ""), "html.parser").get_text(" ", strip=True)


def _truncate_browser_visible_text(value: str, *, limit: int = 180) -> str:
    collapsed = " ".join(str(value or "").split()).strip()
    if len(collapsed) <= limit:
        return collapsed
    boundary = collapsed.rfind(" ", 0, limit)
    if boundary < max(60, limit // 2):
        boundary = limit
    return collapsed[:boundary].rstrip() + "…"


def _evolution_change_tone(change_type: str) -> str:
    normalized = str(change_type or "").strip().lower()
    if normalized in {"continuing", "延续"}:
        return "continuing"
    if normalized in {"emerging", "new", "新出现"}:
        return "emerging"
    if normalized in {"fading", "降温"}:
        return "fading"
    if normalized in {"shifting", "转向"}:
        return "shifting"
    if normalized in {"polarizing", "分歧加剧"}:
        return "polarizing"
    return "mixed"


def _evolution_change_label(change_type: str) -> str:
    tone = _evolution_change_tone(change_type)
    return {
        "continuing": "Continuing",
        "emerging": "Emerging",
        "fading": "Fading",
        "shifting": "Shifting",
        "polarizing": "Polarizing",
    }.get(tone, "Unspecified")


def _extract_evolution_signal(
    *,
    theme: str,
    signal_nodes: list[str],
) -> TrendEvolutionSignal:
    soup = BeautifulSoup("".join(signal_nodes).strip(), "html.parser")
    meta_list: Tag | None = None
    for node in list(soup.contents):
        if isinstance(node, Tag) and node.name in {"ul", "ol"}:
            meta_list = node.extract()
            break

    change_type = ""
    history_labels: list[str] = []
    history_links: list[tuple[str, str]] = []
    if meta_list is not None:
        for li in meta_list.find_all("li", recursive=False):
            raw_text = li.get_text(" ", strip=True)
            parsed_change = _strip_labeled_value(
                raw_text,
                labels=("变化", "Change"),
            )
            if parsed_change is not None:
                change_type = parsed_change
                continue

            parsed_history = _strip_labeled_value(
                raw_text,
                labels=("历史窗口", "History windows", "History window"),
            )
            if parsed_history is None:
                continue

            links = [
                (str(link.get("href") or "").strip(), link.get_text(" ", strip=True))
                for link in li.find_all("a")
                if str(link.get("href") or "").strip()
                and link.get_text(" ", strip=True)
            ]
            if links:
                history_links.extend(links)
                history_labels.extend(label for _href, label in links)
                continue

            history_labels.extend(
                [
                    segment.strip()
                    for segment in re.split(r"[,，]", parsed_history)
                    if segment.strip()
                ]
            )

    summary_html = "".join(
        str(node) for node in soup.contents if str(node).strip()
    ).strip()
    return TrendEvolutionSignal(
        theme=theme,
        change_type=change_type,
        change_tone=_evolution_change_tone(change_type),
        history_labels=history_labels,
        history_links=history_links,
        summary_html=summary_html,
    )


def _extract_evolution_section_data(
    *,
    section: TrendPdfSection,
) -> TrendEvolutionSectionData | None:
    soup = BeautifulSoup(section.inner_html, "html.parser")
    summary_nodes: list[str] = []
    signals: list[TrendEvolutionSignal] = []
    current_theme: str | None = None
    current_signal_nodes: list[str] = []
    seen_signal = False

    for node in list(soup.contents):
        extracted = node.extract()
        if not str(extracted).strip():
            continue
        if isinstance(extracted, Tag) and extracted.name == "h3":
            seen_signal = True
            if current_theme is not None:
                signals.append(
                    _extract_evolution_signal(
                        theme=current_theme,
                        signal_nodes=current_signal_nodes,
                    )
                )
            current_theme = extracted.get_text(" ", strip=True) or "Signal"
            current_signal_nodes = []
            continue
        if not seen_signal:
            summary_nodes.append(str(extracted))
            continue
        current_signal_nodes.append(str(extracted))

    if current_theme is not None:
        signals.append(
            _extract_evolution_signal(
                theme=current_theme,
                signal_nodes=current_signal_nodes,
            )
        )

    summary_html = "".join(summary_nodes).strip()
    if not summary_html and not signals:
        return None
    return TrendEvolutionSectionData(summary_html=summary_html, signals=signals)


def _render_browser_evolution_section_html(*, section: TrendPdfSection) -> str:
    evolution = _extract_evolution_section_data(section=section)
    if evolution is None or not evolution.signals:
        return _render_browser_content_card_html(
            heading=section.heading,
            inner_html=section.inner_html,
        )

    history_labels = {
        label
        for signal in evolution.signals
        for label in signal.history_labels
        if label
    }
    stat_pills = [
        (
            "<span class='evolution-stat'>"
            + f"{len(evolution.signals)} signal"
            + ("s" if len(evolution.signals) != 1 else "")
            + "</span>"
        )
    ]
    if history_labels:
        stat_pills.append(
            (
                "<span class='evolution-stat secondary'>"
                + f"{len(history_labels)} history window"
                + ("s" if len(history_labels) != 1 else "")
                + "</span>"
            )
        )

    def render_signal_summary(signal: TrendEvolutionSignal) -> str:
        visible_text = _html_visible_text(signal.summary_html)
        if not visible_text:
            return ""
        if len(visible_text) <= 220:
            return f"<div class='evolution-copy prose'>{signal.summary_html}</div>"
        preview = html.escape(_truncate_browser_visible_text(visible_text, limit=170))
        return (
            f"<div class='evolution-preview'>{preview}</div>"
            "<details class='evolution-expand'>"
            "<summary class='evolution-expand-toggle'>Read full rationale</summary>"
            f"<div class='evolution-expand-body prose'>{signal.summary_html}</div>"
            "</details>"
        )

    cards = []
    for signal in evolution.signals:
        history_pills: list[str] = []
        if signal.history_links:
            history_pills.extend(
                "<a class='history-pill' href='{}'>{}</a>".format(
                    html.escape(href, quote=True),
                    html.escape(label),
                )
                for href, label in signal.history_links
            )
        elif signal.history_labels:
            history_pills.extend(
                f"<span class='history-pill'>{html.escape(label)}</span>"
                for label in signal.history_labels
            )

        history_html = ""
        if history_pills:
            history_html = (
                "<div class='evolution-history-block'>"
                "<div class='evolution-history-label'>History</div>"
                f"<div class='evolution-history-track'>{''.join(history_pills)}</div>"
                "</div>"
            )

        summary_html = render_signal_summary(signal)
        cards.append(
            "<article class='evolution-card evolution-change-{}'>"
            "<div class='evolution-card-head'>"
            "<h3 class='evolution-card-title'>{}</h3>"
            "<span class='evolution-badge evolution-badge-{}'>{}</span>"
            "</div>"
            "{}"
            "{}"
            "</article>".format(
                html.escape(signal.change_tone, quote=True),
                html.escape(signal.theme),
                html.escape(signal.change_tone, quote=True),
                html.escape(_evolution_change_label(signal.change_type)),
                history_html,
                summary_html,
            )
        )

    summary_html = (
        f"<div class='evolution-summary prose'>{evolution.summary_html}</div>"
        if evolution.summary_html
        else ""
    )
    return (
        "<section class='surface-card section-card evolution-section'>"
        "<div class='evolution-section-head'>"
        f"{_render_browser_section_label_html(section.heading)}"
        f"<div class='evolution-stats'>{''.join(stat_pills)}</div>"
        "</div>"
        f"{summary_html}"
        f"<div class='evolution-grid'>{''.join(cards)}</div>"
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
            "<section class='summary-grid'>" + "".join(summary_cards[:2]) + "</section>"
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
        elif _section_matches(section.heading, "evolution"):
            rendered.append(_render_browser_evolution_section_html(section=section))
            used.add(section.slug)
        elif _section_matches(section.heading, "topics"):
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
