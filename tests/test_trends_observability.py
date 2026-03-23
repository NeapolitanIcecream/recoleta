from __future__ import annotations

import io
import time
from datetime import UTC, date, datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast

from loguru import logger as loguru_logger
import pytest

from recoleta.rag import agent as rag_agent
from recoleta.rag.vector_store import LanceVectorStore
from recoleta.trends import TrendPayload, semantic_search_summaries_in_period
from recoleta.pipeline.service import PipelineService
from tests.spec_support import FakeAnalyzer, FakeTelegramSender, _build_runtime


class _MetricRepository:
    def __init__(self) -> None:
        self.metrics: list[tuple[str, float, str | None]] = []

    def record_metric(
        self,
        *,
        run_id: str,
        name: str,
        value: float,
        unit: str | None = None,
    ) -> None:
        _ = run_id
        self.metrics.append((name, value, unit))


class _FakeTrendResult:
    def __init__(self, payload: TrendPayload) -> None:
        self.output = payload

    def usage(self) -> Any:
        return SimpleNamespace(input_tokens=12, output_tokens=6, requests=1)

    def all_messages(self) -> list[Any]:
        return []


def _metric_values(
    repository: _MetricRepository,
) -> dict[str, float]:
    return {name: float(value) for name, value, _ in repository.metrics}


