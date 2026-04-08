from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class TrendPdfSection:
    heading: str
    slug: str
    inner_html: str


__all__ = ["TrendPdfSection"]
