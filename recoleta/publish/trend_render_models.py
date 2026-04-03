from __future__ import annotations

from dataclasses import dataclass


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


__all__ = [
    "TrendEvolutionSectionData",
    "TrendEvolutionSignal",
    "TrendPdfSection",
]
