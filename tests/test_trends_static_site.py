from __future__ import annotations

from datetime import UTC, datetime, timedelta
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup, Tag
import pytest

from recoleta.presentation import presentation_sidecar_path
from recoleta.site import (
    RECOLETA_QUICKSTART_URL,
    RECOLETA_REPO_URL,
    _item_action_label,
    export_trend_static_site,
)
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


def _page_titles(paths: list[Path], *, selector: str) -> list[str]:
    return [
        node.get_text(" ", strip=True)
        for path in paths
        for node in _read_html(path).select(selector)
    ]


def _collection_card_titles(page_path: Path, *, heading: str) -> list[str]:
    for section in _read_html(page_path).select(".collection-section"):
        section_heading = section.select_one(".section-title")
        if (
            isinstance(section_heading, Tag)
            and section_heading.get_text(" ", strip=True) == heading
        ):
            return [
                node.get_text(" ", strip=True)
                for node in section.select(".trend-card .card-title")
            ]
    raise AssertionError(f"{page_path}: collection section not found: {heading}")


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
        "shared-topic",
        *(f"topic-{index:02d}" for index in range(_PAGINATION_TREND_TOTAL)),
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
        "topic_column_page_size": 6,
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
        "topics/shared-topic/page/5/index.html",
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


def test_export_trend_static_site_paginates_topic_columns_with_shared_page_number(
    paginated_site: Path,
) -> None:
    topic_pages = [paginated_site / "topics" / "shared-topic.html"] + [
        paginated_site
        / "topics"
        / "shared-topic"
        / "page"
        / str(page_number)
        / "index.html"
        for page_number in range(2, 6)
    ]
    assert all(path.exists() for path in topic_pages)

    trend_titles = [
        title
        for page_path in topic_pages
        for title in _collection_card_titles(page_path, heading="Trends")
    ]
    idea_titles = [
        title
        for page_path in topic_pages
        for title in _collection_card_titles(page_path, heading="Ideas")
    ]
    assert trend_titles == [
        f"Trend {index:02d}" for index in reversed(range(_PAGINATION_TREND_TOTAL))
    ]
    assert idea_titles == [
        f"Idea {index:02d}" for index in reversed(range(_PAGINATION_IDEA_TOTAL))
    ]
    assert [
        len(_collection_card_titles(path, heading="Trends")) for path in topic_pages
    ] == [6, 6, 6, 6, 1]
    assert [
        len(_collection_card_titles(path, heading="Ideas")) for path in topic_pages
    ] == [6, 6, 1, 0, 0]

    for page_number, page_path in enumerate(topic_pages, start=1):
        page = _read_html(page_path)
        page_text = page.get_text(" ", strip=True)
        assert "25 trends" in page_text
        assert "13 ideas" in page_text
        summary_meta = page.select_one(".collection-summary-section .meta-date")
        assert isinstance(summary_meta, Tag)
        assert f"Page {page_number} of 5" in summary_meta.get_text(" ", strip=True)
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
            total_pages=5,
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
    assert "Clusters" in trend_html
    assert "Evidence" in trend_html
    assert "Trend brief" not in trend_html
    assert "Trends · 2026-02-25" in trend_html
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
    assert "Agent systems" in index_html
    assert "Latest window" in index_html
    assert "Trend briefs" not in index_html
    assert "Idea briefs" not in index_html
    assert "Trends" in index_html
    assert "Ideas" in index_html
    assert "align-items: start;" in site_css
    assert "align-self: start;" in site_css
    assert RECOLETA_REPO_URL in index_html
    assert RECOLETA_QUICKSTART_URL in index_html
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
    assert "<div class='meta-panel-label'>Ideas</div><div class='meta-panel-value'>1</div>" in ideas_html
    assert "<div class='meta-panel-label'>Evidence</div><div class='meta-panel-value'>1</div>" in ideas_html
    assert "idea-opportunity-meta-row" not in ideas_html
    assert "idea-opportunity-block" not in ideas_html
    assert "<div class='idea-opportunity-label'>Why now</div>" not in ideas_html
    assert "<div class='idea-opportunity-label'>What changed</div>" not in ideas_html
    assert (
        "<div class='idea-opportunity-label'>Validation next step</div>"
        not in ideas_html
    )
    assert "Opportunities" not in ideas_html


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
