from __future__ import annotations

from datetime import UTC, date, datetime
import json
from pathlib import Path
from typing import Any, cast

import pytest
from sqlmodel import Session, select

from recoleta.models import PassOutput
import recoleta.pipeline.ideas_stage as ideas_stage_module
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
    granularity: str,
    period_start: datetime,
    period_end: datetime,
    payload: TrendPayload,
    diagnostics: dict[str, object] | None = None,
) -> int:
    envelope = build_trend_synthesis_pass_output(
        run_id=run_id,
        granularity=granularity,
        period_start=period_start,
        period_end=period_end,
        payload=payload,
        diagnostics={"source": "test", **(diagnostics or {})},
    )
    row = repository.create_pass_output(
        run_id=envelope.run_id,
        pass_kind=envelope.pass_kind,
        status=envelope.status.value,
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


def _ideas_payload(
    *,
    period_start: datetime,
    period_end: datetime,
    evidence_doc_id: int,
    title: str = "Why now ideas",
) -> dict[str, object]:
    return {
        "title": title,
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
                "validation_next_step": (
                    "Prototype a trace viewer for one benchmark workflow."
                ),
                "time_horizon": "now",
            }
        ],
    }


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


def test_record_ideas_debug_artifact_preserves_relative_path_segments() -> None:
    artifacts: list[tuple[str, int | None, str, str]] = []

    class _FakeRepository:
        def add_artifact(
            self, *, run_id: str, item_id: int | None, kind: str, path: str
        ) -> None:
            artifacts.append((run_id, item_id, kind, path))

    class _FakeService:
        def __init__(self) -> None:
            self.settings = type(
                "Settings",
                (),
                {
                    "write_debug_artifacts": True,
                    "artifacts_dir": Path("/tmp/artifacts"),
                },
            )()
            self.repository = _FakeRepository()

        def _write_debug_artifact(  # type: ignore[no-untyped-def]
            self,
            *,
            run_id,
            item_id,
            kind,
            payload,
        ):
            return Path(run_id) / "no-item" / f"{kind}.json"

    payload = ideas_stage_module.TrendIdeasPayload.model_validate(
        {
            "title": "Ideas",
            "granularity": "day",
            "period_start": datetime(2026, 3, 2, tzinfo=UTC).isoformat(),
            "period_end": datetime(2026, 3, 3, tzinfo=UTC).isoformat(),
            "summary_md": "One precise idea.",
            "ideas": [],
        }
    )

    ideas_stage_module._record_ideas_debug_artifact(
        service=cast(Any, _FakeService()),
        run_id="run-ideas-debug",
        upstream_pass_output_id=7,
        status=PassStatus.SUPPRESSED,
        trend_snapshot_pack_md="## snapshot",
        ideas_payload=payload,
        debug={"prompt_chars": 123},
    )

    assert artifacts == [
        (
            "run-ideas-debug",
            None,
            "ideas_llm_response",
            "run-ideas-debug/no-item/ideas_llm_response.json",
        )
    ]


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
    assert metric_values["pipeline.trends.pass.ideas.cost_missing_total"] == 1.0
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


