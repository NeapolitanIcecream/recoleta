from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import html
import json
from pathlib import Path, PurePosixPath
import posixpath
import re
from typing import Any
from urllib.parse import urljoin, urlparse
from xml.etree import ElementTree

from bs4 import BeautifulSoup, Tag


_ATOM_NAMESPACE = "http://www.w3.org/2005/Atom"
_SITEMAP_NAMESPACE = "http://www.sitemaps.org/schemas/sitemap/0.9"
_DATE_IN_STEM_RE = re.compile(r"--(?P<date>\d{4}-\d{2}-\d{2})--")
_DESCRIPTION_MAX_CHARS = 160
_DISCOVERY_TAG_RE = re.compile(
    r"<(?:meta|link)\b"
    r"(?=[^>]*\bdata-recoleta-discovery=(?:'true'|\"true\"))"
    r"[^>]*>\s*",
    flags=re.IGNORECASE,
)


@dataclass(frozen=True, slots=True)
class _LanguageSite:
    slug: str
    code: str
    root: Path
    relative_html_paths: frozenset[str]


@dataclass(frozen=True, slots=True)
class _DiscoveryContext:
    output_dir: Path
    language_sites: tuple[_LanguageSite, ...]
    default_language_slug: str | None
    public_site_url: str | None


@dataclass(frozen=True, slots=True)
class _PageMetadata:
    relative_path: str
    within_language: str
    title: str
    description: str
    indexable: bool


def normalize_public_site_url(value: str | None) -> str | None:
    normalized = str(value or "").strip().rstrip("/")
    if not normalized:
        return None
    parsed = urlparse(normalized)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("PUBLIC_SITE_URL must be an absolute http(s) URL")
    if parsed.query or parsed.fragment:
        raise ValueError("PUBLIC_SITE_URL must not contain a query or fragment")
    return normalized


def _site_url(*, public_site_url: str, relative_path: str) -> str:
    return urljoin(public_site_url.rstrip("/") + "/", relative_path)


def _relative_html_paths(root: Path) -> frozenset[str]:
    return frozenset(
        str(path.relative_to(root)).replace("\\", "/")
        for path in root.rglob("*.html")
    )


def _manifest_language_site(
    *,
    output_dir: Path,
    raw_slug: Any,
    raw_code: Any,
) -> _LanguageSite | None:
    slug = str(raw_slug or "").strip()
    code = str(raw_code or "").strip()
    root = output_dir / slug
    if not slug or not code or not root.is_dir():
        return None
    return _LanguageSite(
        slug=slug,
        code=code,
        root=root,
        relative_html_paths=_relative_html_paths(root),
    )


def _single_language_code(output_dir: Path) -> str:
    index_path = output_dir / "index.html"
    if not index_path.is_file():
        return "en"
    soup = BeautifulSoup(index_path.read_text(encoding="utf-8"), "html.parser")
    html_tag = soup.find("html")
    if not isinstance(html_tag, Tag):
        return "en"
    return str(html_tag.get("lang") or "").strip() or "en"


def _manifest_language_sites(
    *,
    output_dir: Path,
    manifest: dict[str, Any],
) -> tuple[list[_LanguageSite], str | None]:
    language_codes = manifest.get("language_codes")
    if isinstance(language_codes, dict) and language_codes:
        candidates = (
            _manifest_language_site(
                output_dir=output_dir,
                raw_slug=raw_slug,
                raw_code=raw_code,
            )
            for raw_slug, raw_code in language_codes.items()
        )
        sites = [site for site in candidates if site is not None]
        return sites, str(manifest.get("default_language_code") or "").strip() or None

    code = _single_language_code(output_dir)
    return [
        _LanguageSite(
            slug="",
            code=code,
            root=output_dir,
            relative_html_paths=_relative_html_paths(output_dir),
        )
    ], code


