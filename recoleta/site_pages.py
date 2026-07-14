from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime, timezone
import html
import json
from pathlib import Path
from typing import Any, Callable

from loguru import logger

from recoleta.site_email_links import write_email_links_artifact
from recoleta.site_models import (
    IdeaSiteDocument,
    IdeaSiteSourceDocument,
    ItemSiteDocument,
    ItemSiteSelection,
    SiteSourceKey,
    TrendSiteDocument,
    TrendSiteInputDirectory,
    TrendSiteInputSpec,
    TrendSiteSourceDocument,
)


SITE_CARD_PAGE_SIZE = 12
SITE_DENSE_PAGE_SIZE = 24
SITE_TOPIC_COLUMN_PAGE_SIZE = 6


@dataclass(frozen=True, slots=True)
class SitePagination:
    current_page: int
    total_pages: int
    page_path: Path
    page_paths: tuple[Path, ...]


@dataclass(frozen=True, slots=True)
class SiteIndexPageArtifacts:
    trends_index_pages: tuple[Path, ...]
    ideas_index_pages: tuple[Path, ...]
    topics_index_pages: tuple[Path, ...]
    archive_pages: tuple[Path, ...]


@dataclass(frozen=True, slots=True)
class SitePageShellInput:
    title: str
    page_path: Path
    output_dir: Path
    page_heading: str
    page_subtitle: str
    body_class: str
    active_nav: str
    content_html: str
    repo_url: str
    show_page_hero: bool = False


@dataclass(frozen=True, slots=True)
class SingleLanguageSiteExportRequest:
    input_dir: Path | TrendSiteInputSpec | tuple[Path | TrendSiteInputSpec, ...]
    output_dir: Path
    limit: int | None = None
    item_export_scope: str = "linked"
    include_localized_children: bool = True


@dataclass(frozen=True, slots=True)
class SingleLanguageSiteExportDeps:
    normalize_item_export_scope: Callable[[str | None], str]
    coerce_site_input_specs: Callable[..., list[TrendSiteInputSpec]]
    discover_trend_site_input_dirs: Callable[..., list[TrendSiteInputDirectory]]
    paths_overlap: Callable[..., bool]
    reset_directory: Callable[[Path], None]
    load_trend_source_documents: Callable[..., list[TrendSiteSourceDocument]]
    load_idea_source_documents: Callable[..., list[IdeaSiteSourceDocument]]
    select_item_source_documents: Callable[..., ItemSiteSelection]
    load_item_site_documents: Callable[
        ..., tuple[list[ItemSiteDocument], dict[SiteSourceKey, Path]]
    ]
    load_trend_site_documents: Callable[..., list[TrendSiteDocument]]
    site_source_key: Callable[..., SiteSourceKey]
    load_idea_site_documents: Callable[
        ..., tuple[list[IdeaSiteDocument], dict[SiteSourceKey, Path]]
    ]
    topic_slug: Callable[[str], str]
    render_home_page: Callable[..., str]
    render_trends_index_page: Callable[..., str]
    render_archive_page: Callable[..., str]
    render_topics_index_page: Callable[..., str]
    render_ideas_index_page: Callable[..., str]
    render_detail_page: Callable[..., str]
    render_item_page: Callable[..., str]
    render_idea_page: Callable[..., str]
    render_topic_page: Callable[..., str]
    site_css: str


@dataclass(slots=True)
class SingleLanguageSiteExportArtifacts:
    resolved_input_roots: list[TrendSiteInputSpec]
    resolved_input_dirs: list[TrendSiteInputDirectory]
    resolved_output_dir: Path
    item_selection: ItemSiteSelection
    documents: list[TrendSiteDocument]
    item_documents: list[ItemSiteDocument]
    idea_documents: list[IdeaSiteDocument]
    topic_pages: dict[str, Path]
    label_by_topic_slug: dict[str, str]
    topic_documents: dict[str, list[TrendSiteDocument]]
    idea_documents_by_topic: dict[str, list[IdeaSiteDocument]]


