from __future__ import annotations

from dataclasses import dataclass
from collections import Counter, defaultdict
from collections.abc import Sequence
from datetime import datetime, timezone
import html
import json
import os
from pathlib import Path
from pathlib import PurePosixPath
import posixpath
import re
import shutil
import time
from typing import Any
from urllib.parse import quote, urlparse

from babel import Locale
from babel.core import UnknownLocaleError
from bs4 import BeautifulSoup, Tag
from loguru import logger
from markdown_it import MarkdownIt
from slugify import slugify

from recoleta.presentation import (
    PRESENTATION_SCHEMA_VERSION,
    idea_display_labels,
    presentation_sidecar_path,
    trend_display_labels,
    validate_presentation,
)
from recoleta.publish.trend_render_shared import (
    _build_trend_browser_body_html,
    _extract_trend_pdf_sections,
    _render_browser_content_card_html,
    _render_browser_section_label_html,
    _normalize_obsidian_callouts_for_pdf,
    _split_yaml_frontmatter_text,
    _trend_date_token,
    sanitize_trend_title,
)
from recoleta.site_inputs import (
    SiteInputDiscoveryDeps,
    SiteItemSourceLoadDeps,
    SiteLanguageDiscoveryDeps,
    SiteReferenceCollectionDeps,
    TrendSiteDocumentLoadDeps,
    TrendSiteSourceStageDeps,
    TrendSiteSourceStageRequest,
    collect_referenced_item_source_keys as _collect_referenced_item_source_keys_impl,
    discover_site_language_inputs as _discover_site_language_inputs_impl,
    discover_trend_site_input_dirs as _discover_trend_site_input_dirs_impl,
    load_trend_site_documents as _load_trend_site_documents_impl,
    load_item_source_documents as _load_item_source_documents_impl,
    stage_trend_site_source as _stage_trend_site_source_impl,
)
from recoleta.site_models import (
    IdeaBodyRenderResult,
    IdeaSiteDocument,
    IdeaSiteSourceDocument,
    ItemSiteDocument,
    ItemSiteSelection,
    ItemSiteSourceDocument,
    SiteSourceKey,
    TrendSiteDocument,
    TrendSiteInputDirectory,
    TrendSiteInputSpec,
    TrendSiteSourceDocument,
)
from recoleta.site_email_links import (
    aggregate_multilingual_email_links,
    remove_child_email_links_artifacts,
    write_email_links_artifact,
)
from recoleta.site_pages import (
    SingleLanguageSiteExportDeps,
    SingleLanguageSiteExportRequest,
    SitePagination,
    SitePageShellInput,
    export_trend_static_site_single_language as _export_trend_static_site_single_language_impl,
    render_site_page_shell as _render_site_page_shell_impl,
)
from recoleta.site_presentation import (
    IdeaBrowserBodyDeps,
    build_idea_browser_body_html as _build_idea_browser_body_html_impl,
    build_item_browser_body_html as _build_item_browser_body_html_impl,
    render_presentation_source_list as _render_presentation_source_list_impl,
)

RECOLETA_REPO_URL = "https://github.com/NeapolitanIcecream/recoleta"
RECOLETA_QUICKSTART_URL = f"{RECOLETA_REPO_URL}#recoleta-quickstart"


@dataclass(frozen=True, slots=True)
class _SiteLanguageOverrideSpec:
    output_dir: Path
    language_code: str
    language_slug: str
    page_paths_by_language: dict[str, set[str]]
    language_code_by_slug: dict[str, str]


@dataclass(frozen=True, slots=True)
class _TopicCardRenderRequest:
    topic: str
    trend_count: int
    idea_count: int
    latest_token: str
    page_path: Path
    topic_page_path: Path


@dataclass(frozen=True, slots=True)
class _TopicPageRenderRequest:
    topic: str
    topic_slug: str
    documents: list[TrendSiteDocument]
    idea_documents: list[IdeaSiteDocument]
    total_documents: int
    total_idea_documents: int
    output_dir: Path
    topic_pages: dict[str, Path]
    pagination: SitePagination
    page_size: int


@dataclass(frozen=True, slots=True)
class _TopicCardGridRenderRequest:
    page_path: Path
    topic_pages: dict[str, Path]
    label_by_slug: dict[str, str]
    latest_by_topic: dict[str, TrendSiteDocument | IdeaSiteDocument]
    topic_counter: Counter[str]
    trend_counter: Counter[str]
    idea_counter: Counter[str]
    offset: int = 0
    limit: int | None = None


def _export_single_language_trend_static_site(
    *,
    input_dir: Path | TrendSiteInputSpec | Sequence[Path | TrendSiteInputSpec],
    output_dir: Path,
    limit: int | None,
    item_export_scope: str,
    language_inputs: Sequence[tuple[str | None, str, tuple[TrendSiteInputSpec, ...]]],
) -> Path:
    manifest_path = _export_trend_static_site_single_language(
        input_dir=input_dir,
        output_dir=output_dir,
        limit=limit,
        item_export_scope=item_export_scope,
    )
    valid_language_inputs = [
        (language_code, language_slug)
        for language_code, language_slug, _root_paths in language_inputs
        if language_code is not None and language_slug
    ]
    if valid_language_inputs:
        language_code, language_slug = valid_language_inputs[0]
        resolved_output_dir = output_dir.expanduser().resolve()
        _apply_site_language_overrides(
            output_dir=resolved_output_dir,
            language_code=str(language_code),
            language_slug=language_slug,
            page_paths_by_language={
                language_slug: _collect_site_html_files(resolved_output_dir)
            },
            language_code_by_slug={language_slug: str(language_code)},
        )
    return manifest_path


def _write_multilingual_site_outputs(
    *,
    output_dir: Path,
    valid_language_inputs: Sequence[tuple[str, str, tuple[TrendSiteInputSpec, ...]]],
    limit: int | None,
    item_export_scope: str,
    metrics_recorder: Any | None = None,
) -> tuple[dict[str, dict[str, Any]], dict[str, set[str]], dict[str, str]]:
    manifest_by_language: dict[str, dict[str, Any]] = {}
    page_paths_by_language: dict[str, set[str]] = {}
    language_code_by_slug: dict[str, str] = {}
    for language_code, language_slug, root_paths in valid_language_inputs:
        language_output_dir = output_dir / language_slug
        export_started = time.perf_counter()
        manifest_path = _export_trend_static_site_single_language(
            input_dir=list(root_paths),
            output_dir=language_output_dir,
            limit=limit,
            item_export_scope=item_export_scope,
            include_localized_children=False,
        )
        _record_site_build_timing(
            metrics_recorder=metrics_recorder,
            step_name="multilang.export_language",
            started=export_started,
            metadata={"language_slug": language_slug},
        )
        manifest_by_language[language_slug] = json.loads(
            manifest_path.read_text(encoding="utf-8")
        )
        page_paths_by_language[language_slug] = _collect_site_html_files(
            language_output_dir
        )
        language_code_by_slug[language_slug] = str(language_code)
    return manifest_by_language, page_paths_by_language, language_code_by_slug


def _aggregate_multilingual_site_manifest(
    *,
    output_dir: Path,
    manifest_by_language: dict[str, dict[str, Any]],
    language_code_by_slug: dict[str, str],
    default_language_slug: str,
) -> dict[str, Any]:
    default_manifest = manifest_by_language[default_language_slug]
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
    aggregate_manifest["default_language_code"] = default_language_slug
    aggregate_manifest["output_dir"] = str(output_dir)
    return aggregate_manifest


def _record_site_build_timing(
    *,
    metrics_recorder: Any | None,
    step_name: str,
    started: float,
    metadata: dict[str, Any] | None = None,
) -> None:
    if not callable(metrics_recorder):
        return
    metrics_recorder(
        str(step_name),
        int((time.perf_counter() - started) * 1000),
        dict(metadata or {}),
    )


def _coerce_topic_page_render_request(
    *,
    request: _TopicPageRenderRequest | None = None,
    legacy_kwargs: dict[str, Any] | None = None,
) -> _TopicPageRenderRequest:
    if request is not None:
        return request
    values = dict(legacy_kwargs or {})
    topic_slug = str(values["topic_slug"])
    topic_pages = dict(values["topic_pages"])
    page_path = topic_pages[topic_slug]
    pagination = values.get("pagination")
    if not isinstance(pagination, SitePagination):
        pagination = SitePagination(
            current_page=1,
            total_pages=1,
            page_path=page_path,
            page_paths=(page_path,),
        )
    documents = list(values["documents"])
    idea_documents = list(values["idea_documents"])
    return _TopicPageRenderRequest(
        topic=str(values["topic"]),
        topic_slug=topic_slug,
        documents=documents,
        idea_documents=idea_documents,
        total_documents=int(values.get("total_documents", len(documents))),
        total_idea_documents=int(
            values.get("total_idea_documents", len(idea_documents))
        ),
        output_dir=values["output_dir"],
        topic_pages=topic_pages,
        pagination=pagination,
        page_size=max(1, int(values.get("page_size", max(len(documents), 1)))),
    )


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


def _load_presentation_for_site(
    *,
    markdown_path: Path,
    surface_kind: str,
) -> dict[str, Any] | None:
    sidecar_path = presentation_sidecar_path(note_path=markdown_path)
    if not sidecar_path.exists() or not sidecar_path.is_file():
        return None
    try:
        payload = json.loads(sidecar_path.read_text(encoding="utf-8"))
    except Exception:
        return None
    if not isinstance(payload, dict):
        return None
    try:
        schema_version = int(payload.get("presentation_schema_version") or 0)
    except Exception:
        return None
    if schema_version != PRESENTATION_SCHEMA_VERSION:
        return None
    if str(payload.get("surface_kind") or "").strip().lower() != surface_kind:
        return None
    content = payload.get("content")
    if not isinstance(content, dict):
        return None
    if validate_presentation(payload):
        return None
    return payload


def _presentation_labels(
    *,
    surface_kind: str,
    presentation: dict[str, Any],
) -> dict[str, str]:
    language_code = str(presentation.get("language_code") or "").strip() or None
    return (
        trend_display_labels(language_code=language_code)
        if surface_kind == "trend"
        else idea_display_labels(language_code=language_code)
    )


def _humanize_source_type(value: str) -> str:
    normalized = str(value or "").strip().replace("_", " ")
    if not normalized:
        return "Unknown"
    return normalized[:1].upper() + normalized[1:]


