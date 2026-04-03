from __future__ import annotations

from dataclasses import dataclass, field
from collections.abc import Callable, Mapping, Sequence
from datetime import datetime, timedelta, timezone
from typing import Any, Iterator, TypedDict, Unpack

import arxiv  # noqa: F401
import httpx
from huggingface_hub.hf_api import PaperInfo
import openreview  # noqa: F401
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential_jitter,
)

from recoleta.types import ItemDraft


@dataclass(slots=True, frozen=True)
class SourcePullStateSnapshot:
    scope_kind: str
    scope_key: str
    etag: str | None = None
    last_modified: str | None = None
    watermark_published_at: datetime | None = None
    cursor: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class SourcePullStateUpdate:
    scope_kind: str
    scope_key: str
    etag: str | None = None
    last_modified: str | None = None
    watermark_published_at: datetime | None = None
    cursor: dict[str, Any] = field(default_factory=dict)


PullStateLookup = Callable[[str, str], SourcePullStateSnapshot | None]


@dataclass(slots=True)
class SourcePullResult:
    drafts: list[ItemDraft] = field(default_factory=list)
    filtered_out_total: int = 0
    in_window_total: int = 0
    missing_published_at_total: int = 0
    deduped_total: int = 0
    deferred_total: int = 0
    not_modified_total: int = 0
    oldest_published_at: datetime | None = None
    newest_published_at: datetime | None = None
    state_updates: list[SourcePullStateUpdate] = field(default_factory=list)

    def __iter__(self) -> Iterator[ItemDraft]:
        return iter(self.drafts)

    def __len__(self) -> int:
        return len(self.drafts)

    def __getitem__(self, index: int) -> ItemDraft:
        return self.drafts[index]


@dataclass(slots=True, frozen=True)
class HFDailyPapersPullRequest:
    max_items: int = 50
    period_start: datetime | None = None
    period_end: datetime | None = None
    pull_state_lookup: PullStateLookup | None = None
    include_stats: bool = False


@dataclass(slots=True, frozen=True)
class ArxivPullRequest:
    queries: list[str]
    max_results_per_run: int = 50
    period_start: datetime | None = None
    period_end: datetime | None = None
    max_total_items: int | None = None
    pull_state_lookup: PullStateLookup | None = None
    include_stats: bool = False


@dataclass(slots=True, frozen=True)
class OpenReviewPullRequest:
    venues: list[str]
    max_results_per_venue: int = 50
    period_start: datetime | None = None
    period_end: datetime | None = None
    max_total_items: int | None = None
    pull_state_lookup: PullStateLookup | None = None
    include_stats: bool = False


@dataclass(slots=True, frozen=True)
class FeedPullRequest:
    feed_urls: list[str]
    source: str = "rss"
    max_items_per_feed: int = 50
    period_start: datetime | None = None
    period_end: datetime | None = None
    max_total_items: int | None = None
    pull_state_lookup: PullStateLookup | None = None
    include_stats: bool = False


@dataclass(slots=True, frozen=True)
class HNPullRequest:
    feed_urls: list[str]
    max_items_per_feed: int = 50
    period_start: datetime | None = None
    period_end: datetime | None = None
    max_total_items: int | None = None
    pull_state_lookup: PullStateLookup | None = None
    include_stats: bool = False


class _HFDailyPapersPullRequestKwargs(TypedDict, total=False):
    max_items: int
    period_start: datetime | None
    period_end: datetime | None
    pull_state_lookup: PullStateLookup | None
    include_stats: bool


class _ArxivPullRequestKwargs(TypedDict, total=False):
    queries: list[str]
    max_results_per_run: int
    period_start: datetime | None
    period_end: datetime | None
    max_total_items: int | None
    pull_state_lookup: PullStateLookup | None
    include_stats: bool


class _OpenReviewPullRequestKwargs(TypedDict, total=False):
    venues: list[str]
    max_results_per_venue: int
    period_start: datetime | None
    period_end: datetime | None
    max_total_items: int | None
    pull_state_lookup: PullStateLookup | None
    include_stats: bool


class _FeedPullRequestKwargs(TypedDict, total=False):
    feed_urls: list[str]
    source: str
    max_items_per_feed: int
    period_start: datetime | None
    period_end: datetime | None
    max_total_items: int | None
    pull_state_lookup: PullStateLookup | None
    include_stats: bool


class _HNPullRequestKwargs(TypedDict, total=False):
    feed_urls: list[str]
    max_items_per_feed: int
    period_start: datetime | None
    period_end: datetime | None
    max_total_items: int | None
    pull_state_lookup: PullStateLookup | None
    include_stats: bool


