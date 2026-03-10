from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

import pytest
from sqlmodel import Session, select

from recoleta.config import Settings
from recoleta.models import Analysis, Document, DocumentChunk, Metric
from recoleta.pipeline import PipelineService
from recoleta.trends import TrendPayload, day_period_bounds
from recoleta.types import AnalysisResult, AnalyzeDebug, ItemDraft, utc_now
from tests.spec_support import FakeTelegramSender, _build_runtime


class _RecordingAnalyzer:
    def __init__(self) -> None:
        self.calls: list[list[str]] = []

    def analyze(
        self,
        *,
        title: str,
        canonical_url: str,
        user_topics: list[str],
        content: str | None = None,  # noqa: ARG002
        include_debug: bool = False,
    ) -> tuple[AnalysisResult, AnalyzeDebug | None]:
        self.calls.append(list(user_topics))
        result = AnalysisResult(
            model="test/fake-model",
            provider="test",
            summary=f"Summary for {title} via {','.join(user_topics)}",
            topics=user_topics[:1] or ["general"],
            relevance_score=0.92,
            novelty_score=0.55,
            cost_usd=0.0,
            latency_ms=1,
        )
        return result, None


class _FailingOnTopicAnalyzer(_RecordingAnalyzer):
    def __init__(self, *, failing_topic: str) -> None:
        super().__init__()
        self.failing_topic = failing_topic

    def analyze(
        self,
        *,
        title: str,
        canonical_url: str,
        user_topics: list[str],
        content: str | None = None,
        include_debug: bool = False,
    ) -> tuple[AnalysisResult, AnalyzeDebug | None]:
        self.calls.append(list(user_topics))
        if self.failing_topic in user_topics:
            raise RuntimeError(f"simulated analyzer failure for {self.failing_topic}")
        return super().analyze(
            title=title,
            canonical_url=canonical_url,
            user_topics=user_topics,
            content=content,
            include_debug=include_debug,
        )


class _SelectiveRelevanceAnalyzer(_RecordingAnalyzer):
    def analyze(
        self,
        *,
        title: str,
        canonical_url: str,
        user_topics: list[str],
        content: str | None = None,  # noqa: ARG002
        include_debug: bool = False,
    ) -> tuple[AnalysisResult, AnalyzeDebug | None]:
        self.calls.append(list(user_topics))
        relevance = 0.95 if "High" in title else 0.35
        result = AnalysisResult(
            model="test/fake-model",
            provider="test",
            summary=f"Summary for {title} via {','.join(user_topics)}",
            topics=user_topics[:1] or ["general"],
            relevance_score=relevance,
            novelty_score=0.55,
            cost_usd=0.0,
            latency_ms=1,
        )
        return result, None


def _configure_topic_stream_env(
    *,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    publish_targets: list[str] | None = None,
) -> None:
    monkeypatch.delenv("TOPICS", raising=False)
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "outputs"))
    monkeypatch.setenv(
        "PUBLISH_TARGETS",
        json.dumps(publish_targets or ["markdown"]),
    )
    monkeypatch.setenv(
        "TOPIC_STREAMS",
        json.dumps(
            [
                {
                    "name": "agents_lab",
                    "topics": ["agents"],
                },
                {
                    "name": "bio_watch",
                    "topics": ["biology"],
                    "telegram_bot_token_env": "BIO_WATCH_BOT_TOKEN",
                    "telegram_chat_id_env": "BIO_WATCH_CHAT_ID",
                },
            ]
        ),
    )
    monkeypatch.setenv("BIO_WATCH_BOT_TOKEN", "bio-watch-bot")
    monkeypatch.setenv("BIO_WATCH_CHAT_ID", "@bio-watch")


