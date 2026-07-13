from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
import json
from pathlib import Path

import pytest
from sqlmodel import Session, select

from recoleta.models import PassOutput
from recoleta.pipeline import PipelineService
from recoleta.passes import PassStatus, build_trend_synthesis_pass_output
from recoleta.passes.trend_ideas import TrendIdeasPayload
from recoleta.presentation import presentation_sidecar_path, validate_presentation
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
) -> int:
    envelope = build_trend_synthesis_pass_output(
        run_id=run_id,
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


def _seed_item_document(
    *, repository, published_at: datetime, source_item_id: str
) -> int:
    title = (
        "Verifier Budget Calibration for Software Agents"
        if source_item_id.endswith("-a")
        else "Human Escalation Protocols in Repository Automation"
    )
    draft = ItemDraft.from_values(
        source="rss",
        source_item_id=source_item_id,
        canonical_url=f"https://example.com/{source_item_id}",
        title=title,
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
                "## Summary\n\n"
                "Grounded agent runtimes can now keep long traces auditable.\n\n"
                "## Problem\n\n"
                "Teams cannot validate long-horizon agent work reliably.\n\n"
                "## Approach\n\n"
                "Runtime traces and verifier loops are logged explicitly.\n\n"
                "## Results\n\n"
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
        text_value="Summary: grounded agent runtimes make long-horizon evaluation auditable.",
        source_content_type="analysis_summary",
    )
    return int(doc.id)


def _seed_item_documents(*, repository, published_at: datetime) -> tuple[int, int]:
    return (
        _seed_item_document(
            repository=repository,
            published_at=published_at,
            source_item_id="ideas-evidence-paper-a",
        ),
        _seed_item_document(
            repository=repository,
            published_at=published_at,
            source_item_id="ideas-evidence-paper-b",
        ),
    )


def _read_trace(*doc_ids: int) -> dict[str, object]:
    events: list[dict[str, object]] = []
    for doc_id in doc_ids:
        call_id = f"read-{doc_id}"
        events.extend(
            [
                {
                    "kind": "tool-call",
                    "tool_name": "get_doc_bundle",
                    "tool_call_id": call_id,
                    "args": {"doc_id": doc_id},
                },
                {
                    "kind": "tool-return",
                    "tool_name": "get_doc_bundle",
                    "tool_call_id": call_id,
                    "content": {"bundle": {"doc": {"doc_id": doc_id}}},
                },
            ]
        )
    return {
        "status": "captured",
        "events": events,
        "events_total": len(events),
        "tool_calls_total": len(doc_ids),
        "events_truncated": False,
    }


def _generation_debug(*doc_ids: int) -> dict[str, object]:
    return {
        "tool_calls_total": len(doc_ids),
        "tool_call_breakdown": {"get_doc_bundle": len(doc_ids)},
        "raw_tool_trace": _read_trace(*doc_ids),
    }


def _trend_payload(
    *, period_start: datetime, period_end: datetime, evidence_doc_id: int
) -> TrendPayload:
    return TrendPayload.model_validate(
        {
            "title": "Canonical Trend",
            "granularity": "day",
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat(),
            "overview_md": "Grounded runtimes and release discipline are converging.",
            "topics": ["agents"],
            "clusters": [
                {
                    "title": "Grounded runtimes",
                    "content_md": "Grounding and observability are converging.",
                    "evidence_refs": [
                        {
                            "doc_id": evidence_doc_id,
                            "chunk_index": 0,
                            "reason": "Shows grounded runtime traces for evaluation.",
                        }
                    ],
                }
            ],
        }
    )


def _ideas_payload(
    *,
    period_start: datetime,
    period_end: datetime,
    evidence_doc_ids: tuple[int, int],
    with_evidence: bool = True,
) -> TrendIdeasPayload:
    return TrendIdeasPayload.model_validate(
        {
            "title": "Unnormalized title that should be replaced",
            "granularity": "day",
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat(),
            "summary_md": "The evidence supports one strong workflow wedge.",
            "ideas": [
                {
                    "title": "Auditable long-horizon eval workbench",
                    "content_md": (
                        "Build an evaluation workbench around grounded runtime traces."
                    ),
                    "evidence_refs": (
                        [
                            {
                                "doc_id": doc_id,
                                "chunk_index": 0,
                                "reason": "Supports the cross-source runtime hypothesis.",
                            }
                            for doc_id in evidence_doc_ids
                        ]
                        if with_evidence
                        else []
                    ),
                }
            ],
        }
    )


def test_ideas_stage_requires_upstream_trend_synthesis_output(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("PUBLISH_TARGETS", "markdown")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "test/fake-model")
    monkeypatch.setenv("IDEAS_LLM_MODEL", "test/ideas-stage-model")
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
    monkeypatch.setenv("IDEAS_LLM_MODEL", "test/ideas-stage-model")
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
    evidence_doc_ids = _seed_item_documents(
        repository=repository,
        published_at=period_start + (period_end - period_start) / 2,
    )
    evidence_doc_id = evidence_doc_ids[0]
    prior_doc = repository.upsert_document_for_idea(
        granularity="day",
        period_start=period_start - timedelta(days=1),
        period_end=period_start,
        title="Prior agent controls",
    )
    assert prior_doc.id is not None
    repository.upsert_document_chunk(
        doc_id=int(prior_doc.id),
        chunk_index=1,
        kind="content",
        text_value=(
            "Title: Earlier release gate\n"
            "Content: Gate agent prompts before deployment."
        ),
        source_content_type="trend_idea",
    )
    upstream_pass_output_id = _persist_trend_synthesis_pass_output(
        repository=repository,
        run_id="run-trend-upstream",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=_trend_payload(
            period_start=period_start,
            period_end=period_end,
            evidence_doc_id=evidence_doc_id,
        ),
    )

    from recoleta.rag import ideas_agent

    def _fake_generate_ideas_payload(**kwargs):  # type: ignore[no-untyped-def]
        assert kwargs["llm_model"] == "test/ideas-stage-model"
        assert "Earlier release gate" in kwargs["prior_ideas_pack_md"]
        return (
            _ideas_payload(
                period_start=period_start,
                period_end=period_end,
                evidence_doc_ids=evidence_doc_ids,
            ),
            _generation_debug(*evidence_doc_ids),
        )

    def _fake_generate_bundle_title(**kwargs):  # type: ignore[no-untyped-def]
        assert kwargs["llm_model"] == "test/ideas-stage-model"
        return (
            "Verification-first agent rollout",
            {
                "usage": {"requests": 1, "input_tokens": 8, "output_tokens": 4},
                "estimated_cost_usd": 0.0,
                "prompt_chars": 64,
            },
        )

    monkeypatch.setattr(
        ideas_agent,
        "generate_trend_ideas_payload",
        _fake_generate_ideas_payload,
    )
    monkeypatch.setattr(
        ideas_agent,
        "generate_trend_ideas_bundle_title",
        _fake_generate_bundle_title,
    )

    result = service.ideas(
        run_id="run-ideas-stage",
        granularity="day",
        anchor_date=date(2026, 3, 2),
    )

    assert result.status == PassStatus.SUCCEEDED.value
    assert result.upstream_pass_output_id == upstream_pass_output_id
    assert result.note_path is not None
    assert result.note_path.exists()
    assert result.pass_output_id is not None

    markdown = result.note_path.read_text(encoding="utf-8")
    sidecar = json.loads(
        presentation_sidecar_path(note_path=result.note_path).read_text(
            encoding="utf-8"
        )
    )
    assert "# Verification-first agent rollout" in markdown
    assert "## Summary" in markdown
    assert "## Auditable long-horizon eval workbench" in markdown
    assert "Best bet" not in markdown
    assert validate_presentation(sidecar) == []

    with Session(repository.engine) as session:
        row = session.exec(
            select(PassOutput).where(PassOutput.id == result.pass_output_id)
        ).one()
        assert row.status == PassStatus.SUCCEEDED.value
        diagnostics = json.loads(row.diagnostics_json or "{}")
        freshness = diagnostics["workflow_freshness"]
        assert freshness["kind"] == "trend_ideas"
        assert freshness["components"]["upstream_pass_output_id"] == upstream_pass_output_id
        assert freshness["components"]["llm_model"] == "test/ideas-stage-model"
        assert freshness["key"]
        assert "raw_tool_trace" not in diagnostics
        assert diagnostics["evidence_quality_gate"] == {
            "policy": "two_distinct_read_item_documents",
            "trace_status": "captured",
            "trace_events_truncated": False,
            "read_doc_ids": sorted(evidence_doc_ids),
            "read_doc_ids_total": 2,
        }
        assert diagnostics["normalization"]["retained_total"] == 1
        assert diagnostics["prior_ideas_pack_stats"]["retained_entries_total"] == 1


def test_ideas_stage_generates_bundle_title_from_normalized_retained_ideas(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("PUBLISH_TARGETS", "markdown")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "test/fake-model")
    monkeypatch.setenv("LLM_OUTPUT_LANGUAGE", "English")
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
    evidence_doc_ids = _seed_item_documents(
        repository=repository,
        published_at=period_start + (period_end - period_start) / 2,
    )
    evidence_doc_id = evidence_doc_ids[0]
    _persist_trend_synthesis_pass_output(
        repository=repository,
        run_id="run-trend-upstream-normalize",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=_trend_payload(
            period_start=period_start,
            period_end=period_end,
            evidence_doc_id=evidence_doc_id,
        ),
    )

    from recoleta.rag import ideas_agent

    monkeypatch.setattr(
        ideas_agent,
        "generate_trend_ideas_payload",
        lambda **_kwargs: (
            TrendIdeasPayload.model_validate(
                {
                    "title": "Should be replaced",
                    "granularity": "day",
                    "period_start": period_start.isoformat(),
                    "period_end": period_end.isoformat(),
                    "summary_md": "Release controls now travel with runtime checks.",
                    "ideas": [
                        {
                            "title": "Prompt release gate",
                            "content_md": "Add a release gate before prompt rollout.",
                            "evidence_refs": [
                                {
                                    "doc_id": evidence_doc_id,
                                    "chunk_index": 0,
                                    "reason": "Shows grounded runtime traces for evaluation.",
                                },
                                {
                                    "doc_id": evidence_doc_ids[1],
                                    "chunk_index": 0,
                                    "reason": "Supplies an independent source.",
                                },
                            ],
                        },
                        {
                            "title": "Prompt release gate",
                            "content_md": "Duplicate title should be dropped before title generation.",
                            "evidence_refs": [
                                {
                                    "doc_id": evidence_doc_id,
                                    "chunk_index": 1,
                                    "reason": "Duplicate idea should be removed.",
                                }
                            ],
                        },
                        {
                            "title": "Ungrounded idea",
                            "content_md": "This should be dropped because it has no evidence.",
                            "evidence_refs": [],
                        },
                    ],
                }
            ),
            _generation_debug(*evidence_doc_ids),
        ),
    )
    captured: dict[str, object] = {}

    def _fake_bundle_title(**kwargs: object) -> tuple[str, dict[str, object]]:
        captured["summary_md"] = kwargs["summary_md"]
        captured["ideas"] = kwargs["ideas"]
        return (
            "Verification-first agent rollout",
            {
                "usage": {"requests": 1, "input_tokens": 12, "output_tokens": 3},
                "estimated_cost_usd": 0.0,
                "prompt_chars": 72,
            },
        )

    monkeypatch.setattr(
        ideas_agent,
        "generate_trend_ideas_bundle_title",
        _fake_bundle_title,
    )

    result = service.ideas(
        run_id="run-ideas-normalize-title",
        granularity="day",
        anchor_date=date(2026, 3, 2),
        llm_model="test/fake-model",
    )

    assert result.title == "Verification-first agent rollout"
    assert captured["summary_md"] == "Release controls now travel with runtime checks."
    assert captured["ideas"] == [
        {
            "title": "Prompt release gate",
            "content_md": "Add a release gate before prompt rollout.",
        }
    ]


def test_ideas_stage_reuses_valid_primary_title_without_second_model_call(
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
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )
    period_start = datetime(2026, 3, 2, tzinfo=UTC)
    period_end = datetime(2026, 3, 3, tzinfo=UTC)
    evidence_doc_ids = _seed_item_documents(
        repository=repository,
        published_at=period_start + (period_end - period_start) / 2,
    )
    evidence_doc_id = evidence_doc_ids[0]
    _persist_trend_synthesis_pass_output(
        repository=repository,
        run_id="run-trend-upstream-valid-title",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=_trend_payload(
            period_start=period_start,
            period_end=period_end,
            evidence_doc_id=evidence_doc_id,
        ),
    )
    from recoleta.rag import ideas_agent

    payload = _ideas_payload(
        period_start=period_start,
        period_end=period_end,
        evidence_doc_ids=evidence_doc_ids,
    ).model_copy(update={"title": "Verification-first agent rollout"})
    monkeypatch.setattr(
        ideas_agent,
        "generate_trend_ideas_payload",
        lambda **_kwargs: (
            payload,
            {
                "usage": {"requests": 3, "input_tokens": 100, "output_tokens": 20},
                "estimated_cost_usd": 0.01,
                "prompt_chars": 500,
                "tool_calls_total": 0,
                "tool_call_breakdown": {"get_doc_bundle": 2},
                "raw_tool_trace": _read_trace(*evidence_doc_ids),
            },
        ),
    )
    monkeypatch.setattr(
        ideas_agent,
        "generate_trend_ideas_bundle_title",
        lambda **_kwargs: pytest.fail("valid primary title must not be rewritten"),
    )

    result = service.ideas(
        run_id="run-ideas-valid-primary-title",
        granularity="day",
        anchor_date=date(2026, 3, 2),
    )

    assert result.title == "Verification-first agent rollout"
    assert result.pass_output_id is not None
    with Session(repository.engine) as session:
        row = session.exec(
            select(PassOutput).where(PassOutput.id == result.pass_output_id)
        ).one()
        diagnostics = json.loads(row.diagnostics_json or "{}")
    assert diagnostics["usage"]["requests"] == 3
    assert diagnostics["bundle_title"]["quality_gate"] == "reused_primary"


def test_ideas_stage_falls_back_to_primary_title_when_bundle_title_generation_fails(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("PUBLISH_TARGETS", "markdown")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "test/fake-model")
    monkeypatch.setenv("LLM_OUTPUT_LANGUAGE", "English")
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
    evidence_doc_ids = _seed_item_documents(
        repository=repository,
        published_at=period_start + (period_end - period_start) / 2,
    )
    evidence_doc_id = evidence_doc_ids[0]
    _persist_trend_synthesis_pass_output(
        repository=repository,
        run_id="run-trend-upstream-title-fallback",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=_trend_payload(
            period_start=period_start,
            period_end=period_end,
            evidence_doc_id=evidence_doc_id,
        ),
    )

    from recoleta.rag import ideas_agent

    monkeypatch.setattr(
        ideas_agent,
        "generate_trend_ideas_payload",
        lambda **_kwargs: (
            _ideas_payload(
                period_start=period_start,
                period_end=period_end,
                evidence_doc_ids=evidence_doc_ids,
            ),
            _generation_debug(*evidence_doc_ids),
        ),
    )
    monkeypatch.setattr(
        ideas_agent,
        "generate_trend_ideas_bundle_title",
        lambda **_kwargs: (_ for _ in ()).throw(RuntimeError("title model timeout")),
    )

    result = service.ideas(
        run_id="run-ideas-title-fallback",
        granularity="day",
        anchor_date=date(2026, 3, 2),
        llm_model="test/fake-model",
    )

    assert result.status == PassStatus.SUCCEEDED.value
    assert result.title == "Unnormalized title that should be replaced"
    assert result.note_path is not None
    assert result.note_path.exists()

    metric_values = _metric_values(
        repository=repository, run_id="run-ideas-title-fallback"
    )
    assert metric_values["pipeline.trends.pass.ideas.bundle_title_failed_total"] == 1.0


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
    evidence_doc_ids = _seed_item_documents(
        repository=repository,
        published_at=period_start + (period_end - period_start) / 2,
    )
    evidence_doc_id = evidence_doc_ids[0]
    upstream_pass_output_id = _persist_trend_synthesis_pass_output(
        repository=repository,
        run_id="run-trend-upstream-ungrounded",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=_trend_payload(
            period_start=period_start,
            period_end=period_end,
            evidence_doc_id=evidence_doc_id,
        ),
    )

    from recoleta.rag import ideas_agent

    monkeypatch.setattr(
        ideas_agent,
        "generate_trend_ideas_payload",
        lambda **_kwargs: (
            _ideas_payload(
                period_start=period_start,
                period_end=period_end,
                evidence_doc_ids=evidence_doc_ids,
                with_evidence=False,
            ),
            {"tool_calls_total": 0, "tool_call_breakdown": {}},
        ),
    )
    monkeypatch.setattr(
        ideas_agent,
        "generate_trend_ideas_bundle_title",
        lambda **_kwargs: (_ for _ in ()).throw(
            AssertionError("bundle title generation should be skipped for empty ideas")
        ),
    )

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

    with Session(repository.engine) as session:
        row = session.exec(
            select(PassOutput).where(PassOutput.id == result.pass_output_id)
        ).one()
        payload = TrendIdeasPayload.model_validate(json.loads(str(row.payload_json)))
        assert payload.title == "本期暂无想法"
        assert payload.summary_md == "本期没有保留想法。"
        diagnostics = json.loads(row.diagnostics_json or "{}")
        assert (
            diagnostics["workflow_freshness"]["components"]["upstream_pass_output_id"]
            == upstream_pass_output_id
        )


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
    evidence_doc_ids = _seed_item_documents(
        repository=repository,
        published_at=period_start + (period_end - period_start) / 2,
    )
    evidence_doc_id = evidence_doc_ids[0]
    _persist_trend_synthesis_pass_output(
        repository=repository,
        run_id="run-trend-upstream-obsidian",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=_trend_payload(
            period_start=period_start,
            period_end=period_end,
            evidence_doc_id=evidence_doc_id,
        ),
    )

    from recoleta.rag import ideas_agent

    monkeypatch.setattr(
        ideas_agent,
        "generate_trend_ideas_payload",
        lambda **_kwargs: (
            _ideas_payload(
                period_start=period_start,
                period_end=period_end,
                evidence_doc_ids=evidence_doc_ids,
            ),
            _generation_debug(*evidence_doc_ids),
        ),
    )
    monkeypatch.setattr(
        ideas_agent,
        "generate_trend_ideas_bundle_title",
        lambda **_kwargs: (
            "Verification-first agent rollout",
            {
                "usage": {"requests": 1, "input_tokens": 8, "output_tokens": 4},
                "estimated_cost_usd": 0.0,
                "prompt_chars": 64,
            },
        ),
    )

    result = service.ideas(
        run_id="run-ideas-obsidian",
        granularity="day",
        anchor_date=date(2026, 3, 2),
        llm_model="test/fake-model",
    )

    assert result.status == PassStatus.SUCCEEDED.value
    assert result.note_path is None
    assert not (
        settings.markdown_output_dir / "Ideas" / "day--2026-03-02--ideas.md"
    ).exists()

    assert settings.obsidian_vault_path is not None
    obsidian_note = (
        settings.obsidian_vault_path
        / settings.obsidian_base_folder
        / "Ideas"
        / "day--2026-03-02--ideas.md"
    )
    assert obsidian_note.exists()
    assert "# Verification-first agent rollout" in obsidian_note.read_text(
        encoding="utf-8"
    )