def test_generate_trend_payload_emits_heartbeat_and_duration_metrics(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Spec: slow trend generation emits heartbeats and phase duration metrics."""

    repository = _MetricRepository()
    payload = TrendPayload(
        title="Observed Trend",
        granularity="week",
        period_start="2026-03-16T00:00:00+00:00",
        period_end="2026-03-23T00:00:00+00:00",
        overview_md="- observed",
        topics=["agents"],
        clusters=[],
        highlights=["observed"],
    )

    class _FakeAgent:
        def run_sync(self, prompt: str, deps: Any) -> _FakeTrendResult:
            _ = (prompt, deps)
            time.sleep(0.03)
            return _FakeTrendResult(payload)

    monkeypatch.setattr(rag_agent, "_TREND_AGENT_HEARTBEAT_INTERVAL_SECONDS", 0.01)
    monkeypatch.setattr(rag_agent, "build_trend_agent", lambda **_: _FakeAgent())
    monkeypatch.setattr(
        rag_agent,
        "ensure_trend_cluster_representatives",
        lambda **_: {
            "clusters_total": 0,
            "clusters_backfilled_total": 0,
            "invalid_reps_dropped_total": 0,
            "reps_backfilled_total": 0,
        },
    )

    stream = io.StringIO()
    sink_id = loguru_logger.add(stream, level="INFO")
    try:
        result_payload, _ = rag_agent.generate_trend_payload(
            repository=repository,  # type: ignore[arg-type]
            vector_store=cast(LanceVectorStore, SimpleNamespace()),
            run_id="run-heartbeat-ok",
            llm_model="test/fake-model",
            output_language="English",
            embedding_model="test/embed",
            embedding_dimensions=2,
            embedding_batch_max_inputs=8,
            embedding_batch_max_chars=8_000,
            granularity="week",
            period_start=datetime(2026, 3, 16, tzinfo=UTC),
            period_end=datetime(2026, 3, 23, tzinfo=UTC),
            corpus_doc_type="trend",
            corpus_granularity="day",
            scope="default",
            metric_namespace="pipeline.trends",
        )
    finally:
        loguru_logger.remove(sink_id)

    assert result_payload.title == "Observed Trend"
    metrics = _metric_values(repository)
    assert metrics["pipeline.trends.agent_run_sync.duration_ms"] > 0.0
    assert metrics["pipeline.trends.agent_run_sync.failed_total"] == 0.0
    assert metrics["pipeline.trends.rep_backfill.duration_ms"] >= 0.0

    output = stream.getvalue()
    assert "Trend generation started" in output
    assert "Trend generation heartbeat" in output
    assert "Trend generation done" in output


def test_generate_trend_payload_records_failure_metric_when_agent_raises(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Spec: failed trend generation records a failure metric and warning log."""

    repository = _MetricRepository()

    class _ExplodingAgent:
        def run_sync(self, prompt: str, deps: Any) -> _FakeTrendResult:
            _ = (prompt, deps)
            time.sleep(0.02)
            raise RuntimeError("simulated trend failure")

    monkeypatch.setattr(rag_agent, "_TREND_AGENT_HEARTBEAT_INTERVAL_SECONDS", 0.005)
    monkeypatch.setattr(rag_agent, "build_trend_agent", lambda **_: _ExplodingAgent())

    stream = io.StringIO()
    sink_id = loguru_logger.add(stream, level="INFO")
    try:
        with pytest.raises(RuntimeError, match="simulated trend failure"):
            _ = rag_agent.generate_trend_payload(
                repository=repository,  # type: ignore[arg-type]
                vector_store=cast(LanceVectorStore, SimpleNamespace()),
                run_id="run-heartbeat-fail",
                llm_model="test/fake-model",
                output_language="English",
                embedding_model="test/embed",
                embedding_dimensions=2,
                embedding_batch_max_inputs=8,
                embedding_batch_max_chars=8_000,
                granularity="week",
                period_start=datetime(2026, 3, 16, tzinfo=UTC),
                period_end=datetime(2026, 3, 23, tzinfo=UTC),
                corpus_doc_type="trend",
                corpus_granularity="day",
                scope="default",
                metric_namespace="pipeline.trends",
            )
    finally:
        loguru_logger.remove(sink_id)

    metrics = _metric_values(repository)
    assert metrics["pipeline.trends.agent_run_sync.duration_ms"] > 0.0
    assert metrics["pipeline.trends.agent_run_sync.failed_total"] == 1.0

    output = stream.getvalue()
    assert "Trend generation failed" in output


def test_semantic_search_emits_doc_type_duration_metrics(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Spec: semantic search records doc-type-scoped sync and search durations."""

    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))
    _, repository = _build_runtime()

    period_start = datetime(2026, 3, 16, tzinfo=UTC)
    period_end = datetime(2026, 3, 17, tzinfo=UTC)
    doc = repository.upsert_document_for_trend(
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        title="Trend Search Corpus",
    )
    assert doc.id is not None
    _ = repository.upsert_document_chunk(
        doc_id=int(doc.id),
        chunk_index=0,
        kind="summary",
        text_value="Agents coordinate software work.",
        start_char=0,
        end_char=None,
        source_content_type="analysis_summary",
    )

    def _fake_embedding(**kwargs: Any) -> dict[str, Any]:
        inputs = list(kwargs["input"])
        return {
            "data": [{"embedding": [0.1, 0.2]} for _ in inputs],
            "usage": {"prompt_tokens": len(inputs), "total_tokens": len(inputs)},
            "_hidden_params": {"response_cost": 0.0},
        }

    import recoleta.rag.embeddings as rag_embeddings

    monkeypatch.setattr(rag_embeddings, "_embedding", _fake_embedding)

    hits = semantic_search_summaries_in_period(
        repository=repository,
        lancedb_dir=tmp_path / "lancedb",
        run_id="run-search-observability",
        doc_type="trend",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        query="software agents",
        embedding_model="test/embed",
        embedding_dimensions=2,
        max_batch_inputs=64,
        max_batch_chars=40_000,
        limit=5,
        corpus_limit=10,
        metric_namespace="pipeline.trends",
    )

    assert len(hits) == 1
    metric_names = {metric.name for metric in repository.list_metrics(run_id="run-search-observability")}
    assert "pipeline.trends.semantic_index.trend.duration_ms" in metric_names
    assert "pipeline.trends.semantic_search.trend.duration_ms" in metric_names


def test_week_trends_emit_backfill_progress_logs_and_stage_duration_metrics(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Spec: week trends emit backfill progress logs and phase duration metrics."""

    monkeypatch.setenv("PUBLISH_TARGETS", "markdown")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "test/fake-model")
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))
    monkeypatch.setenv("TRENDS_SELF_SIMILAR_ENABLED", "true")

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    import recoleta.trends as trends_module

    def _fake_generate(**kwargs: Any) -> tuple[TrendPayload, dict[str, Any]]:
        period_start = kwargs["period_start"]
        period_end = kwargs["period_end"]
        return (
            TrendPayload(
                title="Weekly Trend",
                granularity="week",
                period_start=period_start.isoformat(),
                period_end=period_end.isoformat(),
                overview_md="- weekly",
                topics=["week"],
                clusters=[],
                highlights=["weekly"],
            ),
            {
                "usage": {"requests": 1, "input_tokens": 10, "output_tokens": 5},
                "estimated_cost_usd": 0.0,
                "tool_calls_total": 0,
                "tool_call_breakdown": {},
                "prompt_chars": 123,
                "overview_pack_chars": len(str(kwargs.get("overview_pack_md") or "")),
                "history_pack_chars": len(str(kwargs.get("history_pack_md") or "")),
            },
        )

    monkeypatch.setattr(trends_module, "generate_trend_via_tools", _fake_generate)

    stream = io.StringIO()
    sink_id = loguru_logger.add(stream, level="INFO")
    try:
        result = service.trends(
            run_id="run-week-observability",
            granularity="week",
            anchor_date=date(2026, 3, 16),
            llm_model="test/fake-model",
            backfill=True,
            backfill_mode="missing",
            reuse_existing_corpus=True,
        )
    finally:
        loguru_logger.remove(sink_id)

    assert result.granularity == "week"
    metric_names = {metric.name for metric in repository.list_metrics(run_id="run-week-observability")}
    assert "pipeline.trends.overview_pack.duration_ms" in metric_names
    assert "pipeline.trends.history.pack.duration_ms" in metric_names
    assert "pipeline.trends.generate.duration_ms" in metric_names

    output = stream.getvalue()
    assert "Trends backfill progress" in output
    assert "Trends synthesis starting" in output
    assert "Trends synthesis completed" in output
