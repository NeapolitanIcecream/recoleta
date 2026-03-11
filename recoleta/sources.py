from __future__ import annotations

from dataclasses import dataclass, field
from collections.abc import Mapping, Sequence
from datetime import datetime, timedelta, timezone
from typing import Any, Iterator, cast
from urllib.parse import urljoin

import arxiv
from bs4 import BeautifulSoup
import feedparser
import httpx
from huggingface_hub import HfApi
from huggingface_hub.hf_api import PaperInfo
import openreview
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential_jitter,
)

from recoleta.types import ItemDraft


@dataclass(slots=True)
class SourcePullResult:
    drafts: list[ItemDraft] = field(default_factory=list)
    filtered_out_total: int = 0
    in_window_total: int = 0
    missing_published_at_total: int = 0

    def __iter__(self) -> Iterator[ItemDraft]:
        return iter(self.drafts)

    def __len__(self) -> int:
        return len(self.drafts)

    def __getitem__(self, index: int) -> ItemDraft:
        return self.drafts[index]


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


def _normalize_period_bounds(
    *,
    period_start: datetime | None,
    period_end: datetime | None,
) -> tuple[datetime | None, datetime | None]:
    if period_start is None and period_end is None:
        return None, None
    if period_start is None or period_end is None:
        raise ValueError("period_start and period_end must be provided together")
    normalized_start = _normalize_datetime(period_start)
    normalized_end = _normalize_datetime(period_end)
    if normalized_start >= normalized_end:
        raise ValueError("period_start must be before period_end")
    return normalized_start, normalized_end


def _normalize_datetime(value: datetime) -> datetime:
    return (
        value.replace(tzinfo=timezone.utc)
        if value.tzinfo is None
        else value.astimezone(timezone.utc)
    )


def _datetime_in_period(
    *,
    value: datetime | None,
    period_start: datetime | None,
    period_end: datetime | None,
) -> bool:
    if value is None:
        return False
    normalized = _normalize_datetime(value)
    if period_start is not None and normalized < period_start:
        return False
    if period_end is not None and normalized >= period_end:
        return False
    return True


def _iter_period_dates(
    *, period_start: datetime | None, period_end: datetime | None
) -> list[str]:
    if period_start is None or period_end is None:
        return []
    if period_start >= period_end:
        return []
    dates: list[str] = []
    cursor = period_start.date()
    final_date = (period_end - timedelta(microseconds=1)).date()
    while cursor <= final_date:
        dates.append(cursor.isoformat())
        cursor += timedelta(days=1)
    return dates


def _merge_provenance_list(
    mapping: dict[str, Any], *, key: str, value: str | None
) -> None:
    normalized = str(value or "").strip()
    if not normalized:
        return
    existing = mapping.get(key)
    items = list(existing) if isinstance(existing, list) else []
    if normalized not in items:
        items.append(normalized)
    mapping[key] = items


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


def _paper_info_to_draft(
    *, paper: PaperInfo, base_url: str, index_url: str, window_date: str | None = None
) -> ItemDraft | None:
    paper_id = str(getattr(paper, "id", "") or "").strip()
    title = str(getattr(paper, "title", "") or "").strip()
    if not paper_id or not title:
        return None

    authors: list[str] = []
    for author in getattr(paper, "authors", []) or []:
        name = getattr(author, "name", None)
        if isinstance(name, str) and name.strip():
            authors.append(name.strip())

    daily_submitted_at = getattr(paper, "submitted_at", None)
    paper_published_at = getattr(paper, "published_at", None)
    effective_published_at = (
        _normalize_datetime(daily_submitted_at)
        if isinstance(daily_submitted_at, datetime)
        else _normalize_datetime(paper_published_at)
        if isinstance(paper_published_at, datetime)
        else datetime.fromisoformat(f"{window_date}T00:00:00+00:00")
        if window_date is not None
        else None
    )

    raw_metadata: dict[str, Any] = {
        "index_url": index_url,
        "paper_source": str(getattr(paper, "source", "") or "").strip() or None,
        "discussion_id": (
            str(getattr(paper, "discussion_id", "") or "").strip() or None
        ),
    }
    _merge_provenance_list(raw_metadata, key="matched_index_urls", value=index_url)
    if isinstance(paper_published_at, datetime):
        raw_metadata["paper_published_at"] = _normalize_datetime(
            paper_published_at
        ).isoformat()
    if isinstance(daily_submitted_at, datetime):
        raw_metadata["daily_submitted_at"] = _normalize_datetime(
            daily_submitted_at
        ).isoformat()
    elif window_date is not None:
        raw_metadata["daily_submitted_date"] = window_date

    return ItemDraft.from_values(
        source="hf_daily",
        source_item_id=paper_id,
        canonical_url=f"{base_url}/papers/{paper_id}",
        title=title,
        authors=authors,
        published_at=effective_published_at,
        raw_metadata={
            key: value for key, value in raw_metadata.items() if value is not None
        },
    )