def _humanize_confidence(value: str) -> str:
    normalized = str(value or "").strip().lower()
    if not normalized:
        return "Unknown"
    return normalized[:1].upper() + normalized[1:]


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
    sentence_boundaries = [
        match.end()
        for match in re.finditer(
            r"(?:[。！？]|[.!?](?=\s|$))",
            collapsed[: limit + 1],
        )
        if match.end() >= max(80, limit // 2)
    ]
    if sentence_boundaries:
        return collapsed[: sentence_boundaries[-1]].rstrip()
    boundary = collapsed.rfind(" ", 0, limit)
    if boundary < max(80, limit // 2):
        boundary = limit
    truncated = re.sub(r"[,;:，；：、]+$", "", collapsed[:boundary].rstrip()).rstrip()
    return truncated + "…"


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


def _display_item_source(source: str | None) -> str:
    cleaned = str(source or "").strip()
    if not cleaned:
        return "Item"
    return {
        "arxiv": "arXiv",
        "hf_daily": "Hugging Face Daily",
        "hn": "Hacker News",
        "openreview": "OpenReview",
        "rss": "RSS",
    }.get(cleaned.lower(), cleaned)


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


def _reject_legacy_stream_layout(path: Path, *, context: str) -> None:
    resolved = path.expanduser().resolve()
    if resolved.name == "Streams":
        raise ValueError(
            f"{context} no longer supports legacy Streams layouts: {resolved}"
        )
    legacy_streams_root = resolved / "Streams"
    if legacy_streams_root.exists() and legacy_streams_root.is_dir():
        if (resolved / "manifest.json").exists():
            return
        raise ValueError(
            f"{context} no longer supports legacy Streams layouts: {legacy_streams_root}"
        )


_STREAM_DISPLAY_INITIALISMS = {
    "ai",
    "api",
    "cpu",
    "cv",
    "gpu",
    "llm",
    "mcp",
    "ml",
    "nlp",
    "ocr",
    "qa",
    "rag",
    "rl",
    "ui",
    "ux",
    "vla",
    "vlm",
    "vln",
}


def _display_site_instance(instance: str | None) -> str | None:
    cleaned = _normalize_site_instance(instance)
    if cleaned is None:
        return None
    normalized = re.sub(r"[_-]+", " ", cleaned).strip()
    if normalized == cleaned and not cleaned.islower():
        return cleaned
    tokens = [
        token.upper()
        if token.lower() in _STREAM_DISPLAY_INITIALISMS
        else token.capitalize()
        for token in normalized.split()
    ]
    return " ".join(tokens) if tokens else cleaned


def _display_topic_label(topic: str) -> str:
    cleaned = str(topic or "").strip()
    if not cleaned:
        return ""
    if "-" in cleaned and any(character.isupper() for character in cleaned):
        return cleaned
    normalized = re.sub(r"[_-]+", " ", cleaned).strip()
    if normalized == cleaned and not cleaned.islower():
        return cleaned
    tokens = [
        token.upper()
        if token.lower() in _STREAM_DISPLAY_INITIALISMS
        else token.capitalize()
        for token in normalized.split()
    ]
    return " ".join(tokens) if tokens else cleaned


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
    return _count_label(0, singular="entry", plural="entries")


def _format_collection_meta(
    *,
    trend_count: int = 0,
    idea_count: int = 0,
    latest_token: str,
) -> str:
    mix = _format_collection_mix(trend_count=trend_count, idea_count=idea_count)
    return f"{mix} · latest window {latest_token}" if latest_token else mix


def _record_latest_document(
    *,
    latest_by_slug: dict[str, TrendSiteDocument | IdeaSiteDocument],
    slug: str,
    document: TrendSiteDocument | IdeaSiteDocument,
) -> None:
    existing = latest_by_slug.get(slug)
    if existing is None or _rendered_document_sort_key(
        document
    ) > _rendered_document_sort_key(existing):
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
    return _infer_instance_name_from_trends_dir(
        path
    ) or _infer_instance_name_from_site_root(
        path.parent if path.name == "Trends" else path
    )


def _discover_trend_site_input_dirs(
    raw_inputs: Sequence[TrendSiteInputSpec],
    *,
    include_localized_children: bool = True,
) -> list[TrendSiteInputDirectory]:
    return _discover_trend_site_input_dirs_impl(
        list(raw_inputs),
        include_localized_children=include_localized_children,
        deps=SiteInputDiscoveryDeps(
            normalize_site_instance=_normalize_site_instance,
            infer_instance_name_from_site_path=_infer_instance_name_from_site_path,
            infer_site_language_code_from_root=_infer_site_language_code_from_root,
            language_slug_from_code=language_slug_from_code,
            reject_legacy_stream_layout=_reject_legacy_stream_layout,
            validate_unique_site_instance_slugs=_validate_unique_site_instance_slugs,
        ),
    )


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
            pills.append(
                f"<span class='topic-pill'>{html.escape(_display_topic_label(cleaned))}</span>"
            )
            continue
        href = _site_href(from_page=from_page, to_page=topic_page)
        pills.append(
            f"<a class='topic-pill topic-pill-link' href='{href}'>{html.escape(_display_topic_label(cleaned))}</a>"
        )
    return (
        "".join(pills)
        if pills
        else "<span class='meta-pill subdued'>No tracked topics</span>"
    )


def _render_site_page(spec: SitePageShellInput) -> str:
    return _render_site_page_shell_impl(
        spec=spec,
        site_href=_site_href,
    )


def _render_trend_card(
    *,
    document: TrendSiteDocument,
    from_page: Path,
    topic_pages: dict[str, Path],
    include_kind: bool = False,
) -> str:
    trend_href = _site_href(from_page=from_page, to_page=document.page_path)
    topic_links = _render_topic_link_pills(
        topics=document.topics[:4],
        from_page=from_page,
        topic_pages=topic_pages,
    )
    meta_parts = [document.granularity.title(), document.period_token]
    if include_kind:
        meta_parts.insert(0, "Trend")
    if display_instance := _display_site_instance(document.instance):
        meta_parts.append(display_instance)
    return (
        "<article class='trend-card'>"
        "<div class='card-meta-row'>"
        f"<span class='meta-date'>{html.escape(' · '.join(meta_parts))}</span>"
        "</div>"
        f"<h2 class='card-title'><a href='{trend_href}'>{html.escape(document.title)}</a></h2>"
        f"<p class='card-excerpt'>{html.escape(document.excerpt)}</p>"
        f"<div class='topic-pill-row'>{topic_links}</div>"
        "</article>"
    )


def _render_topic_card(
    *,
    request: _TopicCardRenderRequest,
) -> str:
    href = _site_href(from_page=request.page_path, to_page=request.topic_page_path)
    return (
        "<article class='topic-card'>"
        f"<h2 class='topic-card-title'><a href='{href}'>{html.escape(_display_topic_label(request.topic))}</a></h2>"
        f"<div class='topic-card-meta'>{html.escape(_format_collection_meta(trend_count=request.trend_count, idea_count=request.idea_count, latest_token=request.latest_token))}</div>"
        "</article>"
    )


def _render_topic_card_grid(*, request: _TopicCardGridRenderRequest) -> str:
    most_common = request.topic_counter.most_common()
    if request.limit is not None:
        most_common = most_common[request.offset : request.offset + request.limit]
    elif request.offset > 0:
        most_common = most_common[request.offset :]
    return "".join(
        _render_topic_card(
            request=_TopicCardRenderRequest(
                topic=request.label_by_slug[slug],
                trend_count=request.trend_counter[slug],
                idea_count=request.idea_counter[slug],
                latest_token=request.latest_by_topic[slug].period_token,
                page_path=request.page_path,
                topic_page_path=request.topic_pages[slug],
            )
        )
        for slug, _count in most_common
        if slug in request.topic_pages
    )


def _latest_collection_token(
    documents: Sequence[TrendSiteDocument | IdeaSiteDocument],
) -> str:
    if not documents:
        return "n/a"
    latest_document = max(documents, key=_rendered_document_sort_key)
    return latest_document.period_token or "n/a"


def _pagination_window(*, current_page: int, total_pages: int) -> list[int | None]:
    if total_pages <= 7:
        return list(range(1, total_pages + 1))
    visible_pages = {1, total_pages}
    visible_pages.update(
        range(max(1, current_page - 2), min(total_pages, current_page + 2) + 1)
    )
    ordered_pages = sorted(visible_pages)
    window: list[int | None] = []
    previous_page = 0
    for page_number in ordered_pages:
        if previous_page and page_number - previous_page > 1:
            window.append(None)
        window.append(page_number)
        previous_page = page_number
    return window


def _render_pagination_direction(
    *,
    label: str,
    target_page: int | None,
    rel: str,
    modifier: str,
    pagination: SitePagination,
) -> str:
    class_name = f"pagination-link pagination-direction {modifier}"
    if target_page is None:
        return (
            f"<span class='{class_name} is-disabled' aria-disabled='true'>"
            f"{html.escape(label)}"
            "</span>"
        )
    href = _site_href(
        from_page=pagination.page_path,
        to_page=pagination.page_paths[target_page - 1],
    )
    return (
        f"<a class='{class_name}' href='{html.escape(href, quote=True)}' rel='{rel}'>"
        f"{html.escape(label)}"
        "</a>"
    )


def _render_collection_pagination(
    *,
    pagination: SitePagination,
    collection_label: str,
) -> str:
    if pagination.total_pages <= 1:
        return ""
    page_links: list[str] = []
    for page_number in _pagination_window(
        current_page=pagination.current_page,
        total_pages=pagination.total_pages,
    ):
        if page_number is None:
            page_links.append(
                "<span class='pagination-ellipsis' aria-hidden='true'>…</span>"
            )
            continue
        if page_number == pagination.current_page:
            page_links.append(
                "<span class='pagination-link is-current' aria-current='page'>"
                f"{page_number}"
                "</span>"
            )
            continue
        href = _site_href(
            from_page=pagination.page_path,
            to_page=pagination.page_paths[page_number - 1],
        )
        page_links.append(
            "<a class='pagination-link' "
            f"href='{html.escape(href, quote=True)}' "
            f"aria-label='Go to page {page_number}'>{page_number}</a>"
        )

    status = f"Page {pagination.current_page} of {pagination.total_pages}"
    return (
        "<nav class='collection-pagination' "
        f"aria-label='{html.escape(collection_label, quote=True)} pagination'>"
        f"{_render_pagination_direction(label='Previous', target_page=pagination.current_page - 1 if pagination.current_page > 1 else None, rel='prev', modifier='pagination-previous', pagination=pagination)}"
        "<div class='pagination-center'>"
        f"<div class='pagination-pages'>{''.join(page_links)}</div>"
        f"<span class='pagination-status'>{html.escape(status)}</span>"
        "</div>"
        f"{_render_pagination_direction(label='Next', target_page=pagination.current_page + 1 if pagination.current_page < pagination.total_pages else None, rel='next', modifier='pagination-next', pagination=pagination)}"
        "</nav>"
    )


def _paginated_count_text(*, count_text: str, pagination: SitePagination) -> str:
    if pagination.total_pages <= 1:
        return count_text
    return f"{count_text} · Page {pagination.current_page} of {pagination.total_pages}"


def _paginated_document_title(*, title: str, pagination: SitePagination) -> str:
    if pagination.current_page <= 1:
        return title
    return f"{title} · Page {pagination.current_page}"


def _render_collection_summary_section(
    *,
    summary_label: str,
    title: str,
    trend_count: int,
    idea_count: int,
    latest_token: str,
    pagination: SitePagination,
) -> str:
    page_status = (
        f"<span class='meta-date'>Page {pagination.current_page} of {pagination.total_pages}</span>"
        if pagination.total_pages > 1
        else ""
    )
    return (
        "<section class='home-section collection-summary-section'>"
        "<div class='section-heading-row'>"
        "<div class='summary-heading'>"
        f"<div class='section-kicker'>{html.escape(summary_label)}</div>"
        f"<h1 class='section-title'>{html.escape(title)}</h1>"
        "</div>"
        f"{page_status}"
        "</div>"
        "<div class='summary-stats'>"
        f"<div class='meta-panel'><div class='meta-panel-label'>Trends</div><div class='meta-panel-value'>{trend_count}</div></div>"
        f"<div class='meta-panel'><div class='meta-panel-label'>Ideas</div><div class='meta-panel-value'>{idea_count}</div></div>"
        f"<div class='meta-panel'><div class='meta-panel-label'>Latest window</div><div class='meta-panel-value'>{html.escape(latest_token)}</div></div>"
        "</div>"
        "</section>"
    )


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

    action_links = [f"<a href='{markdown_href}'>Markdown source</a>"]
    if pdf_href is not None:
        action_links.insert(
            0, f"<a href='{pdf_href}'>PDF</a>"
        )

    meta_parts = [document.granularity.title(), document.period_token]
    if display_instance := _display_site_instance(document.instance):
        meta_parts.append(display_instance)
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
        "<div class='hero-kicker'>Trend</div>"
        f"<h1 class='detail-title'>{html.escape(document.title)}</h1>"
        f"<p class='detail-meta'>{html.escape(' · '.join(meta_parts))}</p>"
        f"<div class='topic-pill-row'>{topic_links}</div>"
        f"<div class='detail-utility'>{' · '.join(action_links)}</div>"
        "</div>"
        "</section>"
        f"<section class='detail-content'>{document.body_html}</section>"
        f"{pager_html}"
    )

    return _render_site_page(
        SitePageShellInput(
            title=f"{document.title} · Recoleta Trends",
            page_path=document.page_path,
            output_dir=output_dir,
            page_heading=document.title,
            page_subtitle="",
            body_class="page-detail",
            active_nav="trends",
            content_html=content_html,
            repo_url=RECOLETA_REPO_URL,
        )
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
        topics=document.topics[:5],
        from_page=document.page_path,
        topic_pages=topic_pages,
    )
    metadata_groups: list[str] = []
    authors = [str(author).strip() for author in document.authors if str(author).strip()]
    if authors:
        authors_html = ", ".join(
            f"<span class='item-author'>{html.escape(author)}</span>"
            for author in authors[:6]
        )
        if len(authors) > 6:
            authors_html += ", <span class='item-author-more'>et al.</span>"
        metadata_groups.append(
            "<div class='item-metadata-group item-metadata-authors'>"
            "<dt>Authors</dt>"
            f"<dd>{authors_html}</dd>"
            "</div>"
        )
    metadata_groups.append(
        "<div class='item-metadata-group item-metadata-fact'>"
        "<dt>Source</dt>"
        f"<dd>{html.escape(_display_item_source(document.source))}</dd>"
        "</div>"
    )
    if document.published_at is not None:
        published_date = (
            document.published_at.astimezone(timezone.utc).date().isoformat()
        )
        published_html = (
            f"<time datetime='{html.escape(published_date, quote=True)}'>"
            f"{html.escape(published_date)}</time>"
        )
    else:
        published_html = "Unknown"
    metadata_groups.append(
        "<div class='item-metadata-group item-metadata-fact'>"
        "<dt>Published</dt>"
        f"<dd>{published_html}</dd>"
        "</div>"
    )
    if display_instance := _display_site_instance(document.instance):
        metadata_groups.append(
            "<div class='item-metadata-group item-metadata-fact'>"
            "<dt>Collection</dt>"
            f"<dd>{html.escape(display_instance)}</dd>"
            "</div>"
        )
    item_metadata_html = (
        "<dl class='detail-meta item-metadata'>"
        f"{''.join(metadata_groups)}"
        "</dl>"
    )
    action_links = [
        f"<a class='action-link secondary' href='{markdown_href}'>Markdown source</a>"
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
        "<div class='hero-kicker'>Source note</div>"
        f"<h1 class='detail-title'>{html.escape(document.title)}</h1>"
        f"{item_metadata_html}"
        f"<div class='topic-pill-row'>{topic_links}</div>"
        f"<div class='card-actions detail-actions'>{''.join(action_links)}</div>"
        "</div>"
        "</section>"
        f"<section class='detail-content'>{document.body_html}</section>"
    )
    return _render_site_page(
        SitePageShellInput(
            title=f"{document.title} · Recoleta",
            page_path=document.page_path,
            output_dir=output_dir,
            page_heading=document.title,
            page_subtitle="",
            body_class="page-item",
            active_nav="archive",
            content_html=content_html,
            repo_url=RECOLETA_REPO_URL,
        )
    )


def _render_idea_card(
    *,
    document: IdeaSiteDocument,
    from_page: Path,
    topic_pages: dict[str, Path],
    include_kind: bool = False,
) -> str:
    idea_href = _site_href(from_page=from_page, to_page=document.page_path)
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
    meta_parts = [document.granularity.title(), document.period_token]
    if include_kind:
        meta_parts.insert(0, "Idea")
    if display_instance := _display_site_instance(document.instance):
        meta_parts.append(display_instance)
    return (
        "<article class='trend-card'>"
        "<div class='card-meta-row'>"
        f"<span class='meta-date'>{html.escape(' · '.join(meta_parts))}</span>"
        "</div>"
        f"<h2 class='card-title'><a href='{idea_href}'>{html.escape(document.title)}</a></h2>"
        f"<p class='card-excerpt'>{html.escape(document.excerpt)}</p>"
        f"{topic_links_html}"
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
    meta_parts = [document.granularity.title(), document.period_token]
    if display_instance := _display_site_instance(document.instance):
        meta_parts.append(display_instance)
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
        "<div class='hero-kicker'>Research idea</div>"
        f"<h1 class='detail-title'>{html.escape(document.title)}</h1>"
        f"<p class='detail-meta'>{html.escape(' · '.join(meta_parts))}</p>"
        f"{topic_links_html}"
        f"<div class='detail-utility'><a href='{markdown_href}'>Markdown source</a></div>"
        "</div>"
        "</section>"
        f"<section class='detail-content'>{document.body_html}</section>"
    )
    return _render_site_page(
        SitePageShellInput(
            title=f"{document.title} · Recoleta Ideas",
            page_path=document.page_path,
            output_dir=output_dir,
            page_heading=document.title,
            page_subtitle="",
            body_class="page-idea",
            active_nav="ideas",
            content_html=content_html,
            repo_url=RECOLETA_REPO_URL,
        )
    )


def _render_trends_index_page(
    *,
    documents: list[TrendSiteDocument],
    total_documents: int,
    output_dir: Path,
    topic_pages: dict[str, Path],
    pagination: SitePagination,
) -> str:
    page_path = pagination.page_path
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
        f"<span class='meta-date'>{html.escape(_paginated_count_text(count_text=_count_label(total_documents, singular='trend'), pagination=pagination))}</span>"
        "</div>"
        f"<div class='trend-grid'>{cards or '<div class="empty-card">No trends available yet.</div>'}</div>"
        f"{_render_collection_pagination(pagination=pagination, collection_label='Trends')}"
        "</section>"
    )
    return _render_site_page(
        SitePageShellInput(
            title=_paginated_document_title(
                title="Trends · Recoleta Trends",
                pagination=pagination,
            ),
            page_path=page_path,
            output_dir=output_dir,
            page_heading="Trends",
            page_subtitle="",
            body_class="page-trends",
            active_nav="trends",
            content_html=content_html,
            repo_url=RECOLETA_REPO_URL,
        )
    )


