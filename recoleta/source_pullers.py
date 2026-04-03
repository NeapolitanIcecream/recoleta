from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, cast
from urllib.parse import urljoin

import arxiv
from bs4 import BeautifulSoup
import feedparser
import httpx
from huggingface_hub import HfApi
from huggingface_hub.hf_api import PaperInfo
import openreview

from recoleta.sources import (
    ArxivPullRequest,
    FeedPullRequest,
    HFDailyPapersPullRequest,
    HNPullRequest,
    OpenReviewPullRequest,
    PullStateLookup,
    SourcePullResult,
    SourcePullStateSnapshot,
    SourcePullStateUpdate,
    _arxiv_query_with_period,
    _discover_feed_url_from_html,
    _datetime_in_period,
    _fetch_feed_response,
    _first_non_empty_str,
    _get_str,
    _iter_period_dates,
    _merge_provenance_list,
    _normalize_datetime,
    _normalize_period_bounds,
    _parse_entry_datetime,
    _paper_info_to_draft,
    _record_stats_published_at,
    _source_pull_now,
    _watermark_after_snapshot,
)
from recoleta.types import ItemDraft


@dataclass(slots=True, frozen=True)
class _FeedLinkCandidate:
    priority: int
    url: str


@dataclass(slots=True, frozen=True)
class _HFDailyWindow:
    period_start: datetime | None
    period_end: datetime | None
    watermark: datetime | None


@dataclass(slots=True, frozen=True)
class _ArxivQueryState:
    query: str
    snapshot: SourcePullStateSnapshot | None
    watermark: datetime | None
    period_start: datetime | None
    period_end: datetime | None


@dataclass(slots=True, frozen=True)
class _OpenReviewVenueState:
    venue: str
    invitation: str
    snapshot: SourcePullStateSnapshot | None
    watermark: datetime | None
    period_start: datetime | None
    period_end: datetime | None


@dataclass(slots=True, frozen=True)
class _FeedState:
    feed_url: str
    snapshot: SourcePullStateSnapshot | None
    watermark: datetime | None
    resolved_feed_url: str
    discovered_from: str | None


def discover_feed_url_from_html(*, page_url: str, html: str) -> str | None:
    candidates = sorted(
        _iter_feed_link_candidates(page_url=page_url, html=html),
        key=lambda item: (item.priority, item.url),
    )
    if not candidates:
        return None
    return candidates[0].url


def _iter_feed_link_candidates(*, page_url: str, html: str) -> list[_FeedLinkCandidate]:
    soup = BeautifulSoup(html, "html.parser")
    search_root = soup.head if soup.head is not None else soup
    candidates: list[_FeedLinkCandidate] = []
    for link in search_root.find_all("link"):
        candidate = _feed_link_candidate(page_url=page_url, link=link)
        if candidate is not None:
            candidates.append(candidate)
    return candidates


def _feed_link_candidate(*, page_url: str, link: Any) -> _FeedLinkCandidate | None:
    href = str(link.get("href") or "").strip()
    if not href:
        return None
    if "alternate" not in _feed_rel_tokens(link.get("rel")):
        return None
    priority = _feed_link_priority(link=link, href=href)
    if priority is None:
        return None
    return _FeedLinkCandidate(priority=priority, url=urljoin(page_url, href))


def _feed_rel_tokens(rel_value: Any) -> list[str]:
    if isinstance(rel_value, list):
        return [str(token).strip().lower() for token in rel_value]
    if rel_value is None:
        return []
    return [str(rel_value).strip().lower()]


def _feed_link_priority(*, link: Any, href: str) -> int | None:
    type_value = str(link.get("type") or "").strip().lower()
    if "rss" in type_value:
        priority = 0
    elif "atom" in type_value:
        priority = 1
    elif "xml" in type_value:
        priority = 2
    else:
        return None
    title_value = str(link.get("title") or "").strip().lower()
    href_value = str(href).strip().lower()
    if "comment" in title_value or "comment" in href_value:
        priority += 10
    return priority


def paper_info_to_draft(
    *, paper: PaperInfo, base_url: str, index_url: str, window_date: str | None = None
) -> ItemDraft | None:
    identity = _paper_identity(paper)
    if identity is None:
        return None
    paper_id, title = identity
    return ItemDraft.from_values(
        source="hf_daily",
        source_item_id=paper_id,
        canonical_url=f"{base_url}/papers/{paper_id}",
        title=title,
        authors=_paper_authors(paper),
        published_at=_paper_effective_published_at(paper=paper, window_date=window_date),
        raw_metadata=_paper_raw_metadata(
            paper=paper,
            index_url=index_url,
            window_date=window_date,
        ),
    )


def _paper_identity(paper: PaperInfo) -> tuple[str, str] | None:
    paper_id = str(getattr(paper, "id", "") or "").strip()
    title = str(getattr(paper, "title", "") or "").strip()
    if not paper_id or not title:
        return None
    return paper_id, title


def _paper_authors(paper: PaperInfo) -> list[str]:
    authors: list[str] = []
    for author in getattr(paper, "authors", []) or []:
        name = getattr(author, "name", None)
        if isinstance(name, str) and name.strip():
            authors.append(name.strip())
    return authors