def test_settings_resolves_topic_stream_runtimes_from_config(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    _configure_topic_stream_env(monkeypatch=monkeypatch, tmp_path=tmp_path)

    settings = Settings()  # pyright: ignore[reportCallIssue]
    streams = settings.topic_stream_runtimes()

    assert settings.topics == []
    assert [stream.name for stream in streams] == ["agents_lab", "bio_watch"]
    assert streams[0].markdown_output_dir == (
        tmp_path / "outputs" / "Streams" / "agents_lab"
    ).resolve()
    assert streams[1].telegram_bot_token is not None
    assert streams[1].telegram_bot_token.get_secret_value() == "bio-watch-bot"
    assert streams[1].telegram_chat_id is not None
    assert streams[1].telegram_chat_id.get_secret_value() == "@bio-watch"


def test_settings_rejects_topic_stream_names_that_collide_after_normalization(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.delenv("TOPICS", raising=False)
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "outputs"))
    monkeypatch.setenv("PUBLISH_TARGETS", json.dumps(["markdown"]))
    monkeypatch.setenv(
        "TOPIC_STREAMS",
        json.dumps(
            [
                {
                    "name": "agents-lab",
                    "topics": ["agents"],
                },
                {
                    "name": "agents_lab",
                    "topics": ["biology"],
                },
            ]
        ),
    )

    with pytest.raises(
        ValueError,
        match="TOPIC_STREAMS names collide after downstream normalization",
    ):
        _ = Settings()  # pyright: ignore[reportCallIssue]


