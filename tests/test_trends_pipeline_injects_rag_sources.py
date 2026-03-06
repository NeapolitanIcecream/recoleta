from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

import pytest

from recoleta.pipeline import PipelineService
from recoleta.trends import (
    TrendPayload,
    day_period_bounds,
    persist_trend_payload,
    week_period_bounds,
)
from tests.spec_support import FakeAnalyzer, FakeTelegramSender, _build_runtime


def test_trends_pipeline_injects_overview_pack_and_rag_sources_when_enabled(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("PUBLISH_TARGETS", "markdown")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "test/fake-model")
    monkeypatch.setenv("LLM_OUTPUT_LANGUAGE", "Chinese (Simplified)")
    monkeypatch.setenv("TOPICS", json.dumps(["agents"]))
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))
    monkeypatch.setenv("TRENDS_SELF_SIMILAR_ENABLED", "true")

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    anchor = date(2026, 3, 5)
    week_start, week_end = week_period_bounds(anchor)

    # Ensure weekly corpus isn't empty (weekly trends read daily trend docs by default).
    day_start, day_end = day_period_bounds(week_start.date())
    _ = persist_trend_payload(
        repository=repository,
        granularity="day",
        period_start=day_start,
        period_end=day_end,
        payload=TrendPayload(
            title="Daily Trend",
            granularity="day",
            period_start=day_start.isoformat(),
            period_end=day_end.isoformat(),
            overview_md="- daily",
            topics=["agents"],
            clusters=[],
            highlights=[],
        ),
    )

    captured: dict[str, Any] = {}

    import recoleta.trends as trends_mod

    def _fake_generate_trend_via_tools(**kwargs):  # type: ignore[no-untyped-def]
        captured.update(kwargs)
        return (
            TrendPayload(
                title="Weekly Trend",
                granularity="week",
                period_start=week_start.isoformat(),
                period_end=week_end.isoformat(),
                overview_md="- weekly",
                topics=["agents"],
                clusters=[],
                highlights=[],
            ),
            {"usage": {}},
        )

    monkeypatch.setattr(
        trends_mod, "generate_trend_via_tools", _fake_generate_trend_via_tools
    )

    _ = service.trends(
        run_id="run-pipeline-inject",
        granularity="week",
        anchor_date=anchor,
        llm_model="test/fake-model",
    )

    assert isinstance(captured.get("overview_pack_md"), str)
    assert str(captured.get("overview_pack_md") or "").startswith("## Overview pack")
    assert captured.get("rag_sources") == [
        {"doc_type": "item", "granularity": None},
        {"doc_type": "trend", "granularity": "day"},
    ]
    assert captured.get("ranking_n") == 10
    assert captured.get("rep_source_doc_type") == "item"
