from __future__ import annotations

from datetime import UTC, datetime
import json

from recoleta.trends import (
    TrendGenerationPlan,
    TrendPayload,
    build_history_pack_md,
    week_period_bounds,
)
from tests.spec_support import _build_runtime


def test_week_plan_builds_previous_same_level_history_windows() -> None:
    anchor = datetime(2026, 3, 12, tzinfo=UTC).date()
    week_start, week_end = week_period_bounds(anchor)

    plan = TrendGenerationPlan(
        target_granularity="week",
        period_start=week_start,
        period_end=week_end,
        peer_history_window_count=3,
    )

    assert [window.window_id for window in plan.peer_history_windows] == [
        "prev_1",
        "prev_2",
        "prev_3",
    ]
    assert plan.peer_history_windows[0].period_end == week_start
    assert plan.peer_history_windows[0].period_start == datetime(2026, 3, 2, tzinfo=UTC)
    assert plan.peer_history_windows[1].period_start == datetime(
        2026, 2, 23, tzinfo=UTC
    )
    assert plan.peer_history_windows[2].period_start == datetime(
        2026, 2, 16, tzinfo=UTC
    )
    assert plan.peer_history_window_count == 3


def test_history_pack_week_includes_previous_windows_with_placeholders(
    configured_env,
) -> None:
    _ = configured_env
    _, repository = _build_runtime()

    anchor = datetime(2026, 3, 12, tzinfo=UTC).date()
    week_start, week_end = week_period_bounds(anchor)
    previous_week_start = datetime(2026, 3, 2, tzinfo=UTC)
    previous_week_end = datetime(2026, 3, 9, tzinfo=UTC)

    doc = repository.upsert_document_for_trend(
        granularity="week",
        period_start=previous_week_start,
        period_end=previous_week_end,
        title="Weekly Trend",
    )
    assert doc.id is not None
    repository.upsert_document_chunk(
        doc_id=int(doc.id),
        chunk_index=1,
        kind="meta",
        text_value=json.dumps(
            TrendPayload(
                title="2026-W10 Weekly Trend",
                granularity="week",
                period_start=previous_week_start.isoformat(),
                period_end=previous_week_end.isoformat(),
                overview_md="Agent tooling keeps tightening the loop.",
                topics=["agents"],
                clusters=[],
            ).model_dump(mode="json"),
            ensure_ascii=False,
        ),
        start_char=0,
        end_char=None,
        source_content_type="trend_payload_json",
    )

    plan = TrendGenerationPlan(
        target_granularity="week",
        period_start=week_start,
        period_end=week_end,
        peer_history_window_count=2,
    )

    md, stats = build_history_pack_md(
        repository,
        plan,
        history_pack_max_chars=10_000,
    )

    assert stats["requested_windows"] == 2
    assert stats["available_windows"] == 1
    assert stats["missing_windows"] == 1
    assert stats["available_window_ids"] == ["prev_1"]
    assert stats["missing_window_ids"] == ["prev_2"]
    assert stats["current_period_token"] == "2026-W11"
    assert stats["truncated"] is False
    assert "### week prev_1" in md
    assert "- requested_window_ids=prev_1, prev_2" in md
    assert "- available_window_ids=prev_1" in md
    assert "- period_token=2026-W10" in md
    assert "- overview=Agent tooling keeps tightening the loop." in md
    assert "### week prev_2" in md
    assert md.count("- status=missing") == 1
