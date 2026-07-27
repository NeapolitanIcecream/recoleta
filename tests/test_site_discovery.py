from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree

from bs4 import BeautifulSoup, Tag

from recoleta.site_discovery import write_site_discovery_artifacts


def _write_page(path: Path, *, language: str, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "<!doctype html>"
        f'<html lang="{language}"><head><title>Research page</title></head>'
        f"<body><main>{body}</main></body></html>",
        encoding="utf-8",
    )


def _meta_content(soup: BeautifulSoup, *, attribute: str, key: str) -> str:
    node = soup.find("meta", attrs={attribute: key})
    assert isinstance(node, Tag)
    return str(node.get("content") or "")


def test_multilingual_discovery_artifacts_expose_only_curated_pages(
    tmp_path: Path,
) -> None:
    for slug, language in (("en", "en"), ("zh-cn", "zh-CN")):
        _write_page(
            tmp_path / slug / "index.html",
            language=language,
            body=(
                '<h2 class="home-feature-title">'
                '<a href="trends/production-trend.html">Production trend</a>'
                "</h2>"
            ),
        )
        _write_page(
            tmp_path / slug / "trends" / "production-trend.html",
            language=language,
            body=(
                '<article class="detail-content">'
                "<p>Evidence from the continuously operated fleet.</p>"
                "</article>"
            ),
        )
        _write_page(
            tmp_path / slug / "topics" / "index.html",
            language=language,
            body="<p>Curated topic directory.</p>",
        )
        _write_page(
            tmp_path / slug / "items" / "source-note.html",
            language=language,
            body="<p>Source note.</p>",
        )
        _write_page(
            tmp_path / slug / "topics" / "agents.html",
            language=language,
            body="<p>Thin topic aggregation.</p>",
        )
        _write_page(
            tmp_path / slug / "trends" / "page" / "2" / "index.html",
            language=language,
            body="<p>Pagination.</p>",
        )
    _write_page(
        tmp_path / "index.html",
        language="en",
        body="<p>Language redirect.</p>",
    )

    discovery = write_site_discovery_artifacts(
        output_dir=tmp_path,
        manifest={
            "generated_at": "2026-07-24T00:00:00Z",
            "language_codes": {"en": "en", "zh-cn": "zh-CN"},
            "default_language_code": "en",
        },
        public_site_url="https://example.github.io/recoleta/",
    )

    assert discovery == {
        "public_site_url": "https://example.github.io/recoleta",
        "indexable_pages_total": 6,
        "noindex_pages_total": 7,
        "sitemap": "sitemap.xml",
        "robots": "robots.txt",
        "feeds": ["en/feed.xml", "feed.xml", "zh-cn/feed.xml"],
    }

    trend_path = tmp_path / "en" / "trends" / "production-trend.html"
    trend_soup = BeautifulSoup(trend_path.read_text(encoding="utf-8"), "html.parser")
    assert (
        _meta_content(trend_soup, attribute="name", key="description")
        == "Evidence from the continuously operated fleet."
    )
    assert (
        _meta_content(trend_soup, attribute="property", key="og:type")
        == "article"
    )
    canonical = trend_soup.select_one("link[rel~='canonical']")
    assert isinstance(canonical, Tag)
    assert (
        canonical["href"]
        == "https://example.github.io/recoleta/en/trends/production-trend.html"
    )
    alternates = {
        str(node.get("hreflang")): str(node.get("href"))
        for node in trend_soup.select("link[rel~='alternate'][hreflang]")
    }
    assert alternates == {
        "en": (
            "https://example.github.io/recoleta/en/trends/"
            "production-trend.html"
        ),
        "zh-CN": (
            "https://example.github.io/recoleta/zh-cn/trends/"
            "production-trend.html"
        ),
        "x-default": (
            "https://example.github.io/recoleta/en/trends/"
            "production-trend.html"
        ),
    }
    feed_link = trend_soup.select_one(
        "link[rel~='alternate'][type='application/atom+xml']"
    )
    assert isinstance(feed_link, Tag)
    assert feed_link["href"] == "../feed.xml"

    item_soup = BeautifulSoup(
        (tmp_path / "en" / "items" / "source-note.html").read_text(
            encoding="utf-8"
        ),
        "html.parser",
    )
    assert (
        _meta_content(item_soup, attribute="name", key="robots")
        == "noindex,follow"
    )
    topic_soup = BeautifulSoup(
        (tmp_path / "en" / "topics" / "agents.html").read_text(
            encoding="utf-8"
        ),
        "html.parser",
    )
    assert (
        _meta_content(topic_soup, attribute="name", key="robots")
        == "noindex,follow"
    )

    atom_namespace = {"atom": "http://www.w3.org/2005/Atom"}
    feed_root = ElementTree.parse(tmp_path / "en" / "feed.xml").getroot()
    entries = feed_root.findall("atom:entry", atom_namespace)
    assert len(entries) == 1
    assert (
        feed_root.findtext("atom:author/atom:name", namespaces=atom_namespace)
        == "Recoleta"
    )
    assert entries[0].findtext("atom:title", namespaces=atom_namespace) == (
        "Research page"
    )
    for relative_path in ("en/feed.xml", "feed.xml"):
        published_feed = ElementTree.parse(tmp_path / relative_path).getroot()
        self_link = published_feed.find(
            "atom:link[@rel='self']",
            atom_namespace,
        )
        assert self_link is not None
        assert self_link.get("href") == (
            f"https://example.github.io/recoleta/{relative_path}"
        )

    sitemap_text = (tmp_path / "sitemap.xml").read_text(encoding="utf-8")
    assert "/en/trends/production-trend.html" in sitemap_text
    assert "/en/items/source-note.html" not in sitemap_text
    assert "/en/topics/agents.html" not in sitemap_text
    assert (
        tmp_path / "robots.txt"
    ).read_text(encoding="utf-8").endswith(
        "Sitemap: https://example.github.io/recoleta/sitemap.xml\n"
    )


def test_unconfigured_public_url_adds_safe_metadata_without_dead_discovery_links(
    tmp_path: Path,
) -> None:
    _write_page(
        tmp_path / "index.html",
        language="en",
        body="<p>Local preview.</p>",
    )

    discovery = write_site_discovery_artifacts(
        output_dir=tmp_path,
        manifest={"generated_at": "2026-07-24T00:00:00Z"},
        public_site_url=None,
    )

    soup = BeautifulSoup(
        (tmp_path / "index.html").read_text(encoding="utf-8"),
        "html.parser",
    )
    assert _meta_content(soup, attribute="name", key="robots") == "index,follow"
    assert _meta_content(soup, attribute="name", key="generator") == "Recoleta"
    assert soup.select_one("link[rel~='canonical']") is None
    assert soup.select_one(
        "link[rel~='alternate'][type='application/atom+xml']"
    ) is None
    assert discovery["feeds"] == []
    assert not (tmp_path / "sitemap.xml").exists()
    assert not (tmp_path / "robots.txt").exists()
