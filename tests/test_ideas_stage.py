from __future__ import annotations

from datetime import UTC, date, datetime
import json
from pathlib import Path

import pytest
from sqlmodel import Session, select

from recoleta.models import PassOutput
from recoleta.pipeline import PipelineService
from recoleta.passes import (
    PassStatus,
    TREND_SYNTHESIS_PASS_KIND,
    build_trend_synthesis_pass_output,
)
from recoleta.trends import TrendPayload
from recoleta.types import AnalysisResult, ItemDraft
from tests.spec_support import FakeAnalyzer, FakeTelegramSender, _build_runtime


def _metric_values(*, repository, run_id: str) -> dict[str, float]:
    return {
        str(getattr(metric, "name", "")): float(getattr(metric, "value", 0.0))
        for metric in repository.list_metrics(run_id=run_id)
    }


def _persist_trend_synthesis_pass_output(
    *,
    repository,
    run_id: str,
    scope: str,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
    payload: TrendPayload,
) -> int:
    envelope = build_trend_synthesis_pass_output(
        run_id=run_id,
        scope=scope,
        granularity=granularity,
        period_start=period_start,
        period_end=period_end,
        payload=payload,
        diagnostics={"source": "test"},
    )
    row = repository.create_pass_output(
        run_id=envelope.run_id,
        pass_kind=envelope.pass_kind,
        status=envelope.status.value,
        scope=envelope.scope,
        granularity=envelope.granularity,
        period_start=period_start,
        period_end=period_end,
        schema_version=envelope.schema_version,
        payload=envelope.payload,
        diagnostics=envelope.diagnostics,
        input_refs=[ref.model_dump(mode="json") for ref in envelope.input_refs],
    )
    assert row.id is not None
    return int(row.id)


def _seed_item_document(*, repository, published_at: datetime) -> int:
    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="ideas-evidence-paper",
        canonical_url="https://example.com/ideas-evidence-paper",
        title="Grounded Agent Runtime for Long-Horizon Evaluation",
        authors=["Alice"],
        published_at=published_at,
    )
    item, _ = repository.upsert_item(draft)
    assert item.id is not None
    repository.save_analysis(
        item_id=int(item.id),
        result=AnalysisResult(
            model="test/fake-model",
            provider="test",
            summary=(
                "## Summary\n"
                "Grounded agent runtimes can now keep long traces auditable.\n\n"
                "## Problem\n"
                "Teams cannot validate long-horizon agent work reliably.\n\n"
                "## Approach\n"
                "Runtime traces and verifier loops are logged explicitly.\n\n"
                "## Results\n"
                "This improves debuggability for multi-step evaluation tasks.\n"
            ),
            topics=["agents", "evals"],
            relevance_score=0.95,
            novelty_score=0.41,
            cost_usd=0.0,
            latency_ms=1,
        ),
    )
    persisted_item = repository.get_item(item_id=int(item.id))
    assert persisted_item is not None
    doc = repository.upsert_document_for_item(item=persisted_item)
    assert doc.id is not None
    repository.upsert_document_chunk(
        doc_id=int(doc.id),
        chunk_index=0,
        kind="summary",
        text_value=(
            "Summary: grounded agent runtimes make long-horizon evaluation auditable."
        ),
        source_content_type="analysis_summary",
    )
    return int(doc.id)


def test_ideas_stage_requires_upstream_trend_synthesis_output(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("PUBLISH_TARGETS", "markdown")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "test/fake-model")
    monkeypatch.setenv("LLM_OUTPUT_LANGUAGE", "Chinese (Simplified)")
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    with pytest.raises(RuntimeError, match="trend_synthesis"):
        service.ideas(
            run_id="run-ideas-missing-upstream",
            granularity="day",
            anchor_date=date(2026, 3, 2),
            llm_model="test/fake-model",
        )

    metric_values = _metric_values(
        repository=repository, run_id="run-ideas-missing-upstream"
    )
    assert metric_values["pipeline.trends.pass.ideas.upstream_missing_total"] == 1.0


