from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import time
from typing import Any, Protocol
from uuid import uuid4

import arxiv

from recoleta.sources import _arxiv_query_with_period
from recoleta.types import ItemDraft

_ARXIV_RATE_STATE_NAME = "arxiv_api"
_ARXIV_SYNC_LEASE_NAME = "arxiv_pool_sync"
_ARXIV_POOL_SCHEMA_VERSION = 1
_ARXIV_VERSION_RE = re.compile(r"v(?P<version>\d+)$")


@dataclass(frozen=True, slots=True)
class ArxivPoolPaper:
    arxiv_id: str
    version: int | None
    canonical_url: str
    title: str
    abstract: str | None = None
    authors: list[str] = field(default_factory=list)
    primary_category: str | None = None
    categories: list[str] = field(default_factory=list)
    published_at: datetime | None = None
    updated_at: datetime | None = None
    comment: str | None = None
    journal_ref: str | None = None
    doi: str | None = None
    raw_atom: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ArxivPoolWindow:
    query_text: str
    period_start: datetime
    period_end: datetime
    max_results: int


@dataclass(frozen=True, slots=True)
class ArxivPoolWindowRecord:
    query_text: str
    period_start: datetime
    period_end: datetime
    max_results: int
    status: str
    requested_at: datetime | None
    completed_at: datetime | None
    cooldown_until: datetime | None
    upstream_requests_total: int
    upstream_status: int | None
    error_category: str | None
    error_message: str | None
    result_count: int


@dataclass(frozen=True, slots=True)
class ArxivPoolRateState:
    last_request_at: datetime | None
    cooldown_until: datetime | None
    consecutive_429_total: int
    last_status: int | None
    last_error_message: str | None


@dataclass(slots=True)
class ArxivPoolSyncResult:
    requested_windows_total: int = 0
    completed_windows_total: int = 0
    cache_hit_total: int = 0
    cache_miss_total: int = 0
    upstream_requests_total: int = 0
    upstream_429_total: int = 0
    cooldown_active_total: int = 0
    skipped_windows_total: int = 0
    rate_limited_windows_total: int = 0
    failed_windows_total: int = 0
    papers_total: int = 0

    def as_payload(self) -> dict[str, int]:
        return {
            "requested_windows_total": self.requested_windows_total,
            "completed_windows_total": self.completed_windows_total,
            "cache_hit_total": self.cache_hit_total,
            "cache_miss_total": self.cache_miss_total,
            "upstream_requests_total": self.upstream_requests_total,
            "upstream_429_total": self.upstream_429_total,
            "cooldown_active_total": self.cooldown_active_total,
            "skipped_windows_total": self.skipped_windows_total,
            "rate_limited_windows_total": self.rate_limited_windows_total,
            "failed_windows_total": self.failed_windows_total,
            "papers_total": self.papers_total,
        }


class ArxivPoolRateLimitedError(RuntimeError):
    def __init__(
        self,
        message: str = "arXiv API rate limited",
        *,
        retry_after_seconds: int | None = None,
    ) -> None:
        super().__init__(message)
        self.retry_after_seconds = retry_after_seconds


class ArxivPoolLeaseHeldError(RuntimeError):
    pass


class ArxivPoolFetcher(Protocol):
    def fetch(self, window: ArxivPoolWindow) -> list[ArxivPoolPaper]: ...


class ArxivApiFetcher:
    def fetch(self, window: ArxivPoolWindow) -> list[ArxivPoolPaper]:
        search = arxiv.Search(
            query=_arxiv_query_with_period(
                query=window.query_text,
                period_start=window.period_start,
                period_end=window.period_end,
            ),
            max_results=max(1, int(window.max_results)),
            sort_by=arxiv.SortCriterion.SubmittedDate,
        )
        try:
            return [
                paper
                for paper in (_paper_from_arxiv_result(result) for result in arxiv.Client().results(search))
                if paper is not None
            ]
        except Exception as exc:
            if _exception_status_code(exc) == 429:
                raise ArxivPoolRateLimitedError(
                    retry_after_seconds=_retry_after_seconds(exc),
                ) from exc
            raise


