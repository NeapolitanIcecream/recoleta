from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

import httpx
import pytest

from recoleta.arxiv_pool import (
    ArxivPoolPaper,
    ArxivPoolReadinessPolicy,
    ArxivPoolStore,
    ArxivPoolWindow,
    HuldraArxivPoolBackend,
    build_arxiv_pool_windows_for_days,
    evaluate_arxiv_pool_readiness,
    pool_paper_to_item_draft,
)
from recoleta.sources import ArxivPullRequest, SourcePullResult, fetch_arxiv_drafts
from tests.spec_support import (
    FakeHuldraArxivPaper as ArxivPaper,
    FakeHuldraArxivResult as ArxivResult,
    install_fake_huldra,
)


@pytest.fixture(autouse=True)
def _fake_huldra_dependency(monkeypatch: pytest.MonkeyPatch) -> None:
    install_fake_huldra(monkeypatch)


def _window() -> ArxivPoolWindow:
    return ArxivPoolWindow(
        query_text="cat:cs.AI AND all:agent",
        period_start=datetime(2026, 5, 20, tzinfo=UTC),
        period_end=datetime(2026, 5, 21, tzinfo=UTC),
        max_results=60,
    )


def _paper(
    arxiv_id: str = "2605.20001v1",
    *,
    published_at: datetime | None = None,
) -> ArxivPaper:
    return ArxivPaper(
        arxiv_id=arxiv_id,
        version=1,
        canonical_url=f"https://arxiv.org/abs/{arxiv_id}",
        title="Huldra Paper",
        abstract="Abstract.",
        authors=["Ada Lovelace"],
        primary_category="cs.AI",
        categories=["cs.AI", "cs.LG"],
        published_at=published_at or datetime(2026, 5, 20, 12, tzinfo=UTC),
        comment="12 pages",
        journal_ref="Journal Demo",
        doi="10.1234/demo",
        raw_atom={"entry_id": f"https://arxiv.org/abs/{arxiv_id}"},
    )


def _pool_paper(
    arxiv_id: str = "2605.20001v1",
    *,
    published_at: datetime | None = None,
) -> ArxivPoolPaper:
    paper = _paper(arxiv_id, published_at=published_at)
    return ArxivPoolPaper(
        arxiv_id=paper.arxiv_id,
        version=paper.version,
        canonical_url=paper.canonical_url,
        title=paper.title,
        abstract=paper.abstract,
        authors=list(paper.authors),
        primary_category=paper.primary_category,
        categories=list(paper.categories),
        published_at=paper.published_at,
        updated_at=paper.updated_at,
        comment=paper.comment,
        journal_ref=paper.journal_ref,
        doi=paper.doi,
        raw_atom=dict(paper.raw_atom),
    )


def _result(
    *,
    status: str,
    cache_readable: bool,
    mature: bool,
    analysis_ready: bool,
    papers: list[ArxivPaper] | None = None,
    blocked_reason: str | None = None,
) -> ArxivResult:
    return ArxivResult(
        serving_mode="analysis_ready",
        status=status,
        cache_key="huldra:v1:cache",
        cache_readable=cache_readable,
        mature=mature,
        analysis_ready=analysis_ready,
        ready=analysis_ready,
        papers=papers or [],
        papers_total=len(papers or []),
        cached_papers_total=len(papers or []),
        blocked_reason=blocked_reason,
    )


class _FakeHuldraClient:
    def __init__(self, *results: Any) -> None:
        self.results = list(results)
        self.requests: list[Any] = []

    def ensure(self, request: Any) -> Any:
        self.requests.append(request)
        result = self.results.pop(0)
        if isinstance(result, BaseException):
            raise result
        return result


