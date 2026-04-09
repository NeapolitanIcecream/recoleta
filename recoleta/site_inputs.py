from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
from typing import Any, Callable

from bs4 import BeautifulSoup
from loguru import logger
from markdown_it import MarkdownIt

from recoleta.site_models import (
    IdeaSiteSourceDocument,
    ItemSiteSelection,
    ItemSiteSourceDocument,
    SiteSourceKey,
    TrendSiteDocument,
    TrendSiteInputDirectory,
    TrendSiteInputSpec,
    TrendSiteSourceDocument,
)


@dataclass(frozen=True, slots=True)
class SiteInputDiscoveryDeps:
    normalize_site_instance: Callable[[str | None], str | None]
    infer_instance_name_from_site_path: Callable[[Path], str | None]
    infer_site_language_code_from_root: Callable[[Path], str | None]
    language_slug_from_code: Callable[[str | None], str]
    reject_legacy_stream_layout: Callable[..., None]
    validate_unique_site_instance_slugs: Callable[..., None]


@dataclass(frozen=True, slots=True)
class SiteLanguageDiscoveryDeps:
    normalize_site_instance: Callable[[str | None], str | None]
    infer_instance_name_from_site_root: Callable[[Path], str | None]
    infer_site_language_code_from_root: Callable[[Path], str | None]
    language_slug_from_code: Callable[[str | None], str]
    reject_legacy_stream_layout: Callable[..., None]


@dataclass(slots=True)
class SiteLanguageDiscoveryState:
    discovered: list[tuple[str | None, str, tuple[TrendSiteInputSpec, ...]]]
    grouped_roots: dict[str, list[TrendSiteInputSpec]]
    language_code_by_slug: dict[str, str]
    seen_roots: set[tuple[Path, str | None]]


@dataclass(frozen=True, slots=True)
class SiteItemSourceLoadDeps:
    split_yaml_frontmatter_text: Callable[[str], tuple[dict[str, Any], str]]
    extract_markdown_h1: Callable[..., str]
    parse_site_datetime: Callable[[Any], datetime | None]
    parse_site_string_list: Callable[[Any], list[str]]
    resolve_site_instance: Callable[..., str | None]
    site_source_key: Callable[..., SiteSourceKey]


@dataclass(frozen=True, slots=True)
class SiteReferenceCollectionDeps:
    presentation_local_markdown_targets: Callable[..., set[Path]]
    resolve_site_source_key: Callable[..., SiteSourceKey | None]
    resolve_site_local_markdown_target: Callable[..., Path | None]


@dataclass(frozen=True, slots=True)
class TrendSiteDocumentLoadDeps:
    site_source_key: Callable[..., SiteSourceKey]
    site_namespaced_page_stem: Callable[..., str]
    normalize_obsidian_callouts_for_pdf: Callable[[str], str]
    extract_trend_pdf_sections: Callable[..., tuple[str, list[Any]]]
    sanitize_trend_title: Callable[..., str]
    section_excerpt: Callable[[list[Any]], str]
    build_trend_body_from_presentation: Callable[..., tuple[str, str]]
    rewrite_site_markdown_links: Callable[..., str]
    build_trend_browser_body_html: Callable[..., str]
    trend_date_token: Callable[..., str]
    site_namespaced_asset_name: Callable[..., str]


@dataclass(frozen=True, slots=True)
class TrendSiteSourceStageDeps:
    normalize_item_export_scope: Callable[[str | None], str]
    coerce_site_input_specs: Callable[..., list[TrendSiteInputSpec]]
    discover_trend_site_input_dirs: Callable[..., list[TrendSiteInputDirectory]]
    paths_overlap: Callable[..., bool]
    reset_stage_output_root: Callable[..., None]
    load_trend_source_documents: Callable[..., list[TrendSiteSourceDocument]]
    load_idea_source_documents: Callable[..., list[IdeaSiteSourceDocument]]
    select_item_source_documents: Callable[..., ItemSiteSelection]
    presentation_sidecar_path: Callable[..., Path]
    language_slug_from_code: Callable[[str | None], str]


@dataclass(frozen=True, slots=True)
class TrendBrowserBodyContext:
    source_document: TrendSiteSourceDocument
    sections: list[Any]
    markdown_title: str
    markdown_excerpt: str
    page_path: Path
    linked_page_by_source_key: dict[SiteSourceKey, Path]


@dataclass(frozen=True, slots=True)
class TrendSiteSourceStageRequest:
    input_dir: Path | TrendSiteInputSpec | Sequence[Path | TrendSiteInputSpec]
    output_dir: Path
    limit: int | None = None
    default_language_code: str | None = None
    item_export_scope: str = "linked"


@dataclass(frozen=True, slots=True)
class StageSourceArtifacts:
    source_documents: list[TrendSiteSourceDocument]
    idea_source_documents: list[IdeaSiteSourceDocument]
    item_selection: ItemSiteSelection
    staged_markdown_files: list[str]
    staged_idea_files: list[str]
    staged_item_files: list[str]
    staged_pdf_files: list[str]