def fetch_hf_daily_papers_drafts(
    *,
    max_items: int = 50,
    period_start: datetime | None = None,
    period_end: datetime | None = None,
    include_stats: bool = False,
) -> list[ItemDraft] | SourcePullResult:
    drafts: list[ItemDraft] = []
    if max_items <= 0:
        return SourcePullResult() if include_stats else drafts

    normalized_start, normalized_end = _normalize_period_bounds(
        period_start=period_start,
        period_end=period_end,
    )
    hf_api = HfApi()
    base_url = hf_api.endpoint.rstrip("/")
    seen_ids: set[str] = set()
    stats = SourcePullResult()
    requested_dates = _iter_period_dates(
        period_start=normalized_start,
        period_end=normalized_end,
    )
    requests = requested_dates or [None]

    for requested_date in requests:
        remaining = max_items - len(drafts)
        if remaining <= 0:
            break
        index_url = (
            f"{base_url}/papers/date/{requested_date}"
            if requested_date is not None
            else f"{base_url}/papers"
        )
        papers = hf_api.list_daily_papers(date=requested_date, limit=remaining)
        for paper in papers:
            draft = _paper_info_to_draft(
                paper=paper,
                base_url=base_url,
                index_url=index_url,
                window_date=requested_date,
            )
            if draft is None:
                continue
            source_item_id = str(draft.source_item_id or "").strip()
            if not source_item_id:
                continue
            if source_item_id in seen_ids:
                continue
            seen_ids.add(source_item_id)

            if normalized_start is not None and normalized_end is not None:
                if draft.published_at is None:
                    stats.missing_published_at_total += 1
                    if requested_date is None:
                        continue
                elif not _datetime_in_period(
                    value=draft.published_at,
                    period_start=normalized_start,
                    period_end=normalized_end,
                ):
                    stats.filtered_out_total += 1
                    continue
                else:
                    stats.in_window_total += 1
            drafts.append(draft)
            if len(drafts) >= max_items:
                break

    stats.drafts = drafts
    return stats if include_stats else drafts


def _format_arxiv_datetime(value: datetime) -> str:
    return _normalize_datetime(value).strftime("%Y%m%d%H%M")


def _arxiv_query_with_period(
    *, query: str, period_start: datetime | None, period_end: datetime | None
) -> str:
    normalized_query = query.strip()
    if period_start is None or period_end is None:
        return normalized_query
    inclusive_end = period_end - timedelta(minutes=1)
    if inclusive_end < period_start:
        inclusive_end = period_start
    window_clause = (
        f"submittedDate:[{_format_arxiv_datetime(period_start)} "
        f"TO {_format_arxiv_datetime(inclusive_end)}]"
    )
    return f"({normalized_query}) AND {window_clause}"


