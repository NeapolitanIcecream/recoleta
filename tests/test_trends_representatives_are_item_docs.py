from __future__ import annotations

import json
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast

import pytest

from recoleta.pipeline import PipelineService
from recoleta.trends import (
    TrendCluster,
    TrendPayload,
    day_period_bounds,
    index_items_as_documents,
    persist_trend_payload,
    week_period_bounds,
)
from recoleta.types import ItemDraft
from tests.spec_support import FakeAnalyzer, FakeTelegramSender, _build_runtime


def test_trends_week_enforces_item_level_representatives(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("PUBLISH_TARGETS", "markdown")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("LLM_OUTPUT_LANGUAGE", "Chinese (Simplified)")
    monkeypatch.setenv("TOPICS", json.dumps(["agents"]))
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    anchor = date(2026, 3, 5)
    week_start, week_end = week_period_bounds(anchor)

    # Create at least one daily trend doc so weekly trends sees a non-empty corpus.
    day_start, day_end = day_period_bounds(week_start.date())
    daily_payload = TrendPayload(
        title="Daily Trend",
        granularity="day",
        period_start=day_start.isoformat(),
        period_end=day_end.isoformat(),
        overview_md="- daily",
        topics=["agents"],
        clusters=[],
        highlights=[],
    )
    daily_trend_doc_id = persist_trend_payload(
        repository=repository,
        granularity="day",
        period_start=day_start,
        period_end=day_end,
        payload=daily_payload,
    )

    # Create at least one analyzed item (paper) in the same window and index as item document.
    paper_url = "https://example.com/paper-1"
    paper_title = "Self-similar agents for trend reps"
    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="paper-1",
        canonical_url=paper_url,
        title=paper_title,
        authors=["Alice"],
        published_at=week_start + timedelta(days=1),
        raw_metadata={"source": "test"},
    )
    item, _ = repository.upsert_item(draft)
    assert item.id is not None
    item_id = int(item.id)
    analysis, _ = service.analyzer.analyze(
        title=paper_title,
        canonical_url=paper_url,
        user_topics=["agents"],
        include_debug=False,
    )
    _ = repository.save_analysis(item_id=item_id, result=analysis)
    _ = index_items_as_documents(
        repository=repository,
        run_id="run-week-reps-item",
        period_start=week_start,
        period_end=week_end,
    )

    # Patch trend generation to return a weekly payload whose reps point to a trend doc (non-item).
    from recoleta.rag import agent as rag_agent

    weekly_payload = TrendPayload(
        title="Weekly Trend",
        granularity="week",
        period_start=week_start.isoformat(),
        period_end=week_end.isoformat(),
        overview_md="- weekly",
        topics=["agents"],
        clusters=[
            TrendCluster(
                name="Self-similar agents",
                description="self-similar agents for representative selection",
                representative_doc_ids=[],
                representative_chunks=[
                    TrendCluster.RepresentativeChunk(
                        doc_id=daily_trend_doc_id, chunk_index=0, score=None
                    )
                ],
            )
        ],
        highlights=[],
    )

    def _fake_generate(**_kwargs):  # type: ignore[no-untyped-def]
        return weekly_payload, {"tool_calls_total": 0}

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    result = service.trends(
        run_id="run-week-reps-item",
        granularity="week",
        anchor_date=anchor,
        llm_model="test/fake-model",
    )

    note_dir = tmp_path / "md" / "Trends"
    note_path = next(note_dir.glob(f"week--*--trend--{result.doc_id}.md"))
    note_text = note_path.read_text(encoding="utf-8")

    rep_section_start = note_text.find("#### Representative papers")
    assert rep_section_start >= 0
    rep_section = note_text[rep_section_start:]

    assert paper_url in rep_section
    assert "Daily Trend" not in rep_section

    metrics = repository.list_metrics(run_id="run-week-reps-item")
    metric_names = [str(getattr(m, "name", "")) for m in metrics]
    assert "pipeline.trends.rep_enforcement.dropped_non_item_total" in metric_names
    assert "pipeline.trends.rep_enforcement.backfilled_total" in metric_names


def test_generate_trend_payload_rep_backfill_uses_item_doc_type_by_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from recoleta.rag import agent as rag_agent

    seen: list[str] = []

    def _fake_semantic_search_summaries_in_period(**kwargs):  # type: ignore[no-untyped-def]
        seen.append(str(kwargs.get("doc_type") or ""))
        return []

    monkeypatch.setattr(
        rag_agent,
        "semantic_search_summaries_in_period",
        _fake_semantic_search_summaries_in_period,
    )

    class _FakeAgent:  # noqa: D401
        def __init__(self, output: TrendPayload) -> None:
            self._output = output

        def run_sync(self, _prompt: str, *, deps):  # type: ignore[no-untyped-def]  # noqa: ARG002
            return SimpleNamespace(
                output=self._output,
                usage=lambda: SimpleNamespace(
                    input_tokens=None, output_tokens=None, requests=None
                ),
            )

    def _make_payload() -> TrendPayload:
        period_start = datetime(2026, 3, 2, tzinfo=UTC)
        period_end = period_start + timedelta(days=7)
        return TrendPayload(
            title="Weekly Trend",
            granularity="week",
            period_start=period_start.isoformat(),
            period_end=period_end.isoformat(),
            overview_md="- weekly",
            topics=["agents"],
            clusters=[
                TrendCluster(
                    name="self-similar agents",
                    description="representative selection",
                    representative_doc_ids=[],
                    representative_chunks=[],
                )
            ],
            highlights=[],
        )

    monkeypatch.setattr(
        rag_agent,
        "build_trend_agent",
        lambda *, llm_model, output_language=None: _FakeAgent(_make_payload()),  # noqa: ARG005
    )

    generate_any = cast(Any, rag_agent.generate_trend_payload)
    payload, _ = generate_any(
        repository=object(),  # only passed through to the patched semantic search
        vector_store=object(),  # only passed through to the patched semantic search
        run_id="run-agent-rep-doc-type",
        llm_model="test/fake-model",
        output_language=None,
        embedding_model="text-embedding-3-small",
        embedding_dimensions=None,
        embedding_batch_max_inputs=8,
        embedding_batch_max_chars=4000,
        embedding_failure_mode="continue",
        embedding_max_errors=0,
        granularity="week",
        period_start=datetime(2026, 3, 2, tzinfo=UTC),
        period_end=datetime(2026, 3, 9, tzinfo=UTC),
        corpus_doc_type="trend",
        corpus_granularity="day",
        overview_pack_md=None,
        rag_sources=None,
        ranking_n=None,
        rep_source_doc_type=None,
        include_debug=False,
    )
    assert payload.title
    assert seen and seen[-1] == "item"

    # If rep_source_doc_type is provided, it should override the default.
    seen.clear()
    _ = generate_any(
        repository=object(),
        vector_store=object(),
        run_id="run-agent-rep-doc-type-override",
        llm_model="test/fake-model",
        output_language=None,
        embedding_model="text-embedding-3-small",
        embedding_dimensions=None,
        embedding_batch_max_inputs=8,
        embedding_batch_max_chars=4000,
        embedding_failure_mode="continue",
        embedding_max_errors=0,
        granularity="week",
        period_start=datetime(2026, 3, 2, tzinfo=UTC),
        period_end=datetime(2026, 3, 9, tzinfo=UTC),
        corpus_doc_type="item",
        corpus_granularity=None,
        overview_pack_md=None,
        rag_sources=None,
        ranking_n=None,
        rep_source_doc_type="trend",
        include_debug=False,
    )
    assert seen and seen[-1] == "trend"