def test_huldra_ready_result_returns_pool_papers_and_cache_only_request() -> None:
    client = _FakeHuldraClient(
        _result(
            status="ready",
            cache_readable=True,
            mature=True,
            analysis_ready=True,
            papers=[_paper()],
        )
    )
    backend = HuldraArxivPoolBackend(
        base_url="http://127.0.0.1:8765",
        request_timeout_seconds=12,
        client=client,
    )

    pull = backend.cached_papers_for_window(
        _window(),
        readiness_policy=ArxivPoolReadinessPolicy(maturity_lag_days=1),
    )

    assert pull.complete is True
    assert pull.readiness.cache_status == "completed"
    assert [paper.arxiv_id for paper in pull.papers or []] == ["2605.20001v1"]
    request = client.requests[0]
    assert request.search_query == "cat:cs.AI AND all:agent"
    assert "submittedDate" not in request.search_query
    assert request.submitted_start == datetime(2026, 5, 20, tzinfo=UTC)
    assert request.submitted_end == datetime(2026, 5, 21, tzinfo=UTC)
    assert request.cache_policy == "cache_only"
    assert request.readiness == "analysis_ready"
    assert request.maturity_lag_days == 1
    assert request.timeout_seconds == 12


def test_huldra_immature_analysis_ready_result_emits_no_papers() -> None:
    client = _FakeHuldraClient(
        _result(
            status="immature",
            cache_readable=True,
            mature=False,
            analysis_ready=False,
            blocked_reason="immature_window",
        )
    )
    backend = HuldraArxivPoolBackend(
        base_url="http://127.0.0.1:8765",
        client=client,
    )

    pull = backend.cached_papers_for_window(
        _window(),
        readiness_policy=ArxivPoolReadinessPolicy(maturity_lag_days=1),
    )

    assert pull.complete is False
    assert pull.papers is None
    assert pull.readiness.cache_status == "completed"
    assert pull.readiness.blocked_reason == "immature_window"


def test_huldra_unsafe_override_reads_raw_completed_papers() -> None:
    client = _FakeHuldraClient(
        _result(
            status="immature",
            cache_readable=True,
            mature=False,
            analysis_ready=False,
            papers=[_paper()],
            blocked_reason="immature_window",
        )
    )
    backend = HuldraArxivPoolBackend(
        base_url="http://127.0.0.1:8765",
        client=client,
    )

    pull = backend.cached_papers_for_window(
        _window(),
        readiness_policy=ArxivPoolReadinessPolicy(
            maturity_lag_days=1,
            allow_immature_windows=True,
        ),
    )

    assert pull.complete is True
    assert [paper.arxiv_id for paper in pull.papers or []] == ["2605.20001v1"]
    assert client.requests[0].readiness == "raw_completed"
    assert pull.readiness.mature is False
    assert pull.readiness.analysis_ready is False


@pytest.mark.parametrize(
    ("readiness_gate", "allow_immature_windows", "expected_readiness"),
    [
        ("strict", False, "analysis_ready"),
        ("warn", False, "analysis_ready"),
        ("off", False, "raw_completed"),
        ("strict", True, "raw_completed"),
    ],
)
def test_huldra_request_readiness_follows_recoleta_unsafe_policy(
    readiness_gate: str,
    allow_immature_windows: bool,
    expected_readiness: str,
) -> None:
    client = _FakeHuldraClient(
        _result(
            status="cache_miss",
            cache_readable=False,
            mature=False,
            analysis_ready=False,
            blocked_reason="cache_miss",
        )
    )
    backend = HuldraArxivPoolBackend(
        base_url="http://127.0.0.1:8765",
        client=client,
    )

    backend.cached_papers_for_window(
        _window(),
        readiness_policy=ArxivPoolReadinessPolicy(
            maturity_lag_days=1,
            readiness_gate=readiness_gate,
            allow_immature_windows=allow_immature_windows,
        ),
    )

    assert client.requests[0].readiness == expected_readiness


@pytest.mark.parametrize(
    ("status", "raw_blocked_reason", "cache_status", "blocked_reason"),
    [
        ("queued", None, "queued", "queued_window"),
        ("cooling_down", "cooldown", "rate_limited", "rate_limited_window"),
        ("failed", None, "failed", "failed_window"),
        ("timeout", "timeout", "timeout", "timeout_window"),
        ("skipped", None, "skipped", "skipped_window"),
    ],
)
def test_huldra_unavailable_statuses_map_to_recoleta_readiness(
    status: str,
    raw_blocked_reason: str | None,
    cache_status: str,
    blocked_reason: str,
) -> None:
    backend = HuldraArxivPoolBackend(
        base_url="http://127.0.0.1:8765",
        client=_FakeHuldraClient(
            _result(
                status=status,
                cache_readable=False,
                mature=False,
                analysis_ready=False,
                blocked_reason=raw_blocked_reason,
            )
        ),
    )

    pull = backend.cached_papers_for_window(
        _window(),
        readiness_policy=ArxivPoolReadinessPolicy(),
    )

    assert pull.complete is False
    assert pull.papers is None
    assert pull.readiness.cache_status == cache_status
    assert pull.readiness.serving_status == status
    assert pull.readiness.blocked_reason == blocked_reason
    assert pull.readiness.unavailable is True