@dataclass(frozen=True, slots=True)
class StageSourceManifestContext:
    resolved_input_roots: list[TrendSiteInputSpec]
    resolved_input_dirs: list[TrendSiteInputDirectory]
    resolved_output_dir: Path
    default_language_code: str | None
    normalized_item_export_scope: str
    artifacts: StageSourceArtifacts
    language_slug_from_code: Callable[[str | None], str]


@dataclass(frozen=True, slots=True)
class StageSourceArtifactsContext:
    resolved_input_dirs: list[TrendSiteInputDirectory]
    request: TrendSiteSourceStageRequest
    stage_root: Path
    resolved_output_dir: Path
    normalized_item_export_scope: str


def _resolved_instance(
    *,
    candidate: Path,
    instance: str | None,
    deps: SiteInputDiscoveryDeps,
) -> str | None:
    if instance is not None:
        return deps.normalize_site_instance(instance)
    inferred = deps.infer_instance_name_from_site_path(candidate)
    return deps.normalize_site_instance(inferred)


def _ideas_path_for_root(root_path: Path) -> Path | None:
    ideas_path = root_path / "Ideas"
    if ideas_path.exists() and ideas_path.is_dir():
        return ideas_path
    return None


def _inbox_path_for_root(root_path: Path) -> Path | None:
    inbox_path = root_path / "Inbox"
    if inbox_path.exists() and inbox_path.is_dir():
        return inbox_path
    return None


def _build_input_directory(
    *,
    candidate: Path,
    instance: str | None,
    deps: SiteInputDiscoveryDeps,
) -> TrendSiteInputDirectory | None:
    resolved_candidate = candidate.expanduser().resolve()
    if not resolved_candidate.exists() or not resolved_candidate.is_dir():
        return None

    root_path = (
        resolved_candidate.parent
        if resolved_candidate.name == "Trends"
        else resolved_candidate
    )
    language_code = deps.infer_site_language_code_from_root(root_path)
    return TrendSiteInputDirectory(
        path=resolved_candidate,
        root_path=root_path,
        inbox_path=_inbox_path_for_root(root_path),
        ideas_path=_ideas_path_for_root(root_path),
        instance=_resolved_instance(
            candidate=resolved_candidate,
            instance=instance,
            deps=deps,
        ),
        language_code=language_code,
        language_slug=deps.language_slug_from_code(language_code) or None,
        is_localized_root=root_path.parent.name == "Localized",
    )


def _collect_localized_candidates(
    *,
    root_path: Path,
    include_localized_children: bool,
    deps: SiteInputDiscoveryDeps,
) -> list[Path]:
    if not include_localized_children:
        return []
    localized_root = root_path / "Localized"
    if not localized_root.exists() or not localized_root.is_dir():
        return []

    candidates: list[Path] = []
    for child in sorted(path for path in localized_root.iterdir() if path.is_dir()):
        deps.reject_legacy_stream_layout(child, context="Localized trend site input")
        child_trends_dir = child / "Trends"
        candidates.append(
            child_trends_dir
            if child_trends_dir.exists() and child_trends_dir.is_dir()
            else child
        )
    return candidates


def _collect_stream_candidates(
    *,
    root_path: Path,
    include_localized_children: bool,
) -> list[tuple[Path, str]]:
    streams_root = root_path / "Streams"
    if not streams_root.exists() or not streams_root.is_dir():
        return []

    candidates: list[tuple[Path, str]] = []
    for stream_root in sorted(path for path in streams_root.iterdir() if path.is_dir()):
        stream_trends_dir = stream_root / "Trends"
        if stream_trends_dir.exists() and stream_trends_dir.is_dir():
            candidates.append((stream_trends_dir, stream_root.name))
        candidates.extend(
            _collect_stream_localized_candidates(
                stream_root=stream_root,
                include_localized_children=include_localized_children,
            )
        )
    return candidates


def _collect_stream_localized_candidates(
    *,
    stream_root: Path,
    include_localized_children: bool,
) -> list[tuple[Path, str]]:
    if not include_localized_children:
        return []
    stream_localized_root = stream_root / "Localized"
    if not stream_localized_root.exists() or not stream_localized_root.is_dir():
        return []

    candidates: list[tuple[Path, str]] = []
    for child in sorted(
        path for path in stream_localized_root.iterdir() if path.is_dir()
    ):
        child_trends_dir = child / "Trends"
        candidates.append(
            (
                child_trends_dir
                if child_trends_dir.exists() and child_trends_dir.is_dir()
                else child,
                stream_root.name,
            )
        )
    return candidates


