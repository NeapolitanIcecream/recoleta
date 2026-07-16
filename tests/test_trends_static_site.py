from __future__ import annotations

from datetime import UTC, datetime, timedelta
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup, Tag
import pytest

from recoleta.markdown_render import html_to_reader_text
from recoleta.presentation import presentation_sidecar_path
from recoleta.site import (
    RECOLETA_QUICKSTART_URL,
    RECOLETA_REPO_URL,
    _build_idea_body_from_presentation,
    _build_trend_body_from_presentation,
    _display_topic_label,
    _excerpt_payload_from_html,
    _item_action_label,
    _localize_site_chrome,
    _localized_site_chrome_text,
    _native_language_name,
    _render_language_switcher_fragment,
    _safe_excerpt,
    _site_chrome_locale,
    export_trend_static_site,
)
from recoleta.site_presentation import build_item_browser_body_html
from recoleta.passes.trend_ideas import TrendIdeasPayload
from recoleta.publish import write_markdown_ideas_note, write_markdown_trend_note
from recoleta.storage import Repository
from recoleta.types import AnalysisResult, ItemDraft


_PAGINATION_TREND_TOTAL = 25
_PAGINATION_IDEA_TOTAL = 13


def _write_minimal_site_note(
    *,
    notes_root: Path,
    kind: str,
    index: int,
    period_start: datetime,
    topics: tuple[str, ...],
) -> None:
    period_end = period_start + timedelta(days=1)
    if kind == "trend":
        note_dir = notes_root / "Trends"
        stem = f"day--{period_start.date().isoformat()}--trend--{index}"
        title = f"Trend {index:02d}"
        sections = ["## Overview", "", f"Overview for {title}."]
    else:
        assert kind == "ideas"
        note_dir = notes_root / "Ideas"
        stem = f"day--{period_start.date().isoformat()}--ideas"
        title = f"Idea {index:02d}"
        sections = [
            "## Summary",
            "",
            f"Summary for {title}.",
            "",
            f"## Candidate {index:02d}",
            "",
            f"Details for {title}.",
        ]
    note_dir.mkdir(parents=True, exist_ok=True)
    topic_lines = [f"- {topic}" for topic in topics]
    status_lines = ["status: succeeded"] if kind == "ideas" else []
    (note_dir / f"{stem}.md").write_text(
        "\n".join(
            [
                "---",
                f"kind: {kind}",
                "granularity: day",
                f"period_start: {period_start.isoformat()}",
                f"period_end: {period_end.isoformat()}",
                *status_lines,
                "topics:",
                *topic_lines,
                "---",
                "",
                f"# {title}",
                "",
                *sections,
                "",
            ]
        ),
        encoding="utf-8",
    )


@pytest.fixture(scope="module")
def paginated_site(tmp_path_factory: pytest.TempPathFactory) -> Path:
    tmp_path = tmp_path_factory.mktemp("paginated-site")
    notes_root = tmp_path / "notes"
    first_day = datetime(2026, 1, 1, tzinfo=UTC)
    for index in range(_PAGINATION_TREND_TOTAL):
        _write_minimal_site_note(
            notes_root=notes_root,
            kind="trend",
            index=index,
            period_start=first_day + timedelta(days=index),
            topics=("shared-topic", f"topic-{index:02d}"),
        )
    for index in range(_PAGINATION_IDEA_TOTAL):
        _write_minimal_site_note(
            notes_root=notes_root,
            kind="ideas",
            index=index,
            period_start=first_day + timedelta(days=index),
            topics=("shared-topic",),
        )

    site_dir = tmp_path / "site"
    export_trend_static_site(
        input_dir=notes_root / "Trends",
        output_dir=site_dir,
    )
    return site_dir


def _read_html(path: Path) -> BeautifulSoup:
    return BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")


def test_two_language_switcher_names_only_the_available_destination() -> None:
    fragment = _render_language_switcher_fragment(
        current_language_slug="en",
        current_page_relative_path="trends/example.html",
        page_paths_by_language={
            "en": {"trends/example.html"},
            "zh-cn": {"trends/example.html"},
        },
        language_code_by_slug={"en": "en", "zh-cn": "zh-CN"},
    )

    switcher = fragment.select_one("nav.language-switcher")
    link = fragment.select_one(".language-switcher-link")
    assert isinstance(switcher, Tag)
    assert switcher["aria-label"] == "Language"
    assert isinstance(link, Tag)
    assert link.get_text(" ", strip=True) == "中文"
    assert link["hreflang"] == "zh-CN"
    assert link.select_one("[lang='zh-CN'][dir='auto']") is not None
    assert link["href"] == "../../zh-cn/trends/example.html"
    assert fragment.select_one("[aria-current]") is None


def test_many_language_switcher_uses_a_native_name_menu() -> None:
    fragment = _render_language_switcher_fragment(
        current_language_slug="en",
        current_page_relative_path="trends/example.html",
        page_paths_by_language={
            "en": {"trends/example.html"},
            "zh-cn": {"index.html"},
            "fr": {"trends/example.html"},
        },
        language_code_by_slug={"en": "en", "zh-cn": "zh-CN", "fr": "fr"},
    )

    menu = fragment.select_one("details.language-switcher-menu")
    current = fragment.select_one(".language-switcher-option[aria-current='page']")
    assert isinstance(menu, Tag)
    assert menu.select_one("summary").get_text(" ", strip=True) == "English"  # type: ignore[union-attr]
    assert [
        label.get_text(" ", strip=True)
        for label in menu.select("ul.language-switcher-list a > span[lang][dir='auto']")
    ] == ["English", "中文", "français"]
    assert isinstance(current, Tag)
    assert current.select_one("[lang='en'][dir='auto']") is not None
    assert [link["data-language-code"] for link in menu.select("a")] == [
        "en",
        "zh-cn",
        "fr",
    ]
    assert [link["hreflang"] for link in menu.select("a")] == [
        "en",
        "zh-CN",
        "fr",
    ]
    assert [link["href"] for link in menu.select("a")] == [
        "example.html",
        "../../zh-cn/index.html",
        "../../fr/trends/example.html",
    ]