def _local_page_parts(*, relative_path: str, language_slug: str) -> tuple[str, ...]:
    parts = PurePosixPath(relative_path).parts
    if language_slug and parts and parts[0] == language_slug:
        return tuple(parts[1:])
    return tuple(parts)


def _is_indexable_page(*, relative_path: str, language_slug: str) -> bool:
    parts = _local_page_parts(
        relative_path=relative_path,
        language_slug=language_slug,
    )
    if not parts:
        return False
    if parts[0] == "items":
        return False
    if "page" in parts:
        return False
    if parts[0] == "topics" and len(parts) == 2 and parts[1] != "index.html":
        return False
    return True


def _clean_description(value: str) -> str:
    normalized = " ".join(str(value or "").split())
    if len(normalized) <= _DESCRIPTION_MAX_CHARS:
        return normalized
    clipped = normalized[: _DESCRIPTION_MAX_CHARS + 1]
    if " " in clipped:
        clipped = clipped.rsplit(" ", 1)[0]
    return clipped.rstrip(" ,.;:") + "…"


def _page_description(*, soup: BeautifulSoup, language_code: str) -> str:
    selectors = (
        ".home-dek",
        ".detail-content p",
        ".home-feature-excerpt",
        ".card-excerpt",
        "main p",
    )
    for selector in selectors:
        node = soup.select_one(selector)
        if isinstance(node, Tag):
            description = _clean_description(node.get_text(" ", strip=True))
            if description:
                return description
    if str(language_code).lower().startswith("zh"):
        return "Recoleta 持续研究雷达生成的趋势、想法与来源记录。"
    return "Traceable trends, ideas, and source notes from a continuously operated Recoleta research radar."


def _page_title(soup: BeautifulSoup) -> str:
    if soup.title is not None:
        title = " ".join(soup.title.get_text(" ", strip=True).split())
        if title:
            return title
    heading = soup.select_one("h1")
    if isinstance(heading, Tag):
        title = " ".join(heading.get_text(" ", strip=True).split())
        if title:
            return title
    return "Recoleta Research Radar"


def _open_graph_type(*, relative_path: str, language_slug: str) -> str:
    parts = _local_page_parts(
        relative_path=relative_path,
        language_slug=language_slug,
    )
    if len(parts) == 2 and parts[0] in {"trends", "ideas"}:
        return "article"
    return "website"


def _page_feed_href(*, page_path: Path, language_site: _LanguageSite) -> str:
    feed_path = language_site.root / "feed.xml"
    return posixpath.relpath(
        str(feed_path.relative_to(language_site.root.parent)).replace("\\", "/"),
        start=str(page_path.parent.relative_to(language_site.root.parent)).replace(
            "\\", "/"
        ),
    )


def _discovery_meta(*, attribute: str, key: str, content: str) -> str:
    return (
        "<meta data-recoleta-discovery='true' "
        f"{attribute}='{html.escape(key, quote=True)}' "
        f"content='{html.escape(content, quote=True)}'>"
    )


def _discovery_link(*, rel: str, href: str, **attrs: str) -> str:
    rendered_attrs = "".join(
        f" {key}='{html.escape(value, quote=True)}'"
        for key, value in attrs.items()
    )
    return (
        "<link data-recoleta-discovery='true' "
        f"rel='{html.escape(rel, quote=True)}' "
        f"href='{html.escape(href, quote=True)}'{rendered_attrs}>"
    )


def _inject_discovery_head_tags(*, source: str, tags: list[str]) -> str:
    cleaned = _DISCOVERY_TAG_RE.sub("", source)
    closing_head = re.search(r"</head\s*>", cleaned, flags=re.IGNORECASE)
    if closing_head is None:
        return cleaned
    return (
        cleaned[: closing_head.start()]
        + "".join(tags)
        + cleaned[closing_head.start() :]
    )