def _render_ideas_index_page(
    *,
    documents: list[IdeaSiteDocument],
    total_documents: int,
    output_dir: Path,
    topic_pages: dict[str, Path],
    pagination: SitePagination,
) -> str:
    page_path = pagination.page_path
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
        f"<span class='meta-date'>{html.escape(_paginated_count_text(count_text=_count_label(total_documents, singular='idea'), pagination=pagination))}</span>"
        "</div>"
        f"<div class='trend-grid'>{cards or '<div class="empty-card">No ideas available yet.</div>'}</div>"
        f"{_render_collection_pagination(pagination=pagination, collection_label='Ideas')}"
        "</section>"
    )
    return _render_site_page(
        SitePageShellInput(
            title=_paginated_document_title(
                title="Ideas · Recoleta Trends",
                pagination=pagination,
            ),
            page_path=page_path,
            output_dir=output_dir,
            page_heading="Ideas",
            page_subtitle="",
            body_class="page-ideas",
            active_nav="ideas",
            content_html=content_html,
            repo_url=RECOLETA_REPO_URL,
        )
    )


def _home_entry_kind(document: TrendSiteDocument | IdeaSiteDocument) -> str:
    return "Trend" if isinstance(document, TrendSiteDocument) else "Idea"


def _render_home_feature(
    *,
    document: TrendSiteDocument | IdeaSiteDocument,
    page_path: Path,
    topic_pages: dict[str, Path],
) -> str:
    href = _site_href(from_page=page_path, to_page=document.page_path)
    topic_links = (
        _render_topic_link_pills(
            topics=document.topics[:3],
            from_page=page_path,
            topic_pages=topic_pages,
        )
        if document.topics
        else ""
    )
    topic_html = (
        f"<div class='topic-pill-row'>{topic_links}</div>" if topic_links else ""
    )
    return (
        "<article class='home-feature'>"
        "<div class='home-feature-meta'>"
        f"<span>{_home_entry_kind(document)}</span>"
        f"<time>{html.escape(document.period_token)}</time>"
        "</div>"
        f"<h2 class='home-feature-title'><a href='{href}'>{html.escape(document.title)}</a></h2>"
        f"<p class='home-feature-excerpt'>{html.escape(document.excerpt)}</p>"
        f"{topic_html}"
        "</article>"
    )


def _render_home_feed_row(
    *,
    document: TrendSiteDocument | IdeaSiteDocument,
    page_path: Path,
) -> str:
    href = _site_href(from_page=page_path, to_page=document.page_path)
    return (
        "<li class='latest-feed-row'>"
        "<div class='latest-feed-meta'>"
        f"<span>{_home_entry_kind(document)}</span>"
        f"<time>{html.escape(document.period_token)}</time>"
        "</div>"
        f"<h3><a href='{href}'>{html.escape(document.title)}</a></h3>"
        "</li>"
    )


def _render_home_page(
    *,
    documents: list[TrendSiteDocument],
    idea_documents: list[IdeaSiteDocument],
    output_dir: Path,
    topic_pages: dict[str, Path],
) -> str:
    page_path = output_dir / "index.html"
    latest_documents = sorted(
        [*documents, *idea_documents],
        key=_rendered_document_sort_key,
        reverse=True,
    )
    feature_html = (
        _render_home_feature(
            document=latest_documents[0],
            page_path=page_path,
            topic_pages=topic_pages,
        )
        if latest_documents
        else "<p class='empty-card'>No research notes available yet.</p>"
    )
    feed_html = "".join(
        _render_home_feed_row(document=document, page_path=page_path)
        for document in latest_documents[1:13]
    )
    content_html = (
        "<section class='home-intro'>"
        "<h1 class='home-title'>Notes</h1>"
        "<p class='home-dek'>"
        "Evidence-led trends and practical ideas from recent technical work."
        "</p>"
        "<div class='home-primary-links'>"
        f"<a href='{_site_href(from_page=page_path, to_page=output_dir / 'trends' / 'index.html')}'>All trends</a>"
        f"<a href='{_site_href(from_page=page_path, to_page=output_dir / 'ideas' / 'index.html')}'>All ideas</a>"
        f"<a class='action-link-external' href='{html.escape(RECOLETA_QUICKSTART_URL, quote=True)}'>Run Recoleta locally</a>"
        "</div>"
        "</section>"
        "<section class='home-latest' aria-labelledby='latest-heading'>"
        "<div class='section-heading-row'>"
        "<h2 class='section-title' id='latest-heading'>Latest</h2>"
        "</div>"
        f"{feature_html}"
        "</section>"
        "<section class='home-feed' aria-labelledby='recent-heading'>"
        "<div class='section-heading-row'>"
        "<h2 class='section-title' id='recent-heading'>More recent notes</h2>"
        f"<a href='{_site_href(from_page=page_path, to_page=output_dir / 'archive.html')}'>Trend archive</a>"
        "</div>"
        f"<ol class='latest-feed'>{feed_html or '<li class="empty-card">No additional notes yet.</li>'}</ol>"
        "</section>"
    )

    return _render_site_page(
        SitePageShellInput(
            title="Recoleta Trends",
            page_path=page_path,
            output_dir=output_dir,
            page_heading="Recoleta Trends",
            page_subtitle="",
            body_class="page-home",
            active_nav="home",
            content_html=content_html,
            repo_url=RECOLETA_REPO_URL,
        )
    )


def _render_topics_index_page(
    *,
    documents: list[TrendSiteDocument],
    idea_documents: list[IdeaSiteDocument],
    output_dir: Path,
    topic_pages: dict[str, Path],
    pagination: SitePagination,
    page_size: int,
) -> str:
    page_path = pagination.page_path
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

    cards = _render_topic_card_grid(
        request=_TopicCardGridRenderRequest(
            page_path=page_path,
            topic_pages=topic_pages,
            label_by_slug=label_by_slug,
            latest_by_topic=latest_by_topic,
            topic_counter=topic_counter,
            trend_counter=trend_counter,
            idea_counter=idea_counter,
            offset=(pagination.current_page - 1) * page_size,
            limit=page_size,
        )
    )

    content_html = (
        "<section class='home-section'>"
        "<div class='section-heading-row'>"
        "<h1 class='section-title page-section-title'>All tracked topics</h1>"
        f"<span class='meta-date'>{html.escape(_paginated_count_text(count_text=_count_label(len(topic_pages), singular='topic'), pagination=pagination))}</span>"
        "</div>"
        f"<div class='topic-card-grid'>{cards or '<div class="empty-card">No topics available yet.</div>'}</div>"
        f"{_render_collection_pagination(pagination=pagination, collection_label='Topics')}"
        "</section>"
    )

    return _render_site_page(
        SitePageShellInput(
            title=_paginated_document_title(
                title="Topics · Recoleta Trends",
                pagination=pagination,
            ),
            page_path=page_path,
            output_dir=output_dir,
            page_heading="Topics",
            page_subtitle="",
            body_class="page-topics",
            active_nav="topics",
            content_html=content_html,
            repo_url=RECOLETA_REPO_URL,
        )
    )


def _render_topic_page_collections(
    *,
    request: _TopicPageRenderRequest,
    page_path: Path,
) -> str:
    start = (request.pagination.current_page - 1) * request.page_size
    stop = start + request.page_size
    ordered_documents = sorted(
        [*request.documents, *request.idea_documents],
        key=_rendered_document_sort_key,
        reverse=True,
    )
    page_documents = ordered_documents[start:stop]
    cards = "".join(
        _render_trend_card(
            document=document,
            from_page=page_path,
            topic_pages=request.topic_pages,
            include_kind=True,
        )
        if isinstance(document, TrendSiteDocument)
        else _render_idea_card(
            document=document,
            from_page=page_path,
            topic_pages=request.topic_pages,
            include_kind=True,
        )
        for document in page_documents
    )
    latest_token = _latest_collection_token(
        [*request.documents, *request.idea_documents]
    )
    empty_copy = (
        "No research notes for this topic."
        if request.pagination.current_page == 1
        else "No research notes on this page."
    )
    entries_html = cards or f"<div class='empty-card'>{html.escape(empty_copy)}</div>"
    return (
        f"{_render_collection_summary_section(summary_label='Topic summary', title=_display_topic_label(request.topic), trend_count=request.total_documents, idea_count=request.total_idea_documents, latest_token=latest_token, pagination=request.pagination)}"
        "<section class='topic-feed'>"
        f"<div class='trend-grid'>{entries_html}</div>"
        "</section>"
        f"{_render_collection_pagination(pagination=request.pagination, collection_label=f'{request.topic} topic')}"
    )


def _render_topic_page(
    *,
    request: _TopicPageRenderRequest | None = None,
    **legacy_kwargs: Any,
) -> str:
    normalized_request = _coerce_topic_page_render_request(
        request=request,
        legacy_kwargs=legacy_kwargs,
    )
    display_topic = _display_topic_label(normalized_request.topic)
    page_path = normalized_request.pagination.page_path
    content_html = _render_topic_page_collections(
        request=normalized_request,
        page_path=page_path,
    )
    return _render_site_page(
        SitePageShellInput(
            title=_paginated_document_title(
                title=f"{display_topic} · Recoleta Trends",
                pagination=normalized_request.pagination,
            ),
            page_path=page_path,
            output_dir=normalized_request.output_dir,
            page_heading=display_topic,
            page_subtitle="",
            body_class="page-topic",
            active_nav="topics",
            content_html=content_html,
            repo_url=RECOLETA_REPO_URL,
        )
    )


def _render_archive_page(
    *,
    documents: list[TrendSiteDocument],
    total_documents: int,
    output_dir: Path,
    pagination: SitePagination,
) -> str:
    page_path = pagination.page_path
    rows = _render_archive_rows(documents=documents, from_page=page_path)
    content_html = (
        "<section class='home-section'>"
        "<div class='section-heading-row'>"
        "<h1 class='section-title page-section-title'>Archive</h1>"
        f"<span class='meta-date'>{html.escape(_paginated_count_text(count_text=_count_label(total_documents, singular='trend'), pagination=pagination))}</span>"
        "</div>"
        f"{rows or '<div class="empty-card">No archive entries yet.</div>'}"
        f"{_render_collection_pagination(pagination=pagination, collection_label='Archive')}"
        "</section>"
    )
    return _render_site_page(
        SitePageShellInput(
            title=_paginated_document_title(
                title="Archive · Recoleta Trends",
                pagination=pagination,
            ),
            page_path=page_path,
            output_dir=output_dir,
            page_heading="Archive",
            page_subtitle="",
            body_class="page-archive",
            active_nav="archive",
            content_html=content_html,
            repo_url=RECOLETA_REPO_URL,
        )
    )


