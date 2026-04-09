from __future__ import annotations

from datetime import UTC, date, datetime
from pathlib import Path

import pytest

from recoleta.pipeline import PipelineService
from recoleta.trends import TrendPayload, week_period_bounds
from recoleta.types import ItemDraft
from tests.spec_support import FakeAnalyzer, FakeTelegramSender, _build_runtime


def test_trends_week_backfill_generates_missing_daily_trends_and_writes_notes(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Spec: week trends can backfill missing daily trends automatically."""

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

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="week-backfill-item",
        canonical_url="https://example.com/week-backfill-item",
        title="Week Backfill Item",
        authors=["Alice"],
        published_at=datetime(2026, 3, 2, 1, 0, tzinfo=UTC),
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="seed-week-backfill", drafts=[draft], limit=10)
    _ = service.analyze(run_id="seed-week-backfill", limit=10)

    anchor = date(2026, 3, 2)  # Monday
    week_start, week_end = week_period_bounds(anchor)
    week_payload = TrendPayload.model_validate(
        {
            "title": "Weekly Trend",
            "granularity": "week",
            "period_start": week_start.isoformat(),
            "period_end": week_end.isoformat(),
            "overview_md": "- weekly",
            "topics": ["week"],
            "clusters": [],
            "highlights": ["weekly"],
        }
    )

    from recoleta.rag import agent as rag_agent

    calls = {"day": 0, "week": 0}

    def _fake_generate(**kwargs):  # type: ignore[no-untyped-def]
        granularity = str(kwargs["granularity"])
        calls[granularity] += 1
        if granularity == "week":
            return week_payload, {"tool_calls_total": 0}
        period_start = kwargs["period_start"]
        period_end = kwargs["period_end"]
        return (
            TrendPayload(
                title=f"Daily Trend {period_start.date().isoformat()}",
                granularity="day",
                period_start=period_start.isoformat(),
                period_end=period_end.isoformat(),
                overview_md="- daily",
                topics=["day"],
                clusters=[],
            ),
            {"tool_calls_total": 0},
        )

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    _ = service.trends(
        run_id="run-week-backfill-1",
        granularity="week",
        anchor_date=anchor,
        llm_model="test/fake-model",
        backfill=True,
        backfill_mode="missing",
    )
    assert calls["week"] == 1
    assert calls["day"] == 1

    # Backfilled daily trends exist in the DB and were written as notes.
    day_docs = repository.list_documents(
        doc_type="trend",
        granularity="day",
        period_start=week_start,
        period_end=week_end,
        order_by="event_asc",
        limit=50,
    )
    assert len(day_docs) == 7

    week_docs = repository.list_documents(
        doc_type="trend",
        granularity="week",
        period_start=week_start,
        period_end=week_end,
        order_by="event_asc",
        limit=10,
    )
    assert len(week_docs) == 1

    trends_dir = (tmp_path / "md" / "Trends").resolve()
    assert trends_dir.exists()

    for i in range(7):
        day = anchor.fromordinal(anchor.toordinal() + i)
        matches = list(trends_dir.glob(f"day--{day.isoformat()}--*.md"))
        assert len(matches) == 1

    iso = week_start.isocalendar()
    token = f"{iso.year}-W{iso.week:02d}"
    week_matches = list(trends_dir.glob(f"week--{token}--*.md"))
    assert len(week_matches) == 1


def test_trends_week_backfill_emits_failure_metric_when_a_day_generation_fails(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Spec: backfill continues on day failure and records an aggregate metric."""

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

    anchor = date(2026, 3, 2)
    week_start, week_end = week_period_bounds(anchor)
    week_payload = TrendPayload.model_validate(
        {
            "title": "Weekly Trend",
            "granularity": "week",
            "period_start": week_start.isoformat(),
            "period_end": week_end.isoformat(),
            "overview_md": "- weekly",
            "topics": ["week"],
            "clusters": [],
            "highlights": ["weekly"],
        }
    )
    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="backfill-day-fail-item",
        canonical_url="https://example.com/backfill-day-fail-item",
        title="Backfill Day Fail Item",
        authors=["Alice"],
        published_at=datetime(2026, 3, 2, 1, 0, tzinfo=UTC),
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="seed-week-backfill-fail", drafts=[draft], limit=10)
    _ = service.analyze(run_id="seed-week-backfill-fail", limit=10)

    from recoleta.rag import agent as rag_agent

    def _fake_generate(**kwargs):  # type: ignore[no-untyped-def]
        _ = kwargs
        return week_payload, {"tool_calls_total": 0}

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    import recoleta.pipeline.trends_stage as trends_stage_mod

    original_index = trends_stage_mod._TrendStageRunner._index_items_for_period
    state = {"raised": False}

    def _fail_once(self, *, period_start, period_end):  # type: ignore[no-untyped-def]
        if not state["raised"] and (period_end - period_start).days <= 1:
            state["raised"] = True
            raise RuntimeError("simulated day index failure")
        return original_index(self, period_start=period_start, period_end=period_end)

    monkeypatch.setattr(trends_stage_mod._TrendStageRunner, "_index_items_for_period", _fail_once)

    _ = service.trends(
        run_id="run-week-backfill-fail-1",
        granularity="week",
        anchor_date=anchor,
        llm_model="test/fake-model",
        backfill=True,
        backfill_mode="missing",
    )

    metrics = repository.list_metrics(run_id="run-week-backfill-fail-1")
    totals = {m.name: float(m.value) for m in metrics}
    assert totals.get("pipeline.trends.backfill.failed_total", 0.0) == 1.0