def _collect_input_candidates(
    *,
    raw_input: TrendSiteInputSpec,
    include_localized_children: bool,
    deps: SiteInputDiscoveryDeps,
) -> tuple[list[Path], list[tuple[Path, str]]]:
    raw_path = raw_input.path
    deps.reject_legacy_stream_layout(raw_path, context="Trend site input")
    candidates: list[Path] = []
    if raw_path.name == "Trends":
        candidates.append(raw_path)

    direct_trends_dir = raw_path / "Trends"
    if direct_trends_dir.exists() and direct_trends_dir.is_dir():
        candidates.append(direct_trends_dir)
    candidates.extend(
        _collect_localized_candidates(
            root_path=raw_path,
            include_localized_children=include_localized_children,
            deps=deps,
        )
    )
    if not candidates:
        candidates.append(raw_path)

    staged_candidates: list[tuple[Path, str]] = []
    if (raw_path / "manifest.json").exists():
        staged_candidates = _collect_stream_candidates(
            root_path=raw_path,
            include_localized_children=include_localized_children,
        )
    return candidates, staged_candidates


def discover_trend_site_input_dirs(
    raw_inputs: list[TrendSiteInputSpec],
    *,
    include_localized_children: bool = True,
    deps: SiteInputDiscoveryDeps,
) -> list[TrendSiteInputDirectory]:
    discovered: list[TrendSiteInputDirectory] = []
    seen_paths: set[tuple[Path, str | None]] = set()

    def add_candidate(candidate: Path, *, instance: str | None) -> None:
        input_dir = _build_input_directory(
            candidate=candidate,
            instance=instance,
            deps=deps,
        )
        if input_dir is None:
            return
        key = (input_dir.path, input_dir.instance)
        if key in seen_paths:
            return
        seen_paths.add(key)
        discovered.append(input_dir)

    for raw_input in raw_inputs:
        candidates, staged_candidates = _collect_input_candidates(
            raw_input=raw_input,
            include_localized_children=include_localized_children,
            deps=deps,
        )
        for candidate, instance in staged_candidates:
            add_candidate(candidate, instance=instance)
        for candidate in candidates:
            add_candidate(candidate, instance=raw_input.instance)

    deps.validate_unique_site_instance_slugs(
        [input_dir.instance for input_dir in discovered],
        context="Trend site input instances",
    )
    return discovered


def _resolved_root_instance(
    *,
    root_path: Path,
    instance: str | None,
    deps: SiteLanguageDiscoveryDeps,
) -> str | None:
    if instance is not None:
        return deps.normalize_site_instance(instance)
    inferred = deps.infer_instance_name_from_site_root(root_path)
    return deps.normalize_site_instance(inferred)


def _collect_localized_language_roots(
    *,
    base_root: Path,
    deps: SiteLanguageDiscoveryDeps,
) -> list[Path]:
    localized_root = base_root / "Localized"
    if not localized_root.exists() or not localized_root.is_dir():
        return []
    roots: list[Path] = []
    for child in sorted(path for path in localized_root.iterdir() if path.is_dir()):
        deps.reject_legacy_stream_layout(child, context="Localized trend site input")
        roots.append(child)
    return roots


def _collect_stream_language_roots(base_root: Path) -> list[tuple[Path, str]]:
    streams_root = base_root / "Streams"
    if not (base_root / "manifest.json").exists():
        return []
    if not streams_root.exists() or not streams_root.is_dir():
        return []

    discovered: list[tuple[Path, str]] = []
    for stream_root in sorted(path for path in streams_root.iterdir() if path.is_dir()):
        discovered.append((stream_root, stream_root.name))
        stream_localized_root = stream_root / "Localized"
        if not stream_localized_root.exists() or not stream_localized_root.is_dir():
            continue
        discovered.extend(
            (child, stream_root.name)
            for child in sorted(
                path for path in stream_localized_root.iterdir() if path.is_dir()
            )
        )
    return discovered


def discover_site_language_inputs(
    raw_inputs: list[TrendSiteInputSpec],
    *,
    deps: SiteLanguageDiscoveryDeps,
) -> list[tuple[str | None, str, tuple[TrendSiteInputSpec, ...]]]:
    state = SiteLanguageDiscoveryState(
        discovered=[],
        grouped_roots={},
        language_code_by_slug={},
        seen_roots=set(),
    )
    for raw_input in raw_inputs:
        for root_path, instance in _site_language_candidate_roots(
            raw_input=raw_input,
            deps=deps,
        ):
            _add_site_language_root(
                root_path=root_path,
                instance=instance,
                state=state,
                deps=deps,
            )

    for language_slug in sorted(state.grouped_roots):
        state.discovered.append(
            (
                state.language_code_by_slug[language_slug],
                language_slug,
                tuple(state.grouped_roots[language_slug]),
            )
        )
    return state.discovered