_SITE_CSS = """
:root {
  --paper: #ffffff;
  --surface: #f5f6f8;
  --surface-hover: #edf2f7;
  --popover: #ffffff;
  --ink: #172033;
  --text: #354052;
  --muted: #5f6875;
  --line: #e2e5ea;
  --line-strong: #c8ced6;
  --control-border: #7c8796;
  --accent: #145da0;
  --accent-dark: #0e477d;
  --on-accent: #ffffff;
  --focus-ring: #4f83bd;
  --disabled-text: #667085;
  --measure: 680px;
}
* {
  box-sizing: border-box;
}
html {
  color-scheme: light;
  background: var(--paper);
}
body {
  min-height: 100%;
  margin: 0;
  overflow-x: hidden;
  background: var(--paper);
  color: var(--ink);
  font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI",
    "PingFang SC", "Hiragino Sans GB", "Noto Sans CJK SC", sans-serif;
  font-size: 16px;
  line-height: 1.62;
  text-rendering: optimizeLegibility;
}
a {
  color: var(--accent);
  text-decoration: underline;
  text-decoration-thickness: 1px;
  text-underline-offset: 0.18em;
}
a:hover {
  color: var(--accent-dark);
}
img,
svg,
video,
iframe {
  max-width: 100%;
  height: auto;
}
.site-shell {
  width: min(1120px, calc(100% - 48px));
  margin: 0 auto;
  padding: 0 0 64px;
}
.site-header {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
  align-items: center;
  gap: 28px;
  min-height: 72px;
  margin-bottom: 28px;
  border-bottom: 1px solid var(--line-strong);
}
.nav-brand-wrap {
  min-width: 0;
}
.nav-brand {
  color: var(--ink);
  font-family: "Songti SC", "STSong", "Noto Serif CJK SC", Georgia, serif;
  font-size: 22px;
  font-weight: 700;
  letter-spacing: -0.015em;
  text-decoration: none;
  white-space: nowrap;
}
.nav-caption {
  color: var(--muted);
  font-size: 13px;
}
.nav-links,
.nav-actions,
.nav-utility-cluster {
  display: flex;
  align-items: center;
}
.nav-links {
  min-width: 0;
  gap: 22px;
}
.nav-actions {
  justify-content: flex-end;
  gap: 16px;
}
.nav-utility-cluster {
  min-width: 0;
}
.nav-utility-cluster:empty {
  display: none;
}
.nav-link {
  display: inline-flex;
  align-items: center;
  min-height: 44px;
  padding: 2px 0 0;
  border-bottom: 2px solid transparent;
  color: var(--text);
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  white-space: nowrap;
}
.nav-link:hover,
.nav-link.is-active {
  border-bottom-color: var(--accent);
  color: var(--accent-dark);
}
.nav-link-external::after,
.action-link-external::after {
  content: "↗";
  margin-left: 0.35em;
  font-size: 0.78em;
}
.nav-link-repo {
  color: var(--muted);
}
.site-main {
  display: grid;
  gap: 36px;
}
.page-hero,
.home-intro {
  padding: 40px 0 34px;
}
.page-hero {
  border-bottom: 1px solid var(--line-strong);
}
.hero-kicker,
.section-kicker,
.section-label,
.idea-opportunity-label,
.idea-meta-pill-label {
  margin: 0 0 8px;
  color: var(--muted);
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.02em;
}
.page-title,
.home-title,
.detail-title,
.section-title,
.card-title,
.topic-card-title,
.home-feature-title,
.detail-content h2,
.detail-content h3 {
  font-family: "Songti SC", "STSong", "Noto Serif CJK SC", Georgia, serif;
}
.page-title,
.home-title,
.detail-title {
  margin: 0;
  color: var(--ink);
  font-size: clamp(38px, 5.2vw, 64px);
  font-weight: 700;
  letter-spacing: -0.035em;
  line-height: 1.08;
}
.home-intro {
  max-width: 820px;
}
.home-title {
  max-width: 17ch;
}
.home-dek {
  max-width: 62ch;
  margin: 22px 0 0;
  color: var(--text);
  font-size: 18px;
  line-height: 1.65;
}
.home-primary-links {
  display: flex;
  flex-wrap: wrap;
  gap: 10px 24px;
  margin-top: 22px;
}
.home-primary-links a {
  font-weight: 650;
}
.home-latest,
.home-feed,
.home-section,
.collection-summary-section,
.archive-block {
  min-width: 0;
}
.section-heading-row {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 18px;
  margin-bottom: 16px;
}
.section-heading-actions {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 12px;
}
.section-title {
  margin: 0;
  color: var(--ink);
  font-size: clamp(26px, 3vw, 34px);
  font-weight: 700;
  letter-spacing: -0.018em;
  line-height: 1.2;
}
.page-section-title {
  font-size: clamp(34px, 4vw, 48px);
}
.meta-date,
.topic-card-meta,
.timeline-item span,
.archive-item span,
.latest-feed-meta,
.home-feature-meta {
  color: var(--muted);
  font-size: 14px;
}
.home-feature {
  padding: clamp(24px, 4vw, 44px);
  border-top: 3px solid var(--ink);
  background: var(--surface);
}
.home-feature-meta {
  display: flex;
  gap: 12px;
}
.home-feature-meta span,
.latest-feed-meta span {
  color: var(--accent-dark);
  font-weight: 700;
}
.home-feature-title {
  max-width: 22ch;
  margin: 12px 0;
  font-size: clamp(32px, 4.6vw, 52px);
  letter-spacing: -0.028em;
  line-height: 1.12;
}
.home-feature-title a,
.card-title a,
.topic-card-title a,
.latest-feed-row h3 a,
.timeline-item a,
.archive-item a,
.pager-card {
  color: inherit;
  text-decoration: none;
}
.home-feature-title a:hover,
.card-title a:hover,
.topic-card-title a:hover,
.latest-feed-row h3 a:hover,
.timeline-item a:hover,
.archive-item a:hover,
.pager-card:hover {
  color: var(--accent-dark);
}
.home-feature-excerpt {
  max-width: 68ch;
  margin: 0;
  color: var(--text);
  font-size: 18px;
  line-height: 1.68;
}
.latest-feed,
.timeline-list,
.archive-list,
.source-list {
  margin: 0;
  padding: 0;
  list-style: none;
}
.latest-feed {
  border-top: 1px solid var(--line-strong);
}
.latest-feed-row {
  display: grid;
  grid-template-columns: 150px minmax(0, 1fr);
  gap: 24px;
  align-items: baseline;
  padding: 18px 0;
  border-bottom: 1px solid var(--line);
}
.latest-feed-meta {
  display: flex;
  justify-content: space-between;
  gap: 8px;
}
.latest-feed-row h3 {
  margin: 0;
  font-family: "Songti SC", "STSong", "Noto Serif CJK SC", Georgia, serif;
  font-size: 22px;
  line-height: 1.32;
}
.trend-grid {
  display: grid;
  grid-template-columns: 1fr;
}
.trend-card {
  min-width: 0;
  padding: 24px 0;
  border-top: 1px solid var(--line);
}
.trend-card:first-child {
  border-top-color: var(--line-strong);
}
.card-meta-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}
.card-title,
.topic-card-title {
  margin: 8px 0;
  color: var(--ink);
  font-size: 28px;
  letter-spacing: -0.018em;
  line-height: 1.22;
}
.card-excerpt {
  max-width: 72ch;
  margin: 0;
  color: var(--text);
  font-size: 16px;
  line-height: 1.68;
}
.topic-pill-row {
  display: flex;
  flex-wrap: wrap;
  gap: 5px 16px;
  margin-top: 12px;
}
.topic-pill,
.meta-pill {
  display: inline;
  padding: 0;
  border: 0;
  background: transparent;
  color: var(--muted);
  font-size: 13px;
  line-height: 1.5;
}
.topic-pill-link {
  color: var(--accent);
  text-decoration: underline;
}
.meta-pill.subdued {
  color: var(--muted);
}
.topic-card-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  border-top: 1px solid var(--line-strong);
  border-left: 1px solid var(--line);
}
.topic-card {
  min-width: 0;
  padding: 20px;
  border-right: 1px solid var(--line);
  border-bottom: 1px solid var(--line);
  background: transparent;
}
.topic-card-title {
  margin-top: 0;
  font-size: 22px;
}
.collection-summary-section {
  padding-bottom: 24px;
  border-bottom: 1px solid var(--line-strong);
}
.summary-heading {
  min-width: 0;
}
.summary-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 12px 28px;
}
.meta-panel {
  display: flex;
  gap: 8px;
  padding: 0;
}
.meta-panel-label,
.meta-panel-value {
  font-size: 14px;
  line-height: 1.5;
}
.meta-panel-label {
  color: var(--muted);
}
.meta-panel-value {
  color: var(--ink);
  font-weight: 650;
}
.empty-card {
  padding: 20px 0;
  border-top: 1px solid var(--line);
  color: var(--muted);
}
.action-link,
.pagination-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 44px;
  color: var(--accent);
  font-size: 14px;
  font-weight: 650;
}
.action-link {
  padding: 0;
  background: transparent;
  text-decoration: underline;
}
.card-actions,
.hero-actions,
.detail-actions,
.detail-utility {
  display: flex;
  flex-wrap: wrap;
  gap: 10px 18px;
}
.detail-actions,
.detail-utility {
  margin-top: 14px;
}
.breadcrumbs,
.detail-hero,
.detail-content,
.pager-row {
  width: min(var(--measure), 100%);
  margin-inline: auto;
}
.breadcrumbs {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
  align-items: center;
  margin-bottom: -18px;
  color: var(--muted);
  font-size: 13px;
}
.detail-hero {
  padding: 18px 0 28px;
  border-bottom: 1px solid var(--line-strong);
}
.detail-hero-main {
  min-width: 0;
}
.detail-title {
  max-width: 24ch;
  font-size: clamp(38px, 5vw, 58px);
}
.detail-meta {
  margin: 16px 0 0;
  color: var(--muted);
  font-size: 14px;
}
.item-metadata {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 8px 24px;
  max-width: 100%;
}
.item-metadata-group {
  display: grid;
  grid-template-columns: max-content minmax(0, 1fr);
  gap: 0 7px;
  align-items: baseline;
  min-width: 0;
}
.item-metadata-authors {
  flex: 1 0 100%;
  max-width: 100%;
}
.item-metadata dt,
.item-metadata dd {
  margin: 0;
}
.item-metadata dt {
  color: var(--muted);
  font-size: 13px;
  font-weight: 700;
  line-height: 1.5;
}
.item-metadata dd {
  min-width: 0;
  color: var(--text);
  font-size: 14px;
  line-height: 1.55;
}
.item-metadata-fact dd,
.item-author,
.item-author-more {
  white-space: nowrap;
}
.item-author {
  display: inline-block;
}
.item-author-more {
  color: var(--muted);
}
.detail-content {
  min-width: 0;
  color: var(--text);
}
.detail-content .document-flow {
  padding: 0;
}
.detail-content .summary-grid,
.detail-content .idea-opportunity-grid,
.detail-content .cluster-columns {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 0;
}
.detail-content .surface-card,
.detail-content .idea-opportunity-card,
.detail-content .cluster-card {
  display: block;
  width: 100%;
  margin: 0;
  padding: 30px 0;
  border: 0;
  border-bottom: 1px solid var(--line);
  background: transparent;
}
.detail-content .document-flow > .surface-card:last-child,
.detail-content .document-flow > .summary-grid:last-child > .surface-card:last-child,
.detail-content .cluster-columns > .cluster-card:last-child,
.detail-content .idea-opportunity-grid > .idea-opportunity-card:last-child {
  border-bottom: 0;
}
.detail-content .summary-grid .surface-card:first-child,
.detail-content > .document-flow > .surface-card:first-child {
  padding-top: 0;
}
.detail-content .idea-section-head {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 8px;
}
.detail-content .idea-opportunities-section {
  padding-bottom: 0;
}
.detail-content .idea-opportunity-grid {
  border-top: 0;
}
.detail-content .idea-opportunity-card {
  align-self: start;
}
.detail-content .idea-opportunity-head,
.detail-content .idea-opportunity-body,
.detail-content .idea-opportunity-block {
  display: grid;
  gap: 10px;
}
.detail-content .idea-opportunity-title,
.detail-content .prose h3,
.detail-content .cluster-card h3 {
  margin: 0 0 12px;
  color: var(--ink);
  font-size: 27px;
  letter-spacing: -0.012em;
  line-height: 1.24;
}
.detail-content .idea-opportunity-meta-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 18px;
}
.detail-content .idea-meta-pill,
.detail-content .idea-opportunity-block-role {
  padding: 0;
  border: 0;
  background: transparent;
}
.detail-content .idea-meta-pill-separator {
  margin: 0 5px;
  color: var(--line-strong);
}
.detail-content .idea-opportunity-block-evidence {
  padding-top: 14px;
  border-top: 1px solid var(--line);
}
.detail-content .idea-opportunity-role-value,
.detail-content .idea-opportunity-copy,
.detail-content .prose,
.detail-content .cluster-body {
  color: var(--text);
  font-size: 16px;
  line-height: 1.7;
}
.detail-content .prose p,
.detail-content .cluster-body p,
.detail-content .idea-opportunity-copy p {
  margin: 0 0 1em;
}
.detail-content .prose h4,
.detail-content .cluster-body h4 {
  margin: 24px 0 8px;
  color: var(--text);
  font-size: 16px;
  line-height: 1.4;
}
.detail-content .prose ul,
.detail-content .prose ol,
.detail-content .cluster-body ul,
.detail-content .cluster-body ol,
.detail-content .idea-opportunity-copy ul,
.detail-content .idea-opportunity-copy ol {
  margin: 10px 0 18px;
  padding-inline-start: 1.4em;
}
.detail-content li {
  margin-bottom: 8px;
}
.detail-content .prose blockquote,
.detail-content .cluster-body blockquote {
  margin: 20px 0;
  padding: 2px 0 2px 18px;
  border-left: 3px solid var(--accent);
  color: var(--text);
}
.detail-content .prose table,
.detail-content .cluster-body table {
  display: block;
  width: 100%;
  max-width: 100%;
  margin: 18px 0;
  overflow-x: auto;
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
  padding: 9px 10px;
  border: 1px solid var(--line);
  text-align: left;
  vertical-align: top;
}
.detail-content .prose th,
.detail-content .cluster-body th {
  background: var(--surface);
}
.detail-content .topic-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 18px;
}
.detail-source-list .source-list {
  padding-left: 1.4em;
  list-style: decimal;
}
.source-list-item {
  margin-bottom: 14px;
  padding-left: 4px;
}
.source-list-title a {
  font-weight: 650;
}
.source-list-meta {
  margin-top: 3px;
  color: var(--muted);
  font-size: 13px;
}
.pager-row {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 28px;
  padding-top: 8px;
  border-top: 1px solid var(--line-strong);
}
.pager-card {
  display: block;
  padding: 18px 0;
}
.pager-card span {
  display: block;
  margin-bottom: 5px;
  color: var(--muted);
  font-size: 13px;
}
.pager-card strong {
  font-size: 18px;
  line-height: 1.4;
}
.timeline-list,
.archive-list {
  display: grid;
}
.timeline-item,
.archive-item {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 20px;
  padding: 15px 0;
  border-top: 1px solid var(--line);
}
.archive-block + .archive-block {
  margin-top: 36px;
}
.collection-pagination {
  display: grid;
  grid-template-columns: minmax(96px, 1fr) auto minmax(96px, 1fr);
  align-items: center;
  gap: 12px;
  margin-top: 26px;
  padding-top: 20px;
  border-top: 1px solid var(--line-strong);
}
.pagination-center,
.pagination-pages {
  display: flex;
  align-items: center;
  justify-content: center;
}
.pagination-pages {
  gap: 5px;
}
.pagination-link,
.pagination-ellipsis,
.pagination-status {
  min-width: 42px;
  min-height: 44px;
  padding: 0 10px;
}
.pagination-link {
  border: 1px solid var(--control-border);
  background: var(--surface);
  text-decoration: none;
}
.pagination-link:hover,
.pagination-link.is-current {
  border-color: var(--accent);
}
.pagination-link.is-current {
  background: var(--accent);
  color: var(--on-accent);
}
.pagination-link.is-disabled {
  border-color: var(--line);
  background: transparent;
  color: var(--disabled-text);
}
.pagination-direction {
  min-width: 96px;
}
.pagination-previous {
  justify-self: start;
}
.pagination-next {
  justify-self: end;
}
.pagination-ellipsis {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: var(--muted);
}
.pagination-status {
  display: none;
  align-items: center;
  justify-content: center;
  color: var(--muted);
  white-space: nowrap;
}
.nav-brand:focus-visible,
.nav-link:focus-visible,
.action-link:focus-visible,
.topic-pill-link:focus-visible,
.pager-card:focus-visible,
.pagination-link:focus-visible,
.breadcrumbs a:focus-visible,
.language-switcher-link:focus-visible {
  outline: 3px solid var(--focus-ring);
  outline-offset: 3px;
}
:lang(zh) .page-title,
:lang(zh) .home-title,
:lang(zh) .detail-title,
:lang(zh) .section-title,
:lang(zh) .card-title,
:lang(zh) .topic-card-title,
:lang(zh) .home-feature-title,
:lang(ja) .page-title,
:lang(ja) .home-title,
:lang(ja) .detail-title,
:lang(ja) .section-title,
:lang(ja) .card-title,
:lang(ja) .topic-card-title,
:lang(ja) .home-feature-title,
:lang(ko) .page-title,
:lang(ko) .home-title,
:lang(ko) .detail-title,
:lang(ko) .section-title,
:lang(ko) .card-title,
:lang(ko) .topic-card-title,
:lang(ko) .home-feature-title {
  letter-spacing: 0;
  line-height: 1.25;
}
@media (max-width: 900px) {
  .site-shell {
    width: min(100% - 32px, 820px);
  }
  .site-header {
    grid-template-columns: 1fr auto;
    gap: 0 20px;
    min-height: 0;
    padding: 14px 0 10px;
  }
  .nav-links {
    grid-column: 1 / -1;
    grid-row: 2;
    gap: 20px;
    overflow-x: auto;
    padding-top: 5px;
    scrollbar-width: none;
  }
  .nav-links::-webkit-scrollbar {
    display: none;
  }
  .nav-actions {
    grid-column: 2;
    grid-row: 1;
  }
  .nav-brand-wrap {
    grid-column: 1;
    grid-row: 1;
  }
  .topic-card-grid {
    grid-template-columns: 1fr;
  }
  .topic-card-grid {
    border-left: 0;
  }
  .topic-card {
    padding-inline: 0;
    border-right: 0;
  }
}
@media (max-width: 600px) {
  .site-shell {
    width: calc(100% - 28px);
    padding-bottom: 44px;
  }
  .site-header {
    margin-bottom: 16px;
  }
  .nav-brand {
    font-size: 20px;
  }
  .nav-links {
    gap: 18px;
  }
  .nav-link {
    font-size: 13px;
  }
  .nav-link-repo {
    min-height: 40px;
    font-size: 13px;
  }
  .site-main {
    gap: 28px;
  }
  .home-intro,
  .page-hero {
    padding: 24px 0 26px;
  }
  .page-title,
  .home-title {
    font-size: clamp(34px, 11vw, 46px);
  }
  .detail-title {
    max-width: none;
    font-size: clamp(1.75rem, 7.5vw, 2rem);
    letter-spacing: -0.015em;
    line-height: 1.16;
  }
  :lang(zh) .detail-title,
  :lang(ja) .detail-title,
  :lang(ko) .detail-title {
    letter-spacing: 0;
    line-height: 1.22;
  }
  .home-dek,
  .home-feature-excerpt {
    font-size: 16px;
  }
  .home-feature {
    padding: 22px 18px;
  }
  .home-feature-title {
    font-size: 32px;
  }
  .section-heading-row {
    align-items: start;
  }
  .collection-summary-section .section-heading-row {
    flex-direction: column;
    gap: 8px;
  }
  .latest-feed-row {
    grid-template-columns: 1fr;
    gap: 5px;
    padding: 16px 0;
  }
  .latest-feed-meta {
    justify-content: flex-start;
    gap: 12px;
  }
  .card-title {
    font-size: 25px;
  }
  .breadcrumbs {
    margin-bottom: -12px;
  }
  .detail-hero {
    margin-bottom: -8px;
    padding: 8px 0 16px;
  }
  .detail-hero .hero-kicker {
    margin-bottom: 6px;
  }
  .detail-meta {
    margin-top: 10px;
    font-size: 13px;
    line-height: 1.55;
  }
  .item-metadata {
    gap: 7px 18px;
  }
  .item-metadata-group {
    gap: 0 6px;
  }
  .item-metadata-authors {
    margin-bottom: 1px;
  }
  .detail-hero .topic-pill-row,
  .detail-actions,
  .detail-utility {
    margin-top: 10px;
  }
  .detail-content .surface-card,
  .detail-content .idea-opportunity-card,
  .detail-content .cluster-card {
    padding: 24px 0;
  }
  .pager-row {
    grid-template-columns: 1fr;
    gap: 8px;
  }
  .timeline-item,
  .archive-item {
    grid-template-columns: 1fr;
    gap: 4px;
  }
  .collection-pagination {
    grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr);
    gap: 8px;
  }
  .pagination-pages {
    display: none;
  }
  .pagination-status {
    display: inline-flex;
    padding: 0 4px;
  }
  .pagination-direction {
    min-width: 0;
    padding-inline: 10px;
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
                    presentation=_load_presentation_for_site(
                        markdown_path=markdown_path,
                        surface_kind="trend",
                    ),
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
        source_key
        for source_key in available_source_keys
        if source_key[0] == target_path
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
    return _load_item_source_documents_impl(
        input_dirs=list(input_dirs),
        allowed_source_keys=allowed_source_keys,
        deps=SiteItemSourceLoadDeps(
            split_yaml_frontmatter_text=_split_yaml_frontmatter_text,
            extract_markdown_h1=_extract_markdown_h1,
            parse_site_datetime=_parse_site_datetime,
            parse_site_string_list=_parse_site_string_list,
            resolve_site_instance=_resolve_site_instance,
            site_source_key=_site_source_key,
        ),
    )


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
                    presentation=_load_presentation_for_site(
                        markdown_path=markdown_path,
                        surface_kind="idea",
                    ),
                    granularity=granularity,
                    period_start=period_start,
                    period_end=period_end,
                    topics=_parse_site_string_list(frontmatter.get("topics")),
                    instance=_resolve_site_instance(
                        input_instance=input_info.instance,
                        frontmatter=frontmatter,
                    ),
                    status=str(frontmatter.get("status") or "").strip().lower()
                    or "unknown",
                )
            )

    source_documents.sort(key=_idea_site_sort_key, reverse=True)
    return source_documents[:limit] if limit is not None else source_documents


def _presentation_local_markdown_targets(
    *,
    presentation: dict[str, Any],
    source_markdown_path: Path,
) -> set[Path]:
    markdown = MarkdownIt("commonmark", {"html": True, "typographer": True})
    candidate_paths: set[Path] = set()
    content = presentation.get("content")
    if not isinstance(content, dict):
        return candidate_paths
    _append_presentation_markdown_targets(
        candidate_paths=candidate_paths,
        markdown=markdown,
        source_markdown_path=source_markdown_path,
        value=content.get("overview"),
    )
    _append_presentation_markdown_targets(
        candidate_paths=candidate_paths,
        markdown=markdown,
        source_markdown_path=source_markdown_path,
        value=content.get("summary"),
    )
    _append_cluster_targets(
        candidate_paths=candidate_paths,
        markdown=markdown,
        source_markdown_path=source_markdown_path,
        clusters=list(content.get("clusters") or []),
    )
    _append_idea_targets(
        candidate_paths=candidate_paths,
        markdown=markdown,
        source_markdown_path=source_markdown_path,
        ideas=list(content.get("ideas") or []),
    )
    return candidate_paths


def _append_presentation_markdown_targets(
    *,
    candidate_paths: set[Path],
    markdown: MarkdownIt,
    source_markdown_path: Path,
    value: Any,
) -> None:
    normalized = str(value or "").strip()
    if not normalized:
        return
    rendered_html = markdown.render(normalized)
    soup = BeautifulSoup(rendered_html, "html.parser")
    for anchor in soup.find_all("a", href=True):
        _append_presentation_href_target(
            candidate_paths=candidate_paths,
            source_markdown_path=source_markdown_path,
            href=str(anchor.get("href") or ""),
        )


def _append_presentation_href_target(
    *,
    candidate_paths: set[Path],
    source_markdown_path: Path,
    href: Any,
) -> None:
    target_path = _resolve_site_local_markdown_target(
        source_markdown_path=source_markdown_path,
        href=str(href or ""),
    )
    if target_path is not None:
        candidate_paths.add(target_path)


def _append_source_entry_targets(
    *,
    candidate_paths: set[Path],
    source_markdown_path: Path,
    entries: Sequence[Any],
) -> None:
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        _append_presentation_href_target(
            candidate_paths=candidate_paths,
            source_markdown_path=source_markdown_path,
            href=entry.get("href"),
        )


def _append_cluster_targets(
    *,
    candidate_paths: set[Path],
    markdown: MarkdownIt,
    source_markdown_path: Path,
    clusters: Sequence[Any],
) -> None:
    for cluster in clusters:
        if not isinstance(cluster, dict):
            continue
        _append_presentation_markdown_targets(
            candidate_paths=candidate_paths,
            markdown=markdown,
            source_markdown_path=source_markdown_path,
            value=cluster.get("content"),
        )
        _append_source_entry_targets(
            candidate_paths=candidate_paths,
            source_markdown_path=source_markdown_path,
            entries=list(cluster.get("evidence") or []),
        )


def _append_idea_targets(
    *,
    candidate_paths: set[Path],
    markdown: MarkdownIt,
    source_markdown_path: Path,
    ideas: Sequence[Any],
) -> None:
    for idea in ideas:
        if not isinstance(idea, dict):
            continue
        _append_presentation_markdown_targets(
            candidate_paths=candidate_paths,
            markdown=markdown,
            source_markdown_path=source_markdown_path,
            value=idea.get("content"),
        )
        _append_source_entry_targets(
            candidate_paths=candidate_paths,
            source_markdown_path=source_markdown_path,
            entries=list(idea.get("evidence") or []),
        )


def _collect_referenced_item_source_keys(
    *,
    source_documents: Sequence[TrendSiteSourceDocument | IdeaSiteSourceDocument],
    available_source_keys: set[SiteSourceKey],
) -> set[SiteSourceKey]:
    return _collect_referenced_item_source_keys_impl(
        source_documents=list(source_documents),
        available_source_keys=available_source_keys,
        deps=SiteReferenceCollectionDeps(
            presentation_local_markdown_targets=_presentation_local_markdown_targets,
            resolve_site_source_key=_resolve_site_source_key,
            resolve_site_local_markdown_target=_resolve_site_local_markdown_target,
        ),
    )


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
    return _build_item_browser_body_html_impl(
        body_html=body_html,
        extract_trend_pdf_sections=_extract_trend_pdf_sections,
        build_trend_browser_body_html=_build_trend_browser_body_html,
    )


def _idea_heading_matches(heading: str, *labels: str) -> bool:
    normalized = str(heading or "").strip().lower()
    if not normalized:
        return False
    return any(label in normalized for label in labels)


def _build_idea_browser_body_html(*, body_html: str) -> IdeaBodyRenderResult:
    return _build_idea_browser_body_html_impl(
        body_html=body_html,
        deps=IdeaBrowserBodyDeps(
            extract_trend_pdf_sections=_extract_trend_pdf_sections,
            build_item_browser_body_html=_build_item_browser_body_html,
            idea_heading_matches=_idea_heading_matches,
            render_browser_content_card_html=_render_browser_content_card_html,
        ),
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


def _render_presentation_markdown_html(markdown_text: Any) -> str:
    normalized = str(markdown_text or "").strip()
    if not normalized:
        return "<p>(none)</p>"
    return MarkdownIt("commonmark", {"html": True, "typographer": True}).render(
        normalized
    )


def _render_presentation_source_list(
    *,
    entries: Sequence[dict[str, Any]],
    labels: dict[str, str],
) -> str:
    return _render_presentation_source_list_impl(
        entries=[entry for entry in entries if isinstance(entry, dict)],
        labels=labels,
        humanize_source_type=_humanize_source_type,
        humanize_confidence=_humanize_confidence,
    )


def _presentation_content(presentation: dict[str, Any]) -> dict[str, Any]:
    content = (
        presentation.get("content")
        if isinstance(presentation.get("content"), dict)
        else {}
    )
    assert isinstance(content, dict)
    return content


def _trend_cluster_cards(
    *,
    clusters: Sequence[dict[str, Any]],
    labels: dict[str, str],
) -> list[str]:
    cards: list[str] = []
    for cluster in clusters:
        evidence_entries = [
            entry
            for entry in list(cluster.get("evidence") or [])
            if isinstance(entry, dict)
        ]
        evidence_html = _render_presentation_source_list(
            entries=evidence_entries,
            labels=labels,
        )
        evidence_section = ""
        if evidence_html:
            evidence_section = (
                f"<h4 class='section-label'>{html.escape(labels['evidence'])}</h4>"
                f"<div class='prose detail-source-list'>{evidence_html}</div>"
            )
        cards.append(
            "<article class='surface-card section-card cluster-card'>"
            f"<h3 class='section-title'>{html.escape(str(cluster.get('title') or 'Cluster').strip())}</h3>"
            f"<div class='prose'>{_render_presentation_markdown_html(cluster.get('content'))}</div>"
            f"{evidence_section}"
            "</article>"
        )
    return cards


def _trend_cluster_section(
    *,
    clusters: Sequence[dict[str, Any]],
    labels: dict[str, str],
) -> str | None:
    if not clusters:
        return None
    cluster_cards = _trend_cluster_cards(clusters=clusters, labels=labels)
    return (
        "<section class='surface-card section-card'>"
        f"{_render_browser_section_label_html(labels['clusters'])}"
        f"<div class='cluster-columns'>{''.join(cluster_cards)}</div>"
        "</section>"
    )


def _build_trend_body_from_presentation(
    *,
    presentation: dict[str, Any],
) -> tuple[str, str]:
    labels = _presentation_labels(surface_kind="trend", presentation=presentation)
    content = _presentation_content(presentation)
    rendered_sections: list[str] = []

    overview_html = _render_presentation_markdown_html(content.get("overview"))
    rendered_sections.append(
        _render_browser_content_card_html(
            heading=labels["overview"],
            inner_html=overview_html,
        )
    )

    clusters = [
        cluster
        for cluster in list(content.get("clusters") or [])
        if isinstance(cluster, dict)
    ]
    if cluster_section := _trend_cluster_section(clusters=clusters, labels=labels):
        rendered_sections.append(cluster_section)

    excerpt = _safe_excerpt(
        BeautifulSoup(overview_html, "html.parser").get_text(" ", strip=True),
        limit=220,
    )
    return (
        "<div class='document-flow'>" + "".join(rendered_sections) + "</div>",
        excerpt,
    )


def _build_idea_body_from_presentation(
    *,
    presentation: dict[str, Any],
) -> IdeaBodyRenderResult:
    labels = _presentation_labels(surface_kind="idea", presentation=presentation)
    content = (
        presentation.get("content")
        if isinstance(presentation.get("content"), dict)
        else {}
    )
    assert isinstance(content, dict)
    summary_html = _render_presentation_markdown_html(content.get("summary"))
    ideas = [
        idea for idea in list(content.get("ideas") or []) if isinstance(idea, dict)
    ]
    cards: list[str] = []
    evidence_count = 0
    for idea in ideas:
        evidence_entries = [
            entry
            for entry in list(idea.get("evidence") or [])
            if isinstance(entry, dict)
        ]
        evidence_count += len(evidence_entries)
        evidence_html = _render_presentation_source_list(
            entries=evidence_entries,
            labels=labels,
        )
        evidence_section = ""
        if evidence_html:
            evidence_section = (
                f"<h4 class='section-label'>{html.escape(labels['evidence'])}</h4>"
                f"<div class='prose detail-source-list'>{evidence_html}</div>"
            )
        cards.append(
            "<article class='idea-opportunity-card'>"
            "<div class='idea-opportunity-head'>"
            f"<h3 class='idea-opportunity-title'>{html.escape(str(idea.get('title') or 'Idea').strip())}</h3>"
            "</div>"
            "<div class='idea-opportunity-body'>"
            f"<div class='prose'>{_render_presentation_markdown_html(idea.get('content'))}</div>"
            f"{evidence_section}"
            "</div>"
            "</article>"
        )
    rendered: list[str] = [
        "<section class='summary-grid summary-grid-single'>"
        + _render_browser_content_card_html(
            heading=labels["summary"],
            inner_html=summary_html,
            card_classes="surface-card section-card summary-card summary-card-primary",
        )
        + "</section>"
    ]
    if cards:
        count_label = f"{len(cards)} idea" if len(cards) == 1 else f"{len(cards)} ideas"
        rendered.append(
            "<section class='surface-card section-card idea-opportunities-section'>"
            "<div class='idea-section-head'>"
            f"{_render_browser_section_label_html(labels['ideas'])}"
            f"<span class='meta-date'>{html.escape(count_label)}</span>"
            "</div>"
            f"<div class='idea-opportunity-grid'>{''.join(cards)}</div>"
            "</section>"
        )
    return IdeaBodyRenderResult(
        body_html="<div class='document-flow'>" + "".join(rendered) + "</div>",
        opportunity_count=len(cards),
        evidence_count=evidence_count,
    )


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
        source_key = _site_source_key(
            markdown_path=source_document.markdown_path,
            instance=source_document.instance,
        )
        page_path = page_by_source_key[source_key]
        if source_document.presentation is not None:
            content = source_document.presentation.get("content")
            title = (
                str(content.get("title") or "").strip()
                if isinstance(content, dict)
                else ""
            ) or source_document.markdown_path.stem
            excerpt = _safe_excerpt(
                BeautifulSoup(
                    _render_presentation_markdown_html(
                        content.get("summary") if isinstance(content, dict) else ""
                    ),
                    "html.parser",
                ).get_text(" ", strip=True),
                limit=220,
            )
            idea_body = _build_idea_body_from_presentation(
                presentation=source_document.presentation,
            )
        else:
            normalized_markdown = source_document.markdown_body.strip() or "# Ideas\n"
            rendered_html = markdown.render(normalized_markdown)
            title, raw_body_html, excerpt = _extract_item_body_html(
                body_html=rendered_html
            )
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
    return _load_trend_site_documents_impl(
        source_documents=list(source_documents),
        output_dir=output_dir,
        item_pages_by_source_key=item_pages_by_source_key,
        deps=TrendSiteDocumentLoadDeps(
            site_source_key=_site_source_key,
            site_namespaced_page_stem=_site_namespaced_page_stem,
            normalize_obsidian_callouts_for_pdf=_normalize_obsidian_callouts_for_pdf,
            extract_trend_pdf_sections=_extract_trend_pdf_sections,
            sanitize_trend_title=sanitize_trend_title,
            section_excerpt=_section_excerpt,
            build_trend_body_from_presentation=_build_trend_body_from_presentation,
            rewrite_site_markdown_links=_rewrite_site_markdown_links,
            build_trend_browser_body_html=_build_trend_browser_body_html,
            trend_date_token=_trend_date_token,
            site_namespaced_asset_name=_site_namespaced_asset_name,
        ),
    )


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
    return _discover_site_language_inputs_impl(
        list(raw_inputs),
        deps=SiteLanguageDiscoveryDeps(
            normalize_site_instance=_normalize_site_instance,
            infer_instance_name_from_site_root=_infer_instance_name_from_site_root,
            infer_site_language_code_from_root=_infer_site_language_code_from_root,
            language_slug_from_code=language_slug_from_code,
            reject_legacy_stream_layout=_reject_legacy_stream_layout,
        ),
    )


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
  position: relative;
  display: inline-flex;
  align-items: center;
}
.language-switcher-link,
.language-switcher-trigger {
  display: inline-flex;
  align-items: center;
  min-height: 44px;
  color: var(--text);
  font-size: 13px;
  font-weight: 650;
  line-height: 1;
  white-space: nowrap;
}
.language-switcher-link {
  justify-content: center;
  min-width: 44px;
  max-width: min(11rem, 35vw);
  padding: 0 2px;
  text-decoration: underline;
  text-decoration-thickness: 1px;
  text-underline-offset: 0.2em;
}
.language-switcher-link > span,
.language-switcher-trigger > span {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
}
.language-switcher-link:hover {
  color: var(--accent-dark);
}
.language-switcher-trigger:hover,
.language-switcher-menu[open] .language-switcher-trigger {
  border-color: var(--accent);
  background: var(--popover);
  color: var(--accent-dark);
}
.language-switcher-menu {
  position: relative;
}
.language-switcher-trigger {
  gap: 9px;
  max-width: min(14rem, 40vw);
  padding: 0 10px;
  border: 1px solid var(--control-border);
  border-radius: 3px;
  background: transparent;
  cursor: pointer;
  list-style: none;
}
.language-switcher-trigger::-webkit-details-marker {
  display: none;
}
.language-switcher-trigger::after {
  width: 6px;
  height: 6px;
  border-right: 1.5px solid currentcolor;
  border-bottom: 1.5px solid currentcolor;
  content: "";
  transform: rotate(45deg) translateY(-2px);
  transform-origin: center;
}
.language-switcher-menu[open] .language-switcher-trigger::after {
  transform: rotate(225deg) translate(-1px, -1px);
}
.language-switcher-list {
  position: absolute;
  z-index: 20;
  top: calc(100% + 6px);
  right: 0;
  width: max-content;
  min-width: 190px;
  max-height: calc(100vh - 120px);
  margin: 0;
  padding: 6px 0;
  overflow-y: auto;
  border: 1px solid var(--control-border);
  background: var(--popover);
  list-style: none;
}
.language-switcher-option {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  min-height: 44px;
  padding: 8px 12px;
  color: var(--text);
  font-size: 14px;
  line-height: 1.35;
  text-decoration: none;
}
.language-switcher-option:hover {
  background: var(--surface-hover);
  color: var(--accent-dark);
}
.language-switcher-option.is-active {
  color: var(--ink);
  font-weight: 700;
}
.language-switcher-check {
  color: var(--accent);
  font-size: 15px;
}
.language-switcher-trigger:focus-visible,
.language-switcher-option:focus-visible {
  outline: 3px solid var(--focus-ring);
  outline-offset: 3px;
}
@media (max-width: 600px) {
  .language-switcher-trigger {
    padding-inline: 8px;
  }
  .language-switcher-list {
    min-width: 180px;
    max-width: calc(100vw - 28px);
  }
}
"""