def test_native_language_names_use_autonyms_and_concise_chinese_label() -> None:
    assert _native_language_name("fr") == "français"
    assert _native_language_name("pt-BR") == "português (Brasil)"
    assert _native_language_name("zh-CN") == "中文"
    assert _native_language_name("zh-Hant-TW") == "繁體中文"


@pytest.mark.parametrize("language_code", ["xx", "und"])
def test_native_language_names_reject_unknown_codes(language_code: str) -> None:
    with pytest.raises(ValueError, match=language_code):
        _native_language_name(language_code)


def _page_titles(paths: list[Path], *, selector: str) -> list[str]:
    return [
        node.get_text(" ", strip=True)
        for path in paths
        for node in _read_html(path).select(selector)
    ]


def _assert_pager(
    *,
    page_path: Path,
    current_page: int,
    total_pages: int,
    previous_href: str | None,
    next_href: str | None,
) -> None:
    pager = _read_html(page_path).select_one("nav.collection-pagination")
    assert isinstance(pager, Tag)
    assert str(pager.get("aria-label") or "").endswith(" pagination")
    current = pager.select_one("[aria-current='page']")
    assert isinstance(current, Tag)
    assert current.get_text(" ", strip=True) == str(current_page)
    assert f"Page {current_page} of {total_pages}" in pager.get_text(" ", strip=True)

    previous = pager.select_one("a[rel~='prev']")
    if previous_href is None:
        assert previous is None
    else:
        assert isinstance(previous, Tag)
        assert previous.get("href") == previous_href

    next_link = pager.select_one("a[rel~='next']")
    if next_href is None:
        assert next_link is None
    else:
        assert isinstance(next_link, Tag)
        assert next_link.get("href") == next_href


def _assert_local_links_resolve(page_path: Path) -> None:
    for node in _read_html(page_path).select("a[href], link[href]"):
        href = str(node.get("href") or "").strip()
        parsed = urlsplit(href)
        if not parsed.path or parsed.scheme or parsed.netloc:
            continue
        target = (page_path.parent / unquote(parsed.path)).resolve()
        assert target.exists(), f"{page_path}: local href does not exist: {href}"


def _seed_item_doc_with_authors(*, repository: Repository, published_at: datetime) -> int:
    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="idea-static-site-authors",
        canonical_url="https://example.com/idea-static-site-authors",
        title="Grounded runtime checks",
        authors=["Peng Wang", "Hao Wang"],
        published_at=published_at,
    )
    item, _ = repository.upsert_item(draft)
    assert item.id is not None
    repository.save_analysis(
        item_id=int(item.id),
        result=AnalysisResult(
            model="test/fake-model",
            provider="test",
            summary=(
                "## Summary\n\n"
                "Grounded runtime checks make long-horizon work auditable.\n\n"
                "## Problem\n\n"
                "Teams lack visible checkpoints for agent execution.\n\n"
                "## Approach\n\n"
                "Runtime traces and verifier loops are logged explicitly.\n\n"
                "## Results\n\n"
                "This makes failures easier to inspect before rollout.\n"
            ),
            topics=["agents"],
            relevance_score=0.9,
            novelty_score=0.4,
            cost_usd=0.0,
            latency_ms=1,
        ),
    )
    persisted_item = repository.get_item(item_id=int(item.id))
    assert persisted_item is not None
    doc = repository.upsert_document_for_item(item=persisted_item)
    assert doc.id is not None
    repository.upsert_document_chunk(
        doc_id=int(doc.id),
        chunk_index=0,
        kind="summary",
        text_value="Grounded runtime checks move verification into the shipping path.",
        source_content_type="analysis_summary",
    )
    return int(doc.id)


def test_item_action_label_uses_known_source_hosts() -> None:
    assert (
        _item_action_label(
            source="",
            canonical_url="https://arxiv.org/abs/2603.02115",
        )
        == "Open arXiv"
    )
    assert (
        _item_action_label(
            source="",
            canonical_url="https://api.openreview.net/forum?id=test",
        )
        == "Open OpenReview"
    )
    assert (
        _item_action_label(
            source="",
            canonical_url="https://gist.github.com/octocat/example",
        )
        == "Open GitHub"
    )


def test_item_action_label_ignores_partial_domain_suffix_matches() -> None:
    assert (
        _item_action_label(
            source="",
            canonical_url="https://notarxiv.org/abs/2603.02115",
        )
        == "Open original"
    )
    assert (
        _item_action_label(
            source="",
            canonical_url="https://mirroropenreview.net/forum?id=test",
        )
        == "Open original"
    )


def test_safe_excerpt_prefers_complete_sentences_and_cleans_trailing_punctuation() -> None:
    complete_sentence = "A" * 90 + ". " + "B" * 100
    assert _safe_excerpt(complete_sentence, limit=120) == "A" * 90 + "."

    hard_cut = "x" * 100 + "," + "y" * 100
    assert _safe_excerpt(hard_cut, limit=101) == "x" * 100 + "…"

    cjk_sentences = "甲" * 50 + "。" + "乙" * 50 + "。" + "丙" * 100
    assert _safe_excerpt(cjk_sentences, limit=130) == (
        "甲" * 50 + "。" + "乙" * 50 + "。"
    )


def test_home_excerpt_text_extraction_handles_deep_inline_markup() -> None:
    nested_html = ("<span>" * 700) + "Readable text" + ("</span>" * 700)

    excerpt, excerpt_html = _excerpt_payload_from_html(nested_html)

    assert excerpt == "Readable text"
    assert BeautifulSoup(excerpt_html, "html.parser").get_text(strip=True) == (
        "Readable text"
    )


def test_display_topic_label_preserves_research_names_with_hyphens() -> None:
    assert _display_topic_label("R-CNN") == "R-CNN"
    assert _display_topic_label("GPT-4o") == "GPT-4o"
    assert _display_topic_label("CLIP-based") == "CLIP-based"
    assert _display_topic_label("agent-memory") == "Agent Memory"
    assert _display_topic_label("mcp") == "MCP"


