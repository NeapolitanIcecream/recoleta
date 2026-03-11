from __future__ import annotations

from datetime import UTC, datetime
import subprocess
import sys
from types import SimpleNamespace
from typing import cast

import pytest
import respx
import httpx
from huggingface_hub import HfApi
from huggingface_hub.hf_api import PaperInfo

from recoleta.sources import (
    fetch_arxiv_drafts,
    fetch_hn_drafts,
    fetch_hf_daily_papers_drafts,
    fetch_openreview_drafts,
    fetch_rss_drafts,
    SourcePullResult,
    SourcePullStateSnapshot,
)


def test_fetch_rss_drafts_fetches_via_httpx_and_parses_feed(
    respx_mock: respx.Router,
) -> None:
    rss_xml = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Example Feed</title>
    <item>
      <title>Hello World</title>
      <link>https://example.com/hello</link>
      <guid>guid-hello</guid>
      <pubDate>Mon, 20 Jan 2025 10:00:00 GMT</pubDate>
      <author>Alice</author>
    </item>
  </channel>
</rss>
"""
    respx_mock.get("https://example.com/feed.xml").respond(
        200,
        text=rss_xml,
        headers={"Content-Type": "application/rss+xml; charset=utf-8"},
    )
    drafts = fetch_rss_drafts(
        feed_urls=["https://example.com/feed.xml"], source="rss", max_items_per_feed=10
    )
    assert len(drafts) == 1
    assert drafts[0].canonical_url == "https://example.com/hello"
    assert drafts[0].title == "Hello World"
    assert drafts[0].source_item_id == "guid-hello"
    assert drafts[0].raw_metadata["feed_title"] == "Example Feed"


def test_fetch_rss_drafts_discovers_feed_from_site_url(
    respx_mock: respx.Router,
) -> None:
    site_html = """<html><head>
<link rel="alternate" type="application/rss+xml" href="/feed.xml" title="RSS" />
</head><body></body></html>"""
    rss_xml = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Discovered Feed</title>
    <item>
      <title>Discovered Post</title>
      <link>https://jack.example/posts/discovered</link>
      <guid>jack-post-1</guid>
    </item>
  </channel>
</rss>
"""
    respx_mock.get("https://jack.example/").respond(
        200,
        text=site_html,
        headers={"Content-Type": "text/html; charset=utf-8"},
    )
    respx_mock.get("https://jack.example/feed.xml").respond(
        200,
        text=rss_xml,
        headers={"Content-Type": "application/rss+xml; charset=utf-8"},
    )

    drafts = fetch_rss_drafts(
        feed_urls=["https://jack.example/"], source="rss", max_items_per_feed=1
    )

    assert len(drafts) == 1
    assert drafts[0].canonical_url == "https://jack.example/posts/discovered"
    assert drafts[0].source_item_id == "jack-post-1"
    assert drafts[0].raw_metadata["feed_url"] == "https://jack.example/feed.xml"
    assert drafts[0].raw_metadata["feed_discovered_from"] == "https://jack.example/"
    assert drafts[0].raw_metadata["feed_title"] == "Discovered Feed"


def test_fetch_rss_drafts_prefers_primary_feed_over_comments_feed(
    respx_mock: respx.Router,
) -> None:
    site_html = """<html><head>
<link rel="alternate" type="application/rss+xml" href="https://jack.example/feed/" title="RSS" />
<link rel="alternate" type="application/rss+xml" href="https://jack.example/comments/feed/" title="Comments" />
</head><body></body></html>"""
    main_rss_xml = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Main Feed</title>
    <item>
      <title>Main Post</title>
      <link>https://jack.example/posts/main</link>
      <guid>main-post-1</guid>
    </item>
  </channel>
</rss>
"""
    comments_rss_xml = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Comments Feed</title>
    <item>
      <title>Comment</title>
      <link>https://jack.example/posts/main#comment-1</link>
      <guid>comment-1</guid>
    </item>
  </channel>
</rss>
"""
    respx_mock.get("https://jack.example/").respond(
        200,
        text=site_html,
        headers={"Content-Type": "text/html; charset=utf-8"},
    )
    respx_mock.get("https://jack.example/feed/").respond(
        200,
        text=main_rss_xml,
        headers={"Content-Type": "application/rss+xml; charset=utf-8"},
    )
    respx_mock.get("https://jack.example/comments/feed/").respond(
        200,
        text=comments_rss_xml,
        headers={"Content-Type": "application/rss+xml; charset=utf-8"},
    )

    drafts = fetch_rss_drafts(
        feed_urls=["https://jack.example/"], source="rss", max_items_per_feed=1
    )

    assert len(drafts) == 1
    assert drafts[0].title == "Main Post"
    assert drafts[0].canonical_url == "https://jack.example/posts/main"
    assert drafts[0].raw_metadata["feed_url"] == "https://jack.example/feed/"


