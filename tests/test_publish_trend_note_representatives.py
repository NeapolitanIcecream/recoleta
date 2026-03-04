from __future__ import annotations

from datetime import UTC, datetime, timedelta

from recoleta.publish import write_markdown_trend_note


def test_publish_trend_note_skips_missing_representative_fields(
    tmp_path,
) -> None:
    period_start = datetime(2026, 3, 2, tzinfo=UTC)
    period_end = period_start + timedelta(days=1)

    note_path = write_markdown_trend_note(
        output_dir=tmp_path,
        trend_doc_id=1,
        title="Daily Trend",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        run_id="run-test",
        overview_md="- overview",
        topics=["agents"],
        clusters=[
            {
                "name": "cluster-a",
                "description": "desc",
                "representative_chunks": [
                    {},
                    {"doc_id": None, "chunk_index": None, "score": None},
                    {"doc_id": 1, "chunk_index": 0, "score": 0.9},
                ],
            }
        ],
        highlights=["h"],
    )

    text = note_path.read_text(encoding="utf-8")
    assert "doc_id=None" not in text
    assert "chunk_index=None" not in text