def test_localized_site_chrome_handles_plural_entries_and_compound_metadata() -> None:
    assert _site_chrome_locale("zh-Hant-TW") == "zh-TW"
    assert _site_chrome_locale("zh-Hans-CN") == "zh-CN"
    assert _site_chrome_locale("JA") == "ja"
    assert (
        _localized_site_chrome_text(
            text="0 entries · latest window 2026-W28",
            locale="zh-CN",
        )
        == "0 项内容 · 最近一期 2026-W28"
    )
    assert (
        _localized_site_chrome_text(
            text="25 trends · Page 2 of 3",
            locale="zh-CN",
        )
        == "25 条趋势 · 第 2 / 3 页"
    )


def test_site_chrome_localization_is_scoped_and_handles_compound_chrome() -> None:
    soup = BeautifulSoup(
        """
        <html lang='en'>
          <head><title>Trends · Recoleta Trends · Page 2</title></head>
          <body class='page-trends'>
            <nav class='site-header'><a class='nav-link'>Trends</a></nav>
            <p class='detail-meta'>Source: arXiv · Published: 2026-07-01 · Authors: A</p>
            <nav class='collection-pagination' aria-label='Trends pagination'>
              <a aria-label='Go to page 2'>2</a>
            </nav>
            <p class='prose'>The paper names 3 trends and a latest window baseline.</p>
          </body>
        </html>
        """,
        "html.parser",
    )

    _localize_site_chrome(soup=soup, language_code="zh-Hans-CN")

    assert soup.title is not None
    assert soup.title.get_text() == "趋势 · Recoleta Trends · 第 2 页"
    assert soup.select_one(".detail-meta").get_text(" ", strip=True) == (  # type: ignore[union-attr]
        "来源: arXiv · 发布日期: 2026-07-01 · 作者: A"
    )
    pagination = soup.select_one(".collection-pagination")
    page_link = soup.select_one(".collection-pagination a")
    assert isinstance(pagination, Tag)
    assert isinstance(page_link, Tag)
    assert pagination.get("aria-label") == "趋势分页"
    assert page_link.get("aria-label") == "前往第 2 页"
    assert "The paper names 3 trends and a latest window baseline." in soup.get_text(
        " ", strip=True
    )

    item_soup = BeautifulSoup(
        "<body class='page-item'><section class='detail-content'>"
        "<h2 class='section-label'>Summary</h2></section></body>",
        "html.parser",
    )
    _localize_site_chrome(soup=item_soup, language_code="zh-CN")
    assert item_soup.select_one(".section-label").get_text(strip=True) == "摘要"  # type: ignore[union-attr]


def test_presentation_bodies_omit_empty_source_placeholders() -> None:
    trend_html, _excerpt = _build_trend_body_from_presentation(
        presentation={
            "language_code": "en",
            "content": {
                "overview": "A scoped finding.",
                "clusters": [
                    {"title": "Finding", "content": "Details.", "evidence": []}
                ],
            },
        }
    )
    idea_result = _build_idea_body_from_presentation(
        presentation={
            "language_code": "en",
            "content": {
                "summary": "A scoped idea.",
                "ideas": [{"title": "Idea", "content": "Details.", "evidence": []}],
            },
        }
    )

    assert "Sources" not in trend_html
    assert "Sources" not in idea_result.body_html
    assert "(none)" not in trend_html
    assert "(none)" not in idea_result.body_html


def test_presentation_body_renders_math_without_duplicating_excerpt_text() -> None:
    trend_html, excerpt = _build_trend_body_from_presentation(
        presentation={
            "language_code": "en",
            "content": {
                "overview": "Energy follows $E=mc^2$.",
                "clusters": [],
            },
        }
    )
    soup = BeautifulSoup(trend_html, "html.parser")

    assert soup.select_one(".math.inline math[display='inline']") is not None
    assert excerpt.count("E=mc^2") == 1


@pytest.mark.parametrize("latest_kind", ["trend", "ideas"])
def test_home_latest_excerpt_renders_complete_math_and_truncates_only_prose(
    tmp_path: Path,
    latest_kind: str,
) -> None:
    notes_root = tmp_path / "notes"
    (notes_root / "Trends").mkdir(parents=True)
    note_dir = notes_root / ("Trends" if latest_kind == "trend" else "Ideas")
    note_dir.mkdir(parents=True, exist_ok=True)
    stem = (
        "day--2026-07-15--trend--1"
        if latest_kind == "trend"
        else "day--2026-07-15--ideas"
    )
    heading = "Overview" if latest_kind == "trend" else "Summary"
    status_lines = ["status: succeeded"] if latest_kind == "ideas" else []
    (note_dir / f"{stem}.md").write_text(
        "\n".join(
            [
                "---",
                f"kind: {latest_kind}",
                "granularity: day",
                "period_start: 2026-07-15T00:00:00+00:00",
                "period_end: 2026-07-16T00:00:00+00:00",
                *status_lines,
                "topics:",
                "- evaluation",
                "---",
                "",
                "# Calibrated decisions",
                "",
                f"## {heading}",
                "",
                '<span onclick="alert(1)">Safe visible text</span> Cost $5, code `$z$`, malformed $x_$, readable before & value=$E=mc^2$, then the block expression',
                "",
                r"$$\frac{a+b}{c}$$",
                "",
                "The ordinary prose after it remains readable and complete.",
                "",
                ("Long tail filler " * 30) + "TAIL_MARKER",
                "",
            ]
        ),
        encoding="utf-8",
    )

    site_dir = tmp_path / "site"
    export_trend_static_site(
        input_dir=notes_root / "Trends",
        output_dir=site_dir,
    )

    home = _read_html(site_dir / "index.html")
    excerpt = home.select_one(".home-latest .home-feature-excerpt")
    assert isinstance(excerpt, Tag)
    assert excerpt.select_one(".math.inline math[display='inline']") is not None
    assert excerpt.select_one(".math.block math[display='block']") is not None
    literal_code = excerpt.select_one("code:not(.math-source-fallback)")
    fallback = excerpt.select_one(".math-source-fallback")
    assert isinstance(literal_code, Tag)
    assert isinstance(fallback, Tag)
    assert literal_code.get_text() == "$z$"
    assert fallback.get_text() == "$x_$"
    assert excerpt.select("script, [onclick]") == []
    annotations = excerpt.select("annotation[encoding='application/x-tex']")
    assert [annotation.get_text() for annotation in annotations] == [
        "E=mc^2",
        r"\frac{a+b}{c}",
    ]
    inline_math = excerpt.select_one(".math.inline math[display='inline']")
    assert isinstance(inline_math, Tag)
    inline_wrapper = inline_math.parent
    assert isinstance(inline_wrapper, Tag)
    assert str(inline_wrapper.previous_sibling).endswith("value=")
    assert str(inline_wrapper.next_sibling).startswith(",")
    reader_text = html_to_reader_text(str(excerpt))
    assert reader_text.count("E=mc^2") == 1
    assert reader_text.count(r"\frac{a+b}{c}") == 1
    assert "Cost $5" in reader_text
    assert "Safe visible text" in reader_text
    assert "readable before & value=" in reader_text
    assert "ordinary prose after it remains readable" in reader_text
    assert "TAIL_MARKER" not in reader_text