class ArxivPoolStore:
    def __init__(self, db_path: Path) -> None:
        self.db_path = Path(db_path).expanduser().resolve()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def init_schema(self) -> None:
        with self._connect() as conn:
            conn.executescript(_SCHEMA_DDL)
            conn.execute(f"PRAGMA user_version = {_ARXIV_POOL_SCHEMA_VERSION}")
            conn.commit()

    def get_window(self, window: ArxivPoolWindow) -> ArxivPoolWindowRecord | None:
        self.init_schema()
        normalized_window = _normalize_window(window)
        with self._connect() as conn:
            query_id = self._query_id(
                conn=conn,
                query_text=normalized_window.query_text,
                create=False,
            )
            if query_id is None:
                return None
            row = conn.execute(
                """
                SELECT w.*, q.query_text
                FROM arxiv_query_windows w
                JOIN arxiv_queries q ON q.id = w.query_id
                WHERE w.query_id = ?
                  AND w.period_start = ?
                  AND w.period_end = ?
                  AND w.max_results = ?
                """,
                (
                    query_id,
                    _datetime_to_text(normalized_window.period_start),
                    _datetime_to_text(normalized_window.period_end),
                    normalized_window.max_results,
                ),
            ).fetchone()
        return _window_record_from_row(row) if row is not None else None

    def is_window_completed(self, window: ArxivPoolWindow) -> bool:
        record = self.get_window(window)
        return record is not None and record.status == "completed"

    def cached_papers_for_window(
        self, window: ArxivPoolWindow
    ) -> list[ArxivPoolPaper] | None:
        self.init_schema()
        normalized_window = _normalize_window(window)
        with self._connect() as conn:
            query_id = self._query_id(
                conn=conn,
                query_text=normalized_window.query_text,
                create=False,
            )
            if query_id is None:
                return None
            window_row = conn.execute(
                """
                SELECT status
                FROM arxiv_query_windows
                WHERE query_id = ?
                  AND period_start = ?
                  AND period_end = ?
                  AND max_results = ?
                """,
                (
                    query_id,
                    _datetime_to_text(normalized_window.period_start),
                    _datetime_to_text(normalized_window.period_end),
                    normalized_window.max_results,
                ),
            ).fetchone()
            if window_row is None or str(window_row["status"]) != "completed":
                return None
            rows = conn.execute(
                """
                SELECT p.*
                FROM arxiv_query_matches m
                JOIN arxiv_papers p ON p.arxiv_id = m.arxiv_id
                WHERE m.query_id = ?
                  AND m.period_start = ?
                  AND m.period_end = ?
                  AND m.max_results = ?
                ORDER BY m.sort_position ASC, m.arxiv_id ASC
                """,
                (
                    query_id,
                    _datetime_to_text(normalized_window.period_start),
                    _datetime_to_text(normalized_window.period_end),
                    normalized_window.max_results,
                ),
            ).fetchall()
        return [_paper_from_row(row) for row in rows]

    def record_completed_window(
        self,
        *,
        window: ArxivPoolWindow,
        papers: list[ArxivPoolPaper],
        upstream_status: int = 200,
    ) -> None:
        self.init_schema()
        normalized_window = _normalize_window(window)
        now = _utc_now()
        with self._connect() as conn:
            query_id = self._query_id(
                conn=conn,
                query_text=normalized_window.query_text,
                create=True,
            )
            assert query_id is not None
            for paper in papers:
                self._upsert_paper(conn=conn, paper=paper, seen_at=now)
            self._replace_matches(
                conn=conn,
                query_id=query_id,
                window=normalized_window,
                papers=papers,
                matched_at=now,
            )
            self._upsert_window(
                conn=conn,
                query_id=query_id,
                window=normalized_window,
                status="completed",
                requested_at=now,
                completed_at=now,
                cooldown_until=None,
                upstream_requests_total=1,
                upstream_status=upstream_status,
                error_category=None,
                error_message=None,
                result_count=len(papers),
            )
            self._set_rate_state(
                conn=conn,
                last_request_at=now,
                cooldown_until=None,
                last_status=upstream_status,
                last_error_message=None,
                consecutive_429_total=0,
            )
            conn.commit()

    def record_rate_limited_window(
        self,
        *,
        window: ArxivPoolWindow,
        cooldown_until: datetime,
        error_message: str,
        upstream_status: int = 429,
    ) -> None:
        self.init_schema()
        normalized_window = _normalize_window(window)
        now = _utc_now()
        with self._connect() as conn:
            query_id = self._query_id(
                conn=conn,
                query_text=normalized_window.query_text,
                create=True,
            )
            assert query_id is not None
            previous = self._rate_state(conn=conn)
            self._upsert_window(
                conn=conn,
                query_id=query_id,
                window=normalized_window,
                status="rate_limited",
                requested_at=now,
                completed_at=None,
                cooldown_until=cooldown_until,
                upstream_requests_total=1,
                upstream_status=upstream_status,
                error_category="rate_limited",
                error_message=error_message,
                result_count=0,
            )
            self._set_rate_state(
                conn=conn,
                last_request_at=now,
                cooldown_until=cooldown_until,
                last_status=upstream_status,
                last_error_message=error_message,
                consecutive_429_total=(
                    int(previous.consecutive_429_total) + 1
                    if previous is not None
                    else 1
                ),
            )
            conn.commit()

    def record_failed_window(
        self,
        *,
        window: ArxivPoolWindow,
        error_category: str,
        error_message: str,
        upstream_status: int | None = None,
    ) -> None:
        self.init_schema()
        normalized_window = _normalize_window(window)
        now = _utc_now()
        with self._connect() as conn:
            query_id = self._query_id(
                conn=conn,
                query_text=normalized_window.query_text,
                create=True,
            )
            assert query_id is not None
            self._upsert_window(
                conn=conn,
                query_id=query_id,
                window=normalized_window,
                status="failed",
                requested_at=now,
                completed_at=None,
                cooldown_until=None,
                upstream_requests_total=1,
                upstream_status=upstream_status,
                error_category=error_category,
                error_message=error_message,
                result_count=0,
            )
            self._set_rate_state(
                conn=conn,
                last_request_at=now,
                cooldown_until=None,
                last_status=upstream_status,
                last_error_message=error_message,
                consecutive_429_total=0,
            )
            conn.commit()

    def get_rate_state(self) -> ArxivPoolRateState | None:
        self.init_schema()
        with self._connect() as conn:
            return self._rate_state(conn=conn)

    def seconds_until_next_request(
        self, *, request_interval_seconds: float, now: datetime | None = None
    ) -> float:
        state = self.get_rate_state()
        if state is None or state.last_request_at is None:
            return 0.0
        reference = _ensure_utc(now or _utc_now())
        next_at = state.last_request_at + timedelta(
            seconds=max(0.0, float(request_interval_seconds))
        )
        return max(0.0, (next_at - reference).total_seconds())

    def list_window_records(
        self, *, limit: int = 50
    ) -> list[ArxivPoolWindowRecord]:
        self.init_schema()
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT w.*, q.query_text
                FROM arxiv_query_windows w
                JOIN arxiv_queries q ON q.id = w.query_id
                ORDER BY w.period_start DESC, q.query_text ASC
                LIMIT ?
                """,
                (max(1, int(limit)),),
            ).fetchall()
        return [_window_record_from_row(row) for row in rows]

    def prune_query_matches_older_than(self, cutoff: datetime) -> int:
        self.init_schema()
        with self._connect() as conn:
            result = conn.execute(
                """
                DELETE FROM arxiv_query_matches
                WHERE period_end < ?
                """,
                (_datetime_to_text(cutoff),),
            )
            conn.commit()
        return int(result.rowcount or 0)

    def acquire_sync_lease(self, *, owner_token: str, timeout_seconds: int) -> None:
        self.init_schema()
        now = _utc_now()
        expires_at = now + timedelta(seconds=max(1, int(timeout_seconds)))
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute(
                """
                SELECT owner_token, expires_at
                FROM arxiv_pool_leases
                WHERE name = ?
                """,
                (_ARXIV_SYNC_LEASE_NAME,),
            ).fetchone()
            if row is not None:
                existing_expires_at = _datetime_from_text(row["expires_at"])
                existing_owner = str(row["owner_token"] or "")
                if (
                    existing_owner != owner_token
                    and existing_expires_at is not None
                    and existing_expires_at > now
                ):
                    raise ArxivPoolLeaseHeldError(
                        "arXiv pool sync lease is already held"
                    )
            conn.execute(
                """
                INSERT INTO arxiv_pool_leases (
                    name, owner_token, acquired_at, expires_at
                )
                VALUES (?, ?, ?, ?)
                ON CONFLICT(name) DO UPDATE SET
                    owner_token = excluded.owner_token,
                    acquired_at = excluded.acquired_at,
                    expires_at = excluded.expires_at
                """,
                (
                    _ARXIV_SYNC_LEASE_NAME,
                    owner_token,
                    _datetime_to_text(now),
                    _datetime_to_text(expires_at),
                ),
            )
            conn.commit()

    def release_sync_lease(self, *, owner_token: str) -> None:
        self.init_schema()
        with self._connect() as conn:
            conn.execute(
                """
                DELETE FROM arxiv_pool_leases
                WHERE name = ?
                  AND owner_token = ?
                """,
                (_ARXIV_SYNC_LEASE_NAME, owner_token),
            )
            conn.commit()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=30)
        conn.row_factory = sqlite3.Row
        return conn

    def _query_id(
        self,
        *,
        conn: sqlite3.Connection,
        query_text: str,
        create: bool,
    ) -> int | None:
        normalized = normalize_arxiv_query(query_text)
        if not normalized:
            return None
        fingerprint = arxiv_query_fingerprint(normalized)
        now = _datetime_to_text(_utc_now())
        if create:
            conn.execute(
                """
                INSERT INTO arxiv_queries (fingerprint, query_text, created_at, updated_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(fingerprint) DO UPDATE SET
                    query_text = excluded.query_text,
                    updated_at = excluded.updated_at
                """,
                (fingerprint, normalized, now, now),
            )
        row = conn.execute(
            "SELECT id FROM arxiv_queries WHERE fingerprint = ?",
            (fingerprint,),
        ).fetchone()
        return int(row["id"]) if row is not None else None

    def _upsert_paper(
        self,
        *,
        conn: sqlite3.Connection,
        paper: ArxivPoolPaper,
        seen_at: datetime,
    ) -> None:
        normalized_paper = normalize_pool_paper(paper)
        conn.execute(
            """
            INSERT INTO arxiv_papers (
                arxiv_id, version, canonical_url, title, abstract, authors_json,
                primary_category, categories_json, published_at, updated_at, comment,
                journal_ref, doi, raw_atom_json, first_seen_at, last_seen_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(arxiv_id) DO UPDATE SET
                version = excluded.version,
                canonical_url = excluded.canonical_url,
                title = excluded.title,
                abstract = excluded.abstract,
                authors_json = excluded.authors_json,
                primary_category = excluded.primary_category,
                categories_json = excluded.categories_json,
                published_at = excluded.published_at,
                updated_at = excluded.updated_at,
                comment = excluded.comment,
                journal_ref = excluded.journal_ref,
                doi = excluded.doi,
                raw_atom_json = excluded.raw_atom_json,
                last_seen_at = excluded.last_seen_at
            """,
            (
                normalized_paper.arxiv_id,
                normalized_paper.version,
                normalized_paper.canonical_url,
                normalized_paper.title,
                normalized_paper.abstract,
                _json_dumps(normalized_paper.authors),
                normalized_paper.primary_category,
                _json_dumps(normalized_paper.categories),
                _datetime_to_text(normalized_paper.published_at),
                _datetime_to_text(normalized_paper.updated_at),
                normalized_paper.comment,
                normalized_paper.journal_ref,
                normalized_paper.doi,
                _json_dumps(normalized_paper.raw_atom),
                _datetime_to_text(seen_at),
                _datetime_to_text(seen_at),
            ),
        )

    def _replace_matches(
        self,
        *,
        conn: sqlite3.Connection,
        query_id: int,
        window: ArxivPoolWindow,
        papers: list[ArxivPoolPaper],
        matched_at: datetime,
    ) -> None:
        period_start = _datetime_to_text(window.period_start)
        period_end = _datetime_to_text(window.period_end)
        conn.execute(
            """
            DELETE FROM arxiv_query_matches
            WHERE query_id = ?
              AND period_start = ?
              AND period_end = ?
              AND max_results = ?
            """,
            (query_id, period_start, period_end, window.max_results),
        )
        for sort_position, paper in enumerate(papers):
            conn.execute(
                """
                INSERT OR IGNORE INTO arxiv_query_matches (
                    query_id, period_start, period_end, max_results,
                    arxiv_id, sort_position, matched_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    query_id,
                    period_start,
                    period_end,
                    window.max_results,
                    normalize_arxiv_id(paper.arxiv_id),
                    sort_position,
                    _datetime_to_text(matched_at),
                ),
            )

    def _upsert_window(
        self,
        *,
        conn: sqlite3.Connection,
        query_id: int,
        window: ArxivPoolWindow,
        status: str,
        requested_at: datetime | None,
        completed_at: datetime | None,
        cooldown_until: datetime | None,
        upstream_requests_total: int,
        upstream_status: int | None,
        error_category: str | None,
        error_message: str | None,
        result_count: int,
    ) -> None:
        conn.execute(
            """
            INSERT INTO arxiv_query_windows (
                query_id, period_start, period_end, max_results, status,
                requested_at, completed_at, cooldown_until, upstream_requests_total,
                upstream_status, error_category, error_message, result_count
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(query_id, period_start, period_end, max_results) DO UPDATE SET
                status = excluded.status,
                requested_at = excluded.requested_at,
                completed_at = excluded.completed_at,
                cooldown_until = excluded.cooldown_until,
                upstream_requests_total = excluded.upstream_requests_total,
                upstream_status = excluded.upstream_status,
                error_category = excluded.error_category,
                error_message = excluded.error_message,
                result_count = excluded.result_count
            """,
            (
                query_id,
                _datetime_to_text(window.period_start),
                _datetime_to_text(window.period_end),
                int(window.max_results),
                status,
                _datetime_to_text(requested_at),
                _datetime_to_text(completed_at),
                _datetime_to_text(cooldown_until),
                int(upstream_requests_total),
                upstream_status,
                error_category,
                _truncate_error(error_message),
                int(result_count),
            ),
        )

    def _rate_state(self, *, conn: sqlite3.Connection) -> ArxivPoolRateState | None:
        row = conn.execute(
            """
            SELECT last_request_at, cooldown_until, consecutive_429_total,
                   last_status, last_error_message
            FROM arxiv_rate_state
            WHERE name = ?
            """,
            (_ARXIV_RATE_STATE_NAME,),
        ).fetchone()
        if row is None:
            return None
        return ArxivPoolRateState(
            last_request_at=_datetime_from_text(row["last_request_at"]),
            cooldown_until=_datetime_from_text(row["cooldown_until"]),
            consecutive_429_total=int(row["consecutive_429_total"] or 0),
            last_status=(
                int(row["last_status"]) if row["last_status"] is not None else None
            ),
            last_error_message=row["last_error_message"],
        )

    def _set_rate_state(
        self,
        *,
        conn: sqlite3.Connection,
        last_request_at: datetime,
        cooldown_until: datetime | None,
        consecutive_429_total: int,
        last_status: int | None,
        last_error_message: str | None,
    ) -> None:
        conn.execute(
            """
            INSERT INTO arxiv_rate_state (
                name, last_request_at, cooldown_until, consecutive_429_total,
                last_status, last_error_message
            )
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                last_request_at = excluded.last_request_at,
                cooldown_until = excluded.cooldown_until,
                consecutive_429_total = excluded.consecutive_429_total,
                last_status = excluded.last_status,
                last_error_message = excluded.last_error_message
            """,
            (
                _ARXIV_RATE_STATE_NAME,
                _datetime_to_text(last_request_at),
                _datetime_to_text(cooldown_until),
                int(consecutive_429_total),
                last_status,
                _truncate_error(last_error_message),
            ),
        )


class ArxivPoolSync:
    def __init__(
        self,
        *,
        store: ArxivPoolStore,
        fetcher: ArxivPoolFetcher | None = None,
        request_interval_seconds: float,
        cooldown_seconds: int,
        sleep: Any = time.sleep,
    ) -> None:
        self.store = store
        self.fetcher = fetcher or ArxivApiFetcher()
        self.request_interval_seconds = max(0.0, float(request_interval_seconds))
        self.cooldown_seconds = max(1, int(cooldown_seconds))
        self.sleep = sleep

    def sync_windows(
        self,
        windows: list[ArxivPoolWindow],
        *,
        force: bool = False,
    ) -> ArxivPoolSyncResult:
        self.store.init_schema()
        owner_token = uuid4().hex
        self.store.acquire_sync_lease(
            owner_token=owner_token,
            timeout_seconds=self._lease_timeout_seconds(windows),
        )
        try:
            return self._sync_windows_locked(windows=windows, force=force)
        finally:
            self.store.release_sync_lease(owner_token=owner_token)

    def _sync_windows_locked(
        self,
        *,
        windows: list[ArxivPoolWindow],
        force: bool,
    ) -> ArxivPoolSyncResult:
        result = ArxivPoolSyncResult(requested_windows_total=len(windows))
        for window in [_normalize_window(candidate) for candidate in windows]:
            if not force and self.store.is_window_completed(window):
                result.cache_hit_total += 1
                continue
            result.cache_miss_total += 1
            if self._cooldown_active():
                result.cooldown_active_total += 1
                result.skipped_windows_total += 1
                continue
            self._respect_request_interval()
            try:
                papers = self.fetcher.fetch(window)
            except ArxivPoolRateLimitedError as exc:
                result.upstream_requests_total += 1
                result.upstream_429_total += 1
                result.rate_limited_windows_total += 1
                cooldown_until = _utc_now() + timedelta(
                    seconds=exc.retry_after_seconds or self.cooldown_seconds
                )
                self.store.record_rate_limited_window(
                    window=window,
                    cooldown_until=cooldown_until,
                    error_message=str(exc),
                )
                break
            except Exception as exc:
                result.upstream_requests_total += 1
                result.failed_windows_total += 1
                self.store.record_failed_window(
                    window=window,
                    error_category=type(exc).__name__,
                    error_message=str(exc),
                    upstream_status=_exception_status_code(exc),
                )
                continue
            result.upstream_requests_total += 1
            normalized_papers = [normalize_pool_paper(paper) for paper in papers]
            self.store.record_completed_window(
                window=window,
                papers=normalized_papers,
            )
            result.completed_windows_total += 1
            result.papers_total += len(normalized_papers)
        return result

    def _lease_timeout_seconds(self, windows: list[ArxivPoolWindow]) -> int:
        estimated_seconds = len(windows) * (self.request_interval_seconds + 30.0)
        return max(3600, int(estimated_seconds))

    def _cooldown_active(self) -> bool:
        state = self.store.get_rate_state()
        if state is None or state.cooldown_until is None:
            return False
        return state.cooldown_until > _utc_now()

    def _respect_request_interval(self) -> None:
        delay = self.store.seconds_until_next_request(
            request_interval_seconds=self.request_interval_seconds
        )
        if delay > 0:
            self.sleep(delay)


def build_arxiv_pool_windows(
    *,
    queries: list[str],
    anchor_date: date,
    lookback_days: int,
    max_results: int,
) -> list[ArxivPoolWindow]:
    days = [
        anchor_date - timedelta(days=offset)
        for offset in range(max(1, int(lookback_days)) - 1, -1, -1)
    ]
    return build_arxiv_pool_windows_for_days(
        queries=queries,
        days=days,
        max_results=max_results,
    )


def build_arxiv_pool_windows_for_period(
    *,
    queries: list[str],
    period_start: datetime,
    period_end: datetime,
    max_results: int,
) -> list[ArxivPoolWindow]:
    start = _ensure_utc(period_start)
    end = _ensure_utc(period_end)
    if start >= end:
        return []
    days: list[date] = []
    cursor = start.date()
    while cursor < end.date():
        days.append(cursor)
        cursor += timedelta(days=1)
    return build_arxiv_pool_windows_for_days(
        queries=queries,
        days=days,
        max_results=max_results,
    )


def build_arxiv_pool_windows_for_days(
    *,
    queries: list[str],
    days: list[date],
    max_results: int,
) -> list[ArxivPoolWindow]:
    deduped_queries = list(dict.fromkeys(normalize_arxiv_query(q) for q in queries))
    deduped_queries = [query for query in deduped_queries if query]
    windows: list[ArxivPoolWindow] = []
    for day in days:
        period_start = datetime(day.year, day.month, day.day, tzinfo=UTC)
        period_end = period_start + timedelta(days=1)
        for query in deduped_queries:
            windows.append(
                ArxivPoolWindow(
                    query_text=query,
                    period_start=period_start,
                    period_end=period_end,
                    max_results=max(1, int(max_results)),
                )
            )
    return windows


def pool_paper_to_item_draft(
    *, paper: ArxivPoolPaper, window: ArxivPoolWindow
) -> ItemDraft:
    normalized = normalize_pool_paper(paper)
    raw_metadata = dict(normalized.raw_atom)
    raw_metadata.update(
        {
            "query": window.query_text,
            "matched_queries": [window.query_text],
            "query_period_start": _datetime_to_text(window.period_start),
            "query_period_end": _datetime_to_text(window.period_end),
            "arxiv_pool": True,
        }
    )
    if normalized.categories:
        raw_metadata["categories"] = list(normalized.categories)
    if normalized.primary_category:
        raw_metadata["primary_category"] = normalized.primary_category
    if normalized.comment:
        raw_metadata["comment"] = normalized.comment
    return ItemDraft.from_values(
        source="arxiv",
        source_item_id=normalized.arxiv_id,
        canonical_url=normalized.canonical_url,
        title=normalized.title,
        authors=normalized.authors,
        published_at=normalized.published_at,
        raw_metadata=raw_metadata,
    )


def normalize_arxiv_query(value: str) -> str:
    return " ".join(str(value or "").strip().split())


def arxiv_query_fingerprint(query_text: str) -> str:
    return hashlib.sha256(normalize_arxiv_query(query_text).encode("utf-8")).hexdigest()


def normalize_arxiv_id(value: str) -> str:
    raw = str(value or "").strip()
    if raw.startswith("http://") or raw.startswith("https://"):
        raw = raw.rstrip("/").rsplit("/", 1)[-1]
    for prefix in ("arXiv:", "arxiv:", "abs/", "pdf/", "html/"):
        if raw.startswith(prefix):
            raw = raw[len(prefix) :]
    if raw.endswith(".pdf"):
        raw = raw[:-4]
    normalized = raw.strip().strip("/")
    if not normalized:
        raise ValueError("arxiv_id must not be empty")
    return normalized


def normalize_pool_paper(paper: ArxivPoolPaper) -> ArxivPoolPaper:
    arxiv_id = normalize_arxiv_id(paper.arxiv_id)
    canonical_url = str(paper.canonical_url or "").strip() or f"https://arxiv.org/abs/{arxiv_id}"
    title = str(paper.title or "").strip()
    if not title:
        raise ValueError("arxiv pool paper title must not be empty")
    return ArxivPoolPaper(
        arxiv_id=arxiv_id,
        version=paper.version if paper.version is not None else _version_from_id(arxiv_id),
        canonical_url=canonical_url,
        title=title,
        abstract=str(paper.abstract or "").strip() or None,
        authors=[str(author).strip() for author in paper.authors if str(author).strip()],
        primary_category=str(paper.primary_category or "").strip() or None,
        categories=[
            str(category).strip()
            for category in paper.categories
            if str(category).strip()
        ],
        published_at=_ensure_utc_optional(paper.published_at),
        updated_at=_ensure_utc_optional(paper.updated_at),
        comment=str(paper.comment or "").strip() or None,
        journal_ref=str(paper.journal_ref or "").strip() or None,
        doi=str(paper.doi or "").strip() or None,
        raw_atom=dict(paper.raw_atom or {}),
    )


def resolve_arxiv_pool_db_path(settings: Any) -> Path:
    pool = getattr(settings, "arxiv_pool", None)
    db_path = getattr(pool, "db_path", None)
    if db_path is None:
        raise ValueError("ARXIV_POOL.db_path is required when arXiv pool mode is used")
    return Path(db_path).expanduser().resolve()


def _normalize_window(window: ArxivPoolWindow) -> ArxivPoolWindow:
    return ArxivPoolWindow(
        query_text=normalize_arxiv_query(window.query_text),
        period_start=_ensure_utc(window.period_start),
        period_end=_ensure_utc(window.period_end),
        max_results=max(1, int(window.max_results)),
    )


def _paper_from_arxiv_result(result: Any) -> ArxivPoolPaper | None:
    entry_id = str(getattr(result, "entry_id", "") or "").strip()
    title = str(getattr(result, "title", "") or "").strip()
    if not entry_id or not title:
        return None
    arxiv_id = _result_short_id(result=result, fallback=entry_id)
    return ArxivPoolPaper(
        arxiv_id=arxiv_id,
        version=_version_from_id(arxiv_id),
        canonical_url=entry_id,
        title=title,
        abstract=str(getattr(result, "summary", "") or "").strip() or None,
        authors=_named_authors(getattr(result, "authors", []) or []),
        primary_category=str(getattr(result, "primary_category", "") or "").strip()
        or None,
        categories=[
            str(category).strip()
            for category in getattr(result, "categories", []) or []
            if str(category).strip()
        ],
        published_at=_ensure_utc_optional(getattr(result, "published", None)),
        updated_at=_ensure_utc_optional(getattr(result, "updated", None)),
        comment=str(getattr(result, "comment", "") or "").strip() or None,
        journal_ref=str(getattr(result, "journal_ref", "") or "").strip() or None,
        doi=str(getattr(result, "doi", "") or "").strip() or None,
        raw_atom={
            "entry_id": entry_id,
            "pdf_url": str(getattr(result, "pdf_url", "") or "").strip() or None,
        },
    )


def _result_short_id(*, result: Any, fallback: str) -> str:
    get_short_id = getattr(result, "get_short_id", None)
    if callable(get_short_id):
        try:
            short_id = str(get_short_id() or "").strip()
        except Exception:
            short_id = ""
        if short_id:
            return short_id
    return normalize_arxiv_id(fallback)


def _named_authors(authors: list[Any]) -> list[str]:
    names: list[str] = []
    for author in authors:
        name = str(getattr(author, "name", author) or "").strip()
        if name:
            names.append(name)
    return names


def _paper_from_row(row: sqlite3.Row) -> ArxivPoolPaper:
    return ArxivPoolPaper(
        arxiv_id=str(row["arxiv_id"]),
        version=int(row["version"]) if row["version"] is not None else None,
        canonical_url=str(row["canonical_url"]),
        title=str(row["title"]),
        abstract=row["abstract"],
        authors=_json_list(row["authors_json"]),
        primary_category=row["primary_category"],
        categories=_json_list(row["categories_json"]),
        published_at=_datetime_from_text(row["published_at"]),
        updated_at=_datetime_from_text(row["updated_at"]),
        comment=row["comment"],
        journal_ref=row["journal_ref"],
        doi=row["doi"],
        raw_atom=_json_object(row["raw_atom_json"]),
    )


def _window_record_from_row(row: sqlite3.Row) -> ArxivPoolWindowRecord:
    return ArxivPoolWindowRecord(
        query_text=str(row["query_text"]),
        period_start=_datetime_from_text(row["period_start"]) or datetime.now(tz=UTC),
        period_end=_datetime_from_text(row["period_end"]) or datetime.now(tz=UTC),
        max_results=int(row["max_results"]),
        status=str(row["status"]),
        requested_at=_datetime_from_text(row["requested_at"]),
        completed_at=_datetime_from_text(row["completed_at"]),
        cooldown_until=_datetime_from_text(row["cooldown_until"]),
        upstream_requests_total=int(row["upstream_requests_total"] or 0),
        upstream_status=(
            int(row["upstream_status"]) if row["upstream_status"] is not None else None
        ),
        error_category=row["error_category"],
        error_message=row["error_message"],
        result_count=int(row["result_count"] or 0),
    )


def _version_from_id(arxiv_id: str) -> int | None:
    match = _ARXIV_VERSION_RE.search(str(arxiv_id or ""))
    if match is None:
        return None
    return int(match.group("version"))


def _utc_now() -> datetime:
    return datetime.now(tz=UTC)


def _ensure_utc(value: datetime) -> datetime:
    return value.replace(tzinfo=UTC) if value.tzinfo is None else value.astimezone(UTC)


def _ensure_utc_optional(value: Any) -> datetime | None:
    if not isinstance(value, datetime):
        return None
    return _ensure_utc(value)


def _datetime_to_text(value: datetime | None) -> str | None:
    if value is None:
        return None
    return _ensure_utc(value).isoformat()


def _datetime_from_text(value: Any) -> datetime | None:
    if value is None:
        return None
    raw = str(value or "").strip()
    if not raw:
        return None
    parsed = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    return _ensure_utc(parsed)


def _json_dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True)