def _site_language_candidate_roots(
    *,
    raw_input: TrendSiteInputSpec,
    deps: SiteLanguageDiscoveryDeps,
) -> list[tuple[Path, str | None]]:
    base_root = (
        (raw_input.path.parent if raw_input.path.name == "Trends" else raw_input.path)
        .expanduser()
        .resolve()
    )
    deps.reject_legacy_stream_layout(base_root, context="Trend site input")
    candidates = [(base_root, raw_input.instance)]
    candidates.extend(
        (localized_root, raw_input.instance)
        for localized_root in _collect_localized_language_roots(
            base_root=base_root,
            deps=deps,
        )
    )
    candidates.extend(_collect_stream_language_roots(base_root))
    return candidates


def _add_site_language_root(
    *,
    root_path: Path,
    instance: str | None,
    state: SiteLanguageDiscoveryState,
    deps: SiteLanguageDiscoveryDeps,
) -> None:
    resolved_root = root_path.expanduser().resolve()
    resolved_instance = _resolved_root_instance(
        root_path=resolved_root,
        instance=instance,
        deps=deps,
    )
    if (resolved_root, resolved_instance) in state.seen_roots:
        return
    if not resolved_root.exists() or not resolved_root.is_dir():
        return
    state.seen_roots.add((resolved_root, resolved_instance))
    language_code = deps.infer_site_language_code_from_root(resolved_root)
    language_slug = (
        deps.language_slug_from_code(language_code) if language_code is not None else ""
    )
    input_spec = TrendSiteInputSpec(path=resolved_root, instance=resolved_instance)
    if language_code is None or not language_slug:
        state.discovered.append((language_code, language_slug, (input_spec,)))
        return
    state.grouped_roots.setdefault(language_slug, []).append(input_spec)
    state.language_code_by_slug[language_slug] = str(language_code)


def _item_relevance_score(frontmatter: dict[str, Any]) -> float | None:
    raw_relevance = frontmatter.get("relevance_score")
    if raw_relevance is None:
        return None
    try:
        return float(raw_relevance)
    except Exception:
        return None


def _load_item_source_document(
    *,
    markdown_path: Path,
    input_info: TrendSiteInputDirectory,
    deps: SiteItemSourceLoadDeps,
) -> tuple[SiteSourceKey, ItemSiteSourceDocument]:
    resolved_markdown_path = markdown_path.resolve()
    raw_markdown = resolved_markdown_path.read_text(encoding="utf-8")
    frontmatter, markdown_body = deps.split_yaml_frontmatter_text(raw_markdown)
    instance = deps.resolve_site_instance(
        input_instance=input_info.instance,
        frontmatter=frontmatter,
    )
    source_key = deps.site_source_key(
        markdown_path=resolved_markdown_path,
        instance=instance,
    )
    return source_key, ItemSiteSourceDocument(
        markdown_path=resolved_markdown_path,
        stem=resolved_markdown_path.stem,
        frontmatter=frontmatter,
        markdown_body=markdown_body,
        title=deps.extract_markdown_h1(
            markdown_body,
            fallback=resolved_markdown_path.stem,
        ),
        canonical_url=str(frontmatter.get("url") or "").strip(),
        source=str(frontmatter.get("source") or "").strip(),
        published_at=deps.parse_site_datetime(frontmatter.get("published_at")),
        authors=deps.parse_site_string_list(frontmatter.get("authors")),
        topics=deps.parse_site_string_list(frontmatter.get("topics")),
        relevance_score=_item_relevance_score(frontmatter),
        instance=instance,
    )


def load_item_source_documents(
    *,
    input_dirs: list[TrendSiteInputDirectory],
    allowed_source_keys: set[SiteSourceKey] | None = None,
    deps: SiteItemSourceLoadDeps,
) -> list[ItemSiteSourceDocument]:
    source_documents: list[ItemSiteSourceDocument] = []
    seen_source_keys: set[SiteSourceKey] = set()
    for input_info in input_dirs:
        if input_info.inbox_path is None:
            continue
        for markdown_path in sorted(input_info.inbox_path.glob("*.md")):
            source_key, source_document = _load_item_source_document(
                markdown_path=markdown_path,
                input_info=input_info,
                deps=deps,
            )
            if source_key in seen_source_keys:
                continue
            seen_source_keys.add(source_key)
            if (
                allowed_source_keys is not None
                and source_key not in allowed_source_keys
            ):
                continue
            source_documents.append(source_document)

    source_documents.sort(
        key=lambda document: (
            document.published_at or datetime.min.replace(tzinfo=timezone.utc),
            document.stem,
        ),
        reverse=True,
    )
    return source_documents


def _presentation_referenced_source_keys(
    *,
    source_document: TrendSiteSourceDocument | IdeaSiteSourceDocument,
    available_source_keys: set[SiteSourceKey],
    deps: SiteReferenceCollectionDeps,
) -> set[SiteSourceKey]:
    if source_document.presentation is None:
        return set()
    referenced_source_keys: set[SiteSourceKey] = set()
    for target_path in deps.presentation_local_markdown_targets(
        presentation=source_document.presentation,
        source_markdown_path=source_document.markdown_path,
    ):
        target_source_key = deps.resolve_site_source_key(
            target_path=target_path,
            source_instance=source_document.instance,
            available_source_keys=available_source_keys,
        )
        if target_source_key is not None:
            referenced_source_keys.add(target_source_key)
    return referenced_source_keys