def test_home_latest_excerpt_never_emits_a_partial_formula_at_its_boundary(
    tmp_path: Path,
) -> None:
    notes_root = tmp_path / "notes"
    trends_dir = notes_root / "Trends"
    trends_dir.mkdir(parents=True)
    formula = r"\frac{a_1+\cdots+a_{40}}{b_1+\cdots+b_{40}}"
    boundary_prefix = "边界文本" * 48
    (trends_dir / "day--2026-07-15--trend--1.md").write_text(
        "\n".join(
            [
                "---",
                "kind: trend",
                "granularity: day",
                "period_start: 2026-07-15T00:00:00+00:00",
                "period_end: 2026-07-16T00:00:00+00:00",
                "topics:",
                "- evaluation",
                "---",
                "",
                "# Boundary-safe formula",
                "",
                "## Overview",
                "",
                f"{boundary_prefix}${formula}$ trailing prose",
                "",
            ]
        ),
        encoding="utf-8",
    )

    site_dir = tmp_path / "site"
    export_trend_static_site(
        input_dir=trends_dir,
        output_dir=site_dir,
    )

    detail = _read_html(site_dir / "trends" / "day--2026-07-15--trend--1.html")
    detail_annotation = detail.select_one(
        "annotation[encoding='application/x-tex']"
    )
    assert isinstance(detail_annotation, Tag)
    assert detail_annotation.get_text() == formula

    home = _read_html(site_dir / "index.html")
    excerpt = home.select_one(".home-latest .home-feature-excerpt")
    assert isinstance(excerpt, Tag)
    annotation = excerpt.select_one("annotation[encoding='application/x-tex']")
    reader_text = html_to_reader_text(str(excerpt))
    if isinstance(annotation, Tag):
        assert annotation.get_text() == formula
        assert reader_text.count(formula) == 1
    else:
        assert excerpt.find("math") is None
        assert r"\frac" not in reader_text
        assert "a_{40}" not in reader_text
        assert "b_{40}" not in reader_text


