from __future__ import annotations

from datetime import datetime, timezone

import feedparser

from recoleta.types import ItemDraft


def _parse_entry_datetime(entry: dict) -> datetime | None:
    parsed = entry.get("published_parsed") or entry.get("updated_parsed")
    if parsed is None:
        return None
    return datetime(*parsed[:6], tzinfo=timezone.utc)


def fetch_rss_drafts(
    *,
    feed_urls: list[str],
    source: str = "rss",
    max_items_per_feed: int = 50,
) -> list[ItemDraft]:
    drafts: list[ItemDraft] = []
    for feed_url in feed_urls:
        parsed = feedparser.parse(feed_url)
        feed_title = parsed.feed.get("title", "")
        for entry in parsed.entries[:max_items_per_feed]:
            link = (entry.get("link") or "").strip()
            title = (entry.get("title") or "").strip()
            if not link or not title:
                continue
            authors = [author.get("name", "").strip() for author in entry.get("authors", [])]
            if not authors:
                single_author = (entry.get("author") or "").strip()
                if single_author:
                    authors = [single_author]
            authors = [author for author in authors if author]
            drafts.append(
                ItemDraft.from_values(
                    source=source,
                    source_item_id=entry.get("id") or entry.get("guid") or link,
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