def test_ideas_stage_consumes_canonical_trend_pass_output_and_writes_projection(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("PUBLISH_TARGETS", "markdown")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "test/fake-model")
    monkeypatch.setenv("LLM_OUTPUT_LANGUAGE", "Chinese (Simplified)")
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    period_start = datetime(2026, 3, 2, tzinfo=UTC)
    period_end = datetime(2026, 3, 3, tzinfo=UTC)
    evidence_doc_id = _seed_item_document(
        repository=repository, published_at=period_start + (period_end - period_start) / 2
    )
    canonical_payload = TrendPayload.model_validate(
        {
            "title": "Canonical Trend",
            "granularity": "day",
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat(),
            "overview_md": "canonical overview only",
            "topics": ["agents"],
            "clusters": [
                {
                    "name": "Grounded runtimes",
                    "description": "Grounding and observability are converging.",
                    "representative_chunks": [
                        {
                            "doc_id": evidence_doc_id,
                            "chunk_index": 0,
                        }
                    ],
                }
            ],
            "highlights": ["Grounded traces are now practical."],
        }
    )
    upstream_pass_output_id = _persist_trend_synthesis_pass_output(
        repository=repository,
        run_id="run-trend-upstream",
        scope="default",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=canonical_payload,
    )

    # Create a conflicting trend document payload to prove ideas reads the pass output,
    # not the projected document body/meta.
    trend_doc = repository.upsert_document_for_trend(
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        title="Projected Trend",
    )
    assert trend_doc.id is not None
    repository.upsert_document_chunk(
        doc_id=int(trend_doc.id),
        chunk_index=0,
        kind="summary",
        text_value="projected overview only",
        source_content_type="trend_overview",
    )
    repository.upsert_document_chunk(
        doc_id=int(trend_doc.id),
        chunk_index=1,
        kind="meta",
        text_value=json.dumps(
            {
                "title": "Projected Trend",
                "granularity": "day",
                "period_start": period_start.isoformat(),
                "period_end": period_end.isoformat(),
                "overview_md": "projected overview only",
                "topics": ["projected"],
                "clusters": [],
                "highlights": [],
            },
            ensure_ascii=False,
        ),
        source_content_type="trend_payload_json",
    )

    captured: dict[str, object] = {}
    from recoleta.rag import ideas_agent

    def _fake_generate(**kwargs):  # type: ignore[no-untyped-def]
        captured["trend_payload"] = kwargs["trend_payload"]
        captured["trend_snapshot_pack_md"] = kwargs["trend_snapshot_pack_md"]
        return (
            ideas_agent.TrendIdeasPayload.model_validate(
                {
                    "title": "Why now ideas",
                    "granularity": "day",
                    "period_start": period_start.isoformat(),
                    "period_end": period_end.isoformat(),
                    "summary_md": "The evidence supports one strong workflow wedge.",
                    "ideas": [
                        {
                            "title": "Auditable long-horizon eval workbench",
                            "kind": "tooling_wedge",
                            "thesis": "Build an evaluation workbench around grounded traces.",
                            "why_now": "Grounded runtime traces have become practical.",
                            "what_changed": "Teams can now capture and inspect multi-step traces.",
                            "user_or_job": "Evaluation teams need auditable long-horizon runs.",
                            "evidence_refs": [
                                {
                                    "doc_id": evidence_doc_id,
                                    "chunk_index": 0,
                                    "reason": "Shows grounded runtime traces for evaluation.",
                                }
                            ],
                            "validation_next_step": "Prototype a trace viewer for one benchmark workflow.",
                            "time_horizon": "now",
                        }
                    ],
                }
            ),
            {
                "usage": {"requests": 1, "input_tokens": 100, "output_tokens": 200},
                "prompt_chars": 999,
                "trend_snapshot_pack_chars": 321,
                "tool_calls_total": 2,
                "tool_call_breakdown": {"search_hybrid": 1, "get_doc_bundle": 1},
            },
        )

    monkeypatch.setattr(ideas_agent, "generate_trend_ideas_payload", _fake_generate)

    result = service.ideas(
        run_id="run-ideas-success",
        granularity="day",
        anchor_date=date(2026, 3, 2),
        llm_model="test/fake-model",
    )

    assert result.status == PassStatus.SUCCEEDED.value
    assert result.upstream_pass_output_id == upstream_pass_output_id
    assert result.note_path is not None
    assert result.note_path.exists()
    assert result.pass_output_id is not None
    assert captured["trend_payload"] == canonical_payload
    assert "canonical overview only" in str(captured["trend_snapshot_pack_md"] or "")
    assert "projected overview only" not in str(captured["trend_snapshot_pack_md"] or "")

    markdown = result.note_path.read_text(encoding="utf-8")
    assert "Auditable long-horizon eval workbench" in markdown
    assert "Grounded Agent Runtime for Long-Horizon Evaluation" in markdown
    assert "doc_id:" not in markdown

    with Session(repository.engine) as session:
        row = session.exec(
            select(PassOutput).where(PassOutput.id == result.pass_output_id)
        ).first()
        assert row is not None
        assert row.pass_kind == "trend_ideas"
        assert row.status == PassStatus.SUCCEEDED.value
        input_refs = json.loads(row.input_refs_json)
        assert input_refs == [
            {
                "ref_kind": "pass_output",
                "pass_kind": TREND_SYNTHESIS_PASS_KIND,
                "scope": "default",
                "granularity": "day",
                "period_start": period_start.isoformat(),
                "period_end": period_end.isoformat(),
                "pass_output_id": upstream_pass_output_id,
                "metadata": {},
            }
        ]

    metric_values = _metric_values(repository=repository, run_id="run-ideas-success")
    assert metric_values["pipeline.trends.pass.ideas.duration_ms"] >= 0.0
    assert metric_values["pipeline.trends.pass.ideas.prompt_chars"] == 999.0
    assert metric_values["pipeline.trends.pass.ideas.tool_calls_total"] == 2.0
    assert (
        metric_values["pipeline.trends.pass.ideas.tool.search_hybrid.calls_total"]
        == 1.0
    )