def _read_page_metadata(
    *,
    html_path: Path,
    context: _DiscoveryContext,
    language_site: _LanguageSite,
    source: str,
) -> _PageMetadata:
    relative_path = str(html_path.relative_to(context.output_dir)).replace("\\", "/")
    within_language = str(html_path.relative_to(language_site.root)).replace(
        "\\", "/"
    )
    soup = BeautifulSoup(source, "html.parser")
    return _PageMetadata(
        relative_path=relative_path,
        within_language=within_language,
        title=_page_title(soup),
        description=_page_description(
            soup=soup,
            language_code=language_site.code,
        ),
        indexable=_is_indexable_page(
            relative_path=relative_path,
            language_slug=language_site.slug,
        ),
    )


def _base_discovery_tags(metadata: _PageMetadata) -> list[str]:
    return [
        _discovery_meta(
            attribute="name",
            key="description",
            content=metadata.description,
        ),
        _discovery_meta(
            attribute="name",
            key="generator",
            content="Recoleta",
        ),
        _discovery_meta(
            attribute="name",
            key="robots",
            content="index,follow" if metadata.indexable else "noindex,follow",
        ),
    ]


def _social_discovery_tags(
    *,
    metadata: _PageMetadata,
    language_site: _LanguageSite,
    canonical_url: str,
) -> list[str]:
    return [
        _discovery_link(rel="canonical", href=canonical_url),
        _discovery_meta(
            attribute="property",
            key="og:type",
            content=_open_graph_type(
                relative_path=metadata.relative_path,
                language_slug=language_site.slug,
            ),
        ),
        _discovery_meta(
            attribute="property",
            key="og:site_name",
            content="Recoleta Research Radar",
        ),
        _discovery_meta(
            attribute="property",
            key="og:title",
            content=metadata.title,
        ),
        _discovery_meta(
            attribute="property",
            key="og:description",
            content=metadata.description,
        ),
        _discovery_meta(
            attribute="property",
            key="og:url",
            content=canonical_url,
        ),
        _discovery_meta(
            attribute="name",
            key="twitter:card",
            content="summary",
        ),
        _discovery_meta(
            attribute="name",
            key="twitter:title",
            content=metadata.title,
        ),
        _discovery_meta(
            attribute="name",
            key="twitter:description",
            content=metadata.description,
        ),
    ]


def _alternate_language_sites(
    *,
    context: _DiscoveryContext,
    within_language: str,
) -> list[_LanguageSite]:
    return [
        site
        for site in context.language_sites
        if within_language in site.relative_html_paths
    ]


def _default_alternate_tag(
    *,
    context: _DiscoveryContext,
    alternate_sites: list[_LanguageSite],
    within_language: str,
) -> str | None:
    if not context.default_language_slug or not context.public_site_url:
        return None
    default_site = next(
        (
            site
            for site in alternate_sites
            if site.slug == context.default_language_slug
        ),
        None,
    )
    if default_site is None:
        return None
    return _discovery_link(
        rel="alternate",
        href=_site_url(
            public_site_url=context.public_site_url,
            relative_path=str(
                PurePosixPath(default_site.slug) / within_language
            ),
        ),
        hreflang="x-default",
    )


def _language_alternate_tags(
    *,
    context: _DiscoveryContext,
    within_language: str,
) -> list[str]:
    alternate_sites = _alternate_language_sites(
        context=context,
        within_language=within_language,
    )
    if len(alternate_sites) <= 1 or not context.public_site_url:
        return []
    tags = [
        _discovery_link(
            rel="alternate",
            href=_site_url(
                public_site_url=context.public_site_url,
                relative_path=str(PurePosixPath(site.slug) / within_language),
            ),
            hreflang=site.code,
        )
        for site in alternate_sites
    ]
    default_tag = _default_alternate_tag(
        context=context,
        alternate_sites=alternate_sites,
        within_language=within_language,
    )
    if default_tag is not None:
        tags.append(default_tag)
    return tags