def _paper_effective_published_at(
    *, paper: PaperInfo, window_date: str | None
) -> datetime | None:
    daily_submitted_at = getattr(paper, "submitted_at", None)
    if isinstance(daily_submitted_at, datetime):
        return _normalize_datetime(daily_submitted_at)
    paper_published_at = getattr(paper, "published_at", None)
    if isinstance(paper_published_at, datetime):
        return _normalize_datetime(paper_published_at)
    if window_date is None:
        return None
    return datetime.fromisoformat(f"{window_date}T00:00:00+00:00")


def _paper_raw_metadata(
    *, paper: PaperInfo, index_url: str, window_date: str | None
) -> dict[str, Any]:
    raw_metadata: dict[str, Any] = {
        "index_url": index_url,
        "paper_source": str(getattr(paper, "source", "") or "").strip() or None,
        "discussion_id": str(getattr(paper, "discussion_id", "") or "").strip() or None,
    }
    _merge_provenance_list(raw_metadata, key="matched_index_urls", value=index_url)
    paper_published_at = getattr(paper, "published_at", None)
    if isinstance(paper_published_at, datetime):
        raw_metadata["paper_published_at"] = _normalize_datetime(
            paper_published_at
        ).isoformat()
    daily_submitted_at = getattr(paper, "submitted_at", None)
    if isinstance(daily_submitted_at, datetime):
        raw_metadata["daily_submitted_at"] = _normalize_datetime(
            daily_submitted_at
        ).isoformat()
    elif window_date is not None:
        raw_metadata["daily_submitted_date"] = window_date
    return {key: value for key, value in raw_metadata.items() if value is not None}


def pull_hf_daily_papers(
    request: HFDailyPapersPullRequest,
) -> list[ItemDraft] | SourcePullResult:
    return _HFDailyPuller(request).pull()


class _HFDailyPuller:
    def __init__(self, request: HFDailyPapersPullRequest) -> None:
        self.request = request
        self.stats = SourcePullResult()
        self.drafts: list[ItemDraft] = []
        self.hf_api = HfApi()
        self.base_url = self.hf_api.endpoint.rstrip("/")
        self.seen_ids: set[str] = set()
        self.snapshot = self._lookup_snapshot()
        self.window = self._window_from_request()

    def pull(self) -> list[ItemDraft] | SourcePullResult:
        if self.request.max_items <= 0:
            return self._result()
        for requested_date in self._requested_dates():
            self._pull_date(requested_date)
            if len(self.drafts) >= self.request.max_items:
                break
        self.stats.drafts = self.drafts
        self.stats.state_updates.append(
            SourcePullStateUpdate(
                scope_kind="global",
                scope_key="daily",
                watermark_published_at=_watermark_after_snapshot(
                    self.snapshot,
                    self.stats.newest_published_at
                    if self.stats.deferred_total <= 0
                    else self.window.watermark,
                ),
            )
        )
        return self._result()

    def _result(self) -> list[ItemDraft] | SourcePullResult:
        return self.stats if self.request.include_stats else self.drafts

    def _requested_dates(self) -> list[str | None]:
        dates = _iter_period_dates(
            period_start=self.window.period_start,
            period_end=self.window.period_end,
        )
        return dates or [None]

    def _pull_date(self, requested_date: str | None) -> None:
        remaining = self.request.max_items - len(self.drafts)
        if remaining <= 0:
            return
        papers = self.hf_api.list_daily_papers(
            date=requested_date,
            limit=remaining + 1,
        )
        for paper in papers:
            draft = _paper_info_to_draft(
                paper=paper,
                base_url=self.base_url,
                index_url=self._index_url(requested_date),
                window_date=requested_date,
            )
            if draft is None or not self._should_keep_draft(draft, requested_date):
                continue
            self.drafts.append(draft)

    def _index_url(self, requested_date: str | None) -> str:
        if requested_date is None:
            return f"{self.base_url}/papers"
        return f"{self.base_url}/papers/date/{requested_date}"

    def _should_keep_draft(
        self, draft: ItemDraft, requested_date: str | None
    ) -> bool:
        source_item_id = str(draft.source_item_id or "").strip()
        if not source_item_id or source_item_id in self.seen_ids:
            if source_item_id:
                self.stats.deduped_total += 1
            return False
        self.seen_ids.add(source_item_id)
        if not self._in_requested_window(draft, requested_date):
            return False
        if len(self.drafts) >= self.request.max_items:
            self.stats.deferred_total += 1
            return False
        _record_stats_published_at(self.stats, draft.published_at)
        return True

    def _in_requested_window(self, draft: ItemDraft, requested_date: str | None) -> bool:
        if self.window.period_start is None or self.window.period_end is None:
            return True
        if draft.published_at is None:
            self.stats.missing_published_at_total += 1
            return requested_date is not None
        if not _datetime_in_period(
            value=draft.published_at,
            period_start=self.window.period_start,
            period_end=self.window.period_end,
        ):
            self.stats.filtered_out_total += 1
            return False
        if self._older_than_watermark(draft.published_at):
            self.stats.filtered_out_total += 1
            return False
        self.stats.in_window_total += 1
        return True

    def _older_than_watermark(self, published_at: datetime) -> bool:
        if self.window.watermark is None:
            return False
        if self.request.period_start is not None or self.request.period_end is not None:
            return False
        return _normalize_datetime(published_at) <= self.window.watermark

    def _lookup_snapshot(self) -> SourcePullStateSnapshot | None:
        lookup = self.request.pull_state_lookup
        if not callable(lookup):
            return None
        return lookup("global", "daily")

    def _window_from_request(self) -> _HFDailyWindow:
        period_start, period_end = _normalize_period_bounds(
            period_start=self.request.period_start,
            period_end=self.request.period_end,
        )
        watermark = (
            _normalize_datetime(self.snapshot.watermark_published_at)
            if self.snapshot is not None
            and isinstance(self.snapshot.watermark_published_at, datetime)
            else None
        )
        if period_start is None and period_end is None and watermark is not None:
            period_start = watermark
            period_end = _source_pull_now() + timedelta(minutes=1)
        return _HFDailyWindow(
            period_start=period_start,
            period_end=period_end,
            watermark=watermark,
        )