_SITE_CHROME_TRANSLATIONS: dict[str, dict[str, str]] = {
    "zh-CN": {
        "Language": "语言",
        "Home": "首页",
        "Trends": "趋势",
        "Ideas": "想法",
        "Topic": "主题",
        "Topics": "主题",
        "Archive": "归档",
        "Notes": "笔记",
        "Evidence-led trends and practical ideas from recent technical work.": "从近期技术资料中整理趋势与可执行的研究想法。",
        "All trends": "全部趋势",
        "All ideas": "全部想法",
        "Run Recoleta locally": "在本地运行 Recoleta",
        "Latest": "最新",
        "More recent notes": "更多近期内容",
        "Full archive": "完整归档",
        "Trend archive": "趋势归档",
        "Trend": "趋势",
        "Idea": "想法",
        "Item": "条目",
        "Research idea": "研究想法",
        "Summary": "摘要",
        "Note": "笔记",
        "Source note": "来源笔记",
        "Markdown source": "Markdown 源文件",
        "Source": "来源",
        "Published": "发布日期",
        "Collection": "栏目",
        "Relevance": "相关度",
        "Authors": "作者",
        "Unknown": "未知",
        "Open original": "打开原文",
        "Open arXiv": "打开 arXiv",
        "Open OpenReview": "打开 OpenReview",
        "Open GitHub": "打开 GitHub",
        "Newer": "较新",
        "Older": "较早",
        "Previous": "上一页",
        "Next": "下一页",
        "All tracked topics": "全部主题",
        "Topic summary": "主题概况",
        "Latest window": "最近一期",
        "Browse trends": "浏览趋势",
        "Browse ideas": "浏览想法",
        "No research notes available yet.": "暂无研究笔记。",
        "No additional notes yet.": "暂无其他内容。",
        "No trends available yet.": "暂无趋势。",
        "No trends on this page.": "本页没有趋势。",
        "No ideas available yet.": "暂无想法。",
        "No ideas on this page.": "本页没有想法。",
        "No topics available yet.": "暂无主题。",
        "No archive entries yet.": "暂无归档内容。",
        "No research notes for this topic.": "该主题暂无研究笔记。",
        "No research notes on this page.": "本页没有研究笔记。",
        "No tracked topics": "暂无主题",
        "Window": "时间",
        "Granularity": "周期",
        "Instance": "栏目",
        "Coverage": "覆盖范围",
    },
    "zh-TW": {
        "Language": "語言",
        "Home": "首頁",
        "Trends": "趨勢",
        "Ideas": "想法",
        "Topic": "主題",
        "Topics": "主題",
        "Archive": "歸檔",
        "Notes": "筆記",
        "Evidence-led trends and practical ideas from recent technical work.": "從近期技術資料中整理趨勢與可執行的研究想法。",
        "All trends": "全部趨勢",
        "All ideas": "全部想法",
        "Run Recoleta locally": "在本機執行 Recoleta",
        "Latest": "最新",
        "More recent notes": "更多近期內容",
        "Full archive": "完整歸檔",
        "Trend archive": "趨勢歸檔",
        "Trend": "趨勢",
        "Idea": "想法",
        "Item": "項目",
        "Research idea": "研究想法",
        "Summary": "摘要",
        "Note": "筆記",
        "Source note": "來源筆記",
        "Markdown source": "Markdown 原始檔",
        "Source": "來源",
        "Published": "發布日期",
        "Collection": "欄目",
        "Relevance": "相關度",
        "Authors": "作者",
        "Unknown": "未知",
        "Open original": "開啟原文",
        "Open arXiv": "開啟 arXiv",
        "Open OpenReview": "開啟 OpenReview",
        "Open GitHub": "開啟 GitHub",
        "Newer": "較新",
        "Older": "較早",
        "Previous": "上一頁",
        "Next": "下一頁",
        "All tracked topics": "全部主題",
        "Topic summary": "主題概況",
        "Latest window": "最近一期",
        "Browse trends": "瀏覽趨勢",
        "Browse ideas": "瀏覽想法",
        "No research notes available yet.": "暫無研究筆記。",
        "No additional notes yet.": "暫無其他內容。",
        "No trends available yet.": "暫無趨勢。",
        "No trends on this page.": "本頁沒有趨勢。",
        "No ideas available yet.": "暫無想法。",
        "No ideas on this page.": "本頁沒有想法。",
        "No topics available yet.": "暫無主題。",
        "No archive entries yet.": "暫無歸檔內容。",
        "No research notes for this topic.": "該主題暫無研究筆記。",
        "No research notes on this page.": "本頁沒有研究筆記。",
        "No tracked topics": "暫無主題",
        "Window": "時間",
        "Granularity": "週期",
        "Instance": "欄目",
        "Coverage": "涵蓋範圍",
    },
    "ja": {
        "Language": "言語",
        "Home": "ホーム",
        "Trends": "トレンド",
        "Ideas": "アイデア",
        "Topic": "トピック",
        "Topics": "トピック",
        "Archive": "アーカイブ",
        "Notes": "ノート",
        "Evidence-led trends and practical ideas from recent technical work.": "最近の技術資料から、根拠のあるトレンドと実践的なアイデアを整理します。",
        "All trends": "すべてのトレンド",
        "All ideas": "すべてのアイデア",
        "Run Recoleta locally": "Recoleta をローカルで実行",
        "Latest": "最新",
        "More recent notes": "最近のノート",
        "Full archive": "全アーカイブ",
        "Trend archive": "トレンドアーカイブ",
        "Trend": "トレンド",
        "Idea": "アイデア",
        "Item": "項目",
        "Research idea": "研究アイデア",
        "Summary": "要約",
        "Note": "ノート",
        "Source note": "資料ノート",
        "Markdown source": "Markdown ソース",
        "Source": "出典",
        "Published": "公開日",
        "Collection": "コレクション",
        "Relevance": "関連度",
        "Authors": "著者",
        "Unknown": "不明",
        "Open original": "原文を開く",
        "Open arXiv": "arXiv を開く",
        "Open OpenReview": "OpenReview を開く",
        "Open GitHub": "GitHub を開く",
        "Newer": "新しい記事",
        "Older": "以前の記事",
        "Previous": "前へ",
        "Next": "次へ",
        "All tracked topics": "すべてのトピック",
        "Topic summary": "トピック概要",
        "Latest window": "最新期間",
        "Browse trends": "トレンドを見る",
        "Browse ideas": "アイデアを見る",
        "No research notes available yet.": "研究ノートはまだありません。",
        "No additional notes yet.": "ほかのノートはまだありません。",
        "No trends available yet.": "トレンドはまだありません。",
        "No trends on this page.": "このページにはトレンドがありません。",
        "No ideas available yet.": "アイデアはまだありません。",
        "No ideas on this page.": "このページにはアイデアがありません。",
        "No topics available yet.": "トピックはまだありません。",
        "No archive entries yet.": "アーカイブはまだありません。",
        "No research notes for this topic.": "このトピックの研究ノートはありません。",
        "No research notes on this page.": "このページには研究ノートがありません。",
        "No tracked topics": "トピックはありません",
        "Window": "期間",
        "Granularity": "集計単位",
        "Instance": "配信元",
        "Coverage": "対象範囲",
    },
    "ko": {
        "Language": "언어",
        "Home": "홈",
        "Trends": "트렌드",
        "Ideas": "아이디어",
        "Topic": "주제",
        "Topics": "주제",
        "Archive": "아카이브",
        "Notes": "노트",
        "Evidence-led trends and practical ideas from recent technical work.": "최근 기술 자료에서 근거 있는 트렌드와 실용적인 아이디어를 정리합니다.",
        "All trends": "모든 트렌드",
        "All ideas": "모든 아이디어",
        "Run Recoleta locally": "Recoleta 로컬 실행",
        "Latest": "최신",
        "More recent notes": "최근 노트",
        "Full archive": "전체 아카이브",
        "Trend archive": "트렌드 아카이브",
        "Trend": "트렌드",
        "Idea": "아이디어",
        "Item": "항목",
        "Research idea": "연구 아이디어",
        "Summary": "요약",
        "Note": "노트",
        "Source note": "자료 노트",
        "Markdown source": "Markdown 원문",
        "Source": "출처",
        "Published": "게시일",
        "Collection": "컬렉션",
        "Relevance": "관련도",
        "Authors": "저자",
        "Unknown": "알 수 없음",
        "Open original": "원문 열기",
        "Open arXiv": "arXiv 열기",
        "Open OpenReview": "OpenReview 열기",
        "Open GitHub": "GitHub 열기",
        "Newer": "최신 글",
        "Older": "이전 글",
        "Previous": "이전",
        "Next": "다음",
        "All tracked topics": "모든 주제",
        "Topic summary": "주제 요약",
        "Latest window": "최근 기간",
        "Browse trends": "트렌드 보기",
        "Browse ideas": "아이디어 보기",
        "No research notes available yet.": "아직 연구 노트가 없습니다.",
        "No additional notes yet.": "아직 다른 노트가 없습니다.",
        "No trends available yet.": "아직 트렌드가 없습니다.",
        "No trends on this page.": "이 페이지에는 트렌드가 없습니다.",
        "No ideas available yet.": "아직 아이디어가 없습니다.",
        "No ideas on this page.": "이 페이지에는 아이디어가 없습니다.",
        "No topics available yet.": "아직 주제가 없습니다.",
        "No archive entries yet.": "아직 보관된 항목이 없습니다.",
        "No research notes for this topic.": "이 주제의 연구 노트가 없습니다.",
        "No research notes on this page.": "이 페이지에는 연구 노트가 없습니다.",
        "No tracked topics": "추적 중인 주제가 없습니다",
        "Window": "기간",
        "Granularity": "집계 단위",
        "Instance": "출처",
        "Coverage": "범위",
    },
}

