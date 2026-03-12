from __future__ import annotations

from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any, cast

import pytest

from recoleta.pipeline.service import PipelineService
from recoleta.trends import TrendPayload
from recoleta.types import ItemDraft
from tests.spec_support import FakeAnalyzer, FakeTelegramSender, _build_runtime


def test_trends_stage_records_per_tool_metrics(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("PUBLISH_TARGETS", "markdown")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=cast(Any, repository),
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    published_at = datetime(2026, 3, 2, 1, 0, tzinfo=UTC)
    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="trend-tool-metrics-1",
        canonical_url="https://example.com/trend-tool-metrics-1",
        title="Trend Tool Metrics Paper",
        authors=["Alice"],
        published_at=published_at,
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-trend-tool-metrics", drafts=[draft], limit=10)
    service.analyze(run_id="run-trend-tool-metrics", limit=10)

    from recoleta.rag import agent as rag_agent

    def _fake_generate(**kwargs):  # type: ignore[no-untyped-def]
        period_start = kwargs["period_start"]
        period_end = kwargs["period_end"]
        payload = TrendPayload(
            title="Daily Trend",
            granularity="day",
            period_start=period_start.isoformat(),
            period_end=period_end.isoformat(),
            overview_md="- grounded summary",
            topics=["agents"],
            clusters=[],
            highlights=["agents"],
        )
        debug = {
            "usage": {},
            "estimated_cost_usd": 0.0,
            "tool_calls_total": 5,
            "tool_call_breakdown": {
                "search_hybrid": 2,
                "read_chunk": 2,
                "get_doc": 1,
            },
        }
        return payload, debug

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    _ = service.trends(
        run_id="run-trend-tool-metrics",
        granularity="day",
        anchor_date=date(2026, 3, 2),
        llm_model="test/fake-model",
    )

    metric_values = {
        str(getattr(metric, "name", "")): float(getattr(metric, "value", 0.0))
        for metric in repository.list_metrics(run_id="run-trend-tool-metrics")
    }

    assert metric_values["pipeline.trends.tool_calls_total"] == 5.0
    assert metric_values["pipeline.trends.tool.search_hybrid.calls_total"] == 2.0
    assert metric_values["pipeline.trends.tool.read_chunk.calls_total"] == 2.0
    assert metric_values["pipeline.trends.tool.get_doc.calls_total"] == 1.0