def test_fetch_rss_drafts_filters_to_requested_event_window_before_limit(
    respx_mock: respx.Router,
) -> None:
    rss_xml = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Windowed Feed</title>
    <item>
      <title>Too New</title>
      <link>https://example.com/too-new</link>
      <guid>guid-too-new</guid>
      <pubDate>Tue, 21 Jan 2025 10:00:00 GMT</pubDate>
    </item>
    <item>
      <title>Still Too New</title>
      <link>https://example.com/still-too-new</link>
      <guid>guid-still-too-new</guid>
      <pubDate>Tue, 21 Jan 2025 08:00:00 GMT</pubDate>
    </item>
    <item>
      <title>Window Match</title>
      <link>https://example.com/window-match</link>
      <guid>guid-window-match</guid>
      <pubDate>Mon, 20 Jan 2025 12:00:00 GMT</pubDate>
    </item>
  </channel>
</rss>
"""
    respx_mock.get("https://feeds.example/windowed.xml").respond(
        200,
        text=rss_xml,
        headers={"Content-Type": "application/rss+xml; charset=utf-8"},
    )

    drafts = fetch_rss_drafts(
        feed_urls=["https://feeds.example/windowed.xml"],
        source="rss",
        max_items_per_feed=1,
        period_start=datetime(2025, 1, 20, tzinfo=UTC),
        period_end=datetime(2025, 1, 21, tzinfo=UTC),
    )

    assert len(drafts) == 1
    assert drafts[0].source_item_id == "guid-window-match"
    assert drafts[0].canonical_url == "https://example.com/window-match"


def test_fetch_rss_drafts_uses_conditional_headers_from_pull_state(
    respx_mock: respx.Router,
) -> None:
    observed_headers: dict[str, str] = {}

    def capture_request(request):  # type: ignore[no-untyped-def]
        observed_headers["if-none-match"] = request.headers.get("if-none-match", "")
        observed_headers["if-modified-since"] = request.headers.get(
            "if-modified-since", ""
        )
        return httpx.Response(status_code=304)

    respx_mock.get("https://example.com/feed.xml").mock(side_effect=capture_request)

    drafts = fetch_rss_drafts(
        feed_urls=["https://example.com/feed.xml"],
        source="rss",
        max_items_per_feed=10,
        pull_state_lookup=lambda scope_kind, scope_key: (
            SourcePullStateSnapshot(
                scope_kind=scope_kind,
                scope_key=scope_key,
                etag='"feed-etag"',
                last_modified="Wed, 22 Jan 2025 00:00:00 GMT",
            )
            if scope_kind == "feed" and scope_key == "https://example.com/feed.xml"
            else None
        ),
    )

    assert len(drafts) == 0
    assert observed_headers == {
        "if-none-match": '"feed-etag"',
        "if-modified-since": "Wed, 22 Jan 2025 00:00:00 GMT",
    }


def test_fetch_hf_daily_papers_drafts_uses_hf_api_and_preserves_daily_submission_time(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    base_url = HfApi().endpoint.rstrip("/")
    calls: list[dict[str, object]] = []

    def fake_list_daily_papers(
        self,
        *,
        date=None,
        limit=None,
        **kwargs,  # type: ignore[no-untyped-def]
    ):
        calls.append({"date": date, "limit": limit, **kwargs})
        return iter(
            [
                PaperInfo(
                    id="1605.08386",
                    title="Attention Is All You Need",
                    paper={
                        "authors": [{"name": "Alice"}, {"name": "Bob"}],
                        "publishedAt": "2025-01-20T00:00:00Z",
                    },
                    submittedOnDailyAt="2025-01-21T09:15:00Z",
                    source="arxiv",
                    discussionId="123",
                )
            ]
        )

    monkeypatch.setattr(HfApi, "list_daily_papers", fake_list_daily_papers)

    drafts = fetch_hf_daily_papers_drafts(max_items=1)

    assert calls == [{"date": None, "limit": 2}]
    assert len(drafts) == 1
    assert drafts[0].source_item_id == "1605.08386"
    assert drafts[0].title == "Attention Is All You Need"
    assert drafts[0].authors == ["Alice", "Bob"]
    assert drafts[0].canonical_url == f"{base_url}/papers/1605.08386"
    assert drafts[0].published_at == datetime(2025, 1, 21, 9, 15, tzinfo=UTC)
    assert drafts[0].raw_metadata["paper_published_at"] == "2025-01-20T00:00:00+00:00"


def test_fetch_hf_daily_papers_drafts_fetches_each_day_in_requested_window(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[str | None] = []

    def fake_list_daily_papers(
        self,
        *,
        date=None,
        limit=None,
        **kwargs,  # type: ignore[no-untyped-def]
    ):
        calls.append(date)
        if date == "2025-01-20":
            return iter(
                [
                    PaperInfo(
                        id="paper-20",
                        title="Paper 20",
                        paper={"authors": [{"name": "Alice"}]},
                        submittedOnDailyAt="2025-01-20T08:00:00Z",
                    )
                ]
            )
        if date == "2025-01-21":
            return iter(
                [
                    PaperInfo(
                        id="paper-21",
                        title="Paper 21",
                        paper={"authors": [{"name": "Bob"}]},
                        submittedOnDailyAt="2025-01-21T08:00:00Z",
                    )
                ]
            )
        return iter([])

    monkeypatch.setattr(HfApi, "list_daily_papers", fake_list_daily_papers)

    drafts = fetch_hf_daily_papers_drafts(
        max_items=10,
        period_start=datetime(2025, 1, 20, tzinfo=UTC),
        period_end=datetime(2025, 1, 22, tzinfo=UTC),
    )

    assert calls == ["2025-01-20", "2025-01-21"]
    assert [draft.source_item_id for draft in drafts] == ["paper-20", "paper-21"]
    assert [draft.published_at is not None for draft in drafts] == [True, True]
    assert [
        draft.published_at.date().isoformat() for draft in drafts if draft.published_at
    ] == [
        "2025-01-20",
        "2025-01-21",
    ]


def test_fetch_hf_daily_papers_drafts_keeps_watermark_when_limit_hides_backlog(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    observed_limits: list[int | None] = []
    watermark = datetime(2025, 1, 20, 12, tzinfo=UTC)
    papers = [
        PaperInfo(
            id="paper-1",
            title="Paper 1",
            paper={"authors": [{"name": "Alice"}]},
            submittedOnDailyAt="2025-01-21T09:00:00Z",
        ),
        PaperInfo(
            id="paper-2",
            title="Paper 2",
            paper={"authors": [{"name": "Bob"}]},
            submittedOnDailyAt="2025-01-21T08:00:00Z",
        ),
    ]

    def fake_list_daily_papers(
        self,
        *,
        date=None,
        limit=None,
        **kwargs,  # type: ignore[no-untyped-def]
    ):
        _ = self, date, kwargs
        observed_limits.append(limit if limit is None else int(limit))
        visible = len(papers) if limit is None else int(limit)
        return iter(papers[:visible])

    monkeypatch.setattr(HfApi, "list_daily_papers", fake_list_daily_papers)

    result = cast(
        SourcePullResult,
        fetch_hf_daily_papers_drafts(
            max_items=1,
            include_stats=True,
            pull_state_lookup=lambda scope_kind, scope_key: (
                SourcePullStateSnapshot(
                    scope_kind=scope_kind,
                    scope_key=scope_key,
                    watermark_published_at=watermark,
                )
                if scope_kind == "global" and scope_key == "daily"
                else None
            ),
        ),
    )

    assert observed_limits == [2]
    assert [draft.source_item_id for draft in result.drafts] == ["paper-1"]
    assert result.deferred_total == 1
    assert len(result.state_updates) == 1
    assert result.state_updates[0].watermark_published_at == watermark


def test_fetch_arxiv_drafts_adds_submitted_date_range_when_window_requested(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    searches: list[dict[str, object]] = []

    class FakeSearch:
        def __init__(self, *, query, max_results, sort_by):  # type: ignore[no-untyped-def]
            searches.append(
                {
                    "query": query,
                    "max_results": max_results,
                    "sort_by": sort_by,
                }
            )

    class FakeClient:
        def results(self, search):  # noqa: ANN001
            _ = search
            return iter([])

    import recoleta.sources as source_module

    monkeypatch.setattr(source_module.arxiv, "Search", FakeSearch)
    monkeypatch.setattr(source_module.arxiv, "Client", FakeClient)

    fetch_arxiv_drafts(
        queries=["cat:cs.AI"],
        max_results_per_run=5,
        period_start=datetime(2025, 1, 20, tzinfo=UTC),
        period_end=datetime(2025, 1, 21, tzinfo=UTC),
    )

    assert searches == [
        {
            "query": "(cat:cs.AI) AND submittedDate:[202501200000 TO 202501202359]",
            "max_results": 5,
            "sort_by": source_module.arxiv.SortCriterion.SubmittedDate,
        }
    ]


def test_fetch_openreview_drafts_uses_window_filters_and_excludes_future_notes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[dict[str, object]] = []

    class FakeClient:
        def __init__(self, *args, **kwargs):  # noqa: ANN002,ANN003
            _ = args, kwargs

        def get_notes(self, **kwargs):  # type: ignore[no-untyped-def]
            calls.append(dict(kwargs))
            return [
                SimpleNamespace(
                    id="future-note",
                    content={
                        "title": {"value": "Future Note"},
                        "authors": {"value": ["Alice"]},
                    },
                    tcdate=int(
                        datetime(2025, 1, 21, 12, tzinfo=UTC).timestamp() * 1000
                    ),
                ),
                SimpleNamespace(
                    id="window-note",
                    content={
                        "title": {"value": "Window Note"},
                        "authors": {"value": ["Bob"]},
                    },
                    tcdate=int(
                        datetime(2025, 1, 20, 12, tzinfo=UTC).timestamp() * 1000
                    ),
                ),
            ]

    import recoleta.sources as source_module

    monkeypatch.setattr(source_module.openreview, "Client", FakeClient)

    drafts = fetch_openreview_drafts(
        venues=["ICLR.cc/2026/Conference"],
        max_results_per_venue=5,
        period_start=datetime(2025, 1, 20, tzinfo=UTC),
        period_end=datetime(2025, 1, 21, tzinfo=UTC),
    )

    assert calls[0]["mintcdate"] == int(
        datetime(2025, 1, 20, tzinfo=UTC).timestamp() * 1000
    )
    assert calls[0]["sort"] == "tcdate:desc"
    assert [draft.source_item_id for draft in drafts] == ["window-note"]


def test_fetch_hn_drafts_uses_algolia_search_for_requested_window(
    respx_mock: respx.Router,
) -> None:
    observed_queries: list[dict[str, str]] = []
    respx_mock.get("https://hn.algolia.com/api/v1/search_by_date").mock(
        side_effect=lambda request: (
            observed_queries.append(dict(request.url.params.multi_items())),
            httpx.Response(
                200,
                json={
                    "hits": [
                        {
                            "objectID": "hn-1",
                            "title": "Windowed HN Story",
                            "author": "dang",
                            "created_at_i": int(
                                datetime(2025, 1, 20, 12, tzinfo=UTC).timestamp()
                            ),
                            "url": "https://example.com/windowed-hn-story",
                        }
                    ],
                    "nbPages": 1,
                    "page": 0,
                },
            ),
        )[1]
    )

    drafts = fetch_hn_drafts(
        feed_urls=["https://news.ycombinator.com/rss"],
        max_items_per_feed=5,
        period_start=datetime(2025, 1, 20, tzinfo=UTC),
        period_end=datetime(2025, 1, 21, tzinfo=UTC),
    )

    assert len(drafts) == 1
    assert drafts[0].source_item_id == "hn-1"
    assert drafts[0].canonical_url == "https://example.com/windowed-hn-story"
    assert drafts[0].authors == ["dang"]
    assert observed_queries[0]["tags"] == "story"
    assert "created_at_i>=" in observed_queries[0]["numericFilters"]
    assert "created_at_i<" in observed_queries[0]["numericFilters"]


def test_fetch_arxiv_drafts_uses_saved_watermark_when_no_window_requested(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    searches: list[dict[str, object]] = []

    class FakeSearch:
        def __init__(self, *, query, max_results, sort_by):  # type: ignore[no-untyped-def]
            searches.append(
                {
                    "query": query,
                    "max_results": max_results,
                    "sort_by": sort_by,
                }
            )

    class FakeClient:
        def results(self, search):  # noqa: ANN001
            _ = search
            return iter([])

    import recoleta.sources as source_module

    monkeypatch.setattr(source_module.arxiv, "Search", FakeSearch)
    monkeypatch.setattr(source_module.arxiv, "Client", FakeClient)

    fetch_arxiv_drafts(
        queries=["cat:cs.AI"],
        max_results_per_run=5,
        pull_state_lookup=lambda scope_kind, scope_key: (
            SourcePullStateSnapshot(
                scope_kind=scope_kind,
                scope_key=scope_key,
                watermark_published_at=datetime(2025, 1, 20, 12, 34, tzinfo=UTC),
            )
            if scope_kind == "query" and scope_key == "cat:cs.AI"
            else None
        ),
    )

    assert searches and "submittedDate:[202501201234 TO " in str(searches[0]["query"])


def test_cli_import_does_not_eager_load_runtime_modules() -> None:
    """Regression: CLI import path should stay light for `--help` startup latency."""

    probe = "\n".join(
        [
            "import sys",
            "import recoleta.cli  # noqa: F401",
            "targets = ('recoleta.pipeline', 'recoleta.storage', 'recoleta.config')",
            "print(' '.join('1' if name in sys.modules else '0' for name in targets))",
        ]
    )
    completed = subprocess.run(
        [sys.executable, "-c", probe],
        check=True,
        capture_output=True,
        text=True,
    )
    assert completed.stdout.strip() == "0 0 0"
