from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
import yaml

from recoleta.arxiv_pool import (
    ArxivPoolLeaseHeldError,
    ArxivPoolPaper,
    ArxivPoolRateLimitedError,
    ArxivPoolStore,
    ArxivPoolSync,
    ArxivPoolSyncResult,
    ArxivPoolWindow,
    build_arxiv_pool_windows,
)
from recoleta.cli.fleet import (
    build_fleet_arxiv_pool_pre_sync_plan,
    execute_fleet_granularity_workflow,
)
from recoleta.sources import ArxivPullRequest, SourcePullResult, fetch_arxiv_drafts


def _window(query: str = "cat:cs.AI") -> ArxivPoolWindow:
    return ArxivPoolWindow(
        query_text=query,
        period_start=datetime(2026, 4, 27, tzinfo=UTC),
        period_end=datetime(2026, 4, 28, tzinfo=UTC),
        max_results=60,
    )


def _paper(arxiv_id: str, *, title: str = "Pool Paper") -> ArxivPoolPaper:
    return ArxivPoolPaper(
        arxiv_id=arxiv_id,
        version=1,
        canonical_url=f"https://arxiv.org/abs/{arxiv_id}",
        title=title,
        abstract="An abstract.",
        authors=["Ada Lovelace", "Grace Hopper"],
        primary_category="cs.AI",
        categories=["cs.AI", "cs.LG"],
        published_at=datetime(2026, 4, 27, 12, tzinfo=UTC),
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


def test_arxiv_pool_429_records_cooldown_and_blocks_followup_requests(
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

    assert fetcher.calls == 1
    assert result.upstream_429_total == 1
    assert result.rate_limited_windows_total == 1
    assert recorded_window is not None
    assert recorded_window.status == "rate_limited"
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


def test_arxiv_api_fetcher_maps_arxiv_http_429_to_pool_rate_limit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import recoleta.arxiv_pool as pool_module

    class FakeClient:
        def results(self, search):  # noqa: ANN001
            _ = search
            raise pool_module.arxiv.HTTPError(
                url="https://export.arxiv.org/api/query",
                retry=0,
                status=429,
            )

    monkeypatch.setattr(pool_module.arxiv, "Client", FakeClient)

    with pytest.raises(ArxivPoolRateLimitedError):
        pool_module.ArxivApiFetcher().fetch(_window("cat:cs.AI"))


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
        )
    )

    assert isinstance(result, SourcePullResult)
    assert result.drafts == []
    assert result.extra_metrics["pool_window_unavailable_total"] == 1


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


def test_fleet_workflow_runs_pool_pre_sync_before_child_ingest(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    manifest_path, _pool_path = _write_pool_fleet_manifest(tmp_path)
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


def _write_pool_fleet_manifest(tmp_path: Path) -> tuple[Path, Path]:
    pool_path = tmp_path / "fleet-arxiv-pool.db"
    child_paths: list[Path] = []
    for name, query in (("embodied_ai", "cat:cs.AI"), ("software", "cat:cs.LG")):
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
                        "request_interval_seconds": 0,
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