def _markdown_referenced_source_keys(
    *,
    source_document: TrendSiteSourceDocument | IdeaSiteSourceDocument,
    markdown: MarkdownIt,
    available_source_keys: set[SiteSourceKey],
    deps: SiteReferenceCollectionDeps,
) -> set[SiteSourceKey]:
    normalized_markdown = str(source_document.markdown_body or "").strip()
    if not normalized_markdown:
        return set()

    referenced_source_keys: set[SiteSourceKey] = set()
    rendered_html = markdown.render(normalized_markdown)
    soup = BeautifulSoup(rendered_html, "html.parser")
    for anchor in soup.find_all("a", href=True):
        target_path = deps.resolve_site_local_markdown_target(
            source_markdown_path=source_document.markdown_path,
            href=str(anchor.get("href") or ""),
        )
        if target_path is None:
            continue
        target_source_key = deps.resolve_site_source_key(
            target_path=target_path,
            source_instance=source_document.instance,
            available_source_keys=available_source_keys,
        )
        if target_source_key is not None:
            referenced_source_keys.add(target_source_key)
    return referenced_source_keys


def collect_referenced_item_source_keys(
    *,
    source_documents: list[TrendSiteSourceDocument | IdeaSiteSourceDocument],
    available_source_keys: set[SiteSourceKey],
    deps: SiteReferenceCollectionDeps,
) -> set[SiteSourceKey]:
    if not source_documents or not available_source_keys:
        return set()
    markdown = MarkdownIt("commonmark", {"html": True, "typographer": True})
    referenced_source_keys: set[SiteSourceKey] = set()
    for source_document in source_documents:
        referenced_source_keys.update(
            _presentation_referenced_source_keys(
                source_document=source_document,
                available_source_keys=available_source_keys,
                deps=deps,
            )
        )
        referenced_source_keys.update(
            _markdown_referenced_source_keys(
                source_document=source_document,
                markdown=markdown,
                available_source_keys=available_source_keys,
                deps=deps,
            )
        )
    return referenced_source_keys


def _trend_pages_by_source_key(
    *,
    source_documents: list[TrendSiteSourceDocument],
    trends_dir: Path,
    deps: TrendSiteDocumentLoadDeps,
) -> dict[SiteSourceKey, Path]:
    return {
        deps.site_source_key(
            markdown_path=source_document.markdown_path,
            instance=source_document.instance,
        ): (
            trends_dir
            / f"{deps.site_namespaced_page_stem(stem=source_document.stem, instance=source_document.instance)}.html"
        )
        for source_document in source_documents
    }


def _trend_markdown_sections(
    *,
    source_document: TrendSiteSourceDocument,
    markdown: MarkdownIt,
    deps: TrendSiteDocumentLoadDeps,
) -> tuple[str, list[Any], str]:
    normalized_markdown = (
        deps.normalize_obsidian_callouts_for_pdf(source_document.markdown_body).strip()
        or "# Trend\n"
    )
    body_html = markdown.render(normalized_markdown)
    markdown_title, sections = deps.extract_trend_pdf_sections(body_html=body_html)
    return (
        deps.sanitize_trend_title(markdown_title, fallback="Trend"),
        sections,
        deps.section_excerpt(sections),
    )


def _trend_browser_body(
    *,
    context: TrendBrowserBodyContext,
    deps: TrendSiteDocumentLoadDeps,
) -> tuple[str, str, str]:
    if context.source_document.presentation is None:
        return (
            context.markdown_title,
            context.markdown_excerpt,
            deps.rewrite_site_markdown_links(
                html_text=deps.build_trend_browser_body_html(
                    sections=context.sections,
                ),
                source_markdown_path=context.source_document.markdown_path,
                source_instance=context.source_document.instance,
                from_page=context.page_path,
                page_by_source_key=context.linked_page_by_source_key,
            ),
        )

    content = context.source_document.presentation.get("content")
    title = deps.sanitize_trend_title(
        str(content.get("title") or "").strip() if isinstance(content, dict) else "",
        fallback="Trend",
    )
    rendered_body_html, excerpt = (
        deps.build_trend_body_from_presentation(
            presentation=context.source_document.presentation,
        )
    )
    return (
        title,
        excerpt,
        deps.rewrite_site_markdown_links(
            html_text=rendered_body_html,
            source_markdown_path=context.source_document.markdown_path,
            source_instance=context.source_document.instance,
            from_page=context.page_path,
            page_by_source_key=context.linked_page_by_source_key,
        ),
    )