def test_huldra_malformed_response_records_structured_failure() -> None:
    class MalformedResult:
        status = "ready"
        cache_key = "huldra:v1:cache"
        cache_readable = True
        mature = True
        analysis_ready = True

    backend = HuldraArxivPoolBackend(
        base_url="http://127.0.0.1:8765",
        client=_FakeHuldraClient(MalformedResult()),
    )

    pull = backend.cached_papers_for_window(
        _window(),
        readiness_policy=ArxivPoolReadinessPolicy(),
    )

    assert pull.complete is False
    assert pull.papers is None
    assert pull.readiness.cache_status == "failed"
    assert pull.readiness.blocked_reason == "malformed_huldra_response"
    assert pull.readiness.diagnostic is not None
    assert pull.readiness.diagnostic["backend"] == "huldra"
    assert pull.readiness.diagnostic["error_type"] == "AttributeError"


def test_huldra_unavailable_and_unreachable_windows_are_structured() -> None:
    cache_miss = _FakeHuldraClient(
        _result(
            status="cache_miss",
            cache_readable=False,
            mature=False,
            analysis_ready=False,
            blocked_reason="cache_miss",
        )
    )
    missing = HuldraArxivPoolBackend(
        base_url="http://127.0.0.1:8765",
        client=cache_miss,
    ).cached_papers_for_window(
        _window(),
        readiness_policy=ArxivPoolReadinessPolicy(),
    )

    assert missing.complete is False
    assert missing.readiness.cache_status == "missing"
    assert missing.readiness.blocked_reason == "missing_window"

    unreachable = HuldraArxivPoolBackend(
        base_url="http://127.0.0.1:8765",
        client=_FakeHuldraClient(httpx.ConnectError("offline")),
    ).cached_papers_for_window(
        _window(),
        readiness_policy=ArxivPoolReadinessPolicy(),
    )

    assert unreachable.complete is False
    assert unreachable.readiness.cache_status == "failed"
    assert unreachable.readiness.blocked_reason == "huldra_unreachable"


def test_huldra_source_puller_records_metrics_and_provenance() -> None:
    client = _FakeHuldraClient(
        _result(
            status="ready",
            cache_readable=True,
            mature=True,
            analysis_ready=True,
            papers=[_paper()],
        )
    )
    backend = HuldraArxivPoolBackend(
        base_url="http://127.0.0.1:8765",
        client=client,
    )

    result = fetch_arxiv_drafts(
        request=ArxivPullRequest(
            queries=["cat:cs.AI AND all:agent"],
            max_results_per_run=60,
            period_start=datetime(2026, 5, 20, tzinfo=UTC),
            period_end=datetime(2026, 5, 21, tzinfo=UTC),
            include_stats=True,
            mode="pool",
            pool_maturity_lag_days=1,
        ),
        pool_backend=backend,
    )

    assert isinstance(result, SourcePullResult)
    assert [draft.source_item_id for draft in result.drafts] == ["2605.20001v1"]
    assert result.extra_metrics["pool_window_analysis_ready_total"] == 1
    assert result.extra_metrics["pool_drafts_total"] == 1
    assert result.drafts[0].raw_metadata["huldra_cache_key"] == "huldra:v1:cache"
    assert result.diagnostics[0]["backend"] == "huldra"
    assert result.diagnostics[0]["record_status"] == "completed"
    assert result.diagnostics[0]["serving_status"] == "ready"


