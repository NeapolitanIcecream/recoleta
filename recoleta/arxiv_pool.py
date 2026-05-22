from __future__ import annotations

import calendar
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta
from email.utils import parsedate_to_datetime
import hashlib
import json
import math
from pathlib import Path
import random
import re
import sqlite3
import time
from typing import Any, Literal, Protocol
from urllib.parse import urlparse
from uuid import uuid4

import feedparser
import httpx
from loguru import logger

from recoleta.sources import _arxiv_query_with_period
from recoleta.types import ItemDraft

_ARXIV_API_URL = "https://export.arxiv.org/api/query"
_ARXIV_POOL_FETCHER_NAME = "httpx_atom"
_ARXIV_POOL_USER_AGENT = "Recoleta/0.2.1 (arxiv-pool; metadata cache)"
_ARXIV_RATE_STATE_NAME = "arxiv_api"
_ARXIV_SYNC_LEASE_NAME = "arxiv_pool_sync"
_ARXIV_POOL_SCHEMA_VERSION = 2
_ARXIV_VERSION_RE = re.compile(r"v(?P<version>\d+)$")
_ARXIV_POOL_READINESS_GATES = {"off", "warn", "strict"}


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
class ArxivPoolReadinessPolicy:
    maturity_lag_days: int = 1
    readiness_gate: str = "strict"
    allow_immature_windows: bool = False
    now: datetime | None = None

    def __post_init__(self) -> None:
        lag_days = max(0, int(self.maturity_lag_days))
        gate = _normalize_readiness_gate(self.readiness_gate)
        reference = _ensure_utc(self.now or _utc_now())
        object.__setattr__(self, "maturity_lag_days", lag_days)
        object.__setattr__(self, "readiness_gate", gate)
        object.__setattr__(self, "now", reference)

    @property
    def maturity_cutoff(self) -> datetime | None:
        if self.maturity_lag_days <= 0:
            return None
        assert self.now is not None
        current_utc_day = datetime(
            self.now.year,
            self.now.month,
            self.now.day,
            tzinfo=UTC,
        )
        return current_utc_day - timedelta(days=self.maturity_lag_days - 1)

    @property
    def allows_immature_windows(self) -> bool:
        return self.readiness_gate == "off" or bool(self.allow_immature_windows)

    def is_mature(self, window: ArxivPoolWindow | ArxivPoolWindowRecord) -> bool:
        cutoff = self.maturity_cutoff
        if cutoff is None:
            return True
        return _ensure_utc(window.period_end) <= cutoff

    def as_payload(self) -> dict[str, Any]:
        return {
            "timezone": "UTC",
            "maturity_lag_days": self.maturity_lag_days,
            "maturity_cutoff": _isoformat_or_none(self.maturity_cutoff),
            "readiness_gate": self.readiness_gate,
            "allow_immature_windows": bool(self.allow_immature_windows),
        }


@dataclass(frozen=True, slots=True)
class ArxivPoolWindowReadiness:
    window: ArxivPoolWindow
    record: ArxivPoolWindowRecord | None
    cache_readable: bool
    mature: bool
    analysis_ready: bool
    blocked_reason: str | None

    @property
    def status(self) -> str:
        if self.record is None:
            return "missing"
        return self.record.status

    @property
    def unavailable(self) -> bool:
        return (
            not self.analysis_ready
            and self.blocked_reason is not None
            and self.blocked_reason != "immature_window"
        )

    def as_payload(self) -> dict[str, Any]:
        return {
            "query_text": self.window.query_text,
            "period_start": self.window.period_start.isoformat(),
            "period_end": self.window.period_end.isoformat(),
            "max_results": self.window.max_results,
            "status": self.status,
            "cache_readable": self.cache_readable,
            "mature": self.mature,
            "analysis_ready": self.analysis_ready,
            "blocked_reason": self.blocked_reason,
        }


@dataclass(frozen=True, slots=True)
class ArxivPoolBackendReadiness:
    query_text: str
    period_start: datetime
    period_end: datetime
    max_results: int
    backend: Literal["local_sqlite", "huldra"]
    cache_status: str
    serving_status: str | None
    cache_readable: bool
    mature: bool
    analysis_ready: bool
    blocked_reason: str | None
    cache_key: str | None = None
    diagnostic: dict[str, Any] | None = None

    @property
    def status(self) -> str:
        return self.cache_status

    @property
    def unavailable(self) -> bool:
        return (
            not self.analysis_ready
            and self.blocked_reason is not None
            and self.blocked_reason != "immature_window"
        )

    def as_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "query_text": self.query_text,
            "period_start": self.period_start.isoformat(),
            "period_end": self.period_end.isoformat(),
            "max_results": self.max_results,
            "backend": self.backend,
            "status": self.cache_status,
            "cache_status": self.cache_status,
            "serving_status": self.serving_status,
            "cache_readable": self.cache_readable,
            "mature": self.mature,
            "analysis_ready": self.analysis_ready,
            "blocked_reason": self.blocked_reason,
            "cache_key": self.cache_key,
        }
        if self.diagnostic:
            payload["diagnostic"] = dict(self.diagnostic)
        return payload


@dataclass(frozen=True, slots=True)
class ArxivPoolWindowPullResult:
    papers: list[ArxivPoolPaper] | None
    complete: bool
    readiness: ArxivPoolBackendReadiness


class ArxivMetadataPoolBackend(Protocol):
    def cached_papers_for_window(
        self,
        window: ArxivPoolWindow,
        *,
        readiness_policy: ArxivPoolReadinessPolicy,
    ) -> ArxivPoolWindowPullResult: ...

    def evaluate_window_readiness(
        self,
        window: ArxivPoolWindow,
        *,
        readiness_policy: ArxivPoolReadinessPolicy,
    ) -> ArxivPoolBackendReadiness: ...


@dataclass(frozen=True, slots=True)
class ArxivPoolBackendDescriptor:
    kind: Literal["local_sqlite", "huldra"]
    identity: str


@dataclass(frozen=True, slots=True)
class ArxivPoolRateState:
    last_request_at: datetime | None
    cooldown_until: datetime | None
    consecutive_429_total: int
    last_status: int | None
    last_error_message: str | None


@dataclass(frozen=True, slots=True)
class ArxivPoolWorkerState:
    name: str
    last_started_at: datetime | None
    last_heartbeat_at: datetime | None
    last_completed_at: datetime | None
    last_planned_windows_total: int
    last_completed_windows_total: int
    last_cache_hit_total: int
    last_failed_windows_total: int
    last_cooldown_until: datetime | None
    next_wake_at: datetime | None
    last_error_category: str | None
    last_error_message: str | None


@dataclass(frozen=True, slots=True)
class ArxivPoolWorkerPassResult:
    planned_windows_total: int
    sync: ArxivPoolSyncResult
    next_wake_at: datetime
    next_sleep_seconds: float
    cooldown_until: datetime | None
    error_category: str | None = None
    error_message: str | None = None


@dataclass(frozen=True, slots=True)
class _WindowWrite:
    query_id: int
    window: ArxivPoolWindow
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
class _WindowRefreshFailure:
    query_id: int
    window: ArxivPoolWindow
    requested_at: datetime
    cooldown_until: datetime | None
    upstream_status: int | None
    error_category: str
    error_message: str


@dataclass(slots=True)
class ArxivPoolSyncResult:
    requested_windows_total: int = 0
    completed_windows_total: int = 0
    cache_hit_total: int = 0
    cache_miss_total: int = 0
    upstream_requests_total: int = 0
    upstream_429_total: int = 0
    retry_after_seconds: int | None = None
    cooldown_active_total: int = 0
    skipped_windows_total: int = 0
    rate_limited_windows_total: int = 0
    failed_windows_total: int = 0
    papers_total: int = 0

    def as_payload(self) -> dict[str, int | None]:
        return {
            "requested_windows_total": self.requested_windows_total,
            "completed_windows_total": self.completed_windows_total,
            "cache_hit_total": self.cache_hit_total,
            "cache_miss_total": self.cache_miss_total,
            "upstream_requests_total": self.upstream_requests_total,
            "upstream_429_total": self.upstream_429_total,
            "retry_after_seconds": self.retry_after_seconds,
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


class ArxivPoolFetchError(RuntimeError):
    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
    ) -> None:
        super().__init__(message)
        self.status = status_code
        self.status_code = status_code