def _linked_page_by_source_key(
    *,
    item_pages_by_source_key: dict[SiteSourceKey, Path],
    documents: list[TrendSiteDocument],
    site_source_key: Callable[..., SiteSourceKey],
) -> dict[SiteSourceKey, Path]:
    linked_page_by_source_key = dict(item_pages_by_source_key)
    linked_page_by_source_key.update(
        {
            site_source_key(
                markdown_path=document.markdown_path,
                instance=document.instance,
            ): document.page_path
            for document in documents
        }
    )
    return linked_page_by_source_key


def _nav_link(*, label: str, href: str, key: str, active_nav: str) -> str:
    class_name = "nav-link is-active" if key == active_nav else "nav-link"
    return f"<a class='{class_name}' href='{href}'>{label}</a>"


def _page_nav_links(
    *,
    spec: SitePageShellInput,
    site_href: Callable[..., str],
) -> tuple[str, str, str, str, str]:
    index_href = site_href(
        from_page=spec.page_path, to_page=spec.output_dir / "index.html"
    )
    return (
        index_href,
        site_href(
            from_page=spec.page_path, to_page=spec.output_dir / "trends" / "index.html"
        ),
        site_href(
            from_page=spec.page_path, to_page=spec.output_dir / "ideas" / "index.html"
        ),
        site_href(
            from_page=spec.page_path, to_page=spec.output_dir / "topics" / "index.html"
        ),
        site_href(from_page=spec.page_path, to_page=spec.output_dir / "archive.html"),
    )


def _nav_caption_html(page_subtitle: str) -> str:
    if not page_subtitle:
        return ""
    return f"<div class='nav-caption'>{html.escape(page_subtitle)}</div>"


def _page_hero_html(*, spec: SitePageShellInput) -> str:
    if not spec.show_page_hero:
        return ""
    return (
        "<section class='page-hero'>"
        f"<div class='hero-kicker'>{html.escape(spec.page_subtitle)}</div>"
        f"<h1 class='page-title'>{html.escape(spec.page_heading)}</h1>"
        "</section>"
    )


def render_site_page_shell(
    *,
    spec: SitePageShellInput,
    site_href: Callable[..., str],
) -> str:
    stylesheet_href = site_href(
        from_page=spec.page_path,
        to_page=spec.output_dir / "assets" / "site.css",
    )
    index_href, trends_href, ideas_href, topics_href, archive_href = _page_nav_links(
        spec=spec,
        site_href=site_href,
    )
    return (
        "<!doctype html>"
        "<html lang='zh-CN'>"
        "<head>"
        "<meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width, initial-scale=1'>"
        f"<title>{html.escape(spec.title)}</title>"
        "<meta name='theme-color' content='#10273f'>"
        f"<link rel='stylesheet' href='{stylesheet_href}'>"
        "</head>"
        f"<body class='{spec.body_class}'>"
        "<div class='site-bg'></div>"
        "<div class='site-shell'>"
        "<header class='site-header'>"
        "<div class='nav-brand-wrap'>"
        f"<a class='nav-brand' href='{index_href}'>Recoleta Trends</a>"
        f"{_nav_caption_html(spec.page_subtitle)}"
        "</div>"
        "<nav class='nav-links'>"
        f"{_nav_link(label='Home', href=index_href, key='home', active_nav=spec.active_nav)}"
        f"{_nav_link(label='Trends', href=trends_href, key='trends', active_nav=spec.active_nav)}"
        f"{_nav_link(label='Ideas', href=ideas_href, key='ideas', active_nav=spec.active_nav)}"
        f"{_nav_link(label='Topics', href=topics_href, key='topics', active_nav=spec.active_nav)}"
        f"{_nav_link(label='Archive', href=archive_href, key='archive', active_nav=spec.active_nav)}"
        "</nav>"
        "<div class='nav-actions'>"
        "<div class='nav-utility-cluster'></div>"
        f"<a class='nav-link nav-link-external nav-link-repo' href='{html.escape(spec.repo_url, quote=True)}'>GitHub</a>"
        "</div>"
        "</header>"
        "<main class='site-main'>"
        f"{_page_hero_html(spec=spec)}"
        f"{spec.content_html}"
        "</main>"
        "</div>"
        "</body>"
        "</html>"
    )