def test_huldra_source_puller_preserves_watermark_for_default_immature_window() -> None:
    client = _FakeHuldraClient(
        _result(
            status="immature",
            cache_readable=True,
            mature=False,
            analysis_ready=False,
            blocked_reason="immature_window",
        )
    )
    backend = HuldraArxivPoolBackend(
        base_url="http://127.0.0.1:8765",
        client=client,
    )
    watermark = datetime(2026, 5, 20, 1, tzinfo=UTC)

    result = fetch_arxiv_drafts(
        request=ArxivPullRequest(
            queries=["cat:cs.AI AND all:agent"],
            max_results_per_run=60,
            period_start=datetime(2026, 5, 20, tzinfo=UTC),
            period_end=datetime(2026, 5, 21, tzinfo=UTC),
            pull_state_lookup=lambda *_: _snapshot(watermark),
            include_stats=True,
            mode="pool",
            pool_maturity_lag_days=1,
        ),
        pool_backend=backend,
    )

    assert isinstance(result, SourcePullResult)
    assert result.drafts == []
    assert result.extra_metrics["pool_window_immature_total"] == 1
    assert result.state_updates[0].watermark_published_at == watermark


def test_huldra_source_puller_records_unsafe_immature_metrics_and_diagnostics() -> None:
    client = _FakeHuldraClient(
        _result(
            status="immature",
            cache_readable=True,
            mature=False,
            analysis_ready=False,
            papers=[_paper()],
            blocked_reason="immature_window",
        )
    )
    backend = HuldraArxivPoolBackend(
        base_url="http://127.0.0.1:8765",
        client=client,
    )

    result = fetch_arxiv_drafts(
        request=ArxivPullRequest(
            queries=["cat:cs.AI AND all:agent"],
            max_results_per_run=60,
            period_start=datetime(2026, 5, 20, tzinfo=UTC),
            period_end=datetime(2026, 5, 21, tzinfo=UTC),
            include_stats=True,
            mode="pool",
            pool_maturity_lag_days=1,
            pool_allow_immature_windows=True,
        ),
        pool_backend=backend,
    )

    assert isinstance(result, SourcePullResult)
    assert [draft.source_item_id for draft in result.drafts] == ["2605.20001v1"]
    assert result.extra_metrics["pool_window_immature_total"] == 1
    assert result.extra_metrics["pool_window_immature_allowed_total"] == 1
    assert result.extra_metrics["pool_drafts_total"] == 1
    assert result.diagnostics[0]["mature"] is False
    assert result.diagnostics[0]["analysis_ready"] is False
    assert result.diagnostics[0]["allow_immature_windows"] is True
    assert result.diagnostics[0]["blocked_reason"] == "immature_window"
    assert result.drafts[0].raw_metadata["huldra_cache_key"] == "huldra:v1:cache"


