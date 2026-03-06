from __future__ import annotations

import importlib
from datetime import UTC, datetime
from typing import Any

trends: Any = importlib.import_module("recoleta.trends")


def test_prev_level_for_granularity_mapping() -> None:
    assert trends.prev_level_for_granularity("day") == "item"
    assert trends.prev_level_for_granularity("week") == "day"
    assert trends.prev_level_for_granularity("month") == "week"


def test_week_plan_has_item_and_trend_day_rag_sources() -> None:
    plan = trends.TrendGenerationPlan(
        target_granularity="week",
        period_start=datetime(2026, 3, 3, tzinfo=UTC),
        period_end=datetime(2026, 3, 10, tzinfo=UTC),
    )
    assert plan.rep_source_doc_type == "item"
    assert plan.overview_pack_strategy == "trend_overviews"
    assert any(
        src.get("doc_type") == "item" and src.get("granularity") is None
        for src in plan.rag_sources
    )
    assert any(
        src.get("doc_type") == "trend" and src.get("granularity") == "day"
        for src in plan.rag_sources
    )


def test_day_plan_uses_item_only_rag_sources() -> None:
    plan = trends.TrendGenerationPlan(
        target_granularity="day",
        period_start=datetime(2026, 3, 1, tzinfo=UTC),
        period_end=datetime(2026, 3, 2, tzinfo=UTC),
    )
    assert plan.rep_source_doc_type == "item"
    assert plan.overview_pack_strategy == "item_top_k"
    assert any(
        src.get("doc_type") == "item" and src.get("granularity") is None
        for src in plan.rag_sources
    )
    assert not any(src.get("doc_type") == "trend" for src in plan.rag_sources)