def _json_list(value: Any) -> list[str]:
    try:
        loaded = json.loads(str(value or "[]"))
    except Exception:
        return []
    if not isinstance(loaded, list):
        return []
    return [str(item) for item in loaded]


def _json_object(value: Any) -> dict[str, Any]:
    try:
        loaded = json.loads(str(value or "{}"))
    except Exception:
        return {}
    return loaded if isinstance(loaded, dict) else {}


def _truncate_error(value: str | None) -> str | None:
    normalized = str(value or "").strip()
    if not normalized:
        return None
    return normalized[:1000]


def _exception_status_code(exc: BaseException) -> int | None:
    response = getattr(exc, "response", None)
    status = getattr(response, "status_code", None)
    if status is None:
        status = getattr(exc, "status", None)
    if status is None:
        return None
    try:
        return int(status)
    except Exception:
        return None


def _retry_after_seconds(exc: BaseException) -> int | None:
    response = getattr(exc, "response", None)
    headers = getattr(response, "headers", {}) or {}
    try:
        raw = headers.get("Retry-After")
    except Exception:
        raw = None
    try:
        return max(1, int(str(raw).strip()))
    except Exception:
        return None


_SCHEMA_DDL = """
CREATE TABLE IF NOT EXISTS arxiv_papers (
    arxiv_id TEXT PRIMARY KEY,
    version INTEGER,
    canonical_url TEXT NOT NULL,
    title TEXT NOT NULL,
    abstract TEXT,
    authors_json TEXT NOT NULL DEFAULT '[]',
    primary_category TEXT,
    categories_json TEXT NOT NULL DEFAULT '[]',
    published_at TEXT,
    updated_at TEXT,
    comment TEXT,
    journal_ref TEXT,
    doi TEXT,
    raw_atom_json TEXT NOT NULL DEFAULT '{}',
    first_seen_at TEXT NOT NULL,
    last_seen_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS arxiv_queries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fingerprint TEXT NOT NULL UNIQUE,
    query_text TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS arxiv_query_windows (
    query_id INTEGER NOT NULL,
    period_start TEXT NOT NULL,
    period_end TEXT NOT NULL,
    max_results INTEGER NOT NULL,
    status TEXT NOT NULL,
    requested_at TEXT,
    completed_at TEXT,
    cooldown_until TEXT,
    upstream_requests_total INTEGER NOT NULL DEFAULT 0,
    upstream_status INTEGER,
    error_category TEXT,
    error_message TEXT,
    result_count INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (query_id, period_start, period_end, max_results),
    FOREIGN KEY(query_id) REFERENCES arxiv_queries(id)
);

CREATE TABLE IF NOT EXISTS arxiv_query_matches (
    query_id INTEGER NOT NULL,
    period_start TEXT NOT NULL,
    period_end TEXT NOT NULL,
    max_results INTEGER NOT NULL,
    arxiv_id TEXT NOT NULL,
    sort_position INTEGER NOT NULL,
    matched_at TEXT NOT NULL,
    PRIMARY KEY (query_id, period_start, period_end, max_results, arxiv_id),
    FOREIGN KEY(query_id) REFERENCES arxiv_queries(id),
    FOREIGN KEY(arxiv_id) REFERENCES arxiv_papers(arxiv_id)
);

CREATE TABLE IF NOT EXISTS arxiv_rate_state (
    name TEXT PRIMARY KEY,
    last_request_at TEXT,
    cooldown_until TEXT,
    consecutive_429_total INTEGER NOT NULL DEFAULT 0,
    last_status INTEGER,
    last_error_message TEXT
);

CREATE TABLE IF NOT EXISTS arxiv_pool_leases (
    name TEXT PRIMARY KEY,
    owner_token TEXT NOT NULL,
    acquired_at TEXT NOT NULL,
    expires_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_arxiv_query_windows_status
    ON arxiv_query_windows(status);
CREATE INDEX IF NOT EXISTS ix_arxiv_query_windows_period
    ON arxiv_query_windows(period_start, period_end);
CREATE INDEX IF NOT EXISTS ix_arxiv_query_matches_arxiv_id
    ON arxiv_query_matches(arxiv_id);
"""