def fetch_arxiv_drafts(
    *,
    queries: list[str],
    max_results_per_run: int = 50,
    period_start: datetime | None = None,
    period_end: datetime | None = None,
    include_stats: bool = False,
) -> list[ItemDraft] | SourcePullResult:
    if max_results_per_run <= 0:
        return SourcePullResult() if include_stats else []

    normalized_start, normalized_end = _normalize_period_bounds(
        period_start=period_start,
        period_end=period_end,
    )
    client = arxiv.Client()
    drafts: list[ItemDraft] = []
    seen_entry_ids: set[str] = set()
    stats = SourcePullResult()
    for query in (q.strip() for q in queries):
        if not query:
            continue
        search = arxiv.Search(
            query=_arxiv_query_with_period(
                query=query,
                period_start=normalized_start,
                period_end=normalized_end,
            ),
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
            if normalized_start is not None and normalized_end is not None:
                if not isinstance(published_at, datetime):
                    stats.missing_published_at_total += 1
                    continue
                if not _datetime_in_period(
                    value=published_at,
                    period_start=normalized_start,
                    period_end=normalized_end,
                ):
                    stats.filtered_out_total += 1
                    continue
                stats.in_window_total += 1

            source_item_id: str | None = None
            get_short_id = getattr(result, "get_short_id", None)
            if callable(get_short_id):
                try:
                    source_item_id = str(get_short_id())
                except Exception:
                    source_item_id = None
            source_item_id = _first_non_empty_str(source_item_id, entry_id)

            raw_metadata: dict[str, Any] = {"query": query, "matched_queries": [query]}
            categories = getattr(result, "categories", None)
            if isinstance(categories, list) and categories:
                raw_metadata["categories"] = [str(cat) for cat in categories]
            comment = getattr(result, "comment", None)
            if isinstance(comment, str) and comment.strip():
                raw_metadata["comment"] = comment.strip()
            if normalized_start is not None and normalized_end is not None:
                raw_metadata["query_period_start"] = normalized_start.isoformat()
                raw_metadata["query_period_end"] = normalized_end.isoformat()

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
    stats.drafts = drafts
    return stats if include_stats else drafts


def fetch_openreview_drafts(
    *,
    venues: list[str],
    max_results_per_venue: int = 50,
    period_start: datetime | None = None,
    period_end: datetime | None = None,
    include_stats: bool = False,
) -> list[ItemDraft] | SourcePullResult:
    drafts: list[ItemDraft] = []
    if max_results_per_venue <= 0:
        return SourcePullResult() if include_stats else drafts

    normalized_start, normalized_end = _normalize_period_bounds(
        period_start=period_start,
        period_end=period_end,
    )
    client = openreview.Client(baseurl="https://api.openreview.net")
    seen_note_ids: set[str] = set()
    stats = SourcePullResult()
    for venue in (v.strip() for v in venues):
        if not venue:
            continue
        invitation = venue if "/-/" in venue else f"{venue}/-/Blind_Submission"
        page_size = max(1, min(max_results_per_venue, 100))
        offset = 0
        venue_collected = 0
        while venue_collected < max_results_per_venue:
            kwargs: dict[str, Any] = {
                "invitation": invitation,
                "limit": page_size,
                "offset": offset,
            }
            if normalized_start is not None:
                kwargs["mintcdate"] = int(normalized_start.timestamp() * 1000)
            try:
                notes = client.get_notes(**kwargs, sort="tcdate:desc")
            except Exception:
                notes = client.get_notes(**kwargs)
            if not notes:
                break

            for note in notes:
                if venue_collected >= max_results_per_venue:
                    break
                note_id = str(getattr(note, "id", "") or "").strip()
                if not note_id or note_id in seen_note_ids:
                    continue
                seen_note_ids.add(note_id)

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
                        str(author).strip()
                        for author in raw_authors
                        if str(author).strip()
                    ]

                tcdate = getattr(note, "tcdate", None)
                published_at: datetime | None = None
                if isinstance(tcdate, int):
                    published_at = datetime.fromtimestamp(
                        tcdate / 1000, tz=timezone.utc
                    )

                if normalized_start is not None and normalized_end is not None:
                    if published_at is None:
                        stats.missing_published_at_total += 1
                        continue
                    if not _datetime_in_period(
                        value=published_at,
                        period_start=normalized_start,
                        period_end=normalized_end,
                    ):
                        stats.filtered_out_total += 1
                        continue
                    stats.in_window_total += 1

                canonical_url = f"https://openreview.net/forum?id={note_id}"
                drafts.append(
                    ItemDraft.from_values(
                        source="openreview",
                        source_item_id=note_id,
                        canonical_url=canonical_url,
                        title=title,
                        authors=authors,
                        published_at=published_at,
                        raw_metadata={
                            "invitation": invitation,
                            "venue": venue,
                            "matched_venues": [venue],
                            "matched_invitations": [invitation],
                        },
                    )
                )
                venue_collected += 1

            if len(notes) < page_size:
                break
            offset += len(notes)

    stats.drafts = drafts
    return stats if include_stats else drafts


def fetch_rss_drafts(
    *,
    feed_urls: list[str],
    source: str = "rss",
    max_items_per_feed: int = 50,
    period_start: datetime | None = None,
    period_end: datetime | None = None,
    include_stats: bool = False,
) -> list[ItemDraft] | SourcePullResult:
    drafts: list[ItemDraft] = []
    normalized_start, normalized_end = _normalize_period_bounds(
        period_start=period_start,
        period_end=period_end,
    )
    timeout = httpx.Timeout(10.0, connect=5.0)
    headers = {"User-Agent": "recoleta/0.1"}
    resolved_feed_urls: set[str] = set()
    stats = SourcePullResult()
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
            filtered_entries = (
                entries
                if normalized_start is not None and normalized_end is not None
                else entries[:max_items_per_feed]
            )
            kept_for_feed = 0
            for entry in filtered_entries:
                if kept_for_feed >= max_items_per_feed:
                    break
                link = _get_str(entry, "link")
                title = _get_str(entry, "title")
                if not link or not title:
                    continue
                published_at = _parse_entry_datetime(entry)
                if normalized_start is not None and normalized_end is not None:
                    if published_at is None:
                        stats.missing_published_at_total += 1
                        continue
                    if not _datetime_in_period(
                        value=published_at,
                        period_start=normalized_start,
                        period_end=normalized_end,
                    ):
                        stats.filtered_out_total += 1
                        continue
                    stats.in_window_total += 1
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
                        published_at=published_at,
                        raw_metadata={
                            "feed_url": resolved_feed_url,
                            "feed_title": feed_title,
                            "matched_feed_urls": [resolved_feed_url],
                            **(
                                {"feed_discovered_from": discovered_from}
                                if discovered_from is not None
                                else {}
                            ),
                        },
                    )
                )
                kept_for_feed += 1
    stats.drafts = drafts
    return stats if include_stats else drafts