def _validate_export_output_dir(
    *,
    resolved_input_dirs: list[TrendSiteInputDirectory],
    resolved_output_dir: Path,
    paths_overlap: Callable[..., bool],
) -> None:
    for input_info in resolved_input_dirs:
        if paths_overlap(input_info.path, resolved_output_dir):
            raise ValueError(
                "Trend site output directory must not overlap the input directory"
            )


def _prepare_export_output_dir(
    *,
    resolved_output_dir: Path,
    reset_directory: Callable[[Path], None],
    site_css: str,
) -> None:
    reset_directory(resolved_output_dir)
    for name in ("assets", "ideas", "items", "topics"):
        (resolved_output_dir / name).mkdir(parents=True, exist_ok=True)
    (resolved_output_dir / "assets" / "site.css").write_text(
        site_css.strip() + "\n", encoding="utf-8"
    )
    (resolved_output_dir / ".nojekyll").write_text("", encoding="utf-8")


def _collect_topic_page_artifacts(
    *,
    documents: list[TrendSiteDocument],
    idea_documents: list[IdeaSiteDocument],
    resolved_output_dir: Path,
    topic_slug: Callable[[str], str],
) -> tuple[
    dict[str, str],
    dict[str, list[TrendSiteDocument]],
    dict[str, list[IdeaSiteDocument]],
    dict[str, Path],
]:
    label_by_topic_slug: dict[str, str] = {}
    topic_documents: dict[str, list[TrendSiteDocument]] = defaultdict(list)
    idea_documents_by_topic: dict[str, list[IdeaSiteDocument]] = defaultdict(list)
    for document in documents:
        for topic in document.topics:
            slug = topic_slug(topic)
            label_by_topic_slug.setdefault(slug, topic)
            topic_documents[slug].append(document)
    for document in idea_documents:
        for topic in document.topics:
            slug = topic_slug(topic)
            label_by_topic_slug.setdefault(slug, topic)
            idea_documents_by_topic[slug].append(document)
    topic_pages = {
        slug: resolved_output_dir / "topics" / f"{slug}.html"
        for slug in sorted(
            set(topic_documents.keys()) | set(idea_documents_by_topic.keys())
        )
    }
    return label_by_topic_slug, topic_documents, idea_documents_by_topic, topic_pages


