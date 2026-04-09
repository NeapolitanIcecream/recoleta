from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from scripts import bench_trends_hotspots as bench
from recoleta.storage import Repository
from recoleta.trends import day_period_bounds


def _seed_indexable_repository(
    *,
    root: Path,
) -> tuple[Repository, datetime, datetime, list[int], dict[str, Any]]:
    repository = bench._build_repository(root=root)
    period_start, period_end = day_period_bounds(
        datetime(2026, 3, 5, tzinfo=UTC).date()
    )
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


def test_index_items_batched_materializes_summary_and_content_chunks(
    tmp_path: Path,
) -> None:
    repository, period_start, period_end, item_doc_ids, result = (
        _seed_indexable_repository(root=tmp_path)
    )

    assert result["stats"]["items_total"] == 3
    assert result["stats"]["docs_upserted"] == 3
    assert result["stats"]["chunks_upserted"] >= 6
    assert len(item_doc_ids) == 3
    summary_chunk = repository.read_document_chunk(
        doc_id=item_doc_ids[0], chunk_index=0
    )
    content_chunk = repository.read_document_chunk(
        doc_id=item_doc_ids[0], chunk_index=1
    )
    assert summary_chunk is not None
    assert summary_chunk.kind == "summary"
    assert content_chunk is not None
    assert content_chunk.kind == "content"
