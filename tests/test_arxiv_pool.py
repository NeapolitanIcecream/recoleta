from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from email.utils import format_datetime
import json
from pathlib import Path
import signal
import sqlite3
from typing import Any

import httpx
import pytest
import typer
import yaml
from typer.testing import CliRunner

import recoleta.cli
from recoleta.arxiv_pool import (
    ArxivApiFetcher,
    ArxivPoolBackendReadiness,
    ArxivPoolLeaseHeldError,
    ArxivPoolPaper,
    ArxivPoolRateLimitedError,
    ArxivPoolReadinessPolicy,
    ArxivPoolStore,
    ArxivPoolSync,
    ArxivPoolSyncResult,
    ArxivPoolWorker,
    ArxivPoolWindow,
    build_arxiv_pool_windows,
    build_arxiv_pool_worker_windows,
    evaluate_arxiv_pool_window_readiness,
)
from recoleta.cli.arxiv_pool import (
    ArxivPoolWorkerCommandOptions,
    run_admin_arxiv_pool_gc_command,
    run_arxiv_pool_backfill_command,
    run_arxiv_pool_sync_command,
    run_arxiv_pool_worker_command,
    run_inspect_arxiv_pool_freshness_command,
)
from recoleta.cli.arxiv_pool_readiness import (
    build_arxiv_pool_workflow_readiness_plan,
)
from recoleta.cli.fleet import (
    build_fleet_arxiv_pool_pre_sync_plan,
    execute_fleet_granularity_workflow,
    run_fleet_arxiv_pool_pre_sync,
)
from recoleta.fleet import load_child_settings, load_fleet_manifest
from recoleta.sources import (
    ArxivPullRequest,
    SourcePullResult,
    SourcePullStateSnapshot,
    fetch_arxiv_drafts,
)
from tests.spec_support import install_fake_huldra


_EMPTY_ARXIV_FEED = """\
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" />
"""


_ARXIV_FEED_WITH_PAPER = """\
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
  <entry>
    <id>http://arxiv.org/abs/2604.27001v2</id>
    <updated>2026-04-28T12:34:56Z</updated>
    <published>2026-04-27T11:00:00Z</published>
    <title>  Pool
 Paper  </title>
    <summary>Abstract text.</summary>
    <author><name>Ada Lovelace</name></author>
    <author><name>Grace Hopper</name></author>
    <arxiv:primary_category term="cs.AI" scheme="http://arxiv.org/schemas/atom" />
    <category term="cs.AI" scheme="http://arxiv.org/schemas/atom" />
    <category term="cs.LG" scheme="http://arxiv.org/schemas/atom" />
    <arxiv:comment>12 pages</arxiv:comment>
    <arxiv:journal_ref>Journal Demo</arxiv:journal_ref>
    <arxiv:doi>10.1234/demo</arxiv:doi>
    <link href="http://arxiv.org/abs/2604.27001v2" rel="alternate" type="text/html" />
    <link href="http://arxiv.org/pdf/2604.27001v2" rel="related" type="application/pdf" title="pdf" />
  </entry>
</feed>
"""


_ARXIV_FEED_WITH_OLD_STYLE_PAPER = """\
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>http://arxiv.org/abs/math/0309136v1</id>
    <updated>2003-09-12T00:00:00Z</updated>
    <published>2003-09-12T00:00:00Z</published>
    <title>Old Style Identifier</title>
    <summary>Abstract text.</summary>
    <author><name>Author One</name></author>
  </entry>
</feed>
"""


def _window(query: str = "cat:cs.AI") -> ArxivPoolWindow:
    return ArxivPoolWindow(
        query_text=query,
        period_start=datetime(2026, 4, 27, tzinfo=UTC),
        period_end=datetime(2026, 4, 28, tzinfo=UTC),
        max_results=60,
    )


def _paper(
    arxiv_id: str,
    *,
    title: str = "Pool Paper",
    published_at: datetime | None = None,
) -> ArxivPoolPaper:
    return ArxivPoolPaper(
        arxiv_id=arxiv_id,
        version=1,
        canonical_url=f"https://arxiv.org/abs/{arxiv_id}",
        title=title,
        abstract="An abstract.",
        authors=["Ada Lovelace", "Grace Hopper"],
        primary_category="cs.AI",
        categories=["cs.AI", "cs.LG"],
        published_at=published_at or datetime(2026, 4, 27, 12, tzinfo=UTC),
        updated_at=datetime(2026, 4, 27, 13, tzinfo=UTC),
        comment="demo",
        journal_ref=None,
        doi=None,
        raw_atom={"entry_id": f"https://arxiv.org/abs/{arxiv_id}"},
    )


class _FakeFetcher:
    def __init__(self, papers_by_query: dict[str, list[ArxivPoolPaper]]) -> None:
        self.papers_by_query = papers_by_query
        self.calls: list[ArxivPoolWindow] = []

    def fetch(self, window: ArxivPoolWindow) -> list[ArxivPoolPaper]:
        self.calls.append(window)
        return list(self.papers_by_query.get(window.query_text, []))


class _RaisingFetcher:
    def __init__(self, exc: Exception) -> None:
        self.exc = exc
        self.calls: list[ArxivPoolWindow] = []

    def fetch(self, window: ArxivPoolWindow) -> list[ArxivPoolPaper]:
        self.calls.append(window)
        raise self.exc


def _record_completed_window(
    store: ArxivPoolStore,
    window: ArxivPoolWindow,
    *,
    arxiv_id: str | None = None,
) -> None:
    paper_id = arxiv_id or f"{window.period_start:%y%m.%d}001v1"
    store.record_completed_window(
        window=window,
        papers=[
            _paper(
                paper_id,
                published_at=window.period_start + timedelta(hours=12),
            )
        ],
    )


class _FakeSignalInterrupt(KeyboardInterrupt):
    def __init__(self, signum: int) -> None:
        super().__init__()
        self.signum = signum


def test_arxiv_pool_daily_sync_fetches_one_page_per_uncached_query(
    tmp_path: Path,
) -> None:
    store = ArxivPoolStore(tmp_path / "arxiv_pool.db")
    fetcher = _FakeFetcher(
        {
            "cat:cs.AI": [_paper("2604.27001v1")],
            "cat:cs.LG": [_paper("2604.27002v1")],
        }
    )
    sync = ArxivPoolSync(
        store=store,
        fetcher=fetcher,
        request_interval_seconds=0,
        cooldown_seconds=3600,
    )

    result = sync.sync_windows(
        [
            _window("cat:cs.AI"),
            _window("cat:cs.LG"),
        ]
    )

    assert [call.query_text for call in fetcher.calls] == ["cat:cs.AI", "cat:cs.LG"]
    assert result.upstream_requests_total == 2
    assert result.completed_windows_total == 2
    assert result.cache_hit_total == 0


def test_arxiv_pool_repeated_daily_sync_uses_cached_windows_without_fetch(
    tmp_path: Path,
) -> None:
    store = ArxivPoolStore(tmp_path / "arxiv_pool.db")
    first_fetcher = _FakeFetcher({"cat:cs.AI": [_paper("2604.27001v1")]})
    ArxivPoolSync(
        store=store,
        fetcher=first_fetcher,
        request_interval_seconds=0,
        cooldown_seconds=3600,
    ).sync_windows([_window("cat:cs.AI")])
    second_fetcher = _FakeFetcher({"cat:cs.AI": [_paper("2604.27099v1")]})

    result = ArxivPoolSync(
        store=store,
        fetcher=second_fetcher,
        request_interval_seconds=0,
        cooldown_seconds=3600,
    ).sync_windows([_window("cat:cs.AI")])

    assert second_fetcher.calls == []
    assert result.upstream_requests_total == 0
    assert result.cache_hit_total == 1


def test_arxiv_pool_gc_prunes_completed_windows_before_normal_refetch(
    tmp_path: Path,
) -> None:
    """Regression: GC left completed windows looking cached after deleting matches."""
    store = ArxivPoolStore(tmp_path / "arxiv_pool.db")
    window = _window("cat:cs.AI")
    ArxivPoolSync(
        store=store,
        fetcher=_FakeFetcher({"cat:cs.AI": [_paper("2604.27001v1")]}),
        request_interval_seconds=0,
        cooldown_seconds=3600,
    ).sync_windows([window])

    deleted = store.prune_query_matches_older_than(
        window.period_end + timedelta(seconds=1)
    )
    pruned_window = store.get_window(window)
    refresh_fetcher = _FakeFetcher({"cat:cs.AI": [_paper("2604.27099v1")]})

    result = ArxivPoolSync(
        store=store,
        fetcher=refresh_fetcher,
        request_interval_seconds=0,
        cooldown_seconds=3600,
    ).sync_windows([window])

    assert deleted == 1
    assert pruned_window is not None
    assert pruned_window.status == "pruned"
    assert refresh_fetcher.calls == [window]
    assert result.cache_hit_total == 0
    assert result.completed_windows_total == 1
    assert [paper.arxiv_id for paper in store.cached_papers_for_window(window) or []] == [
        "2604.27099v1"
    ]


def test_forced_refresh_failure_preserves_completed_cache_for_ingest_and_sync(
    tmp_path: Path,
) -> None:
    """Regression: a failed forced refresh made the last successful cache unreadable."""
    pool_path = tmp_path / "arxiv_pool.db"
    store = ArxivPoolStore(pool_path)
    window = _window("cat:cs.AI")
    ArxivPoolSync(
        store=store,
        fetcher=_FakeFetcher({"cat:cs.AI": [_paper("2604.27001v1")]}),
        request_interval_seconds=0,
        cooldown_seconds=3600,
    ).sync_windows([window])

    forced_fetcher = _RaisingFetcher(RuntimeError("temporary arXiv outage"))
    forced = ArxivPoolSync(
        store=store,
        fetcher=forced_fetcher,
        request_interval_seconds=0,
        cooldown_seconds=3600,
    ).sync_windows([window], force=True)
    cached = store.cached_papers_for_window(window)
    completed_after_failure = store.get_window(window)
    normal_fetcher = _FakeFetcher({"cat:cs.AI": [_paper("2604.27099v1")]})
    normal = ArxivPoolSync(
        store=store,
        fetcher=normal_fetcher,
        request_interval_seconds=0,
        cooldown_seconds=3600,
    ).sync_windows([window])
    ingested = fetch_arxiv_drafts(
        request=ArxivPullRequest(
            queries=["cat:cs.AI"],
            max_results_per_run=60,
            period_start=datetime(2026, 4, 27, tzinfo=UTC),
            period_end=datetime(2026, 4, 28, tzinfo=UTC),
            include_stats=True,
            mode="pool",
            pool_db_path=pool_path,
            pool_maturity_lag_days=0,
        )
    )

    assert forced_fetcher.calls == [window]
    assert forced.failed_windows_total == 1
    assert cached is not None
    assert [paper.arxiv_id for paper in cached] == ["2604.27001v1"]
    assert completed_after_failure is not None
    assert completed_after_failure.status == "completed"
    assert normal_fetcher.calls == []
    assert normal.cache_hit_total == 1
    assert isinstance(ingested, SourcePullResult)
    assert [draft.source_item_id for draft in ingested.drafts] == ["2604.27001v1"]
    assert ingested.extra_metrics.get("pool_window_unavailable_total", 0) == 0