def _load_export_artifacts(
    *,
    request: SingleLanguageSiteExportRequest,
    deps: SingleLanguageSiteExportDeps,
) -> SingleLanguageSiteExportArtifacts:
    normalized_item_export_scope = deps.normalize_item_export_scope(
        request.item_export_scope
    )
    resolved_input_roots = deps.coerce_site_input_specs(request.input_dir)
    resolved_input_dirs = deps.discover_trend_site_input_dirs(
        resolved_input_roots,
        include_localized_children=request.include_localized_children,
    )
    resolved_output_dir = request.output_dir.expanduser().resolve()
    _validate_export_output_dir(
        resolved_input_dirs=resolved_input_dirs,
        resolved_output_dir=resolved_output_dir,
        paths_overlap=deps.paths_overlap,
    )
    _prepare_export_output_dir(
        resolved_output_dir=resolved_output_dir,
        reset_directory=deps.reset_directory,
        site_css=deps.site_css,
    )

    trend_source_documents = deps.load_trend_source_documents(
        input_dirs=resolved_input_dirs,
        limit=request.limit,
    )
    idea_source_documents = deps.load_idea_source_documents(
        input_dirs=resolved_input_dirs,
        limit=request.limit,
    )
    item_selection = deps.select_item_source_documents(
        input_dirs=resolved_input_dirs,
        trend_source_documents=trend_source_documents,
        idea_source_documents=idea_source_documents,
        item_export_scope=normalized_item_export_scope,
    )
    item_documents, item_pages_by_source_key = deps.load_item_site_documents(
        source_documents=item_selection.source_documents,
        output_dir=resolved_output_dir,
    )
    documents = deps.load_trend_site_documents(
        source_documents=trend_source_documents,
        output_dir=resolved_output_dir,
        item_pages_by_source_key=item_pages_by_source_key,
    )
    linked_page_by_source_key = _linked_page_by_source_key(
        item_pages_by_source_key=item_pages_by_source_key,
        documents=documents,
        site_source_key=deps.site_source_key,
    )
    idea_documents, _ = deps.load_idea_site_documents(
        source_documents=idea_source_documents,
        output_dir=resolved_output_dir,
        linked_page_by_source_key=linked_page_by_source_key,
    )
    label_by_topic_slug, topic_documents, idea_documents_by_topic, topic_pages = (
        _collect_topic_page_artifacts(
            documents=documents,
            idea_documents=idea_documents,
            resolved_output_dir=resolved_output_dir,
            topic_slug=deps.topic_slug,
        )
    )
    return SingleLanguageSiteExportArtifacts(
        resolved_input_roots=resolved_input_roots,
        resolved_input_dirs=resolved_input_dirs,
        resolved_output_dir=resolved_output_dir,
        item_selection=item_selection,
        documents=documents,
        item_documents=item_documents,
        idea_documents=idea_documents,
        topic_pages=topic_pages,
        label_by_topic_slug=label_by_topic_slug,
        topic_documents=topic_documents,
        idea_documents_by_topic=idea_documents_by_topic,
    )


