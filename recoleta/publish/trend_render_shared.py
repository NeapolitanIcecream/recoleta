from __future__ import annotations

from datetime import datetime, timezone
import html
import re
from typing import Any

import yaml

from recoleta.publish.trend_render_models import (
    TrendPdfSection,
)
from recoleta.publish.trend_render_sections import (
    _build_topic_grid,
    _extract_cluster_entries,
    _extract_topic_items,
    _extract_trend_pdf_sections,
    _is_primary_trend_section_heading,
    _normalize_section_heading,
    _render_browser_clusters_section_html,
    _render_browser_content_card_html,
    _render_browser_section_label_html,
    _render_browser_topics_section_html,
    _render_cluster_grid_html,
    _render_generic_section_html,
    _render_section_label_html,
    _render_summary_panel_html,
    _render_topics_section_html,
    _section_matches,
    build_trend_browser_body_html,
    decorate_trend_pdf_body_html,
    sanitize_trend_overview_markdown,
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


def _strip_labeled_value(value: str, *, labels: tuple[str, ...]) -> str | None:
    normalized = str(value or "").strip()
    if not normalized:
        return None
    for label in labels:
        pattern = re.compile(rf"^\s*{re.escape(label)}\s*[:：]\s*(.+)$", re.IGNORECASE)
        match = pattern.match(normalized)
        if match is not None:
            extracted = str(match.group(1) or "").strip()
            return extracted or None
    return None


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
    return f"{granularity.title()} trends page with an overview, evidence-backed clusters, and linked notes."


def _decorate_trend_pdf_body_html(*, body_html: str) -> tuple[str, str]:
    return decorate_trend_pdf_body_html(body_html=body_html)


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
        "<div class='hero-kicker'>Recoleta Trends</div>"
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


def _build_trend_browser_body_html(
    *,
    sections: list[TrendPdfSection],
) -> str:
    return build_trend_browser_body_html(sections=sections)


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
        "<div class='hero-kicker'>Recoleta Trends</div>"
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


__all__ = [
    "TrendPdfSection",
    "_build_topic_grid",
    "_build_trend_browser_body_html",
    "_build_trend_browser_pdf_html",
    "_build_trend_pdf_html",
    "_decorate_trend_pdf_body_html",
    "_extract_cluster_entries",
    "_extract_topic_items",
    "_extract_trend_pdf_sections",
    "_is_primary_trend_section_heading",
    "_normalize_obsidian_callouts_for_pdf",
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
    "_split_yaml_frontmatter_text",
    "_strip_labeled_value",
    "_trend_date_token",
    "_trend_pdf_hero_dek",
    "_trend_pdf_meta_rows",
    "_trend_pdf_period_label",
    "_trend_pdf_topics_summary",
    "clamp_trend_overview_markdown",
    "sanitize_trend_overview_markdown",
    "sanitize_trend_title",
]