def _public_discovery_tags(
    *,
    html_path: Path,
    metadata: _PageMetadata,
    context: _DiscoveryContext,
    language_site: _LanguageSite,
) -> list[str]:
    if context.public_site_url is None:
        return []
    canonical_url = _site_url(
        public_site_url=context.public_site_url,
        relative_path=metadata.relative_path,
    )
    tags = _social_discovery_tags(
        metadata=metadata,
        language_site=language_site,
        canonical_url=canonical_url,
    )
    tags.extend(
        _language_alternate_tags(
            context=context,
            within_language=metadata.within_language,
        )
    )
    tags.append(
        _discovery_link(
            rel="alternate",
            href=_page_feed_href(
                page_path=html_path,
                language_site=language_site,
            ),
            type="application/atom+xml",
            title="Recoleta Research Radar feed",
        )
    )
    return tags


def _apply_page_metadata(
    *,
    html_path: Path,
    context: _DiscoveryContext,
    language_site: _LanguageSite,
) -> bool:
    source = html_path.read_text(encoding="utf-8")
    metadata = _read_page_metadata(
        html_path=html_path,
        context=context,
        language_site=language_site,
        source=source,
    )
    tags = _base_discovery_tags(metadata)
    tags.extend(
        _public_discovery_tags(
            html_path=html_path,
            metadata=metadata,
            context=context,
            language_site=language_site,
        )
    )
    updated = _inject_discovery_head_tags(source=source, tags=tags)
    html_path.write_text(updated, encoding="utf-8")
    return metadata.indexable


def _entry_updated(relative_path: str, fallback: str) -> str:
    match = _DATE_IN_STEM_RE.search(relative_path)
    if match is None:
        return fallback
    return f"{match.group('date')}T00:00:00Z"


def _atom_text(parent: ElementTree.Element, tag: str, value: str) -> None:
    node = ElementTree.SubElement(parent, tag)
    node.text = value


def _write_atom_feed(
    *,
    language_site: _LanguageSite,
    output_dir: Path,
    public_site_url: str,
    generated_at: str,
) -> Path:
    home_path = language_site.root / "index.html"
    soup = BeautifulSoup(home_path.read_text(encoding="utf-8"), "html.parser")
    feed_relative_path = str(
        PurePosixPath(language_site.slug) / "feed.xml"
        if language_site.slug
        else PurePosixPath("feed.xml")
    )
    feed_url = _site_url(
        public_site_url=public_site_url,
        relative_path=feed_relative_path,
    )
    home_relative_path = str(
        PurePosixPath(language_site.slug) / "index.html"
        if language_site.slug
        else PurePosixPath("index.html")
    )
    home_url = _site_url(
        public_site_url=public_site_url,
        relative_path=home_relative_path,
    )

    feed = ElementTree.Element("feed", {"xmlns": _ATOM_NAMESPACE})
    feed.set("{http://www.w3.org/XML/1998/namespace}lang", language_site.code)
    _atom_text(feed, "title", "Recoleta Research Radar")
    _atom_text(feed, "id", home_url)
    _atom_text(feed, "updated", generated_at)
    ElementTree.SubElement(
        feed,
        "link",
        {"rel": "alternate", "href": home_url, "type": "text/html"},
    )
    ElementTree.SubElement(
        feed,
        "link",
        {"rel": "self", "href": feed_url, "type": "application/atom+xml"},
    )

    seen: set[str] = set()
    for link in soup.select(".home-feature-title a, .latest-feed-row h3 a"):
        href = str(link.get("href") or "").strip()
        if not href:
            continue
        target_path = (home_path.parent / href).resolve()
        try:
            target_relative_path = str(target_path.relative_to(output_dir)).replace(
                "\\", "/"
            )
        except ValueError:
            continue
        if target_relative_path in seen or not target_path.is_file():
            continue
        seen.add(target_relative_path)
        target_soup = BeautifulSoup(
            target_path.read_text(encoding="utf-8"),
            "html.parser",
        )
        entry_url = _site_url(
            public_site_url=public_site_url,
            relative_path=target_relative_path,
        )
        entry = ElementTree.SubElement(feed, "entry")
        _atom_text(entry, "title", _page_title(target_soup))
        _atom_text(entry, "id", entry_url)
        _atom_text(
            entry,
            "updated",
            _entry_updated(target_relative_path, generated_at),
        )
        ElementTree.SubElement(
            entry,
            "link",
            {"href": entry_url, "type": "text/html"},
        )
        _atom_text(
            entry,
            "summary",
            _page_description(
                soup=target_soup,
                language_code=language_site.code,
            ),
        )
        if len(seen) >= 20:
            break

    feed_path = language_site.root / "feed.xml"
    ElementTree.ElementTree(feed).write(
        feed_path,
        encoding="utf-8",
        xml_declaration=True,
    )
    return feed_path


