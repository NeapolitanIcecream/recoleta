from __future__ import annotations

import html
import re
from typing import Callable

from bs4 import BeautifulSoup, Tag

from recoleta.publish.trend_render_models import (
    TrendEvolutionSectionData,
    TrendEvolutionSignal,
    TrendPdfSection,
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


def _should_collapse_evolution_signal(value: str) -> bool:
    visible_length = len(" ".join(str(value or "").split()).strip())
    return visible_length > 320


def _evolution_change_tone(change_type: str) -> str:
    normalized = str(change_type or "").strip().lower()
    tone_by_change = {
        "continuing": "continuing",
        "延续": "continuing",
        "emerging": "emerging",
        "new": "emerging",
        "新出现": "emerging",
        "fading": "fading",
        "降温": "fading",
        "shifting": "shifting",
        "转向": "shifting",
        "polarizing": "polarizing",
        "分歧加剧": "polarizing",
    }
    return tone_by_change.get(normalized, "mixed")


def _evolution_change_label(change_type: str) -> str:
    tone = _evolution_change_tone(change_type)
    return {
        "continuing": "Continuing",
        "emerging": "Emerging",
        "fading": "Fading",
        "shifting": "Shifting",
        "polarizing": "Polarizing",
    }.get(tone, "Unspecified")


def _extract_history_links(li: Tag) -> list[tuple[str, str]]:
    return [
        (str(link.get("href") or "").strip(), link.get_text(" ", strip=True))
        for link in li.find_all("a")
        if str(link.get("href") or "").strip() and link.get_text(" ", strip=True)
    ]


def _extract_history_metadata(meta_list: Tag | None) -> tuple[str, list[str], list[tuple[str, str]]]:
    if meta_list is None:
        return "", [], []

    change_type = ""
    history_labels: list[str] = []
    history_links: list[tuple[str, str]] = []
    for li in meta_list.find_all("li", recursive=False):
        raw_text = li.get_text(" ", strip=True)
        parsed_change = _strip_labeled_value(raw_text, labels=("变化", "Change"))
        if parsed_change is not None:
            change_type = parsed_change
            continue

        parsed_history = _strip_labeled_value(
            raw_text,
            labels=("历史窗口", "History windows", "History window"),
        )
        if parsed_history is None:
            continue

        links = _extract_history_links(li)
        if links:
            history_links.extend(links)
            history_labels.extend(label for _href, label in links)
            continue

        history_labels.extend(
            segment.strip()
            for segment in re.split(r"[,，]", parsed_history)
            if segment.strip()
        )
    return change_type, history_labels, history_links


def _extract_evolution_signal(
    *,
    theme: str,
    signal_nodes: list[str],
) -> TrendEvolutionSignal:
    soup = BeautifulSoup("".join(signal_nodes).strip(), "html.parser")
    meta_list = None
    for node in list(soup.contents):
        if isinstance(node, Tag) and node.name in {"ul", "ol"}:
            meta_list = node.extract()
            break

    change_type, history_labels, history_links = _extract_history_metadata(meta_list)
    summary_html = "".join(str(node) for node in soup.contents if str(node).strip()).strip()
    return TrendEvolutionSignal(
        theme=theme,
        change_type=change_type,
        change_tone=_evolution_change_tone(change_type),
        history_labels=history_labels,
        history_links=history_links,
        summary_html=summary_html,
    )


def _append_signal(
    *,
    signals: list[TrendEvolutionSignal],
    theme: str | None,
    signal_nodes: list[str],
) -> None:
    if theme is None:
        return
    signals.append(_extract_evolution_signal(theme=theme, signal_nodes=signal_nodes))


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
            _append_signal(
                signals=signals,
                theme=current_theme,
                signal_nodes=current_signal_nodes,
            )
            current_theme = extracted.get_text(" ", strip=True) or "Signal"
            current_signal_nodes = []
            continue
        if not seen_signal:
            summary_nodes.append(str(extracted))
            continue
        current_signal_nodes.append(str(extracted))

    _append_signal(
        signals=signals,
        theme=current_theme,
        signal_nodes=current_signal_nodes,
    )
    summary_html = "".join(summary_nodes).strip()
    if not summary_html and not signals:
        return None
    return TrendEvolutionSectionData(summary_html=summary_html, signals=signals)


def _render_signal_summary(
    *,
    signal: TrendEvolutionSignal,
    allow_disclosure: bool,
) -> str:
    visible_text = _html_visible_text(signal.summary_html)
    if not visible_text:
        return ""
    if not allow_disclosure or not _should_collapse_evolution_signal(visible_text):
        return f"<div class='evolution-copy prose'>{signal.summary_html}</div>"
    preview = html.escape(_truncate_browser_visible_text(visible_text, limit=170))
    return (
        "<details class='evolution-expand'>"
        "<summary class='evolution-expand-toggle'>"
        f"<span class='evolution-expand-summary-copy'>{preview}</span>"
        "<span class='evolution-expand-label evolution-expand-label-more'>Read full rationale</span>"
        "<span class='evolution-expand-label evolution-expand-label-less'>Collapse</span>"
        "</summary>"
        f"<div class='evolution-expand-body prose'>{signal.summary_html}</div>"
        "</details>"
    )


def _render_signal_history(signal: TrendEvolutionSignal) -> str:
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
    if not history_pills:
        return ""
    return (
        "<div class='evolution-history-block'>"
        "<div class='evolution-history-label'>History</div>"
        f"<div class='evolution-history-track'>{''.join(history_pills)}</div>"
        "</div>"
    )


def _render_signal_card(
    *,
    signal: TrendEvolutionSignal,
    allow_disclosure: bool,
) -> str:
    return (
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
            _render_signal_history(signal),
            _render_signal_summary(signal=signal, allow_disclosure=allow_disclosure),
        )
    )


