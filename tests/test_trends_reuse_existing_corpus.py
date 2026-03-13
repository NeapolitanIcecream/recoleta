from __future__ import annotations

from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any, cast

import pytest

from recoleta.pipeline.service import PipelineService
from recoleta.trends import (
    TrendPayload,
    day_period_bounds,
    index_items_as_documents,
    persist_trend_payload,
    week_period_bounds,
)
from recoleta.types import ItemDraft
from tests.spec_support import FakeAnalyzer, FakeTelegramSender, _build_runtime


def _raise_if_called(*args, **kwargs):  # type: ignore[no-untyped-def]
    raise AssertionError("prepare/analyze should not run when reusing existing corpus")


def test_day_trends_reuse_existing_corpus_skips_prepare_and_analyze(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("PUBLISH_TARGETS", "markdown")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "test/fake-model")
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=cast(Any, repository),
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    anchor = date(2026, 3, 5)
    day_start, day_end = day_period_bounds(anchor)
    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="reuse-existing-day",
        canonical_url="https://example.com/reuse-existing-day",
        title="Reuse Existing Day Corpus",
        authors=["Alice"],
        published_at=datetime(2026, 3, 5, 1, 0, tzinfo=UTC),
        raw_metadata={"source": "test"},
    )
    item, _ = repository.upsert_item(draft)
    assert item.id is not None
    analysis, _ = service.analyzer.analyze(
        title=draft.title,
        canonical_url=draft.canonical_url,
        user_topics=["agents"],
        include_debug=False,
    )
    _ = repository.save_analysis(item_id=int(item.id), result=analysis)
    _ = index_items_as_documents(
        repository=repository,
        run_id="seed-existing-day",
        period_start=day_start,
        period_end=day_end,
    )

    monkeypatch.setattr(service, "prepare", _raise_if_called)
    monkeypatch.setattr(service, "analyze", _raise_if_called)

    from recoleta.rag import agent as rag_agent

    def _fake_generate(**kwargs):  # type: ignore[no-untyped-def]
        period_start = kwargs["period_start"]
        period_end = kwargs["period_end"]
        return (
            TrendPayload(
                title="Day Trend",
                granularity="day",
                period_start=period_start.isoformat(),
                period_end=period_end.isoformat(),
                overview_md="- reused day corpus",
                topics=["agents"],
                clusters=[],
                highlights=["agents"],
            ),
            {"tool_calls_total": 0, "tool_call_breakdown": {}},
        )

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    result = service.trends(
        run_id="run-reuse-existing-day",
        granularity="day",
        anchor_date=anchor,
        llm_model="test/fake-model",
        reuse_existing_corpus=True,
    )

    assert result.doc_id > 0
    metric_values = {
        str(getattr(metric, "name", "")): float(getattr(metric, "value", 0.0))
        for metric in repository.list_metrics(run_id="run-reuse-existing-day")
    }
    assert metric_values["pipeline.trends.corpus.reuse_existing"] == 1.0
    assert metric_values["pipeline.trends.prepare.skipped_total"] == 1.0
    assert metric_values["pipeline.trends.index.skipped_total"] == 1.0


def test_week_trends_reuse_existing_corpus_skips_prepare_and_analyze(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("PUBLISH_TARGETS", "markdown")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "test/fake-model")
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=cast(Any, repository),
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    anchor = date(2026, 3, 5)
    week_start, week_end = week_period_bounds(anchor)
    day_start, day_end = day_period_bounds(week_start.date())
    _ = persist_trend_payload(
        repository=repository,
        granularity="day",
        period_start=day_start,
        period_end=day_end,
        payload=TrendPayload(
            title="Seed Daily Trend",
            granularity="day",
            period_start=day_start.isoformat(),
            period_end=day_end.isoformat(),
            overview_md="- daily",
            topics=["agents"],
            clusters=[],
            highlights=[],
        ),
    )

    monkeypatch.setattr(service, "prepare", _raise_if_called)
    monkeypatch.setattr(service, "analyze", _raise_if_called)

    from recoleta.rag import agent as rag_agent

    def _fake_generate(**kwargs):  # type: ignore[no-untyped-def]
        period_start = kwargs["period_start"]
        period_end = kwargs["period_end"]
        return (
            TrendPayload(
                title="Week Trend",
                granularity="week",
                period_start=period_start.isoformat(),
                period_end=period_end.isoformat(),
                overview_md="- reused week corpus",
                topics=["agents"],
                clusters=[],
                highlights=["agents"],
            ),
            {"tool_calls_total": 0, "tool_call_breakdown": {}},
        )

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    result = service.trends(
        run_id="run-reuse-existing-week",
        granularity="week",
        anchor_date=anchor,
        llm_model="test/fake-model",
        reuse_existing_corpus=True,
    )

    assert result.doc_id > 0
    metric_values = {
        str(getattr(metric, "name", "")): float(getattr(metric, "value", 0.0))
        for metric in repository.list_metrics(run_id="run-reuse-existing-week")
    }
    assert metric_values["pipeline.trends.corpus.reuse_existing"] == 1.0
    assert metric_values["pipeline.trends.prepare.skipped_total"] == 1.0
    assert metric_values["pipeline.trends.index.skipped_total"] == 1.0
