from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from scripts import bench_trends_hotspots as bench
from recoleta.storage import Repository
from recoleta.trends import TrendCluster, TrendPayload, day_period_bounds


def _seed_indexable_repository(
    *,
    root: Path,
) -> tuple[Repository, datetime, datetime, list[int], dict[str, Any]]:
    repository = bench._build_repository(root=root)
    period_start, period_end = day_period_bounds(datetime(2026, 3, 5, tzinfo=UTC).date())
    bench._seed_analyzed_items(
        repository,
        period_start=period_start,
        items=3,
        content_chars=2600,
    )
    result = bench._index_items_batched(
        request=bench._IndexBatchRequest(
            repository=repository,
            period_start=period_start,
            period_end=period_end,
        )
    )
    item_doc_ids = [
        int(document.id)
        for document in bench._list_item_documents(
            repository,
            period_start=period_start,
            period_end=period_end,
        )
        if document.id is not None
    ]
    return repository, period_start, period_end, item_doc_ids, result


def test_index_items_batched_materializes_summary_and_content_chunks(tmp_path: Path) -> None:
    repository, period_start, period_end, item_doc_ids, result = (
        _seed_indexable_repository(root=tmp_path)
    )

    assert result["stats"]["items_total"] == 3
    assert result["stats"]["docs_upserted"] == 3
    assert result["stats"]["chunks_upserted"] >= 6
    assert len(item_doc_ids) == 3
    summary_chunk = repository.read_document_chunk(doc_id=item_doc_ids[0], chunk_index=0)
    content_chunk = repository.read_document_chunk(doc_id=item_doc_ids[0], chunk_index=1)
    assert summary_chunk is not None
    assert summary_chunk.kind == "summary"
    assert content_chunk is not None
    assert content_chunk.kind == "content"


def test_run_stage_rep_enforcement_like_current_backfills_text_results(
    tmp_path: Path,
) -> None:
    repository, period_start, period_end, item_doc_ids, _ = _seed_indexable_repository(
        root=tmp_path
    )
    trend_doc_ids = bench._seed_trend_documents(
        repository,
        period_start=period_start,
        trend_docs=1,
    )
    payload = TrendPayload(
        title="Bench Trends",
        granularity="day",
        period_start=period_start.isoformat(),
        period_end=period_end.isoformat(),
        overview_md="- Bench overview",
        topics=["agents"],
        clusters=[
            TrendCluster(
                name="agents retrieval",
                description="memory routing benchmark",
                representative_doc_ids=[],
                representative_chunks=[
                    TrendCluster.RepresentativeChunk(
                        doc_id=trend_doc_ids[0],
                        chunk_index=0,
                        score=0.8,
                    )
                ],
            )
        ],
        highlights=[],
    )

    result = bench._run_stage_rep_enforcement_like_current(
        request=bench._RepresentativeEnforcementRequest(
            repository=repository,
            payload=payload,
            lancedb_dir=tmp_path / "lancedb",
            run_id="bench-text-backfill",
            period_start=period_start,
            period_end=period_end,
            embedding_model="bench/embedding",
            embedding_dimensions=16,
        )
    )

    assert result["dropped_non_item_total"] == 1
    assert result["backfilled_total"] == 1
    assert result["text_search_calls"] >= 1
    assert result["semantic_search_calls"] == 0
    representatives = payload.clusters[0].representative_chunks
    assert representatives
    assert representatives[0].doc_id in item_doc_ids
    representative_doc = repository.get_document(doc_id=representatives[0].doc_id)
    assert representative_doc is not None
    assert representative_doc.doc_type == "item"


def test_run_stage_rep_enforcement_like_current_uses_semantic_backfill_when_text_misses(
    monkeypatch,
    tmp_path: Path,
) -> None:
    repository, period_start, period_end, item_doc_ids, _ = _seed_indexable_repository(
        root=tmp_path
    )
    trend_doc_ids = bench._seed_trend_documents(
        repository,
        period_start=period_start,
        trend_docs=1,
    )
    payload = TrendPayload(
        title="Bench Trends",
        granularity="day",
        period_start=period_start.isoformat(),
        period_end=(period_start + timedelta(days=1)).isoformat(),
        overview_md="- Bench overview",
        topics=["agents"],
        clusters=[
            TrendCluster(
                name="zxqv semantic only",
                description="unmatched query",
                representative_doc_ids=[],
                representative_chunks=[
                    TrendCluster.RepresentativeChunk(
                        doc_id=trend_doc_ids[0],
                        chunk_index=0,
                        score=0.8,
                    )
                ],
            )
        ],
        highlights=[],
    )

    monkeypatch.setattr(
        bench,
        "semantic_search_summaries_in_period",
        lambda **kwargs: [  # noqa: ARG005
            SimpleNamespace(doc_id=item_doc_ids[0], chunk_index=0, score=0.77)
        ],
    )

    result = bench._run_stage_rep_enforcement_like_current(
        request=bench._RepresentativeEnforcementRequest(
            repository=repository,
            payload=payload,
            lancedb_dir=tmp_path / "lancedb",
            run_id="bench-semantic-backfill",
            period_start=period_start,
            period_end=period_end,
            embedding_model="bench/embedding",
            embedding_dimensions=16,
        )
    )

    assert result["dropped_non_item_total"] == 1
    assert result["backfilled_total"] == 1
    assert result["semantic_search_calls"] == 1
    representatives = payload.clusters[0].representative_chunks
    assert representatives[0].doc_id == item_doc_ids[0]
    assert representatives[0].score == 0.77
