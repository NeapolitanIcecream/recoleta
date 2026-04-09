from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import pytest

from recoleta.pipeline import PipelineService
from recoleta.trends import TrendPayload, month_period_bounds, week_period_bounds
from tests.spec_support import FakeAnalyzer, FakeTelegramSender, _build_runtime


def test_trends_month_backfill_generates_missing_weekly_trends(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Spec: month trends can backfill missing weekly trends automatically."""

    monkeypatch.setenv("PUBLISH_TARGETS", "markdown")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("LLM_OUTPUT_LANGUAGE", "Chinese (Simplified)")
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    anchor = date(2026, 3, 18)  # In-month anchor.
    month_start, month_end = month_period_bounds(anchor)
    month_payload = TrendPayload.model_validate(
        {
            "title": "Monthly Trend",
            "granularity": "month",
            "period_start": month_start.isoformat(),
            "period_end": month_end.isoformat(),
            "overview_md": "- monthly",
            "topics": ["month"],
            "clusters": [],
            "highlights": ["monthly"],
        }
    )

    from recoleta.rag import agent as rag_agent

    calls = {"total": 0}

    def _fake_generate(**kwargs):  # type: ignore[no-untyped-def]
        _ = kwargs
        calls["total"] += 1
        return month_payload, {"tool_calls_total": 0}

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    _ = service.trends(
        run_id="run-month-backfill-1",
        granularity="month",
        anchor_date=anchor,
        llm_model="test/fake-model",
        backfill=True,
        backfill_mode="missing",
    )
    assert calls["total"] >= 1

    expected_week_starts: list[date] = []
    cursor = month_start.date()
    while True:
        week_start, _week_end = week_period_bounds(cursor)
        if week_start >= month_end:
            break
        expected_week_starts.append(week_start.date())
        cursor = (week_start + timedelta(days=7)).date()

    week_docs = repository.list_documents(
        doc_type="trend",
        granularity="week",
        period_start=month_start,
        period_end=month_end,
        order_by="event_asc",
        limit=100,
    )
    week_starts = {doc.period_start.date() for doc in week_docs if doc.period_start}
    assert week_starts == set(expected_week_starts)


def test_trends_month_source_ensure_generates_required_lower_level_trends_without_backfill(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("PUBLISH_TARGETS", "markdown")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("LLM_OUTPUT_LANGUAGE", "Chinese (Simplified)")
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    anchor = date(2026, 3, 18)
    month_start, month_end = month_period_bounds(anchor)

    from recoleta.rag import agent as rag_agent

    def _fake_generate(**kwargs):  # type: ignore[no-untyped-def]
        granularity = kwargs["granularity"]
        period_start = kwargs["period_start"]
        period_end = kwargs["period_end"]
        return (
            TrendPayload(
                title=f"{granularity.title()} Trend",
                granularity=granularity,
                period_start=period_start.isoformat(),
                period_end=period_end.isoformat(),
                overview_md=f"- {granularity}",
                topics=[granularity],
                clusters=[],
            ),
            {"tool_calls_total": 0},
        )

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    result = service.trends(
        run_id="run-month-source-ensure-1",
        granularity="month",
        anchor_date=anchor,
        llm_model="test/fake-model",
        reuse_existing_corpus=True,
    )

    assert result.granularity == "month"

    week_docs = repository.list_documents(
        doc_type="trend",
        granularity="week",
        period_start=month_start,
        period_end=month_end,
        order_by="event_asc",
        limit=100,
    )
    day_docs = repository.list_documents(
        doc_type="trend",
        granularity="day",
        period_start=month_start,
        period_end=month_end,
        order_by="event_asc",
        limit=100,
    )

    assert week_docs
    assert day_docs

    metric_values = {
        str(getattr(metric, "name", "")): float(getattr(metric, "value", 0.0))
        for metric in repository.list_metrics(run_id="run-month-source-ensure-1")
    }
    assert (
        metric_values[
            "pipeline.trends.source_materialization.materialized_total.trend_day"
        ]
        == 1.0
    )
    assert (
        metric_values[
            "pipeline.trends.source_materialization.materialized_total.trend_week"
        ]
        == 1.0
    )
