from __future__ import annotations

from datetime import UTC, datetime

from recoleta.trend_materialize import materialize_trend_note_payload
from recoleta.trends import TrendPayload, persist_trend_payload, week_period_bounds
from tests.spec_support import _build_runtime


def test_materialize_trend_note_payload_builds_history_window_refs(
    configured_env, tmp_path
) -> None:
    _ = configured_env
    _, repository = _build_runtime()

    anchor = datetime(2026, 3, 12, tzinfo=UTC).date()
    current_week_start, current_week_end = week_period_bounds(anchor)
    previous_week_start = datetime(2026, 3, 2, tzinfo=UTC)
    previous_week_end = datetime(2026, 3, 9, tzinfo=UTC)

    doc_id = persist_trend_payload(
        repository=repository,
        granularity="week",
        period_start=previous_week_start,
        period_end=previous_week_end,
        payload=TrendPayload(
            title="Previous Weekly Trend",
            granularity="week",
            period_start=previous_week_start.isoformat(),
            period_end=previous_week_end.isoformat(),
            overview_md="- previous weekly trend",
            topics=["agents"],
            clusters=[],
            highlights=[],
        ),
    )

    materialized = materialize_trend_note_payload(
        repository=repository,
        payload=TrendPayload(
            title="Current Weekly Trend",
            granularity="week",
            period_start=current_week_start.isoformat(),
            period_end=current_week_end.isoformat(),
            overview_md="- current weekly trend",
            topics=["agents"],
            clusters=[],
            highlights=[],
            evolution={
                "summary_md": "Execution loops are becoming more explicit.",
                "signals": [
                    {
                        "theme": "Verification",
                        "change_type": "continuing",
                        "summary": "Concrete evaluation work keeps surfacing.",
                        "history_windows": ["prev_1"],
                    }
                ],
            },
        ),
        markdown_output_dir=tmp_path,
        output_language="Chinese (Simplified)",
    )

    assert materialized.history_window_refs == {
        "prev_1": {
            "window_id": "prev_1",
            "label": "2026-W10",
            "granularity": "week",
            "period_start": previous_week_start.isoformat(),
            "trend_doc_id": doc_id,
        }
    }