def test_forced_rate_limit_preserves_completed_cache_during_cooldown(
    tmp_path: Path,
) -> None:
    """Regression: a forced 429 overwrote a readable completed window."""
    store = ArxivPoolStore(tmp_path / "arxiv_pool.db")
    window = _window("cat:cs.AI")
    ArxivPoolSync(
        store=store,
        fetcher=_FakeFetcher({"cat:cs.AI": [_paper("2604.27001v1")]}),
        request_interval_seconds=0,
        cooldown_seconds=3600,
    ).sync_windows([window])

    forced_fetcher = _RaisingFetcher(
        ArxivPoolRateLimitedError(retry_after_seconds=120)
    )
    forced = ArxivPoolSync(
        store=store,
        fetcher=forced_fetcher,
        request_interval_seconds=0,
        cooldown_seconds=3600,
    ).sync_windows([window], force=True)
    normal_fetcher = _FakeFetcher({"cat:cs.AI": [_paper("2604.27099v1")]})
    normal = ArxivPoolSync(
        store=store,
        fetcher=normal_fetcher,
        request_interval_seconds=0,
        cooldown_seconds=3600,
    ).sync_windows([window])
    rate_state = store.get_rate_state()
    completed_after_rate_limit = store.get_window(window)

    assert forced_fetcher.calls == [window]
    assert forced.upstream_429_total == 1
    assert forced.rate_limited_windows_total == 1
    assert rate_state is not None
    assert rate_state.cooldown_until is not None
    cached = store.cached_papers_for_window(window)
    assert cached is not None
    assert [paper.arxiv_id for paper in cached] == ["2604.27001v1"]
    assert completed_after_rate_limit is not None
    assert completed_after_rate_limit.status == "completed"
    assert normal_fetcher.calls == []
    assert normal.cache_hit_total == 1
    assert normal.cooldown_active_total == 0


def test_arxiv_pool_readiness_current_day_is_immature(tmp_path: Path) -> None:
    store = ArxivPoolStore(tmp_path / "arxiv_pool.db")
    window = ArxivPoolWindow(
        query_text="cat:cs.AI",
        period_start=datetime(2026, 5, 20, tzinfo=UTC),
        period_end=datetime(2026, 5, 21, tzinfo=UTC),
        max_results=60,
    )
    _record_completed_window(store, window, arxiv_id="2605.20001v1")

    readiness = evaluate_arxiv_pool_window_readiness(
        store=store,
        window=window,
        policy=ArxivPoolReadinessPolicy(
            maturity_lag_days=1,
            now=datetime(2026, 5, 20, 12, tzinfo=UTC),
        ),
    )

    assert readiness.cache_readable is True
    assert readiness.mature is False
    assert readiness.analysis_ready is False
    assert readiness.blocked_reason == "immature_window"


def test_arxiv_pool_readiness_yesterday_is_analysis_ready(tmp_path: Path) -> None:
    store = ArxivPoolStore(tmp_path / "arxiv_pool.db")
    window = ArxivPoolWindow(
        query_text="cat:cs.AI",
        period_start=datetime(2026, 5, 19, tzinfo=UTC),
        period_end=datetime(2026, 5, 20, tzinfo=UTC),
        max_results=60,
    )
    _record_completed_window(store, window, arxiv_id="2605.19001v1")

    readiness = evaluate_arxiv_pool_window_readiness(
        store=store,
        window=window,
        policy=ArxivPoolReadinessPolicy(
            maturity_lag_days=1,
            now=datetime(2026, 5, 20, 0, 1, tzinfo=UTC),
        ),
    )

    assert readiness.cache_readable is True
    assert readiness.mature is True
    assert readiness.analysis_ready is True
    assert readiness.blocked_reason is None


def test_arxiv_pool_readiness_keeps_completed_cache_ready_after_refresh_failure(
    tmp_path: Path,
) -> None:
    store = ArxivPoolStore(tmp_path / "arxiv_pool.db")
    window = _window("cat:cs.AI")
    _record_completed_window(store, window, arxiv_id="2604.27001v1")

    store.record_rate_limited_window(
        window=window,
        cooldown_until=datetime(2026, 5, 20, 13, tzinfo=UTC),
        error_message="rate limited",
    )

    readiness = evaluate_arxiv_pool_window_readiness(
        store=store,
        window=window,
        policy=ArxivPoolReadinessPolicy(
            maturity_lag_days=1,
            now=datetime(2026, 5, 20, 12, tzinfo=UTC),
        ),
    )
    record = store.get_window(window)

    assert record is not None
    assert record.status == "completed"
    assert record.error_category == "rate_limited"
    assert readiness.cache_readable is True
    assert readiness.mature is True
    assert readiness.analysis_ready is True


def test_arxiv_pool_sync_stops_after_first_429_without_fetching_later_windows(
    tmp_path: Path,
) -> None:
    class RateLimitedFetcher:
        def __init__(self) -> None:
            self.calls = 0

        def fetch(self, window: ArxivPoolWindow) -> list[ArxivPoolPaper]:
            self.calls += 1
            raise ArxivPoolRateLimitedError(retry_after_seconds=120)

    store = ArxivPoolStore(tmp_path / "arxiv_pool.db")
    fetcher = RateLimitedFetcher()
    sync = ArxivPoolSync(
        store=store,
        fetcher=fetcher,
        request_interval_seconds=0,
        cooldown_seconds=3600,
    )

    result = sync.sync_windows([_window("cat:cs.AI"), _window("cat:cs.LG")])
    rate_state = store.get_rate_state()
    recorded_window = store.get_window(_window("cat:cs.AI"))
    later_window = store.get_window(_window("cat:cs.LG"))

    assert fetcher.calls == 1
    assert result.upstream_429_total == 1
    assert result.rate_limited_windows_total == 1
    assert recorded_window is not None
    assert recorded_window.status == "rate_limited"
    assert later_window is None
    assert rate_state is not None
    assert rate_state.cooldown_until is not None

    blocked_fetcher = _FakeFetcher({"cat:cs.AI": [_paper("2604.27001v1")]})
    blocked = ArxivPoolSync(
        store=store,
        fetcher=blocked_fetcher,
        request_interval_seconds=0,
        cooldown_seconds=3600,
    ).sync_windows([_window("cat:cs.AI")])

    assert blocked_fetcher.calls == []
    assert blocked.cooldown_active_total == 1
    assert blocked.skipped_windows_total == 1


def test_arxiv_pool_fetcher_sends_single_request_per_window() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, text=_EMPTY_ARXIV_FEED)

    fetcher = ArxivApiFetcher(
        client=httpx.Client(transport=httpx.MockTransport(handler))
    )

    papers = fetcher.fetch(_window("cat:cs.AI"))

    assert papers == []
    assert len(requests) == 1
    request = requests[0]
    assert str(request.url).startswith("https://export.arxiv.org/api/query?")
    assert request.url.params["search_query"] == (
        "(cat:cs.AI) AND submittedDate:[202604270000 TO 202604272359]"
    )
    assert request.url.params["sortBy"] == "submittedDate"
    assert request.url.params["sortOrder"] == "descending"
    assert request.url.params["start"] == "0"
    assert request.url.params["max_results"] == "60"
    assert "Recoleta" in request.headers["user-agent"]


def test_arxiv_pool_fetcher_429_raises_rate_limited_with_retry_after() -> None:
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            429,
            headers={"Retry-After": "120"},
            text="rate limited",
        )

    fetcher = ArxivApiFetcher(
        client=httpx.Client(transport=httpx.MockTransport(handler))
    )

    with pytest.raises(ArxivPoolRateLimitedError) as exc:
        fetcher.fetch(_window("cat:cs.AI"))

    assert len(requests) == 1
    assert exc.value.retry_after_seconds == 120


def test_arxiv_pool_fetcher_parses_http_date_retry_after(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import recoleta.arxiv_pool as pool_module

    fixed_now = datetime(2026, 5, 15, 12, tzinfo=UTC)
    retry_at = fixed_now + timedelta(seconds=75)
    monkeypatch.setattr(pool_module, "_utc_now", lambda: fixed_now)

    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(
            429,
            headers={"Retry-After": format_datetime(retry_at, usegmt=True)},
            text="rate limited",
        )

    fetcher = ArxivApiFetcher(
        client=httpx.Client(transport=httpx.MockTransport(handler))
    )

    with pytest.raises(ArxivPoolRateLimitedError) as exc:
        fetcher.fetch(_window("cat:cs.AI"))

    assert exc.value.retry_after_seconds == 75


def test_arxiv_pool_fetcher_parses_atom_feed_to_pool_papers() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text=_ARXIV_FEED_WITH_PAPER)

    fetcher = ArxivApiFetcher(
        client=httpx.Client(transport=httpx.MockTransport(handler))
    )

    papers = fetcher.fetch(_window("cat:cs.AI"))

    assert len(papers) == 1
    paper = papers[0]
    assert paper.arxiv_id == "2604.27001v2"
    assert paper.version == 2
    assert paper.canonical_url == "https://arxiv.org/abs/2604.27001v2"
    assert paper.title == "Pool Paper"
    assert paper.abstract == "Abstract text."
    assert paper.authors == ["Ada Lovelace", "Grace Hopper"]
    assert paper.primary_category == "cs.AI"
    assert paper.categories == ["cs.AI", "cs.LG"]
    assert paper.published_at == datetime(2026, 4, 27, 11, tzinfo=UTC)
    assert paper.updated_at == datetime(2026, 4, 28, 12, 34, 56, tzinfo=UTC)
    assert paper.comment == "12 pages"
    assert paper.journal_ref == "Journal Demo"
    assert paper.doi == "10.1234/demo"
    assert paper.raw_atom["entry_id"] == "http://arxiv.org/abs/2604.27001v2"
    assert paper.raw_atom["pdf_url"] == "http://arxiv.org/pdf/2604.27001v2"


def test_arxiv_pool_fetcher_preserves_old_style_arxiv_ids() -> None:
    """Regression: Atom URL parsing must not drop old archive prefixes."""

    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text=_ARXIV_FEED_WITH_OLD_STYLE_PAPER)

    fetcher = ArxivApiFetcher(
        client=httpx.Client(transport=httpx.MockTransport(handler))
    )

    papers = fetcher.fetch(_window("all:old"))

    assert len(papers) == 1
    assert papers[0].arxiv_id == "math/0309136v1"
    assert papers[0].canonical_url == "https://arxiv.org/abs/math/0309136v1"


def test_arxiv_pool_fetcher_records_http_status_for_non_retryable_failure(
    tmp_path: Path,
) -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(403, text="forbidden")

    store = ArxivPoolStore(tmp_path / "arxiv_pool.db")
    sync = ArxivPoolSync(
        store=store,
        fetcher=ArxivApiFetcher(
            client=httpx.Client(transport=httpx.MockTransport(handler))
        ),
        request_interval_seconds=0,
        cooldown_seconds=3600,
    )

    result = sync.sync_windows([_window("cat:cs.AI")])
    recorded_window = store.get_window(_window("cat:cs.AI"))

    assert result.upstream_requests_total == 1
    assert result.failed_windows_total == 1
    assert recorded_window is not None
    assert recorded_window.status == "failed"
    assert recorded_window.upstream_status == 403
    assert recorded_window.error_category == "ArxivPoolFetchError"


def test_arxiv_pool_sync_lease_prevents_concurrent_upstream_batches(
    tmp_path: Path,
) -> None:
    store = ArxivPoolStore(tmp_path / "arxiv_pool.db")
    store.acquire_sync_lease(owner_token="holder", timeout_seconds=60)

    with pytest.raises(ArxivPoolLeaseHeldError):
        ArxivPoolSync(
            store=store,
            fetcher=_FakeFetcher({"cat:cs.AI": [_paper("2604.27001v1")]}),
            request_interval_seconds=0,
            cooldown_seconds=3600,
        ).sync_windows([_window("cat:cs.AI")])