def test_analyze_runs_each_topic_stream_with_its_own_topics(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    _configure_topic_stream_env(monkeypatch=monkeypatch, tmp_path=tmp_path)
    settings, repository = _build_runtime()
    analyzer = _RecordingAnalyzer()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=analyzer,
        telegram_sender=FakeTelegramSender(),
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="topic-stream-analyze-1",
        canonical_url="https://example.com/topic-stream-analyze-1",
        title="Topic Stream Analyze",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-topic-stream-analyze", drafts=[draft], limit=10)

    result = service.analyze(run_id="run-topic-stream-analyze", limit=10)

    assert result.processed == 2
    assert result.failed == 0
    assert sorted(analyzer.calls) == [["agents"], ["biology"]]

    with Session(repository.engine) as session:
        analyses = list(session.exec(select(Analysis).order_by(Analysis.scope)))
        assert len(analyses) == 2
        assert [analysis.scope for analysis in analyses] == [
            "agents_lab",
            "bio_watch",
        ]


def test_analyze_emits_stream_scoped_failure_metric_for_topic_streams(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    _configure_topic_stream_env(monkeypatch=monkeypatch, tmp_path=tmp_path)
    settings, repository = _build_runtime()
    analyzer = _FailingOnTopicAnalyzer(failing_topic="biology")
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=analyzer,
        telegram_sender=FakeTelegramSender(),
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="topic-stream-failure-1",
        canonical_url="https://example.com/topic-stream-failure-1",
        title="Topic Stream Failure",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-topic-stream-failure", drafts=[draft], limit=10)

    result = service.analyze(run_id="run-topic-stream-failure", limit=10)
    metrics = repository.list_metrics(run_id="run-topic-stream-failure")
    by_name: dict[str, Metric] = {metric.name: metric for metric in metrics}

    assert result.processed == 1
    assert result.failed == 1
    assert by_name["pipeline.analyze.stream.agents_lab.processed_total"].value == 1
    assert by_name["pipeline.analyze.stream.bio_watch.failed_total"].value == 1
    assert by_name["pipeline.analyze.streams_total"].value == 2


def test_publish_allows_topic_stream_to_explicitly_clear_inherited_tag_filters(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.delenv("TOPICS", raising=False)
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "outputs"))
    monkeypatch.setenv("PUBLISH_TARGETS", json.dumps(["markdown"]))
    monkeypatch.setenv("ALLOW_TAGS", json.dumps(["never-match"]))
    monkeypatch.setenv("DENY_TAGS", json.dumps(["agents"]))
    monkeypatch.setenv(
        "TOPIC_STREAMS",
        json.dumps(
            [
                {
                    "name": "agents_lab",
                    "topics": ["agents"],
                    "allow_tags": [],
                    "deny_tags": [],
                }
            ]
        ),
    )

    settings, repository = _build_runtime()
    streams = settings.topic_stream_runtimes()
    assert len(streams) == 1
    assert streams[0].allow_tags == []
    assert streams[0].deny_tags == []

    analyzer = _RecordingAnalyzer()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=analyzer,
        telegram_sender=FakeTelegramSender(),
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="topic-stream-empty-filters-1",
        canonical_url="https://example.com/topic-stream-empty-filters-1",
        title="Topic Stream Empty Filters",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-topic-stream-empty-filters", drafts=[draft], limit=10)
    service.analyze(run_id="run-topic-stream-empty-filters", limit=10)

    result = service.publish(run_id="run-topic-stream-empty-filters", limit=10)

    assert result.sent == 1
    assert result.skipped == 0
    assert (
        tmp_path / "outputs" / "Streams" / "agents_lab" / "latest.md"
    ).exists()


def test_publish_writes_markdown_outputs_into_separate_topic_stream_directories(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    _configure_topic_stream_env(monkeypatch=monkeypatch, tmp_path=tmp_path)
    settings, repository = _build_runtime()
    analyzer = _RecordingAnalyzer()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=analyzer,
        telegram_sender=FakeTelegramSender(),
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="topic-stream-publish-1",
        canonical_url="https://example.com/topic-stream-publish-1",
        title="Topic Stream Publish",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-topic-stream-publish", drafts=[draft], limit=10)
    service.analyze(run_id="run-topic-stream-publish", limit=10)

    result = service.publish(run_id="run-topic-stream-publish", limit=10)

    assert result.sent == 2
    assert result.failed == 0
    assert (
        tmp_path / "outputs" / "Streams" / "agents_lab" / "latest.md"
    ).exists()
    assert (
        tmp_path / "outputs" / "Streams" / "bio_watch" / "latest.md"
    ).exists()
    assert (tmp_path / "outputs" / "latest.md").exists()


def test_trends_generate_separate_stream_local_documents_for_topic_streams(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    _configure_topic_stream_env(monkeypatch=monkeypatch, tmp_path=tmp_path)
    settings, repository = _build_runtime()
    analyzer = _RecordingAnalyzer()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=analyzer,
        telegram_sender=FakeTelegramSender(),
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="topic-stream-trend-1",
        canonical_url="https://example.com/topic-stream-trend-1",
        title="Topic Stream Trend",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-topic-stream-trend", drafts=[draft], limit=10)
    service.analyze(run_id="run-topic-stream-trend", limit=10)

    from recoleta.rag import agent as rag_agent

    def _fake_generate(**kwargs):  # type: ignore[no-untyped-def]
        period_start = kwargs["period_start"]
        period_end = kwargs["period_end"]
        scope = kwargs["scope"]
        docs = kwargs["repository"].list_documents(
            doc_type="item",
            period_start=period_start,
            period_end=period_end,
            scope=scope,
            limit=10,
        )
        assert len(docs) == 1
        doc = docs[0]
        chunk = kwargs["repository"].read_document_chunk(
            doc_id=int(getattr(doc, "id")),
            chunk_index=0,
        )
        assert chunk is not None
        summary = str(getattr(chunk, "text", "") or "")
        payload = TrendPayload(
            title=f"Trend for {getattr(doc, 'scope', 'unknown')}",
            granularity="day",
            period_start=period_start.isoformat(),
            period_end=period_end.isoformat(),
            overview_md=f"- {summary}",
            topics=["stream-local"],
            clusters=[],
            highlights=[summary],
        )
        return payload, {"tool_calls_total": 0}

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    anchor = utc_now().date()
    result = service.trends(
        run_id="run-topic-stream-trend",
        granularity="day",
        anchor_date=anchor,
        llm_model="test/fake-model",
    )

    assert len(result.stream_results) == 2
    assert {entry.stream for entry in result.stream_results} == {
        "agents_lab",
        "bio_watch",
    }

    period_start, period_end = day_period_bounds(anchor)
    with Session(repository.engine) as session:
        item_docs = list(
            session.exec(
                select(Document).where(
                    Document.doc_type == "item",
                    cast(Any, Document.scope).in_(["agents_lab", "bio_watch"]),
                )
            )
        )
        trend_docs = list(
            session.exec(
                select(Document).where(
                    Document.doc_type == "trend",
                    cast(Any, Document.scope).in_(["agents_lab", "bio_watch"]),
                    cast(Any, Document.period_start) == period_start,
                    cast(Any, Document.period_end) == period_end,
                )
            )
        )
        assert len(item_docs) == 2
        assert len(trend_docs) == 2

        summaries = list(
            session.exec(
                select(DocumentChunk)
                .join(Document, cast(Any, Document.id) == cast(Any, DocumentChunk.doc_id))
                .where(
                    Document.doc_type == "item",
                    cast(Any, DocumentChunk.chunk_index) == 0,
                    cast(Any, Document.scope).in_(["agents_lab", "bio_watch"]),
                )
            )
        )
        summary_texts = {chunk.text for chunk in summaries}
        assert "Summary for Topic Stream Trend via agents" in summary_texts
        assert "Summary for Topic Stream Trend via biology" in summary_texts

    assert list((tmp_path / "outputs" / "Streams" / "agents_lab" / "Trends").glob("*.md"))
    assert list((tmp_path / "outputs" / "Streams" / "bio_watch" / "Trends").glob("*.md"))


def test_trends_only_index_high_relevance_items_for_topic_streams(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Regression: low-relevance analyzed items must not enter a topic stream trend corpus."""

    _configure_topic_stream_env(monkeypatch=monkeypatch, tmp_path=tmp_path)
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))
    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=_SelectiveRelevanceAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    for idx, title in enumerate(
        ["High Signal Topic Stream Trend", "Low Signal Topic Stream Trend"],
        start=1,
    ):
        draft = ItemDraft.from_values(
            source="rss",
            source_item_id=f"topic-stream-trend-quality-{idx}",
            canonical_url=f"https://example.com/topic-stream-trend-quality-{idx}",
            title=title,
            authors=["Alice"],
            raw_metadata={"source": "test"},
        )
        service.prepare(
            run_id=f"run-topic-stream-trend-quality-prepare-{idx}",
            drafts=[draft],
            limit=10,
        )

    service.analyze(run_id="run-topic-stream-trend-quality-analyze", limit=10)

    from recoleta.rag import agent as rag_agent

    def _fake_generate(**kwargs):  # type: ignore[no-untyped-def]
        period_start = kwargs["period_start"]
        period_end = kwargs["period_end"]
        scope = kwargs["scope"]
        docs = kwargs["repository"].list_documents(
            doc_type="item",
            period_start=period_start,
            period_end=period_end,
            scope=scope,
            limit=10,
        )
        assert [str(getattr(doc, "title") or "") for doc in docs] == [
            "High Signal Topic Stream Trend"
        ]
        return (
            TrendPayload(
                title=f"Trend for {scope}",
                granularity="day",
                period_start=period_start.isoformat(),
                period_end=period_end.isoformat(),
                overview_md="- ok",
                topics=["stream-local"],
                clusters=[],
                highlights=[],
            ),
            {"tool_calls_total": 0},
        )

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    result = service.trends(
        run_id="run-topic-stream-trend-quality",
        granularity="day",
        anchor_date=utc_now().date(),
        llm_model="test/fake-model",
    )

    assert len(result.stream_results) == 2


def test_trends_emit_stream_scoped_metrics_for_topic_streams(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Regression: trend metrics stay stream-scoped for explicit topic streams."""

    _configure_topic_stream_env(monkeypatch=monkeypatch, tmp_path=tmp_path)
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))
    settings, repository = _build_runtime()
    analyzer = _RecordingAnalyzer()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=analyzer,
        telegram_sender=FakeTelegramSender(),
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="topic-stream-trend-metrics-1",
        canonical_url="https://example.com/topic-stream-trend-metrics-1",
        title="Topic Stream Trend Metrics",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-topic-stream-trend-metrics", drafts=[draft], limit=10)
    service.analyze(run_id="run-topic-stream-trend-metrics", limit=10)

    from recoleta.rag import agent as rag_agent
    metric_namespaces: list[str] = []

    def _fake_generate(**kwargs):  # type: ignore[no-untyped-def]
        metric_namespaces.append(str(kwargs["metric_namespace"]))
        period_start = kwargs["period_start"]
        period_end = kwargs["period_end"]
        return (
            TrendPayload(
                title="Scoped Stream Trend",
                granularity="day",
                period_start=period_start.isoformat(),
                period_end=period_end.isoformat(),
                overview_md="- scoped",
                topics=["stream-local"],
                clusters=[],
                highlights=["scoped"],
            ),
            {"tool_calls_total": 0},
        )

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    _ = service.trends(
        run_id="run-topic-stream-trend-metrics",
        granularity="day",
        anchor_date=utc_now().date(),
        llm_model="test/fake-model",
    )

    metrics = repository.list_metrics(run_id="run-topic-stream-trend-metrics")
    metric_names = {metric.name for metric in metrics}

    assert "pipeline.trends.stream.agents_lab.duration_ms" in metric_names
    assert "pipeline.trends.stream.bio_watch.duration_ms" in metric_names
    assert "pipeline.trends.stream.agents_lab.tool_calls_total" in metric_names
    assert "pipeline.trends.stream.bio_watch.tool_calls_total" in metric_names
    assert "pipeline.trends.streams_total" in metric_names
    assert set(metric_namespaces) == {
        "pipeline.trends.stream.agents_lab",
        "pipeline.trends.stream.bio_watch",
    }