def pull_arxiv_drafts(request: ArxivPullRequest) -> list[ItemDraft] | SourcePullResult:
    return _ArxivPuller(request).pull()


class _ArxivPuller:
    def __init__(self, request: ArxivPullRequest) -> None:
        self.request = request
        self.stats = SourcePullResult()
        self.drafts: list[ItemDraft] = []
        self.client = arxiv.Client()
        self.seen_entry_ids: set[str] = set()
        self.total_cap = (
            max(1, int(request.max_total_items))
            if request.max_total_items is not None and int(request.max_total_items) > 0
            else None
        )
        self.period_start, self.period_end = _normalize_period_bounds(
            period_start=request.period_start,
            period_end=request.period_end,
        )
        self.upper_bound = _source_pull_now() + timedelta(minutes=1)

    def pull(self) -> list[ItemDraft] | SourcePullResult:
        if self.request.max_results_per_run <= 0:
            return self._result()
        for query in self._queries():
            self._pull_query(query)
        self.stats.drafts = self.drafts
        return self._result()

    def _result(self) -> list[ItemDraft] | SourcePullResult:
        return self.stats if self.request.include_stats else self.drafts

    def _queries(self) -> list[str]:
        return [query.strip() for query in self.request.queries if query.strip()]

    def _pull_query(self, query: str) -> None:
        state = self._query_state(query)
        newest_published_at = state.watermark
        search = arxiv.Search(
            query=_arxiv_query_with_period(
                query=query,
                period_start=state.period_start,
                period_end=state.period_end,
            ),
            max_results=self.request.max_results_per_run,
            sort_by=arxiv.SortCriterion.SubmittedDate,
        )
        for result in self.client.results(search):
            draft = self._draft_for_result(query=query, result=result)
            if draft is None or not self._should_keep_draft(draft=draft, state=state):
                continue
            self.drafts.append(draft)
            newest_published_at = _newest_seen_timestamp(
                current=newest_published_at,
                candidate=draft.published_at,
            )
        self.stats.state_updates.append(
            SourcePullStateUpdate(
                scope_kind="query",
                scope_key=query,
                watermark_published_at=_watermark_after_snapshot(
                    state.snapshot,
                    newest_published_at
                    if self.stats.deferred_total <= 0
                    else state.watermark,
                ),
            )
        )

    def _should_keep_draft(
        self, *, draft: ItemDraft, state: _ArxivQueryState
    ) -> bool:
        entry_id = str(draft.canonical_url or "").strip()
        if not entry_id or entry_id in self.seen_entry_ids:
            if entry_id:
                self.stats.deduped_total += 1
            return False
        self.seen_entry_ids.add(entry_id)
        if not self._draft_in_query_window(draft=draft, state=state):
            return False
        if self.total_cap is not None and len(self.drafts) >= self.total_cap:
            self.stats.deferred_total += 1
            return False
        _record_stats_published_at(self.stats, draft.published_at)
        return True

    def _draft_in_query_window(
        self, *, draft: ItemDraft, state: _ArxivQueryState
    ) -> bool:
        if state.period_start is None or state.period_end is None:
            return True
        if draft.published_at is None:
            self.stats.missing_published_at_total += 1
            return False
        if not _datetime_in_period(
            value=draft.published_at,
            period_start=state.period_start,
            period_end=state.period_end,
        ):
            self.stats.filtered_out_total += 1
            return False
        if self._older_than_query_watermark(draft=draft, state=state):
            self.stats.filtered_out_total += 1
            return False
        self.stats.in_window_total += 1
        return True

    def _older_than_query_watermark(
        self, *, draft: ItemDraft, state: _ArxivQueryState
    ) -> bool:
        if state.watermark is None:
            return False
        if self.request.period_start is not None or self.request.period_end is not None:
            return False
        if draft.published_at is None:
            return False
        return _normalize_datetime(draft.published_at) <= state.watermark

    def _draft_for_result(self, *, query: str, result: Any) -> ItemDraft | None:
        entry_id = str(getattr(result, "entry_id", "") or "").strip()
        title = str(getattr(result, "title", "") or "").strip()
        if not entry_id or not title:
            return None
        published_at = _normalize_optional_datetime(getattr(result, "published", None))
        return ItemDraft.from_values(
            source="arxiv",
            source_item_id=_arxiv_source_item_id(result=result, fallback=entry_id),
            canonical_url=entry_id,
            title=title,
            authors=_named_authors(getattr(result, "authors", []) or []),
            published_at=published_at,
            raw_metadata=_arxiv_raw_metadata(
                query=query,
                result=result,
                period_start=self.period_start,
                period_end=self.period_end,
            ),
        )

    def _query_state(self, query: str) -> _ArxivQueryState:
        snapshot = _lookup_snapshot(self.request.pull_state_lookup, "query", query)
        watermark = _snapshot_watermark(snapshot)
        period_start = self.period_start
        period_end = self.period_end
        if period_start is None and period_end is None and watermark is not None:
            period_start = watermark
            period_end = self.upper_bound
        return _ArxivQueryState(
            query=query,
            snapshot=snapshot,
            watermark=watermark,
            period_start=period_start,
            period_end=period_end,
        )


