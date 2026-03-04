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
                representative_chunks=[{"score": 0.1}, {}],
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
    assert reps[0]["doc_id"] == 123
    assert reps[0]["chunk_index"] == 0