def _page_count(*, item_count: int, page_size: int) -> int:
    return max(1, (item_count + page_size - 1) // page_size)


def _paginated_page_paths(
    *,
    first_page_path: Path,
    total_pages: int,
) -> tuple[Path, ...]:
    paths = [first_page_path]
    for page_number in range(2, total_pages + 1):
        pagination_root = (
            first_page_path.parent
            if first_page_path.name == "index.html"
            else first_page_path.with_suffix("")
        )
        page_path = pagination_root / "page" / str(page_number) / "index.html"
        paths.append(page_path)
    return tuple(paths)


def _site_paginations(
    *,
    first_page_path: Path,
    total_pages: int,
) -> tuple[SitePagination, ...]:
    page_paths = _paginated_page_paths(
        first_page_path=first_page_path,
        total_pages=total_pages,
    )
    return tuple(
        SitePagination(
            current_page=page_number,
            total_pages=total_pages,
            page_path=page_path,
            page_paths=page_paths,
        )
        for page_number, page_path in enumerate(page_paths, start=1)
    )


def _page_slice_bounds(
    *, pagination: SitePagination, page_size: int
) -> tuple[int, int]:
    start = (pagination.current_page - 1) * page_size
    return start, start + page_size


def _write_html_page(*, page_path: Path, content: str) -> None:
    page_path.parent.mkdir(parents=True, exist_ok=True)
    page_path.write_text(content, encoding="utf-8")


def _write_index_pages(
    *,
    artifacts: SingleLanguageSiteExportArtifacts,
    deps: SingleLanguageSiteExportDeps,
) -> SiteIndexPageArtifacts:
    output_dir = artifacts.resolved_output_dir
    (output_dir / "index.html").write_text(
        deps.render_home_page(
            documents=artifacts.documents,
            idea_documents=artifacts.idea_documents,
            output_dir=output_dir,
            topic_pages=artifacts.topic_pages,
        ),
        encoding="utf-8",
    )

    trends_paginations = _site_paginations(
        first_page_path=output_dir / "trends" / "index.html",
        total_pages=_page_count(
            item_count=len(artifacts.documents),
            page_size=SITE_CARD_PAGE_SIZE,
        ),
    )
    for pagination in trends_paginations:
        start, stop = _page_slice_bounds(
            pagination=pagination,
            page_size=SITE_CARD_PAGE_SIZE,
        )
        _write_html_page(
            page_path=pagination.page_path,
            content=deps.render_trends_index_page(
                documents=artifacts.documents[start:stop],
                total_documents=len(artifacts.documents),
                output_dir=output_dir,
                topic_pages=artifacts.topic_pages,
                pagination=pagination,
            ),
        )

    archive_paginations = _site_paginations(
        first_page_path=output_dir / "archive.html",
        total_pages=_page_count(
            item_count=len(artifacts.documents),
            page_size=SITE_DENSE_PAGE_SIZE,
        ),
    )
    for pagination in archive_paginations:
        start, stop = _page_slice_bounds(
            pagination=pagination,
            page_size=SITE_DENSE_PAGE_SIZE,
        )
        _write_html_page(
            page_path=pagination.page_path,
            content=deps.render_archive_page(
                documents=artifacts.documents[start:stop],
                total_documents=len(artifacts.documents),
                output_dir=output_dir,
                pagination=pagination,
            ),
        )

    topics_paginations = _site_paginations(
        first_page_path=output_dir / "topics" / "index.html",
        total_pages=_page_count(
            item_count=len(artifacts.topic_pages),
            page_size=SITE_DENSE_PAGE_SIZE,
        ),
    )
    for pagination in topics_paginations:
        _write_html_page(
            page_path=pagination.page_path,
            content=deps.render_topics_index_page(
                documents=artifacts.documents,
                idea_documents=artifacts.idea_documents,
                output_dir=output_dir,
                topic_pages=artifacts.topic_pages,
                pagination=pagination,
                page_size=SITE_DENSE_PAGE_SIZE,
            ),
        )

    ideas_paginations = _site_paginations(
        first_page_path=output_dir / "ideas" / "index.html",
        total_pages=_page_count(
            item_count=len(artifacts.idea_documents),
            page_size=SITE_CARD_PAGE_SIZE,
        ),
    )
    for pagination in ideas_paginations:
        start, stop = _page_slice_bounds(
            pagination=pagination,
            page_size=SITE_CARD_PAGE_SIZE,
        )
        _write_html_page(
            page_path=pagination.page_path,
            content=deps.render_ideas_index_page(
                documents=artifacts.idea_documents[start:stop],
                total_documents=len(artifacts.idea_documents),
                output_dir=output_dir,
                topic_pages=artifacts.topic_pages,
                pagination=pagination,
            ),
        )

    return SiteIndexPageArtifacts(
        trends_index_pages=tuple(
            pagination.page_path for pagination in trends_paginations
        ),
        ideas_index_pages=tuple(
            pagination.page_path for pagination in ideas_paginations
        ),
        topics_index_pages=tuple(
            pagination.page_path for pagination in topics_paginations
        ),
        archive_pages=tuple(pagination.page_path for pagination in archive_paginations),
    )


def _write_detail_pages(
    *,
    artifacts: SingleLanguageSiteExportArtifacts,
    deps: SingleLanguageSiteExportDeps,
) -> dict[str, tuple[Path, ...]]:
    output_dir = artifacts.resolved_output_dir
    for idx, document in enumerate(artifacts.documents):
        previous_document = artifacts.documents[idx - 1] if idx > 0 else None
        next_document = (
            artifacts.documents[idx + 1] if idx + 1 < len(artifacts.documents) else None
        )
        document.page_path.write_text(
            deps.render_detail_page(
                document=document,
                output_dir=output_dir,
                topic_pages=artifacts.topic_pages,
                previous_document=previous_document,
                next_document=next_document,
            ),
            encoding="utf-8",
        )
    for document in artifacts.item_documents:
        document.page_path.write_text(
            deps.render_item_page(
                document=document,
                output_dir=output_dir,
                topic_pages=artifacts.topic_pages,
            ),
            encoding="utf-8",
        )
    for document in artifacts.idea_documents:
        document.page_path.write_text(
            deps.render_idea_page(
                document=document,
                output_dir=output_dir,
                topic_pages=artifacts.topic_pages,
            ),
            encoding="utf-8",
        )
    topic_collection_pages: dict[str, tuple[Path, ...]] = {}
    for slug, first_page_path in artifacts.topic_pages.items():
        topic_documents = artifacts.topic_documents[slug]
        topic_idea_documents = artifacts.idea_documents_by_topic.get(slug, [])
        paginations = _site_paginations(
            first_page_path=first_page_path,
            total_pages=max(
                _page_count(
                    item_count=len(topic_documents),
                    page_size=SITE_TOPIC_COLUMN_PAGE_SIZE,
                ),
                _page_count(
                    item_count=len(topic_idea_documents),
                    page_size=SITE_TOPIC_COLUMN_PAGE_SIZE,
                ),
            ),
        )
        topic_collection_pages[slug] = tuple(
            pagination.page_path for pagination in paginations
        )
        for pagination in paginations:
            _write_html_page(
                page_path=pagination.page_path,
                content=deps.render_topic_page(
                    topic=artifacts.label_by_topic_slug[slug],
                    topic_slug=slug,
                    documents=topic_documents,
                    idea_documents=topic_idea_documents,
                    total_documents=len(topic_documents),
                    total_idea_documents=len(topic_idea_documents),
                    output_dir=output_dir,
                    topic_pages=artifacts.topic_pages,
                    pagination=pagination,
                    page_size=SITE_TOPIC_COLUMN_PAGE_SIZE,
                ),
            )
    return topic_collection_pages


def _relative_site_paths(*, output_dir: Path, paths: Iterable[Path]) -> list[str]:
    return [str(path.relative_to(output_dir)) for path in paths]


def _relative_document_page_paths(
    *,
    output_dir: Path,
    documents: Iterable[TrendSiteDocument | IdeaSiteDocument | ItemSiteDocument],
) -> list[str]:
    return _relative_site_paths(
        output_dir=output_dir,
        paths=(document.page_path for document in documents),
    )


def _topic_collection_manifest_paths(
    *,
    output_dir: Path,
    topic_collection_pages: dict[str, tuple[Path, ...]],
) -> dict[str, list[str]]:
    return {
        slug: _relative_site_paths(output_dir=output_dir, paths=paths)
        for slug, paths in topic_collection_pages.items()
    }


def _single_language_export_files_manifest(
    *,
    artifacts: SingleLanguageSiteExportArtifacts,
    index_pages: SiteIndexPageArtifacts,
    topic_collection_pages: dict[str, tuple[Path, ...]],
) -> dict[str, Any]:
    output_dir = artifacts.resolved_output_dir
    return {
        "index": "index.html",
        "archive": "archive.html",
        "nojekyll": ".nojekyll",
        "trends_index": "trends/index.html",
        "ideas_index": "ideas/index.html",
        "topics_index": "topics/index.html",
        "stylesheet": "assets/site.css",
        "trends_index_pages": _relative_site_paths(
            output_dir=output_dir,
            paths=index_pages.trends_index_pages,
        ),
        "ideas_index_pages": _relative_site_paths(
            output_dir=output_dir,
            paths=index_pages.ideas_index_pages,
        ),
        "topics_index_pages": _relative_site_paths(
            output_dir=output_dir,
            paths=index_pages.topics_index_pages,
        ),
        "archive_pages": _relative_site_paths(
            output_dir=output_dir,
            paths=index_pages.archive_pages,
        ),
        "topic_collection_pages": _topic_collection_manifest_paths(
            output_dir=output_dir,
            topic_collection_pages=topic_collection_pages,
        ),
        "trend_pages": _relative_document_page_paths(
            output_dir=output_dir,
            documents=artifacts.documents,
        ),
        "idea_pages": _relative_document_page_paths(
            output_dir=output_dir,
            documents=artifacts.idea_documents,
        ),
        "item_pages": _relative_document_page_paths(
            output_dir=output_dir,
            documents=artifacts.item_documents,
        ),
        "topic_pages": _relative_site_paths(
            output_dir=output_dir,
            paths=artifacts.topic_pages.values(),
        ),
    }


def _single_language_export_manifest(
    *,
    artifacts: SingleLanguageSiteExportArtifacts,
    normalized_item_export_scope: str,
    index_pages: SiteIndexPageArtifacts,
    topic_collection_pages: dict[str, tuple[Path, ...]],
) -> dict[str, Any]:
    output_dir = artifacts.resolved_output_dir
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "input_dir": (
            str(artifacts.resolved_input_roots[0].path)
            if len(artifacts.resolved_input_roots) == 1
            else [str(input_spec.path) for input_spec in artifacts.resolved_input_roots]
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
            }
            for input_info in artifacts.resolved_input_dirs
        ],
        "output_dir": str(output_dir),
        "item_export_scope": normalized_item_export_scope,
        "trends_total": len(artifacts.documents),
        "ideas_total": len(artifacts.idea_documents),
        "items_total": len(artifacts.item_documents),
        "items_available_total": artifacts.item_selection.available_total,
        "items_unreferenced_total": artifacts.item_selection.unreferenced_total,
        "topics_total": len(artifacts.topic_pages),
        "pagination": {
            "card_page_size": SITE_CARD_PAGE_SIZE,
            "dense_page_size": SITE_DENSE_PAGE_SIZE,
            "topic_column_page_size": SITE_TOPIC_COLUMN_PAGE_SIZE,
        },
        "files": _single_language_export_files_manifest(
            artifacts=artifacts,
            index_pages=index_pages,
            topic_collection_pages=topic_collection_pages,
        ),
    }