def _copy_trend_assets(
    *,
    source_document: TrendSiteSourceDocument,
    artifacts_dir: Path,
    deps: TrendSiteDocumentLoadDeps,
) -> tuple[Path, Path | None]:
    markdown_asset_path = artifacts_dir / deps.site_namespaced_asset_name(
        name=source_document.markdown_path.name,
        instance=source_document.instance,
    )
    shutil.copy2(source_document.markdown_path, markdown_asset_path)

    pdf_asset_path: Path | None = None
    if source_document.pdf_path is not None:
        pdf_asset_path = artifacts_dir / deps.site_namespaced_asset_name(
            name=source_document.pdf_path.name,
            instance=source_document.instance,
        )
        shutil.copy2(source_document.pdf_path, pdf_asset_path)
    return markdown_asset_path, pdf_asset_path


def load_trend_site_documents(
    *,
    source_documents: list[TrendSiteSourceDocument],
    output_dir: Path,
    item_pages_by_source_key: dict[SiteSourceKey, Path],
    deps: TrendSiteDocumentLoadDeps,
) -> list[TrendSiteDocument]:
    markdown = MarkdownIt("commonmark", {"html": True, "typographer": True})
    artifacts_dir = output_dir / "artifacts"
    trends_dir = output_dir / "trends"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    trends_dir.mkdir(parents=True, exist_ok=True)

    documents: list[TrendSiteDocument] = []
    trend_pages_by_source_key = _trend_pages_by_source_key(
        source_documents=source_documents,
        trends_dir=trends_dir,
        deps=deps,
    )
    linked_page_by_source_key = dict(item_pages_by_source_key)
    linked_page_by_source_key.update(trend_pages_by_source_key)

    for source_document in source_documents:
        markdown_title, sections, markdown_excerpt = (
            _trend_markdown_sections(
                source_document=source_document,
                markdown=markdown,
                deps=deps,
            )
        )
        source_key = deps.site_source_key(
            markdown_path=source_document.markdown_path,
            instance=source_document.instance,
        )
        page_path = trend_pages_by_source_key[source_key]
        title, excerpt, browser_body_html = _trend_browser_body(
            context=TrendBrowserBodyContext(
                source_document=source_document,
                sections=sections,
                markdown_title=markdown_title,
                markdown_excerpt=markdown_excerpt,
                page_path=page_path,
                linked_page_by_source_key=linked_page_by_source_key,
            ),
            deps=deps,
        )
        period_token = (
            deps.trend_date_token(
                granularity=source_document.granularity,
                period_start=source_document.period_start,
            )
            if source_document.period_start is not None
            else source_document.stem
        )
        markdown_asset_path, pdf_asset_path = _copy_trend_assets(
            source_document=source_document,
            artifacts_dir=artifacts_dir,
            deps=deps,
        )
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
                frontmatter=source_document.frontmatter,
            )
        )
    return documents


def _matching_input_dir(
    *,
    input_dirs: list[TrendSiteInputDirectory],
    path_attr: str,
    target_path: Path,
) -> TrendSiteInputDirectory | None:
    return next(
        (
            input_info
            for input_info in input_dirs
            if getattr(input_info, path_attr) == target_path
        ),
        None,
    )


def _stage_surface_root(
    *,
    stage_root: Path,
    instance: str | None,
    source_input: TrendSiteInputDirectory | None,
) -> Path:
    language_slug = (
        str(getattr(source_input, "language_slug", None) or "").strip()
        if source_input is not None
        and getattr(source_input, "is_localized_root", False)
        else ""
    )
    if instance:
        base_root = stage_root / "Streams" / instance
        return base_root / "Localized" / language_slug if language_slug else base_root
    if language_slug:
        return stage_root / "Localized" / language_slug
    return stage_root


def _copy_sidecar_if_present(
    *,
    markdown_path: Path,
    target_dir: Path,
    presentation_sidecar_path: Callable[..., Path],
) -> None:
    source_sidecar_path = presentation_sidecar_path(note_path=markdown_path)
    if not source_sidecar_path.exists() or not source_sidecar_path.is_file():
        return
    shutil.copy2(source_sidecar_path, target_dir / source_sidecar_path.name)