_SITE_COUNT_LABELS = {
    "zh-CN": {
        "trend": "条趋势",
        "idea": "个想法",
        "topic": "个主题",
        "entry": "项内容",
    },
    "zh-TW": {
        "trend": "則趨勢",
        "idea": "個想法",
        "topic": "個主題",
        "entry": "項內容",
    },
    "ja": {
        "trend": "件のトレンド",
        "idea": "件のアイデア",
        "topic": "件のトピック",
        "entry": "件",
    },
    "ko": {
        "trend": "개 트렌드",
        "idea": "개 아이디어",
        "topic": "개 주제",
        "entry": "개 항목",
    },
}


def _site_chrome_locale(language_code: str) -> str | None:
    normalized = language_code.strip().replace("_", "-").lower()
    parts = [part for part in normalized.split("-") if part]
    if not parts:
        return None
    primary = parts[0]
    if primary == "zh":
        if "hant" in parts or any(region in parts for region in {"hk", "mo", "tw"}):
            return "zh-TW"
        return "zh-CN"
    if primary == "ja":
        return "ja"
    if primary == "ko":
        return "ko"
    return None


def _localized_site_chrome_text(*, text: str, locale: str) -> str:
    translated = _SITE_CHROME_TRANSLATIONS[locale].get(text)
    if translated is not None:
        return translated

    count_labels = _SITE_COUNT_LABELS[locale]
    count_nouns = {
        "trend": "trend",
        "trends": "trend",
        "idea": "idea",
        "ideas": "idea",
        "topic": "topic",
        "topics": "topic",
        "entry": "entry",
        "entries": "entry",
    }

    def _replace_count(match: re.Match[str]) -> str:
        noun = count_nouns[match.group(2)]
        return f"{match.group(1)} {count_labels[noun]}"

    localized = re.sub(
        r"\b(\d+) (trend|trends|idea|ideas|topic|topics|entry|entries)\b",
        _replace_count,
        text,
    )
    latest_window_label = _SITE_CHROME_TRANSLATIONS[locale]["Latest window"]
    localized = re.sub(
        r"\blatest window\b",
        latest_window_label,
        localized,
        flags=re.IGNORECASE,
    )
    for kind in ("Trend", "Idea"):
        translated_kind = _SITE_CHROME_TRANSLATIONS[locale].get(kind, kind)
        if localized.startswith(f"{kind} ·"):
            localized = translated_kind + localized[len(kind) :]

    metadata_labels = ("Source", "Published", "Relevance", "Authors", "Instance")
    for label in metadata_labels:
        translated_label = _SITE_CHROME_TRANSLATIONS[locale].get(label, label)
        localized = re.sub(
            rf"(^| · ){re.escape(label)}:",
            lambda match, value=translated_label: f"{match.group(1)}{value}:",
            localized,
        )

    go_to_page_match = re.fullmatch(r"Go to page (\d+)", localized)
    if go_to_page_match:
        page_number = go_to_page_match.group(1)
        if locale in {"zh-CN", "zh-TW"}:
            return f"前往第 {page_number} 页" if locale == "zh-CN" else f"前往第 {page_number} 頁"
        if locale == "ja":
            return f"{page_number} ページへ"
        return f"{page_number}페이지로 이동"

    pagination_match = re.fullmatch(r"(.+) pagination", localized)
    if pagination_match:
        collection_label = pagination_match.group(1)
        if collection_label.endswith(" topic"):
            topic_label = _SITE_CHROME_TRANSLATIONS[locale].get("Topic", "Topic")
            collection_label = f"{collection_label[:-6]} {topic_label}".strip()
        else:
            collection_label = _SITE_CHROME_TRANSLATIONS[locale].get(
                collection_label,
                collection_label,
            )
        if locale in {"zh-CN", "zh-TW"}:
            return f"{collection_label}分页"
        if locale == "ja":
            return f"{collection_label}のページ移動"
        return f"{collection_label} 페이지 탐색"

    def _replace_page_range(match: re.Match[str]) -> str:
        current, total = match.groups()
        if locale == "zh-CN":
            return f"第 {current} / {total} 页"
        if locale == "zh-TW":
            return f"第 {current} / {total} 頁"
        if locale == "ja":
            return f"{current} / {total} ページ"
        return f"{current} / {total} 페이지"

    localized = re.sub(r"Page (\d+) of (\d+)", _replace_page_range, localized)

    def _replace_page_number(match: re.Match[str]) -> str:
        page_number = match.group(1)
        if locale == "zh-CN":
            return f"第 {page_number} 页"
        if locale == "zh-TW":
            return f"第 {page_number} 頁"
        if locale == "ja":
            return f"{page_number} ページ"
        return f"{page_number} 페이지"

    localized = re.sub(r"\bPage (\d+)\b", _replace_page_number, localized)

    period_labels = {
        "zh-CN": {"Day": "日", "Week": "周", "Month": "月"},
        "zh-TW": {"Day": "日", "Week": "週", "Month": "月"},
        "ja": {"Day": "日", "Week": "週", "Month": "月"},
        "ko": {"Day": "일", "Week": "주", "Month": "월"},
    }[locale]
    for source, target in period_labels.items():
        localized = re.sub(rf"^{source}(?= · )", target, localized)
        localized = localized.replace(f" · {source} ·", f" · {target} ·")
    return localized


