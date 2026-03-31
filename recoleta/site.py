from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
import html
import json
import os
from pathlib import Path
from pathlib import PurePosixPath
import posixpath
import re
import shutil
from typing import Any
from urllib.parse import quote, urlparse

from bs4 import BeautifulSoup, Tag
from loguru import logger
from markdown_it import MarkdownIt
from slugify import slugify

from recoleta.publish.trend_render_shared import (
    _build_trend_browser_body_html,
    _evolution_change_label,
    _extract_evolution_section_data,
    _extract_trend_pdf_sections,
    _render_browser_content_card_html,
    _render_browser_section_label_html,
    _strip_labeled_value,
    _normalize_obsidian_callouts_for_pdf,
    _split_yaml_frontmatter_text,
    _trend_date_token,
    _trend_pdf_hero_dek,
    _trend_pdf_topics_summary,
    sanitize_trend_title,
)
from recoleta.types import DEFAULT_TOPIC_STREAM

RECOLETA_REPO_URL = "https://github.com/NeapolitanIcecream/recoleta"
RECOLETA_QUICKSTART_URL = f"{RECOLETA_REPO_URL}#recoleta-quickstart"


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


def _parse_site_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    normalized = str(value or "").strip().lower()
    return normalized in {"1", "true", "yes", "on"}


def _normalize_item_export_scope(item_export_scope: str | None) -> str:
    normalized = str(item_export_scope or "").strip().lower() or "linked"
    if normalized not in {"linked", "all"}:
        raise ValueError("item_export_scope must be one of: linked, all")
    return normalized


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


def _extract_trend_evolution_insight(sections: list[Any]) -> str | None:
    evolution_data = None
    for section in sections:
        heading = str(getattr(section, "heading", "") or "").strip().lower()
        if "evolution" not in heading:
            continue
        evolution_data = _extract_evolution_section_data(section=section)
        break
    if evolution_data is None:
        return None
    if not evolution_data.signals:
        return None

    change_counts: dict[str, int] = {}
    for signal in evolution_data.signals:
        label = _evolution_change_label(signal.change_type)
        if not label:
            continue
        change_counts[label] = change_counts.get(label, 0) + 1

    parts = [
        f"{len(evolution_data.signals)} signal{'s' if len(evolution_data.signals) != 1 else ''}"
    ]
    parts.extend(f"{label} {count}" for label, count in change_counts.items())
    return " · ".join(parts)


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
    if (
        _host_matches(host=host, domain="openreview.net")
        or normalized_source == "openreview"
    ):
        return "Open OpenReview"
    if _host_matches(host=host, domain="github.com"):
        return "Open GitHub"
    return "Open original"


def _topic_slug(topic: str) -> str:
    return slugify(str(topic or "").strip(), lowercase=True) or "topic"


def _instance_slug(instance: str) -> str:
    return slugify(str(instance or "").strip(), lowercase=True) or "instance"


def _validate_unique_site_instance_slugs(
    instances: Sequence[str | None],
    *,
    context: str,
) -> None:
    slug_to_instances: dict[str, list[str]] = {}
    for instance in instances:
        cleaned_instance = _normalize_site_instance(instance)
        if cleaned_instance is None:
            continue
        instance_slug = _instance_slug(cleaned_instance)
        bucket = slug_to_instances.setdefault(instance_slug, [])
        if cleaned_instance not in bucket:
            bucket.append(cleaned_instance)
    collisions = {
        instance_slug: names
        for instance_slug, names in slug_to_instances.items()
        if len(names) > 1
    }
    if not collisions:
        return
    details = "; ".join(
        f"slug '{instance_slug}' is shared by {', '.join(names)}"
        for instance_slug, names in sorted(collisions.items())
    )
    raise ValueError(f"{context} must produce unique public instance slugs: {details}")


def _normalize_site_instance(instance: str | None) -> str | None:
    cleaned = str(instance or "").strip()
    if not cleaned:
        return None
    return cleaned


def _normalize_legacy_site_stream(stream: str | None) -> str | None:
    cleaned = _normalize_site_instance(stream)
    if cleaned == DEFAULT_TOPIC_STREAM:
        return None
    return cleaned


def _repo_cta_links() -> str:
    repo_href = html.escape(RECOLETA_REPO_URL, quote=True)
    quickstart_href = html.escape(RECOLETA_QUICKSTART_URL, quote=True)
    return (
        f"<a class='action-link action-link-external' href='{repo_href}'>View repo</a>"
        f"<a class='action-link secondary action-link-external' href='{quickstart_href}'>5-minute quickstart</a>"
    )


def _render_repo_cta_card() -> str:
    return (
        "<section class='repo-cta-card'>"
        "<div class='section-kicker'>Built with Recoleta</div>"
        "<h2 class='section-title'>Run your own research radar</h2>"
        "<p class='repo-cta-copy'>"
        "Turn arXiv, Hacker News, OpenReview, Hugging Face Daily Papers, and RSS "
        "into local Markdown, Obsidian notes, Telegram digests, and a public site."
        "</p>"
        f"<div class='card-actions'>{_repo_cta_links()}</div>"
        "</section>"
    )


_STREAM_DISPLAY_INITIALISMS = {
    "ai",
    "api",
    "cpu",
    "cv",
    "gpu",
    "llm",
    "ml",
    "nlp",
    "ocr",
    "qa",
    "rag",
    "rl",
    "ui",
    "ux",
}


def _display_site_instance(instance: str | None) -> str | None:
    cleaned = _normalize_site_instance(instance)
    if cleaned is None:
        return None
    normalized = re.sub(r"[_-]+", " ", cleaned).strip()
    if normalized == cleaned and not cleaned.islower():
        return cleaned
    tokens = [
        token.upper() if token.lower() in _STREAM_DISPLAY_INITIALISMS else token.capitalize()
        for token in normalized.split()
    ]
    return " ".join(tokens) if tokens else cleaned


def _render_instance_meta_pill(instance: str | None) -> str:
    display_instance = _display_site_instance(instance)
    if display_instance is None:
        return ""
    return f"<span class='meta-pill subdued'>{html.escape(display_instance)}</span>"


def _resolve_site_instance(
    *,
    input_instance: str | None,
    frontmatter: dict[str, Any],
) -> str | None:
    if resolved_input_instance := _normalize_site_instance(input_instance):
        return resolved_input_instance
    if resolved_frontmatter_instance := _normalize_site_instance(
        frontmatter.get("instance")
    ):
        return resolved_frontmatter_instance
    if resolved_legacy_stream := _normalize_legacy_site_stream(
        frontmatter.get("stream")
    ):
        return resolved_legacy_stream
    return None


def _paths_overlap(path_a: Path, path_b: Path) -> bool:
    return path_a == path_b or path_a in path_b.parents or path_b in path_a.parents


_TREND_GRANULARITY_SORT_PRIORITY = {
    "month": 3,
    "week": 2,
    "day": 1,
}


def _site_period_sort_key(
    *,
    period_end: datetime | None,
    period_start: datetime | None,
    granularity: str,
    stem: str,
) -> tuple[datetime, int, datetime, str]:
    floor = datetime.min.replace(tzinfo=timezone.utc)
    return (
        period_end or period_start or floor,
        _TREND_GRANULARITY_SORT_PRIORITY.get(granularity, 0),
        period_start or floor,
        stem,
    )


def _trend_site_sort_key(
    document: TrendSiteSourceDocument,
) -> tuple[datetime, int, datetime, str]:
    return _site_period_sort_key(
        period_end=document.period_end,
        period_start=document.period_start,
        granularity=document.granularity,
        stem=document.stem,
    )


def _idea_site_sort_key(
    document: IdeaSiteSourceDocument,
) -> tuple[datetime, int, datetime, str]:
    return _site_period_sort_key(
        period_end=document.period_end,
        period_start=document.period_start,
        granularity=document.granularity,
        stem=document.stem,
    )


def _rendered_document_sort_key(
    document: TrendSiteDocument | IdeaSiteDocument,
) -> tuple[datetime, int, datetime, str]:
    return _site_period_sort_key(
        period_end=document.period_end,
        period_start=document.period_start,
        granularity=document.granularity,
        stem=document.stem,
    )


def _count_label(
    value: int,
    *,
    singular: str,
    plural: str | None = None,
) -> str:
    normalized_plural = plural or f"{singular}s"
    return f"{value} {singular if value == 1 else normalized_plural}"


def _format_collection_mix(
    *,
    trend_count: int = 0,
    idea_count: int = 0,
) -> str:
    parts: list[str] = []
    if trend_count > 0:
        parts.append(_count_label(trend_count, singular="trend"))
    if idea_count > 0:
        parts.append(_count_label(idea_count, singular="idea"))
    if parts:
        return " · ".join(parts)
    return _count_label(0, singular="brief", plural="briefs")


def _format_collection_meta(
    *,
    trend_count: int = 0,
    idea_count: int = 0,
    latest_token: str,
) -> str:
    mix = _format_collection_mix(trend_count=trend_count, idea_count=idea_count)
    return f"{mix} · latest {latest_token}" if latest_token else mix


def _site_date_range_label(
    *,
    period_start: datetime | None,
    period_end: datetime | None,
    fallback: str,
) -> str:
    if period_start is None and period_end is None:
        return fallback
    if period_start is None:
        assert period_end is not None
        return period_end.astimezone(timezone.utc).date().isoformat()
    if period_end is None:
        return period_start.astimezone(timezone.utc).date().isoformat()
    return (
        f"{period_start.astimezone(timezone.utc).date().isoformat()} "
        f"to {period_end.astimezone(timezone.utc).date().isoformat()}"
    )


def _record_latest_document(
    *,
    latest_by_slug: dict[str, TrendSiteDocument | IdeaSiteDocument],
    slug: str,
    document: TrendSiteDocument | IdeaSiteDocument,
) -> None:
    existing = latest_by_slug.get(slug)
    if existing is None or _rendered_document_sort_key(document) > _rendered_document_sort_key(
        existing
    ):
        latest_by_slug[slug] = document


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
    _remove_managed_stage_path(stage_root / "Ideas")
    _remove_managed_stage_path(stage_root / "Inbox")
    _remove_managed_stage_path(stage_root / "Streams")
    trends_output_dir.mkdir(parents=True, exist_ok=True)


def _coerce_site_input_specs(
    input_dir: Path | TrendSiteInputSpec | Sequence[Path | TrendSiteInputSpec],
) -> list[TrendSiteInputSpec]:
    raw_inputs = (
        [input_dir]
        if isinstance(input_dir, Path | TrendSiteInputSpec)
        else list(input_dir)
    )
    if not raw_inputs:
        raise ValueError("Trend input directory list must not be empty")

    resolved_inputs: list[TrendSiteInputSpec] = []
    for raw_input in raw_inputs:
        input_spec = (
            raw_input
            if isinstance(raw_input, TrendSiteInputSpec)
            else TrendSiteInputSpec(path=raw_input)
        )
        resolved_input = input_spec.path.expanduser().resolve()
        if not resolved_input.exists() or not resolved_input.is_dir():
            raise ValueError(f"Trend input directory must exist: {resolved_input}")
        resolved_inputs.append(
            TrendSiteInputSpec(
                path=resolved_input,
                instance=_normalize_site_instance(input_spec.instance),
            )
        )
    _validate_unique_site_instance_slugs(
        [input_spec.instance for input_spec in resolved_inputs],
        context="Explicit trend site input instances",
    )
    return resolved_inputs


def _infer_instance_name_from_trends_dir(path: Path) -> str | None:
    if path.name != "Trends":
        return None
    if len(path.parts) < 3:
        return None
    if path.parent.parent.name == "Streams":
        return path.parent.name
    if len(path.parts) < 5:
        return None
    if path.parent.parent.name != "Localized":
        return None
    if path.parent.parent.parent.parent.name != "Streams":
        return None
    return path.parent.parent.parent.name


def _infer_instance_name_from_site_root(path: Path) -> str | None:
    if len(path.parts) < 2:
        return None
    if path.parent.name == "Streams":
        return path.name
    if len(path.parts) < 4:
        return None
    if path.parent.name != "Localized":
        return None
    if path.parent.parent.parent.name != "Streams":
        return None
    return path.parent.parent.name


def _infer_instance_name_from_site_path(path: Path) -> str | None:
    return _infer_instance_name_from_trends_dir(path) or _infer_instance_name_from_site_root(
        path.parent if path.name == "Trends" else path
    )


def _infer_grouped_child_instance_within_parent(
    *,
    path: Path,
    parent_root: Path,
) -> str | None:
    resolved_path = path.expanduser().resolve()
    resolved_parent_root = parent_root.expanduser().resolve()
    try:
        relative = resolved_path.relative_to(resolved_parent_root)
    except ValueError:
        return None
    if not relative.parts:
        return None
    if resolved_parent_root.name == "Streams":
        return relative.parts[0]
    for index, part in enumerate(relative.parts[:-1]):
        if part == "Streams":
            return relative.parts[index + 1]
    return None