def _stage_trend_documents(
    *,
    source_documents: list[TrendSiteSourceDocument],
    input_dirs: list[TrendSiteInputDirectory],
    stage_root: Path,
    resolved_output_dir: Path,
    presentation_sidecar_path: Callable[..., Path],
) -> tuple[list[str], list[str]]:
    staged_markdown_files: list[str] = []
    staged_pdf_files: list[str] = []
    has_instance_documents = any(
        bool(source_document.instance) for source_document in source_documents
    )
    for source_document in source_documents:
        source_input = _matching_input_dir(
            input_dirs=input_dirs,
            path_attr="path",
            target_path=source_document.markdown_path.parent,
        )
        surface_root = _stage_surface_root(
            stage_root=stage_root,
            instance=source_document.instance,
            source_input=source_input,
        )
        target_dir = (
            surface_root / "Trends"
            if source_document.instance
            or has_instance_documents
            or surface_root != stage_root
            else resolved_output_dir
        )
        target_dir.mkdir(parents=True, exist_ok=True)
        staged_markdown_path = target_dir / source_document.markdown_path.name
        shutil.copy2(source_document.markdown_path, staged_markdown_path)
        staged_markdown_files.append(str(staged_markdown_path.relative_to(stage_root)))
        _copy_sidecar_if_present(
            markdown_path=source_document.markdown_path,
            target_dir=target_dir,
            presentation_sidecar_path=presentation_sidecar_path,
        )
        if source_document.pdf_path is None:
            continue
        staged_pdf_path = target_dir / source_document.pdf_path.name
        shutil.copy2(source_document.pdf_path, staged_pdf_path)
        staged_pdf_files.append(str(staged_pdf_path.relative_to(stage_root)))
    return staged_markdown_files, staged_pdf_files


def _stage_item_documents(
    *,
    source_documents: list[ItemSiteSourceDocument],
    input_dirs: list[TrendSiteInputDirectory],
    stage_root: Path,
) -> list[str]:
    staged_item_files: list[str] = []
    for source_document in source_documents:
        source_input = _matching_input_dir(
            input_dirs=input_dirs,
            path_attr="inbox_path",
            target_path=source_document.markdown_path.parent,
        )
        surface_root = _stage_surface_root(
            stage_root=stage_root,
            instance=source_document.instance,
            source_input=source_input,
        )
        target_dir = surface_root / "Inbox"
        target_dir.mkdir(parents=True, exist_ok=True)
        staged_item_path = target_dir / source_document.markdown_path.name
        shutil.copy2(source_document.markdown_path, staged_item_path)
        staged_item_files.append(str(staged_item_path.relative_to(stage_root)))
    return staged_item_files


def _stage_idea_documents(
    *,
    source_documents: list[IdeaSiteSourceDocument],
    input_dirs: list[TrendSiteInputDirectory],
    stage_root: Path,
    presentation_sidecar_path: Callable[..., Path],
) -> list[str]:
    staged_idea_files: list[str] = []
    for source_document in source_documents:
        source_input = _matching_input_dir(
            input_dirs=input_dirs,
            path_attr="ideas_path",
            target_path=source_document.markdown_path.parent,
        )
        surface_root = _stage_surface_root(
            stage_root=stage_root,
            instance=source_document.instance,
            source_input=source_input,
        )
        target_dir = surface_root / "Ideas"
        target_dir.mkdir(parents=True, exist_ok=True)
        staged_idea_path = target_dir / source_document.markdown_path.name
        shutil.copy2(source_document.markdown_path, staged_idea_path)
        staged_idea_files.append(str(staged_idea_path.relative_to(stage_root)))
        _copy_sidecar_if_present(
            markdown_path=source_document.markdown_path,
            target_dir=target_dir,
            presentation_sidecar_path=presentation_sidecar_path,
        )
    return staged_idea_files


def stage_trend_site_source(
    *,
    request: TrendSiteSourceStageRequest,
    deps: TrendSiteSourceStageDeps,
) -> Path:
    normalized_item_export_scope = deps.normalize_item_export_scope(
        request.item_export_scope
    )
    resolved_input_roots = deps.coerce_site_input_specs(request.input_dir)
    resolved_input_dirs = deps.discover_trend_site_input_dirs(resolved_input_roots)
    resolved_output_dir = request.output_dir.expanduser().resolve()
    stage_root = (
        resolved_output_dir.parent
        if resolved_output_dir.name == "Trends"
        else resolved_output_dir
    )
    for input_info in resolved_input_dirs:
        if deps.paths_overlap(input_info.path, stage_root):
            raise ValueError(
                "Trend site stage output directory must not overlap the input directory"
            )
    deps.reset_stage_output_root(
        stage_root=stage_root,
        trends_output_dir=resolved_output_dir,
    )
    artifacts = _stage_source_artifacts(
        context=StageSourceArtifactsContext(
            resolved_input_dirs=resolved_input_dirs,
            request=request,
            stage_root=stage_root,
            resolved_output_dir=resolved_output_dir,
            normalized_item_export_scope=normalized_item_export_scope,
        ),
        deps=deps,
    )
    manifest = _stage_source_manifest(
        context=StageSourceManifestContext(
            resolved_input_roots=resolved_input_roots,
            resolved_input_dirs=resolved_input_dirs,
            resolved_output_dir=resolved_output_dir,
            default_language_code=request.default_language_code,
            normalized_item_export_scope=normalized_item_export_scope,
            artifacts=artifacts,
            language_slug_from_code=deps.language_slug_from_code,
        ),
    )
    manifest_path = resolved_output_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    logger.bind(
        module="site.stage",
        output_dir=str(resolved_output_dir),
        item_export_scope=normalized_item_export_scope,
        trends_total=len(artifacts.source_documents),
        ideas_total=len(artifacts.idea_source_documents),
        items_total=len(artifacts.item_selection.source_documents),
        items_available_total=artifacts.item_selection.available_total,
        items_unreferenced_total=artifacts.item_selection.unreferenced_total,
        pdf_total=len(artifacts.staged_pdf_files),
    ).info("Trend site source staging completed")
    return manifest_path


