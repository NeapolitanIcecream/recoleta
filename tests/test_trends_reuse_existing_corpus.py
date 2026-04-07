from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any, cast

import pytest

from recoleta.passes import TREND_SYNTHESIS_PASS_KIND
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
    assert (
        metric_values[
            "pipeline.trends.source_materialization.checked_total.item"
        ]
        == 1.0
    )
    assert (
        metric_values[
            "pipeline.trends.source_materialization.already_ready_total.item"
        ]
        == 1.0
    )


def test_day_trends_reuse_existing_corpus_indexes_missing_item_documents(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Regression: day trends rebuild missing item docs without rerunning prepare/analyze."""

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
        source_item_id="reuse-missing-day-docs",
        canonical_url="https://example.com/reuse-missing-day-docs",
        title="Reuse Missing Day Docs",
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

    monkeypatch.setattr(service, "prepare", _raise_if_called)
    monkeypatch.setattr(service, "analyze", _raise_if_called)

    from recoleta.rag import agent as rag_agent

    calls = {"total": 0}

    def _fake_generate(**kwargs):  # type: ignore[no-untyped-def]
        calls["total"] += 1
        period_start = kwargs["period_start"]
        period_end = kwargs["period_end"]
        return (
            TrendPayload(
                title="Day Trend",
                granularity="day",
                period_start=period_start.isoformat(),
                period_end=period_end.isoformat(),
                overview_md="- rebuilt missing item docs",
                topics=["agents"],
                clusters=[],
                highlights=["agents"],
            ),
            {"tool_calls_total": 0, "tool_call_breakdown": {}},
        )

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    result = service.trends(
        run_id="run-reuse-missing-day-docs",
        granularity="day",
        anchor_date=anchor,
        llm_model="test/fake-model",
        reuse_existing_corpus=True,
    )

    docs = repository.list_documents(
        doc_type="item",
        period_start=day_start,
        period_end=day_end,
        order_by="event_desc",
        limit=10,
    )

    assert calls["total"] == 1
    assert result.title == "Day Trend"
    assert len(docs) == 1

    metric_values = {
        str(getattr(metric, "name", "")): float(getattr(metric, "value", 0.0))
        for metric in repository.list_metrics(run_id="run-reuse-missing-day-docs")
    }
    assert metric_values["pipeline.trends.corpus.reuse_existing"] == 1.0
    assert metric_values["pipeline.trends.prepare.skipped_total"] == 1.0
    assert metric_values["pipeline.trends.index.skipped_total"] == 0.0
    assert metric_values["pipeline.trends.corpus.empty"] == 0.0
    assert metric_values["pipeline.trends.index.docs_upserted_total"] == 1.0
    assert (
        metric_values[
            "pipeline.trends.source_materialization.checked_total.item"
        ]
        == 1.0
    )
    assert (
        metric_values[
            "pipeline.trends.source_materialization.materialized_total.item"
        ]
        == 1.0
    )


def test_day_trends_non_reuse_reindexes_existing_item_documents(
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
        source_item_id="non-reuse-refresh-day-docs",
        canonical_url="https://example.com/non-reuse-refresh-day-docs",
        title="Non Reuse Refresh Day Docs",
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
        repository=cast(Any, repository),
        run_id="seed-non-reuse-refresh-day-docs",
        period_start=day_start,
        period_end=day_end,
    )

    monkeypatch.setattr(service, "prepare", lambda **_: None)
    monkeypatch.setattr(service, "analyze", lambda **_: None)

    from recoleta.pipeline import trends_stage as trends_stage_mod
    from recoleta.rag import agent as rag_agent

    original_index = trends_stage_mod._TrendStageRunner._index_items_for_period
    index_calls = {"total": 0}

    def _recording_index(self, *, period_start, period_end):  # type: ignore[no-untyped-def]
        index_calls["total"] += 1
        return original_index(self, period_start=period_start, period_end=period_end)

    monkeypatch.setattr(
        trends_stage_mod._TrendStageRunner,
        "_index_items_for_period",
        _recording_index,
    )

    def _fake_generate(**kwargs):  # type: ignore[no-untyped-def]
        period_start = kwargs["period_start"]
        period_end = kwargs["period_end"]
        return (
            TrendPayload(
                title="Day Trend",
                granularity="day",
                period_start=period_start.isoformat(),
                period_end=period_end.isoformat(),
                overview_md="- refreshed existing item docs",
                topics=["agents"],
                clusters=[],
                highlights=["agents"],
            ),
            {"tool_calls_total": 0, "tool_call_breakdown": {}},
        )

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    result = service.trends(
        run_id="run-non-reuse-refresh-day-docs",
        granularity="day",
        anchor_date=anchor,
        llm_model="test/fake-model",
        reuse_existing_corpus=False,
    )

    assert result.doc_id > 0
    assert index_calls["total"] == 1
    metric_values = {
        str(getattr(metric, "name", "")): float(getattr(metric, "value", 0.0))
        for metric in repository.list_metrics(run_id="run-non-reuse-refresh-day-docs")
    }
    assert metric_values["pipeline.trends.corpus.reuse_existing"] == 0.0
    assert metric_values["pipeline.trends.prepare.skipped_total"] == 0.0
    assert metric_values["pipeline.trends.index.skipped_total"] == 0.0
    assert (
        metric_values[
            "pipeline.trends.source_materialization.materialized_total.item"
        ]
        == 1.0
    )


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
    assert (
        metric_values[
            "pipeline.trends.source_materialization.checked_total.item"
        ]
        == 1.0
    )
    assert (
        metric_values[
            "pipeline.trends.source_materialization.already_ready_total.item"
        ]
        == 1.0
    )
    assert (
        metric_values[
            "pipeline.trends.source_materialization.checked_total.trend_day"
        ]
        == 1.0
    )
    assert (
        metric_values[
            "pipeline.trends.source_materialization.materialized_total.trend_day"
        ]
        == 1.0
    )


def test_week_trends_reuse_existing_corpus_repairs_missing_trend_meta_from_pass_output(
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
    _ = week_end
    for offset in range(7):
        day_anchor = (week_start + timedelta(days=offset)).date()
        day_start, day_end = day_period_bounds(day_anchor)
        payload = TrendPayload(
            title=f"Seed Daily Trend {offset}",
            granularity="day",
            period_start=day_start.isoformat(),
            period_end=day_end.isoformat(),
            overview_md=f"- daily {offset}",
            topics=["agents"],
            clusters=[],
            highlights=[],
        )
        if offset == 0:
            doc = repository.upsert_document_for_trend(
                granularity="day",
                period_start=day_start,
                period_end=day_end,
                title=payload.title,
            )
            assert doc.id is not None
            repository.upsert_document_chunk(
                doc_id=int(doc.id),
                chunk_index=0,
                kind="summary",
                text_value=payload.overview_md,
                start_char=0,
                end_char=None,
                source_content_type="trend_overview",
            )
            repository.create_pass_output(
                run_id="seed-day-pass-output",
                pass_kind=TREND_SYNTHESIS_PASS_KIND,
                status="succeeded",
                granularity="day",
                period_start=day_start,
                period_end=day_end,
                payload=payload.model_dump(mode="json"),
            )
            continue
        _ = persist_trend_payload(
            repository=repository,
            granularity="day",
            period_start=day_start,
            period_end=day_end,
            payload=payload,
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
                overview_md="- repaired week corpus",
                topics=["agents"],
                clusters=[],
                highlights=["agents"],
            ),
            {"tool_calls_total": 0, "tool_call_breakdown": {}},
        )

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    result = service.trends(
        run_id="run-repair-trend-meta-week",
        granularity="week",
        anchor_date=anchor,
        llm_model="test/fake-model",
        reuse_existing_corpus=True,
    )

    assert result.doc_id > 0
    repaired_day_start, repaired_day_end = day_period_bounds(week_start.date())
    repaired_docs = repository.list_documents(
        doc_type="trend",
        granularity="day",
        period_start=repaired_day_start,
        period_end=repaired_day_end,
        order_by="event_desc",
        limit=10,
    )
    assert repaired_docs
    repaired_meta = repository.list_document_chunks_in_period(
        doc_type="trend",
        kind="meta",
        granularity="day",
        period_start=repaired_day_start,
        period_end=repaired_day_end,
        limit=10,
    )
    assert len(repaired_meta) == 1

    metric_values = {
        str(getattr(metric, "name", "")): float(getattr(metric, "value", 0.0))
        for metric in repository.list_metrics(run_id="run-repair-trend-meta-week")
    }
    assert (
        metric_values[
            "pipeline.trends.source_materialization.materialized_total.trend_day"
        ]
        == 1.0
    )


def test_week_trends_reuse_existing_corpus_fails_when_required_trend_meta_cannot_be_repaired(
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
    week_start, _week_end = week_period_bounds(anchor)
    for offset in range(7):
        day_anchor = (week_start + timedelta(days=offset)).date()
        day_start, day_end = day_period_bounds(day_anchor)
        payload = TrendPayload(
            title=f"Seed Daily Trend {offset}",
            granularity="day",
            period_start=day_start.isoformat(),
            period_end=day_end.isoformat(),
            overview_md=f"- daily {offset}",
            topics=["agents"],
            clusters=[],
            highlights=[],
        )
        if offset == 0:
            doc = repository.upsert_document_for_trend(
                granularity="day",
                period_start=day_start,
                period_end=day_end,
                title=payload.title,
            )
            assert doc.id is not None
            repository.upsert_document_chunk(
                doc_id=int(doc.id),
                chunk_index=0,
                kind="summary",
                text_value=payload.overview_md,
                start_char=0,
                end_char=None,
                source_content_type="trend_overview",
            )
            continue
        _ = persist_trend_payload(
            repository=repository,
            granularity="day",
            period_start=day_start,
            period_end=day_end,
            payload=payload,
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
                overview_md="- should not be reached",
                topics=["agents"],
                clusters=[],
                highlights=["agents"],
            ),
            {"tool_calls_total": 0, "tool_call_breakdown": {}},
        )

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    with pytest.raises(RuntimeError, match="required source materialization failed"):
        _ = service.trends(
            run_id="run-fail-missing-trend-meta-week",
            granularity="week",
            anchor_date=anchor,
            llm_model="test/fake-model",
            reuse_existing_corpus=True,
        )

    metric_values = {
        str(getattr(metric, "name", "")): float(getattr(metric, "value", 0.0))
        for metric in repository.list_metrics(run_id="run-fail-missing-trend-meta-week")
    }
    assert (
        metric_values[
            "pipeline.trends.source_materialization.failed_total.trend_day"
        ]
        == 1.0
    )
