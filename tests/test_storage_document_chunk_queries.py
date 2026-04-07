from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

from recoleta.storage import Repository


def test_list_summary_chunks_in_period_preserves_granularity_filter(
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()

    week_start = datetime(2026, 3, 2, tzinfo=UTC)
    week_end = week_start + timedelta(days=7)
    day_start = week_start
    day_end = day_start + timedelta(days=1)

    week_doc = repository.upsert_document_for_trend(
        granularity="week",
        period_start=week_start,
        period_end=week_end,
        title="Weekly trend",
    )
    day_doc = repository.upsert_document_for_trend(
        granularity="day",
        period_start=day_start,
        period_end=day_end,
        title="Daily trend",
    )
    repository.upsert_document_chunk(
        doc_id=int(week_doc.id or 0),
        chunk_index=0,
        kind="summary",
        text_value="Weekly summary",
        source_content_type="trend_summary",
    )
    repository.upsert_document_chunk(
        doc_id=int(day_doc.id or 0),
        chunk_index=0,
        kind="summary",
        text_value="Daily summary",
        source_content_type="trend_summary",
    )

    rows = repository.list_summary_chunks_in_period(
        doc_type="trend",
        granularity="week",
        period_start=week_start,
        period_end=week_end,
        limit=10,
    )

    assert [int(row.doc_id) for row in rows] == [int(week_doc.id or 0)]
