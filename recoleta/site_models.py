from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass(slots=True, frozen=True)
class TrendSiteInputSpec:
    path: Path
    instance: str | None = None


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
    instance: str | None
    body_html: str
    excerpt: str
    evolution_insight: str | None
    frontmatter: dict[str, Any]


@dataclass(slots=True)
class TrendSiteInputDirectory:
    path: Path
    root_path: Path
    inbox_path: Path | None
    ideas_path: Path | None
    instance: str | None
    language_code: str | None = None
    language_slug: str | None = None
    is_localized_root: bool = False


@dataclass(slots=True)
class TrendSiteSourceDocument:
    markdown_path: Path
    pdf_path: Path | None
    stem: str
    frontmatter: dict[str, Any]
    markdown_body: str
    presentation: dict[str, Any] | None
    granularity: str
    period_start: datetime | None
    period_end: datetime | None
    topics: list[str]
    instance: str | None


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
    instance: str | None


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
    instance: str | None
    relevance_score: float | None
    body_html: str
    excerpt: str
    frontmatter: dict[str, Any]


@dataclass(slots=True)
class IdeaSiteSourceDocument:
    markdown_path: Path
    stem: str
    frontmatter: dict[str, Any]
    markdown_body: str
    presentation: dict[str, Any] | None
    granularity: str
    period_start: datetime | None
    period_end: datetime | None
    topics: list[str]
    instance: str | None
    status: str


@dataclass(slots=True)
class IdeaSiteDocument:
    markdown_path: Path
    markdown_asset_path: Path
    page_path: Path
    stem: str
    title: str
    granularity: str
    period_token: str
    period_start: datetime | None
    period_end: datetime | None
    topics: list[str]
    instance: str | None
    status: str
    opportunity_count: int
    evidence_count: int
    body_html: str
    excerpt: str
    frontmatter: dict[str, Any]


@dataclass(slots=True)
class IdeaBodyRenderResult:
    body_html: str
    opportunity_count: int
    evidence_count: int


@dataclass(slots=True)
class ItemSiteSelection:
    source_documents: list[ItemSiteSourceDocument]
    available_total: int
    unreferenced_total: int


type SiteSourceKey = tuple[Path, str | None]


__all__ = [
    "IdeaBodyRenderResult",
    "IdeaSiteDocument",
    "IdeaSiteSourceDocument",
    "ItemSiteDocument",
    "ItemSiteSelection",
    "ItemSiteSourceDocument",
    "SiteSourceKey",
    "TrendSiteDocument",
    "TrendSiteInputDirectory",
    "TrendSiteInputSpec",
    "TrendSiteSourceDocument",
]
