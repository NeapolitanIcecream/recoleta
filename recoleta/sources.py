from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime, timezone
from typing import Any, cast

import feedparser
import httpx
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential_jitter

from recoleta.types import ItemDraft


def _should_retry_httpx(exc: BaseException) -> bool:
    if isinstance(exc, httpx.RequestError):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        status = exc.response.status_code
        return status >= 500 or status == 429
    return False


@retry(
    retry=retry_if_exception(_should_retry_httpx),
    stop=stop_after_attempt(3),
    wait=wait_exponential_jitter(initial=0.5, max=6.0),
    reraise=True,
)
def _fetch_feed_text(client: httpx.Client, url: str) -> str:
    response = client.get(url)
    response.raise_for_status()
    return response.text


def _parse_entry_datetime(entry: Mapping[str, Any]) -> datetime | None:
    parsed = entry.get("published_parsed") or entry.get("updated_parsed")
    if parsed is None:
        return None
    if not isinstance(parsed, Sequence) or len(parsed) < 6:
        return None
    try:
        year, month, day, hour, minute, second = (int(parsed[i]) for i in range(6))
    except Exception:
        return None
    return datetime(year, month, day, hour, minute, second, tzinfo=timezone.utc)


def _get_str(mapping: Mapping[str, Any], key: str) -> str:
    value = mapping.get(key)
    return value.strip() if isinstance(value, str) else ""


def _first_non_empty_str(*values: object) -> str | None:
    for value in values:
        if isinstance(value, str):
            candidate = value.strip()
            if candidate:
                return candidate
    return None


def fetch_rss_drafts(
    *,
    feed_urls: list[str],
    source: str = "rss",
    max_items_per_feed: int = 50,
) -> list[ItemDraft]:
    drafts: list[ItemDraft] = []
    timeout = httpx.Timeout(10.0, connect=5.0)
    headers = {"User-Agent": "recoleta/0.1"}
    with httpx.Client(timeout=timeout, headers=headers, follow_redirects=True) as client:
        for feed_url in feed_urls:
            feed_text = _fetch_feed_text(client, feed_url)
            parsed = cast(Any, feedparser.parse(feed_text))
            feed = cast(Mapping[str, Any], getattr(parsed, "feed", {}) or {})
            entries = cast(list[Mapping[str, Any]], getattr(parsed, "entries", []) or [])
            feed_title = _get_str(feed, "title")
            for entry in entries[:max_items_per_feed]:
                link = _get_str(entry, "link")
                title = _get_str(entry, "title")
                if not link or not title:
                    continue
                authors: list[str] = []
                raw_authors = entry.get("authors")
                if isinstance(raw_authors, list):
                    for author in raw_authors:
                        if isinstance(author, Mapping):
                            name = author.get("name")
                            if isinstance(name, str):
                                stripped = name.strip()
                                if stripped:
                                    authors.append(stripped)
                if not authors:
                    single_author = _get_str(entry, "author")
                    if single_author:
                        authors = [single_author]
                source_item_id = _first_non_empty_str(entry.get("id"), entry.get("guid"), link)
                drafts.append(
                    ItemDraft.from_values(
                        source=source,
                        source_item_id=source_item_id,
                        canonical_url=link,
                        title=title,
                        authors=authors,
                        published_at=_parse_entry_datetime(entry),
                        raw_metadata={
                            "feed_url": feed_url,
                            "feed_title": feed_title,
                        },
                    )
                )
    return drafts