def test_pool_backed_arxiv_ingest_reads_cached_drafts_without_upstream(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pool_path = tmp_path / "arxiv_pool.db"
    store = ArxivPoolStore(pool_path)
    ArxivPoolSync(
        store=store,
        fetcher=_FakeFetcher({"cat:cs.AI": [_paper("2604.27001v1")]}),
        request_interval_seconds=0,
        cooldown_seconds=3600,
    ).sync_windows([_window("cat:cs.AI")])

    import recoleta.source_pullers as source_pullers

    class ForbiddenClient:
        def __init__(self) -> None:
            raise AssertionError("pool mode must not instantiate arxiv.Client")

    monkeypatch.setattr(source_pullers.arxiv, "Client", ForbiddenClient)

    result = fetch_arxiv_drafts(
        request=ArxivPullRequest(
            queries=["cat:cs.AI"],
            max_results_per_run=60,
            period_start=datetime(2026, 4, 27, tzinfo=UTC),
            period_end=datetime(2026, 4, 28, tzinfo=UTC),
            include_stats=True,
            mode="pool",
            pool_db_path=pool_path,
            pool_maturity_lag_days=0,
        )
    )

    assert isinstance(result, SourcePullResult)
    assert len(result.drafts) == 1
    draft = result.drafts[0]
    assert draft.source == "arxiv"
    assert draft.source_item_id == "2604.27001v1"
    assert draft.canonical_url == "https://arxiv.org/abs/2604.27001v1"
    assert draft.title == "Pool Paper"
    assert draft.authors == ["Ada Lovelace", "Grace Hopper"]
    assert draft.published_at == datetime(2026, 4, 27, 12, tzinfo=UTC)
    assert draft.raw_metadata["query"] == "cat:cs.AI"
    assert result.extra_metrics["pool_drafts_total"] == 1


def test_pool_backed_arxiv_ingest_reports_unavailable_window_without_direct_fetch(
    tmp_path: Path,
) -> None:
    pool_path = tmp_path / "arxiv_pool.db"
    ArxivPoolStore(pool_path).init_schema()

    result = fetch_arxiv_drafts(
        request=ArxivPullRequest(
            queries=["cat:cs.AI"],
            max_results_per_run=60,
            period_start=datetime(2026, 4, 27, tzinfo=UTC),
            period_end=datetime(2026, 4, 28, tzinfo=UTC),
            include_stats=True,
            mode="pool",
            pool_db_path=pool_path,
            pool_maturity_lag_days=0,
        )
    )

    assert isinstance(result, SourcePullResult)
    assert result.drafts == []
    assert result.extra_metrics["pool_window_unavailable_total"] == 1


def test_arxiv_pool_puller_skips_immature_completed_window(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pool_path = tmp_path / "arxiv_pool.db"
    store = ArxivPoolStore(pool_path)
    window = ArxivPoolWindow(
        query_text="cat:cs.AI",
        period_start=datetime(2026, 5, 20, tzinfo=UTC),
        period_end=datetime(2026, 5, 21, tzinfo=UTC),
        max_results=60,
    )
    _record_completed_window(store, window, arxiv_id="2605.20001v1")

    import recoleta.source_pullers as source_pullers

    monkeypatch.setattr(
        source_pullers,
        "_source_pull_now",
        lambda: datetime(2026, 5, 20, 12, tzinfo=UTC),
    )

    result = fetch_arxiv_drafts(
        request=ArxivPullRequest(
            queries=["cat:cs.AI"],
            max_results_per_run=60,
            period_start=datetime(2026, 5, 20, tzinfo=UTC),
            period_end=datetime(2026, 5, 21, tzinfo=UTC),
            include_stats=True,
            mode="pool",
            pool_db_path=pool_path,
        )
    )

    assert isinstance(result, SourcePullResult)
    assert result.drafts == []
    assert result.extra_metrics["pool_window_immature_total"] == 1
    assert result.extra_metrics.get("pool_window_unavailable_total", 0) == 0
    assert result.extra_metrics.get("pool_drafts_total", 0) == 0


def test_arxiv_pool_puller_records_structured_window_diagnostics(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pool_path = tmp_path / "arxiv_pool.db"
    store = ArxivPoolStore(pool_path)
    window = ArxivPoolWindow(
        query_text="cat:cs.AI",
        period_start=datetime(2026, 5, 20, tzinfo=UTC),
        period_end=datetime(2026, 5, 21, tzinfo=UTC),
        max_results=60,
    )
    _record_completed_window(store, window, arxiv_id="2605.20001v1")

    import recoleta.source_pullers as source_pullers

    monkeypatch.setattr(
        source_pullers,
        "_source_pull_now",
        lambda: datetime(2026, 5, 20, 12, tzinfo=UTC),
    )

    result = fetch_arxiv_drafts(
        request=ArxivPullRequest(
            queries=["cat:cs.AI"],
            max_results_per_run=60,
            period_start=datetime(2026, 5, 20, tzinfo=UTC),
            period_end=datetime(2026, 5, 21, tzinfo=UTC),
            include_stats=True,
            mode="pool",
            pool_db_path=pool_path,
            pool_readiness_gate="warn",
        )
    )

    assert isinstance(result, SourcePullResult)
    assert result.extra_metrics["pool_window_immature_total"] == 1
    assert result.diagnostics == [
        {
            "source": "arxiv",
            "kind": "pool_window_readiness",
            "query_text": "cat:cs.AI",
            "period_start": "2026-05-20T00:00:00+00:00",
            "period_end": "2026-05-21T00:00:00+00:00",
            "max_results": 60,
            "record_status": "completed",
            "cache_readable": True,
            "mature": False,
            "analysis_ready": False,
            "blocked_reason": "immature_window",
            "readiness_gate": "warn",
            "allow_immature_windows": False,
        }
    ]


def test_arxiv_pool_puller_uses_current_time_for_maturity_cutoff_near_midnight(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Regression: the pool puller must not mature today's window via +1 minute."""
    pool_path = tmp_path / "arxiv_pool.db"
    store = ArxivPoolStore(pool_path)
    window = ArxivPoolWindow(
        query_text="cat:cs.AI",
        period_start=datetime(2026, 5, 20, tzinfo=UTC),
        period_end=datetime(2026, 5, 21, tzinfo=UTC),
        max_results=60,
    )
    _record_completed_window(store, window, arxiv_id="2605.20001v1")

    import recoleta.source_pullers as source_pullers

    monkeypatch.setattr(
        source_pullers,
        "_source_pull_now",
        lambda: datetime(2026, 5, 20, 23, 59, 30, tzinfo=UTC),
    )

    result = fetch_arxiv_drafts(
        request=ArxivPullRequest(
            queries=["cat:cs.AI"],
            max_results_per_run=60,
            period_start=datetime(2026, 5, 20, tzinfo=UTC),
            period_end=datetime(2026, 5, 21, tzinfo=UTC),
            include_stats=True,
            mode="pool",
            pool_db_path=pool_path,
        )
    )

    assert isinstance(result, SourcePullResult)
    assert result.drafts == []
    assert result.extra_metrics["pool_window_immature_total"] == 1
    assert result.extra_metrics.get("pool_drafts_total", 0) == 0


def test_arxiv_pool_puller_preserves_watermark_for_immature_window(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pool_path = tmp_path / "arxiv_pool.db"
    store = ArxivPoolStore(pool_path)
    window = ArxivPoolWindow(
        query_text="cat:cs.AI",
        period_start=datetime(2026, 5, 20, tzinfo=UTC),
        period_end=datetime(2026, 5, 21, tzinfo=UTC),
        max_results=60,
    )
    _record_completed_window(store, window, arxiv_id="2605.20001v1")

    import recoleta.source_pullers as source_pullers

    monkeypatch.setattr(
        source_pullers,
        "_source_pull_now",
        lambda: datetime(2026, 5, 20, 12, tzinfo=UTC),
    )
    watermark = datetime(2026, 5, 19, 23, tzinfo=UTC)

    result = fetch_arxiv_drafts(
        request=ArxivPullRequest(
            queries=["cat:cs.AI"],
            max_results_per_run=60,
            period_start=datetime(2026, 5, 20, tzinfo=UTC),
            period_end=datetime(2026, 5, 21, tzinfo=UTC),
            pull_state_lookup=lambda scope_kind, scope_key: SourcePullStateSnapshot(
                scope_kind=scope_kind,
                scope_key=scope_key,
                watermark_published_at=watermark,
            )
            if (scope_kind, scope_key) == ("query", "cat:cs.AI")
            else None,
            include_stats=True,
            mode="pool",
            pool_db_path=pool_path,
        )
    )

    assert isinstance(result, SourcePullResult)
    assert result.drafts == []
    assert len(result.state_updates) == 1
    assert result.state_updates[0].watermark_published_at == watermark


def test_pool_backed_arxiv_ingest_without_watermark_uses_latest_mature_day_gh_54(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Regression: first-time strict pool ingest must not deadlock on today."""
    pool_path = tmp_path / "arxiv_pool.db"
    store = ArxivPoolStore(pool_path)
    mature_window = ArxivPoolWindow(
        query_text="cat:cs.AI",
        period_start=datetime(2026, 5, 19, tzinfo=UTC),
        period_end=datetime(2026, 5, 20, tzinfo=UTC),
        max_results=60,
    )
    immature_window = ArxivPoolWindow(
        query_text="cat:cs.AI",
        period_start=datetime(2026, 5, 20, tzinfo=UTC),
        period_end=datetime(2026, 5, 21, tzinfo=UTC),
        max_results=60,
    )
    _record_completed_window(store, mature_window, arxiv_id="2605.19001v1")
    _record_completed_window(store, immature_window, arxiv_id="2605.20001v1")

    import recoleta.source_pullers as source_pullers

    monkeypatch.setattr(
        source_pullers,
        "_source_pull_now",
        lambda: datetime(2026, 5, 20, 12, tzinfo=UTC),
    )

    result = fetch_arxiv_drafts(
        request=ArxivPullRequest(
            queries=["cat:cs.AI"],
            max_results_per_run=60,
            include_stats=True,
            mode="pool",
            pool_db_path=pool_path,
        )
    )

    assert isinstance(result, SourcePullResult)
    assert [draft.source_item_id for draft in result.drafts] == ["2605.19001v1"]
    assert result.extra_metrics.get("pool_window_immature_total", 0) == 0
    assert result.extra_metrics["pool_drafts_total"] == 1
    assert len(result.state_updates) == 1
    assert result.state_updates[0].watermark_published_at == datetime(
        2026,
        5,
        19,
        12,
        tzinfo=UTC,
    )


def test_pool_backed_arxiv_ingest_uses_saved_watermark_without_period_bounds(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Regression: no-bound pool ingest skipped cached arXiv rows before reading watermarks."""
    pool_path = tmp_path / "arxiv_pool.db"
    watermark = datetime(2026, 4, 27, 12, tzinfo=UTC)
    newer_published_at = datetime(2026, 4, 27, 13, tzinfo=UTC)
    ArxivPoolSync(
        store=ArxivPoolStore(pool_path),
        fetcher=_FakeFetcher(
            {
                "cat:cs.AI": [
                    _paper(
                        "2604.27000v1",
                        title="Already Seen",
                        published_at=datetime(2026, 4, 27, 11, tzinfo=UTC),
                    ),
                    _paper(
                        "2604.27001v1",
                        title="New Since Watermark",
                        published_at=newer_published_at,
                    ),
                ]
            }
        ),
        request_interval_seconds=0,
        cooldown_seconds=3600,
    ).sync_windows([_window("cat:cs.AI")])

    import recoleta.source_pullers as source_pullers

    monkeypatch.setattr(
        source_pullers,
        "_source_pull_now",
        lambda: datetime(2026, 4, 27, 18, tzinfo=UTC),
    )

    result = fetch_arxiv_drafts(
        request=ArxivPullRequest(
            queries=["cat:cs.AI"],
            max_results_per_run=60,
            pull_state_lookup=lambda scope_kind, scope_key: SourcePullStateSnapshot(
                scope_kind=scope_kind,
                scope_key=scope_key,
                watermark_published_at=watermark,
            )
            if (scope_kind, scope_key) == ("query", "cat:cs.AI")
            else None,
            include_stats=True,
            mode="pool",
            pool_db_path=pool_path,
            pool_maturity_lag_days=0,
        )
    )

    assert isinstance(result, SourcePullResult)
    assert [draft.source_item_id for draft in result.drafts] == ["2604.27001v1"]
    assert result.extra_metrics.get("pool_window_unavailable_total", 0) == 0
    assert result.extra_metrics["pool_drafts_total"] == 1
    assert len(result.state_updates) == 1
    assert result.state_updates[0].scope_kind == "query"
    assert result.state_updates[0].scope_key == "cat:cs.AI"
    assert result.state_updates[0].watermark_published_at == newer_published_at


def test_build_arxiv_pool_windows_expands_lookback_days() -> None:
    windows = build_arxiv_pool_windows(
        queries=["cat:cs.AI", "cat:cs.AI", "cat:cs.LG"],
        anchor_date=datetime(2026, 4, 29, tzinfo=UTC).date(),
        lookback_days=2,
        max_results=60,
    )

    assert [(window.query_text, window.period_start.date()) for window in windows] == [
        ("cat:cs.AI", datetime(2026, 4, 28, tzinfo=UTC).date()),
        ("cat:cs.LG", datetime(2026, 4, 28, tzinfo=UTC).date()),
        ("cat:cs.AI", datetime(2026, 4, 29, tzinfo=UTC).date()),
        ("cat:cs.LG", datetime(2026, 4, 29, tzinfo=UTC).date()),
    ]


def test_arxiv_pool_worker_plans_current_lookback_and_backfill_windows() -> None:
    windows = build_arxiv_pool_worker_windows(
        queries=["cat:cs.AI", "cat:cs.AI", "cat:cs.LG"],
        max_results=25,
        now=datetime(2026, 5, 14, 9, tzinfo=UTC),
        lookback_days=2,
        backfill_start=date(2026, 5, 10),
        backfill_end=date(2026, 5, 11),
    )

    assert [(window.query_text, window.period_start.date()) for window in windows] == [
        ("cat:cs.AI", date(2026, 5, 13)),
        ("cat:cs.LG", date(2026, 5, 13)),
        ("cat:cs.AI", date(2026, 5, 14)),
        ("cat:cs.LG", date(2026, 5, 14)),
        ("cat:cs.AI", date(2026, 5, 10)),
        ("cat:cs.LG", date(2026, 5, 10)),
        ("cat:cs.AI", date(2026, 5, 11)),
        ("cat:cs.LG", date(2026, 5, 11)),
    ]
    assert {window.max_results for window in windows} == {25}


def test_arxiv_pool_worker_sleeps_until_cooldown_without_fetch(
    tmp_path: Path,
) -> None:
    fixed_now = datetime(2026, 5, 14, 8, tzinfo=UTC)
    cooldown_until = fixed_now + timedelta(seconds=90)
    store = ArxivPoolStore(tmp_path / "arxiv_pool.db")
    store.record_rate_limited_window(
        window=_window("cat:cs.AI"),
        cooldown_until=cooldown_until,
        error_message="rate limited",
    )
    fetcher = _FakeFetcher({"cat:cs.AI": [_paper("2605.14001v1")]})
    events: list[dict[str, object]] = []

    pass_result = ArxivPoolWorker(
        store=store,
        queries=["cat:cs.AI"],
        max_results=60,
        request_interval_seconds=0,
        cooldown_seconds=3600,
        poll_interval_seconds=300,
        lookback_days=1,
        idle_jitter_seconds=0,
        fetcher=fetcher,
        now=lambda: fixed_now,
        event_sink=events.append,
    ).run_once()

    assert fetcher.calls == []
    assert pass_result.sync.upstream_requests_total == 0
    assert pass_result.sync.cooldown_active_total == 1
    assert pass_result.next_sleep_seconds == 90
    assert pass_result.next_wake_at == cooldown_until
    assert any(event["event"] == "cooldown_active" for event in events)
    state = store.get_worker_state()
    assert state is not None
    assert state.last_cooldown_until == cooldown_until
    assert state.next_wake_at == cooldown_until


def test_arxiv_pool_worker_refreshes_completed_current_lookback_windows(
    tmp_path: Path,
) -> None:
    """Regression: completed worker windows stopped receiving later arXiv results."""

    class WindowAwareFetcher:
        def __init__(self) -> None:
            self.calls: list[ArxivPoolWindow] = []
            self.papers_by_day: dict[date, list[ArxivPoolPaper]] = {
                date(2026, 5, 13): [
                    _paper(
                        "2605.13001v1",
                        published_at=datetime(2026, 5, 13, 12, tzinfo=UTC),
                    )
                ],
                date(2026, 5, 14): [
                    _paper(
                        "2605.14001v1",
                        published_at=datetime(2026, 5, 14, 12, tzinfo=UTC),
                    )
                ],
            }

        def fetch(self, window: ArxivPoolWindow) -> list[ArxivPoolPaper]:
            self.calls.append(window)
            return list(self.papers_by_day[window.period_start.date()])

    fixed_now = datetime(2026, 5, 14, 8, tzinfo=UTC)
    pool_path = tmp_path / "arxiv_pool.db"
    fetcher = WindowAwareFetcher()
    worker = ArxivPoolWorker(
        store=ArxivPoolStore(pool_path),
        queries=["cat:cs.AI"],
        max_results=60,
        request_interval_seconds=0,
        cooldown_seconds=3600,
        poll_interval_seconds=30,
        lookback_days=2,
        idle_jitter_seconds=0,
        fetcher=fetcher,
        now=lambda: fixed_now,
    )
    first = worker.run_once()
    fetcher.papers_by_day[date(2026, 5, 13)].append(
        _paper(
            "2605.13002v1",
            published_at=datetime(2026, 5, 13, 14, tzinfo=UTC),
        )
    )
    fetcher.papers_by_day[date(2026, 5, 14)].append(
        _paper(
            "2605.14002v1",
            published_at=datetime(2026, 5, 14, 14, tzinfo=UTC),
        )
    )

    second = worker.run_once()
    ingested = fetch_arxiv_drafts(
        request=ArxivPullRequest(
            queries=["cat:cs.AI"],
            max_results_per_run=60,
            period_start=datetime(2026, 5, 14, tzinfo=UTC),
            period_end=datetime(2026, 5, 15, tzinfo=UTC),
            include_stats=True,
            mode="pool",
            pool_db_path=pool_path,
        )
    )

    assert first.sync.completed_windows_total == 2
    assert second.sync.upstream_requests_total == 2
    assert second.sync.completed_windows_total == 2
    assert second.sync.cache_hit_total == 0
    assert [call.period_start.date() for call in fetcher.calls] == [
        date(2026, 5, 13),
        date(2026, 5, 14),
        date(2026, 5, 13),
        date(2026, 5, 14),
    ]
    assert isinstance(ingested, SourcePullResult)
    assert [draft.source_item_id for draft in ingested.drafts] == [
        "2605.14001v1",
        "2605.14002v1",
    ]


def test_arxiv_pool_worker_refresh_policy_honors_active_cooldown(
    tmp_path: Path,
) -> None:
    """Regression: mutable worker refreshes must not bypass arXiv cooldown."""

    fixed_now = datetime(2026, 5, 14, 8, tzinfo=UTC)
    cooldown_until = fixed_now + timedelta(seconds=90)
    current_window = build_arxiv_pool_worker_windows(
        queries=["cat:cs.AI"],
        max_results=60,
        now=fixed_now,
        lookback_days=1,
    )[0]
    store = ArxivPoolStore(tmp_path / "arxiv_pool.db")
    ArxivPoolSync(
        store=store,
        fetcher=_FakeFetcher({"cat:cs.AI": [_paper("2605.14001v1")]}),
        request_interval_seconds=0,
        cooldown_seconds=3600,
    ).sync_windows([current_window])
    store.record_rate_limited_window(
        window=current_window,
        cooldown_until=cooldown_until,
        error_message="rate limited",
    )
    refresh_fetcher = _FakeFetcher({"cat:cs.AI": [_paper("2605.14002v1")]})

    pass_result = ArxivPoolWorker(
        store=store,
        queries=["cat:cs.AI"],
        max_results=60,
        request_interval_seconds=0,
        cooldown_seconds=3600,
        poll_interval_seconds=300,
        lookback_days=1,
        idle_jitter_seconds=0,
        fetcher=refresh_fetcher,
        now=lambda: fixed_now,
    ).run_once()

    cached = store.cached_papers_for_window(current_window)
    assert refresh_fetcher.calls == []
    assert pass_result.sync.upstream_requests_total == 0
    assert pass_result.sync.cooldown_active_total == 1
    assert pass_result.next_wake_at == cooldown_until
    assert cached is not None
    assert [paper.arxiv_id for paper in cached] == ["2605.14001v1"]


def test_arxiv_pool_worker_retries_transient_failures_with_bounded_backoff(
    tmp_path: Path,
) -> None:
    class FlakyFetcher:
        def __init__(self) -> None:
            self.calls: list[ArxivPoolWindow] = []

        def fetch(self, window: ArxivPoolWindow) -> list[ArxivPoolPaper]:
            self.calls.append(window)
            if len(self.calls) == 1:
                raise RuntimeError("temporary arXiv outage")
            return [_paper("2605.14001v1")]

    fixed_now = datetime(2026, 5, 14, 8, tzinfo=UTC)
    store = ArxivPoolStore(tmp_path / "arxiv_pool.db")
    fetcher = FlakyFetcher()
    sleeps: list[float] = []
    events: list[dict[str, object]] = []

    ArxivPoolWorker(
        store=store,
        queries=["cat:cs.AI"],
        max_results=60,
        request_interval_seconds=0,
        cooldown_seconds=3600,
        poll_interval_seconds=30,
        lookback_days=1,
        idle_jitter_seconds=0,
        failure_backoff_seconds=5,
        fetcher=fetcher,
        sleep=sleeps.append,
        now=lambda: fixed_now,
        event_sink=events.append,
    ).run(max_passes=2)

    assert len(fetcher.calls) == 2
    assert sleeps == [5.0]
    transient_event = next(
        event for event in events if event["event"] == "transient_failure"
    )
    assert transient_event["error_category"] == "transient_failure"
    assert transient_event["sync"]["failed_windows_total"] == 1  # type: ignore[index]
    assert store.get_window(fetcher.calls[-1]).status == "completed"  # type: ignore[union-attr]
    state = store.get_worker_state()
    assert state is not None
    assert state.last_error_category is None
    assert state.last_completed_windows_total == 1


def test_arxiv_pool_worker_emits_stop_event_on_interrupt(tmp_path: Path) -> None:
    fixed_now = datetime(2026, 5, 14, 8, tzinfo=UTC)
    events: list[dict[str, object]] = []

    def interrupting_sleep(_: float) -> None:
        raise KeyboardInterrupt

    worker = ArxivPoolWorker(
        store=ArxivPoolStore(tmp_path / "arxiv_pool.db"),
        queries=["cat:cs.AI"],
        max_results=60,
        request_interval_seconds=0,
        cooldown_seconds=3600,
        poll_interval_seconds=30,
        lookback_days=1,
        idle_jitter_seconds=0,
        fetcher=_FakeFetcher({"cat:cs.AI": [_paper("2605.14001v1")]}),
        sleep=interrupting_sleep,
        now=lambda: fixed_now,
        event_sink=events.append,
    )

    with pytest.raises(KeyboardInterrupt):
        worker.run()

    assert events[-1]["event"] == "worker_stop"
    assert events[-1]["reason"] == "interrupted"
    assert worker.store.get_worker_state() is not None


def test_arxiv_pool_worker_recovers_stale_sync_lease_and_releases_before_idle(
    tmp_path: Path,
) -> None:
    store = ArxivPoolStore(tmp_path / "arxiv_pool.db")
    store.acquire_sync_lease(owner_token="stale", timeout_seconds=1)
    with sqlite3.connect(store.db_path) as conn:
        conn.execute(
            "UPDATE arxiv_pool_leases SET expires_at = ? WHERE name = ?",
            ("2000-01-01T00:00:00+00:00", "arxiv_pool_sync"),
        )
        conn.commit()
    fetcher = _FakeFetcher({"cat:cs.AI": [_paper("2605.14001v1")]})

    result = ArxivPoolWorker(
        store=store,
        queries=["cat:cs.AI"],
        max_results=60,
        request_interval_seconds=0,
        cooldown_seconds=3600,
        poll_interval_seconds=30,
        lookback_days=1,
        idle_jitter_seconds=0,
        fetcher=fetcher,
        now=lambda: datetime(2026, 5, 14, 8, tzinfo=UTC),
    ).run_once()

    with sqlite3.connect(store.db_path) as conn:
        lease_rows = conn.execute("SELECT COUNT(*) FROM arxiv_pool_leases").fetchone()
    assert fetcher.calls
    assert result.sync.completed_windows_total == 1
    assert lease_rows is not None
    assert lease_rows[0] == 0


def test_pool_mode_ingest_reads_worker_cached_windows_after_worker_stops(
    tmp_path: Path,
) -> None:
    pool_path = tmp_path / "arxiv_pool.db"
    fetcher = _FakeFetcher(
        {
            "cat:cs.AI": [
                _paper(
                    "2605.14001v1",
                    published_at=datetime(2026, 5, 14, 12, tzinfo=UTC),
                )
            ]
        }
    )
    worker = ArxivPoolWorker(
        store=ArxivPoolStore(pool_path),
        queries=["cat:cs.AI"],
        max_results=60,
        request_interval_seconds=0,
        cooldown_seconds=3600,
        poll_interval_seconds=30,
        lookback_days=1,
        idle_jitter_seconds=0,
        fetcher=fetcher,
        now=lambda: datetime(2026, 5, 14, 8, tzinfo=UTC),
    )
    worker.run(max_passes=1)

    result = fetch_arxiv_drafts(
        request=ArxivPullRequest(
            queries=["cat:cs.AI"],
            max_results_per_run=60,
            period_start=datetime(2026, 5, 14, tzinfo=UTC),
            period_end=datetime(2026, 5, 15, tzinfo=UTC),
            include_stats=True,
            mode="pool",
            pool_db_path=pool_path,
        )
    )

    assert isinstance(result, SourcePullResult)
    assert [draft.source_item_id for draft in result.drafts] == ["2605.14001v1"]
    assert result.extra_metrics.get("pool_window_unavailable_total", 0) == 0


def test_inspect_arxiv_pool_freshness_json_reports_worker_state(
    tmp_path: Path,
) -> None:
    pool_path = tmp_path / "arxiv_pool.db"
    config_path = _write_pool_config(tmp_path=tmp_path, pool_path=pool_path)
    ArxivPoolWorker(
        store=ArxivPoolStore(pool_path),
        queries=["cat:cs.AI"],
        max_results=60,
        request_interval_seconds=0,
        cooldown_seconds=3600,
        poll_interval_seconds=30,
        lookback_days=1,
        idle_jitter_seconds=0,
        fetcher=_FakeFetcher({"cat:cs.AI": [_paper("2605.14001v1")]}),
        now=lambda: datetime(2026, 5, 14, 8, tzinfo=UTC),
    ).run(max_passes=1)

    payload = run_inspect_arxiv_pool_freshness_command(
        config_path=config_path,
        limit=10,
        json_output=True,
    )

    assert payload["worker_state"] is not None
    assert payload["worker_state"]["last_heartbeat_at"] is not None
    assert payload["worker_state"]["next_wake_at"] is not None
    assert payload["active_cooldown"] is False
    assert payload["fetcher"] == "httpx_atom"
    assert payload["window_status_summary"]["completed"] == 1
    assert payload["window_status_summary"]["analysis_ready"] == 1
    assert payload["maturity_policy"]["timezone"] == "UTC"


def test_inspect_arxiv_pool_freshness_reports_maturity_fields(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pool_path = tmp_path / "arxiv_pool.db"
    config_path = _write_pool_config(tmp_path=tmp_path, pool_path=pool_path)
    store = ArxivPoolStore(pool_path)
    window = ArxivPoolWindow(
        query_text="cat:cs.AI",
        period_start=datetime(2026, 5, 20, tzinfo=UTC),
        period_end=datetime(2026, 5, 21, tzinfo=UTC),
        max_results=60,
    )
    _record_completed_window(store, window, arxiv_id="2605.20001v1")

    import recoleta.arxiv_pool as arxiv_pool_module

    monkeypatch.setattr(
        arxiv_pool_module,
        "_utc_now",
        lambda: datetime(2026, 5, 20, 12, tzinfo=UTC),
    )

    payload = run_inspect_arxiv_pool_freshness_command(
        config_path=config_path,
        limit=10,
        json_output=True,
    )

    assert payload["maturity_policy"] == {
        "timezone": "UTC",
        "maturity_lag_days": 1,
        "maturity_cutoff": "2026-05-20T00:00:00+00:00",
        "readiness_gate": "strict",
        "allow_immature_windows": False,
    }
    assert payload["window_status_summary"]["completed"] == 1
    assert payload["window_status_summary"]["analysis_ready"] == 0
    assert payload["window_status_summary"]["immature"] == 1
    assert payload["windows"][0]["cache_readable"] is True
    assert payload["windows"][0]["mature"] is False
    assert payload["windows"][0]["analysis_ready"] is False
    assert payload["windows"][0]["blocked_reason"] == "immature_window"


def test_inspect_arxiv_pool_freshness_reports_huldra_configured_windows(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import recoleta.cli.arxiv_pool as arxiv_pool_cli

    config_path = _write_huldra_pool_config(
        tmp_path=tmp_path,
        base_url="http://127.0.0.1:8765",
    )
    seen_windows: list[ArxivPoolWindow] = []

    class FakeBackend:
        def evaluate_window_readiness(
            self,
            window: ArxivPoolWindow,
            *,
            readiness_policy: ArxivPoolReadinessPolicy,
        ) -> ArxivPoolBackendReadiness:
            seen_windows.append(window)
            return ArxivPoolBackendReadiness(
                query_text=window.query_text,
                period_start=window.period_start,
                period_end=window.period_end,
                max_results=window.max_results,
                backend="huldra",
                cache_status="missing",
                serving_status="cache_miss",
                cache_readable=False,
                mature=False,
                analysis_ready=False,
                blocked_reason="missing_window",
                cache_key="huldra:v1:demo",
                diagnostic={"huldra_status": "cache_miss"},
            )

    monkeypatch.setattr(
        arxiv_pool_cli,
        "build_arxiv_pool_backend_from_settings",
        lambda settings: FakeBackend(),  # noqa: ARG005
    )

    payload = run_inspect_arxiv_pool_freshness_command(
        config_path=config_path,
        limit=2,
        json_output=True,
    )

    assert payload["backend"] == "huldra"
    assert payload["huldra_base_url"] == "http://127.0.0.1:8765"
    assert payload["inspect_scope"] == "configured_windows"
    assert payload["cache_listing_supported"] is False
    assert payload["pool_db_path"] is None
    assert len(payload["windows"]) == 2
    assert len(seen_windows) == 2
    assert payload["windows"][0]["serving_status"] == "cache_miss"


def test_arxiv_pool_worker_command_emits_json_lifecycle_lines(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    import recoleta.cli.arxiv_pool as arxiv_pool_cli

    pool_path = tmp_path / "arxiv_pool.db"
    config_path = _write_pool_config(tmp_path=tmp_path, pool_path=pool_path)

    class FakeWorker:
        def __init__(self, **kwargs: object) -> None:
            self.event_sink = kwargs["event_sink"]

        def run(self) -> None:
            assert callable(self.event_sink)
            self.event_sink(
                {
                    "event": "worker_start",
                    "worker": "default",
                    "timestamp": "2026-05-14T00:00:00+00:00",
                }
            )

    monkeypatch.setattr(arxiv_pool_cli, "ArxivPoolWorker", FakeWorker)

    arxiv_pool_cli.run_arxiv_pool_worker_command(
        poll_interval_seconds=30,
        lookback_days=1,
        idle_jitter_seconds=0,
        backfill_start=None,
        backfill_end=None,
        config_path=config_path,
        json_output=True,
    )

    output = capsys.readouterr().out.strip().splitlines()
    assert len(output) == 1
    event = json.loads(output[0])
    assert event["command"] == "arxiv-pool worker"
    assert event["event"] == "worker_start"
    assert event["pool_db_path"] == str(pool_path.resolve())


def test_arxiv_pool_worker_command_preserves_sigterm_exit_code(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import recoleta.cli.arxiv_pool as arxiv_pool_cli

    config_path = _write_pool_config(
        tmp_path=tmp_path,
        pool_path=tmp_path / "arxiv_pool.db",
    )

    class FakeWorker:
        def __init__(self, **_: object) -> None:
            return None

        def run(self) -> None:
            raise _FakeSignalInterrupt(signal.SIGTERM)

    monkeypatch.setattr(arxiv_pool_cli, "ArxivPoolWorker", FakeWorker)

    with pytest.raises(typer.Exit) as exc:
        arxiv_pool_cli.run_arxiv_pool_worker_command(
            poll_interval_seconds=30,
            lookback_days=1,
            idle_jitter_seconds=0,
            backfill_start=None,
            backfill_end=None,
            config_path=config_path,
            json_output=True,
        )

    assert exc.value.exit_code == 143


def test_huldra_pool_worker_and_gc_commands_do_not_touch_local_store(
    tmp_path: Path,
) -> None:
    config_path = _write_huldra_pool_config(
        tmp_path=tmp_path,
        base_url="http://127.0.0.1:8765",
    )

    worker_payload = run_arxiv_pool_worker_command(
        ArxivPoolWorkerCommandOptions(
            poll_interval_seconds=300,
            lookback_days=3,
            idle_jitter_seconds=30,
            backfill_start=None,
            backfill_end=None,
            config_path=config_path,
            json_output=True,
        )
    )
    gc_payload = run_admin_arxiv_pool_gc_command(
        config_path=config_path,
        older_than_days=30,
        json_output=True,
    )

    assert worker_payload["status"] == "skipped"
    assert worker_payload["reason"] == "huldra_backend_uses_huldra_worker"
    assert worker_payload["pool_db_path"] is None
    assert gc_payload["status"] == "skipped"
    assert gc_payload["reason"] == "huldra_backend_gc_not_supported"
    assert not (tmp_path / "arxiv_pool.db").exists()


def test_huldra_pool_sync_command_delegates_to_huldra_client(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    install_fake_huldra(monkeypatch)
    from huldra.models import HuldraMaintenanceResult

    config_path = _write_huldra_pool_config(
        tmp_path=tmp_path,
        base_url="http://127.0.0.1:8765",
    )
    calls: list[dict[str, Any]] = []

    class FakeHuldraClient:
        def __init__(self, *, base_url: str, timeout: float) -> None:
            calls.append({"base_url": base_url, "timeout": timeout})

        def __enter__(self) -> "FakeHuldraClient":
            return self

        def __exit__(self, *_: object) -> None:
            return None

        def sync_windows(
            self,
            requests: list[Any],
            *,
            wait: bool,
            wait_timeout_seconds: float | None,
        ) -> HuldraMaintenanceResult:
            calls.append(
                {
                    "requests": requests,
                    "wait": wait,
                    "wait_timeout_seconds": wait_timeout_seconds,
                }
            )
            return HuldraMaintenanceResult(
                requested_total=len(requests),
                completed_windows_total=len(requests),
                papers_total=3,
            )

    import huldra.client

    monkeypatch.setattr(huldra.client, "HuldraClient", FakeHuldraClient)

    payload = run_arxiv_pool_sync_command(
        anchor_date="2026-05-20",
        lookback_days=1,
        force=False,
        config_path=config_path,
        json_output=True,
    )

    assert payload["backend"] == "huldra"
    assert payload["pool_db_path"] is None
    assert payload["sync"]["requested_windows_total"] == 1
    assert payload["sync"]["completed_windows_total"] == 1
    assert calls[0] == {"base_url": "http://127.0.0.1:8765", "timeout": 5.0}
    assert calls[1]["wait"] is True
    assert calls[1]["wait_timeout_seconds"] == 3600
    assert calls[1]["requests"][0].readiness == "analysis_ready"
    assert calls[1]["requests"][0].cache_policy == "cache_only"


@pytest.mark.parametrize("json_output", [True, False])
def test_huldra_pool_sync_cli_rejects_force_refresh_with_stable_reason(
    tmp_path: Path,
    json_output: bool,
) -> None:
    config_path = _write_huldra_pool_config(
        tmp_path=tmp_path,
        base_url="http://127.0.0.1:8765",
    )
    args = [
        "arxiv-pool",
        "sync",
        "--date",
        "2026-05-20",
        "--force",
        "--config",
        str(config_path),
    ]
    if json_output:
        args.append("--json")

    result = CliRunner().invoke(recoleta.cli.app, args)

    assert result.exit_code == 1
    if json_output:
        payload = json.loads(result.output)
        assert payload["status"] == "error"
        assert payload["reason"] == "huldra_force_refresh_unsupported"
    else:
        assert "huldra_force_refresh_unsupported" in result.output


def test_huldra_pool_backfill_command_uses_huldra_backfill_api(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    install_fake_huldra(monkeypatch)
    from huldra.models import HuldraMaintenanceResult

    config_path = _write_huldra_pool_config(
        tmp_path=tmp_path,
        base_url="http://127.0.0.1:8765",
    )
    calls: list[dict[str, Any]] = []

    class FakeHuldraClient:
        def __init__(self, *, base_url: str, timeout: float) -> None:
            calls.append({"base_url": base_url, "timeout": timeout})

        def __enter__(self) -> "FakeHuldraClient":
            return self

        def __exit__(self, *_: object) -> None:
            return None

        def backfill_windows(self, **kwargs: Any) -> HuldraMaintenanceResult:
            calls.append(kwargs)
            return HuldraMaintenanceResult(
                requested_total=3,
                completed_windows_total=3,
            )

    import huldra.client

    monkeypatch.setattr(huldra.client, "HuldraClient", FakeHuldraClient)

    payload = run_arxiv_pool_backfill_command(
        start_date="2026-05-18",
        end_date="2026-05-20",
        force=False,
        config_path=config_path,
        json_output=True,
    )

    assert payload["backend"] == "huldra"
    assert payload["pool_db_path"] is None
    assert payload["sync"]["requested_windows_total"] == 3
    assert calls[0] == {"base_url": "http://127.0.0.1:8765", "timeout": 5.0}
    assert calls[1]["search_queries"] == ["cat:cs.AI"]
    assert calls[1]["start_date"] == date(2026, 5, 18)
    assert calls[1]["end_date"] == date(2026, 5, 20)
    assert calls[1]["wait"] is True
    assert calls[1]["wait_timeout_seconds"] == 3600


@pytest.mark.parametrize("json_output", [True, False])
def test_huldra_pool_backfill_cli_rejects_force_refresh_with_stable_reason(
    tmp_path: Path,
    json_output: bool,
) -> None:
    config_path = _write_huldra_pool_config(
        tmp_path=tmp_path,
        base_url="http://127.0.0.1:8765",
    )
    args = [
        "arxiv-pool",
        "backfill",
        "--start",
        "2026-05-18",
        "--end",
        "2026-05-20",
        "--force",
        "--config",
        str(config_path),
    ]
    if json_output:
        args.append("--json")

    result = CliRunner().invoke(recoleta.cli.app, args)

    assert result.exit_code == 1
    if json_output:
        payload = json.loads(result.output)
        assert payload["status"] == "error"
        assert payload["reason"] == "huldra_force_refresh_unsupported"
    else:
        assert "huldra_force_refresh_unsupported" in result.output


def test_fleet_pre_sync_plan_collects_unique_pool_windows(tmp_path: Path) -> None:
    manifest_path, pool_path = _write_pool_fleet_manifest(tmp_path)

    plan = build_fleet_arxiv_pool_pre_sync_plan(
        manifest_path=manifest_path,
        workflow_name="week",
        anchor_date="2026-04-27",
    )

    assert plan.status == "planned"
    assert plan.pool_db_path == pool_path
    assert len(plan.windows) == 14
    assert {window.query_text for window in plan.windows} == {"cat:cs.AI", "cat:cs.LG"}
    assert {window.period_start.date() for window in plan.windows} == {
        datetime(2026, 4, 27, tzinfo=UTC).date() + timedelta(days=offset)
        for offset in range(7)
    }


def test_fleet_pre_sync_plan_rejects_mixed_pool_backends(tmp_path: Path) -> None:
    manifest_path = _write_mixed_backend_fleet_manifest(tmp_path)

    plan = build_fleet_arxiv_pool_pre_sync_plan(
        manifest_path=manifest_path,
        workflow_name="day",
        anchor_date="2026-05-20",
    )

    assert plan.status == "blocked"
    assert plan.reason == "mixed_arxiv_pool_backends"


def test_fleet_pre_sync_plan_rejects_multiple_huldra_endpoints(
    tmp_path: Path,
) -> None:
    manifest_path = _write_huldra_fleet_manifest(
        tmp_path,
        base_urls=("http://127.0.0.1:8765", "http://127.0.0.1:8766"),
    )

    plan = build_fleet_arxiv_pool_pre_sync_plan(
        manifest_path=manifest_path,
        workflow_name="day",
        anchor_date="2026-05-20",
    )

    assert plan.status == "blocked"
    assert plan.reason == "multiple_huldra_endpoints"


@pytest.mark.parametrize(
    ("scenario", "reason"),
    [
        ("mixed_backend", "mixed_arxiv_pool_backends"),
        ("multiple_huldra_endpoints", "multiple_huldra_endpoints"),
        ("multiple_local_pool_db_paths", "multiple_pool_db_paths"),
    ],
)
def test_fleet_workflow_pool_backend_conflicts_block_before_children(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    scenario: str,
    reason: str,
) -> None:
    """Regression: fleet-level pool conflicts must be terminal, not skipped."""
    if scenario == "mixed_backend":
        manifest_path = _write_mixed_backend_fleet_manifest(tmp_path)
    elif scenario == "multiple_huldra_endpoints":
        manifest_path = _write_huldra_fleet_manifest(
            tmp_path,
            base_urls=("http://127.0.0.1:8765", "http://127.0.0.1:8766"),
        )
    else:
        manifest_path = _write_multiple_local_pool_fleet_manifest(tmp_path)

    import recoleta.cli.fleet as fleet_module

    def fake_pre_sync(plan):  # type: ignore[no-untyped-def]
        raise AssertionError(f"pre-sync must not run for {plan.reason}")

    def fake_child_payload(*, request):  # type: ignore[no-untyped-def]
        raise AssertionError(f"child payload must not run for {request.instance.name}")

    monkeypatch.setattr(fleet_module, "run_fleet_arxiv_pool_pre_sync", fake_pre_sync)
    monkeypatch.setattr(
        fleet_module,
        "_fleet_granularity_child_payload",
        fake_child_payload,
    )

    with pytest.raises(typer.Exit) as exc:
        execute_fleet_granularity_workflow(
            manifest_path=manifest_path,
            workflow_name="day",
            command="fleet run day",
            anchor_date="2026-05-20",
            json_output=True,
        )

    emitted = json.loads(capsys.readouterr().out.strip().splitlines()[-1])
    assert exc.value.exit_code == 1
    assert emitted["status"] == "blocked"
    assert emitted["children"] == []
    assert emitted["arxiv_pool_pre_sync"]["status"] == "blocked"
    assert emitted["arxiv_pool_pre_sync"]["reason"] == reason
    assert emitted["arxiv_pool_readiness"]["status"] == "blocked"
    assert emitted["arxiv_pool_readiness"]["reason"] == reason


def test_huldra_fleet_pre_sync_delegates_deduped_windows_to_huldra(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    install_fake_huldra(monkeypatch)
    from huldra.models import HuldraMaintenanceResult

    manifest_path = _write_huldra_fleet_manifest(
        tmp_path,
        base_urls=("http://127.0.0.1:8765", "http://127.0.0.1:8765"),
        queries=("cat:cs.AI", "cat:cs.AI"),
    )
    calls: list[dict[str, Any]] = []

    class FakeHuldraClient:
        def __init__(self, *, base_url: str, timeout: float) -> None:
            calls.append({"base_url": base_url, "timeout": timeout})

        def __enter__(self) -> "FakeHuldraClient":
            return self

        def __exit__(self, *_: object) -> None:
            return None

        def sync_windows(
            self,
            requests: list[Any],
            *,
            wait: bool,
            wait_timeout_seconds: float | None,
        ) -> HuldraMaintenanceResult:
            calls.append(
                {
                    "requests": requests,
                    "wait": wait,
                    "wait_timeout_seconds": wait_timeout_seconds,
                }
            )
            return HuldraMaintenanceResult(
                requested_total=len(requests),
                completed_windows_total=len(requests),
                papers_total=4,
            )

    import huldra.client

    monkeypatch.setattr(huldra.client, "HuldraClient", FakeHuldraClient)

    plan = build_fleet_arxiv_pool_pre_sync_plan(
        manifest_path=manifest_path,
        workflow_name="day",
        anchor_date="2026-05-20",
    )
    result = run_fleet_arxiv_pool_pre_sync(plan)

    assert plan.status == "planned"
    assert plan.backend_descriptor is not None
    assert plan.backend_descriptor.kind == "huldra"
    assert len(plan.windows) == 1
    assert result.requested_windows_total == 1
    assert result.completed_windows_total == 1
    assert calls[0] == {"base_url": "http://127.0.0.1:8765", "timeout": 30.0}
    assert calls[1]["wait"] is True
    assert calls[1]["wait_timeout_seconds"] == 3600
    assert len(calls[1]["requests"]) == 1
    assert calls[1]["requests"][0].search_query == "cat:cs.AI"
    assert calls[1]["requests"][0].readiness == "analysis_ready"


def test_fleet_pre_sync_preserves_default_huldra_wait_timeout_for_unset_children(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Regression: one explicit child timeout must not suppress another child's default."""
    install_fake_huldra(monkeypatch)
    from huldra.models import HuldraMaintenanceResult

    manifest_path = _write_huldra_fleet_manifest(
        tmp_path,
        base_urls=("http://127.0.0.1:8765", "http://127.0.0.1:8765"),
        queries=("cat:cs.AI", "cat:cs.AI"),
        huldra_wait_timeout_seconds=(None, 5),
    )
    calls: list[dict[str, Any]] = []

    class FakeHuldraClient:
        def __init__(self, *, base_url: str, timeout: float) -> None:
            calls.append({"base_url": base_url, "timeout": timeout})

        def __enter__(self) -> "FakeHuldraClient":
            return self

        def __exit__(self, *_: object) -> None:
            return None

        def sync_windows(
            self,
            requests: list[Any],
            *,
            wait: bool,
            wait_timeout_seconds: float | None,
        ) -> HuldraMaintenanceResult:
            calls.append(
                {
                    "requests": requests,
                    "wait": wait,
                    "wait_timeout_seconds": wait_timeout_seconds,
                }
            )
            return HuldraMaintenanceResult(
                requested_total=len(requests),
                completed_windows_total=len(requests),
                papers_total=4,
            )

    import huldra.client

    monkeypatch.setattr(huldra.client, "HuldraClient", FakeHuldraClient)

    plan = build_fleet_arxiv_pool_pre_sync_plan(
        manifest_path=manifest_path,
        workflow_name="day",
        anchor_date="2026-05-20",
    )
    result = run_fleet_arxiv_pool_pre_sync(plan)

    assert plan.status == "planned"
    assert result.completed_windows_total == 1
    assert calls[1]["wait_timeout_seconds"] == 3600


def test_fleet_pre_sync_plan_merges_mixed_child_readiness_policies_safely(
    tmp_path: Path,
) -> None:
    """Regression: fleet readiness must not depend on child manifest order."""
    manifest_path, _pool_path = _write_pool_fleet_manifest(
        tmp_path,
        readiness_gate=("warn", "strict"),
        maturity_lag_days=(0, 2),
        allow_immature_windows=(True, False),
        request_interval_seconds=(0, 2),
        cooldown_seconds=(60, 3600),
    )

    plan = build_fleet_arxiv_pool_pre_sync_plan(
        manifest_path=manifest_path,
        workflow_name="day",
        anchor_date="2026-05-20",
    )

    assert plan.status == "planned"
    assert plan.readiness_gate == "strict"
    assert plan.maturity_lag_days == 2
    assert plan.allow_immature_windows is False
    assert plan.request_interval_seconds == 2
    assert plan.cooldown_seconds == 3600


def test_fleet_workflow_readiness_plan_merges_huldra_timeout(
    tmp_path: Path,
) -> None:
    """Regression: Huldra readiness must not depend on child manifest order."""
    manifest_path = _write_huldra_fleet_manifest(
        tmp_path,
        base_urls=("http://127.0.0.1:8765", "http://127.0.0.1:8765"),
        huldra_request_timeout_seconds=(3, 12),
    )
    manifest = load_fleet_manifest(manifest_path)
    settings_list = [
        load_child_settings(instance.config_path) for instance in manifest.instances
    ]

    plan = build_arxiv_pool_workflow_readiness_plan(
        settings_list=settings_list,
        target_period_start=datetime(2026, 5, 20, tzinfo=UTC),
        target_period_end=datetime(2026, 5, 21, tzinfo=UTC),
        requested_steps=["trends:day"],
    )

    assert plan.status == "planned"
    assert plan.pool_backend is not None
    assert getattr(plan.pool_backend, "request_timeout_seconds") == 12.0


def test_fleet_workflow_runs_pool_pre_sync_before_child_ingest(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    manifest_path, _pool_path = _write_pool_fleet_manifest(
        tmp_path,
        readiness_gate="warn",
    )
    events: list[str] = []

    import recoleta.cli.fleet as fleet_module

    def fake_pre_sync(plan):  # type: ignore[no-untyped-def]
        events.append("pre_sync")
        return ArxivPoolSyncResult(requested_windows_total=len(plan.windows))

    def fake_child_payload(*, request):  # type: ignore[no-untyped-def]
        events.append(f"child:{request.instance.name}")
        return {
            "instance": request.instance.name,
            "config_path": str(request.instance.config_path),
        }

    monkeypatch.setattr(fleet_module, "run_fleet_arxiv_pool_pre_sync", fake_pre_sync)
    monkeypatch.setattr(
        fleet_module,
        "_fleet_granularity_child_payload",
        fake_child_payload,
    )

    payload = execute_fleet_granularity_workflow(
        manifest_path=manifest_path,
        workflow_name="week",
        command="fleet run week",
        anchor_date="2026-04-27",
        json_output=False,
    )

    assert events == ["pre_sync", "child:embodied_ai", "child:software"]
    assert payload["arxiv_pool_pre_sync"]["status"] == "completed"
    assert payload["arxiv_pool_pre_sync"]["sync"]["requested_windows_total"] == 14


def test_fleet_workflow_skip_ingest_skips_pool_pre_sync_but_still_gates_analysis(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Regression: skipping ingest must not skip strict analysis readiness."""
    manifest_path, _pool_path = _write_pool_fleet_manifest(tmp_path)
    events: list[str] = []

    import recoleta.cli.fleet as fleet_module

    def fake_pre_sync(plan):  # type: ignore[no-untyped-def]
        raise AssertionError("pre-sync should be skipped when ingest is skipped")

    def fake_child_payload(*, request):  # type: ignore[no-untyped-def]
        raise AssertionError("strict readiness should stop before children")

    monkeypatch.setattr(fleet_module, "run_fleet_arxiv_pool_pre_sync", fake_pre_sync)
    monkeypatch.setattr(
        fleet_module,
        "_fleet_granularity_child_payload",
        fake_child_payload,
    )

    with pytest.raises(typer.Exit) as exc:
        execute_fleet_granularity_workflow(
            manifest_path=manifest_path,
            workflow_name="week",
            command="fleet run week",
            anchor_date="2026-04-27",
            skip="ingest",
            json_output=True,
        )

    emitted = json.loads(capsys.readouterr().out.strip().splitlines()[-1])
    assert exc.value.exit_code == 1
    assert events == []
    assert emitted["arxiv_pool_pre_sync"]["status"] == "skipped"
    assert emitted["arxiv_pool_pre_sync"]["reason"] == "ingest_not_requested"
    assert emitted["arxiv_pool_readiness"]["blocked_windows_total"] == 14


def test_fleet_arxiv_pool_readiness_blocks_strict_mode(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    manifest_path, pool_path = _write_pool_fleet_manifest(tmp_path)
    plan = build_fleet_arxiv_pool_pre_sync_plan(
        manifest_path=manifest_path,
        workflow_name="day",
        anchor_date="2026-05-20",
    )
    store = ArxivPoolStore(pool_path)
    for index, window in enumerate(plan.windows):
        _record_completed_window(store, window, arxiv_id=f"2605.20{index:03d}v1")

    import recoleta.arxiv_pool as arxiv_pool_module
    import recoleta.cli.fleet as fleet_module

    monkeypatch.setattr(
        arxiv_pool_module,
        "_utc_now",
        lambda: datetime(2026, 5, 20, 12, tzinfo=UTC),
    )
    events: list[str] = []

    def fake_pre_sync(pre_sync_plan):  # type: ignore[no-untyped-def]
        events.append("pre_sync")
        return ArxivPoolSyncResult(
            requested_windows_total=len(pre_sync_plan.windows),
            cache_hit_total=len(pre_sync_plan.windows),
        )

    def fake_child_payload(*, request):  # type: ignore[no-untyped-def]
        events.append(f"child:{request.instance.name}")
        return {"instance": request.instance.name}

    monkeypatch.setattr(fleet_module, "run_fleet_arxiv_pool_pre_sync", fake_pre_sync)
    monkeypatch.setattr(
        fleet_module,
        "_fleet_granularity_child_payload",
        fake_child_payload,
    )

    with pytest.raises(typer.Exit) as exc:
        execute_fleet_granularity_workflow(
            manifest_path=manifest_path,
            workflow_name="day",
            command="fleet run day",
            anchor_date="2026-05-20",
            json_output=True,
        )

    emitted = json.loads(capsys.readouterr().out.strip().splitlines()[-1])
    assert exc.value.exit_code == 1
    assert events == ["pre_sync"]
    assert emitted["status"] == "blocked"
    assert emitted["arxiv_pool_readiness"]["status"] == "blocked"
    assert emitted["arxiv_pool_readiness"]["immature_windows_total"] == 2
    assert emitted["children"] == []


def test_fleet_arxiv_pool_readiness_blocks_when_analyze_skipped_but_publish_requested(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    manifest_path, pool_path = _write_pool_fleet_manifest(tmp_path)
    plan = build_fleet_arxiv_pool_pre_sync_plan(
        manifest_path=manifest_path,
        workflow_name="day",
        anchor_date="2026-05-20",
    )
    store = ArxivPoolStore(pool_path)
    for index, window in enumerate(plan.windows):
        _record_completed_window(store, window, arxiv_id=f"2605.20{index:03d}v1")

    import recoleta.arxiv_pool as arxiv_pool_module
    import recoleta.cli.fleet as fleet_module

    monkeypatch.setattr(
        arxiv_pool_module,
        "_utc_now",
        lambda: datetime(2026, 5, 20, 12, tzinfo=UTC),
    )
    events: list[str] = []

    def fake_pre_sync(pre_sync_plan):  # type: ignore[no-untyped-def]
        events.append("pre_sync")
        return ArxivPoolSyncResult(
            requested_windows_total=len(pre_sync_plan.windows),
            cache_hit_total=len(pre_sync_plan.windows),
        )

    def fake_child_payload(*, request):  # type: ignore[no-untyped-def]
        raise AssertionError("strict readiness should stop before children")

    monkeypatch.setattr(fleet_module, "run_fleet_arxiv_pool_pre_sync", fake_pre_sync)
    monkeypatch.setattr(
        fleet_module,
        "_fleet_granularity_child_payload",
        fake_child_payload,
    )

    with pytest.raises(typer.Exit) as exc:
        execute_fleet_granularity_workflow(
            manifest_path=manifest_path,
            workflow_name="day",
            command="fleet run day",
            anchor_date="2026-05-20",
            skip="analyze",
            json_output=True,
        )

    emitted = json.loads(capsys.readouterr().out.strip().splitlines()[-1])
    assert exc.value.exit_code == 1
    assert events == ["pre_sync"]
    assert emitted["status"] == "blocked"
    assert emitted["arxiv_pool_readiness"]["status"] == "blocked"
    assert emitted["arxiv_pool_readiness"]["immature_windows_total"] == 2


@pytest.mark.parametrize(
    ("workflow_name", "command"),
    [
        ("week", "fleet run week"),
        ("month", "fleet run month"),
    ],
)
def test_fleet_arxiv_pool_readiness_blocks_periods_until_all_days_mature(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    workflow_name: str,
    command: str,
) -> None:
    manifest_path, pool_path = _write_pool_fleet_manifest(tmp_path)
    plan = build_fleet_arxiv_pool_pre_sync_plan(
        manifest_path=manifest_path,
        workflow_name=workflow_name,
        anchor_date="2026-05-20",
    )
    store = ArxivPoolStore(pool_path)
    for index, window in enumerate(plan.windows):
        _record_completed_window(store, window, arxiv_id=f"2605.{index:05d}v1")

    import recoleta.arxiv_pool as arxiv_pool_module
    import recoleta.cli.fleet as fleet_module

    monkeypatch.setattr(
        arxiv_pool_module,
        "_utc_now",
        lambda: datetime(2026, 5, 20, 12, tzinfo=UTC),
    )
    monkeypatch.setattr(
        fleet_module,
        "run_fleet_arxiv_pool_pre_sync",
        lambda pre_sync_plan: ArxivPoolSyncResult(
            requested_windows_total=len(pre_sync_plan.windows),
            cache_hit_total=len(pre_sync_plan.windows),
        ),
    )
    monkeypatch.setattr(
        fleet_module,
        "_fleet_granularity_child_payload",
        lambda *, request: pytest.fail("strict readiness should stop before children"),
    )

    with pytest.raises(typer.Exit) as exc:
        execute_fleet_granularity_workflow(
            manifest_path=manifest_path,
            workflow_name=workflow_name,
            command=command,
            anchor_date="2026-05-20",
            json_output=True,
        )

    emitted = json.loads(capsys.readouterr().out.strip().splitlines()[-1])
    assert exc.value.exit_code == 1
    assert emitted["arxiv_pool_readiness"]["status"] == "blocked"
    assert emitted["arxiv_pool_readiness"]["immature_windows_total"] > 0


def test_fleet_arxiv_pool_readiness_warn_mode_continues(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    manifest_path, pool_path = _write_pool_fleet_manifest(
        tmp_path,
        readiness_gate="warn",
    )
    plan = build_fleet_arxiv_pool_pre_sync_plan(
        manifest_path=manifest_path,
        workflow_name="day",
        anchor_date="2026-05-20",
    )
    store = ArxivPoolStore(pool_path)
    for index, window in enumerate(plan.windows):
        _record_completed_window(store, window, arxiv_id=f"2605.21{index:03d}v1")

    import recoleta.arxiv_pool as arxiv_pool_module
    import recoleta.cli.fleet as fleet_module

    monkeypatch.setattr(
        arxiv_pool_module,
        "_utc_now",
        lambda: datetime(2026, 5, 20, 12, tzinfo=UTC),
    )
    events: list[str] = []

    def fake_pre_sync(pre_sync_plan):  # type: ignore[no-untyped-def]
        events.append("pre_sync")
        return ArxivPoolSyncResult(
            requested_windows_total=len(pre_sync_plan.windows),
            cache_hit_total=len(pre_sync_plan.windows),
        )

    def fake_child_payload(*, request):  # type: ignore[no-untyped-def]
        events.append(f"child:{request.instance.name}")
        return {
            "instance": request.instance.name,
            "config_path": str(request.instance.config_path),
        }

    monkeypatch.setattr(fleet_module, "run_fleet_arxiv_pool_pre_sync", fake_pre_sync)
    monkeypatch.setattr(
        fleet_module,
        "_fleet_granularity_child_payload",
        fake_child_payload,
    )

    payload = execute_fleet_granularity_workflow(
        manifest_path=manifest_path,
        workflow_name="day",
        command="fleet run day",
        anchor_date="2026-05-20",
        json_output=False,
    )

    assert events == ["pre_sync", "child:embodied_ai", "child:software"]
    assert payload["status"] == "ok"
    assert payload["arxiv_pool_readiness"]["status"] == "blocked"
    assert payload["arxiv_pool_readiness"]["immature_windows_total"] == 2


def _write_pool_fleet_manifest(
    tmp_path: Path,
    *,
    readiness_gate: str | tuple[str, str] = "strict",
    maturity_lag_days: int | tuple[int, int] = 1,
    allow_immature_windows: bool | tuple[bool, bool] = False,
    request_interval_seconds: float | tuple[float, float] = 0,
    cooldown_seconds: int | tuple[int, int] = 3600,
) -> tuple[Path, Path]:
    pool_path = tmp_path / "fleet-arxiv-pool.db"
    child_paths: list[Path] = []
    for index, (name, query) in enumerate(
        (("embodied_ai", "cat:cs.AI"), ("software", "cat:cs.LG"))
    ):
        child_path = tmp_path / f"{name}.yaml"
        child_path.write_text(
            yaml.safe_dump(
                {
                    "RECOLETA_DB_PATH": str(tmp_path / f"{name}.db"),
                    "LLM_MODEL": "openai/gpt-4o-mini",
                    "PUBLISH_TARGETS": ["markdown"],
                    "ARXIV_POOL": {
                        "enabled": True,
                        "db_path": str(pool_path),
                        "request_interval_seconds": _child_setting(
                            request_interval_seconds, index
                        ),
                        "cooldown_seconds": _child_setting(cooldown_seconds, index),
                        "maturity_lag_days": _child_setting(maturity_lag_days, index),
                        "readiness_gate": _child_setting(readiness_gate, index),
                        "allow_immature_windows": _child_setting(
                            allow_immature_windows, index
                        ),
                    },
                    "SOURCES": {
                        "arxiv": {
                            "enabled": True,
                            "mode": "pool",
                            "queries": [query],
                            "max_results_per_run": 60,
                        }
                    },
                }
            ),
            encoding="utf-8",
        )
        child_paths.append(child_path)
    manifest_path = tmp_path / "fleet.yaml"
    manifest_path.write_text(
        yaml.safe_dump(
            {
                "schema_version": 1,
                "instances": [
                    {"name": "embodied_ai", "config_path": str(child_paths[0])},
                    {"name": "software", "config_path": str(child_paths[1])},
                ],
            }
        ),
        encoding="utf-8",
    )
    return manifest_path, pool_path


def _child_setting(value: Any, index: int) -> Any:
    if isinstance(value, tuple):
        return value[index]
    return value


def _write_pool_config(*, tmp_path: Path, pool_path: Path) -> Path:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        yaml.safe_dump(
            {
                "RECOLETA_DB_PATH": str(tmp_path / "recoleta.db"),
                "LLM_MODEL": "openai/gpt-4o-mini",
                "PUBLISH_TARGETS": ["markdown"],
                "ARXIV_POOL": {
                    "enabled": True,
                    "db_path": str(pool_path),
                    "request_interval_seconds": 0,
                },
                "SOURCES": {
                    "arxiv": {
                        "enabled": True,
                        "mode": "pool",
                        "queries": ["cat:cs.AI"],
                        "max_results_per_run": 60,
                    }
                },
            }
        ),
        encoding="utf-8",
    )
    return config_path


def _write_huldra_pool_config(*, tmp_path: Path, base_url: str) -> Path:
    config_path = tmp_path / "huldra-config.yaml"
    config_path.write_text(
        yaml.safe_dump(
            {
                "RECOLETA_DB_PATH": str(tmp_path / "recoleta.db"),
                "LLM_MODEL": "openai/gpt-4o-mini",
                "PUBLISH_TARGETS": ["markdown"],
                "ARXIV_POOL": {
                    "enabled": True,
                    "backend": "huldra",
                    "huldra_base_url": base_url,
                    "huldra_request_timeout_seconds": 5,
                },
                "SOURCES": {
                    "arxiv": {
                        "enabled": True,
                        "mode": "pool",
                        "queries": ["cat:cs.AI"],
                        "max_results_per_run": 60,
                    }
                },
            }
        ),
        encoding="utf-8",
    )
    return config_path


def _write_huldra_fleet_manifest(
    tmp_path: Path,
    *,
    base_urls: tuple[str, str],
    queries: tuple[str, str] = ("cat:cs.AI", "cat:cs.LG"),
    huldra_request_timeout_seconds: tuple[float, float] = (30.0, 30.0),
    huldra_wait_timeout_seconds: tuple[float | None, float | None] = (None, None),
) -> Path:
    child_paths: list[Path] = []
    for index, name in enumerate(("embodied_ai", "software")):
        query = queries[index]
        child_path = tmp_path / f"{name}.yaml"
        arxiv_pool_config: dict[str, Any] = {
            "enabled": True,
            "backend": "huldra",
            "huldra_base_url": base_urls[index],
            "huldra_request_timeout_seconds": huldra_request_timeout_seconds[index],
        }
        wait_timeout = huldra_wait_timeout_seconds[index]
        if wait_timeout is not None:
            arxiv_pool_config["huldra_wait_timeout_seconds"] = wait_timeout
        child_path.write_text(
            yaml.safe_dump(
                {
                    "RECOLETA_DB_PATH": str(tmp_path / f"{name}.db"),
                    "LLM_MODEL": "openai/gpt-4o-mini",
                    "PUBLISH_TARGETS": ["markdown"],
                    "ARXIV_POOL": arxiv_pool_config,
                    "SOURCES": {
                        "arxiv": {
                            "enabled": True,
                            "mode": "pool",
                            "queries": [query],
                            "max_results_per_run": 60,
                        }
                    },
                }
            ),
            encoding="utf-8",
        )
        child_paths.append(child_path)
    return _write_manifest_for_children(tmp_path, child_paths)


def _write_mixed_backend_fleet_manifest(tmp_path: Path) -> Path:
    local_path = tmp_path / "local.yaml"
    local_path.write_text(
        yaml.safe_dump(
            {
                "RECOLETA_DB_PATH": str(tmp_path / "local.db"),
                "LLM_MODEL": "openai/gpt-4o-mini",
                "PUBLISH_TARGETS": ["markdown"],
                "ARXIV_POOL": {
                    "enabled": True,
                    "backend": "local_sqlite",
                    "db_path": str(tmp_path / "arxiv_pool.db"),
                },
                "SOURCES": {
                    "arxiv": {
                        "enabled": True,
                        "mode": "pool",
                        "queries": ["cat:cs.AI"],
                    }
                },
            }
        ),
        encoding="utf-8",
    )
    huldra_path = _write_huldra_pool_config(
        tmp_path=tmp_path,
        base_url="http://127.0.0.1:8765",
    )
    return _write_manifest_for_children(tmp_path, [local_path, huldra_path])


def _write_multiple_local_pool_fleet_manifest(tmp_path: Path) -> Path:
    child_paths: list[Path] = []
    for index, (name, query) in enumerate(
        (("embodied_ai", "cat:cs.AI"), ("software", "cat:cs.LG"))
    ):
        child_path = tmp_path / f"{name}.yaml"
        child_path.write_text(
            yaml.safe_dump(
                {
                    "RECOLETA_DB_PATH": str(tmp_path / f"{name}.db"),
                    "LLM_MODEL": "openai/gpt-4o-mini",
                    "PUBLISH_TARGETS": ["markdown"],
                    "ARXIV_POOL": {
                        "enabled": True,
                        "backend": "local_sqlite",
                        "db_path": str(tmp_path / f"arxiv_pool_{index}.db"),
                    },
                    "SOURCES": {
                        "arxiv": {
                            "enabled": True,
                            "mode": "pool",
                            "queries": [query],
                        }
                    },
                }
            ),
            encoding="utf-8",
        )
        child_paths.append(child_path)
    return _write_manifest_for_children(tmp_path, child_paths)


def _write_manifest_for_children(tmp_path: Path, child_paths: list[Path]) -> Path:
    manifest_path = tmp_path / f"fleet-{len(child_paths)}.yaml"
    manifest_path.write_text(
        yaml.safe_dump(
            {
                "schema_version": 1,
                "instances": [
                    {"name": f"child-{index}", "config_path": str(path)}
                    for index, path in enumerate(child_paths)
                ],
            }
        ),
        encoding="utf-8",
    )
    return manifest_path