def _write_sitemap(
    *,
    output_dir: Path,
    public_site_url: str,
    indexable_paths: list[str],
) -> Path:
    urlset = ElementTree.Element("urlset", {"xmlns": _SITEMAP_NAMESPACE})
    for relative_path in sorted(set(indexable_paths)):
        url = ElementTree.SubElement(urlset, "url")
        location = ElementTree.SubElement(url, "loc")
        location.text = _site_url(
            public_site_url=public_site_url,
            relative_path=relative_path,
        )
    sitemap_path = output_dir / "sitemap.xml"
    ElementTree.ElementTree(urlset).write(
        sitemap_path,
        encoding="utf-8",
        xml_declaration=True,
    )
    return sitemap_path


def _generated_at_for_feed(manifest: dict[str, Any]) -> str:
    raw_value = str(manifest.get("generated_at") or "").strip()
    if raw_value:
        try:
            parsed = datetime.fromisoformat(raw_value.replace("Z", "+00:00"))
            return parsed.astimezone(UTC).isoformat().replace("+00:00", "Z")
        except ValueError:
            pass
    return datetime.now(tz=UTC).isoformat().replace("+00:00", "Z")


def _build_discovery_context(
    *,
    output_dir: Path,
    manifest: dict[str, Any],
    public_site_url: str | None,
) -> _DiscoveryContext:
    resolved_output_dir = output_dir.expanduser().resolve()
    language_sites, default_language_slug = _manifest_language_sites(
        output_dir=resolved_output_dir,
        manifest=manifest,
    )
    return _DiscoveryContext(
        output_dir=resolved_output_dir,
        language_sites=tuple(language_sites),
        default_language_slug=default_language_slug,
        public_site_url=normalize_public_site_url(public_site_url),
    )


def _apply_all_page_metadata(
    context: _DiscoveryContext,
) -> tuple[list[str], int]:
    indexable_paths: list[str] = []
    noindex_total = 0
    for language_site in context.language_sites:
        for within_language in sorted(language_site.relative_html_paths):
            html_path = language_site.root / within_language
            if _apply_page_metadata(
                html_path=html_path,
                context=context,
                language_site=language_site,
            ):
                indexable_paths.append(
                    str(html_path.relative_to(context.output_dir)).replace(
                        "\\", "/"
                    )
                )
            else:
                noindex_total += 1
    return indexable_paths, noindex_total


def _mark_multilingual_root_noindex(context: _DiscoveryContext) -> int:
    if len(context.language_sites) <= 1:
        return 0
    root_index = context.output_dir / "index.html"
    if not root_index.is_file():
        return 0
    tags = [
        _discovery_meta(
            attribute="name",
            key="robots",
            content="noindex,follow",
        )
    ]
    if context.public_site_url and context.default_language_slug:
        tags.append(
            _discovery_link(
                rel="canonical",
                href=_site_url(
                    public_site_url=context.public_site_url,
                    relative_path=(
                        f"{context.default_language_slug}/index.html"
                    ),
                ),
            )
        )
    source = root_index.read_text(encoding="utf-8")
    root_index.write_text(
        _inject_discovery_head_tags(source=source, tags=tags),
        encoding="utf-8",
    )
    return 1


