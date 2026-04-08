from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

import pytest
from sqlmodel import Session, select

from recoleta.pipeline import PipelineService
from recoleta.models import Artifact
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
    monkeypatch.setenv("TRENDS_PEER_HISTORY_ENABLED", "true")
    monkeypatch.setenv("TRENDS_PEER_HISTORY_WINDOW_COUNT", "2")
    monkeypatch.setenv("TRENDS_EVOLUTION_MAX_SIGNALS", "4")

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    anchor = date(2026, 3, 5)
    week_start, week_end = week_period_bounds(anchor)
    previous_week_start, previous_week_end = week_period_bounds(date(2026, 2, 26))

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
        ),
    )
    _ = persist_trend_payload(
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
    assert isinstance(captured.get("history_pack_md"), str)
    assert str(captured.get("history_pack_md") or "").startswith("## History pack")
    assert captured.get("rag_sources") == [
        {"doc_type": "item", "granularity": None},
        {"doc_type": "trend", "granularity": "day"},
    ]
    assert captured.get("ranking_n") == 10
    assert captured.get("rep_source_doc_type") == "item"
    assert captured.get("evolution_max_signals") == 4

    metric_values = {
        str(getattr(metric, "name", "")): float(getattr(metric, "value", 0.0))
        for metric in repository.list_metrics(run_id="run-pipeline-inject")
    }
    assert metric_values["pipeline.trends.history.windows_requested"] == 2.0
    assert metric_values["pipeline.trends.history.windows_available"] == 1.0


def test_trends_debug_artifact_captures_context_packs_when_history_enabled(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    artifacts_dir = tmp_path / "artifacts"
    monkeypatch.setenv("PUBLISH_TARGETS", "markdown")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("ARTIFACTS_DIR", str(artifacts_dir))
    monkeypatch.setenv("WRITE_DEBUG_ARTIFACTS", "true")
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "test/fake-model")
    monkeypatch.setenv("LLM_OUTPUT_LANGUAGE", "Chinese (Simplified)")
    monkeypatch.setenv("TOPICS", json.dumps(["agents"]))
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))
    monkeypatch.setenv("TRENDS_SELF_SIMILAR_ENABLED", "true")
    monkeypatch.setenv("TRENDS_PEER_HISTORY_ENABLED", "true")
    monkeypatch.setenv("TRENDS_PEER_HISTORY_WINDOW_COUNT", "1")

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    anchor = date(2026, 3, 5)
    week_start, week_end = week_period_bounds(anchor)
    previous_week_start, previous_week_end = week_period_bounds(date(2026, 2, 26))

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
        ),
    )
    _ = persist_trend_payload(
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
        ),
    )

    import recoleta.trends as trends_mod

    def _fake_generate_trend_via_tools(**_kwargs):  # type: ignore[no-untyped-def]
        return (
            TrendPayload(
                title="Weekly Trend",
                granularity="week",
                period_start=week_start.isoformat(),
                period_end=week_end.isoformat(),
                overview_md="- weekly",
                topics=["agents"],
                clusters=[],
            ),
            {
                "usage": {"requests": 1, "input_tokens": 10, "output_tokens": 20},
                "tool_calls_total": 0,
                "tool_call_breakdown": {},
                "prompt_chars": 100,
                "overview_pack_chars": 10,
                "history_pack_chars": 20,
            },
        )

    monkeypatch.setattr(
        trends_mod, "generate_trend_via_tools", _fake_generate_trend_via_tools
    )

    _ = service.trends(
        run_id="run-pipeline-history-debug",
        granularity="week",
        anchor_date=anchor,
        llm_model="test/fake-model",
    )

    with Session(repository.engine) as session:
        artifact = session.exec(
            select(Artifact).where(Artifact.run_id == "run-pipeline-history-debug")
        ).first()
    assert artifact is not None
    payload = json.loads((artifacts_dir / artifact.path).read_text(encoding="utf-8"))
    debug = payload["debug"]
    assert debug["context_packs"]["overview_pack_md"].startswith("## Overview pack")
    assert debug["context_packs"]["history_pack_md"].startswith("## History pack")
    assert debug["history_pack_stats"]["available_windows"] == 1
    assert debug["history_pack_stats"]["available_window_ids"] == ["prev_1"]
