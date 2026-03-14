from __future__ import annotations

from datetime import UTC, date, datetime
import json
from pathlib import Path

import pytest
from sqlmodel import Session, select

from recoleta.models import Document, DocumentChunk, Metric, PassOutput
from recoleta.pipeline import PipelineService
from recoleta.types import ItemDraft
from tests.spec_support import FakeAnalyzer, FakeTelegramSender, _build_runtime


def test_trends_persist_canonical_pass_output_before_projection_rewrites(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
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
    repository.create_run(
        config_fingerprint="fp-run-trend-pass-output",
        run_id="run-trend-pass-output",
    )

    published_at = datetime(2026, 3, 2, 1, 0, tzinfo=UTC)
    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="trend-pass-output-1",
        canonical_url="https://example.com/pass-output-paper",
        title="Pass Output Paper",
        authors=["Alice"],
        published_at=published_at,
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-trend-pass-output", drafts=[draft], limit=10)
    service.analyze(run_id="run-trend-pass-output", limit=10)

    from recoleta.rag import agent as rag_agent
    from recoleta.trends import TrendPayload

    def _fake_generate(**kwargs):  # type: ignore[no-untyped-def]
        repo = kwargs["repository"]
        pstart = kwargs["period_start"]
        pend = kwargs["period_end"]
        docs = repo.list_documents(
            doc_type="item",
            period_start=pstart,
            period_end=pend,
            granularity=None,
            order_by="event_desc",
            offset=0,
            limit=1,
        )
        assert docs and docs[0].id is not None
        doc_id = int(docs[0].id)
        payload = {
            "title": "Daily Trend",
            "granularity": "day",
            "period_start": pstart.isoformat(),
            "period_end": pend.isoformat(),
            "overview_md": f"See doc_id: {doc_id}, chunk: 0.",
            "topics": ["agents"],
            "clusters": [],
            "highlights": [f"Hit doc_id {doc_id}, chunk 0"],
        }
        return TrendPayload.model_validate(payload), {"tool_calls_total": 0}

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    result = service.trends(
        run_id="run-trend-pass-output",
        granularity="day",
        anchor_date=date(2026, 3, 2),
        llm_model="test/fake-model",
    )

    assert result.doc_id > 0
    assert result.pass_output_id is not None

    with Session(repository.engine) as session:
        pass_output = session.get(PassOutput, result.pass_output_id)
        assert pass_output is not None
        canonical_payload = json.loads(pass_output.payload_json)
        assert "doc_id" in str(canonical_payload.get("overview_md") or "")

        trend_doc = session.exec(
            select(Document).where(Document.doc_type == "trend")
        ).first()
        assert trend_doc is not None
        meta_chunk = session.exec(
            select(DocumentChunk).where(
                DocumentChunk.doc_id == int(trend_doc.id or 0),
                DocumentChunk.chunk_index == 1,
            )
        ).first()
        assert meta_chunk is not None
        projected_payload = json.loads(str(meta_chunk.text))
        assert "doc_id" not in str(projected_payload.get("overview_md") or "")


def test_trends_records_metric_when_pass_output_persist_fails(
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
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )
    repository.create_run(
        config_fingerprint="fp-run-pass-output-metric",
        run_id="run-pass-output-metric",
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="trend-pass-output-2",
        canonical_url="https://example.com/pass-output-metric",
        title="Pass Output Metric",
        authors=["Alice"],
        published_at=datetime(2026, 3, 3, 1, 0, tzinfo=UTC),
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-pass-output-metric", drafts=[draft], limit=10)
    service.analyze(run_id="run-pass-output-metric", limit=10)

    from recoleta.rag import agent as rag_agent
    from recoleta.trends import TrendPayload

    def _fake_generate(**kwargs):  # type: ignore[no-untyped-def]
        pstart = kwargs["period_start"]
        pend = kwargs["period_end"]
        payload = {
            "title": "Daily Trend",
            "granularity": "day",
            "period_start": pstart.isoformat(),
            "period_end": pend.isoformat(),
            "overview_md": "- metric test",
            "topics": ["agents"],
            "clusters": [],
            "highlights": [],
        }
        return TrendPayload.model_validate(payload), {"tool_calls_total": 0}

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    def _explode_create_pass_output(**kwargs):  # type: ignore[no-untyped-def]
        _ = kwargs
        raise RuntimeError("simulated pass output write failure")

    monkeypatch.setattr(repository, "create_pass_output", _explode_create_pass_output)

    result = service.trends(
        run_id="run-pass-output-metric",
        granularity="day",
        anchor_date=date(2026, 3, 3),
        llm_model="test/fake-model",
    )

    assert result.doc_id > 0
    assert result.pass_output_id is None

    with Session(repository.engine) as session:
        metrics = list(
            session.exec(
                select(Metric).where(
                    Metric.name == "pipeline.trends.pass_outputs.persist_failed_total"
                )
            )
        )
        assert metrics
        assert metrics[-1].value == 1
        assert list(session.exec(select(PassOutput))) == []