def test_ideas_stage_skips_llm_when_upstream_trend_corpus_is_empty(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Regression: ideas should not invoke the LLM when the upstream trend had no corpus."""

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

    period_start = datetime(2026, 3, 13, tzinfo=UTC)
    period_end = datetime(2026, 3, 14, tzinfo=UTC)
    upstream_pass_output_id = _persist_trend_synthesis_pass_output(
        repository=repository,
        run_id="run-trend-upstream-empty-corpus",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=TrendPayload.model_validate(
            {
                "title": "本期暂无可发布研究趋势",
                "granularity": "day",
                "period_start": period_start.isoformat(),
                "period_end": period_end.isoformat(),
                "overview_md": "- 该周期没有可用文档。",
                "topics": [],
                "clusters": [],
                "highlights": [],
            }
        ),
        diagnostics={"empty_corpus": True},
    )

    from recoleta.rag import ideas_agent

    def _must_not_call_agent(**_kwargs):  # type: ignore[no-untyped-def]
        raise AssertionError("Ideas agent must not be called for empty upstream corpus")

    monkeypatch.setattr(ideas_agent, "generate_trend_ideas_payload", _must_not_call_agent)

    result = service.ideas(
        run_id="run-ideas-empty-upstream",
        granularity="day",
        anchor_date=date(2026, 3, 13),
    )

    assert result.status == PassStatus.SUPPRESSED.value
    assert result.pass_output_id is not None
    assert result.upstream_pass_output_id == upstream_pass_output_id
    assert result.note_path is None
    assert not (settings.markdown_output_dir / "Ideas" / "day--2026-03-13--ideas.md").exists()

    with Session(repository.engine) as session:
        row = session.exec(
            select(PassOutput).where(PassOutput.id == result.pass_output_id)
        ).first()
        assert row is not None
        assert row.status == PassStatus.SUPPRESSED.value
        assert json.loads(row.payload_json)["ideas"] == []
        assert json.loads(row.diagnostics_json)["empty_corpus"] is True

    metric_values = _metric_values(repository=repository, run_id="run-ideas-empty-upstream")
    assert metric_values["pipeline.trends.pass.ideas.suppressed_total"] == 1.0
    assert metric_values["pipeline.trends.pass.ideas.llm_requests_total"] == 0.0
    assert metric_values["pipeline.trends.pass.ideas.llm_input_tokens_total"] == 0.0
    assert metric_values["pipeline.trends.pass.ideas.llm_output_tokens_total"] == 0.0


def test_ideas_stage_suppresses_ungrounded_ideas_without_evidence_refs(
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
        run_id="run-trend-upstream-ungrounded",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=TrendPayload.model_validate(
            {
                "title": "Canonical Trend",
                "granularity": "day",
                "period_start": period_start.isoformat(),
                "period_end": period_end.isoformat(),
                "overview_md": "Signals exist but the candidate idea is ungrounded.",
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
                    "summary_md": "The candidate idea lacks concrete evidence anchors.",
                    "ideas": [
                        {
                            "title": "Ungrounded workflow wedge",
                            "kind": "tooling_wedge",
                            "thesis": "Ship the idea anyway.",
                            "why_now": "Because the model suggested it.",
                            "what_changed": "Nothing verifiable was cited.",
                            "user_or_job": "Unknown user.",
                            "evidence_refs": [],
                            "validation_next_step": "Ask for evidence first.",
                            "time_horizon": "now",
                        }
                    ],
                }
            ),
            {"tool_calls_total": 0, "tool_call_breakdown": {}},
        )

    monkeypatch.setattr(ideas_agent, "generate_trend_ideas_payload", _fake_generate)

    result = service.ideas(
        run_id="run-ideas-ungrounded",
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
        assert json.loads(row.payload_json)["ideas"] == []

    docs = repository.list_documents(
        doc_type="idea",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        limit=10,
    )
    assert docs == []

    metric_values = _metric_values(repository=repository, run_id="run-ideas-ungrounded")
    assert metric_values["pipeline.trends.pass.ideas.suppressed_total"] == 1.0


def test_ideas_stage_respects_publish_targets_and_writes_obsidian_note(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("PUBLISH_TARGETS", "obsidian")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("OBSIDIAN_VAULT_PATH", str(tmp_path / "vault"))
    monkeypatch.setenv("OBSIDIAN_BASE_FOLDER", "Recoleta")
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
    _persist_trend_synthesis_pass_output(
        repository=repository,
        run_id="run-trend-upstream-obsidian",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=TrendPayload.model_validate(
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
        ),
    )

    from recoleta.rag import ideas_agent

    def _fake_generate(**_kwargs):  # type: ignore[no-untyped-def]
        return (
            ideas_agent.TrendIdeasPayload.model_validate(
                _ideas_payload(
                    period_start=period_start,
                    period_end=period_end,
                    evidence_doc_id=evidence_doc_id,
                )
            ),
            {"tool_calls_total": 0, "tool_call_breakdown": {}},
        )

    monkeypatch.setattr(ideas_agent, "generate_trend_ideas_payload", _fake_generate)

    result = service.ideas(
        run_id="run-ideas-obsidian",
        granularity="day",
        anchor_date=date(2026, 3, 2),
        llm_model="test/fake-model",
    )

    assert result.status == PassStatus.SUCCEEDED.value
    assert result.note_path is None
    assert not (settings.markdown_output_dir / "Ideas" / "day--2026-03-02--ideas.md").exists()

    assert settings.obsidian_vault_path is not None
    obsidian_note = (
        settings.obsidian_vault_path
        / settings.obsidian_base_folder
        / "Ideas"
        / "day--2026-03-02--ideas.md"
    )
    assert obsidian_note.exists()
    text = obsidian_note.read_text(encoding="utf-8")
    assert "# Why now ideas" in text
    assert "../Inbox/" in text
    assert "Grounded Agent Runtime for Long-Horizon Evaluation" in text
    assert "topics:" in text
    assert "recoleta/ideas" in text

    metric_values = _metric_values(repository=repository, run_id="run-ideas-obsidian")
    assert (
        metric_values["pipeline.trends.projection.ideas_obsidian.emitted_total"] == 1.0
    )


def test_ideas_stage_projects_searchable_idea_documents(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("PUBLISH_TARGETS", "markdown,telegram")
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
    _persist_trend_synthesis_pass_output(
        repository=repository,
        run_id="run-trend-upstream-docs",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=TrendPayload.model_validate(
            {
                "title": "Canonical Trend",
                "granularity": "day",
                "period_start": period_start.isoformat(),
                "period_end": period_end.isoformat(),
                "overview_md": "canonical overview only",
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
                _ideas_payload(
                    period_start=period_start,
                    period_end=period_end,
                    evidence_doc_id=evidence_doc_id,
                    title="Workflow wedges",
                )
            ),
            {"tool_calls_total": 0, "tool_call_breakdown": {}},
        )

    monkeypatch.setattr(ideas_agent, "generate_trend_ideas_payload", _fake_generate)

    result = service.ideas(
        run_id="run-ideas-docs",
        granularity="day",
        anchor_date=date(2026, 3, 2),
        llm_model="test/fake-model",
    )

    assert result.status == PassStatus.SUCCEEDED.value

    docs = repository.list_documents(
        doc_type="idea",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        limit=10,
    )
    assert len(docs) == 1
    doc = docs[0]
    assert doc.id is not None
    assert doc.title == "Workflow wedges"

    summary_chunk = repository.read_document_chunk(doc_id=int(doc.id), chunk_index=0)
    assert summary_chunk is not None
    assert summary_chunk.kind == "summary"
    assert "strong workflow wedge" in summary_chunk.text

    content_chunk = repository.read_document_chunk(doc_id=int(doc.id), chunk_index=1)
    assert content_chunk is not None
    assert content_chunk.kind == "content"
    assert "Auditable long-horizon eval workbench" in content_chunk.text
    assert "Validation next step" in content_chunk.text

    meta_chunk = repository.read_document_chunk(doc_id=int(doc.id), chunk_index=2)
    assert meta_chunk is not None
    assert meta_chunk.kind == "meta"
    assert meta_chunk.source_content_type == "trend_ideas_payload_json"
    meta_payload = json.loads(meta_chunk.text)
    assert meta_payload.get("_projection") == {
        "pass_output_id": result.pass_output_id,
        "pass_kind": "trend_ideas",
        "upstream_pass_output_id": result.upstream_pass_output_id,
        "upstream_pass_kind": TREND_SYNTHESIS_PASS_KIND,
    }

    assert result.note_path is not None
    note_text = result.note_path.read_text(encoding="utf-8")
    assert f"pass_output_id: {result.pass_output_id}" in note_text
    assert "pass_kind: trend_ideas" in note_text
    assert f"upstream_pass_output_id: {result.upstream_pass_output_id}" in note_text
    assert f"upstream_pass_kind: {TREND_SYNTHESIS_PASS_KIND}" in note_text

    hits = repository.search_chunks_text(
        query="trace viewer benchmark workflow",
        doc_type="idea",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        limit=5,
    )
    assert hits
    assert any(int(hit["doc_id"]) == int(doc.id) for hit in hits)

    metric_values = _metric_values(repository=repository, run_id="run-ideas-docs")
    assert (
        metric_values["pipeline.trends.projection.ideas_documents.emitted_total"] == 1.0
    )
    assert (
        metric_values["pipeline.trends.projection.ideas_telegram.skipped_total"] == 1.0
    )
    sender = service.telegram_sender
    assert isinstance(sender, FakeTelegramSender)
    assert sender.documents == []
    assert sender.messages == []