def test_ideas_stage_persists_suppressed_pass_output_without_projection(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("PUBLISH_TARGETS", "markdown")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "test/fake-model")
    monkeypatch.setenv("LLM_OUTPUT_LANGUAGE", "Chinese (Simplified)")
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    period_start = datetime(2026, 3, 2, tzinfo=UTC)
    period_end = datetime(2026, 3, 3, tzinfo=UTC)
    upstream_pass_output_id = _persist_trend_synthesis_pass_output(
        repository=repository,
        run_id="run-trend-upstream-suppressed",
        scope="default",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=TrendPayload.model_validate(
            {
                "title": "Canonical Trend",
                "granularity": "day",
                "period_start": period_start.isoformat(),
                "period_end": period_end.isoformat(),
                "overview_md": "Signals are still thin.",
                "topics": ["agents"],
                "clusters": [],
                "highlights": [],
            }
        ),
    )

    from recoleta.rag import ideas_agent

    def _fake_generate(**_kwargs):  # type: ignore[no-untyped-def]
        return (
            ideas_agent.TrendIdeasPayload.model_validate(
                {
                    "title": "Why now ideas",
                    "granularity": "day",
                    "period_start": period_start.isoformat(),
                    "period_end": period_end.isoformat(),
                    "summary_md": "Evidence is too thin for high-confidence ideas.",
                    "ideas": [],
                }
            ),
            {
                "usage": {"requests": 1, "input_tokens": 10, "output_tokens": 10},
                "prompt_chars": 111,
                "trend_snapshot_pack_chars": 55,
                "tool_calls_total": 0,
                "tool_call_breakdown": {},
            },
        )

    monkeypatch.setattr(ideas_agent, "generate_trend_ideas_payload", _fake_generate)

    result = service.ideas(
        run_id="run-ideas-suppressed",
        granularity="day",
        anchor_date=date(2026, 3, 2),
        llm_model="test/fake-model",
    )

    assert result.status == PassStatus.SUPPRESSED.value
    assert result.pass_output_id is not None
    assert result.upstream_pass_output_id == upstream_pass_output_id
    assert result.note_path is None
    assert not (settings.markdown_output_dir / "Ideas" / "day--2026-03-02--ideas.md").exists()

    with Session(repository.engine) as session:
        row = session.exec(
            select(PassOutput).where(PassOutput.id == result.pass_output_id)
        ).first()
        assert row is not None
        assert row.status == PassStatus.SUPPRESSED.value

    metric_values = _metric_values(repository=repository, run_id="run-ideas-suppressed")
    assert metric_values["pipeline.trends.pass.ideas.suppressed_total"] == 1.0