def test_home_latest_excerpt_bounds_oversized_math_and_code(
    tmp_path: Path,
) -> None:
    notes_root = tmp_path / "notes"
    trends_dir = notes_root / "Trends"
    trends_dir.mkdir(parents=True)
    formula = "+".join(f"x_{{{index}}}" for index in range(80))
    code = "z" * 500
    (trends_dir / "day--2026-07-15--trend--1.md").write_text(
        "\n".join(
            [
                "---",
                "kind: trend",
                "granularity: day",
                "period_start: 2026-07-15T00:00:00+00:00",
                "period_end: 2026-07-16T00:00:00+00:00",
                "topics:",
                "- evaluation",
                "---",
                "",
                "# Bounded excerpt atoms",
                "",
                "## Overview",
                "",
                f"${formula}$",
                "",
                f"`{code}`",
                "",
                "Readable prose remains available after oversized atoms.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    site_dir = tmp_path / "site"
    export_trend_static_site(
        input_dir=trends_dir,
        output_dir=site_dir,
    )

    detail = _read_html(site_dir / "trends" / "day--2026-07-15--trend--1.html")
    detail_annotation = detail.select_one(
        "annotation[encoding='application/x-tex']"
    )
    detail_code = detail.select_one("code:not(.math-source-fallback)")
    assert isinstance(detail_annotation, Tag)
    assert isinstance(detail_code, Tag)
    assert detail_annotation.get_text() == formula
    assert detail_code.get_text() == code

    home = _read_html(site_dir / "index.html")
    excerpt = home.select_one(".home-latest .home-feature-excerpt")
    assert isinstance(excerpt, Tag)
    assert excerpt.find("math") is None
    assert excerpt.find("code") is None
    reader_text = html_to_reader_text(str(excerpt))
    assert reader_text == "Readable prose remains available after oversized atoms."


def test_item_body_omits_repeated_summary_heading() -> None:
    rendered = build_item_browser_body_html(
        body_html="unused",
        extract_trend_pdf_sections=lambda **_kwargs: ("Title", [object()]),
        build_trend_browser_body_html=lambda **_kwargs: (
            "<div class='document-flow'><section class='summary-grid'>"
            "<section class='surface-card section-card summary-card'>"
            "<h2 class='section-label'>Summary</h2>"
            "<div class='prose'><h3>摘要</h3><p>保留正文。</p></div>"
            "</section></section></div>"
        ),
    )
    soup = BeautifulSoup(rendered, "html.parser")
    paragraph = soup.select_one(".summary-card .prose p")

    assert soup.select_one(".summary-card .prose h3") is None
    assert isinstance(paragraph, Tag)
    assert paragraph.get_text(strip=True) == "保留正文。"


def test_export_trend_static_site_paginates_top_level_collections_without_loss(
    paginated_site: Path,
) -> None:
    trend_pages = [
        paginated_site / "trends" / "index.html",
        paginated_site / "trends" / "page" / "2" / "index.html",
        paginated_site / "trends" / "page" / "3" / "index.html",
    ]
    idea_pages = [
        paginated_site / "ideas" / "index.html",
        paginated_site / "ideas" / "page" / "2" / "index.html",
    ]
    topics_pages = [
        paginated_site / "topics" / "index.html",
        paginated_site / "topics" / "page" / "2" / "index.html",
    ]
    archive_pages = [
        paginated_site / "archive.html",
        paginated_site / "archive" / "page" / "2" / "index.html",
    ]
    assert all(path.exists() for path in trend_pages)
    assert all(path.exists() for path in idea_pages)
    assert all(path.exists() for path in topics_pages)
    assert all(path.exists() for path in archive_pages)

    expected_trends = [
        f"Trend {index:02d}" for index in reversed(range(_PAGINATION_TREND_TOTAL))
    ]
    expected_ideas = [
        f"Idea {index:02d}" for index in reversed(range(_PAGINATION_IDEA_TOTAL))
    ]
    assert (
        _page_titles(
            trend_pages,
            selector=".trend-card .card-title",
        )
        == expected_trends
    )
    assert [len(_read_html(path).select(".trend-card")) for path in trend_pages] == [
        12,
        12,
        1,
    ]
    assert (
        _page_titles(
            idea_pages,
            selector=".trend-card .card-title",
        )
        == expected_ideas
    )
    assert [len(_read_html(path).select(".trend-card")) for path in idea_pages] == [
        12,
        1,
    ]

    archive_titles = _page_titles(archive_pages, selector=".archive-item a")
    assert archive_titles == expected_trends
    assert [
        len(_read_html(path).select(".archive-item")) for path in archive_pages
    ] == [24, 1]

    topic_titles = _page_titles(topics_pages, selector=".topic-card-title")
    assert len(topic_titles) == 26
    assert len(set(topic_titles)) == 26
    assert set(topic_titles) == {
        "Shared Topic",
        *(f"Topic {index:02d}" for index in range(_PAGINATION_TREND_TOTAL)),
    }
    assert [len(_read_html(path).select(".topic-card")) for path in topics_pages] == [
        24,
        2,
    ]

    for page_path in trend_pages:
        assert "25 trends" in _read_html(page_path).get_text(" ", strip=True)
    for page_path in idea_pages:
        assert "13 ideas" in _read_html(page_path).get_text(" ", strip=True)

    _assert_pager(
        page_path=trend_pages[0],
        current_page=1,
        total_pages=3,
        previous_href=None,
        next_href="page/2/index.html",
    )
    _assert_pager(
        page_path=trend_pages[1],
        current_page=2,
        total_pages=3,
        previous_href="../../index.html",
        next_href="../3/index.html",
    )
    _assert_pager(
        page_path=trend_pages[2],
        current_page=3,
        total_pages=3,
        previous_href="../2/index.html",
        next_href=None,
    )
    _assert_pager(
        page_path=idea_pages[0],
        current_page=1,
        total_pages=2,
        previous_href=None,
        next_href="page/2/index.html",
    )
    _assert_pager(
        page_path=idea_pages[1],
        current_page=2,
        total_pages=2,
        previous_href="../../index.html",
        next_href=None,
    )
    _assert_pager(
        page_path=topics_pages[0],
        current_page=1,
        total_pages=2,
        previous_href=None,
        next_href="page/2/index.html",
    )
    _assert_pager(
        page_path=topics_pages[1],
        current_page=2,
        total_pages=2,
        previous_href="../../index.html",
        next_href=None,
    )
    _assert_pager(
        page_path=archive_pages[0],
        current_page=1,
        total_pages=2,
        previous_href=None,
        next_href="archive/page/2/index.html",
    )
    _assert_pager(
        page_path=archive_pages[1],
        current_page=2,
        total_pages=2,
        previous_href="../../../archive.html",
        next_href=None,
    )

    for page_path in (
        trend_pages[1],
        idea_pages[1],
        topics_pages[1],
        archive_pages[1],
    ):
        _assert_local_links_resolve(page_path)

    manifest = json.loads(
        (paginated_site / "manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["trends_total"] == _PAGINATION_TREND_TOTAL
    assert manifest["ideas_total"] == _PAGINATION_IDEA_TOTAL
    assert manifest["topics_total"] == 26
    assert manifest["pagination"] == {
        "card_page_size": 12,
        "dense_page_size": 24,
        "topic_page_size": 12,
        "topic_column_page_size": 12,
    }
    assert manifest["files"]["trends_index"] == "trends/index.html"
    assert manifest["files"]["ideas_index"] == "ideas/index.html"
    assert manifest["files"]["topics_index"] == "topics/index.html"
    assert manifest["files"]["archive"] == "archive.html"
    assert manifest["files"]["trends_index_pages"] == [
        "trends/index.html",
        "trends/page/2/index.html",
        "trends/page/3/index.html",
    ]
    assert manifest["files"]["ideas_index_pages"] == [
        "ideas/index.html",
        "ideas/page/2/index.html",
    ]
    assert manifest["files"]["topics_index_pages"] == [
        "topics/index.html",
        "topics/page/2/index.html",
    ]
    assert manifest["files"]["archive_pages"] == [
        "archive.html",
        "archive/page/2/index.html",
    ]
    assert len(manifest["files"]["trend_pages"]) == _PAGINATION_TREND_TOTAL
    assert len(manifest["files"]["idea_pages"]) == _PAGINATION_IDEA_TOTAL
    assert all("/page/" not in page for page in manifest["files"]["topic_pages"])
    assert manifest["files"]["topic_collection_pages"]["shared-topic"] == [
        "topics/shared-topic.html",
        "topics/shared-topic/page/2/index.html",
        "topics/shared-topic/page/3/index.html",
        "topics/shared-topic/page/4/index.html",
    ]

    page_boundary_detail = _read_html(
        paginated_site / "trends" / "day--2026-01-14--trend--13.html"
    )
    pager_cards = page_boundary_detail.select("a.pager-card")
    assert [card.get_text(" ", strip=True) for card in pager_cards] == [
        "Newer Trend 14",
        "Older Trend 12",
    ]
    assert pager_cards[1].get("href") == "day--2026-01-13--trend--12.html"


def test_export_trend_static_site_merges_topic_entries_newest_first_without_loss(
    paginated_site: Path,
) -> None:
    topic_pages = [paginated_site / "topics" / "shared-topic.html"] + [
        paginated_site
        / "topics"
        / "shared-topic"
        / "page"
        / str(page_number)
        / "index.html"
        for page_number in range(2, 5)
    ]
    assert all(path.exists() for path in topic_pages)

    pages = [_read_html(page_path) for page_path in topic_pages]
    cards = [card for page in pages for card in page.select(".topic-feed .trend-card")]
    titles = [
        node.get_text(" ", strip=True)
        for card in cards
        if isinstance((node := card.select_one(".card-title")), Tag)
    ]
    assert len(titles) == _PAGINATION_TREND_TOTAL + _PAGINATION_IDEA_TOTAL
    assert len(set(titles)) == len(titles)
    assert set(titles) == {
        *(f"Trend {index:02d}" for index in range(_PAGINATION_TREND_TOTAL)),
        *(f"Idea {index:02d}" for index in range(_PAGINATION_IDEA_TOTAL)),
    }
    assert [len(page.select(".topic-feed .trend-card")) for page in pages] == [
        12,
        12,
        12,
        2,
    ]
    meta_labels = [
        node.get_text(" ", strip=True)
        for card in cards
        if isinstance((node := card.select_one(".meta-date")), Tag)
    ]
    assert sum(label.startswith("Trend ·") for label in meta_labels) == 25
    assert sum(label.startswith("Idea ·") for label in meta_labels) == 13
    period_tokens = [label.rsplit(" · ", 1)[-1] for label in meta_labels]
    assert period_tokens == sorted(period_tokens, reverse=True)

    for page_number, page_path in enumerate(topic_pages, start=1):
        page = _read_html(page_path)
        summary_stats = {
            panel.select_one(".meta-panel-label").get_text(" ", strip=True): panel.select_one(  # type: ignore[union-attr]
                ".meta-panel-value"
            ).get_text(" ", strip=True)  # type: ignore[union-attr]
            for panel in page.select(".summary-stats .meta-panel")
        }
        assert summary_stats["Trends"] == "25"
        assert summary_stats["Ideas"] == "13"
        summary_meta = page.select_one(".collection-summary-section .meta-date")
        assert isinstance(summary_meta, Tag)
        assert f"Page {page_number} of 4" in summary_meta.get_text(" ", strip=True)
        assert "trends" not in summary_meta.get_text(" ", strip=True)
        assert "ideas" not in summary_meta.get_text(" ", strip=True)
        assert page.select_one(".paired-collection-layout") is None
        previous_href = None
        if page_number == 2:
            previous_href = "../../../shared-topic.html"
        elif page_number > 2:
            previous_href = f"../{page_number - 1}/index.html"
        next_href = (
            "shared-topic/page/2/index.html"
            if page_number == 1
            else (
                f"../{page_number + 1}/index.html"
                if page_number < len(topic_pages)
                else None
            )
        )
        _assert_pager(
            page_path=page_path,
            current_page=page_number,
            total_pages=4,
            previous_href=previous_href,
            next_href=next_href,
        )

    _assert_local_links_resolve(topic_pages[1])


def test_export_trend_static_site_renders_new_trend_and_idea_contracts(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "notes"
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    evidence_doc_id = _seed_item_doc_with_authors(
        repository=repository,
        published_at=datetime(2026, 2, 25, 12, tzinfo=UTC),
    )

    trend_note = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=71,
        title="Agent systems",
        granularity="day",
        period_start=datetime(2026, 2, 25, tzinfo=UTC),
        period_end=datetime(2026, 2, 26, tzinfo=UTC),
        run_id="run-site-1",
        overview_md="Agent workflows are getting more production-ready.",
        topics=["agents", "embedded_ai"],
        clusters=[
            {
                "title": "Release discipline",
                "content_md": "Verification moved into the shipping path.",
                "evidence_refs": [
                    {
                        "doc_id": 1,
                        "chunk_index": 0,
                        "title": "CodeScout",
                        "href": "../Inbox/2026-02-25--codescout.md",
                        "reason": "The note grounds release discipline in the corpus.",
                    }
                ],
            }
        ],
    )
    trend_note.with_suffix(".pdf").write_bytes(b"%PDF-1.7\n")

    _ = write_markdown_ideas_note(
        repository=repository,
        output_dir=output_dir,
        pass_output_id=9,
        upstream_pass_output_id=7,
        granularity="day",
        period_start=datetime(2026, 2, 25, tzinfo=UTC),
        period_end=datetime(2026, 2, 26, tzinfo=UTC),
        run_id="run-site-ideas",
        status="succeeded",
        payload=TrendIdeasPayload.model_validate(
            {
                "title": "Operator wedges",
                "granularity": "day",
                "period_start": datetime(2026, 2, 25, tzinfo=UTC).isoformat(),
                "period_end": datetime(2026, 2, 26, tzinfo=UTC).isoformat(),
                "summary_md": "Structured release controls now feel overdue.",
                "ideas": [
                    {
                        "title": "Prompt release gate",
                        "content_md": "Add a release gate before prompt rollout.",
                        "evidence_refs": [
                            {
                                "doc_id": evidence_doc_id,
                                "chunk_index": 0,
                                "reason": "The trend note ties verification to rollout control.",
                            }
                        ],
                    }
                ],
            }
        ),
        topics=["agents"],
    )

    site_dir = tmp_path / "site"
    manifest_path = export_trend_static_site(
        input_dir=output_dir / "Trends",
        output_dir=site_dir,
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    trend_html = (site_dir / "trends" / f"{trend_note.stem}.html").read_text(
        encoding="utf-8"
    )
    ideas_html = (site_dir / "ideas" / "day--2026-02-25--ideas.html").read_text(
        encoding="utf-8"
    )
    index_html = (site_dir / "index.html").read_text(encoding="utf-8")
    site_css = (site_dir / "assets" / "site.css").read_text(encoding="utf-8")
    single_page_collections = [
        site_dir / "trends" / "index.html",
        site_dir / "ideas" / "index.html",
        site_dir / "topics" / "index.html",
        site_dir / "archive.html",
        site_dir / "topics" / "agents.html",
    ]

    assert manifest["trends_total"] == 1
    assert "Overview" in trend_html
    assert "Findings" in trend_html
    assert "Sources" in trend_html
    assert "Trend brief" not in trend_html
    assert "<div class='hero-kicker'>Trend</div>" in trend_html
    assert "Day · 2026-02-25" in trend_html
    assert "Top shifts" not in trend_html
    assert "Counter-signal" not in trend_html
    assert "Representative sources" not in trend_html
    assert "Summary" in ideas_html
    assert "Ideas" in ideas_html
    assert "Prompt release gate" in ideas_html
    assert "Idea brief" not in ideas_html
    assert "Opportunities" not in ideas_html
    assert "Idea notes from the trend snapshot" not in ideas_html
    assert "Evidence-grounded idea notes" not in ideas_html
    assert "Peng Wang" in ideas_html
    assert "Hao Wang" in ideas_html
    assert "[, &quot;" not in ideas_html
    assert "Best bet" not in ideas_html
    assert "Alternate" not in ideas_html
    assert "Anti-thesis" not in ideas_html
    index_page = BeautifulSoup(index_html, "html.parser")
    trend_page = BeautifulSoup(trend_html, "html.parser")
    idea_page = BeautifulSoup(ideas_html, "html.parser")
    assert "Agent systems" in index_html
    assert len(index_page.select(".home-feature")) == 1
    assert len(index_page.select(".latest-feed-row")) == 1
    assert index_page.select(".home-intro > .hero-kicker") == []
    assert [
        node.get_text(" ", strip=True)
        for node in index_page.select(".home-intro > .home-title")
    ] == ["Notes"]
    assert index_page.select(".home-latest .section-kicker") == []
    assert [
        node.get_text(" ", strip=True)
        for node in index_page.select(".home-latest .section-title")
    ] == ["Latest"]
    assert index_page.select_one(".paired-collection-layout") is None
    assert "Latest window" not in index_html
    assert "1 trend · 1 idea" not in index_html
    assert "Open brief" not in index_html
    assert "embedded_ai" not in index_page.get_text(" ", strip=True)
    assert "Embedded AI" in index_page.get_text(" ", strip=True)
    assert "Trend briefs" not in index_html
    assert "Idea briefs" not in index_html
    assert "Trends" in index_html
    assert "Ideas" in index_html
    assert trend_page.get_text(" ", strip=True).count(
        "Agent workflows are getting more production-ready."
    ) == 1
    assert idea_page.get_text(" ", strip=True).count(
        "Structured release controls now feel overdue."
    ) == 1
    assert trend_page.select_one(".detail-hero-side") is None
    assert idea_page.select_one(".detail-hero-side") is None
    assert trend_page.select_one(".repo-cta-card") is None
    assert idea_page.select_one(".repo-cta-card") is None
    assert {node.name for node in trend_page.select(".cluster-card .section-label")} == {
        "h4"
    }
    assert "align-items: start;" in site_css
    assert "align-self: start;" in site_css
    assert RECOLETA_REPO_URL in index_html
    assert RECOLETA_QUICKSTART_URL in index_html
    favicon_path = site_dir / "assets" / "favicon.svg"
    favicon_link = index_page.select_one("link[rel~='icon']")
    assert favicon_path.exists()
    assert isinstance(favicon_link, Tag)
    assert favicon_link.get("href") == "assets/favicon.svg"
    assert all(
        _read_html(page_path).select_one("nav.collection-pagination") is None
        for page_path in single_page_collections
    )


def test_export_trend_static_site_idea_markdown_fallback_uses_current_shape_only(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "notes"
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    evidence_doc_id = _seed_item_doc_with_authors(
        repository=repository,
        published_at=datetime(2026, 2, 25, 12, tzinfo=UTC),
    )

    _ = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=71,
        title="Agent systems",
        granularity="day",
        period_start=datetime(2026, 2, 25, tzinfo=UTC),
        period_end=datetime(2026, 2, 26, tzinfo=UTC),
        run_id="run-site-fallback-1",
        overview_md="Agent workflows are getting more production-ready.",
        topics=["agents", "tooling"],
        clusters=[
            {
                "title": "Release discipline",
                "content_md": "Verification moved into the shipping path.",
                "evidence_refs": [
                    {
                        "doc_id": 1,
                        "chunk_index": 0,
                        "title": "CodeScout",
                        "href": "../Inbox/2026-02-25--codescout.md",
                        "reason": "The note grounds release discipline in the corpus.",
                    }
                ],
            }
        ],
    )

    idea_note = write_markdown_ideas_note(
        repository=repository,
        output_dir=output_dir,
        pass_output_id=9,
        upstream_pass_output_id=7,
        granularity="day",
        period_start=datetime(2026, 2, 25, tzinfo=UTC),
        period_end=datetime(2026, 2, 26, tzinfo=UTC),
        run_id="run-site-fallback-ideas",
        status="succeeded",
        payload=TrendIdeasPayload.model_validate(
            {
                "title": "Operator wedges",
                "granularity": "day",
                "period_start": datetime(2026, 2, 25, tzinfo=UTC).isoformat(),
                "period_end": datetime(2026, 2, 26, tzinfo=UTC).isoformat(),
                "summary_md": "Structured release controls now feel overdue.",
                "ideas": [
                    {
                        "title": "Prompt release gate",
                        "content_md": "Add a release gate before prompt rollout.",
                        "evidence_refs": [
                            {
                                "doc_id": evidence_doc_id,
                                "chunk_index": 0,
                                "reason": "The trend note ties verification to rollout control.",
                            }
                        ],
                    }
                ],
            }
        ),
        topics=["agents"],
    )
    idea_note.write_text(
        "\n".join(
            [
                "---",
                "kind: ideas",
                "granularity: day",
                "period_start: 2026-02-25T00:00:00+00:00",
                "period_end: 2026-02-26T00:00:00+00:00",
                "run_id: run-site-fallback-ideas",
                "status: succeeded",
                "topics:",
                "- agents",
                "---",
                "",
                "# Operator wedges",
                "",
                "## Summary",
                "",
                "Structured release controls now feel overdue.",
                "",
                "## Prompt release gate",
                "",
                "**Why now.** Verification failures are reaching production.",
                "",
                "**What changed.** Tooling can gate prompt releases.",
                "",
                "**Validation next step.** Run the gate on one release train.",
                "",
                "### Evidence",
                "",
                "- [Grounded runtime checks](../Inbox/idea-static-site-authors.md)",
            ]
        ),
        encoding="utf-8",
    )
    presentation_sidecar_path(note_path=idea_note).unlink()

    site_dir = tmp_path / "site"
    export_trend_static_site(
        input_dir=output_dir / "Trends",
        output_dir=site_dir,
    )

    ideas_html = (site_dir / "ideas" / "day--2026-02-25--ideas.html").read_text(
        encoding="utf-8"
    )

    assert "Summary" in ideas_html
    assert "Prompt release gate" in ideas_html
    assert "Evidence" in ideas_html
    assert "<div class='meta-panel-label'>Ideas</div>" not in ideas_html
    assert "<div class='meta-panel-label'>Evidence</div>" not in ideas_html
    assert "<div class='meta-panel-label'>Status</div>" not in ideas_html
    assert "idea-opportunity-meta-row" not in ideas_html
    assert "idea-opportunity-block" not in ideas_html
    assert "<div class='idea-opportunity-label'>Why now</div>" not in ideas_html
    assert "<div class='idea-opportunity-label'>What changed</div>" not in ideas_html
    assert (
        "<div class='idea-opportunity-label'>Validation next step</div>"
        not in ideas_html
    )
    assert "Opportunities" not in ideas_html


def test_multilingual_export_validates_language_names_before_resetting_output(
    tmp_path: Path,
) -> None:
    notes_root = tmp_path / "notes"
    for trend_doc_id, title, language_code, output_dir in [
        (301, "Known language", "en", notes_root),
        (302, "Unknown language", "xx", notes_root / "Localized" / "xx"),
    ]:
        write_markdown_trend_note(
            output_dir=output_dir,
            trend_doc_id=trend_doc_id,
            title=title,
            granularity="day",
            period_start=datetime(2026, 3, 1, tzinfo=UTC),
            period_end=datetime(2026, 3, 2, tzinfo=UTC),
            run_id=f"run-site-language-{language_code}",
            overview_md="## Overview\n\nResearch note.\n",
            topics=["agents"],
            clusters=[],
            language_code=language_code,
        )

    site_dir = tmp_path / "site"
    site_dir.mkdir()
    sentinel = site_dir / "existing-output.txt"
    sentinel.write_text("keep", encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported site language code 'xx'"):
        export_trend_static_site(
            input_dir=notes_root,
            output_dir=site_dir,
            default_language_code="en",
        )

    assert sentinel.read_text(encoding="utf-8") == "keep"


def test_export_trend_static_site_metrics_recorder_uses_low_cardinality_step_names(
    tmp_path: Path,
) -> None:
    notes_root = tmp_path / "notes"
    write_markdown_trend_note(
        output_dir=notes_root,
        trend_doc_id=301,
        title="Agent Systems",
        granularity="day",
        period_start=datetime(2026, 3, 1, tzinfo=UTC),
        period_end=datetime(2026, 3, 2, tzinfo=UTC),
        run_id="run-site-metrics-en",
        overview_md="## Overview\n\nEnglish note.\n",
        topics=["agents"],
        clusters=[],
        language_code="en",
    )
    write_markdown_trend_note(
        output_dir=notes_root / "Localized" / "zh-cn",
        trend_doc_id=301,
        title="智能体系统",
        granularity="day",
        period_start=datetime(2026, 3, 1, tzinfo=UTC),
        period_end=datetime(2026, 3, 2, tzinfo=UTC),
        run_id="run-site-metrics-zh",
        overview_md="## Overview\n\n中文笔记。\n",
        topics=["agents"],
        clusters=[],
        language_code="zh-CN",
    )

    calls: list[tuple[str, int, dict[str, object]]] = []

    def _record_metric(
        step_name: str,
        duration_ms: int,
        metadata: dict[str, object],
    ) -> None:
        calls.append((step_name, duration_ms, metadata))

    site_dir = tmp_path / "site"
    manifest_path = export_trend_static_site(
        input_dir=notes_root,
        output_dir=site_dir,
        default_language_code="en",
        metrics_recorder=_record_metric,
    )

    expected_step_names = {
        "multilang.prepare_output",
        "multilang.export_language",
        "multilang.export_languages",
        "multilang.apply_language_overrides",
        "multilang.aggregate_manifest",
        "multilang.email_links",
        "multilang.write_root_files",
    }

    assert manifest_path.exists()
    assert calls
    assert {step_name for step_name, _duration_ms, _metadata in calls} <= expected_step_names
    assert "multilang.export_language" in {
        step_name for step_name, _duration_ms, _metadata in calls
    }
    assert "multilang.apply_language_overrides" in {
        step_name for step_name, _duration_ms, _metadata in calls
    }
    assert all(duration_ms >= 0 for _step_name, duration_ms, _metadata in calls)

    english_home = _read_html(site_dir / "en" / "index.html")
    chinese_home = _read_html(site_dir / "zh-cn" / "index.html")
    english_html = english_home.select_one("html")
    chinese_html = chinese_home.select_one("html")
    assert isinstance(english_html, Tag)
    assert isinstance(chinese_html, Tag)
    assert english_html["lang"] == "en"
    assert chinese_html["lang"] == "zh-CN"
    assert [
        node.get_text(" ", strip=True)
        for node in english_home.select(".nav-links .nav-link")
    ] == ["Home", "Trends", "Ideas", "Topics", "Archive"]
    assert [
        node.get_text(" ", strip=True)
        for node in chinese_home.select(".nav-links .nav-link")
    ] == ["首页", "趋势", "想法", "主题", "归档"]
    assert [
        node.get_text(" ", strip=True)
        for node in english_home.select(".home-intro > .home-title")
    ] == ["Notes"]
    assert [
        node.get_text(" ", strip=True)
        for node in chinese_home.select(".home-intro > .home-title")
    ] == ["笔记"]
    assert [
        node.get_text(" ", strip=True)
        for node in english_home.select(".home-latest .section-title")
    ] == ["Latest"]
    assert [
        node.get_text(" ", strip=True)
        for node in chinese_home.select(".home-latest .section-title")
    ] == ["最新"]
    assert english_home.select(".home-intro > .hero-kicker") == []
    assert chinese_home.select(".home-intro > .hero-kicker") == []
    assert english_home.select(".home-latest .section-kicker") == []
    assert chinese_home.select(".home-latest .section-kicker") == []
    assert "Overview" not in _read_html(
        next((site_dir / "zh-cn" / "trends").glob("*.html"))
    ).get_text(" ", strip=True)