_SITE_CHROME_TEXT_SELECTORS = (
    ".site-header",
    ".language-switcher",
    ".hero-kicker",
    ".home-title",
    ".home-dek",
    ".home-primary-links",
    ".home-latest > .section-heading-row",
    ".home-feed > .section-heading-row",
    ".home-feature-meta",
    ".latest-feed-meta",
    ".page-section-title",
    ".section-kicker",
    ".meta-date",
    ".detail-meta",
    ".detail-utility",
    ".detail-actions",
    ".page-item .detail-content .section-label",
    ".breadcrumbs",
    ".pager-card",
    ".topic-card-meta",
    ".meta-panel-label",
    ".collection-pagination",
    ".archive-item > span",
    ".empty-card",
    ".meta-pill.subdued",
)


def _localize_site_document_title(*, soup: BeautifulSoup, locale: str) -> None:
    title_tag = soup.find("title")
    body_tag = soup.find("body")
    if title_tag is None or body_tag is None:
        return
    raw_title = title_tag.get_text()
    title_parts = raw_title.split(" · ")
    raw_body_classes = body_tag.get("class")
    if isinstance(raw_body_classes, list):
        body_classes = {str(class_name) for class_name in raw_body_classes}
    elif isinstance(raw_body_classes, str):
        body_classes = set(raw_body_classes.split())
    else:
        body_classes = set()
    collection_label_by_class = {
        "page-trends": "Trends",
        "page-ideas": "Ideas",
        "page-topics": "Topics",
        "page-archive": "Archive",
    }
    for body_class, label in collection_label_by_class.items():
        if body_class in body_classes and title_parts and title_parts[0] == label:
            title_parts[0] = _SITE_CHROME_TRANSLATIONS[locale][label]
            break
    if title_parts and re.fullmatch(r"Page \d+", title_parts[-1]):
        title_parts[-1] = _localized_site_chrome_text(
            text=title_parts[-1],
            locale=locale,
        )
    title_tag.string = " · ".join(title_parts)


def _localize_site_chrome(*, soup: BeautifulSoup, language_code: str) -> None:
    locale = _site_chrome_locale(language_code)
    if locale is None:
        return
    nodes: list[Any] = []
    aria_tags: list[Tag] = []
    seen_nodes: set[int] = set()
    seen_aria_tags: set[int] = set()
    for container in soup.select(", ".join(_SITE_CHROME_TEXT_SELECTORS)):
        for node in container.find_all(string=True):
            if id(node) not in seen_nodes:
                seen_nodes.add(id(node))
                nodes.append(node)
        if container.has_attr("aria-label") and id(container) not in seen_aria_tags:
            seen_aria_tags.add(id(container))
            aria_tags.append(container)
        for tag in container.select("[aria-label]"):
            if id(tag) not in seen_aria_tags:
                seen_aria_tags.add(id(tag))
                aria_tags.append(tag)
    for node in nodes:
        parent = node.parent
        if parent is not None and parent.name in {"script", "style"}:
            continue
        raw = str(node)
        stripped = raw.strip()
        if not stripped:
            continue
        localized = _localized_site_chrome_text(text=stripped, locale=locale)
        if localized != stripped:
            node.replace_with(raw.replace(stripped, localized, 1))
    for tag in aria_tags:
        aria_label = str(tag.get("aria-label") or "").strip()
        if aria_label:
            tag["aria-label"] = _localized_site_chrome_text(
                text=aria_label,
                locale=locale,
            )
    _localize_site_document_title(soup=soup, locale=locale)