def test_trends_week_backfill_fails_when_required_item_source_materialization_fails(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Regression: week trends now require item corpus materialization before synthesis."""

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

    anchor = date(2026, 3, 2)
    week_start, week_end = week_period_bounds(anchor)
    week_payload = TrendPayload.model_validate(
        {
            "title": "Weekly Trend",
            "granularity": "week",
            "period_start": week_start.isoformat(),
            "period_end": week_end.isoformat(),
            "overview_md": "- weekly",
            "topics": ["week"],
            "clusters": [],
            "highlights": ["weekly"],
        }
    )
    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="week-index-fail-item",
        canonical_url="https://example.com/week-index-fail-item",
        title="Week Index Fail Item",
        authors=["Alice"],
        published_at=datetime(2026, 3, 2, 1, 0, tzinfo=UTC),
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="seed-week-index-fail", drafts=[draft], limit=10)
    _ = service.analyze(run_id="seed-week-index-fail", limit=10)

    from recoleta.rag import agent as rag_agent

    def _fake_generate(**kwargs):  # type: ignore[no-untyped-def]
        _ = kwargs
        return week_payload, {"tool_calls_total": 0}

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    import recoleta.pipeline.trends_stage as trends_stage_mod

    original_index = trends_stage_mod._TrendStageRunner._index_items_for_period
    state = {"raised": False}

    def _fail_week_index_once(self, *, period_start, period_end):  # type: ignore[no-untyped-def]
        if not state["raised"] and (period_end - period_start).days > 1:
            state["raised"] = True
            raise RuntimeError("simulated week index failure")
        return original_index(self, period_start=period_start, period_end=period_end)

    monkeypatch.setattr(
        trends_stage_mod._TrendStageRunner,
        "_index_items_for_period",
        _fail_week_index_once,
    )

    with pytest.raises(RuntimeError, match="required source materialization failed"):
        _ = service.trends(
            run_id="run-week-index-fail-1",
            granularity="week",
            anchor_date=anchor,
            llm_model="test/fake-model",
            backfill=False,
            backfill_mode="missing",
        )

    metrics = repository.list_metrics(run_id="run-week-index-fail-1")
    assert (
        sum(
            float(m.value)
            for m in metrics
            if m.name == "pipeline.trends.source_materialization.failed_total.item"
        )
        == 1.0
    )
    assert (
        sum(
            float(m.value)
            for m in metrics
            if m.name == "pipeline.trends.index.failed_total"
        )
        == 0.0
    )
