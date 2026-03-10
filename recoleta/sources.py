from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime, timezone
from typing import Any, cast
from urllib.parse import urljoin

import arxiv
from bs4 import BeautifulSoup
import feedparser
import httpx
from huggingface_hub import HfApi
import openreview
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential_jitter,
)

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


def _discover_feed_url_from_html(*, page_url: str, html: str) -> str | None:
    soup = BeautifulSoup(html, "html.parser")
    search_root = soup.head if soup.head is not None else soup
    candidates: list[tuple[int, str]] = []
    for link in search_root.find_all("link"):
        href = str(link.get("href") or "").strip()
        if not href:
            continue
        rel_value = link.get("rel")
        rel_tokens = (
            [str(token).strip().lower() for token in rel_value]
            if isinstance(rel_value, list)
            else [str(rel_value).strip().lower()]
            if rel_value is not None
            else []
        )
        if "alternate" not in rel_tokens:
            continue
        type_value = str(link.get("type") or "").strip().lower()
        if "rss" in type_value:
            priority = 0
        elif "atom" in type_value:
            priority = 1
        elif "xml" in type_value:
            priority = 2
        else:
            continue
        title_value = str(link.get("title") or "").strip().lower()
        href_value = str(href).strip().lower()
        if "comment" in title_value or "comment" in href_value:
            priority += 10
        candidates.append((priority, urljoin(page_url, href)))
    if not candidates:
        return None
    candidates.sort(key=lambda entry: (entry[0], entry[1]))
    return candidates[0][1]


def _normalize_hf_paper_href(href: str | None) -> str | None:
    raw_href = str(href or "").strip()
    if not raw_href.startswith("/papers/"):
        return None
    normalized = raw_href.split("#", 1)[0].strip()
    if not normalized or normalized in {"/papers", "/papers/"}:
        return None
    if normalized.startswith("/papers/date/") or normalized == "/papers/trending":
        return None
    parts = [part for part in normalized.split("/") if part]
    if len(parts) != 2:
        return None
    return normalized


def _iter_hf_paper_title_candidates(soup: BeautifulSoup) -> list[tuple[str, str]]:
    candidates: list[tuple[str, str]] = []
    for article in soup.find_all("article"):
        heading_anchors = article.select(
            "h1 a[href^='/papers/'], h2 a[href^='/papers/'], h3 a[href^='/papers/'], h4 a[href^='/papers/']"
        )
        anchor_iterable = heading_anchors or article.select("a[href^='/papers/']")
        for anchor in anchor_iterable:
            href_value = anchor.get("href")
            normalized_href = _normalize_hf_paper_href(
                href_value if isinstance(href_value, str) else None
            )
            if normalized_href is None:
                continue
            title = anchor.get_text(" ", strip=True)
            if not title or title.isdigit():
                continue
            candidates.append((normalized_href, title))
            break
    return candidates


def fetch_hf_daily_papers_drafts(*, max_items: int = 50) -> list[ItemDraft]:
    drafts: list[ItemDraft] = []
    if max_items <= 0:
        return drafts

    hf_api = HfApi()
    base_url = hf_api.endpoint.rstrip("/")
    index_url = f"{base_url}/papers"
    timeout = httpx.Timeout(10.0, connect=5.0)
    headers = {"User-Agent": "recoleta/0.1"}
    with httpx.Client(
        timeout=timeout, headers=headers, follow_redirects=True
    ) as client:
        html = _fetch_feed_text(client, index_url)
    soup = BeautifulSoup(html, "html.parser")
    seen: set[str] = set()
    candidates = _iter_hf_paper_title_candidates(soup)
    if not candidates:
        for anchor in soup.select('a[href^="/papers/"]'):
            href_value = anchor.get("href")
            normalized_href = _normalize_hf_paper_href(
                href_value if isinstance(href_value, str) else None
            )
            if normalized_href is None:
                continue
            title = anchor.get_text(" ", strip=True)
            if not title or title.isdigit():
                continue
            candidates.append((normalized_href, title))

    for normalized_href, title in candidates:
        if normalized_href in seen:
            continue
        seen.add(normalized_href)

        canonical_url = f"{base_url}{normalized_href}"
        drafts.append(
            ItemDraft.from_values(
                source="hf_daily",
                source_item_id=normalized_href.lstrip("/"),
                canonical_url=canonical_url,
                title=title,
                authors=[],
                published_at=None,
                raw_metadata={"index_url": index_url},
            )
        )
        if len(drafts) >= max_items:
            break
    return drafts