def export_trend_static_site_single_language(
    *,
    request: SingleLanguageSiteExportRequest,
    deps: SingleLanguageSiteExportDeps,
) -> Path:
    normalized_item_export_scope = deps.normalize_item_export_scope(
        request.item_export_scope
    )
    artifacts = _load_export_artifacts(request=request, deps=deps)
    index_pages = _write_index_pages(artifacts=artifacts, deps=deps)
    topic_collection_pages = _write_detail_pages(artifacts=artifacts, deps=deps)
    manifest = _single_language_export_manifest(
        artifacts=artifacts,
        normalized_item_export_scope=normalized_item_export_scope,
        index_pages=index_pages,
        topic_collection_pages=topic_collection_pages,
    )
    manifest_path = artifacts.resolved_output_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_email_links_artifact(
        site_output_dir=artifacts.resolved_output_dir,
        pages_by_source_markdown={
            str(document.markdown_path.resolve()): str(
                document.page_path.relative_to(artifacts.resolved_output_dir)
            )
            for document in [
                *artifacts.documents,
                *artifacts.item_documents,
                *artifacts.idea_documents,
            ]
        },
        topic_pages_by_slug={
            slug: str(path.relative_to(artifacts.resolved_output_dir))
            for slug, path in artifacts.topic_pages.items()
        },
    )
    logger.bind(
        module="site.build",
        output_dir=str(artifacts.resolved_output_dir),
        item_export_scope=normalized_item_export_scope,
        trends_total=len(artifacts.documents),
        ideas_total=len(artifacts.idea_documents),
        items_total=len(artifacts.item_documents),
        items_available_total=artifacts.item_selection.available_total,
        items_unreferenced_total=artifacts.item_selection.unreferenced_total,
        topics_total=len(artifacts.topic_pages),
    ).info("Trend static site export completed")
    return manifest_path


__all__ = [
    "SingleLanguageSiteExportDeps",
    "SingleLanguageSiteExportRequest",
    "SitePagination",
    "SitePageShellInput",
    "export_trend_static_site_single_language",
    "render_site_page_shell",
]