def _arxiv_source_item_id(*, result: Any, fallback: str) -> str:
    get_short_id = getattr(result, "get_short_id", None)
    if not callable(get_short_id):
        return fallback
    try:
        short_id = str(get_short_id())
    except Exception:
        return fallback
    return _first_non_empty_str(short_id, fallback) or fallback


def _arxiv_raw_metadata(
    *,
    query: str,
    result: Any,
    period_start: datetime | None,
    period_end: datetime | None,
) -> dict[str, Any]:
    raw_metadata: dict[str, Any] = {"query": query, "matched_queries": [query]}
    categories = getattr(result, "categories", None)
    if isinstance(categories, list) and categories:
        raw_metadata["categories"] = [str(category) for category in categories]
    comment = getattr(result, "comment", None)
    if isinstance(comment, str) and comment.strip():
        raw_metadata["comment"] = comment.strip()
    if period_start is not None and period_end is not None:
        raw_metadata["query_period_start"] = period_start.isoformat()
        raw_metadata["query_period_end"] = period_end.isoformat()
    return raw_metadata


def pull_openreview_drafts(
    request: OpenReviewPullRequest,
) -> list[ItemDraft] | SourcePullResult:
    return _OpenReviewPuller(request).pull()


class _OpenReviewPuller:
    def __init__(self, request: OpenReviewPullRequest) -> None:
        self.request = request
        self.stats = SourcePullResult()
        self.drafts: list[ItemDraft] = []
        self.client = openreview.Client(baseurl="https://api.openreview.net")
        self.seen_note_ids: set[str] = set()
        self.total_cap = (
            max(1, int(request.max_total_items))
            if request.max_total_items is not None and int(request.max_total_items) > 0
            else None
        )
        self.period_start, self.period_end = _normalize_period_bounds(
            period_start=request.period_start,
            period_end=request.period_end,
        )

    def pull(self) -> list[ItemDraft] | SourcePullResult:
        if self.request.max_results_per_venue <= 0:
            return self._result()
        for venue in self._venues():
            self._pull_venue(venue)
        self.stats.drafts = self.drafts
        return self._result()

    def _result(self) -> list[ItemDraft] | SourcePullResult:
        return self.stats if self.request.include_stats else self.drafts

    def _venues(self) -> list[str]:
        return [venue.strip() for venue in self.request.venues if venue.strip()]

    def _pull_venue(self, venue: str) -> None:
        state = self._venue_state(venue)
        newest_published_at = state.watermark
        page_size = max(1, min(self.request.max_results_per_venue, 100))
        offset = 0
        venue_collected = 0
        while venue_collected < self.request.max_results_per_venue:
            notes = self._venue_notes(
                invitation=state.invitation,
                offset=offset,
                limit=page_size,
                period_start=state.period_start,
            )
            if not notes:
                break
            newest_published_at, venue_collected, collected = self._collect_venue_page(
                notes=notes,
                state=state,
                newest_published_at=newest_published_at,
                venue_collected=venue_collected,
            )
            if len(notes) < page_size or collected <= 0:
                if len(notes) < page_size:
                    break
            offset += len(notes)
        self.stats.state_updates.append(
            SourcePullStateUpdate(
                scope_kind="venue",
                scope_key=venue,
                watermark_published_at=_watermark_after_snapshot(
                    state.snapshot,
                    newest_published_at
                    if self.stats.deferred_total <= 0
                    else state.watermark,
                ),
            )
        )

    def _collect_venue_page(
        self,
        *,
        notes: list[Any],
        state: _OpenReviewVenueState,
        newest_published_at: datetime | None,
        venue_collected: int,
    ) -> tuple[datetime | None, int, int]:
        collected = 0
        for note in notes:
            draft = self._draft_for_note(note=note, state=state)
            if draft is None or not self._should_keep_draft(draft=draft, state=state):
                continue
            self.drafts.append(draft)
            newest_published_at = _newest_seen_timestamp(
                current=newest_published_at,
                candidate=draft.published_at,
            )
            venue_collected += 1
            collected += 1
            if venue_collected >= self.request.max_results_per_venue:
                break
        return newest_published_at, venue_collected, collected

    def _should_keep_draft(
        self, *, draft: ItemDraft, state: _OpenReviewVenueState
    ) -> bool:
        note_id = str(draft.source_item_id or "").strip()
        if not note_id or note_id in self.seen_note_ids:
            if note_id:
                self.stats.deduped_total += 1
            return False
        self.seen_note_ids.add(note_id)
        if not self._draft_in_venue_window(draft=draft, state=state):
            return False
        if self.total_cap is not None and len(self.drafts) >= self.total_cap:
            self.stats.deferred_total += 1
            return False
        _record_stats_published_at(self.stats, draft.published_at)
        return True

    def _draft_in_venue_window(
        self, *, draft: ItemDraft, state: _OpenReviewVenueState
    ) -> bool:
        if state.period_start is None or state.period_end is None:
            return True
        if draft.published_at is None:
            self.stats.missing_published_at_total += 1
            return False
        if not _datetime_in_period(
            value=draft.published_at,
            period_start=state.period_start,
            period_end=state.period_end,
        ):
            self.stats.filtered_out_total += 1
            return False
        if self._older_than_venue_watermark(draft=draft, state=state):
            self.stats.filtered_out_total += 1
            return False
        self.stats.in_window_total += 1
        return True

    def _older_than_venue_watermark(
        self, *, draft: ItemDraft, state: _OpenReviewVenueState
    ) -> bool:
        if state.watermark is None:
            return False
        if self.request.period_start is not None or self.request.period_end is not None:
            return False
        if draft.published_at is None:
            return False
        return _normalize_datetime(draft.published_at) <= state.watermark

    def _draft_for_note(
        self, *, note: Any, state: _OpenReviewVenueState
    ) -> ItemDraft | None:
        note_id = str(getattr(note, "id", "") or "").strip()
        title = _openreview_title(note)
        if not note_id or not title:
            return None
        published_at = _openreview_published_at(note)
        return ItemDraft.from_values(
            source="openreview",
            source_item_id=note_id,
            canonical_url=f"https://openreview.net/forum?id={note_id}",
            title=title,
            authors=_openreview_authors(note),
            published_at=published_at,
            raw_metadata={
                "invitation": state.invitation,
                "venue": state.venue,
                "matched_venues": [state.venue],
                "matched_invitations": [state.invitation],
            },
        )

    def _venue_notes(
        self, *, invitation: str, offset: int, limit: int, period_start: datetime | None
    ) -> list[Any]:
        kwargs: dict[str, Any] = {
            "invitation": invitation,
            "limit": limit,
            "offset": offset,
        }
        if period_start is not None:
            kwargs["mintcdate"] = int(period_start.timestamp() * 1000)
        try:
            return list(self.client.get_notes(**kwargs, sort="tcdate:desc"))
        except Exception:
            return list(self.client.get_notes(**kwargs))

    def _venue_state(self, venue: str) -> _OpenReviewVenueState:
        invitation = venue if "/-/" in venue else f"{venue}/-/Blind_Submission"
        snapshot = _lookup_snapshot(self.request.pull_state_lookup, "venue", venue)
        watermark = _snapshot_watermark(snapshot)
        period_start = self.period_start
        period_end = self.period_end
        if period_start is None and period_end is None and watermark is not None:
            period_start = watermark
            period_end = _source_pull_now() + timedelta(minutes=1)
        return _OpenReviewVenueState(
            venue=venue,
            invitation=invitation,
            snapshot=snapshot,
            watermark=watermark,
            period_start=period_start,
            period_end=period_end,
        )


