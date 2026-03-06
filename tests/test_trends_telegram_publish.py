from __future__ import annotations

from datetime import UTC, date, datetime
import json
from pathlib import Path

import fitz
import pytest

from recoleta.pipeline import PipelineService
from recoleta.publish import render_trend_note_pdf, write_markdown_trend_note
from recoleta.trends import TrendPayload
from recoleta.types import ItemDraft
from tests.spec_support import FakeAnalyzer, FakeTelegramSender, _build_runtime


def test_render_trend_note_pdf_preserves_title_and_sections(tmp_path: Path) -> None:
    note_path = write_markdown_trend_note(
        output_dir=tmp_path,
        trend_doc_id=7,
        title="Weekly Trend",
        granularity="week",
        period_start=datetime(2026, 3, 2, tzinfo=UTC),
        period_end=datetime(2026, 3, 9, tzinfo=UTC),
        run_id="run-trend-pdf",
        overview_md="## Signal\n\n- A strong shift toward agentic tooling.\n",
        topics=["agents", "tooling"],
        clusters=[
            {
                "name": "Top must-read",
                "description": "The strongest cluster of the week.",
                "representative_chunks": [
                    {
                        "doc_id": 1,
                        "chunk_index": 0,
                        "title": "Robots That Use Tools",
                        "url": "https://example.com/paper-1",
                        "authors": ["Alice", "Bob"],
                    }
                ],
            }
        ],
        highlights=["Tool use is converging with long-context workflows."],
    )

    pdf_path = render_trend_note_pdf(markdown_path=note_path)

    assert pdf_path.exists()
    assert pdf_path.suffix == ".pdf"
    assert pdf_path.read_bytes().startswith(b"%PDF")

    with fitz.open(pdf_path) as document:
        text = "\n".join(str(page.get_text()) for page in document)

    assert "Weekly Trend" in text
    assert "Overview" in text
    assert "Representative papers" in text


def test_trends_telegram_publish_sends_overview_caption_and_pdf_document(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("PUBLISH_TARGETS", "telegram")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-bot-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "test-chat-id")
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("TOPICS", json.dumps(["agents"]))
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))

    settings, repository = _build_runtime()
    sender = FakeTelegramSender()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=sender,
    )

    anchor = date(2026, 3, 5)
    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="trend-telegram-1",
        canonical_url="https://example.com/trend-telegram-1",
        title="Tool-Using Agents",
        authors=["Alice"],
        published_at=datetime(2026, 3, 5, 8, 0, tzinfo=UTC),
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-trend-telegram", drafts=[draft], limit=10)
    service.analyze(run_id="run-trend-telegram", limit=10)

    from recoleta.rag import agent as rag_agent

    payload = TrendPayload(
        title="Daily Trend",
        granularity="day",
        period_start=datetime(2026, 3, 5, tzinfo=UTC).isoformat(),
        period_end=datetime(2026, 3, 6, tzinfo=UTC).isoformat(),
        overview_md=(
            "## Overview\n\n"
            "- Agents are bundling retrieval, tools, and planning.\n"
            "- Evaluation is moving from static benchmarks to task loops.\n"
        ),
        topics=["agents"],
        clusters=[],
        highlights=["Agent stacks are getting more production-shaped."],
    )

    def _fake_generate(**_kwargs):  # type: ignore[no-untyped-def]
        return payload, {"tool_calls_total": 0}

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    result = service.trends(
        run_id="run-trend-telegram",
        granularity="day",
        anchor_date=anchor,
        llm_model="test/fake-model",
    )

    assert result.doc_id > 0
    assert len(sender.messages) == 0
    assert len(sender.documents) == 1

    document_payload = sender.documents[0]
    assert document_payload["filename"].endswith(".pdf")
    assert document_payload["content"].startswith(b"%PDF")
    assert "Daily Trend" in str(document_payload["caption"] or "")
    assert "Overview" in str(document_payload["caption"] or "")

    trends_dir = settings.markdown_output_dir / "Trends"
    markdown_files = sorted(trends_dir.glob("*.md"))
    pdf_files = sorted(trends_dir.glob("*.pdf"))
    assert len(markdown_files) == 1
    assert len(pdf_files) == 1
    assert pdf_files[0].name == markdown_files[0].with_suffix(".pdf").name

    with fitz.open(stream=document_payload["content"], filetype="pdf") as document:
        text = "\n".join(str(page.get_text()) for page in document)

    assert "Daily Trend" in text
    assert "Agent stacks are getting more production-shaped." in text

    metrics = repository.list_metrics(run_id="run-trend-telegram")
    by_name = {metric.name: metric for metric in metrics}
    assert by_name["pipeline.trends.pdf.generated_total"].value == 1
    assert by_name["pipeline.trends.telegram.sent_total"].value == 1
    assert by_name["pipeline.trends.telegram.failed_total"].value == 0


def test_trends_telegram_publish_records_failure_metric_when_document_send_fails(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    class FailingDocumentTelegramSender(FakeTelegramSender):
        def send_document(
            self,
            *,
            filename: str,
            content: bytes,
            caption: str | None = None,
        ) -> str:
            _ = (filename, content, caption)
            raise RuntimeError("simulated telegram document failure")

    monkeypatch.setenv("PUBLISH_TARGETS", "telegram")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-bot-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "test-chat-id")
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("TOPICS", json.dumps(["agents"]))
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))

    settings, repository = _build_runtime()
    sender = FailingDocumentTelegramSender()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=sender,
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="trend-telegram-failure-1",
        canonical_url="https://example.com/trend-telegram-failure-1",
        title="Failure Case",
        authors=["Alice"],
        published_at=datetime(2026, 3, 5, 8, 0, tzinfo=UTC),
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-trend-telegram-fail", drafts=[draft], limit=10)
    service.analyze(run_id="run-trend-telegram-fail", limit=10)

    from recoleta.rag import agent as rag_agent

    def _fake_generate(**_kwargs):  # type: ignore[no-untyped-def]
        return (
            TrendPayload(
                title="Daily Trend",
                granularity="day",
                period_start=datetime(2026, 3, 5, tzinfo=UTC).isoformat(),
                period_end=datetime(2026, 3, 6, tzinfo=UTC).isoformat(),
                overview_md="A delivery failure should not discard the trend note.",
                topics=["agents"],
                clusters=[],
                highlights=[],
            ),
            {"tool_calls_total": 0},
        )

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    result = service.trends(
        run_id="run-trend-telegram-fail",
        granularity="day",
        anchor_date=date(2026, 3, 5),
        llm_model="test/fake-model",
    )

    assert result.doc_id > 0

    metrics = repository.list_metrics(run_id="run-trend-telegram-fail")
    by_name = {metric.name: metric for metric in metrics}
    assert by_name["pipeline.trends.pdf.generated_total"].value == 1
    assert by_name["pipeline.trends.telegram.sent_total"].value == 0
    assert by_name["pipeline.trends.telegram.failed_total"].value == 1

    trends_dir = settings.markdown_output_dir / "Trends"
    assert len(list(trends_dir.glob("*.md"))) == 1
    assert len(list(trends_dir.glob("*.pdf"))) == 1