def _native_language_name(language_code: str) -> str:
    normalized = language_code.strip().replace("_", "-").lower()
    primary = normalized.split("-", 1)[0]
    error_message = (
        f"Unsupported site language code {language_code!r}: "
        "no native display name is available"
    )
    if primary == "und":
        raise ValueError(error_message)
    try:
        locale = Locale.parse(normalized.replace("-", "_"), sep="_")
        native_name = str(locale.get_display_name(locale) or "").strip()
    except (UnknownLocaleError, ValueError) as exc:
        raise ValueError(error_message) from exc
    if primary == "zh":
        return "繁體中文" if _site_chrome_locale(language_code) == "zh-TW" else "简体中文"
    if not native_name:
        raise ValueError(error_message)
    return native_name


def _render_language_switcher_fragment(
    *,
    current_language_slug: str,
    current_page_relative_path: str,
    page_paths_by_language: dict[str, set[str]],
    language_code_by_slug: dict[str, str],
) -> Tag:
    switcher_soup = BeautifulSoup("", "html.parser")
    container = switcher_soup.new_tag("nav")
    container["class"] = "language-switcher"
    container["aria-label"] = "Language"
    current_page_path = (
        PurePosixPath(current_language_slug) / current_page_relative_path
    )

    def _build_language_link(
        *,
        language_slug: str,
        language_code: str,
        class_name: str,
        is_current: bool = False,
    ) -> Tag:
        target_relative_path = (
            current_page_relative_path
            if current_page_relative_path
            in page_paths_by_language.get(language_slug, set())
            else "index.html"
        )
        target_page_path = PurePosixPath(language_slug) / target_relative_path
        anchor = switcher_soup.new_tag(
            "a",
            href=posixpath.relpath(
                str(target_page_path),
                start=str(current_page_path.parent),
            ),
        )
        classes = [class_name]
        if is_current:
            classes.append("is-active")
            anchor["aria-current"] = "page"
        anchor["class"] = " ".join(classes)
        anchor["data-language-code"] = language_slug
        anchor["hreflang"] = language_code
        name = switcher_soup.new_tag("span")
        name["lang"] = language_code
        name["dir"] = "auto"
        name.string = _native_language_name(language_code)
        anchor.append(name)
        if is_current:
            check = switcher_soup.new_tag("span")
            check["class"] = "language-switcher-check"
            check["aria-hidden"] = "true"
            check.string = "✓"
            anchor.append(check)
        return anchor

    if len(language_code_by_slug) == 2:
        alternate_slug, alternate_code = next(
            (slug, code)
            for slug, code in language_code_by_slug.items()
            if slug != current_language_slug
        )
        container.append(
            _build_language_link(
                language_slug=alternate_slug,
                language_code=alternate_code,
                class_name="language-switcher-link",
            )
        )
    else:
        menu = switcher_soup.new_tag("details")
        menu["class"] = "language-switcher-menu"
        trigger = switcher_soup.new_tag("summary")
        trigger["class"] = "language-switcher-trigger"
        current_code = language_code_by_slug.get(
            current_language_slug,
            current_language_slug,
        )
        current_name = switcher_soup.new_tag("span")
        current_name["lang"] = current_code
        current_name["dir"] = "auto"
        current_name.string = _native_language_name(current_code)
        trigger.append(current_name)
        menu.append(trigger)

        language_list = switcher_soup.new_tag("ul")
        language_list["class"] = "language-switcher-list"
        for language_slug, language_code in language_code_by_slug.items():
            item = switcher_soup.new_tag("li")
            item.append(
                _build_language_link(
                    language_slug=language_slug,
                    language_code=language_code,
                    class_name="language-switcher-option",
                    is_current=language_slug == current_language_slug,
                )
            )
            language_list.append(item)
        menu.append(language_list)
        container.append(menu)

    script = switcher_soup.new_tag("script")
    script.string = (
        "(function(){"
        "var links=document.querySelectorAll('.language-switcher [data-language-code]');"
        "for(var i=0;i<links.length;i+=1){"
        "links[i].addEventListener('click',function(){"
        "try{localStorage.setItem('recoleta-language-code',this.getAttribute('data-language-code')||'');}catch(_err){}"
        "});"
        "}"
        "var menus=document.querySelectorAll('details.language-switcher-menu');"
        "document.addEventListener('click',function(event){"
        "for(var j=0;j<menus.length;j+=1){"
        "if(menus[j].open&&!menus[j].contains(event.target)){menus[j].open=false;}"
        "}"
        "});"
        "document.addEventListener('keydown',function(event){"
        "if(event.key!=='Escape'){return;}"
        "for(var j=0;j<menus.length;j+=1){"
        "if(menus[j].open){menus[j].open=false;"
        "var summary=menus[j].querySelector('summary');"
        "if(summary){summary.focus();}"
        "}"
        "}"
        "});"
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
    spec = _SiteLanguageOverrideSpec(
        output_dir=output_dir,
        language_code=language_code,
        language_slug=language_slug,
        page_paths_by_language=page_paths_by_language,
        language_code_by_slug=language_code_by_slug,
    )
    _append_language_switcher_styles(output_dir=output_dir)
    for html_path in output_dir.rglob("*.html"):
        _apply_site_language_override_to_page(html_path=html_path, spec=spec)


def _append_language_switcher_styles(*, output_dir: Path) -> None:
    stylesheet_path = output_dir / "assets" / "site.css"
    if not stylesheet_path.exists():
        return
    stylesheet = stylesheet_path.read_text(encoding="utf-8")
    if ".language-switcher {" in stylesheet:
        return
    stylesheet_path.write_text(
        stylesheet.rstrip() + "\n" + _LANGUAGE_SWITCHER_CSS.strip() + "\n",
        encoding="utf-8",
    )


def _apply_site_language_override_to_page(
    *,
    html_path: Path,
    spec: _SiteLanguageOverrideSpec,
) -> None:
    relative_path = str(html_path.relative_to(spec.output_dir)).replace("\\", "/")
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")
    html_tag = soup.find("html")
    if html_tag is not None:
        html_tag["lang"] = spec.language_code

    if len(spec.language_code_by_slug) > 1:
        nav_actions = soup.select_one(".site-header .nav-actions")
        if nav_actions is not None:
            nav_actions["data-has-language-switcher"] = "true"
            utility_cluster = nav_actions.select_one(".nav-utility-cluster")
            insertion_target = (
                utility_cluster if utility_cluster is not None else nav_actions
            )
            if nav_actions.select_one(".language-switcher") is None:
                insertion_target.insert(
                    0,
                    _render_language_switcher_fragment(
                        current_language_slug=spec.language_slug,
                        current_page_relative_path=relative_path,
                        page_paths_by_language=spec.page_paths_by_language,
                        language_code_by_slug=spec.language_code_by_slug,
                    ),
                )
    _localize_site_chrome(soup=soup, language_code=spec.language_code)
    rendered_html = str(soup).replace(
        f'<html lang="{spec.language_code}">',
        f"<html lang='{spec.language_code}'>",
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
    return _export_trend_static_site_single_language_impl(
        request=SingleLanguageSiteExportRequest(
            input_dir=tuple(input_dir)
            if isinstance(input_dir, Sequence)
            and not isinstance(input_dir, (Path, TrendSiteInputSpec))
            else input_dir,
            output_dir=output_dir,
            limit=limit,
            item_export_scope=item_export_scope,
            include_localized_children=include_localized_children,
        ),
        deps=SingleLanguageSiteExportDeps(
            normalize_item_export_scope=_normalize_item_export_scope,
            coerce_site_input_specs=_coerce_site_input_specs,
            discover_trend_site_input_dirs=_discover_trend_site_input_dirs,
            paths_overlap=_paths_overlap,
            reset_directory=_reset_directory,
            load_trend_source_documents=_load_trend_source_documents,
            load_idea_source_documents=_load_idea_source_documents,
            select_item_source_documents=_select_item_source_documents,
            load_item_site_documents=_load_item_site_documents,
            load_trend_site_documents=_load_trend_site_documents,
            site_source_key=_site_source_key,
            load_idea_site_documents=_load_idea_site_documents,
            topic_slug=_topic_slug,
            render_home_page=_render_home_page,
            render_trends_index_page=_render_trends_index_page,
            render_archive_page=_render_archive_page,
            render_topics_index_page=_render_topics_index_page,
            render_ideas_index_page=_render_ideas_index_page,
            render_detail_page=_render_detail_page,
            render_item_page=_render_item_page,
            render_idea_page=_render_idea_page,
            render_topic_page=_render_topic_page,
            site_css=_SITE_CSS,
        ),
    )


def export_trend_static_site(
    *,
    input_dir: Path | TrendSiteInputSpec | Sequence[Path | TrendSiteInputSpec],
    output_dir: Path,
    limit: int | None = None,
    default_language_code: str | None = None,
    item_export_scope: str = "linked",
    metrics_recorder: Any | None = None,
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
        export_started = time.perf_counter()
        manifest_path = _export_single_language_trend_static_site(
            input_dir=input_dir,
            output_dir=output_dir,
            limit=limit,
            item_export_scope=normalized_item_export_scope,
            language_inputs=language_inputs,
        )
        _record_site_build_timing(
            metrics_recorder=metrics_recorder,
            step_name="single_language.export",
            started=export_started,
        )
        return manifest_path

    normalized_default_language_slug = language_slug_from_code(default_language_code)
    if not normalized_default_language_slug:
        raise ValueError(
            "default_language_code is required when exporting a multilingual site"
        )
    if normalized_default_language_slug not in {
        language_slug
        for _language_code, language_slug, _root_paths in valid_language_inputs
    }:
        raise ValueError(
            "default_language_code must match one discovered language root"
        )

    for language_code, _language_slug, _root_paths in valid_language_inputs:
        _native_language_name(language_code)

    resolved_output_dir = output_dir.expanduser().resolve()
    prepare_started = time.perf_counter()
    _reset_directory(resolved_output_dir)
    (resolved_output_dir / ".nojekyll").write_text("", encoding="utf-8")
    _record_site_build_timing(
        metrics_recorder=metrics_recorder,
        step_name="multilang.prepare_output",
        started=prepare_started,
    )

    export_started = time.perf_counter()
    manifest_by_language, page_paths_by_language, language_code_by_slug = (
        _write_multilingual_site_outputs(
            output_dir=resolved_output_dir,
            valid_language_inputs=valid_language_inputs,
            limit=limit,
            item_export_scope=normalized_item_export_scope,
            metrics_recorder=metrics_recorder,
        )
    )
    _record_site_build_timing(
        metrics_recorder=metrics_recorder,
        step_name="multilang.export_languages",
        started=export_started,
        metadata={"language_count": len(language_code_by_slug)},
    )

    for language_slug, language_code in language_code_by_slug.items():
        overrides_started = time.perf_counter()
        _apply_site_language_overrides(
            output_dir=resolved_output_dir / language_slug,
            language_code=language_code,
            language_slug=language_slug,
            page_paths_by_language=page_paths_by_language,
            language_code_by_slug=language_code_by_slug,
        )
        _record_site_build_timing(
            metrics_recorder=metrics_recorder,
            step_name="multilang.apply_language_overrides",
            started=overrides_started,
            metadata={"language_slug": language_slug},
        )

    aggregate_started = time.perf_counter()
    aggregate_manifest = _aggregate_multilingual_site_manifest(
        output_dir=resolved_output_dir,
        manifest_by_language=manifest_by_language,
        language_code_by_slug=language_code_by_slug,
        default_language_slug=normalized_default_language_slug,
    )
    _record_site_build_timing(
        metrics_recorder=metrics_recorder,
        step_name="multilang.aggregate_manifest",
        started=aggregate_started,
        metadata={"language_count": len(language_code_by_slug)},
    )
    email_links_started = time.perf_counter()
    aggregated_email_links = aggregate_multilingual_email_links(
        output_dir=resolved_output_dir,
        language_slugs=sorted(language_code_by_slug),
        default_language_slug=normalized_default_language_slug,
    )
    write_email_links_artifact(
        site_output_dir=resolved_output_dir,
        pages_by_source_markdown=aggregated_email_links["pages_by_source_markdown"],
        topic_pages_by_slug=aggregated_email_links["topic_pages_by_slug"],
        topic_pages_by_language=aggregated_email_links["topic_pages_by_language"],
    )
    remove_child_email_links_artifacts(
        output_dir=resolved_output_dir,
        language_slugs=sorted(language_code_by_slug),
    )
    _record_site_build_timing(
        metrics_recorder=metrics_recorder,
        step_name="multilang.email_links",
        started=email_links_started,
        metadata={"language_count": len(language_code_by_slug)},
    )

    root_files_started = time.perf_counter()
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
    _record_site_build_timing(
        metrics_recorder=metrics_recorder,
        step_name="multilang.write_root_files",
        started=root_files_started,
        metadata={"language_count": len(language_code_by_slug)},
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
    return _stage_trend_site_source_impl(
        request=TrendSiteSourceStageRequest(
            input_dir=input_dir,
            output_dir=output_dir,
            limit=limit,
            default_language_code=default_language_code,
            item_export_scope=item_export_scope,
        ),
        deps=TrendSiteSourceStageDeps(
            normalize_item_export_scope=_normalize_item_export_scope,
            coerce_site_input_specs=_coerce_site_input_specs,
            discover_trend_site_input_dirs=_discover_trend_site_input_dirs,
            paths_overlap=_paths_overlap,
            reset_stage_output_root=_reset_stage_output_root,
            load_trend_source_documents=_load_trend_source_documents,
            load_idea_source_documents=_load_idea_source_documents,
            select_item_source_documents=_select_item_source_documents,
            presentation_sidecar_path=presentation_sidecar_path,
            language_slug_from_code=language_slug_from_code,
        ),
    )