def _openreview_title(note: Any) -> str:
    content = getattr(note, "content", None) or {}
    title_value = content.get("title") if isinstance(content, Mapping) else None
    if isinstance(title_value, Mapping):
        return str(title_value.get("value") or "").strip()
    return str(title_value or "").strip()


def _openreview_authors(note: Any) -> list[str]:
    content = getattr(note, "content", None) or {}
    authors_value = content.get("authors") if isinstance(content, Mapping) else None
    if isinstance(authors_value, Mapping):
        authors_value = authors_value.get("value")
    if not isinstance(authors_value, list):
        return []
    return [str(author).strip() for author in authors_value if str(author).strip()]


def _openreview_published_at(note: Any) -> datetime | None:
    tcdate = getattr(note, "tcdate", None)
    if not isinstance(tcdate, int):
        return None
    return datetime.fromtimestamp(tcdate / 1000, tz=timezone.utc)


def pull_rss_drafts(request: FeedPullRequest) -> list[ItemDraft] | SourcePullResult:
    return _FeedPuller(request).pull()


class _FeedPuller:
    def __init__(self, request: FeedPullRequest) -> None:
        self.request = request
        self.stats = SourcePullResult()
        self.drafts: list[ItemDraft] = []
        self.resolved_feed_urls: set[str] = set()
        self.seen_draft_keys: set[str] = set()
        self.normalized_start, self.normalized_end = _normalize_period_bounds(
            period_start=request.period_start,
            period_end=request.period_end,
        )
        self.total_cap = (
            max(1, int(request.max_total_items))
            if request.max_total_items is not None and int(request.max_total_items) > 0
            else None
        )

    def pull(self) -> list[ItemDraft] | SourcePullResult:
        with httpx.Client(
            timeout=httpx.Timeout(10.0, connect=5.0),
            headers={"User-Agent": "recoleta/0.1"},
            follow_redirects=True,
        ) as client:
            for feed_url in self.request.feed_urls:
                self._pull_feed(client=client, feed_url=feed_url)
        self.stats.drafts = self.drafts
        return self._result()

    def _result(self) -> list[ItemDraft] | SourcePullResult:
        return self.stats if self.request.include_stats else self.drafts

    def _pull_feed(self, *, client: httpx.Client, feed_url: str) -> None:
        state = self._initial_feed_state(feed_url)
        parsed, entries, response, loaded_state = self._loaded_feed(
            client=client,
            feed_url=feed_url,
            state=state,
        )
        if response.status_code == 304:
            self._record_not_modified(feed_url=feed_url, state=state)
            return
        if loaded_state.resolved_feed_url in self.resolved_feed_urls:
            return
        self.resolved_feed_urls.add(loaded_state.resolved_feed_url)
        feed = cast(dict[str, Any], getattr(parsed, "feed", {}) or {})
        feed_title = _get_str(feed, "title")
        newest_published_at = loaded_state.watermark
        kept_for_feed = 0
        for entry in self._filtered_entries(entries):
            if kept_for_feed >= self.request.max_items_per_feed:
                break
            draft = _feed_entry_draft(
                entry=entry,
                source=self.request.source,
                resolved_feed_url=loaded_state.resolved_feed_url,
                feed_title=feed_title,
                discovered_from=loaded_state.discovered_from,
            )
            if draft is None or not self._should_keep_draft(
                draft, watermark=loaded_state.watermark
            ):
                continue
            self.drafts.append(draft)
            kept_for_feed += 1
            newest_published_at = _newest_seen_timestamp(
                current=newest_published_at,
                candidate=draft.published_at,
            )
        self.stats.state_updates.append(
            SourcePullStateUpdate(
                scope_kind="feed",
                scope_key=feed_url,
                etag=str(response.headers.get("etag") or "").strip() or None,
                last_modified=(
                    str(response.headers.get("last-modified") or "").strip() or None
                ),
                watermark_published_at=_watermark_after_snapshot(
                    loaded_state.snapshot,
                    newest_published_at
                    if self.stats.deferred_total <= 0
                    else loaded_state.watermark,
                ),
                cursor={"resolved_feed_url": loaded_state.resolved_feed_url},
            )
        )

    def _should_keep_draft(self, draft: ItemDraft, *, watermark: datetime | None) -> bool:
        if not self._draft_in_feed_window(draft, watermark=watermark):
            return False
        draft_key = str(draft.source_item_id or "").strip() or draft.canonical_url_hash
        if draft_key in self.seen_draft_keys:
            self.stats.deduped_total += 1
            return False
        if self.total_cap is not None and len(self.drafts) >= self.total_cap:
            self.stats.deferred_total += 1
            return False
        self.seen_draft_keys.add(draft_key)
        _record_stats_published_at(self.stats, draft.published_at)
        return True

    def _draft_in_feed_window(
        self, draft: ItemDraft, *, watermark: datetime | None
    ) -> bool:
        if self.normalized_start is None or self.normalized_end is None:
            if self._older_than_feed_watermark(
                draft.published_at,
                watermark=watermark,
            ):
                self.stats.filtered_out_total += 1
                return False
            return True
        if draft.published_at is None:
            self.stats.missing_published_at_total += 1
            return False
        if not _datetime_in_period(
            value=draft.published_at,
            period_start=self.normalized_start,
            period_end=self.normalized_end,
        ):
            self.stats.filtered_out_total += 1
            return False
        self.stats.in_window_total += 1
        return True

    def _older_than_feed_watermark(
        self, published_at: datetime | None, *, watermark: datetime | None
    ) -> bool:
        if watermark is None or published_at is None:
            return False
        return _normalize_datetime(published_at) <= watermark

    def _filtered_entries(self, entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if self.normalized_start is None or self.normalized_end is None:
            return entries[: self.request.max_items_per_feed]
        return entries

    def _record_not_modified(self, *, feed_url: str, state: _FeedState) -> None:
        self.stats.not_modified_total += 1
        self.stats.state_updates.append(
            SourcePullStateUpdate(
                scope_kind="feed",
                scope_key=feed_url,
                etag=state.snapshot.etag if state.snapshot is not None else None,
                last_modified=(
                    state.snapshot.last_modified if state.snapshot is not None else None
                ),
                watermark_published_at=_watermark_after_snapshot(
                    state.snapshot,
                    state.watermark,
                ),
                cursor={"resolved_feed_url": state.resolved_feed_url},
            )
        )

    def _loaded_feed(
        self, *, client: httpx.Client, feed_url: str, state: _FeedState
    ) -> tuple[Any, list[dict[str, Any]], httpx.Response, _FeedState]:
        response = _fetch_feed_response(
            client,
            state.resolved_feed_url,
            etag=state.snapshot.etag if state.snapshot is not None else None,
            last_modified=state.snapshot.last_modified
            if state.snapshot is not None
            else None,
        )
        if response.status_code == 304:
            return None, [], response, state
        parsed = cast(Any, feedparser.parse(response.text))
        entries = cast(list[dict[str, Any]], getattr(parsed, "entries", []) or [])
        if entries or str(getattr(parsed, "version", "") or "").strip():
            return parsed, entries, response, state
        discovered = _discover_feed_url_from_html(
            page_url=state.resolved_feed_url,
            html=response.text,
        )
        if not discovered or discovered == state.resolved_feed_url:
            return parsed, entries, response, state
        discovered_state = _FeedState(
            feed_url=state.feed_url,
            snapshot=state.snapshot,
            watermark=state.watermark,
            resolved_feed_url=discovered,
            discovered_from=feed_url,
        )
        discovered_response = _fetch_feed_response(client, discovered)
        discovered_parsed = cast(Any, feedparser.parse(discovered_response.text))
        discovered_entries = cast(
            list[dict[str, Any]], getattr(discovered_parsed, "entries", []) or []
        )
        return discovered_parsed, discovered_entries, discovered_response, discovered_state

    def _initial_feed_state(self, feed_url: str) -> _FeedState:
        snapshot = _lookup_snapshot(self.request.pull_state_lookup, "feed", feed_url)
        resolved_feed_url = (
            _first_non_empty_str(
                (snapshot.cursor or {}).get("resolved_feed_url")
                if snapshot is not None
                else None,
                feed_url,
            )
            or feed_url
        )
        return _FeedState(
            feed_url=feed_url,
            snapshot=snapshot,
            watermark=_snapshot_watermark(snapshot),
            resolved_feed_url=resolved_feed_url,
            discovered_from=None,
        )


def _feed_entry_draft(
    *,
    entry: dict[str, Any],
    source: str,
    resolved_feed_url: str,
    feed_title: str,
    discovered_from: str | None,
) -> ItemDraft | None:
    link = _get_str(entry, "link")
    title = _get_str(entry, "title")
    if not link or not title:
        return None
    published_at = _parse_entry_datetime(entry)
    raw_metadata: dict[str, Any] = {
        "feed_url": resolved_feed_url,
        "feed_title": feed_title,
        "feed_discovered_from": discovered_from,
    }
    _merge_provenance_list(
        raw_metadata,
        key="matched_feed_urls",
        value=resolved_feed_url,
    )
    return ItemDraft.from_values(
        source=source,
        source_item_id=_first_non_empty_str(entry.get("id"), entry.get("guid"), link),
        canonical_url=link,
        title=title,
        authors=_feed_authors(entry),
        published_at=published_at,
        raw_metadata={key: value for key, value in raw_metadata.items() if value is not None},
    )


def _feed_authors(entry: dict[str, Any]) -> list[str]:
    authors: list[str] = []
    raw_authors = entry.get("authors")
    if isinstance(raw_authors, list):
        for author in raw_authors:
            if isinstance(author, dict):
                name = author.get("name")
                if isinstance(name, str) and name.strip():
                    authors.append(name.strip())
    if authors:
        return authors
    single_author = _get_str(entry, "author")
    return [single_author] if single_author else []


def pull_hn_drafts(request: HNPullRequest) -> list[ItemDraft] | SourcePullResult:
    return _HNPuller(request).pull()


class _HNPuller:
    def __init__(self, request: HNPullRequest) -> None:
        self.request = request
        self.stats = SourcePullResult()
        self.drafts: list[ItemDraft] = []
        self.normalized_start, self.normalized_end = _normalize_period_bounds(
            period_start=request.period_start,
            period_end=request.period_end,
        )
        self.total_cap = (
            max(1, int(request.max_total_items))
            if request.max_total_items is not None and int(request.max_total_items) > 0
            else max(1, int(request.max_items_per_feed)) * max(1, len(request.feed_urls))
        )
        self.seen_ids: set[str] = set()

    def pull(self) -> list[ItemDraft] | SourcePullResult:
        if self.normalized_start is None or self.normalized_end is None:
            return pull_rss_drafts(
                FeedPullRequest(
                    feed_urls=self.request.feed_urls,
                    source="hn",
                    max_items_per_feed=self.request.max_items_per_feed,
                    period_start=self.request.period_start,
                    period_end=self.request.period_end,
                    max_total_items=self.request.max_total_items,
                    pull_state_lookup=self.request.pull_state_lookup,
                    include_stats=self.request.include_stats,
                )
            )
        self._pull_algolia_window()
        self.stats.drafts = self.drafts
        self.stats.state_updates.append(
            SourcePullStateUpdate(
                scope_kind="feed",
                scope_key=str(
                    self.request.feed_urls[0]
                    if self.request.feed_urls
                    else "https://news.ycombinator.com/rss"
                ),
                watermark_published_at=(
                    self.stats.newest_published_at
                    if self.stats.deferred_total <= 0
                    else None
                ),
                cursor={"source_api": "algolia"},
            )
        )
        return self._result()

    def _pull_algolia_window(self) -> None:
        with httpx.Client(
            timeout=httpx.Timeout(10.0, connect=5.0),
            headers={"User-Agent": "recoleta/0.1"},
            follow_redirects=True,
        ) as client:
            page = 0
            page_size = min(max(self.total_cap, self.request.max_items_per_feed), 100)
            while len(self.drafts) < self.total_cap:
                hits, has_next_page = self._hits_for_page(
                    client=client,
                    page=page,
                    page_size=page_size,
                )
                if not hits:
                    break
                self._append_hits(hits)
                if not has_next_page:
                    break
                page += 1

    def _append_hits(self, hits: list[dict[str, Any]]) -> int:
        kept = 0
        for hit in hits:
            if len(self.drafts) >= self.total_cap:
                self.stats.deferred_total += 1
                continue
            draft = _hn_hit_draft(hit=hit, feed_urls=self.request.feed_urls)
            if draft is None or not self._should_keep_draft(draft):
                continue
            self.drafts.append(draft)
            kept += 1
        return kept

    def _result(self) -> list[ItemDraft] | SourcePullResult:
        return self.stats if self.request.include_stats else self.drafts

    def _hits_for_page(
        self, *, client: httpx.Client, page: int, page_size: int
    ) -> tuple[list[dict[str, Any]], bool]:
        response = client.get(
            "https://hn.algolia.com/api/v1/search_by_date",
            params={
                "tags": "story",
                "hitsPerPage": page_size,
                "page": page,
                "numericFilters": ",".join(
                    [
                        f"created_at_i>={int(self.normalized_start.timestamp())}",
                        f"created_at_i<{int(self.normalized_end.timestamp())}",
                    ]
                ),
            },
        )
        response.raise_for_status()
        payload = response.json()
        hits = payload.get("hits") if isinstance(payload, dict) else None
        nb_pages = int(payload.get("nbPages") or 0) if isinstance(payload, dict) else 0
        has_next_page = nb_pages > 0 and page + 1 < nb_pages
        return (list(hits) if isinstance(hits, list) else [], has_next_page)

    def _should_keep_draft(self, draft: ItemDraft) -> bool:
        source_item_id = str(draft.source_item_id or "").strip()
        if not source_item_id or source_item_id in self.seen_ids:
            if source_item_id:
                self.stats.deduped_total += 1
            return False
        self.seen_ids.add(source_item_id)
        if draft.published_at is None:
            self.stats.missing_published_at_total += 1
            return False
        if not _datetime_in_period(
            value=draft.published_at,
            period_start=self.normalized_start,
            period_end=self.normalized_end,
        ):
            self.stats.filtered_out_total += 1
            return False
        self.stats.in_window_total += 1
        _record_stats_published_at(self.stats, draft.published_at)
        return True


def _hn_hit_draft(*, hit: Any, feed_urls: list[str]) -> ItemDraft | None:
    if not isinstance(hit, dict):
        return None
    source_item_id = str(hit.get("objectID") or "").strip()
    title = _first_non_empty_str(hit.get("title"), hit.get("story_title"))
    created_at_i = hit.get("created_at_i")
    if not source_item_id or title is None or not isinstance(created_at_i, int):
        return None
    published_at = datetime.fromtimestamp(created_at_i, tz=timezone.utc)
    canonical_url = _first_non_empty_str(
        hit.get("url"),
        hit.get("story_url"),
        f"https://news.ycombinator.com/item?id={source_item_id}",
    )
    if canonical_url is None:
        return None
    author = str(hit.get("author") or "").strip()
    raw_metadata: dict[str, Any] = {"source_api": "algolia"}
    for feed_url in feed_urls:
        _merge_provenance_list(
            raw_metadata,
            key="matched_feed_urls",
            value=feed_url,
        )
    return ItemDraft.from_values(
        source="hn",
        source_item_id=source_item_id,
        canonical_url=canonical_url,
        title=title,
        authors=[author] if author else [],
        published_at=published_at,
        raw_metadata=raw_metadata,
    )


def _lookup_snapshot(
    lookup: PullStateLookup | None, scope_kind: str, scope_key: str
) -> SourcePullStateSnapshot | None:
    if not callable(lookup):
        return None
    return lookup(scope_kind, scope_key)


def _snapshot_watermark(snapshot: SourcePullStateSnapshot | None) -> datetime | None:
    if snapshot is None or not isinstance(snapshot.watermark_published_at, datetime):
        return None
    return _normalize_datetime(snapshot.watermark_published_at)


def _normalize_optional_datetime(value: Any) -> datetime | None:
    if not isinstance(value, datetime):
        return None
    return _normalize_datetime(value)


def _named_authors(authors: list[Any]) -> list[str]:
    names: list[str] = []
    for author in authors:
        name = getattr(author, "name", None)
        if isinstance(name, str) and name.strip():
            names.append(name.strip())
    return names


def _newest_seen_timestamp(
    *, current: datetime | None, candidate: datetime | None
) -> datetime | None:
    if candidate is None:
        return current
    normalized_candidate = _normalize_datetime(candidate)
    if current is None or normalized_candidate > current:
        return normalized_candidate
    return current