def _should_retry_httpx(exc: BaseException) -> bool:
    if isinstance(exc, httpx.RequestError):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        status = exc.response.status_code
        return status >= 500 or status == 429
    return False


def _source_pull_now() -> datetime:
    return datetime.now(timezone.utc)


@retry(
    retry=retry_if_exception(_should_retry_httpx),
    stop=stop_after_attempt(3),
    wait=wait_exponential_jitter(initial=0.5, max=6.0),
    reraise=True,
)
def _fetch_feed_response(
    client: httpx.Client,
    url: str,
    *,
    etag: str | None = None,
    last_modified: str | None = None,
) -> httpx.Response:
    headers: dict[str, str] = {}
    normalized_etag = str(etag or "").strip()
    normalized_last_modified = str(last_modified or "").strip()
    if normalized_etag:
        headers["If-None-Match"] = normalized_etag
    if normalized_last_modified:
        headers["If-Modified-Since"] = normalized_last_modified
    response = client.get(url, headers=headers or None)
    if response.status_code == 304:
        return response
    response.raise_for_status()
    return response


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


def _record_stats_published_at(stats: SourcePullResult, value: datetime | None) -> None:
    if value is None:
        return
    normalized = _normalize_datetime(value)
    if stats.oldest_published_at is None or normalized < stats.oldest_published_at:
        stats.oldest_published_at = normalized
    if stats.newest_published_at is None or normalized > stats.newest_published_at:
        stats.newest_published_at = normalized


def _watermark_after_snapshot(
    snapshot: SourcePullStateSnapshot | None, candidate: datetime | None
) -> datetime | None:
    existing = (
        _normalize_datetime(snapshot.watermark_published_at)
        if snapshot is not None
        and isinstance(snapshot.watermark_published_at, datetime)
        else None
    )
    if candidate is None:
        return existing
    normalized_candidate = _normalize_datetime(candidate)
    if existing is None or normalized_candidate > existing:
        return normalized_candidate
    return existing


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
    from recoleta.source_pullers import discover_feed_url_from_html

    return discover_feed_url_from_html(page_url=page_url, html=html)


def _paper_info_to_draft(
    *, paper: PaperInfo, base_url: str, index_url: str, window_date: str | None = None
) -> ItemDraft | None:
    from recoleta.source_pullers import paper_info_to_draft

    return paper_info_to_draft(
        paper=paper,
        base_url=base_url,
        index_url=index_url,
        window_date=window_date,
    )


def fetch_hf_daily_papers_drafts(
    *,
    request: HFDailyPapersPullRequest | None = None,
    **legacy_kwargs: Unpack[_HFDailyPapersPullRequestKwargs],
) -> list[ItemDraft] | SourcePullResult:
    normalized_request = request or HFDailyPapersPullRequest(**legacy_kwargs)
    from recoleta.source_pullers import pull_hf_daily_papers

    return pull_hf_daily_papers(normalized_request)


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
    request: ArxivPullRequest | None = None,
    **legacy_kwargs: Unpack[_ArxivPullRequestKwargs],
) -> list[ItemDraft] | SourcePullResult:
    normalized_request = request or ArxivPullRequest(**legacy_kwargs)
    from recoleta.source_pullers import pull_arxiv_drafts

    return pull_arxiv_drafts(normalized_request)


def fetch_openreview_drafts(
    *,
    request: OpenReviewPullRequest | None = None,
    **legacy_kwargs: Unpack[_OpenReviewPullRequestKwargs],
) -> list[ItemDraft] | SourcePullResult:
    normalized_request = request or OpenReviewPullRequest(**legacy_kwargs)
    from recoleta.source_pullers import pull_openreview_drafts

    return pull_openreview_drafts(normalized_request)


def fetch_rss_drafts(
    *,
    request: FeedPullRequest | None = None,
    **legacy_kwargs: Unpack[_FeedPullRequestKwargs],
) -> list[ItemDraft] | SourcePullResult:
    normalized_request = request or FeedPullRequest(**legacy_kwargs)
    from recoleta.source_pullers import pull_rss_drafts

    return pull_rss_drafts(normalized_request)


def fetch_hn_drafts(
    *,
    request: HNPullRequest | None = None,
    **legacy_kwargs: Unpack[_HNPullRequestKwargs],
) -> list[ItemDraft] | SourcePullResult:
    normalized_request = request or HNPullRequest(**legacy_kwargs)
    from recoleta.source_pullers import pull_hn_drafts

    return pull_hn_drafts(normalized_request)