class LocalSqliteArxivPoolBackend:
    def __init__(self, store: ArxivPoolStore) -> None:
        self.store = store

    def cached_papers_for_window(
        self,
        window: ArxivPoolWindow,
        *,
        readiness_policy: ArxivPoolReadinessPolicy,
    ) -> ArxivPoolWindowPullResult:
        readiness = self.evaluate_window_readiness(
            window,
            readiness_policy=readiness_policy,
        )
        if not readiness.analysis_ready:
            if readiness.blocked_reason != "immature_window":
                return ArxivPoolWindowPullResult(
                    papers=None,
                    complete=False,
                    readiness=readiness,
                )
            if not readiness_policy.allows_immature_windows:
                return ArxivPoolWindowPullResult(
                    papers=None,
                    complete=False,
                    readiness=readiness,
                )
        papers = self.store.cached_papers_for_window(window)
        return ArxivPoolWindowPullResult(
            papers=papers,
            complete=papers is not None,
            readiness=readiness,
        )

    def evaluate_window_readiness(
        self,
        window: ArxivPoolWindow,
        *,
        readiness_policy: ArxivPoolReadinessPolicy,
    ) -> ArxivPoolBackendReadiness:
        readiness = evaluate_arxiv_pool_window_readiness(
            store=self.store,
            window=window,
            policy=readiness_policy,
        )
        return ArxivPoolBackendReadiness(
            query_text=readiness.window.query_text,
            period_start=readiness.window.period_start,
            period_end=readiness.window.period_end,
            max_results=readiness.window.max_results,
            backend="local_sqlite",
            cache_status=readiness.status,
            serving_status=None,
            cache_readable=readiness.cache_readable,
            mature=readiness.mature,
            analysis_ready=readiness.analysis_ready,
            blocked_reason=readiness.blocked_reason,
        )


class HuldraArxivPoolBackend:
    def __init__(
        self,
        *,
        base_url: str,
        request_timeout_seconds: float = 30.0,
        client: Any | None = None,
        client_id: str = "recoleta",
    ) -> None:
        self.base_url = str(base_url or "").strip().rstrip("/")
        self.request_timeout_seconds = float(request_timeout_seconds)
        self.client_id = str(client_id or "recoleta").strip() or "recoleta"
        self._client = client

    @property
    def client(self) -> Any:
        if self._client is None:
            from huldra.client import HuldraClient

            self._client = HuldraClient(
                base_url=self.base_url,
                timeout=self.request_timeout_seconds,
            )
        return self._client

    def cached_papers_for_window(
        self,
        window: ArxivPoolWindow,
        *,
        readiness_policy: ArxivPoolReadinessPolicy,
    ) -> ArxivPoolWindowPullResult:
        normalized_window = _normalize_window(window)
        readiness, papers = self._request_window(
            normalized_window,
            readiness_policy=readiness_policy,
        )
        if readiness.analysis_ready:
            return ArxivPoolWindowPullResult(
                papers=papers,
                complete=True,
                readiness=readiness,
            )
        if readiness.blocked_reason == "immature_window":
            if readiness_policy.allows_immature_windows:
                return ArxivPoolWindowPullResult(
                    papers=papers,
                    complete=papers is not None,
                    readiness=readiness,
                )
            return ArxivPoolWindowPullResult(
                papers=None,
                complete=False,
                readiness=readiness,
            )
        return ArxivPoolWindowPullResult(
            papers=None,
            complete=False,
            readiness=readiness,
        )

    def evaluate_window_readiness(
        self,
        window: ArxivPoolWindow,
        *,
        readiness_policy: ArxivPoolReadinessPolicy,
    ) -> ArxivPoolBackendReadiness:
        readiness, _ = self._request_window(
            _normalize_window(window),
            readiness_policy=readiness_policy,
        )
        return readiness

    def _request_window(
        self,
        window: ArxivPoolWindow,
        *,
        readiness_policy: ArxivPoolReadinessPolicy,
    ) -> tuple[ArxivPoolBackendReadiness, list[ArxivPoolPaper] | None]:
        request = build_huldra_arxiv_request_for_window(
            window=window,
            readiness_policy=readiness_policy,
            client_id=self.client_id,
            timeout_seconds=self.request_timeout_seconds,
        )
        try:
            result = self.client.ensure(request)
        except Exception as exc:
            readiness = _failed_huldra_readiness(
                window=window,
                reason="huldra_unreachable",
                diagnostic={
                    "backend": "huldra",
                    "huldra_base_url": self.base_url,
                    "error_type": type(exc).__name__,
                    "error_message": str(exc),
                },
            )
            return readiness, None
        try:
            readiness = _huldra_result_readiness(window=window, result=result)
            papers = [_huldra_paper_to_pool_paper(paper) for paper in result.papers]
        except Exception as exc:
            readiness = _failed_huldra_readiness(
                window=window,
                reason="malformed_huldra_response",
                diagnostic={
                    "backend": "huldra",
                    "huldra_base_url": self.base_url,
                    "error_type": type(exc).__name__,
                    "error_message": str(exc),
                },
            )
            return readiness, None
        return readiness, papers if papers else []


class ArxivPoolTransientFetchError(ArxivPoolFetchError):
    pass


class ArxivPoolLeaseHeldError(RuntimeError):
    pass


class ArxivPoolFetcher(Protocol):
    def fetch(self, window: ArxivPoolWindow) -> list[ArxivPoolPaper]: ...


@dataclass(frozen=True, slots=True)
class ArxivPoolWorkerConfig:
    store: ArxivPoolStore
    queries: list[str]
    max_results: int
    request_interval_seconds: float
    cooldown_seconds: int
    poll_interval_seconds: int = 300
    lookback_days: int = 3
    idle_jitter_seconds: int = 30
    backfill_start: date | None = None
    backfill_end: date | None = None
    fetcher: ArxivPoolFetcher | None = None
    sleep: Callable[[float], None] = time.sleep
    sync_sleep: Callable[[float], None] | None = None
    now: Callable[[], datetime] | None = None
    event_sink: Callable[[dict[str, Any]], None] | None = None
    state_name: str = "default"
    failure_backoff_seconds: int = 60


@dataclass(frozen=True, slots=True)
class ArxivPoolWorkerPassRecord:
    planned_windows_total: int
    result: ArxivPoolSyncResult
    cooldown_until: datetime | None
    next_wake_at: datetime | None
    error_category: str | None = None
    error_message: str | None = None


@dataclass(frozen=True, slots=True)
class _WorkerPassCompletion:
    planned_windows_total: int
    result: ArxivPoolSyncResult
    delay_seconds: float
    cooldown_until: datetime | None
    event_name: str
    error_category: str | None = None
    error_message: str | None = None


_WORKER_PASS_RESULT_SQL = """
INSERT INTO arxiv_pool_worker_state (
    name, last_started_at, last_heartbeat_at, last_completed_at,
    last_planned_windows_total, last_completed_windows_total,
    last_cache_hit_total, last_failed_windows_total,
    last_cooldown_until, next_wake_at,
    last_error_category, last_error_message
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
ON CONFLICT(name) DO UPDATE SET
    last_heartbeat_at = excluded.last_heartbeat_at,
    last_completed_at = excluded.last_completed_at,
    last_planned_windows_total = excluded.last_planned_windows_total,
    last_completed_windows_total = excluded.last_completed_windows_total,
    last_cache_hit_total = excluded.last_cache_hit_total,
    last_failed_windows_total = excluded.last_failed_windows_total,
    last_cooldown_until = excluded.last_cooldown_until,
    next_wake_at = excluded.next_wake_at,
    last_error_category = excluded.last_error_category,
    last_error_message = excluded.last_error_message
"""


class ArxivApiFetcher:
    def __init__(
        self,
        *,
        client: httpx.Client | None = None,
        api_url: str = _ARXIV_API_URL,
        timeout_seconds: float = 30.0,
        user_agent: str = _ARXIV_POOL_USER_AGENT,
    ) -> None:
        self._client = client
        self._api_url = str(api_url)
        self._timeout_seconds = max(1.0, float(timeout_seconds))
        self._user_agent = str(user_agent or _ARXIV_POOL_USER_AGENT)

    def fetch(self, window: ArxivPoolWindow) -> list[ArxivPoolPaper]:
        response = self._request(window)
        status_code = int(response.status_code)
        if status_code == 429:
            raise ArxivPoolRateLimitedError(
                "arXiv API rate limited (HTTP 429)",
                retry_after_seconds=_retry_after_seconds_from_response(response),
            )
        if status_code >= 500:
            raise ArxivPoolTransientFetchError(
                f"arXiv API returned HTTP {status_code}",
                status_code=status_code,
            )
        if status_code < 200 or status_code >= 300:
            raise ArxivPoolFetchError(
                f"arXiv API returned HTTP {status_code}",
                status_code=status_code,
            )
        return _papers_from_arxiv_atom_feed(response.text)

    def _request(self, window: ArxivPoolWindow) -> httpx.Response:
        kwargs = {
            "params": _arxiv_api_query_params(window),
            "headers": {"User-Agent": self._user_agent},
            "timeout": self._timeout_seconds,
        }
        try:
            if self._client is not None:
                return self._client.get(self._api_url, **kwargs)
            with httpx.Client() as client:
                return client.get(self._api_url, **kwargs)
        except httpx.RequestError as exc:
            raise ArxivPoolTransientFetchError(
                f"arXiv API request failed: {type(exc).__name__}"
            ) from exc