def render_browser_evolution_section_html(
    *,
    section: TrendPdfSection,
    allow_disclosure: bool,
    render_browser_content_card_html: Callable[..., str],
    render_browser_section_label_html: Callable[[str], str],
) -> str:
    evolution = _extract_evolution_section_data(section=section)
    if evolution is None or not evolution.signals:
        return render_browser_content_card_html(
            heading=section.heading,
            inner_html=section.inner_html,
        )

    history_label_total = len(
        {
            label
            for signal in evolution.signals
            for label in signal.history_labels
            if label
        }
    )
    stat_pills = [
        (
            "<span class='evolution-stat'>"
            + f"{len(evolution.signals)} signal"
            + ("s" if len(evolution.signals) != 1 else "")
            + "</span>"
        )
    ]
    if history_label_total:
        stat_pills.append(
            (
                "<span class='evolution-stat secondary'>"
                + f"{history_label_total} history window"
                + ("s" if history_label_total != 1 else "")
                + "</span>"
            )
        )

    summary_html = (
        f"<div class='evolution-summary prose'>{evolution.summary_html}</div>"
        if evolution.summary_html
        else ""
    )
    cards = "".join(
        _render_signal_card(signal=signal, allow_disclosure=allow_disclosure)
        for signal in evolution.signals
    )
    return (
        "<section class='surface-card section-card evolution-section'>"
        "<div class='evolution-section-head'>"
        f"{render_browser_section_label_html(section.heading)}"
        f"<div class='evolution-stats'>{''.join(stat_pills)}</div>"
        "</div>"
        f"{summary_html}"
        f"<div class='evolution-grid'>{cards}</div>"
        "</section>"
    )


__all__ = [
    "_evolution_change_label",
    "_evolution_change_tone",
    "_extract_evolution_section_data",
    "_extract_evolution_signal",
    "_strip_labeled_value",
    "render_browser_evolution_section_html",
]