def test_huldra_and_local_sqlite_pool_parity_for_fixture_windows(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Proposal Step 7: Huldra must match local SQLite except additive cache key."""
    query = "cat:cs.AI AND all:agent"
    now = datetime(2026, 5, 21, 12, tzinfo=UTC)
    watermark = datetime(2026, 5, 18, 23, tzinfo=UTC)
    windows = build_arxiv_pool_windows_for_days(
        queries=[query],
        days=[date(2026, 5, 19), date(2026, 5, 20), date(2026, 5, 21)],
        max_results=60,
    )
    store = ArxivPoolStore(tmp_path / "arxiv_pool.db")
    store.record_completed_window(
        window=windows[0],
        papers=[
            _pool_paper(
                "2605.19001v1",
                published_at=windows[0].period_start + timedelta(hours=12),
            )
        ],
    )
    store.record_completed_window(
        window=windows[2],
        papers=[
            _pool_paper(
                "2605.21001v1",
                published_at=windows[2].period_start + timedelta(hours=12),
            )
        ],
    )

    import recoleta.source_pullers as source_pullers_module

    monkeypatch.setattr(source_pullers_module, "_source_pull_now", lambda: now)

    def request() -> ArxivPullRequest:
        return ArxivPullRequest(
            queries=[query],
            max_results_per_run=60,
            period_start=windows[0].period_start,
            period_end=windows[-1].period_end,
            pull_state_lookup=lambda *_: _snapshot(watermark),
            include_stats=True,
            mode="pool",
            pool_db_path=store.db_path,
            pool_maturity_lag_days=1,
        )

    def huldra_results() -> list[ArxivResult]:
        return [
            _result(
                status="ready",
                cache_readable=True,
                mature=True,
                analysis_ready=True,
                papers=[
                    _paper(
                        "2605.19001v1",
                        published_at=windows[0].period_start + timedelta(hours=12),
                    )
                ],
            ),
            _result(
                status="cache_miss",
                cache_readable=False,
                mature=True,
                analysis_ready=False,
                blocked_reason="cache_miss",
            ),
            _result(
                status="immature",
                cache_readable=True,
                mature=False,
                analysis_ready=False,
                papers=[
                    _paper(
                        "2605.21001v1",
                        published_at=windows[2].period_start + timedelta(hours=12),
                    )
                ],
                blocked_reason="immature_window",
            ),
        ]

    local_result = fetch_arxiv_drafts(
        request=request(),
        pool_backend=None,
    )
    huldra_result = fetch_arxiv_drafts(
        request=request(),
        pool_backend=HuldraArxivPoolBackend(
            base_url="http://127.0.0.1:8765",
            client=_FakeHuldraClient(*huldra_results()),
        ),
    )

    assert isinstance(local_result, SourcePullResult)
    assert isinstance(huldra_result, SourcePullResult)
    assert [draft.source_item_id for draft in local_result.drafts] == [
        "2605.19001v1"
    ]
    assert [draft.source_item_id for draft in huldra_result.drafts] == [
        "2605.19001v1"
    ]
    expected_metrics = {
        "pool_window_analysis_ready_total": 1,
        "pool_window_unavailable_total": 1,
        "pool_window_immature_total": 1,
        "pool_drafts_total": 1,
    }
    for result in (local_result, huldra_result):
        assert {
            key: int(result.extra_metrics.get(key) or 0)
            for key in expected_metrics
        } == expected_metrics
        assert result.state_updates[0].watermark_published_at == watermark

    local_metadata = local_result.drafts[0].raw_metadata
    huldra_metadata = huldra_result.drafts[0].raw_metadata
    assert set(huldra_metadata) - set(local_metadata) == {"huldra_cache_key"}
    assert {
        key: huldra_metadata[key]
        for key in local_metadata
    } == local_metadata

    policy = ArxivPoolReadinessPolicy(maturity_lag_days=1, now=now)
    local_readiness = evaluate_arxiv_pool_readiness(
        store=store,
        windows=windows,
        policy=policy,
    )
    huldra_readiness = evaluate_arxiv_pool_readiness(
        backend=HuldraArxivPoolBackend(
            base_url="http://127.0.0.1:8765",
            client=_FakeHuldraClient(*huldra_results()),
        ),
        windows=windows,
        policy=policy,
    )
    aggregate_keys = {
        "status",
        "windows_total",
        "analysis_ready_windows_total",
        "blocked_windows_total",
        "immature_windows_total",
        "unavailable_windows_total",
        "unsafe_override_windows_total",
    }
    assert {
        key: local_readiness[key]
        for key in aggregate_keys
    } == {key: huldra_readiness[key] for key in aggregate_keys}
    per_window_keys = {
        "query_text",
        "period_start",
        "period_end",
        "max_results",
        "status",
        "cache_readable",
        "mature",
        "analysis_ready",
        "blocked_reason",
    }
    assert [
        {key: window[key] for key in per_window_keys}
        for window in local_readiness["windows"]
    ] == [
        {key: window[key] for key in per_window_keys}
        for window in huldra_readiness["windows"]
    ]


def test_pool_paper_to_item_draft_applies_additive_huldra_metadata() -> None:
    draft = pool_paper_to_item_draft(
        paper=_pool_paper(),
        window=_window(),
        extra_raw_metadata={"huldra_cache_key": "huldra:v1:cache"},
    )

    assert draft.raw_metadata["journal_ref"] == "Journal Demo"
    assert draft.raw_metadata["doi"] == "10.1234/demo"
    assert draft.raw_metadata["huldra_cache_key"] == "huldra:v1:cache"


def _snapshot(watermark: datetime) -> Any:
    from recoleta.sources import SourcePullStateSnapshot

    return SourcePullStateSnapshot(
        scope_kind="query",
        scope_key="cat:cs.AI AND all:agent",
        watermark_published_at=watermark,
    )