def _write_language_feeds(
    *,
    context: _DiscoveryContext,
    manifest: dict[str, Any],
) -> list[str]:
    if context.public_site_url is None:
        return []
    generated_at = _generated_at_for_feed(manifest)
    feed_paths = [
        _write_atom_feed(
            language_site=language_site,
            output_dir=context.output_dir,
            public_site_url=context.public_site_url,
            generated_at=generated_at,
        )
        for language_site in context.language_sites
    ]
    relative_paths = [
        str(path.relative_to(context.output_dir)).replace("\\", "/")
        for path in feed_paths
    ]
    root_feed = _copy_default_feed_to_root(context)
    if root_feed is not None:
        relative_paths.append(root_feed)
    return sorted(relative_paths)


def _copy_default_feed_to_root(context: _DiscoveryContext) -> str | None:
    if len(context.language_sites) <= 1 or not context.default_language_slug:
        return None
    default_feed = (
        context.output_dir / context.default_language_slug / "feed.xml"
    )
    root_feed = context.output_dir / "feed.xml"
    root_feed.write_bytes(default_feed.read_bytes())
    return "feed.xml"


def _write_robots(
    *,
    context: _DiscoveryContext,
) -> Path:
    assert context.public_site_url is not None
    robots = context.output_dir / "robots.txt"
    sitemap_url = _site_url(
        public_site_url=context.public_site_url,
        relative_path="sitemap.xml",
    )
    robots.write_text(
        f"User-agent: *\nAllow: /\nSitemap: {sitemap_url}\n",
        encoding="utf-8",
    )
    return robots


def _write_public_discovery_files(
    *,
    context: _DiscoveryContext,
    manifest: dict[str, Any],
    indexable_paths: list[str],
) -> tuple[list[str], str | None, str | None]:
    if context.public_site_url is None:
        return [], None, None
    feed_paths = _write_language_feeds(context=context, manifest=manifest)
    sitemap = _write_sitemap(
        output_dir=context.output_dir,
        public_site_url=context.public_site_url,
        indexable_paths=indexable_paths,
    )
    robots = _write_robots(context=context)
    return (
        feed_paths,
        str(sitemap.relative_to(context.output_dir)).replace("\\", "/"),
        str(robots.relative_to(context.output_dir)).replace("\\", "/"),
    )


def write_site_discovery_artifacts(
    *,
    output_dir: Path,
    manifest: dict[str, Any],
    public_site_url: str | None,
) -> dict[str, Any]:
    context = _build_discovery_context(
        output_dir=output_dir,
        manifest=manifest,
        public_site_url=public_site_url,
    )
    indexable_paths, noindex_total = _apply_all_page_metadata(context)
    noindex_total += _mark_multilingual_root_noindex(context)
    feed_paths, sitemap_path, robots_path = _write_public_discovery_files(
        context=context,
        manifest=manifest,
        indexable_paths=indexable_paths,
    )

    return {
        "public_site_url": context.public_site_url,
        "indexable_pages_total": len(indexable_paths),
        "noindex_pages_total": noindex_total,
        "sitemap": sitemap_path,
        "robots": robots_path,
        "feeds": sorted(feed_paths),
    }


def update_site_manifest_with_discovery(
    *,
    manifest_path: Path,
    public_site_url: str | None,
) -> dict[str, Any]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    discovery = write_site_discovery_artifacts(
        output_dir=manifest_path.parent,
        manifest=manifest,
        public_site_url=public_site_url,
    )
    manifest["discovery"] = discovery
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return discovery


__all__ = [
    "normalize_public_site_url",
    "update_site_manifest_with_discovery",
    "write_site_discovery_artifacts",
]