def fetch_arxiv_drafts(
    *, queries: list[str], max_results_per_run: int = 50
) -> list[ItemDraft]:
    if max_results_per_run <= 0:
        return []

    client = arxiv.Client()
    drafts: list[ItemDraft] = []
    seen_entry_ids: set[str] = set()
    for query in (q.strip() for q in queries):
        if not query:
            continue
        search = arxiv.Search(
            query=query,
            max_results=max_results_per_run,
            sort_by=arxiv.SortCriterion.SubmittedDate,
        )
        for result in client.results(search):
            entry_id = str(getattr(result, "entry_id", "") or "").strip()
            if not entry_id or entry_id in seen_entry_ids:
                continue
            seen_entry_ids.add(entry_id)

            title = str(getattr(result, "title", "") or "").strip()
            if not title:
                continue

            authors: list[str] = []
            for author in getattr(result, "authors", []) or []:
                name = getattr(author, "name", None)
                if isinstance(name, str) and name.strip():
                    authors.append(name.strip())

            published_at = getattr(result, "published", None)
            if (
                published_at is not None
                and isinstance(published_at, datetime)
                and published_at.tzinfo is None
            ):
                published_at = published_at.replace(tzinfo=timezone.utc)

            source_item_id: str | None = None
            get_short_id = getattr(result, "get_short_id", None)
            if callable(get_short_id):
                try:
                    source_item_id = str(get_short_id())
                except Exception:
                    source_item_id = None
            source_item_id = _first_non_empty_str(source_item_id, entry_id)

            raw_metadata: dict[str, Any] = {"query": query}
            categories = getattr(result, "categories", None)
            if isinstance(categories, list) and categories:
                raw_metadata["categories"] = [str(cat) for cat in categories]
            comment = getattr(result, "comment", None)
            if isinstance(comment, str) and comment.strip():
                raw_metadata["comment"] = comment.strip()

            drafts.append(
                ItemDraft.from_values(
                    source="arxiv",
                    source_item_id=source_item_id,
                    canonical_url=entry_id,
                    title=title,
                    authors=authors,
                    published_at=published_at
                    if isinstance(published_at, datetime)
                    else None,
                    raw_metadata=raw_metadata,
                )
            )
    return drafts


def fetch_openreview_drafts(
    *, venues: list[str], max_results_per_venue: int = 50
) -> list[ItemDraft]:
    drafts: list[ItemDraft] = []
    if max_results_per_venue <= 0:
        return drafts

    client = openreview.Client(baseurl="https://api.openreview.net")
    for venue in (v.strip() for v in venues):
        if not venue:
            continue
        invitation = venue if "/-/" in venue else f"{venue}/-/Blind_Submission"
        try:
            notes = client.get_notes(
                invitation=invitation, limit=max_results_per_venue, sort="tcdate:desc"
            )
        except Exception:
            notes = client.get_notes(invitation=invitation, limit=max_results_per_venue)

        for note in notes:
            note_id = str(getattr(note, "id", "") or "").strip()
            if not note_id:
                continue

            content = getattr(note, "content", None) or {}
            title_value = None
            if isinstance(content, Mapping):
                title_value = content.get("title")
            title: str = ""
            if isinstance(title_value, Mapping):
                raw_title = title_value.get("value")
                title = str(raw_title or "").strip()
            else:
                title = str(title_value or "").strip()
            if not title:
                continue

            authors: list[str] = []
            authors_value = (
                content.get("authors") if isinstance(content, Mapping) else None
            )
            if isinstance(authors_value, Mapping):
                raw_authors = authors_value.get("value")
            else:
                raw_authors = authors_value
            if isinstance(raw_authors, list):
                authors = [
                    str(author).strip() for author in raw_authors if str(author).strip()
                ]

            tcdate = getattr(note, "tcdate", None)
            published_at: datetime | None = None
            if isinstance(tcdate, int):
                published_at = datetime.fromtimestamp(tcdate / 1000, tz=timezone.utc)

            canonical_url = f"https://openreview.net/forum?id={note_id}"
            drafts.append(
                ItemDraft.from_values(
                    source="openreview",
                    source_item_id=note_id,
                    canonical_url=canonical_url,
                    title=title,
                    authors=authors,
                    published_at=published_at,
                    raw_metadata={"invitation": invitation},
                )
            )
    return drafts


def fetch_rss_drafts(
    *,
    feed_urls: list[str],
    source: str = "rss",
    max_items_per_feed: int = 50,
) -> list[ItemDraft]:
    drafts: list[ItemDraft] = []
    timeout = httpx.Timeout(10.0, connect=5.0)
    headers = {"User-Agent": "recoleta/0.1"}
    resolved_feed_urls: set[str] = set()
    with httpx.Client(
        timeout=timeout, headers=headers, follow_redirects=True
    ) as client:
        for feed_url in feed_urls:
            resolved_feed_url = feed_url
            discovered_from: str | None = None
            feed_text = _fetch_feed_text(client, resolved_feed_url)
            parsed = cast(Any, feedparser.parse(feed_text))
            parsed_version = str(getattr(parsed, "version", "") or "").strip()
            entries = cast(
                list[Mapping[str, Any]], getattr(parsed, "entries", []) or []
            )
            if not entries and not parsed_version:
                discovered = _discover_feed_url_from_html(
                    page_url=resolved_feed_url,
                    html=feed_text,
                )
                if discovered and discovered != resolved_feed_url:
                    resolved_feed_url = discovered
                    discovered_from = feed_url
                    feed_text = _fetch_feed_text(client, resolved_feed_url)
                    parsed = cast(Any, feedparser.parse(feed_text))
                    entries = cast(
                        list[Mapping[str, Any]], getattr(parsed, "entries", []) or []
                    )
            if resolved_feed_url in resolved_feed_urls:
                continue
            resolved_feed_urls.add(resolved_feed_url)
            feed = cast(Mapping[str, Any], getattr(parsed, "feed", {}) or {})
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
                source_item_id = _first_non_empty_str(
                    entry.get("id"), entry.get("guid"), link
                )
                drafts.append(
                    ItemDraft.from_values(
                        source=source,
                        source_item_id=source_item_id,
                        canonical_url=link,
                        title=title,
                        authors=authors,
                        published_at=_parse_entry_datetime(entry),
                        raw_metadata={
                            "feed_url": resolved_feed_url,
                            "feed_title": feed_title,
                            **(
                                {"feed_discovered_from": discovered_from}
                                if discovered_from is not None
                                else {}
                            ),
                        },
                    )
                )
    return drafts
