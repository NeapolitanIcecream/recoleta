from __future__ import annotations

from datetime import UTC, datetime
import json

from recoleta.trends import (
    TrendGenerationPlan,
    TrendEvolutionChangeType,
    TrendEvolutionSection,
    TrendPayload,
    build_history_pack_md,
    day_period_bounds,
    normalize_trend_evolution,
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
    assert plan.peer_history_windows[0].period_start == datetime(
        2026, 3, 2, tzinfo=UTC
    )
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
                highlights=[],
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


def test_trend_evolution_signal_normalizes_change_type_aliases() -> None:
    signal = TrendEvolutionSection.model_validate(
        {
            "summary_md": "Agent coordination keeps tightening.",
            "signals": [
                {
                    "theme": "Agent workflow",
                    "change_type": "strengthening",
                    "summary": "The workflow is sticking around and becoming more explicit.",
                    "history_windows": ["prev_1"],
                }
            ],
        }
    ).signals[0]

    assert signal.change_type == TrendEvolutionChangeType.CONTINUING


def test_normalize_trend_evolution_maps_window_labels_to_prev_ids() -> None:
    anchor = datetime(2026, 3, 5, tzinfo=UTC).date()
    day_start, day_end = day_period_bounds(anchor)
    plan = TrendGenerationPlan(
        target_granularity="day",
        period_start=day_start,
        period_end=day_end,
        peer_history_window_count=3,
    )

    normalized, stats = normalize_trend_evolution(
        TrendEvolutionSection.model_validate(
            {
                "summary_md": "Execution loops are becoming more explicit over time.",
                "signals": [
                    {
                        "theme": "Agent workflow",
                        "change_type": "continuing",
                        "summary": "The workflow keeps maturing.",
                        "history_windows": [
                            "2026-03-02",
                            "2026-03-04",
                            "2026-03-05",
                            "bogus",
                        ],
                    }
                ],
            }
        ),
        granularity="day",
        period_start=day_start,
        history_windows=plan.peer_history_windows,
        available_window_ids={"prev_1", "prev_2", "prev_3"},
    )

    assert normalized is not None
    assert [signal.history_windows for signal in normalized.signals] == [
        ["prev_3", "prev_1"]
    ]
    assert stats["history_windows_normalized_total"] == 2
    assert stats["history_windows_dropped_total"] == 2
    assert stats["signals_dropped_total"] == 0


def test_normalize_trend_evolution_strips_trailing_punctuation_from_history_ids() -> (
    None
):
    anchor = datetime(2026, 3, 5, tzinfo=UTC).date()
    day_start, day_end = day_period_bounds(anchor)
    plan = TrendGenerationPlan(
        target_granularity="day",
        period_start=day_start,
        period_end=day_end,
        peer_history_window_count=3,
    )

    normalized, stats = normalize_trend_evolution(
        TrendEvolutionSection.model_validate(
            {
                "summary_md": "Execution loops are becoming more explicit over time.",
                "signals": [
                    {
                        "theme": "Agent workflow",
                        "change_type": "continuing",
                        "summary": "The workflow keeps maturing.",
                        "history_windows": [
                            "prev_1.",
                            "2026-03-03.",
                            "bogus.",
                        ],
                    }
                ],
            }
        ),
        granularity="day",
        period_start=day_start,
        history_windows=plan.peer_history_windows,
        available_window_ids={"prev_1", "prev_2", "prev_3"},
    )

    assert normalized is not None
    assert [signal.history_windows for signal in normalized.signals] == [
        ["prev_1", "prev_2"]
    ]
    assert stats["history_windows_normalized_total"] == 1
    assert stats["history_windows_dropped_total"] == 1
    assert stats["signals_dropped_total"] == 0