def _stage_source_artifacts(
    *,
    context: StageSourceArtifactsContext,
    deps: TrendSiteSourceStageDeps,
) -> StageSourceArtifacts:
    source_documents = deps.load_trend_source_documents(
        input_dirs=context.resolved_input_dirs,
        limit=context.request.limit,
    )
    idea_source_documents = deps.load_idea_source_documents(
        input_dirs=context.resolved_input_dirs,
        limit=context.request.limit,
    )
    item_selection = deps.select_item_source_documents(
        input_dirs=context.resolved_input_dirs,
        trend_source_documents=source_documents,
        idea_source_documents=idea_source_documents,
        item_export_scope=context.normalized_item_export_scope,
    )
    staged_markdown_files, staged_pdf_files = _stage_trend_documents(
        source_documents=source_documents,
        input_dirs=context.resolved_input_dirs,
        stage_root=context.stage_root,
        resolved_output_dir=context.resolved_output_dir,
        presentation_sidecar_path=deps.presentation_sidecar_path,
    )
    staged_item_files = _stage_item_documents(
        source_documents=item_selection.source_documents,
        input_dirs=context.resolved_input_dirs,
        stage_root=context.stage_root,
    )
    staged_idea_files = _stage_idea_documents(
        source_documents=idea_source_documents,
        input_dirs=context.resolved_input_dirs,
        stage_root=context.stage_root,
        presentation_sidecar_path=deps.presentation_sidecar_path,
    )
    return StageSourceArtifacts(
        source_documents=source_documents,
        idea_source_documents=idea_source_documents,
        item_selection=item_selection,
        staged_markdown_files=staged_markdown_files,
        staged_idea_files=staged_idea_files,
        staged_item_files=staged_item_files,
        staged_pdf_files=staged_pdf_files,
    )


def _stage_source_manifest(
    *,
    context: StageSourceManifestContext,
) -> dict[str, Any]:
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "input_dir": (
            str(context.resolved_input_roots[0].path)
            if len(context.resolved_input_roots) == 1
            else [str(input_spec.path) for input_spec in context.resolved_input_roots]
        ),
        "input_dirs": [
            {
                "path": str(input_info.path),
                "ideas_path": str(input_info.ideas_path)
                if input_info.ideas_path is not None
                else None,
                "inbox_path": str(input_info.inbox_path)
                if input_info.inbox_path is not None
                else None,
                "instance": input_info.instance,
                "language_code": input_info.language_code,
                "language_slug": input_info.language_slug,
                "is_localized_root": bool(input_info.is_localized_root),
            }
            for input_info in context.resolved_input_dirs
        ],
        "output_dir": str(context.resolved_output_dir),
        "default_language_code": context.language_slug_from_code(
            context.default_language_code
        ),
        "languages": sorted(
            {
                str(input_info.language_slug or "").strip()
                for input_info in context.resolved_input_dirs
                if str(input_info.language_slug or "").strip()
            }
        ),
        "item_export_scope": context.normalized_item_export_scope,
        "trends_total": len(context.artifacts.source_documents),
        "ideas_total": len(context.artifacts.idea_source_documents),
        "items_total": len(context.artifacts.item_selection.source_documents),
        "items_available_total": context.artifacts.item_selection.available_total,
        "items_unreferenced_total": context.artifacts.item_selection.unreferenced_total,
        "pdf_total": len(context.artifacts.staged_pdf_files),
        "files": {
            "markdown": context.artifacts.staged_markdown_files,
            "ideas_markdown": context.artifacts.staged_idea_files,
            "items_markdown": context.artifacts.staged_item_files,
            "pdf": context.artifacts.staged_pdf_files,
        },
    }


__all__ = [
    "SiteInputDiscoveryDeps",
    "SiteItemSourceLoadDeps",
    "SiteLanguageDiscoveryDeps",
    "SiteLanguageDiscoveryState",
    "SiteReferenceCollectionDeps",
    "StageSourceArtifacts",
    "StageSourceArtifactsContext",
    "StageSourceManifestContext",
    "TrendSiteDocumentLoadDeps",
    "TrendBrowserBodyContext",
    "TrendSiteSourceStageDeps",
    "TrendSiteSourceStageRequest",
    "collect_referenced_item_source_keys",
    "discover_site_language_inputs",
    "discover_trend_site_input_dirs",
    "load_trend_site_documents",
    "load_item_source_documents",
    "stage_trend_site_source",
]
