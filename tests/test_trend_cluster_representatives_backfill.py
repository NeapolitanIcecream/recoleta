from __future__ import annotations

from datetime import UTC, datetime

from recoleta.rag import agent as rag_agent
from recoleta.trends import TrendCluster, TrendPayload


def test_trends_backfills_cluster_representatives_when_invalid() -> None:
    payload = TrendPayload(
        title="Daily Trend",
        granularity="day",
        period_start=datetime(2026, 3, 2, tzinfo=UTC).isoformat(),
        period_end=datetime(2026, 3, 3, tzinfo=UTC).isoformat(),
        overview_md="- overview",
        topics=["agents"],
        clusters=[
            TrendCluster(
                name="cluster-a",
                description="agents and tools",
                representative_doc_ids=[],
                representative_chunks=[],
            )
        ],
        highlights=[],
    )

    def fake_search(query: str, limit: int) -> list[dict[str, object]]:
        assert "cluster-a" in query
        assert limit == 6
        return [
            {"doc_id": 123, "chunk_index": 0, "score": 0.42},
            {"doc_id": 124, "chunk_index": 0, "score": 0.41},
        ]

    stats = rag_agent.ensure_trend_cluster_representatives(
        payload=payload, search=fake_search, max_reps=6
    )
    assert stats["clusters_backfilled_total"] == 1
    reps = payload.clusters[0].representative_chunks
    assert reps
    assert reps[0].doc_id == 123
    assert reps[0].chunk_index == 0


def test_trends_backfill_falls_back_to_doc_ids_when_search_errors() -> None:
    """Regression: representative search failures should still degrade to doc-id fallback."""

    payload = TrendPayload(
        title="Daily Trend",
        granularity="day",
        period_start=datetime(2026, 3, 2, tzinfo=UTC).isoformat(),
        period_end=datetime(2026, 3, 3, tzinfo=UTC).isoformat(),
        overview_md="- overview",
        topics=["agents"],
        clusters=[
            TrendCluster(
                name="cluster-a",
                description="agents and tools",
                representative_doc_ids=[321],
                representative_chunks=[],
            )
        ],
        highlights=[],
    )

    def exploding_search(query: str, limit: int) -> list[dict[str, object]]:
        _ = (query, limit)
        raise RuntimeError("transient search failure")

    stats = rag_agent.ensure_trend_cluster_representatives(
        payload=payload,
        search=exploding_search,
        max_reps=6,
    )

    assert stats["clusters_backfilled_total"] == 1
    reps = payload.clusters[0].representative_chunks
    assert reps
    assert reps[0].doc_id == 321
    assert reps[0].chunk_index == 0


def test_trends_backfill_legacy_wrapper_preserves_explicit_max_reps_zero() -> None:
    """Regression: max_reps=0 must keep backfill disabled in the legacy wrapper."""

    payload = TrendPayload(
        title="Daily Trend",
        granularity="day",
        period_start=datetime(2026, 3, 2, tzinfo=UTC).isoformat(),
        period_end=datetime(2026, 3, 3, tzinfo=UTC).isoformat(),
        overview_md="- overview",
        topics=["agents"],
        clusters=[
            TrendCluster(
                name="cluster-a",
                description="agents and tools",
                representative_doc_ids=[321],
                representative_chunks=[],
            )
        ],
        highlights=[],
    )
    search_calls: list[tuple[str, int]] = []

    def fake_search(query: str, limit: int) -> list[dict[str, object]]:
        search_calls.append((query, limit))
        return [{"doc_id": 123, "chunk_index": 0, "score": 0.42}]

    stats = rag_agent.ensure_trend_cluster_representatives(
        payload=payload,
        search=fake_search,
        max_reps=0,
    )

    assert stats["clusters_backfilled_total"] == 0
    assert stats["reps_backfilled_total"] == 0
    assert payload.clusters[0].representative_chunks == []
    assert search_calls == []


def test_trends_backfill_skips_non_dict_search_rows_and_falls_back_to_doc_ids() -> None:
    """Regression: legacy search callbacks may return non-dict rows without aborting backfill."""

    payload = TrendPayload(
        title="Daily Trend",
        granularity="day",
        period_start=datetime(2026, 3, 2, tzinfo=UTC).isoformat(),
        period_end=datetime(2026, 3, 3, tzinfo=UTC).isoformat(),
        overview_md="- overview",
        topics=["agents"],
        clusters=[
            TrendCluster(
                name="cluster-a",
                description="agents and tools",
                representative_doc_ids=[456],
                representative_chunks=[],
            )
        ],
        highlights=[],
    )

    def fake_search(query: str, limit: int) -> list[object]:
        assert "cluster-a" in query
        assert limit == 6
        return [object()]

    stats = rag_agent.ensure_trend_cluster_representatives(
        payload=payload,
        search=fake_search,
        max_reps=6,
    )

    assert stats["clusters_backfilled_total"] == 1
    reps = payload.clusters[0].representative_chunks
    assert reps
    assert reps[0].doc_id == 456
    assert reps[0].chunk_index == 0