def _discover_trend_site_input_dirs(
    raw_inputs: Sequence[TrendSiteInputSpec],
    *,
    include_localized_children: bool = True,
) -> list[TrendSiteInputDirectory]:
    discovered: list[TrendSiteInputDirectory] = []
    seen_paths: set[tuple[Path, str | None]] = set()

    def add_candidate(candidate: Path, *, instance: str | None) -> None:
        resolved_candidate = candidate.expanduser().resolve()
        resolved_instance = (
            _normalize_site_instance(instance)
            if instance is not None
            else _normalize_legacy_site_stream(
                _infer_instance_name_from_site_path(resolved_candidate)
            )
        )
        if not resolved_candidate.exists() or not resolved_candidate.is_dir():
            return
        if (resolved_candidate, resolved_instance) in seen_paths:
            return
        seen_paths.add((resolved_candidate, resolved_instance))
        root_path = (
            resolved_candidate.parent
            if resolved_candidate.name == "Trends"
            else resolved_candidate
        )
        language_code = _infer_site_language_code_from_root(root_path)
        inbox_path = root_path / "Inbox"
        discovered.append(
            TrendSiteInputDirectory(
                path=resolved_candidate,
                root_path=root_path,
                inbox_path=inbox_path
                if inbox_path.exists() and inbox_path.is_dir()
                else None,
                ideas_path=(
                    root_path / "Ideas"
                    if (root_path / "Ideas").exists()
                    and (root_path / "Ideas").is_dir()
                    else None
                ),
                instance=resolved_instance,
                language_code=language_code,
                language_slug=language_slug_from_code(language_code) or None,
                is_localized_root=root_path.parent.name == "Localized",
            )
        )

    for raw_input in raw_inputs:
        raw_path = raw_input.path
        candidates: list[Path] = []
        if raw_path.name == "Trends":
            candidates.append(raw_path)

        direct_trends_dir = raw_path / "Trends"
        if direct_trends_dir.exists() and direct_trends_dir.is_dir():
            candidates.append(direct_trends_dir)

        if include_localized_children:
            localized_root = raw_path / "Localized"
            if localized_root.exists() and localized_root.is_dir():
                for child in sorted(path for path in localized_root.iterdir() if path.is_dir()):
                    child_trends_dir = child / "Trends"
                    if child_trends_dir.exists() and child_trends_dir.is_dir():
                        candidates.append(child_trends_dir)
                    else:
                        candidates.append(child)
                    child_streams_root = child / "Streams"
                    if child_streams_root.exists() and child_streams_root.is_dir():
                        candidates.extend(
                            path
                            for path in sorted(child_streams_root.glob("*/Trends"))
                            if path.is_dir()
                        )

        streams_root = (
            raw_path if raw_path.name == "Streams" else raw_path / "Streams"
        )
        if streams_root.exists() and streams_root.is_dir():
            for stream_root in sorted(path for path in streams_root.iterdir() if path.is_dir()):
                stream_trends_dir = stream_root / "Trends"
                if stream_trends_dir.exists() and stream_trends_dir.is_dir():
                    candidates.append(stream_trends_dir)
                if not include_localized_children:
                    continue
                stream_localized_root = stream_root / "Localized"
                if not stream_localized_root.exists() or not stream_localized_root.is_dir():
                    continue
                for child in sorted(path for path in stream_localized_root.iterdir() if path.is_dir()):
                    child_trends_dir = child / "Trends"
                    if child_trends_dir.exists() and child_trends_dir.is_dir():
                        candidates.append(child_trends_dir)
                    else:
                        candidates.append(child)

        if not candidates:
            candidates.append(raw_path)

        for candidate in candidates:
            candidate_instance = (
                None
                if _infer_grouped_child_instance_within_parent(
                    path=candidate,
                    parent_root=raw_path,
                )
                is not None
                else raw_input.instance
            )
            add_candidate(candidate, instance=candidate_instance)

    _validate_unique_site_instance_slugs(
        [input_dir.instance for input_dir in discovered],
        context="Trend site input instances",
    )
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
    return (
        "".join(pills)
        if pills
        else "<span class='meta-pill subdued'>No tracked topics</span>"
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
    trends_href = _site_href(
        from_page=page_path, to_page=output_dir / "trends" / "index.html"
    )
    archive_href = _site_href(from_page=page_path, to_page=output_dir / "archive.html")
    ideas_href = _site_href(from_page=page_path, to_page=output_dir / "ideas" / "index.html")
    topics_href = _site_href(
        from_page=page_path, to_page=output_dir / "topics" / "index.html"
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
        f"{nav_link('Trends', trends_href, 'trends')}"
        f"{nav_link('Ideas', ideas_href, 'ideas')}"
        f"{nav_link('Topics', topics_href, 'topics')}"
        f"{nav_link('Archive', archive_href, 'archive')}"
        "</nav>"
        "<div class='nav-actions'>"
        "<div class='nav-utility-cluster'></div>"
        f"<a class='nav-link nav-link-external nav-link-repo' href='{html.escape(RECOLETA_REPO_URL, quote=True)}'>GitHub</a>"
        "</div>"
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
) -> str:
    trend_href = _site_href(from_page=from_page, to_page=document.page_path)
    pdf_href = (
        _site_href(from_page=from_page, to_page=document.pdf_asset_path)
        if document.pdf_asset_path is not None
        else None
    )
    markdown_href = _site_href(
        from_page=from_page, to_page=document.markdown_asset_path
    )
    topic_links = _render_topic_link_pills(
        topics=document.topics[:4],
        from_page=from_page,
        topic_pages=topic_pages,
    )
    meta_pills = [
        f"<span class='meta-pill'>{html.escape(document.granularity.title())}</span>"
    ]
    if instance_pill := _render_instance_meta_pill(document.instance):
        meta_pills.append(instance_pill)
    actions = [
        f"<a class='action-link' href='{trend_href}'>Open brief</a>",
        f"<a class='action-link secondary' href='{markdown_href}'>Markdown</a>",
    ]
    if pdf_href is not None:
        actions.insert(1, f"<a class='action-link secondary' href='{pdf_href}'>PDF</a>")
    insight_html = ""
    if document.evolution_insight:
        insight_html = (
            "<div class='trend-insight-row'>"
            "<span class='trend-insight-badge'>Evolution</span>"
            f"<span class='trend-insight-copy'>{html.escape(document.evolution_insight)}</span>"
            "</div>"
        )
    return (
        "<article class='trend-card'>"
        "<div class='card-meta-row'>"
        f"<div class='card-pill-row'>{''.join(meta_pills)}</div>"
        f"<span class='meta-date'>{html.escape(document.period_token)}</span>"
        "</div>"
        f"<h2 class='card-title'><a href='{trend_href}'>{html.escape(document.title)}</a></h2>"
        f"<p class='card-excerpt'>{html.escape(document.excerpt)}</p>"
        f"{insight_html}"
        f"<div class='topic-pill-row'>{topic_links}</div>"
        f"<div class='card-actions'>{''.join(actions)}</div>"
        "</article>"
    )


def _render_topic_card(
    *,
    topic: str,
    trend_count: int,
    idea_count: int,
    latest_token: str,
    page_path: Path,
    topic_page_path: Path,
) -> str:
    href = _site_href(from_page=page_path, to_page=topic_page_path)
    return (
        "<article class='topic-card'>"
        f"<h2 class='topic-card-title'><a href='{href}'>{html.escape(topic)}</a></h2>"
        f"<div class='topic-card-meta'>{html.escape(_format_collection_meta(trend_count=trend_count, idea_count=idea_count, latest_token=latest_token))}</div>"
        "</article>"
    )


def _latest_collection_token(
    documents: Sequence[TrendSiteDocument | IdeaSiteDocument],
) -> str:
    if not documents:
        return "n/a"
    latest_document = max(documents, key=_rendered_document_sort_key)
    return latest_document.period_token or "n/a"


def _collection_window_span(
    documents: Sequence[TrendSiteDocument | IdeaSiteDocument],
) -> str:
    if not documents:
        return ""
    ordered_documents = sorted(
        documents,
        key=_rendered_document_sort_key,
        reverse=True,
    )
    newest = ordered_documents[0].period_token or "n/a"
    oldest = ordered_documents[-1].period_token or "n/a"
    return f"{oldest} to {newest}"


def _render_collection_section(
    *,
    title: str,
    count_text: str,
    cards_html: str,
    empty_copy: str,
    action_label: str | None = None,
    action_href: str | None = None,
) -> str:
    action_html = ""
    if action_label is not None and action_href is not None:
        action_html = (
            f"<a class='action-link secondary' href='{action_href}'>"
            f"{html.escape(action_label)}"
            "</a>"
        )
    empty_html = f"<div class='empty-card'>{html.escape(empty_copy)}</div>"
    return (
        "<div class='home-section collection-section'>"
        "<div class='section-heading-row'>"
        f"<h2 class='section-title'>{html.escape(title)}</h2>"
        "<div class='section-heading-actions'>"
        f"<span class='meta-date'>{html.escape(count_text)}</span>"
        f"{action_html}"
        "</div>"
        "</div>"
        f"<div class='trend-grid'>{cards_html or empty_html}</div>"
        "</div>"
    )


def _render_collection_summary_section(
    *,
    summary_label: str,
    title: str,
    trend_count: int,
    idea_count: int,
    latest_token: str,
) -> str:
    return (
        "<section class='home-section collection-summary-section'>"
        "<div class='section-heading-row'>"
        "<div class='summary-heading'>"
        f"<div class='section-kicker'>{html.escape(summary_label)}</div>"
        f"<h1 class='section-title'>{html.escape(title)}</h1>"
        "</div>"
        f"<span class='meta-date'>{html.escape(_format_collection_mix(trend_count=trend_count, idea_count=idea_count))}</span>"
        "</div>"
        "<div class='summary-stats'>"
        f"<div class='meta-panel'><div class='meta-panel-label'>Trend briefs</div><div class='meta-panel-value'>{trend_count}</div></div>"
        f"<div class='meta-panel'><div class='meta-panel-label'>Idea briefs</div><div class='meta-panel-value'>{idea_count}</div></div>"
        f"<div class='meta-panel'><div class='meta-panel-label'>Latest</div><div class='meta-panel-value'>{html.escape(latest_token)}</div></div>"
        "</div>"
        "</section>"
    )


def _trend_site_meta_rows(document: TrendSiteDocument) -> list[tuple[str, str]]:
    topic_count = len([topic for topic in document.topics if str(topic).strip()])
    rows = [
        ("Window", document.period_token),
        ("Granularity", document.granularity.title()),
        ("Topics", str(topic_count) if topic_count > 0 else "None"),
        (
            "Coverage",
            _site_date_range_label(
                period_start=document.period_start,
                period_end=document.period_end,
                fallback=document.period_token,
            ),
        ),
    ]
    if display_instance := _display_site_instance(document.instance):
        rows.insert(2, ("Instance", display_instance))
    return rows


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
            f"<span>{html.escape(document.granularity.title())} · {html.escape(document.period_token)}</span>"
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
    previous_document: TrendSiteDocument | None,
    next_document: TrendSiteDocument | None,
) -> str:
    breadcrumb_home = _site_href(
        from_page=document.page_path, to_page=output_dir / "index.html"
    )
    breadcrumb_trends = _site_href(
        from_page=document.page_path, to_page=output_dir / "trends" / "index.html"
    )
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
    meta_items = "".join(
        "<div class='meta-panel'>"
        f"<div class='meta-panel-label'>{html.escape(label)}</div>"
        f"<div class='meta-panel-value'>{html.escape(value)}</div>"
        "</div>"
        for label, value in _trend_site_meta_rows(document)
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
        next_href = _site_href(
            from_page=document.page_path, to_page=next_document.page_path
        )
        pager_items.append(
            "<a class='pager-card' href='{}'><span>Older</span><strong>{}</strong></a>".format(
                next_href, html.escape(next_document.title)
            )
        )

    action_links = [
        f"<a class='action-link' href='{markdown_href}'>Source markdown</a>",
    ]
    if pdf_href is not None:
        action_links.insert(
            0, f"<a class='action-link' href='{pdf_href}'>Download PDF</a>"
        )

    hero_dek = document.excerpt or _trend_pdf_hero_dek(document.frontmatter)
    insight_html = ""
    if document.evolution_insight:
        insight_html = (
            "<div class='detail-insight-row'>"
            "<span class='detail-insight-badge'>Evolution</span>"
            f"<span class='detail-insight-copy'>{html.escape(document.evolution_insight)}</span>"
            "</div>"
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
        f"<a href='{breadcrumb_trends}'>Trends</a>"
        "<span>/</span>"
        f"<span>{html.escape(document.period_token)}</span>"
        "</nav>"
        "<section class='detail-hero'>"
        "<div class='detail-hero-main'>"
        f"<div class='hero-kicker'>Trend brief · {html.escape(document.period_token)}</div>"
        f"<h1 class='detail-title'>{html.escape(document.title)}</h1>"
        f"<p class='detail-dek'>{html.escape(hero_dek)}</p>"
        f"<div class='detail-summary'>{html.escape(_trend_pdf_topics_summary(document.frontmatter))}</div>"
        f"{insight_html}"
        f"<div class='topic-pill-row'>{topic_links}</div>"
        f"<div class='card-actions detail-actions'>{''.join(action_links)}</div>"
        "</div>"
        "<aside class='detail-hero-side'>"
        f"{meta_items}"
        "</aside>"
        "</section>"
        f"<section class='detail-content'>{document.body_html}</section>"
        f"{_render_repo_cta_card()}"
        f"{pager_html}"
    )

    return _site_page_shell(
        title=f"{document.title} · Recoleta Trends",
        page_path=document.page_path,
        output_dir=output_dir,
        page_heading=document.title,
        page_subtitle="",
        body_class="page-detail",
        active_nav="trends",
        content_html=content_html,
    )


def _render_item_page(
    *,
    document: ItemSiteDocument,
    output_dir: Path,
    topic_pages: dict[str, Path],
) -> str:
    breadcrumb_home = _site_href(
        from_page=document.page_path, to_page=output_dir / "index.html"
    )
    markdown_href = _site_href(
        from_page=document.page_path,
        to_page=document.markdown_asset_path,
    )
    topic_links = _render_topic_link_pills(
        topics=document.topics,
        from_page=document.page_path,
        topic_pages=topic_pages,
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
    if display_instance := _display_site_instance(document.instance):
        meta_rows.insert(2, ("Instance", display_instance))
    meta_items = "".join(
        "<div class='meta-panel'>"
        f"<div class='meta-panel-label'>{html.escape(label)}</div>"
        f"<div class='meta-panel-value'>{html.escape(value)}</div>"
        "</div>"
        for label, value in meta_rows
    )
    action_links = [
        f"<a class='action-link' href='{markdown_href}'>Source markdown</a>"
    ]
    if document.canonical_url:
        action_links.insert(
            0,
            "<a class='action-link action-link-external' href='{}'>{}</a>".format(
                html.escape(document.canonical_url, quote=True),
                html.escape(
                    _item_action_label(
                        source=document.source,
                        canonical_url=document.canonical_url,
                    )
                ),
            ),
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
        f"<div class='topic-pill-row'>{topic_links}</div>"
        f"<div class='card-actions detail-actions'>{''.join(action_links)}</div>"
        "</div>"
        "<aside class='detail-hero-side'>"
        f"{meta_items}"
        "</aside>"
        "</section>"
        f"<section class='detail-content'>{document.body_html}</section>"
        f"{_render_repo_cta_card()}"
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


def _render_idea_card(
    *,
    document: IdeaSiteDocument,
    from_page: Path,
    topic_pages: dict[str, Path],
) -> str:
    idea_href = _site_href(from_page=from_page, to_page=document.page_path)
    markdown_href = _site_href(
        from_page=from_page, to_page=document.markdown_asset_path
    )
    topic_links = (
        _render_topic_link_pills(
            topics=document.topics[:4],
            from_page=from_page,
            topic_pages=topic_pages,
        )
        if document.topics
        else ""
    )
    topic_links_html = (
        f"<div class='topic-pill-row'>{topic_links}</div>" if topic_links else ""
    )
    meta_pills = [
        f"<span class='meta-pill'>{html.escape(document.granularity.title())}</span>"
    ]
    if instance_pill := _render_instance_meta_pill(document.instance):
        meta_pills.append(instance_pill)
    if document.status and document.status != "succeeded":
        meta_pills.append(
            f"<span class='meta-pill subdued'>{html.escape(document.status.title())}</span>"
        )
    insight_parts: list[str] = []
    if document.opportunity_count:
        insight_parts.append(
            f"{document.opportunity_count} opportunit{'ies' if document.opportunity_count != 1 else 'y'}"
        )
    if document.evidence_count:
        insight_parts.append(
            f"{document.evidence_count} evidence link{'s' if document.evidence_count != 1 else ''}"
        )
    insight_html = (
        "<div class='trend-insight-row'>"
        "<span class='trend-insight-badge'>Opportunities</span>"
        f"<span class='trend-insight-copy'>{html.escape(' · '.join(insight_parts))}</span>"
        "</div>"
        if insight_parts
        else ""
    )
    return (
        "<article class='trend-card'>"
        "<div class='card-meta-row'>"
        f"<div class='card-pill-row'>{''.join(meta_pills)}</div>"
        f"<span class='meta-date'>{html.escape(document.period_token)}</span>"
        "</div>"
        f"<h2 class='card-title'><a href='{idea_href}'>{html.escape(document.title)}</a></h2>"
        f"<p class='card-excerpt'>{html.escape(document.excerpt)}</p>"
        f"{insight_html}"
        f"{topic_links_html}"
        "<div class='card-actions'>"
        f"<a class='action-link' href='{idea_href}'>Open brief</a>"
        f"<a class='action-link secondary' href='{markdown_href}'>Markdown</a>"
        "</div>"
        "</article>"
    )


def _render_idea_page(
    *,
    document: IdeaSiteDocument,
    output_dir: Path,
    topic_pages: dict[str, Path],
) -> str:
    breadcrumb_home = _site_href(
        from_page=document.page_path, to_page=output_dir / "index.html"
    )
    breadcrumb_ideas = _site_href(
        from_page=document.page_path, to_page=output_dir / "ideas" / "index.html"
    )
    markdown_href = _site_href(
        from_page=document.page_path,
        to_page=document.markdown_asset_path,
    )
    topic_links = (
        _render_topic_link_pills(
            topics=document.topics,
            from_page=document.page_path,
            topic_pages=topic_pages,
        )
        if document.topics
        else ""
    )
    topic_links_html = (
        f"<div class='topic-pill-row'>{topic_links}</div>" if topic_links else ""
    )
    meta_rows = [
        ("Window", document.period_token),
        ("Granularity", document.granularity.title()),
        ("Opportunities", str(document.opportunity_count or 0)),
        ("Evidence", str(document.evidence_count or 0)),
        ("Status", (document.status or "Unknown").title()),
    ]
    if display_instance := _display_site_instance(document.instance):
        meta_rows.insert(2, ("Instance", display_instance))
    meta_items = "".join(
        "<div class='meta-panel'>"
        f"<div class='meta-panel-label'>{html.escape(label)}</div>"
        f"<div class='meta-panel-value'>{html.escape(value)}</div>"
        "</div>"
        for label, value in meta_rows
    )
    content_html = (
        "<nav class='breadcrumbs'>"
        f"<a href='{breadcrumb_home}'>Home</a>"
        "<span>/</span>"
        f"<a href='{breadcrumb_ideas}'>Ideas</a>"
        "<span>/</span>"
        f"<span>{html.escape(document.period_token)}</span>"
        "</nav>"
        "<section class='detail-hero'>"
        "<div class='detail-hero-main'>"
        f"<div class='hero-kicker'>Idea brief · {html.escape(document.period_token)}</div>"
        f"<h1 class='detail-title'>{html.escape(document.title)}</h1>"
        f"<p class='detail-dek'>{html.escape(document.excerpt or 'Evidence-grounded opportunity brief derived from a trend window.')}</p>"
        f"{topic_links_html}"
        "<div class='card-actions detail-actions'>"
        f"<a class='action-link' href='{markdown_href}'>Source markdown</a>"
        "</div>"
        "</div>"
        "<aside class='detail-hero-side'>"
        f"{meta_items}"
        "</aside>"
        "</section>"
        f"<section class='detail-content'>{document.body_html}</section>"
        f"{_render_repo_cta_card()}"
    )
    return _site_page_shell(
        title=f"{document.title} · Recoleta Ideas",
        page_path=document.page_path,
        output_dir=output_dir,
        page_heading=document.title,
        page_subtitle="",
        body_class="page-idea",
        active_nav="ideas",
        content_html=content_html,
    )


def _render_trends_index_page(
    *,
    documents: list[TrendSiteDocument],
    output_dir: Path,
    topic_pages: dict[str, Path],
) -> str:
    page_path = output_dir / "trends" / "index.html"
    cards = "".join(
        _render_trend_card(
            document=document,
            from_page=page_path,
            topic_pages=topic_pages,
        )
        for document in documents
    )
    content_html = (
        "<section class='home-section'>"
        "<div class='section-heading-row'>"
        "<h1 class='section-title page-section-title'>Trends</h1>"
        f"<span class='meta-date'>{html.escape(_count_label(len(documents), singular='trend'))}</span>"
        "</div>"
        f"<div class='trend-grid'>{cards or '<div class=\"empty-card\">No trend briefs available yet.</div>'}</div>"
        "</section>"
    )
    return _site_page_shell(
        title="Trends · Recoleta Trends",
        page_path=page_path,
        output_dir=output_dir,
        page_heading="Trends",
        page_subtitle="",
        body_class="page-trends",
        active_nav="trends",
        content_html=content_html,
    )


def _render_ideas_index_page(
    *,
    documents: list[IdeaSiteDocument],
    output_dir: Path,
    topic_pages: dict[str, Path],
) -> str:
    page_path = output_dir / "ideas" / "index.html"
    cards = "".join(
        _render_idea_card(
            document=document,
            from_page=page_path,
            topic_pages=topic_pages,
        )
        for document in documents
    )
    content_html = (
        "<section class='home-section'>"
        "<div class='section-heading-row'>"
        "<h1 class='section-title page-section-title'>Ideas</h1>"
        f"<span class='meta-date'>{html.escape(_count_label(len(documents), singular='idea'))}</span>"
        "</div>"
        f"<div class='trend-grid'>{cards or '<div class=\"empty-card\">No idea briefs available yet.</div>'}</div>"
        "</section>"
    )
    return _site_page_shell(
        title="Ideas · Recoleta Trends",
        page_path=page_path,
        output_dir=output_dir,
        page_heading="Ideas",
        page_subtitle="",
        body_class="page-ideas",
        active_nav="ideas",
        content_html=content_html,
    )


def _render_home_page(
    *,
    documents: list[TrendSiteDocument],
    idea_documents: list[IdeaSiteDocument],
    output_dir: Path,
    topic_pages: dict[str, Path],
) -> str:
    page_path = output_dir / "index.html"
    latest_cards = "".join(
        _render_trend_card(
            document=document,
            from_page=page_path,
            topic_pages=topic_pages,
        )
        for document in documents[:4]
    )
    latest_idea_cards = "".join(
        _render_idea_card(
            document=document,
            from_page=page_path,
            topic_pages=topic_pages,
        )
        for document in idea_documents[:4]
    )

    topic_counter: Counter[str] = Counter()
    topic_trend_counter: Counter[str] = Counter()
    topic_idea_counter: Counter[str] = Counter()
    latest_by_topic: dict[str, TrendSiteDocument | IdeaSiteDocument] = {}
    label_by_slug: dict[str, str] = {}
    for document in documents:
        for topic in document.topics:
            cleaned = str(topic).strip()
            if not cleaned:
                continue
            slug = _topic_slug(cleaned)
            topic_counter[slug] += 1
            topic_trend_counter[slug] += 1
            label_by_slug.setdefault(slug, cleaned)
            _record_latest_document(
                latest_by_slug=latest_by_topic,
                slug=slug,
                document=document,
            )
    for document in idea_documents:
        for topic in document.topics:
            cleaned = str(topic).strip()
            if not cleaned:
                continue
            slug = _topic_slug(cleaned)
            topic_counter[slug] += 1
            topic_idea_counter[slug] += 1
            label_by_slug.setdefault(slug, cleaned)
            _record_latest_document(
                latest_by_slug=latest_by_topic,
                slug=slug,
                document=document,
            )

    topic_cards = "".join(
        _render_topic_card(
            topic=label_by_slug[slug],
            trend_count=topic_trend_counter[slug],
            idea_count=topic_idea_counter[slug],
            latest_token=latest_by_topic[slug].period_token,
            page_path=page_path,
            topic_page_path=topic_pages[slug],
        )
        for slug, _count in topic_counter.most_common(12)
        if slug in topic_pages
    )

    archive_preview = "".join(
        "<li class='timeline-item'>"
        f"<a href='{_site_href(from_page=page_path, to_page=document.page_path)}'>{html.escape(document.title)}</a>"
        f"<span>{html.escape(document.period_token)}</span>"
        "</li>"
        for document in documents[:8]
    )

    generated_span = _collection_window_span([*documents, *idea_documents])

    content_html = (
        "<section class='home-hero-card'>"
        "<div class='home-hero-copy'>"
        "<div class='hero-kicker'>Local-first AI research radar</div>"
        "<h1 class='home-title'>Trend briefs, idea briefs, and a public research site</h1>"
        "<p class='home-dek'>"
        "Turn arXiv, Hacker News, OpenReview, Hugging Face Daily Papers, and RSS "
        "into publishable research briefs that stay local first."
        "</p>"
        "<div class='hero-actions'>"
        f"<a class='action-link' href='{_site_href(from_page=page_path, to_page=output_dir / 'trends' / 'index.html')}'>Browse trends</a>"
        f"<a class='action-link secondary' href='{_site_href(from_page=page_path, to_page=output_dir / 'ideas' / 'index.html')}'>Browse ideas</a>"
        f"<a class='action-link secondary action-link-external' href='{html.escape(RECOLETA_QUICKSTART_URL, quote=True)}'>5-minute quickstart</a>"
        "</div>"
        "</div>"
        "<div class='hero-stats'>"
        f"<div class='meta-panel'><div class='meta-panel-label'>Trends</div><div class='meta-panel-value'>{len(documents)}</div></div>"
        f"<div class='meta-panel'><div class='meta-panel-label'>Ideas</div><div class='meta-panel-value'>{len(idea_documents)}</div></div>"
        f"<div class='meta-panel'><div class='meta-panel-label'>Topics</div><div class='meta-panel-value'>{len(topic_pages)}</div></div>"
        f"<div class='meta-panel'><div class='meta-panel-label'>Window</div><div class='meta-panel-value'>{html.escape(generated_span or 'n/a')}</div></div>"
        "</div>"
        "</section>"
        "<section class='split-layout paired-collection-layout'>"
        f"{_render_collection_section(title='Trend briefs', count_text=_count_label(len(documents), singular='trend'), cards_html=latest_cards, empty_copy='No trend briefs available yet.', action_label='Browse trends', action_href=_site_href(from_page=page_path, to_page=output_dir / 'trends' / 'index.html'))}"
        f"{_render_collection_section(title='Idea briefs', count_text=_count_label(len(idea_documents), singular='idea'), cards_html=latest_idea_cards, empty_copy='No idea briefs available yet.', action_label='Browse ideas', action_href=_site_href(from_page=page_path, to_page=output_dir / 'ideas' / 'index.html'))}"
        "</section>"
        "<section class='home-section split-layout'>"
        "<div>"
        "<h2 class='section-title'>Topic radar</h2>"
        f"<div class='topic-card-grid'>{topic_cards or '<div class="empty-card">No topics available yet.</div>'}</div>"
        "</div>"
        "<div>"
        "<h2 class='section-title'>Archive preview</h2>"
        f"<ul class='timeline-list'>{archive_preview or '<li class="timeline-item empty">No archive entries yet.</li>'}</ul>"
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
    idea_documents: list[IdeaSiteDocument],
    output_dir: Path,
    topic_pages: dict[str, Path],
) -> str:
    page_path = output_dir / "topics" / "index.html"
    topic_counter: Counter[str] = Counter()
    trend_counter: Counter[str] = Counter()
    idea_counter: Counter[str] = Counter()
    latest_by_topic: dict[str, TrendSiteDocument | IdeaSiteDocument] = {}
    label_by_slug: dict[str, str] = {}

    for document in documents:
        for topic in document.topics:
            cleaned = str(topic).strip()
            if not cleaned:
                continue
            slug = _topic_slug(cleaned)
            topic_counter[slug] += 1
            trend_counter[slug] += 1
            label_by_slug.setdefault(slug, cleaned)
            _record_latest_document(
                latest_by_slug=latest_by_topic,
                slug=slug,
                document=document,
            )
    for document in idea_documents:
        for topic in document.topics:
            cleaned = str(topic).strip()
            if not cleaned:
                continue
            slug = _topic_slug(cleaned)
            topic_counter[slug] += 1
            idea_counter[slug] += 1
            label_by_slug.setdefault(slug, cleaned)
            _record_latest_document(
                latest_by_slug=latest_by_topic,
                slug=slug,
                document=document,
            )

    cards = "".join(
        _render_topic_card(
            topic=label_by_slug[slug],
            trend_count=trend_counter[slug],
            idea_count=idea_counter[slug],
            latest_token=latest_by_topic[slug].period_token,
            page_path=page_path,
            topic_page_path=topic_pages[slug],
        )
        for slug, _count in topic_counter.most_common()
        if slug in topic_pages
    )

    content_html = (
        "<section class='home-section'>"
        "<div class='section-heading-row'>"
        "<h1 class='section-title page-section-title'>All tracked topics</h1>"
        f"<span class='meta-date'>{html.escape(_count_label(len(topic_pages), singular='topic'))}</span>"
        "</div>"
        f"<div class='topic-card-grid'>{cards or '<div class="empty-card">No topics available yet.</div>'}</div>"
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

def _render_topic_page(
    *,
    topic: str,
    topic_slug: str,
    documents: list[TrendSiteDocument],
    idea_documents: list[IdeaSiteDocument],
    output_dir: Path,
    topic_pages: dict[str, Path],
) -> str:
    page_path = topic_pages[topic_slug]
    cards = "".join(
        _render_trend_card(
            document=document,
            from_page=page_path,
            topic_pages=topic_pages,
        )
        for document in documents
    )
    idea_cards = "".join(
        _render_idea_card(
            document=document,
            from_page=page_path,
            topic_pages=topic_pages,
        )
        for document in idea_documents
    )
    latest_token = _latest_collection_token([*documents, *idea_documents])
    content_html = (
        f"{_render_collection_summary_section(summary_label='Topic summary', title=topic, trend_count=len(documents), idea_count=len(idea_documents), latest_token=latest_token)}"
        "<section class='split-layout paired-collection-layout'>"
        f"{_render_collection_section(title='Trend briefs', count_text=_count_label(len(documents), singular='trend'), cards_html=cards, empty_copy='No trend briefs available yet.')}"
        f"{_render_collection_section(title='Idea briefs', count_text=_count_label(len(idea_documents), singular='idea'), cards_html=idea_cards, empty_copy='No idea briefs available yet.')}"
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

def _render_archive_page(
    *, documents: list[TrendSiteDocument], output_dir: Path
) -> str:
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
.nav-actions {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 14px;
}
.nav-utility-cluster {
  display: flex;
  align-items: center;
  min-width: 0;
}
.nav-utility-cluster:empty {
  display: none;
}
.nav-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 14px;
  border-radius: 999px;
  color: #2f4b69;
  font-size: 13px;
  font-weight: 600;
}
.nav-link.nav-link-external {
  background: rgba(29, 103, 194, 0.10);
  color: #1b579d;
}
.nav-link.nav-link-external::after,
.action-link.action-link-external::after {
  content: "\\2197";
  display: inline-block;
  margin-left: 0.45em;
  font-size: 0.82em;
  line-height: 1;
}
.nav-link.nav-link-repo {
  position: relative;
  padding: 8px 0;
  border-radius: 0;
  background: transparent;
  color: #4a657f;
  white-space: nowrap;
}
.nav-link.nav-link-repo.nav-link-external {
  background: transparent;
}
.nav-link.nav-link-repo:hover {
  color: #1b579d;
}
.nav-actions[data-has-language-switcher='true'] .nav-link.nav-link-repo {
  padding-left: 16px;
}
.nav-actions[data-has-language-switcher='true'] .nav-link.nav-link-repo::before {
  content: "";
  position: absolute;
  left: 0;
  top: 50%;
  width: 1px;
  height: 22px;
  transform: translateY(-50%);
  background: rgba(17, 41, 71, 0.12);
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
.repo-cta-card,
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
.repo-cta-card,
.archive-block {
  padding: 20px;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
}
.repo-cta-card {
  display: grid;
  gap: 12px;
}
.repo-cta-card .section-title {
  margin-bottom: 0;
}
.repo-cta-copy {
  margin: 0;
  max-width: 72ch;
  color: #4f647a;
  line-height: 1.65;
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
.section-heading-actions {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: flex-end;
  gap: 10px;
}
.summary-heading {
  display: grid;
  gap: 4px;
  min-width: 0;
}
.section-kicker {
  color: #6a8098;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
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
.summary-heading .section-title {
  margin-bottom: 0;
}
.paired-collection-layout {
  grid-template-columns: repeat(2, minmax(0, 1fr));
  align-items: start;
}
.collection-summary-section {
  display: grid;
  gap: 16px;
}
.summary-stats {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
}
.collection-section {
  display: grid;
  gap: 14px;
}
.collection-section .trend-grid {
  grid-template-columns: 1fr;
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
.action-link:hover,
.trend-card a:hover,
.topic-card a:hover {
  opacity: 0.85;
}
.nav-brand:focus-visible,
.nav-link:focus-visible,
.action-link:focus-visible,
.topic-pill-link:focus-visible,
.pager-card:focus-visible,
.breadcrumbs a:focus-visible,
.language-switcher-link:focus-visible {
  opacity: 1;
  outline: 2px solid rgba(29, 103, 194, 0.36);
  outline-offset: 3px;
  box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.92);
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
.trend-insight-row,
.detail-insight-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
}
.trend-insight-row {
  margin-bottom: 14px;
  padding: 10px 12px;
  border: 1px solid rgba(29, 103, 194, 0.12);
  border-radius: 16px;
  background: linear-gradient(180deg, rgba(239, 245, 252, 0.92), rgba(247, 250, 254, 0.96));
}
.trend-insight-badge,
.detail-insight-badge {
  display: inline-flex;
  align-items: center;
  min-height: 28px;
  padding: 0 10px;
  border-radius: 999px;
  background: #1d67c2;
  color: #f7fbff;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}
.trend-insight-copy,
.detail-insight-copy {
  color: #33506f;
  font-size: 13px;
  font-weight: 600;
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
.detail-insight-row {
  margin-bottom: 8px;
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
.detail-content .idea-section-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 14px;
  flex-wrap: wrap;
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
.detail-content .idea-opportunities-section {
  background:
    radial-gradient(circle at top right, rgba(29, 103, 194, 0.08), transparent 30%),
    linear-gradient(180deg, rgba(243, 248, 254, 0.96), rgba(250, 252, 255, 0.98));
}
.detail-content .idea-section-intro {
  margin-bottom: 14px;
}
.detail-content .idea-opportunity-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}
.detail-content .idea-opportunity-card {
  display: grid;
  gap: 14px;
  padding: 18px;
  border: 1px solid rgba(24, 52, 83, 0.10);
  border-radius: 18px;
  background:
    linear-gradient(180deg, rgba(252, 254, 255, 0.98), rgba(247, 250, 254, 0.96));
}
.detail-content .idea-opportunity-head,
.detail-content .idea-opportunity-body {
  display: grid;
  gap: 12px;
}
.detail-content .idea-opportunity-title {
  margin: 0;
  color: #183453;
  font-family: "Songti SC", "STSong", Georgia, serif;
  font-size: 24px;
  line-height: 1.08;
}
.detail-content .idea-opportunity-meta-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.detail-content .idea-meta-pill {
  background: rgba(255, 255, 255, 0.88);
  border-color: rgba(24, 52, 83, 0.10);
  color: #34506f;
}
.detail-content .idea-meta-pill-label {
  color: #70849a;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}
.detail-content .idea-meta-pill-separator {
  margin: 0 6px;
  color: #9aabc0;
}
.detail-content .idea-opportunity-block {
  display: grid;
  gap: 6px;
}
.detail-content .idea-opportunity-block-role {
  padding: 12px 14px;
  border: 1px solid rgba(24, 52, 83, 0.10);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.82);
}
.detail-content .idea-opportunity-label {
  color: #6a8098;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}
.detail-content .idea-opportunity-copy {
  color: #213246;
}
.detail-content .idea-opportunity-role-value {
  color: #34506f;
  font-size: 14px;
  line-height: 1.5;
  overflow-wrap: anywhere;
  word-break: break-word;
  white-space: normal;
  display: block;
}
.detail-content .idea-opportunity-copy p,
.detail-content .idea-opportunity-copy ul,
.detail-content .idea-opportunity-copy ol {
  margin: 0;
}
.detail-content .idea-opportunity-block-evidence {
  padding-top: 12px;
  border-top: 1px dashed rgba(24, 52, 83, 0.12);
}
.detail-content .idea-evidence-list ul,
.detail-content .idea-evidence-list ol {
  padding-inline-start: 1.08em;
}
.detail-content .highlight-card {
  background:
    linear-gradient(180deg, rgba(247, 250, 254, 0.95), rgba(241, 247, 253, 0.96));
}
.detail-content .evolution-section {
  background:
    radial-gradient(circle at top right, rgba(29, 103, 194, 0.10), transparent 32%),
    linear-gradient(180deg, rgba(236, 244, 253, 0.95), rgba(248, 251, 255, 0.98));
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
.detail-content .evolution-section-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}
.detail-content .evolution-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.detail-content .evolution-stat,
.detail-content .history-pill,
.detail-content .evolution-badge {
  display: inline-flex;
  align-items: center;
  min-height: 30px;
  padding: 0 11px;
  border-radius: 999px;
  border: 1px solid rgba(29, 103, 194, 0.14);
  background: rgba(29, 103, 194, 0.08);
  color: #1e5b9d;
  font-size: 12px;
  font-weight: 700;
}
.detail-content .evolution-stat.secondary,
.detail-content .history-pill {
  background: rgba(255, 255, 255, 0.88);
  color: #4d647d;
}
.detail-content .evolution-summary {
  margin-bottom: 14px;
}
.detail-content .evolution-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}
.detail-content .evolution-card {
  position: relative;
  display: grid;
  gap: 12px;
  padding: 16px;
  border: 1px solid rgba(24, 52, 83, 0.10);
  border-radius: 18px;
  background: rgba(252, 254, 255, 0.96);
  overflow: hidden;
}
.detail-content .evolution-card::before {
  content: "";
  position: absolute;
  inset: 0 auto 0 0;
  width: 4px;
  border-radius: 18px 0 0 18px;
  background: #7d94ae;
}
.detail-content .evolution-change-continuing::before {
  background: #2c6bc5;
}
.detail-content .evolution-change-emerging::before {
  background: #1d8b6f;
}
.detail-content .evolution-change-fading::before {
  background: #b66a35;
}
.detail-content .evolution-change-shifting::before {
  background: #7459c6;
}
.detail-content .evolution-change-polarizing::before {
  background: #c24d6b;
}
.detail-content .evolution-card-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}
.detail-content .evolution-card-title {
  margin: 0;
  color: #183453;
  font-family: "Songti SC", "STSong", Georgia, serif;
  font-size: 24px;
  line-height: 1.08;
}
.detail-content .evolution-badge {
  flex: 0 0 auto;
}
.detail-content .evolution-badge-continuing {
  background: rgba(29, 103, 194, 0.10);
  color: #1e5aa1;
}
.detail-content .evolution-badge-emerging {
  background: rgba(29, 139, 111, 0.10);
  color: #176d58;
  border-color: rgba(29, 139, 111, 0.16);
}
.detail-content .evolution-badge-fading {
  background: rgba(182, 106, 53, 0.11);
  color: #9c5a2b;
  border-color: rgba(182, 106, 53, 0.16);
}
.detail-content .evolution-badge-shifting {
  background: rgba(116, 89, 198, 0.10);
  color: #654bb0;
  border-color: rgba(116, 89, 198, 0.16);
}
.detail-content .evolution-badge-polarizing {
  background: rgba(194, 77, 107, 0.10);
  color: #a2415a;
  border-color: rgba(194, 77, 107, 0.16);
}
.detail-content .evolution-history-block {
  display: grid;
  gap: 8px;
}
.detail-content .evolution-history-label {
  color: #7589a0;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}
.detail-content .evolution-history-track {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.detail-content .evolution-copy {
  margin-top: -2px;
}
.detail-content .evolution-expand {
  margin-top: -2px;
  border-top: 1px dashed rgba(24, 52, 83, 0.12);
  padding-top: 10px;
}
.detail-content .evolution-expand-toggle {
  display: block;
  cursor: pointer;
  list-style: none;
}
.detail-content .evolution-expand-toggle::-webkit-details-marker {
  display: none;
}
.detail-content .evolution-expand-summary-copy {
  display: block;
  color: #30485f;
  font-size: 14px;
  line-height: 1.66;
}
.detail-content .evolution-expand-label {
  display: inline-flex;
  align-items: center;
  margin-top: 10px;
  color: #1f5ea9;
  font-size: 12px;
  font-weight: 700;
}
.detail-content .evolution-expand-label::before {
  display: inline-block;
  margin-right: 6px;
}
.detail-content .evolution-expand-label-more::before {
  content: "+";
}
.detail-content .evolution-expand-label-less {
  display: none;
}
.detail-content .evolution-expand-label-less::before {
  content: "−";
}
.detail-content .evolution-expand[open] .evolution-expand-summary-copy,
.detail-content .evolution-expand[open] .evolution-expand-label-more {
  display: none;
}
.detail-content .evolution-expand[open] .evolution-expand-label-less {
  display: inline-flex;
}
.detail-content .evolution-expand-body {
  margin-top: 10px;
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
  .summary-stats,
  .detail-content .summary-grid,
  .detail-content .idea-opportunity-grid,
  .detail-content .evolution-grid,
  .pager-row {
    grid-template-columns: 1fr;
  }
}
@media (max-width: 1040px) {
  .site-header {
    flex-wrap: wrap;
    align-items: center;
    column-gap: 14px;
    row-gap: 12px;
    padding: 14px 16px 16px;
    border-radius: 30px;
  }
  .nav-brand-wrap {
    flex: 1 1 auto;
  }
  .nav-brand {
    font-size: 22px;
    white-space: nowrap;
  }
  .nav-links {
    order: 3;
    flex: 1 1 100%;
    gap: 8px;
    padding-top: 10px;
    border-top: 1px solid rgba(17, 41, 71, 0.08);
  }
  .nav-links .nav-link {
    padding: 8px 12px;
    font-size: 12px;
  }
  .nav-actions {
    flex: 0 0 auto;
    margin-left: auto;
    gap: 12px;
  }
  .nav-actions[data-has-language-switcher='true'] .nav-link.nav-link-repo {
    padding-left: 12px;
  }
  .nav-actions[data-has-language-switcher='true'] .nav-link.nav-link-repo::before {
    height: 18px;
  }
}
@media (max-width: 820px) {
  .site-header {
    align-items: stretch;
    row-gap: 10px;
  }
  .nav-brand-wrap {
    width: 100%;
    flex: 1 1 100%;
  }
  .nav-actions {
    width: 100%;
    margin-left: 0;
    justify-content: space-between;
    gap: 10px;
  }
  .nav-utility-cluster {
    flex: 1 1 auto;
  }
  .nav-links {
    padding-top: 8px;
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
  .nav-actions {
    width: 100%;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
  }
  .nav-links .nav-link {
    flex: 1 1 calc(50% - 5px);
    justify-content: center;
    text-align: center;
  }
  .nav-utility-cluster {
    flex: 1 1 auto;
  }
  .nav-actions .nav-link.nav-link-repo {
    flex: 0 0 auto;
  }
  .nav-actions[data-has-language-switcher='true'] .nav-link.nav-link-repo {
    padding-left: 0;
  }
  .nav-actions[data-has-language-switcher='true'] .nav-link.nav-link-repo::before {
    display: none;
  }
  .page-hero,
  .home-hero-card,
  .home-section,
  .detail-hero,
  .detail-content,
  .repo-cta-card,
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
  .section-heading-actions {
    width: 100%;
    justify-content: flex-start;
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
  .trend-insight-row,
  .detail-insight-row,
  .detail-content .evolution-card-head {
    align-items: flex-start;
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
            if _parse_site_bool(frontmatter.get("site_exclude")):
                continue

            period_start = _parse_site_datetime(frontmatter.get("period_start"))
            period_end = _parse_site_datetime(frontmatter.get("period_end"))
            granularity = (
                str(frontmatter.get("granularity") or "trend").strip().lower()
                or "trend"
            )
            topics = _parse_site_string_list(frontmatter.get("topics"))

            instance = _resolve_site_instance(
                input_instance=input_info.instance,
                frontmatter=frontmatter,
            )
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
                    instance=instance,
                )
            )

    source_documents.sort(key=_trend_site_sort_key, reverse=True)
    return source_documents[:limit] if limit is not None else source_documents


def _site_namespaced_page_stem(*, stem: str, instance: str | None) -> str:
    cleaned_instance = str(instance or "").strip()
    if not cleaned_instance:
        return stem
    return f"{_instance_slug(cleaned_instance)}--{stem}"


def _site_namespaced_asset_name(*, name: str, instance: str | None) -> str:
    cleaned_instance = str(instance or "").strip()
    if not cleaned_instance:
        return name
    return f"{_instance_slug(cleaned_instance)}--{name}"


def _site_source_key(*, markdown_path: Path, instance: str | None) -> SiteSourceKey:
    return (markdown_path.resolve(), _normalize_site_instance(instance))


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


def _resolve_site_source_key(
    *,
    target_path: Path,
    source_instance: str | None,
    available_source_keys: set[SiteSourceKey],
) -> SiteSourceKey | None:
    if source_instance is not None:
        same_instance_key = _site_source_key(
            markdown_path=target_path,
            instance=source_instance,
        )
        if same_instance_key in available_source_keys:
            return same_instance_key
    default_instance_key = _site_source_key(markdown_path=target_path, instance=None)
    if default_instance_key in available_source_keys:
        return default_instance_key
    matching_keys = [
        source_key for source_key in available_source_keys if source_key[0] == target_path
    ]
    if len(matching_keys) == 1:
        return matching_keys[0]
    return None


def _rewrite_site_markdown_links(
    *,
    html_text: str,
    source_markdown_path: Path,
    source_instance: str | None,
    from_page: Path,
    page_by_source_key: dict[SiteSourceKey, Path],
) -> str:
    soup = BeautifulSoup(html_text, "html.parser")
    rewritten = False
    available_source_keys = set(page_by_source_key)
    for anchor in soup.find_all("a", href=True):
        target_path = _resolve_site_local_markdown_target(
            source_markdown_path=source_markdown_path,
            href=str(anchor.get("href") or ""),
        )
        if target_path is None:
            continue
        target_source_key = _resolve_site_source_key(
            target_path=target_path,
            source_instance=source_instance,
            available_source_keys=available_source_keys,
        )
        if target_source_key is None:
            continue
        target_page_path = page_by_source_key.get(target_source_key)
        if target_page_path is None:
            continue
        anchor["href"] = _site_href(from_page=from_page, to_page=target_page_path)
        rewritten = True
    return str(soup) if rewritten else html_text


def _load_item_source_documents(
    *,
    input_dirs: Sequence[TrendSiteInputDirectory],
    allowed_source_keys: set[SiteSourceKey] | None = None,
) -> list[ItemSiteSourceDocument]:
    source_documents: list[ItemSiteSourceDocument] = []
    seen_source_keys: set[SiteSourceKey] = set()
    for input_info in input_dirs:
        if input_info.inbox_path is None:
            continue
        for markdown_path in sorted(input_info.inbox_path.glob("*.md")):
            resolved_markdown_path = markdown_path.resolve()
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
            instance = _resolve_site_instance(
                input_instance=input_info.instance,
                frontmatter=frontmatter,
            )
            source_key = _site_source_key(
                markdown_path=resolved_markdown_path,
                instance=instance,
            )
            if source_key in seen_source_keys:
                continue
            seen_source_keys.add(source_key)
            if allowed_source_keys is not None and source_key not in allowed_source_keys:
                continue
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
                    instance=instance,
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


def _load_idea_source_documents(
    *,
    input_dirs: Sequence[TrendSiteInputDirectory],
    limit: int | None = None,
) -> list[IdeaSiteSourceDocument]:
    source_documents: list[IdeaSiteSourceDocument] = []
    for input_info in input_dirs:
        if input_info.ideas_path is None:
            continue
        markdown_paths = sorted(input_info.ideas_path.glob("*.md"))
        for markdown_path in markdown_paths:
            raw_markdown = markdown_path.read_text(encoding="utf-8")
            frontmatter, markdown_body = _split_yaml_frontmatter_text(raw_markdown)
            if str(frontmatter.get("kind") or "").strip().lower() != "ideas":
                continue
            if _parse_site_bool(frontmatter.get("site_exclude")):
                continue
            period_start = _parse_site_datetime(frontmatter.get("period_start"))
            period_end = _parse_site_datetime(frontmatter.get("period_end"))
            granularity = (
                str(frontmatter.get("granularity") or "ideas").strip().lower()
                or "ideas"
            )
            source_documents.append(
                IdeaSiteSourceDocument(
                    markdown_path=markdown_path,
                    stem=markdown_path.stem,
                    frontmatter=frontmatter,
                    markdown_body=markdown_body,
                    granularity=granularity,
                    period_start=period_start,
                    period_end=period_end,
                    topics=_parse_site_string_list(frontmatter.get("topics")),
                    instance=_resolve_site_instance(
                        input_instance=input_info.instance,
                        frontmatter=frontmatter,
                    ),
                    status=str(frontmatter.get("status") or "").strip().lower() or "unknown",
                )
            )

    source_documents.sort(key=_idea_site_sort_key, reverse=True)
    return source_documents[:limit] if limit is not None else source_documents


def _collect_referenced_item_source_keys(
    *,
    source_documents: Sequence[TrendSiteSourceDocument | IdeaSiteSourceDocument],
    available_source_keys: set[SiteSourceKey],
) -> set[SiteSourceKey]:
    if not source_documents or not available_source_keys:
        return set()
    markdown = MarkdownIt("commonmark", {"html": True, "typographer": True})
    referenced_source_keys: set[SiteSourceKey] = set()
    for source_document in source_documents:
        normalized_markdown = str(source_document.markdown_body or "").strip()
        if not normalized_markdown:
            continue
        rendered_html = markdown.render(normalized_markdown)
        soup = BeautifulSoup(rendered_html, "html.parser")
        for anchor in soup.find_all("a", href=True):
            target_path = _resolve_site_local_markdown_target(
                source_markdown_path=source_document.markdown_path,
                href=str(anchor.get("href") or ""),
            )
            if target_path is None:
                continue
            target_source_key = _resolve_site_source_key(
                target_path=target_path,
                source_instance=source_document.instance,
                available_source_keys=available_source_keys,
            )
            if target_source_key is None:
                continue
            referenced_source_keys.add(target_source_key)
    return referenced_source_keys


def _select_item_source_documents(
    *,
    input_dirs: Sequence[TrendSiteInputDirectory],
    trend_source_documents: Sequence[TrendSiteSourceDocument],
    idea_source_documents: Sequence[IdeaSiteSourceDocument],
    item_export_scope: str,
) -> ItemSiteSelection:
    all_source_documents = _load_item_source_documents(input_dirs=input_dirs)
    available_source_keys = {
        _site_source_key(
            markdown_path=source_document.markdown_path,
            instance=source_document.instance,
        )
        for source_document in all_source_documents
    }
    normalized_scope = _normalize_item_export_scope(item_export_scope)
    selected_source_keys = (
        available_source_keys
        if normalized_scope == "all"
        else _collect_referenced_item_source_keys(
            source_documents=[*trend_source_documents, *idea_source_documents],
            available_source_keys=available_source_keys,
        )
    )
    source_documents = [
        source_document
        for source_document in all_source_documents
        if _site_source_key(
            markdown_path=source_document.markdown_path,
            instance=source_document.instance,
        )
        in selected_source_keys
    ]
    return ItemSiteSelection(
        source_documents=source_documents,
        available_total=len(all_source_documents),
        unreferenced_total=(
            0
            if normalized_scope == "all"
            else max(len(all_source_documents) - len(selected_source_keys), 0)
        ),
    )


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


def _idea_heading_matches(heading: str, *labels: str) -> bool:
    normalized = str(heading or "").strip().lower()
    if not normalized:
        return False
    return any(label in normalized for label in labels)


def _idea_meta_pill(label: str, value: str) -> str:
    return (
        "<span class='meta-pill idea-meta-pill'>"
        f"<span class='idea-meta-pill-label'>{html.escape(label)}</span>"
        f"<span class='idea-meta-pill-separator'>·</span>{html.escape(value)}"
        "</span>"
    )


def _render_idea_role_block(value: str) -> str:
    safe_value = html.escape(value)
    return (
        "<section class='idea-opportunity-block idea-opportunity-block-role'>"
        "<div class='idea-opportunity-label'>Role</div>"
        f"<div class='idea-opportunity-copy idea-opportunity-role-value' title='{html.escape(value, quote=True)}'>{safe_value}</div>"
        "</section>"
    )


def _extract_idea_opportunity_meta_sections(
    node: Tag,
) -> tuple[str | None, str | None] | None:
    if node.name not in {"ul", "ol"}:
        return None
    pills: list[str] = []
    role_html: str | None = None
    items = node.find_all("li", recursive=False)
    if not items:
        return None
    for item in items:
        text = item.get_text(" ", strip=True)
        if (value := _strip_labeled_value(text, labels=("Kind",))) is not None:
            pills.append(_idea_meta_pill("Kind", value))
            continue
        if (value := _strip_labeled_value(text, labels=("Time horizon",))) is not None:
            pills.append(_idea_meta_pill("Time horizon", value))
            continue
        if (value := _strip_labeled_value(text, labels=("User/job",))) is not None:
            role_html = _render_idea_role_block(value)
            continue
        if (value := _strip_labeled_value(text, labels=("Role",))) is not None:
            role_html = _render_idea_role_block(value)
            continue
        if " ".join(text.split()).strip():
            return None
    pills_html = f"<div class='idea-opportunity-meta-row'>{''.join(pills)}</div>" if pills else None
    if pills_html is None and role_html is None:
        return None
    return pills_html, role_html


def _extract_idea_labeled_paragraph(node: Tag) -> tuple[str, str] | None:
    if node.name != "p":
        return None
    label_by_key = {
        "thesis": "Thesis",
        "why now": "Why now",
        "what changed": "What changed",
        "validation next step": "Validation next step",
    }
    paragraph = BeautifulSoup(str(node), "html.parser").find("p")
    if paragraph is None:
        return None
    strong = paragraph.find("strong", recursive=False)
    if strong is None:
        return None
    raw_label = strong.get_text(" ", strip=True).rstrip(".:：").strip().lower()
    label = label_by_key.get(raw_label)
    if label is None:
        return None
    strong.extract()
    inner_html = re.sub(
        r"^\s*([.:：]|&nbsp;)+\s*",
        "",
        paragraph.decode_contents(),
    ).strip()
    if not inner_html:
        return None
    return label, inner_html


def _render_idea_opportunity_card(*, title: str, inner_html: str) -> tuple[str, int]:
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
        if not meta_row_html:
            extracted_meta_sections = _extract_idea_opportunity_meta_sections(child)
            if extracted_meta_sections is not None:
                extracted_meta_html, role_html = extracted_meta_sections
                if extracted_meta_html is not None:
                    meta_row_html = extracted_meta_html
                if role_html is not None:
                    content_blocks.append(role_html)
                index += 1
                continue
        if child.name in {"h4", "h5"} and _idea_heading_matches(
            child.get_text(" ", strip=True), "evidence"
        ):
            evidence_nodes: list[str] = []
            look_ahead = index + 1
            while look_ahead < len(children):
                candidate = children[look_ahead]
                if isinstance(candidate, Tag) and candidate.name in {
                    "h3",
                    "h4",
                    "h5",
                }:
                    break
                if str(candidate).strip():
                    evidence_nodes.append(str(candidate))
                look_ahead += 1
            evidence_soup = BeautifulSoup("".join(evidence_nodes), "html.parser")
            evidence_count += sum(
                1
                for item in evidence_soup.find_all("li")
                if item.find_parent("li") is None
            )
            evidence_html = "".join(evidence_nodes).strip() or "<p>(none)</p>"
            content_blocks.append(
                "<section class='idea-opportunity-block idea-opportunity-block-evidence'>"
                "<div class='idea-opportunity-label'>Evidence</div>"
                f"<div class='idea-opportunity-copy prose idea-evidence-list'>{evidence_html}</div>"
                "</section>"
            )
            index = look_ahead
            continue
        labeled = _extract_idea_labeled_paragraph(child)
        if labeled is not None:
            label, value_html = labeled
            content_blocks.append(
                "<section class='idea-opportunity-block'>"
                f"<div class='idea-opportunity-label'>{html.escape(label)}</div>"
                f"<div class='idea-opportunity-copy prose'><p>{value_html}</p></div>"
                "</section>"
            )
            index += 1
            continue
        generic_nodes.append(str(child))
        index += 1

    if generic_nodes:
        content_blocks.insert(
            0,
            "<section class='idea-opportunity-block'>"
            "<div class='idea-opportunity-copy prose'>"
            f"{''.join(generic_nodes)}"
            "</div>"
            "</section>",
        )

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


def _render_idea_opportunities_section(
    *, heading: str, inner_html: str
) -> tuple[str, int, int]:
    section_soup = BeautifulSoup(inner_html, "html.parser")
    cards: list[str] = []
    intro_nodes: list[str] = []
    evidence_count = 0
    current_title: str | None = None
    current_nodes: list[str] = []
    for node in section_soup.contents:
        if not str(node).strip():
            continue
        if isinstance(node, Tag) and node.name == "h3":
            if current_title is not None:
                card_html, entry_evidence_count = _render_idea_opportunity_card(
                    title=current_title,
                    inner_html="".join(current_nodes),
                )
                cards.append(card_html)
                evidence_count += entry_evidence_count
            current_title = node.get_text(" ", strip=True) or "Opportunity"
            current_nodes = []
            continue
        if current_title is None:
            intro_nodes.append(str(node))
            continue
        current_nodes.append(str(node))

    if current_title is not None:
        card_html, entry_evidence_count = _render_idea_opportunity_card(
            title=current_title,
            inner_html="".join(current_nodes),
        )
        cards.append(card_html)
        evidence_count += entry_evidence_count

    if not cards:
        return (
            _render_browser_content_card_html(heading=heading, inner_html=inner_html),
            0,
            evidence_count,
        )

    intro_html = (
        f"<div class='prose idea-section-intro'>{''.join(intro_nodes)}</div>"
        if "".join(intro_nodes).strip()
        else ""
    )
    count_label = (
        f"{len(cards)} opportunity" if len(cards) == 1 else f"{len(cards)} opportunities"
    )
    return (
        "<section class='surface-card section-card idea-opportunities-section'>"
        "<div class='idea-section-head'>"
        f"{_render_browser_section_label_html(heading)}"
        f"<span class='meta-date'>{html.escape(count_label)}</span>"
        "</div>"
        f"{intro_html}"
        f"<div class='idea-opportunity-grid'>{''.join(cards)}</div>"
        "</section>",
        len(cards),
        evidence_count,
    )


def _build_idea_browser_body_html(*, body_html: str) -> IdeaBodyRenderResult:
    _title, sections = _extract_trend_pdf_sections(body_html=body_html)
    if not sections:
        return IdeaBodyRenderResult(
            body_html=_build_item_browser_body_html(body_html=body_html),
            opportunity_count=0,
            evidence_count=0,
        )

    rendered: list[str] = []
    summary_cards: list[str] = []
    opportunity_count = 0
    evidence_count = 0
    for section in sections:
        if _idea_heading_matches(section.heading, "summary", "overview"):
            summary_cards.append(
                _render_browser_content_card_html(
                    heading=section.heading,
                    inner_html=section.inner_html,
                    card_classes=(
                        "surface-card section-card summary-card summary-card-primary"
                    ),
                )
            )
            continue
        if _idea_heading_matches(section.heading, "opportunit"):
            (
                opportunities_html,
                section_opportunity_count,
                section_evidence_count,
            ) = _render_idea_opportunities_section(
                heading=section.heading,
                inner_html=section.inner_html,
            )
            rendered.append(opportunities_html)
            opportunity_count += section_opportunity_count
            evidence_count += section_evidence_count
            continue
        rendered.append(
            _render_browser_content_card_html(
                heading=section.heading,
                inner_html=section.inner_html,
            )
        )

    if summary_cards:
        summary_classes = (
            "summary-grid summary-grid-single" if len(summary_cards) == 1 else "summary-grid"
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


def _load_item_site_documents(
    *,
    source_documents: Sequence[ItemSiteSourceDocument],
    output_dir: Path,
) -> tuple[list[ItemSiteDocument], dict[SiteSourceKey, Path]]:
    markdown = MarkdownIt("commonmark", {"html": True, "typographer": True})
    items_dir = output_dir / "items"
    item_artifacts_dir = output_dir / "artifacts" / "items"
    items_dir.mkdir(parents=True, exist_ok=True)
    item_artifacts_dir.mkdir(parents=True, exist_ok=True)

    documents: list[ItemSiteDocument] = []
    page_by_source_key: dict[SiteSourceKey, Path] = {}
    for source_document in source_documents:
        normalized_markdown = source_document.markdown_body.strip() or "# Item\n"
        rendered_html = markdown.render(normalized_markdown)
        title, raw_body_html, excerpt = _extract_item_body_html(body_html=rendered_html)
        body_html = _build_item_browser_body_html(body_html=raw_body_html)
        page_stem = _site_namespaced_page_stem(
            stem=source_document.stem,
            instance=source_document.instance,
        )
        page_path = items_dir / f"{page_stem}.html"
        markdown_asset_path = item_artifacts_dir / _site_namespaced_asset_name(
            name=source_document.markdown_path.name,
            instance=source_document.instance,
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
                instance=source_document.instance,
                relevance_score=source_document.relevance_score,
                body_html=body_html,
                excerpt=excerpt,
                frontmatter=source_document.frontmatter,
            )
        )
        page_by_source_key[
            _site_source_key(
                markdown_path=source_document.markdown_path,
                instance=source_document.instance,
            )
        ] = page_path
    return documents, page_by_source_key


def _load_idea_site_documents(
    *,
    source_documents: Sequence[IdeaSiteSourceDocument],
    output_dir: Path,
    linked_page_by_source_key: dict[SiteSourceKey, Path],
) -> tuple[list[IdeaSiteDocument], dict[SiteSourceKey, Path]]:
    markdown = MarkdownIt("commonmark", {"html": True, "typographer": True})
    ideas_dir = output_dir / "ideas"
    idea_artifacts_dir = output_dir / "artifacts" / "ideas"
    ideas_dir.mkdir(parents=True, exist_ok=True)
    idea_artifacts_dir.mkdir(parents=True, exist_ok=True)

    page_by_source_key = {
        _site_source_key(
            markdown_path=source_document.markdown_path,
            instance=source_document.instance,
        ): (
            ideas_dir
            / f"{_site_namespaced_page_stem(stem=source_document.stem, instance=source_document.instance)}.html"
        )
        for source_document in source_documents
    }
    all_linked_pages = dict(linked_page_by_source_key)
    all_linked_pages.update(page_by_source_key)

    documents: list[IdeaSiteDocument] = []
    for source_document in source_documents:
        normalized_markdown = source_document.markdown_body.strip() or "# Ideas\n"
        rendered_html = markdown.render(normalized_markdown)
        title, raw_body_html, excerpt = _extract_item_body_html(body_html=rendered_html)
        source_key = _site_source_key(
            markdown_path=source_document.markdown_path,
            instance=source_document.instance,
        )
        page_path = page_by_source_key[source_key]
        idea_body = _build_idea_browser_body_html(body_html=raw_body_html)
        body_html = _rewrite_site_markdown_links(
            html_text=idea_body.body_html,
            source_markdown_path=source_document.markdown_path,
            source_instance=source_document.instance,
            from_page=page_path,
            page_by_source_key=all_linked_pages,
        )
        period_token = (
            _trend_date_token(
                granularity=source_document.granularity,
                period_start=source_document.period_start,
            )
            if source_document.period_start is not None
            else source_document.stem
        )
        markdown_asset_path = idea_artifacts_dir / _site_namespaced_asset_name(
            name=source_document.markdown_path.name,
            instance=source_document.instance,
        )
        shutil.copy2(source_document.markdown_path, markdown_asset_path)
        documents.append(
            IdeaSiteDocument(
                markdown_path=source_document.markdown_path,
                markdown_asset_path=markdown_asset_path,
                page_path=page_path,
                stem=source_document.stem,
                title=title,
                granularity=source_document.granularity,
                period_token=period_token,
                period_start=source_document.period_start,
                period_end=source_document.period_end,
                topics=source_document.topics,
                instance=source_document.instance,
                status=source_document.status,
                opportunity_count=idea_body.opportunity_count,
                evidence_count=idea_body.evidence_count,
                body_html=body_html,
                excerpt=excerpt,
                frontmatter=source_document.frontmatter,
            )
        )
    return documents, page_by_source_key


def _load_trend_site_documents(
    *,
    source_documents: Sequence[TrendSiteSourceDocument],
    output_dir: Path,
    item_pages_by_source_key: dict[SiteSourceKey, Path],
) -> list[TrendSiteDocument]:
    markdown = MarkdownIt("commonmark", {"html": True, "typographer": True})
    documents: list[TrendSiteDocument] = []

    artifacts_dir = output_dir / "artifacts"
    trends_dir = output_dir / "trends"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    trends_dir.mkdir(parents=True, exist_ok=True)

    trend_pages_by_source_key = {
        _site_source_key(
            markdown_path=source_document.markdown_path,
            instance=source_document.instance,
        ): (
            trends_dir
            / f"{_site_namespaced_page_stem(stem=source_document.stem, instance=source_document.instance)}.html"
        )
        for source_document in source_documents
    }
    linked_page_by_source_key = dict(item_pages_by_source_key)
    linked_page_by_source_key.update(trend_pages_by_source_key)

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
        evolution_insight = _extract_trend_evolution_insight(sections)
        source_key = _site_source_key(
            markdown_path=source_document.markdown_path,
            instance=source_document.instance,
        )
        page_path = trend_pages_by_source_key[source_key]
        browser_body_html = _rewrite_site_markdown_links(
            html_text=_build_trend_browser_body_html(
                sections=sections,
                allow_evolution_disclosure=True,
            ),
            source_markdown_path=source_document.markdown_path,
            source_instance=source_document.instance,
            from_page=page_path,
            page_by_source_key=linked_page_by_source_key,
        )

        period_token = (
            _trend_date_token(
                granularity=source_document.granularity,
                period_start=source_document.period_start,
            )
            if source_document.period_start is not None
            else source_document.stem
        )

        markdown_asset_path = artifacts_dir / _site_namespaced_asset_name(
            name=source_document.markdown_path.name,
            instance=source_document.instance,
        )
        shutil.copy2(source_document.markdown_path, markdown_asset_path)

        pdf_asset_path: Path | None = None
        if source_document.pdf_path is not None:
            pdf_asset_path = artifacts_dir / _site_namespaced_asset_name(
                name=source_document.pdf_path.name,
                instance=source_document.instance,
            )
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
                instance=source_document.instance,
                body_html=browser_body_html,
                excerpt=excerpt,
                evolution_insight=evolution_insight,
                frontmatter=source_document.frontmatter,
            )
        )

    return documents


def _markdown_language_code(path: Path) -> str | None:
    try:
        raw_markdown = path.read_text(encoding="utf-8")
    except Exception:
        return None
    frontmatter, _markdown_body = _split_yaml_frontmatter_text(raw_markdown)
    normalized = str(
        frontmatter.get("language_code") or frontmatter.get("lang") or ""
    ).strip()
    return normalized or None


def _infer_site_language_code_from_root(root_path: Path) -> str | None:
    candidate_dirs = [root_path / "Trends", root_path / "Ideas", root_path / "Inbox"]
    if root_path.name == "Trends":
        candidate_dirs.insert(0, root_path)
    for candidate_dir in candidate_dirs:
        if not candidate_dir.exists() or not candidate_dir.is_dir():
            continue
        for markdown_path in sorted(candidate_dir.glob("*.md")):
            if language_code := _markdown_language_code(markdown_path):
                return language_code
    return None


def _discover_site_language_inputs(
    raw_inputs: Sequence[TrendSiteInputSpec],
) -> list[tuple[str | None, str, tuple[TrendSiteInputSpec, ...]]]:
    discovered: list[tuple[str | None, str, tuple[TrendSiteInputSpec, ...]]] = []
    grouped_roots: dict[str, list[TrendSiteInputSpec]] = {}
    language_code_by_slug: dict[str, str] = {}
    seen_roots: set[tuple[Path, str | None]] = set()

    def add_root(root_path: Path, *, instance: str | None) -> None:
        resolved_root = root_path.expanduser().resolve()
        resolved_instance = (
            _normalize_site_instance(instance)
            if instance is not None
            else _normalize_legacy_site_stream(
                _infer_instance_name_from_site_root(resolved_root)
            )
        )
        if (
            (resolved_root, resolved_instance) in seen_roots
            or not resolved_root.exists()
            or not resolved_root.is_dir()
        ):
            return
        seen_roots.add((resolved_root, resolved_instance))
        language_code = _infer_site_language_code_from_root(resolved_root)
        language_slug = (
            language_slug_from_code(language_code)
            if language_code is not None
            else ""
        )
        input_spec = TrendSiteInputSpec(
            path=resolved_root,
            instance=resolved_instance,
        )
        if language_code is None or not language_slug:
            discovered.append((language_code, language_slug, (input_spec,)))
            return
        grouped_roots.setdefault(language_slug, []).append(input_spec)
        language_code_by_slug[language_slug] = str(language_code)

    for raw_input in raw_inputs:
        base_root = (
            raw_input.path.parent if raw_input.path.name == "Trends" else raw_input.path
        ).expanduser().resolve()
        add_root(base_root, instance=raw_input.instance)
        localized_root = base_root / "Localized"
        if localized_root.exists() and localized_root.is_dir():
            for child in sorted(path for path in localized_root.iterdir() if path.is_dir()):
                child_instance = (
                    None
                    if _infer_grouped_child_instance_within_parent(
                        path=child,
                        parent_root=base_root,
                    )
                    is not None
                    else raw_input.instance
                )
                add_root(child, instance=child_instance)
        streams_root = (
            base_root if base_root.name == "Streams" else base_root / "Streams"
        )
        if streams_root.exists() and streams_root.is_dir():
            for stream_root in sorted(path for path in streams_root.iterdir() if path.is_dir()):
                add_root(stream_root, instance=None)
                stream_localized_root = stream_root / "Localized"
                if stream_localized_root.exists() and stream_localized_root.is_dir():
                    for child in sorted(
                        path for path in stream_localized_root.iterdir() if path.is_dir()
                    ):
                        add_root(child, instance=None)
    for language_slug in sorted(grouped_roots):
        discovered.append(
            (
                language_code_by_slug[language_slug],
                language_slug,
                tuple(grouped_roots[language_slug]),
            )
        )
    return discovered


def language_slug_from_code(language_code: str | None) -> str:
    normalized = str(language_code or "").strip().lower().replace("_", "-")
    return normalized


def _collect_site_html_files(output_dir: Path) -> set[str]:
    return {
        str(path.relative_to(output_dir)).replace("\\", "/")
        for path in output_dir.rglob("*.html")
    }


_LANGUAGE_SWITCHER_CSS = """
.language-switcher {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  flex-wrap: nowrap;
  padding: 6px 8px 6px 12px;
  border: 1px solid rgba(16, 39, 63, 0.08);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.58);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.40);
}
.language-switcher-label {
  color: #6f859d;
  flex-shrink: 0;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.10em;
  text-transform: uppercase;
}
.language-switcher-links {
  display: inline-flex;
  gap: 6px;
  flex-wrap: nowrap;
}
.language-switcher-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 34px;
  padding: 0 12px;
  border-radius: 999px;
  border: 1px solid rgba(16, 39, 63, 0.12);
  background: rgba(247, 250, 253, 0.92);
  color: #16304f;
  font-size: 12px;
  font-weight: 700;
  text-decoration: none;
}
@media (max-width: 1040px) {
  .language-switcher {
    gap: 8px;
    padding: 5px 6px 5px 8px;
  }
  .language-switcher-label {
    display: none;
  }
  .language-switcher-link {
    min-height: 32px;
    padding: 0 10px;
  }
}
.language-switcher-link.is-active {
  background: #16304f;
  border-color: #16304f;
  color: #f8fbff;
}
@media (max-width: 760px) {
  .language-switcher {
    gap: 8px;
    padding: 0;
    border: 0;
    background: transparent;
    box-shadow: none;
  }
  .language-switcher-label {
    display: none;
  }
}
"""


def _render_language_switcher_fragment(
    *,
    current_language_slug: str,
    current_page_relative_path: str,
    page_paths_by_language: dict[str, set[str]],
    language_code_by_slug: dict[str, str],
) -> Tag:
    switcher_soup = BeautifulSoup("", "html.parser")
    container = switcher_soup.new_tag("div")
    container["class"] = "language-switcher"
    label = switcher_soup.new_tag("span")
    label["class"] = "language-switcher-label"
    label.string = "Language"
    container.append(label)
    links = switcher_soup.new_tag("div")
    links["class"] = "language-switcher-links"
    for language_slug, language_code in language_code_by_slug.items():
        target_relative_path = (
            current_page_relative_path
            if current_page_relative_path in page_paths_by_language.get(language_slug, set())
            else "index.html"
        )
        current_page_path = PurePosixPath(current_language_slug) / current_page_relative_path
        target_page_path = PurePosixPath(language_slug) / target_relative_path
        anchor = switcher_soup.new_tag(
            "a",
            href=posixpath.relpath(
                str(target_page_path),
                start=str(current_page_path.parent),
            ),
        )
        classes = ["language-switcher-link"]
        if language_slug == current_language_slug:
            classes.append("is-active")
        anchor["class"] = " ".join(classes)
        anchor["data-language-code"] = language_slug
        anchor.string = language_code
        links.append(anchor)
    container.append(links)

    script = switcher_soup.new_tag("script")
    script.string = (
        "(function(){"
        "var links=document.querySelectorAll('.language-switcher-link[data-language-code]');"
        "for(var i=0;i<links.length;i+=1){"
        "links[i].addEventListener('click',function(){"
        "try{localStorage.setItem('recoleta-language-code',this.getAttribute('data-language-code')||'');}catch(_err){}"
        "});"
        "}"
        "})();"
    )
    fragment = switcher_soup.new_tag("div")
    fragment.append(container)
    fragment.append(script)
    return fragment


def _apply_site_language_overrides(
    *,
    output_dir: Path,
    language_code: str,
    language_slug: str,
    page_paths_by_language: dict[str, set[str]],
    language_code_by_slug: dict[str, str],
) -> None:
    stylesheet_path = output_dir / "assets" / "site.css"
    if stylesheet_path.exists():
        stylesheet = stylesheet_path.read_text(encoding="utf-8")
        if ".language-switcher {" not in stylesheet:
            stylesheet_path.write_text(
                stylesheet.rstrip() + "\n" + _LANGUAGE_SWITCHER_CSS.strip() + "\n",
                encoding="utf-8",
            )

    inject_switcher = len(language_code_by_slug) > 1
    for html_path in output_dir.rglob("*.html"):
        relative_path = str(html_path.relative_to(output_dir)).replace("\\", "/")
        soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")
        html_tag = soup.find("html")
        if html_tag is not None:
            html_tag["lang"] = language_code

        if inject_switcher:
            nav_actions = soup.select_one(".site-header .nav-actions")
            if nav_actions is not None:
                nav_actions["data-has-language-switcher"] = "true"
                utility_cluster = nav_actions.select_one(".nav-utility-cluster")
                insertion_target = utility_cluster if utility_cluster is not None else nav_actions
                if nav_actions.select_one(".language-switcher") is None:
                    insertion_target.insert(
                        0,
                        _render_language_switcher_fragment(
                            current_language_slug=language_slug,
                            current_page_relative_path=relative_path,
                            page_paths_by_language=page_paths_by_language,
                            language_code_by_slug=language_code_by_slug,
                        ),
                    )
        rendered_html = str(soup).replace(
            f'<html lang="{language_code}">', f"<html lang='{language_code}'>"
        )
        html_path.write_text(rendered_html, encoding="utf-8")


def _render_language_redirect_page(
    *,
    default_language_slug: str,
    language_slugs: list[str],
) -> str:
    languages_json = json.dumps(language_slugs, ensure_ascii=False)
    default_href = f"{default_language_slug}/index.html"
    return (
        "<!doctype html>"
        "<html lang='en'>"
        "<head>"
        "<meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width, initial-scale=1'>"
        "<title>Recoleta Trends</title>"
        "<script>"
        f"const recoletaLanguages={languages_json};"
        "let recoletaLanguage='';"
        "try{recoletaLanguage=(localStorage.getItem('recoleta-language-code')||'').toLowerCase();}catch(_err){}"
        "if(!recoletaLanguages.includes(recoletaLanguage)){"
        f"recoletaLanguage='{default_language_slug}';"
        "}"
        "window.location.replace(recoletaLanguage+'/index.html');"
        "</script>"
        "</head>"
        "<body>"
        f"<p>Redirecting to <a href='{default_href}'>{default_href}</a>...</p>"
        "</body>"
        "</html>"
    )


def _export_trend_static_site_single_language(
    *,
    input_dir: Path | TrendSiteInputSpec | Sequence[Path | TrendSiteInputSpec],
    output_dir: Path,
    limit: int | None = None,
    item_export_scope: str = "linked",
    include_localized_children: bool = True,
) -> Path:
    normalized_item_export_scope = _normalize_item_export_scope(item_export_scope)
    resolved_input_roots = _coerce_site_input_specs(input_dir)
    resolved_input_dirs = _discover_trend_site_input_dirs(
        resolved_input_roots,
        include_localized_children=include_localized_children,
    )
    resolved_output_dir = output_dir.expanduser().resolve()
    for input_info in resolved_input_dirs:
        if _paths_overlap(input_info.path, resolved_output_dir):
            raise ValueError(
                "Trend site output directory must not overlap the input directory"
            )
    _reset_directory(resolved_output_dir)
    (resolved_output_dir / "assets").mkdir(parents=True, exist_ok=True)
    (resolved_output_dir / "ideas").mkdir(parents=True, exist_ok=True)
    (resolved_output_dir / "items").mkdir(parents=True, exist_ok=True)
    (resolved_output_dir / "topics").mkdir(parents=True, exist_ok=True)
    (resolved_output_dir / "streams").mkdir(parents=True, exist_ok=True)

    trend_source_documents = _load_trend_source_documents(
        input_dirs=resolved_input_dirs,
        limit=limit,
    )
    idea_source_documents = _load_idea_source_documents(
        input_dirs=resolved_input_dirs,
        limit=limit,
    )
    item_selection = _select_item_source_documents(
        input_dirs=resolved_input_dirs,
        trend_source_documents=trend_source_documents,
        idea_source_documents=idea_source_documents,
        item_export_scope=normalized_item_export_scope,
    )
    item_documents, item_pages_by_source_key = _load_item_site_documents(
        source_documents=item_selection.source_documents,
        output_dir=resolved_output_dir,
    )
    documents = _load_trend_site_documents(
        source_documents=trend_source_documents,
        output_dir=resolved_output_dir,
        item_pages_by_source_key=item_pages_by_source_key,
    )
    linked_page_by_source_key = dict(item_pages_by_source_key)
    linked_page_by_source_key.update(
        {
            _site_source_key(
                markdown_path=document.markdown_path,
                instance=document.instance,
            ): document.page_path
            for document in documents
        }
    )
    idea_documents, idea_pages_by_source_key = _load_idea_site_documents(
        source_documents=idea_source_documents,
        output_dir=resolved_output_dir,
        linked_page_by_source_key=linked_page_by_source_key,
    )
    linked_page_by_source_key.update(idea_pages_by_source_key)

    label_by_topic_slug: dict[str, str] = {}
    topic_documents: dict[str, list[TrendSiteDocument]] = defaultdict(list)
    idea_documents_by_topic: dict[str, list[IdeaSiteDocument]] = defaultdict(list)
    for document in documents:
        for topic in document.topics:
            slug = _topic_slug(topic)
            label_by_topic_slug.setdefault(slug, topic)
            topic_documents[slug].append(document)
    for document in idea_documents:
        for topic in document.topics:
            slug = _topic_slug(topic)
            label_by_topic_slug.setdefault(slug, topic)
            idea_documents_by_topic[slug].append(document)

    topic_pages = {
        slug: resolved_output_dir / "topics" / f"{slug}.html"
        for slug in sorted(set(topic_documents.keys()) | set(idea_documents_by_topic.keys()))
    }

    (resolved_output_dir / "assets" / "site.css").write_text(
        _SITE_CSS.strip() + "\n",
        encoding="utf-8",
    )
    (resolved_output_dir / ".nojekyll").write_text("", encoding="utf-8")

    (resolved_output_dir / "index.html").write_text(
        _render_home_page(
            documents=documents,
            idea_documents=idea_documents,
            output_dir=resolved_output_dir,
            topic_pages=topic_pages,
        ),
        encoding="utf-8",
    )
    (resolved_output_dir / "trends" / "index.html").write_text(
        _render_trends_index_page(
            documents=documents,
            output_dir=resolved_output_dir,
            topic_pages=topic_pages,
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
            idea_documents=idea_documents,
            output_dir=resolved_output_dir,
            topic_pages=topic_pages,
        ),
        encoding="utf-8",
    )
    (resolved_output_dir / "ideas" / "index.html").write_text(
        _render_ideas_index_page(
            documents=idea_documents,
            output_dir=resolved_output_dir,
            topic_pages=topic_pages,
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
            ),
            encoding="utf-8",
        )

    for document in idea_documents:
        document.page_path.write_text(
            _render_idea_page(
                document=document,
                output_dir=resolved_output_dir,
                topic_pages=topic_pages,
            ),
            encoding="utf-8",
        )

    for slug, page_path in topic_pages.items():
        page_path.write_text(
            _render_topic_page(
                topic=label_by_topic_slug[slug],
                topic_slug=slug,
                documents=topic_documents[slug],
                idea_documents=idea_documents_by_topic.get(slug, []),
                output_dir=resolved_output_dir,
                topic_pages=topic_pages,
            ),
            encoding="utf-8",
        )

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "input_dir": (
            str(resolved_input_roots[0].path)
            if len(resolved_input_roots) == 1
            else [str(input_spec.path) for input_spec in resolved_input_roots]
        ),
        "input_dirs": [
            {
                "path": str(input_info.path),
                "ideas_path": str(input_info.ideas_path) if input_info.ideas_path is not None else None,
                "inbox_path": str(input_info.inbox_path) if input_info.inbox_path is not None else None,
                "instance": input_info.instance,
            }
            for input_info in resolved_input_dirs
        ],
        "output_dir": str(resolved_output_dir),
        "item_export_scope": normalized_item_export_scope,
        "trends_total": len(documents),
        "ideas_total": len(idea_documents),
        "items_total": len(item_documents),
        "items_available_total": item_selection.available_total,
        "items_unreferenced_total": item_selection.unreferenced_total,
        "topics_total": len(topic_pages),
        "files": {
            "index": "index.html",
            "archive": "archive.html",
            "nojekyll": ".nojekyll",
            "trends_index": "trends/index.html",
            "ideas_index": "ideas/index.html",
            "topics_index": "topics/index.html",
            "stylesheet": "assets/site.css",
            "trend_pages": [
                str(document.page_path.relative_to(resolved_output_dir))
                for document in documents
            ],
            "idea_pages": [
                str(document.page_path.relative_to(resolved_output_dir))
                for document in idea_documents
            ],
            "item_pages": [
                str(document.page_path.relative_to(resolved_output_dir))
                for document in item_documents
            ],
            "topic_pages": [
                str(path.relative_to(resolved_output_dir))
                for path in topic_pages.values()
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
        item_export_scope=normalized_item_export_scope,
        trends_total=len(documents),
        ideas_total=len(idea_documents),
        items_total=len(item_documents),
        items_available_total=item_selection.available_total,
        items_unreferenced_total=item_selection.unreferenced_total,
        topics_total=len(topic_pages),
    ).info("Trend static site export completed")
    return manifest_path


def export_trend_static_site(
    *,
    input_dir: Path | TrendSiteInputSpec | Sequence[Path | TrendSiteInputSpec],
    output_dir: Path,
    limit: int | None = None,
    default_language_code: str | None = None,
    item_export_scope: str = "linked",
) -> Path:
    normalized_item_export_scope = _normalize_item_export_scope(item_export_scope)
    resolved_input_roots = _coerce_site_input_specs(input_dir)
    language_inputs = _discover_site_language_inputs(resolved_input_roots)
    valid_language_inputs = [
        (language_code, language_slug, root_paths)
        for language_code, language_slug, root_paths in language_inputs
        if language_code is not None and language_slug
    ]

    if len(valid_language_inputs) <= 1:
        manifest_path = _export_trend_static_site_single_language(
            input_dir=input_dir,
            output_dir=output_dir,
            limit=limit,
            item_export_scope=normalized_item_export_scope,
        )
        if valid_language_inputs:
            language_code, language_slug, _root_paths = valid_language_inputs[0]
            resolved_output_dir = output_dir.expanduser().resolve()
            _apply_site_language_overrides(
                output_dir=resolved_output_dir,
                language_code=str(language_code),
                language_slug=language_slug,
                page_paths_by_language={language_slug: _collect_site_html_files(resolved_output_dir)},
                language_code_by_slug={language_slug: str(language_code)},
            )
        return manifest_path

    normalized_default_language_slug = language_slug_from_code(default_language_code)
    if not normalized_default_language_slug:
        raise ValueError(
            "default_language_code is required when exporting a multilingual site"
        )
    if normalized_default_language_slug not in {
        language_slug for _language_code, language_slug, _root_paths in valid_language_inputs
    }:
        raise ValueError(
            "default_language_code must match one discovered language root"
        )

    resolved_output_dir = output_dir.expanduser().resolve()
    _reset_directory(resolved_output_dir)
    (resolved_output_dir / ".nojekyll").write_text("", encoding="utf-8")

    manifest_by_language: dict[str, dict[str, Any]] = {}
    page_paths_by_language: dict[str, set[str]] = {}
    language_code_by_slug: dict[str, str] = {}

    for language_code, language_slug, root_paths in valid_language_inputs:
        language_output_dir = resolved_output_dir / language_slug
        manifest_path = _export_trend_static_site_single_language(
            input_dir=list(root_paths),
            output_dir=language_output_dir,
            limit=limit,
            item_export_scope=normalized_item_export_scope,
            include_localized_children=False,
        )
        manifest_by_language[language_slug] = json.loads(
            manifest_path.read_text(encoding="utf-8")
        )
        page_paths_by_language[language_slug] = _collect_site_html_files(language_output_dir)
        language_code_by_slug[language_slug] = str(language_code)

    for language_slug, language_code in language_code_by_slug.items():
        _apply_site_language_overrides(
            output_dir=resolved_output_dir / language_slug,
            language_code=language_code,
            language_slug=language_slug,
            page_paths_by_language=page_paths_by_language,
            language_code_by_slug=language_code_by_slug,
        )

    default_manifest = manifest_by_language[normalized_default_language_slug]
    aggregate_manifest = dict(default_manifest)
    aggregate_files = dict(default_manifest.get("files") or {})
    aggregate_files["language_homes"] = {
        language_slug: f"{language_slug}/index.html"
        for language_slug in sorted(language_code_by_slug)
    }
    aggregate_files["language_manifests"] = {
        language_slug: f"{language_slug}/manifest.json"
        for language_slug in sorted(language_code_by_slug)
    }
    aggregate_files["by_language"] = {
        language_slug: dict(manifest_by_language[language_slug].get("files") or {})
        for language_slug in sorted(language_code_by_slug)
    }
    aggregate_manifest["files"] = aggregate_files
    aggregate_manifest["languages"] = sorted(language_code_by_slug)
    aggregate_manifest["language_codes"] = language_code_by_slug
    aggregate_manifest["default_language_code"] = normalized_default_language_slug
    aggregate_manifest["output_dir"] = str(resolved_output_dir)

    manifest_path = resolved_output_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(aggregate_manifest, ensure_ascii=False, indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )
    (resolved_output_dir / "index.html").write_text(
        _render_language_redirect_page(
            default_language_slug=normalized_default_language_slug,
            language_slugs=sorted(language_code_by_slug),
        ),
        encoding="utf-8",
    )
    logger.bind(
        module="site.build.multilang",
        output_dir=str(resolved_output_dir),
        languages=sorted(language_code_by_slug),
        default_language_code=normalized_default_language_slug,
    ).info("Multilingual trend static site export completed")
    return manifest_path


def stage_trend_site_source(
    *,
    input_dir: Path | TrendSiteInputSpec | Sequence[Path | TrendSiteInputSpec],
    output_dir: Path,
    limit: int | None = None,
    default_language_code: str | None = None,
    item_export_scope: str = "linked",
) -> Path:
    normalized_item_export_scope = _normalize_item_export_scope(item_export_scope)
    resolved_input_roots = _coerce_site_input_specs(input_dir)
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
    idea_source_documents = _load_idea_source_documents(
        input_dirs=resolved_input_dirs,
        limit=limit,
    )
    item_selection = _select_item_source_documents(
        input_dirs=resolved_input_dirs,
        trend_source_documents=source_documents,
        idea_source_documents=idea_source_documents,
        item_export_scope=normalized_item_export_scope,
    )
    item_source_documents = item_selection.source_documents
    has_instance_documents = any(
        bool(source_document.instance) for source_document in source_documents
    )
    staged_markdown_files: list[str] = []
    staged_idea_files: list[str] = []
    staged_pdf_files: list[str] = []
    staged_item_files: list[str] = []

    def relative_to_stage_root(path: Path) -> str:
        return str(path.relative_to(stage_root))

    def stage_root_for_surface(
        *,
        instance: str | None,
        source_input: TrendSiteInputDirectory | None,
    ) -> Path:
        language_slug = (
            str(getattr(source_input, "language_slug", None) or "").strip()
            if source_input is not None and getattr(source_input, "is_localized_root", False)
            else ""
        )
        if instance:
            base_root = stage_root / "Streams" / instance
            return base_root / "Localized" / language_slug if language_slug else base_root
        if language_slug:
            return stage_root / "Localized" / language_slug
        return stage_root

    for source_document in source_documents:
        source_input = next(
            (
                input_info
                for input_info in resolved_input_dirs
                if input_info.path == source_document.markdown_path.parent
            ),
            None,
        )
        surface_root = stage_root_for_surface(
            instance=source_document.instance,
            source_input=source_input,
        )
        target_dir = (
            surface_root / "Trends"
            if source_document.instance or has_instance_documents or surface_root != stage_root
            else resolved_output_dir
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
        source_input = next(
            (
                input_info
                for input_info in resolved_input_dirs
                if input_info.inbox_path == source_document.markdown_path.parent
            ),
            None,
        )
        surface_root = stage_root_for_surface(
            instance=source_document.instance,
            source_input=source_input,
        )
        target_dir = surface_root / "Inbox"
        target_dir.mkdir(parents=True, exist_ok=True)
        staged_item_path = target_dir / source_document.markdown_path.name
        shutil.copy2(source_document.markdown_path, staged_item_path)
        staged_item_files.append(relative_to_stage_root(staged_item_path))

    for source_document in idea_source_documents:
        source_input = next(
            (
                input_info
                for input_info in resolved_input_dirs
                if input_info.ideas_path == source_document.markdown_path.parent
            ),
            None,
        )
        surface_root = stage_root_for_surface(
            instance=source_document.instance,
            source_input=source_input,
        )
        target_dir = surface_root / "Ideas"
        target_dir.mkdir(parents=True, exist_ok=True)
        staged_idea_path = target_dir / source_document.markdown_path.name
        shutil.copy2(source_document.markdown_path, staged_idea_path)
        staged_idea_files.append(relative_to_stage_root(staged_idea_path))

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "input_dir": (
            str(resolved_input_roots[0].path)
            if len(resolved_input_roots) == 1
            else [str(input_spec.path) for input_spec in resolved_input_roots]
        ),
        "input_dirs": [
            {
                "path": str(input_info.path),
                "ideas_path": str(input_info.ideas_path) if input_info.ideas_path is not None else None,
                "inbox_path": str(input_info.inbox_path) if input_info.inbox_path is not None else None,
                "instance": input_info.instance,
                "language_code": input_info.language_code,
                "language_slug": input_info.language_slug,
                "is_localized_root": bool(input_info.is_localized_root),
            }
            for input_info in resolved_input_dirs
        ],
        "output_dir": str(resolved_output_dir),
        "default_language_code": language_slug_from_code(default_language_code),
        "languages": sorted(
            {
                str(input_info.language_slug or "").strip()
                for input_info in resolved_input_dirs
                if str(input_info.language_slug or "").strip()
            }
        ),
        "item_export_scope": normalized_item_export_scope,
        "trends_total": len(source_documents),
        "ideas_total": len(idea_source_documents),
        "items_total": len(item_source_documents),
        "items_available_total": item_selection.available_total,
        "items_unreferenced_total": item_selection.unreferenced_total,
        "pdf_total": len(staged_pdf_files),
        "files": {
            "markdown": staged_markdown_files,
            "ideas_markdown": staged_idea_files,
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
        item_export_scope=normalized_item_export_scope,
        trends_total=len(source_documents),
        ideas_total=len(idea_source_documents),
        items_total=len(item_source_documents),
        items_available_total=item_selection.available_total,
        items_unreferenced_total=item_selection.unreferenced_total,
        pdf_total=len(staged_pdf_files),
    ).info("Trend site source staging completed")
    return manifest_path