def arxiv_pool_fetcher_name() -> str:
    return _ARXIV_POOL_FETCHER_NAME


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
        return (
            record is not None
            and record.status == "completed"
            and self.cached_papers_for_window(window) is not None
        )

    def is_window_cache_readable(
        self, window: ArxivPoolWindow | ArxivPoolWindowRecord
    ) -> bool:
        return (
            self.cached_papers_for_window(_window_from_record_or_window(window))
            is not None
        )

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
            window_row = self._window_cache_row(
                conn=conn,
                query_id=query_id,
                window=normalized_window,
            )
            if window_row is None or str(window_row["status"]) != "completed":
                return None
            rows = self._cached_paper_rows_for_window(
                conn=conn,
                query_id=query_id,
                window=normalized_window,
            ).fetchall()
            if len(rows) != int(window_row["result_count"] or 0):
                return None
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
                record=_WindowWrite(
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
                ),
            )
            self._set_rate_state(
                conn=conn,
                state=ArxivPoolRateState(
                    last_request_at=now,
                    cooldown_until=None,
                    consecutive_429_total=0,
                    last_status=upstream_status,
                    last_error_message=None,
                ),
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
            if self._window_has_readable_completed_cache(
                conn=conn,
                query_id=query_id,
                window=normalized_window,
            ):
                self._record_refresh_failure_for_cached_window(
                    conn=conn,
                    failure=_WindowRefreshFailure(
                        query_id=query_id,
                        window=normalized_window,
                        requested_at=now,
                        cooldown_until=cooldown_until,
                        upstream_status=upstream_status,
                        error_category="rate_limited",
                        error_message=error_message,
                    ),
                )
            else:
                self._upsert_window(
                    conn=conn,
                    record=_WindowWrite(
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
                    ),
                )
            self._set_rate_state(
                conn=conn,
                state=ArxivPoolRateState(
                    last_request_at=now,
                    cooldown_until=cooldown_until,
                    consecutive_429_total=(
                        int(previous.consecutive_429_total) + 1
                        if previous is not None
                        else 1
                    ),
                    last_status=upstream_status,
                    last_error_message=error_message,
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
            if self._window_has_readable_completed_cache(
                conn=conn,
                query_id=query_id,
                window=normalized_window,
            ):
                self._record_refresh_failure_for_cached_window(
                    conn=conn,
                    failure=_WindowRefreshFailure(
                        query_id=query_id,
                        window=normalized_window,
                        requested_at=now,
                        cooldown_until=None,
                        upstream_status=upstream_status,
                        error_category=error_category,
                        error_message=error_message,
                    ),
                )
            else:
                self._upsert_window(
                    conn=conn,
                    record=_WindowWrite(
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
                    ),
                )
            self._set_rate_state(
                conn=conn,
                state=ArxivPoolRateState(
                    last_request_at=now,
                    cooldown_until=None,
                    consecutive_429_total=0,
                    last_status=upstream_status,
                    last_error_message=error_message,
                ),
            )
            conn.commit()

    def get_rate_state(self) -> ArxivPoolRateState | None:
        self.init_schema()
        with self._connect() as conn:
            return self._rate_state(conn=conn)

    def record_worker_started(self, *, name: str = "default") -> ArxivPoolWorkerState:
        self.init_schema()
        normalized_name = _normalize_worker_name(name)
        now = _utc_now()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO arxiv_pool_worker_state (
                    name, last_started_at, last_heartbeat_at,
                    last_planned_windows_total, last_completed_windows_total,
                    last_cache_hit_total, last_failed_windows_total
                )
                VALUES (?, ?, ?, 0, 0, 0, 0)
                ON CONFLICT(name) DO UPDATE SET
                    last_started_at = excluded.last_started_at,
                    last_heartbeat_at = excluded.last_heartbeat_at,
                    next_wake_at = NULL,
                    last_error_category = NULL,
                    last_error_message = NULL
                """,
                (
                    normalized_name,
                    _datetime_to_text(now),
                    _datetime_to_text(now),
                ),
            )
            conn.commit()
        return self.get_worker_state(name=normalized_name) or ArxivPoolWorkerState(
            name=normalized_name,
            last_started_at=now,
            last_heartbeat_at=now,
            last_completed_at=None,
            last_planned_windows_total=0,
            last_completed_windows_total=0,
            last_cache_hit_total=0,
            last_failed_windows_total=0,
            last_cooldown_until=None,
            next_wake_at=None,
            last_error_category=None,
            last_error_message=None,
        )

    def record_worker_heartbeat(
        self,
        *,
        name: str = "default",
        planned_windows_total: int | None = None,
    ) -> ArxivPoolWorkerState:
        self.init_schema()
        normalized_name = _normalize_worker_name(name)
        now = _utc_now()
        with self._connect() as conn:
            if planned_windows_total is None:
                conn.execute(
                    """
                    INSERT INTO arxiv_pool_worker_state (
                        name, last_started_at, last_heartbeat_at
                    )
                    VALUES (?, ?, ?)
                    ON CONFLICT(name) DO UPDATE SET
                        last_heartbeat_at = excluded.last_heartbeat_at
                    """,
                    (
                        normalized_name,
                        _datetime_to_text(now),
                        _datetime_to_text(now),
                    ),
                )
            else:
                conn.execute(
                    """
                    INSERT INTO arxiv_pool_worker_state (
                        name, last_started_at, last_heartbeat_at,
                        last_planned_windows_total
                    )
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(name) DO UPDATE SET
                        last_heartbeat_at = excluded.last_heartbeat_at,
                        last_planned_windows_total = excluded.last_planned_windows_total
                    """,
                    (
                        normalized_name,
                        _datetime_to_text(now),
                        _datetime_to_text(now),
                        max(0, int(planned_windows_total)),
                    ),
                )
            conn.commit()
        return self.get_worker_state(name=normalized_name) or ArxivPoolWorkerState(
            name=normalized_name,
            last_started_at=now,
            last_heartbeat_at=now,
            last_completed_at=None,
            last_planned_windows_total=max(0, int(planned_windows_total or 0)),
            last_completed_windows_total=0,
            last_cache_hit_total=0,
            last_failed_windows_total=0,
            last_cooldown_until=None,
            next_wake_at=None,
            last_error_category=None,
            last_error_message=None,
        )

    def record_worker_pass_result(
        self,
        *,
        name: str = "default",
        pass_record: ArxivPoolWorkerPassRecord | None = None,
        **raw_pass_record: Any,
    ) -> ArxivPoolWorkerState:
        self.init_schema()
        normalized_name = _normalize_worker_name(name)
        now = _utc_now()
        record = _coerce_worker_pass_record(pass_record, raw_pass_record)
        with self._connect() as conn:
            conn.execute(
                _WORKER_PASS_RESULT_SQL,
                _worker_pass_record_params(
                    name=normalized_name,
                    completed_at=now,
                    record=record,
                ),
            )
            conn.commit()
        return self.get_worker_state(name=normalized_name) or _worker_state_from_pass_record(
            name=normalized_name,
            completed_at=now,
            record=record,
        )

    def get_worker_state(
        self, *, name: str = "default"
    ) -> ArxivPoolWorkerState | None:
        self.init_schema()
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT name, last_started_at, last_heartbeat_at, last_completed_at,
                       last_planned_windows_total, last_completed_windows_total,
                       last_cache_hit_total, last_failed_windows_total,
                       last_cooldown_until, next_wake_at,
                       last_error_category, last_error_message
                FROM arxiv_pool_worker_state
                WHERE name = ?
                """,
                (_normalize_worker_name(name),),
            ).fetchone()
        return _worker_state_from_row(row) if row is not None else None

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
            conn.execute(
                """
                UPDATE arxiv_query_windows
                SET status = 'pruned',
                    completed_at = NULL,
                    result_count = 0,
                    error_category = 'pruned',
                    error_message = 'query matches pruned by arxiv pool gc'
                WHERE status = 'completed'
                  AND result_count > 0
                  AND period_end < ?
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
        conn.row_factory = sqlite3.Row  # noqa: V101 - sqlite uses this runtime hook.
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

    def _window_cache_row(
        self,
        *,
        conn: sqlite3.Connection,
        query_id: int,
        window: ArxivPoolWindow,
    ) -> sqlite3.Row | None:
        return conn.execute(
            """
            SELECT status, result_count
            FROM arxiv_query_windows
            WHERE query_id = ?
              AND period_start = ?
              AND period_end = ?
              AND max_results = ?
            """,
            (
                query_id,
                _datetime_to_text(window.period_start),
                _datetime_to_text(window.period_end),
                window.max_results,
            ),
        ).fetchone()

    def _cached_paper_rows_for_window(
        self,
        *,
        conn: sqlite3.Connection,
        query_id: int,
        window: ArxivPoolWindow,
    ) -> sqlite3.Cursor:
        return conn.execute(
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
                _datetime_to_text(window.period_start),
                _datetime_to_text(window.period_end),
                window.max_results,
            ),
        )

    def _window_has_readable_completed_cache(
        self,
        *,
        conn: sqlite3.Connection,
        query_id: int,
        window: ArxivPoolWindow,
    ) -> bool:
        window_row = self._window_cache_row(
            conn=conn,
            query_id=query_id,
            window=window,
        )
        if window_row is None or str(window_row["status"]) != "completed":
            return False
        rows = self._cached_paper_rows_for_window(
            conn=conn,
            query_id=query_id,
            window=window,
        ).fetchall()
        return len(rows) == int(window_row["result_count"] or 0)

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
        record: _WindowWrite,
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
                record.query_id,
                _datetime_to_text(record.window.period_start),
                _datetime_to_text(record.window.period_end),
                int(record.window.max_results),
                record.status,
                _datetime_to_text(record.requested_at),
                _datetime_to_text(record.completed_at),
                _datetime_to_text(record.cooldown_until),
                int(record.upstream_requests_total),
                record.upstream_status,
                record.error_category,
                _truncate_error(record.error_message),
                int(record.result_count),
            ),
        )

    def _record_refresh_failure_for_cached_window(
        self,
        *,
        conn: sqlite3.Connection,
        failure: _WindowRefreshFailure,
    ) -> None:
        conn.execute(
            """
            UPDATE arxiv_query_windows
            SET requested_at = ?,
                cooldown_until = ?,
                upstream_requests_total = upstream_requests_total + 1,
                upstream_status = ?,
                error_category = ?,
                error_message = ?
            WHERE query_id = ?
              AND period_start = ?
              AND period_end = ?
              AND max_results = ?
              AND status = 'completed'
            """,
            (
                _datetime_to_text(failure.requested_at),
                _datetime_to_text(failure.cooldown_until),
                failure.upstream_status,
                failure.error_category,
                _truncate_error(failure.error_message),
                failure.query_id,
                _datetime_to_text(failure.window.period_start),
                _datetime_to_text(failure.window.period_end),
                failure.window.max_results,
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
        state: ArxivPoolRateState,
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
                _datetime_to_text(state.last_request_at),
                _datetime_to_text(state.cooldown_until),
                int(state.consecutive_429_total),
                state.last_status,
                _truncate_error(state.last_error_message),
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
        refresh_windows: Iterable[ArxivPoolWindow] | None = None,
    ) -> ArxivPoolSyncResult:
        self.store.init_schema()
        refresh_window_keys = (
            {_window_cache_key(window) for window in refresh_windows}
            if refresh_windows is not None
            else set()
        )
        owner_token = uuid4().hex
        self.store.acquire_sync_lease(
            owner_token=owner_token,
            timeout_seconds=self._lease_timeout_seconds(windows),
        )
        try:
            return self._sync_windows_locked(
                windows=windows,
                force=force,
                refresh_window_keys=refresh_window_keys,
            )
        finally:
            self.store.release_sync_lease(owner_token=owner_token)

    def _sync_windows_locked(
        self,
        *,
        windows: list[ArxivPoolWindow],
        force: bool,
        refresh_window_keys: set[tuple[str, str, str, int]],
    ) -> ArxivPoolSyncResult:
        result = ArxivPoolSyncResult(requested_windows_total=len(windows))
        for window in [_normalize_window(candidate) for candidate in windows]:
            should_refresh = force or _window_cache_key(window) in refresh_window_keys
            if not should_refresh and self.store.is_window_completed(window):
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
                result.retry_after_seconds = exc.retry_after_seconds
                result.rate_limited_windows_total += 1
                retry_after_seconds = (
                    exc.retry_after_seconds
                    if exc.retry_after_seconds is not None
                    else self.cooldown_seconds
                )
                cooldown_until = _utc_now() + timedelta(
                    seconds=retry_after_seconds
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


class ArxivPoolWorker:
    def __init__(
        self,
        config: ArxivPoolWorkerConfig | None = None,
        **raw_config: Any,
    ) -> None:
        worker_config = _coerce_worker_config(config, raw_config)
        self.store = worker_config.store
        self.queries = list(worker_config.queries)
        self.max_results = max(1, int(worker_config.max_results))
        self.request_interval_seconds = max(
            0.0, float(worker_config.request_interval_seconds)
        )
        self.cooldown_seconds = max(1, int(worker_config.cooldown_seconds))
        self.poll_interval_seconds = max(1, int(worker_config.poll_interval_seconds))
        self.lookback_days = max(1, int(worker_config.lookback_days))
        self.idle_jitter_seconds = max(0, int(worker_config.idle_jitter_seconds))
        self.backfill_start = worker_config.backfill_start
        self.backfill_end = worker_config.backfill_end
        self.fetcher = worker_config.fetcher
        self.sleep = worker_config.sleep
        self.sync_sleep = worker_config.sync_sleep or time.sleep
        self.now = worker_config.now or _utc_now
        self.event_sink = worker_config.event_sink
        self.state_name = _normalize_worker_name(worker_config.state_name)
        self.failure_backoff_seconds = max(
            1, int(worker_config.failure_backoff_seconds)
        )
        self._failure_streak = 0
        self._log = logger.bind(module="arxiv_pool.worker", worker=self.state_name)

    def run(self, *, max_passes: int | None = None) -> None:
        self.store.record_worker_started(name=self.state_name)
        self._emit_event("worker_start", pool_db_path=str(self.store.db_path))
        passes_completed = 0
        stop_reason = "completed"
        try:
            while True:
                pass_result = self.run_once()
                passes_completed += 1
                if max_passes is not None and passes_completed >= max_passes:
                    break
                self.sleep(pass_result.next_sleep_seconds)
        except KeyboardInterrupt:
            stop_reason = "interrupted"
            raise
        finally:
            self.store.record_worker_heartbeat(name=self.state_name)
            self._emit_event("worker_stop", reason=stop_reason)

    def run_once(self) -> ArxivPoolWorkerPassResult:
        reference = self._now()
        planned_windows = self.plan_windows(now=reference)
        refresh_windows = self.plan_refresh_windows(now=reference)
        planned_total = len(planned_windows)
        self.store.record_worker_heartbeat(
            name=self.state_name,
            planned_windows_total=planned_total,
        )
        self._emit_event("heartbeat")
        self._emit_event("planned_windows", planned_windows_total=planned_total)

        active_cooldown_until = self._active_cooldown_until()
        if active_cooldown_until is not None:
            result = ArxivPoolSyncResult(
                requested_windows_total=planned_total,
                cooldown_active_total=planned_total,
                skipped_windows_total=planned_total,
            )
            return self._finish_pass(
                planned_windows_total=planned_total,
                result=result,
                delay_seconds=self._cooldown_delay_seconds(active_cooldown_until),
                cooldown_until=active_cooldown_until,
                event_name="cooldown_active",
            )

        try:
            result = self._sync().sync_windows(
                planned_windows,
                refresh_windows=refresh_windows,
            )
        except ArxivPoolLeaseHeldError as exc:
            result = ArxivPoolSyncResult(
                requested_windows_total=planned_total,
                skipped_windows_total=planned_total,
                failed_windows_total=planned_total,
            )
            return self._finish_pass(
                planned_windows_total=planned_total,
                result=result,
                delay_seconds=self._failure_delay_seconds(),
                cooldown_until=self._cooldown_until(),
                error_category=type(exc).__name__,
                error_message=str(exc),
                event_name="transient_failure",
            )

        cooldown_until = self._cooldown_until()
        if result.upstream_429_total > 0 or result.rate_limited_windows_total > 0:
            return self._finish_pass(
                planned_windows_total=planned_total,
                result=result,
                delay_seconds=self._cooldown_delay_seconds(cooldown_until),
                cooldown_until=cooldown_until,
                error_category="rate_limited",
                error_message="arXiv pool sync entered cooldown",
                event_name="cooldown_active",
            )
        if result.failed_windows_total > 0:
            return self._finish_pass(
                planned_windows_total=planned_total,
                result=result,
                delay_seconds=self._failure_delay_seconds(),
                cooldown_until=cooldown_until,
                error_category="transient_failure",
                error_message=(
                    f"{result.failed_windows_total} arXiv pool window(s) "
                    "failed during sync"
                ),
                event_name="transient_failure",
            )

        self._failure_streak = 0
        return self._finish_pass(
            planned_windows_total=planned_total,
            result=result,
            delay_seconds=self._poll_delay_seconds(),
            cooldown_until=cooldown_until,
            event_name="sync_pass_result",
        )

    def plan_windows(self, *, now: datetime | None = None) -> list[ArxivPoolWindow]:
        reference = _ensure_utc(now or self.now())
        return build_arxiv_pool_worker_windows(
            queries=self.queries,
            max_results=self.max_results,
            now=reference,
            lookback_days=self.lookback_days,
            backfill_start=self.backfill_start,
            backfill_end=self.backfill_end,
        )

    def plan_refresh_windows(
        self, *, now: datetime | None = None
    ) -> list[ArxivPoolWindow]:
        reference = _ensure_utc(now or self.now())
        return build_arxiv_pool_windows(
            queries=self.queries,
            anchor_date=reference.date(),
            lookback_days=self.lookback_days,
            max_results=self.max_results,
        )

    def _sync(self) -> ArxivPoolSync:
        return ArxivPoolSync(
            store=self.store,
            fetcher=self.fetcher,
            request_interval_seconds=self.request_interval_seconds,
            cooldown_seconds=self.cooldown_seconds,
            sleep=self.sync_sleep,
        )

    def _finish_pass(
        self,
        completion: _WorkerPassCompletion | None = None,
        **raw_completion: Any,
    ) -> ArxivPoolWorkerPassResult:
        pass_completion = _coerce_worker_pass_completion(completion, raw_completion)
        next_wake_at = self._next_wake_at(pass_completion.delay_seconds)
        state = self.store.record_worker_pass_result(
            name=self.state_name,
            pass_record=ArxivPoolWorkerPassRecord(
                planned_windows_total=pass_completion.planned_windows_total,
                result=pass_completion.result,
                cooldown_until=pass_completion.cooldown_until,
                next_wake_at=next_wake_at,
                error_category=pass_completion.error_category,
                error_message=pass_completion.error_message,
            ),
        )
        self._emit_event(
            pass_completion.event_name,
            sync=pass_completion.result.as_payload(),
            worker_state=worker_state_payload(state),
            cooldown_until=_isoformat_or_none(pass_completion.cooldown_until),
            next_wake_at=next_wake_at.isoformat(),
            sleep_seconds=pass_completion.delay_seconds,
            error_category=pass_completion.error_category,
            error_message=pass_completion.error_message,
        )
        self._emit_event(
            "next_wake_time",
            next_wake_at=next_wake_at.isoformat(),
            sleep_seconds=pass_completion.delay_seconds,
        )
        return ArxivPoolWorkerPassResult(
            planned_windows_total=pass_completion.planned_windows_total,
            sync=pass_completion.result,
            next_wake_at=next_wake_at,
            next_sleep_seconds=pass_completion.delay_seconds,
            cooldown_until=pass_completion.cooldown_until,
            error_category=pass_completion.error_category,
            error_message=pass_completion.error_message,
        )

    def _active_cooldown_until(self) -> datetime | None:
        cooldown_until = self._cooldown_until()
        if cooldown_until is None:
            return None
        return cooldown_until if cooldown_until > self._now() else None

    def _cooldown_until(self) -> datetime | None:
        state = self.store.get_rate_state()
        return getattr(state, "cooldown_until", None)

    def _cooldown_delay_seconds(self, cooldown_until: datetime | None) -> float:
        if cooldown_until is None:
            return self._failure_delay_seconds()
        delay = max(0.0, (cooldown_until - self._now()).total_seconds())
        return delay + self._jitter_seconds()

    def _failure_delay_seconds(self) -> float:
        self._failure_streak += 1
        exponential = self.failure_backoff_seconds * (2 ** (self._failure_streak - 1))
        capped = min(float(self.poll_interval_seconds), float(exponential))
        return max(1.0, capped) + self._jitter_seconds()

    def _poll_delay_seconds(self) -> float:
        return float(self.poll_interval_seconds) + self._jitter_seconds()

    def _jitter_seconds(self) -> float:
        if self.idle_jitter_seconds <= 0:
            return 0.0
        return random.uniform(0.0, float(self.idle_jitter_seconds))

    def _next_wake_at(self, delay_seconds: float) -> datetime:
        return self._now() + timedelta(seconds=max(0.0, float(delay_seconds)))

    def _now(self) -> datetime:
        return _ensure_utc(self.now())

    def _emit_event(self, event: str, **payload: Any) -> None:
        event_payload: dict[str, Any] = {
            "event": event,
            "worker": self.state_name,
            "timestamp": self._now().isoformat(),
            **{key: value for key, value in payload.items() if value is not None},
        }
        self._log.bind(event=event).info("arXiv pool worker event")
        if self.event_sink is not None:
            self.event_sink(event_payload)


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


def build_arxiv_pool_worker_windows(
    *,
    queries: list[str],
    max_results: int,
    now: datetime | None = None,
    lookback_days: int = 3,
    backfill_start: date | None = None,
    backfill_end: date | None = None,
) -> list[ArxivPoolWindow]:
    reference = _ensure_utc(now or _utc_now())
    windows = build_arxiv_pool_windows(
        queries=queries,
        anchor_date=reference.date(),
        lookback_days=lookback_days,
        max_results=max_results,
    )
    if backfill_start is not None or backfill_end is not None:
        if backfill_start is None or backfill_end is None:
            raise ValueError("backfill_start and backfill_end must be provided together")
        if backfill_end < backfill_start:
            raise ValueError("backfill_end must be on or after backfill_start")
        days: list[date] = []
        cursor = backfill_start
        while cursor <= backfill_end:
            days.append(cursor)
            cursor += timedelta(days=1)
        windows.extend(
            build_arxiv_pool_windows_for_days(
                queries=queries,
                days=days,
                max_results=max_results,
            )
        )
    return _dedupe_windows(windows)


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


def _dedupe_windows(windows: list[ArxivPoolWindow]) -> list[ArxivPoolWindow]:
    deduped: dict[tuple[str, str, str, int], ArxivPoolWindow] = {}
    for window in (_normalize_window(candidate) for candidate in windows):
        deduped[_window_cache_key(window)] = window
    return list(deduped.values())


def _window_cache_key(window: ArxivPoolWindow) -> tuple[str, str, str, int]:
    normalized = _normalize_window(window)
    return (
        normalized.query_text,
        _datetime_to_text(normalized.period_start) or "",
        _datetime_to_text(normalized.period_end) or "",
        int(normalized.max_results),
    )


def pool_paper_to_item_draft(
    *,
    paper: ArxivPoolPaper,
    window: ArxivPoolWindow,
    extra_raw_metadata: Mapping[str, Any] | None = None,
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
    if normalized.journal_ref:
        raw_metadata["journal_ref"] = normalized.journal_ref
    if normalized.doi:
        raw_metadata["doi"] = normalized.doi
    if extra_raw_metadata:
        raw_metadata.update(dict(extra_raw_metadata))
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
        raw = urlparse(raw).path.strip("/")
    for prefix in ("arXiv:", "arxiv:", "abs/", "pdf/", "html/"):
        if raw.startswith(prefix):
            raw = raw[len(prefix) :]
    if raw.endswith(".pdf"):
        raw = raw[:-4]
    normalized = raw.strip().strip("/")
    if not normalized:
        raise ValueError("arxiv_id must not be empty")
    return normalized


def worker_state_payload(state: ArxivPoolWorkerState | None) -> dict[str, Any] | None:
    if state is None:
        return None
    return {
        "name": state.name,
        "last_started_at": _isoformat_or_none(state.last_started_at),
        "last_heartbeat_at": _isoformat_or_none(state.last_heartbeat_at),
        "last_completed_at": _isoformat_or_none(state.last_completed_at),
        "last_planned_windows_total": state.last_planned_windows_total,
        "last_completed_windows_total": state.last_completed_windows_total,
        "last_cache_hit_total": state.last_cache_hit_total,
        "last_failed_windows_total": state.last_failed_windows_total,
        "last_cooldown_until": _isoformat_or_none(state.last_cooldown_until),
        "next_wake_at": _isoformat_or_none(state.next_wake_at),
        "last_error_category": state.last_error_category,
        "last_error_message": state.last_error_message,
    }


def _clean_text(value: Any) -> str:
    return str(value or "").strip()


def _optional_text(value: Any) -> str | None:
    text = _clean_text(value)
    return text if text else None


def _clean_text_list(values: Iterable[Any] | None) -> list[str]:
    if values is None:
        return []
    cleaned: list[str] = []
    for value in values:
        text = _clean_text(value)
        if text:
            cleaned.append(text)
    return cleaned


def _paper_version(*, paper: ArxivPoolPaper, arxiv_id: str) -> int | None:
    if paper.version is not None:
        return paper.version
    return _version_from_id(arxiv_id)


def _paper_canonical_url(value: Any, *, arxiv_id: str) -> str:
    url = _clean_text(value)
    if url:
        return url
    return f"https://arxiv.org/abs/{arxiv_id}"


def normalize_pool_paper(paper: ArxivPoolPaper) -> ArxivPoolPaper:
    arxiv_id = normalize_arxiv_id(paper.arxiv_id)
    title = _clean_text(paper.title)
    if not title:
        raise ValueError("arxiv pool paper title must not be empty")
    return ArxivPoolPaper(
        arxiv_id=arxiv_id,
        version=_paper_version(paper=paper, arxiv_id=arxiv_id),
        canonical_url=_paper_canonical_url(paper.canonical_url, arxiv_id=arxiv_id),
        title=title,
        abstract=_optional_text(paper.abstract),
        authors=_clean_text_list(paper.authors),
        primary_category=_optional_text(paper.primary_category),
        categories=_clean_text_list(paper.categories),
        published_at=_ensure_utc_optional(paper.published_at),
        updated_at=_ensure_utc_optional(paper.updated_at),
        comment=_optional_text(paper.comment),
        journal_ref=_optional_text(paper.journal_ref),
        doi=_optional_text(paper.doi),
        raw_atom=dict(paper.raw_atom or {}),
    )


def resolve_arxiv_pool_db_path(settings: Any) -> Path:
    pool = getattr(settings, "arxiv_pool", None)
    db_path = getattr(pool, "db_path", None)
    if db_path is None:
        raise ValueError("ARXIV_POOL.db_path is required when arXiv pool mode is used")
    return Path(db_path).expanduser().resolve()


def arxiv_pool_readiness_policy_from_settings(
    settings: Any,
    *,
    now: datetime | None = None,
) -> ArxivPoolReadinessPolicy:
    pool = getattr(settings, "arxiv_pool", settings)
    return ArxivPoolReadinessPolicy(
        maturity_lag_days=int(getattr(pool, "maturity_lag_days", 1) or 0),
        readiness_gate=str(getattr(pool, "readiness_gate", "strict") or "strict"),
        allow_immature_windows=bool(
            getattr(pool, "allow_immature_windows", False)
        ),
        now=now,
    )


def arxiv_pool_backend_descriptor_from_settings(
    settings: Any,
) -> ArxivPoolBackendDescriptor:
    pool = getattr(settings, "arxiv_pool", settings)
    backend = str(getattr(pool, "backend", "local_sqlite") or "local_sqlite").lower()
    if backend == "huldra":
        base_url = _normalize_huldra_base_url(getattr(pool, "huldra_base_url", None))
        if not base_url:
            raise ValueError(
                "ARXIV_POOL.huldra_base_url is required when backend=huldra"
            )
        return ArxivPoolBackendDescriptor(kind="huldra", identity=base_url)
    return ArxivPoolBackendDescriptor(
        kind="local_sqlite",
        identity=str(resolve_arxiv_pool_db_path(settings)),
    )


def build_arxiv_pool_backend_from_settings(settings: Any) -> ArxivMetadataPoolBackend:
    pool = getattr(settings, "arxiv_pool", settings)
    descriptor = arxiv_pool_backend_descriptor_from_settings(settings)
    if descriptor.kind == "huldra":
        return HuldraArxivPoolBackend(
            base_url=descriptor.identity,
            request_timeout_seconds=float(
                getattr(pool, "huldra_request_timeout_seconds", 30.0) or 30.0
            ),
        )
    return LocalSqliteArxivPoolBackend(ArxivPoolStore(Path(descriptor.identity)))


def build_huldra_arxiv_request_for_window(
    *,
    window: ArxivPoolWindow,
    readiness_policy: ArxivPoolReadinessPolicy,
    client_id: str,
    timeout_seconds: float,
) -> Any:
    from huldra.models import ArxivRequest, CachePolicy, ReadinessMode

    normalized_window = _normalize_window(window)
    readiness = (
        ReadinessMode.RAW_COMPLETED
        if readiness_policy.allows_immature_windows
        else ReadinessMode.ANALYSIS_READY
    )
    return ArxivRequest(
        client_id=client_id,
        search_query=normalized_window.query_text,
        sort_by="submittedDate",
        sort_order="descending",
        start=0,
        max_results=normalized_window.max_results,
        submitted_start=normalized_window.period_start,
        submitted_end=normalized_window.period_end,
        cache_policy=CachePolicy.CACHE_ONLY,
        readiness=readiness,
        maturity_lag_days=readiness_policy.maturity_lag_days,
        timeout_seconds=float(timeout_seconds),
    )


def huldra_wait_timeout_seconds(
    *,
    configured_timeout_seconds: float | None,
    requested_windows_total: int,
) -> float:
    if configured_timeout_seconds is not None:
        return float(configured_timeout_seconds)
    return float(max(3600, int(requested_windows_total) * 35))


def arxiv_pool_sync_result_from_huldra(result: Any) -> ArxivPoolSyncResult:
    return ArxivPoolSyncResult(
        requested_windows_total=int(getattr(result, "requested_total", 0) or 0),
        completed_windows_total=int(
            getattr(result, "completed_windows_total", 0) or 0
        ),
        cache_hit_total=int(getattr(result, "cache_hit_total", 0) or 0),
        cache_miss_total=int(getattr(result, "cache_miss_total", 0) or 0),
        upstream_requests_total=int(
            getattr(result, "upstream_requests_total", 0) or 0
        ),
        upstream_429_total=int(getattr(result, "upstream_429_total", 0) or 0),
        retry_after_seconds=getattr(result, "retry_after_seconds", None),
        cooldown_active_total=int(getattr(result, "cooldown_active_total", 0) or 0),
        skipped_windows_total=int(getattr(result, "skipped_windows_total", 0) or 0),
        rate_limited_windows_total=int(
            getattr(result, "rate_limited_windows_total", 0) or 0
        ),
        failed_windows_total=int(getattr(result, "failed_windows_total", 0) or 0),
        papers_total=int(getattr(result, "papers_total", 0) or 0),
    )


def evaluate_arxiv_pool_window_readiness(
    *,
    store: ArxivPoolStore,
    window: ArxivPoolWindow,
    policy: ArxivPoolReadinessPolicy,
) -> ArxivPoolWindowReadiness:
    normalized_window = _normalize_window(window)
    record = store.get_window(normalized_window)
    cache_readable = (
        record is not None
        and record.status == "completed"
        and store.is_window_cache_readable(normalized_window)
    )
    mature = policy.is_mature(normalized_window)
    analysis_ready = bool(cache_readable and mature)
    blocked_reason = _arxiv_pool_blocked_reason(
        record=record,
        cache_readable=cache_readable,
        mature=mature,
    )
    return ArxivPoolWindowReadiness(
        window=normalized_window,
        record=record,
        cache_readable=cache_readable,
        mature=mature,
        analysis_ready=analysis_ready,
        blocked_reason=blocked_reason,
    )


def evaluate_arxiv_pool_readiness(
    *,
    store: ArxivPoolStore | None = None,
    backend: ArxivMetadataPoolBackend | None = None,
    windows: list[ArxivPoolWindow],
    policy: ArxivPoolReadinessPolicy,
) -> dict[str, Any]:
    resolved_backend = backend
    if resolved_backend is None:
        if store is None:
            raise ValueError("store or backend is required")
        resolved_backend = LocalSqliteArxivPoolBackend(store)
    window_readiness = [
        resolved_backend.evaluate_window_readiness(
            window=window,
            readiness_policy=policy,
        )
        for window in windows
    ]
    immature_windows = [
        readiness
        for readiness in window_readiness
        if readiness.blocked_reason == "immature_window"
    ]
    unavailable_windows = [
        readiness for readiness in window_readiness if readiness.unavailable
    ]
    unsafe_override_total = (
        len(immature_windows) if policy.allows_immature_windows else 0
    )
    blocked_windows_total = len(unavailable_windows) + (
        0 if policy.allows_immature_windows else len(immature_windows)
    )
    if policy.readiness_gate == "off":
        status = "disabled"
    elif blocked_windows_total > 0:
        status = "blocked"
    else:
        status = "ready"
    return {
        "status": status,
        "windows_total": len(window_readiness),
        "analysis_ready_windows_total": sum(
            1 for readiness in window_readiness if readiness.analysis_ready
        ),
        "blocked_windows_total": blocked_windows_total,
        "immature_windows_total": len(immature_windows),
        "unavailable_windows_total": len(unavailable_windows),
        "unsafe_override_windows_total": unsafe_override_total,
        "maturity_policy": policy.as_payload(),
        "windows": [readiness.as_payload() for readiness in window_readiness],
    }


def _normalize_window(window: ArxivPoolWindow) -> ArxivPoolWindow:
    return ArxivPoolWindow(
        query_text=normalize_arxiv_query(window.query_text),
        period_start=_ensure_utc(window.period_start),
        period_end=_ensure_utc(window.period_end),
        max_results=max(1, int(window.max_results)),
    )


def _window_from_record_or_window(
    value: ArxivPoolWindow | ArxivPoolWindowRecord,
) -> ArxivPoolWindow:
    return ArxivPoolWindow(
        query_text=value.query_text,
        period_start=value.period_start,
        period_end=value.period_end,
        max_results=value.max_results,
    )


def _arxiv_pool_blocked_reason(
    *,
    record: ArxivPoolWindowRecord | None,
    cache_readable: bool,
    mature: bool,
) -> str | None:
    if record is None:
        return "missing_window"
    if not cache_readable:
        status = str(record.status or "").strip().lower()
        if status in {"rate_limited", "failed"}:
            return f"{status}_window"
        if status == "completed":
            return "incomplete_cache"
        return f"{status or 'unavailable'}_window"
    if not mature:
        return "immature_window"
    return None


def _normalize_huldra_base_url(value: Any) -> str | None:
    normalized = str(value or "").strip()
    return normalized.rstrip("/") if normalized else None


def _failed_huldra_readiness(
    *,
    window: ArxivPoolWindow,
    reason: str,
    diagnostic: dict[str, Any],
) -> ArxivPoolBackendReadiness:
    normalized_window = _normalize_window(window)
    return ArxivPoolBackendReadiness(
        query_text=normalized_window.query_text,
        period_start=normalized_window.period_start,
        period_end=normalized_window.period_end,
        max_results=normalized_window.max_results,
        backend="huldra",
        cache_status="failed",
        serving_status=None,
        cache_readable=False,
        mature=False,
        analysis_ready=False,
        blocked_reason=reason,
        diagnostic=diagnostic,
    )


def _huldra_result_readiness(
    *,
    window: ArxivPoolWindow,
    result: Any,
) -> ArxivPoolBackendReadiness:
    normalized_window = _normalize_window(window)
    status = _clean_text(getattr(result, "status", "")).lower()
    cache_readable = bool(getattr(result, "cache_readable", False))
    mature = bool(getattr(result, "mature", False))
    analysis_ready = bool(getattr(result, "analysis_ready", False))
    cache_key = _optional_text(getattr(result, "cache_key", None))
    blocked_reason = _huldra_blocked_reason(
        status=status,
        cache_readable=cache_readable,
        mature=mature,
        analysis_ready=analysis_ready,
        raw_blocked_reason=_optional_text(getattr(result, "blocked_reason", None)),
    )
    diagnostic = {
        key: value
        for key, value in {
            "backend": "huldra",
            "huldra_status": status or None,
            "huldra_cache_key": cache_key,
            "huldra_serving_mode": _optional_text(
                getattr(result, "serving_mode", None)
            ),
            "stale": bool(getattr(result, "stale", False)),
            "error_category": _optional_text(getattr(result, "error_category", None)),
            "error_message": _optional_text(getattr(result, "error_message", None)),
        }.items()
        if value is not None
    }
    return ArxivPoolBackendReadiness(
        query_text=normalized_window.query_text,
        period_start=normalized_window.period_start,
        period_end=normalized_window.period_end,
        max_results=normalized_window.max_results,
        backend="huldra",
        cache_status=_huldra_cache_status(
            status=status,
            cache_readable=cache_readable,
        ),
        serving_status=status or None,
        cache_readable=cache_readable,
        mature=mature,
        analysis_ready=analysis_ready,
        blocked_reason=blocked_reason,
        cache_key=cache_key,
        diagnostic=diagnostic,
    )


def _huldra_cache_status(*, status: str, cache_readable: bool) -> str:
    if cache_readable:
        return "completed"
    return {
        "ready": "completed",
        "immature": "completed",
        "cache_miss": "missing",
        "queued": "queued",
        "cooling_down": "rate_limited",
        "rate_limited": "rate_limited",
        "failed": "failed",
        "timeout": "timeout",
        "skipped": "skipped",
    }.get(status, "failed")


def _huldra_blocked_reason(
    *,
    status: str,
    cache_readable: bool,
    mature: bool,
    analysis_ready: bool,
    raw_blocked_reason: str | None,
) -> str | None:
    if analysis_ready:
        return None
    if cache_readable and (status == "immature" or not mature):
        return "immature_window"
    if raw_blocked_reason == "immature_window":
        return "immature_window"
    mapped = {
        "cache_miss": "missing_window",
        "queued": "queued_window",
        "cooling_down": "rate_limited_window",
        "rate_limited": "rate_limited_window",
        "failed": "failed_window",
        "timeout": "timeout_window",
        "skipped": "skipped_window",
    }.get(status)
    if mapped is not None:
        return mapped
    if raw_blocked_reason in {"cache_miss", "missing"}:
        return "missing_window"
    if raw_blocked_reason == "cooldown":
        return "rate_limited_window"
    if raw_blocked_reason:
        return raw_blocked_reason
    return "unavailable_window"


def _huldra_paper_to_pool_paper(paper: Any) -> ArxivPoolPaper:
    return ArxivPoolPaper(
        arxiv_id=str(getattr(paper, "arxiv_id")),
        version=getattr(paper, "version", None),
        canonical_url=str(getattr(paper, "canonical_url")),
        title=str(getattr(paper, "title")),
        abstract=getattr(paper, "abstract", None),
        authors=list(getattr(paper, "authors", []) or []),
        primary_category=getattr(paper, "primary_category", None),
        categories=list(getattr(paper, "categories", []) or []),
        published_at=getattr(paper, "published_at", None),
        updated_at=getattr(paper, "updated_at", None),
        comment=getattr(paper, "comment", None),
        journal_ref=getattr(paper, "journal_ref", None),
        doi=getattr(paper, "doi", None),
        raw_atom=dict(getattr(paper, "raw_atom", {}) or {}),
    )


def _normalize_readiness_gate(value: Any) -> str:
    normalized = str(value or "").strip().lower()
    if not normalized:
        return "strict"
    if normalized not in _ARXIV_POOL_READINESS_GATES:
        raise ValueError("ARXIV_POOL.readiness_gate must be one of: off, warn, strict")
    return normalized


def _arxiv_api_query_params(window: ArxivPoolWindow) -> dict[str, str]:
    normalized_window = _normalize_window(window)
    return {
        "search_query": _arxiv_query_with_period(
            query=normalized_window.query_text,
            period_start=normalized_window.period_start,
            period_end=normalized_window.period_end,
        ),
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "start": "0",
        "max_results": str(normalized_window.max_results),
    }


def _papers_from_arxiv_atom_feed(feed_text: str) -> list[ArxivPoolPaper]:
    parsed = feedparser.parse(feed_text)
    entries = getattr(parsed, "entries", []) or []
    return [
        paper
        for paper in (_paper_from_arxiv_atom_entry(entry) for entry in entries)
        if paper is not None
    ]


def _paper_from_arxiv_atom_entry(entry: Any) -> ArxivPoolPaper | None:
    entry_id = _clean_text(_feed_value(entry, "id") or _feed_value(entry, "link"))
    title = _clean_whitespace(_feed_value(entry, "title"))
    if not entry_id or not title:
        return None
    arxiv_id = normalize_arxiv_id(entry_id)
    return ArxivPoolPaper(
        arxiv_id=arxiv_id,
        version=_version_from_id(arxiv_id),
        canonical_url=f"https://arxiv.org/abs/{arxiv_id}",
        title=title,
        abstract=_optional_text(_feed_value(entry, "summary")),
        authors=_atom_authors(_feed_value(entry, "authors")),
        primary_category=_atom_primary_category(entry),
        categories=_atom_categories(_feed_value(entry, "tags")),
        published_at=_datetime_from_struct_time(_feed_value(entry, "published_parsed")),
        updated_at=_datetime_from_struct_time(_feed_value(entry, "updated_parsed")),
        comment=_optional_text(_feed_value(entry, "arxiv_comment")),
        journal_ref=_optional_text(_feed_value(entry, "arxiv_journal_ref")),
        doi=_optional_text(_feed_value(entry, "arxiv_doi")),
        raw_atom=_atom_raw_metadata(entry=entry, entry_id=entry_id),
    )


def _feed_value(container: Any, key: str) -> Any:
    getter = getattr(container, "get", None)
    if callable(getter):
        return getter(key)
    return getattr(container, key, None)


def _clean_whitespace(value: Any) -> str:
    return " ".join(_clean_text(value).split())


def _atom_authors(raw_authors: Any) -> list[str]:
    if not isinstance(raw_authors, Iterable) or isinstance(raw_authors, (str, bytes)):
        return []
    return _clean_text_list(_feed_value(author, "name") for author in raw_authors)


def _atom_primary_category(entry: Any) -> str | None:
    primary = _feed_value(entry, "arxiv_primary_category")
    return _optional_text(_feed_value(primary, "term"))


def _atom_categories(raw_tags: Any) -> list[str]:
    if not isinstance(raw_tags, Iterable) or isinstance(raw_tags, (str, bytes)):
        return []
    return _clean_text_list(_feed_value(tag, "term") for tag in raw_tags)


def _datetime_from_struct_time(value: Any) -> datetime | None:
    if value is None:
        return None
    try:
        return datetime.fromtimestamp(calendar.timegm(value), tz=UTC)
    except Exception:
        return None


def _atom_raw_metadata(*, entry: Any, entry_id: str) -> dict[str, Any]:
    raw_atom: dict[str, Any] = {
        "entry_id": entry_id,
        "fetcher": _ARXIV_POOL_FETCHER_NAME,
    }
    pdf_url = _atom_pdf_url(_feed_value(entry, "links"))
    if pdf_url is not None:
        raw_atom["pdf_url"] = pdf_url
    return raw_atom


def _atom_pdf_url(raw_links: Any) -> str | None:
    if not isinstance(raw_links, Iterable) or isinstance(raw_links, (str, bytes)):
        return None
    for link in raw_links:
        href = _optional_text(_feed_value(link, "href"))
        if href is None:
            continue
        title = str(_feed_value(link, "title") or "").lower()
        media_type = str(_feed_value(link, "type") or "").lower()
        if title == "pdf" or media_type == "application/pdf" or "/pdf/" in href:
            return href
    return None


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


def _worker_state_from_row(row: sqlite3.Row) -> ArxivPoolWorkerState:
    return ArxivPoolWorkerState(
        name=str(row["name"] or "default"),
        last_started_at=_datetime_from_text(row["last_started_at"]),
        last_heartbeat_at=_datetime_from_text(row["last_heartbeat_at"]),
        last_completed_at=_datetime_from_text(row["last_completed_at"]),
        last_planned_windows_total=int(row["last_planned_windows_total"] or 0),
        last_completed_windows_total=int(row["last_completed_windows_total"] or 0),
        last_cache_hit_total=int(row["last_cache_hit_total"] or 0),
        last_failed_windows_total=int(row["last_failed_windows_total"] or 0),
        last_cooldown_until=_datetime_from_text(row["last_cooldown_until"]),
        next_wake_at=_datetime_from_text(row["next_wake_at"]),
        last_error_category=row["last_error_category"],
        last_error_message=row["last_error_message"],
    )


def _coerce_worker_pass_record(
    pass_record: ArxivPoolWorkerPassRecord | None,
    raw_pass_record: dict[str, Any],
) -> ArxivPoolWorkerPassRecord:
    if pass_record is not None:
        if raw_pass_record:
            raise TypeError("pass_record cannot be combined with result fields")
        return pass_record
    return ArxivPoolWorkerPassRecord(**raw_pass_record)


def _coerce_worker_config(
    config: ArxivPoolWorkerConfig | None,
    raw_config: dict[str, Any],
) -> ArxivPoolWorkerConfig:
    if config is not None:
        if raw_config:
            raise TypeError("config cannot be combined with worker fields")
        return config
    return ArxivPoolWorkerConfig(**raw_config)


def _coerce_worker_pass_completion(
    completion: _WorkerPassCompletion | None,
    raw_completion: dict[str, Any],
) -> _WorkerPassCompletion:
    if completion is not None:
        if raw_completion:
            raise TypeError("completion cannot be combined with pass fields")
        return completion
    return _WorkerPassCompletion(**raw_completion)


def _worker_pass_record_params(
    *,
    name: str,
    completed_at: datetime,
    record: ArxivPoolWorkerPassRecord,
) -> tuple[Any, ...]:
    result = record.result
    return (
        name,
        _datetime_to_text(completed_at),
        _datetime_to_text(completed_at),
        _datetime_to_text(completed_at),
        max(0, int(record.planned_windows_total)),
        int(result.completed_windows_total),
        int(result.cache_hit_total),
        int(result.failed_windows_total + result.rate_limited_windows_total),
        _datetime_to_text(record.cooldown_until),
        _datetime_to_text(record.next_wake_at),
        _optional_text(record.error_category),
        _truncate_error(record.error_message),
    )


def _worker_state_from_pass_record(
    *,
    name: str,
    completed_at: datetime,
    record: ArxivPoolWorkerPassRecord,
) -> ArxivPoolWorkerState:
    result = record.result
    return ArxivPoolWorkerState(
        name=name,
        last_started_at=completed_at,
        last_heartbeat_at=completed_at,
        last_completed_at=completed_at,
        last_planned_windows_total=max(0, int(record.planned_windows_total)),
        last_completed_windows_total=int(result.completed_windows_total),
        last_cache_hit_total=int(result.cache_hit_total),
        last_failed_windows_total=int(
            result.failed_windows_total + result.rate_limited_windows_total
        ),
        last_cooldown_until=_ensure_utc_optional(record.cooldown_until),
        next_wake_at=_ensure_utc_optional(record.next_wake_at),
        last_error_category=_optional_text(record.error_category),
        last_error_message=_truncate_error(record.error_message),
    )


def _normalize_worker_name(value: str) -> str:
    normalized = str(value or "").strip()
    return normalized or "default"


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


def _isoformat_or_none(value: datetime | None) -> str | None:
    return _datetime_to_text(value)


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


def _retry_after_seconds_from_response(response: Any | None) -> int | None:
    if response is None:
        return None
    headers = getattr(response, "headers", {}) or {}
    try:
        raw = headers.get("Retry-After")
    except Exception:
        raw = None
    return _parse_retry_after_seconds(raw)


def _parse_retry_after_seconds(raw: Any) -> int | None:
    text = str(raw or "").strip()
    if not text:
        return None
    try:
        return max(0, int(text))
    except Exception:
        pass
    try:
        retry_at = parsedate_to_datetime(text)
    except Exception:
        return None
    if retry_at.tzinfo is None:
        retry_at = retry_at.replace(tzinfo=UTC)
    delay_seconds = (retry_at.astimezone(UTC) - _utc_now()).total_seconds()
    return max(0, int(math.ceil(delay_seconds)))


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

CREATE TABLE IF NOT EXISTS arxiv_pool_worker_state (
    name TEXT PRIMARY KEY,
    last_started_at TEXT,
    last_heartbeat_at TEXT,
    last_completed_at TEXT,
    last_planned_windows_total INTEGER NOT NULL DEFAULT 0,
    last_completed_windows_total INTEGER NOT NULL DEFAULT 0,
    last_cache_hit_total INTEGER NOT NULL DEFAULT 0,
    last_failed_windows_total INTEGER NOT NULL DEFAULT 0,
    last_cooldown_until TEXT,
    next_wake_at TEXT,
    last_error_category TEXT,
    last_error_message TEXT
);

CREATE INDEX IF NOT EXISTS ix_arxiv_query_windows_status
    ON arxiv_query_windows(status);
CREATE INDEX IF NOT EXISTS ix_arxiv_query_windows_period
    ON arxiv_query_windows(period_start, period_end);
CREATE INDEX IF NOT EXISTS ix_arxiv_query_matches_arxiv_id
    ON arxiv_query_matches(arxiv_id);
"""
