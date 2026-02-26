from __future__ import annotations

import subprocess
import sys

import pytest
import respx
from huggingface_hub import HfApi

from recoleta.sources import fetch_hf_daily_papers_drafts, fetch_rss_drafts

def test_fetch_rss_drafts_fetches_via_httpx_and_parses_feed(respx_mock: respx.Router) -> None:
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
    drafts = fetch_rss_drafts(feed_urls=["https://example.com/feed.xml"], source="rss", max_items_per_feed=10)
    assert len(drafts) == 1
    assert drafts[0].canonical_url == "https://example.com/hello"
    assert drafts[0].title == "Hello World"
    assert drafts[0].source_item_id == "guid-hello"
    assert drafts[0].raw_metadata["feed_title"] == "Example Feed"


def test_fetch_hf_daily_papers_drafts_fetches_index_and_parses_items(respx_mock: respx.Router) -> None:
    base_url = HfApi().endpoint.rstrip("/")
    index_url = f"{base_url}/papers"
    html = """<html><body>
<a href="/papers/1">Paper One</a>
<a href="/papers/1">Paper One Duplicate</a>
<a href="/papers/2"> Paper Two </a>
<a href="/models/bert-base-uncased">Not a paper</a>
<a href="/papers/3"></a>
</body></html>"""
    route = respx_mock.get(index_url).respond(
        200,
        text=html,
        headers={"Content-Type": "text/html; charset=utf-8"},
    )
    drafts = fetch_hf_daily_papers_drafts(max_items=2)
    assert route.called
    request_headers = {k.lower() for k in route.calls[0].request.headers.keys()}
    assert "user-agent" in request_headers

    assert [d.source_item_id for d in drafts] == ["papers/1", "papers/2"]
    assert [d.canonical_url for d in drafts] == [
        f"{base_url}/papers/1",
        f"{base_url}/papers/2",
    ]
    assert [d.title for d in drafts] == ["Paper One", "Paper Two"]


def test_fetch_hf_daily_papers_drafts_raises_on_http_error(respx_mock: respx.Router) -> None:
    base_url = HfApi().endpoint.rstrip("/")
    index_url = f"{base_url}/papers"
    import httpx

    respx_mock.get(index_url).respond(
        503,
        text="service unavailable",
        headers={"Content-Type": "text/plain; charset=utf-8"},
    )
    with pytest.raises(httpx.HTTPStatusError):
        fetch_hf_daily_papers_drafts(max_items=10)


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
