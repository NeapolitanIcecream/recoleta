from __future__ import annotations

from datetime import UTC, date, datetime
import json
from pathlib import Path
import shutil

import fitz
import pytest

import recoleta.publish as publish_module
from recoleta.pipeline import PipelineService
from recoleta.publish import render_trend_note_pdf, write_markdown_trend_note
from recoleta.trends import TrendPayload
from recoleta.types import ItemDraft
from tests.spec_support import FakeAnalyzer, FakeTelegramSender, _build_runtime


def test_render_trend_note_pdf_preserves_title_and_sections(tmp_path: Path) -> None:
    note_path = write_markdown_trend_note(
        output_dir=tmp_path,
        trend_doc_id=7,
        title="Agentic tooling shifts into evaluation loops",
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

    assert "Agentic tooling shifts into evaluation loops" in text
    assert "Overview" in text
    assert "Representative sources" in text


def test_render_trend_note_pdf_debug_bundle_exports_intermediate_files(
    tmp_path: Path,
) -> None:
    note_path = write_markdown_trend_note(
        output_dir=tmp_path,
        trend_doc_id=8,
        title="Agentic tooling shifts into evaluation loops",
        granularity="week",
        period_start=datetime(2026, 3, 2, tzinfo=UTC),
        period_end=datetime(2026, 3, 9, tzinfo=UTC),
        run_id="run-trend-pdf-debug",
        overview_md="## Signal\n\n- A stronger emphasis on evaluation loops.\n",
        topics=["agents", "evaluation"],
        clusters=[],
        highlights=["Teams are optimizing for system reliability, not just demos."],
    )

    debug_dir = tmp_path / "pdf-debug"
    pdf_path = render_trend_note_pdf(markdown_path=note_path, debug_dir=debug_dir)

    assert pdf_path.exists()
    assert (debug_dir / "manifest.json").exists()
    assert (debug_dir / "source.md").exists()
    assert (debug_dir / "normalized.md").exists()
    assert (debug_dir / "document.html").exists()
    assert (debug_dir / "styles.css").exists()
    assert list(debug_dir.glob("page-*.png"))

    manifest = json.loads((debug_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["page_count"] >= 1
    assert manifest["pdf_path"].endswith(".pdf")
    assert manifest["title"] == "Agentic tooling shifts into evaluation loops"


def test_render_trend_note_pdf_browser_renderer_uses_continuous_page(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    note_path = write_markdown_trend_note(
        output_dir=tmp_path,
        trend_doc_id=18,
        title="Agentic tooling shifts into evaluation loops",
        granularity="week",
        period_start=datetime(2026, 3, 2, tzinfo=UTC),
        period_end=datetime(2026, 3, 9, tzinfo=UTC),
        run_id="run-trend-pdf-browser",
        overview_md="A denser browser-based PDF renderer.",
        topics=["agents", "evaluation"],
        clusters=[],
        highlights=["Browser PDF should support continuous height."],
    )

    calls: dict[str, object] = {}

    class _FakePage:
        def set_content(self, html: str, *, wait_until: str = "load") -> None:
            calls["html"] = html
            calls["wait_until"] = wait_until

        def emulate_media(self, *, media: str) -> None:
            calls["media"] = media

        def evaluate(self, _script: str) -> int:
            return 2400

        def pdf(self, **kwargs: object) -> None:
            calls["pdf_kwargs"] = kwargs
            pdf_path = Path(str(kwargs["path"]))
            pdf_path.parent.mkdir(parents=True, exist_ok=True)
            doc = fitz.open()
            doc.new_page()
            doc.save(pdf_path)
            doc.close()

    class _FakeBrowser:
        def new_page(self, **kwargs: object) -> _FakePage:
            calls["new_page_kwargs"] = kwargs
            return _FakePage()

        def close(self) -> None:
            calls["browser_closed"] = True

    class _FakeChromium:
        def launch(self, **kwargs: object) -> _FakeBrowser:
            calls["launch_kwargs"] = kwargs
            return _FakeBrowser()

    class _FakePlaywrightContext:
        chromium = _FakeChromium()

        def __enter__(self) -> "_FakePlaywrightContext":
            return self

        def __exit__(self, *_args: object) -> None:
            return None

    monkeypatch.setattr(
        publish_module,
        "_get_playwright_sync_api",
        lambda: (lambda: _FakePlaywrightContext()),
    )
    monkeypatch.setattr(
        publish_module,
        "_trend_pdf_browser_launch_options",
        lambda: [{"executable_path": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"}],
    )

    debug_dir = tmp_path / "browser-debug"
    pdf_path = publish_module.render_trend_note_pdf(
        markdown_path=note_path,
        backend="browser",
        page_mode="continuous",
        debug_dir=debug_dir,
    )

    assert pdf_path.exists()
    assert calls["media"] == "screen"
    assert "width" in dict(calls["pdf_kwargs"])  # type: ignore[arg-type]
    assert dict(calls["pdf_kwargs"])["width"] == "210mm"  # type: ignore[arg-type]
    assert str(dict(calls["pdf_kwargs"])["height"]).endswith("px")  # type: ignore[arg-type]

    manifest = json.loads((debug_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["renderer"] == "browser"
    assert manifest["page_mode"] == "continuous"


def test_prepare_trend_pdf_browser_css_uses_raster_card_gradients(
    tmp_path: Path,
) -> None:
    """Regression: browser PDF card gradients must avoid vector print seams."""

    note_path = write_markdown_trend_note(
        output_dir=tmp_path,
        trend_doc_id=20,
        title="Agentic tooling shifts into evaluation loops",
        granularity="week",
        period_start=datetime(2026, 3, 2, tzinfo=UTC),
        period_end=datetime(2026, 3, 9, tzinfo=UTC),
        run_id="run-trend-pdf-css",
        overview_md="Raster card gradients should stay visually stable in PDF viewers.",
        topics=["agents"],
        clusters=[],
        highlights=["Card backgrounds should not show horizontal seams."],
    )

    inputs = publish_module._prepare_trend_pdf_render_inputs(
        markdown_path=note_path,
        backend="browser",
        page_mode="continuous",
    )

    assert 'url("data:image/png;base64,' in inputs.css
    assert (
        "linear-gradient(180deg, rgba(235, 243, 253, 0.99),"
        " rgba(248, 251, 254, 0.99))" not in inputs.css
    )


def test_render_trend_note_pdf_auto_falls_back_to_story_renderer(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    note_path = write_markdown_trend_note(
        output_dir=tmp_path,
        trend_doc_id=19,
        title="Agentic tooling shifts into evaluation loops",
        granularity="week",
        period_start=datetime(2026, 3, 2, tzinfo=UTC),
        period_end=datetime(2026, 3, 9, tzinfo=UTC),
        run_id="run-trend-pdf-fallback",
        overview_md="Browser rendering fails, story renderer saves the day.",
        topics=["agents"],
        clusters=[],
        highlights=[],
    )

    calls = {"story_total": 0}

    def _fake_browser_render(_inputs: object) -> None:
        raise RuntimeError("simulated browser render failure")

    def _fake_story_render(inputs: object) -> None:
        calls["story_total"] += 1
        output_path = Path(str(getattr(inputs, "output_path")))
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((72, 72), "story fallback")
        doc.save(output_path)
        doc.close()

    monkeypatch.setattr(
        publish_module,
        "_render_trend_note_pdf_browser",
        _fake_browser_render,
    )
    monkeypatch.setattr(
        publish_module,
        "_render_trend_note_pdf_story",
        _fake_story_render,
    )

    pdf_path = publish_module.render_trend_note_pdf(
        markdown_path=note_path,
        backend="auto",
    )

    assert pdf_path.exists()
    assert calls["story_total"] == 1


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
        title="Agents bundle retrieval, tools, and planning",
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
    assert "Agents bundle retrieval, tools, and planning" in str(
        document_payload["caption"] or ""
    )
    assert "Overview" in str(document_payload["caption"] or "")

    trends_dir = settings.markdown_output_dir / "Trends"
    markdown_files = sorted(trends_dir.glob("*.md"))
    pdf_files = sorted(trends_dir.glob("*.pdf"))
    assert len(markdown_files) == 1
    assert len(pdf_files) == 1
    assert pdf_files[0].name == markdown_files[0].with_suffix(".pdf").name

    with fitz.open(stream=document_payload["content"], filetype="pdf") as document:
        text = "\n".join(str(page.get_text()) for page in document)

    normalized_text = " ".join(text.split())
    assert "Agents bundle retrieval, tools, and planning" in normalized_text

    metrics = repository.list_metrics(run_id="run-trend-telegram")
    by_name = {metric.name: metric for metric in metrics}
    assert by_name["pipeline.trends.pdf.generated_total"].value == 1
    assert (
        by_name["pipeline.trends.pdf.browser.generated_total"].value
        + by_name["pipeline.trends.pdf.story.generated_total"].value
        == 1
    )
    assert by_name["pipeline.trends.telegram.sent_total"].value == 1
    assert by_name["pipeline.trends.telegram.failed_total"].value == 0


def test_trends_telegram_publish_respects_daily_delivery_cap(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Regression: trend PDFs must not bypass the shared Telegram daily cap."""

    monkeypatch.setenv("PUBLISH_TARGETS", "telegram")
    monkeypatch.setenv("MAX_DELIVERIES_PER_DAY", "0")
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

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="trend-telegram-cap-1",
        canonical_url="https://example.com/trend-telegram-cap-1",
        title="Trend Cap",
        authors=["Alice"],
        published_at=datetime(2026, 3, 5, 8, 0, tzinfo=UTC),
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-trend-telegram-cap-prepare", drafts=[draft], limit=10)
    service.analyze(run_id="run-trend-telegram-cap-analyze", limit=10)

    from recoleta.rag import agent as rag_agent

    payload = TrendPayload(
        title="Agents bundle retrieval, tools, and planning",
        granularity="day",
        period_start=datetime(2026, 3, 5, tzinfo=UTC).isoformat(),
        period_end=datetime(2026, 3, 6, tzinfo=UTC).isoformat(),
        overview_md="The daily cap should block this PDF delivery.",
        topics=["agents"],
        clusters=[],
        highlights=["No outbound Telegram delivery should be created."],
    )

    def _fake_generate(**_kwargs):  # type: ignore[no-untyped-def]
        return payload, {"tool_calls_total": 0}

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    result = service.trends(
        run_id="run-trend-telegram-cap",
        granularity="day",
        anchor_date=date(2026, 3, 5),
        llm_model="test/fake-model",
    )

    assert result.doc_id > 0
    assert len(sender.documents) == 0
    assert not (settings.markdown_output_dir / "Trends").exists()

    metrics = repository.list_metrics(run_id="run-trend-telegram-cap")
    by_name = {metric.name: metric for metric in metrics}
    assert by_name["pipeline.trends.pdf.generated_total"].value == 0
    assert by_name["pipeline.trends.telegram.sent_total"].value == 0
    assert by_name["pipeline.trends.telegram.failed_total"].value == 0


def test_publish_counts_trend_delivery_toward_telegram_daily_cap(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Regression: item publish must count earlier trend PDF sends against the same cap."""

    monkeypatch.setenv("PUBLISH_TARGETS", "telegram")
    monkeypatch.setenv("MAX_DELIVERIES_PER_DAY", "1")
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

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="trend-telegram-cap-shared-1",
        canonical_url="https://example.com/trend-telegram-cap-shared-1",
        title="Trend Cap Shared",
        authors=["Alice"],
        published_at=datetime(2026, 3, 5, 8, 0, tzinfo=UTC),
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-trend-telegram-cap-shared-prepare", drafts=[draft], limit=10)
    service.analyze(run_id="run-trend-telegram-cap-shared-analyze", limit=10)

    from recoleta.rag import agent as rag_agent

    payload = TrendPayload(
        title="Agents bundle retrieval, tools, and planning",
        granularity="day",
        period_start=datetime(2026, 3, 5, tzinfo=UTC).isoformat(),
        period_end=datetime(2026, 3, 6, tzinfo=UTC).isoformat(),
        overview_md="The trend delivery should consume the only allowed send today.",
        topics=["agents"],
        clusters=[],
        highlights=["Subsequent item publishing should be skipped."],
    )

    def _fake_generate(**_kwargs):  # type: ignore[no-untyped-def]
        return payload, {"tool_calls_total": 0}

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    trend_result = service.trends(
        run_id="run-trend-telegram-cap-shared-trend",
        granularity="day",
        anchor_date=date(2026, 3, 5),
        llm_model="test/fake-model",
    )
    publish_result = service.publish(
        run_id="run-trend-telegram-cap-shared-publish",
        limit=10,
    )

    assert trend_result.doc_id > 0
    assert len(sender.documents) == 1
    assert publish_result.sent == 0
    assert publish_result.failed == 0
    assert len(sender.messages) == 0


def test_trends_telegram_publish_debug_pdf_exports_preview_bundle(
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

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="trend-telegram-debug-1",
        canonical_url="https://example.com/trend-telegram-debug-1",
        title="Tool-Using Agents",
        authors=["Alice"],
        published_at=datetime(2026, 3, 5, 8, 0, tzinfo=UTC),
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-trend-telegram-debug", drafts=[draft], limit=10)
    service.analyze(run_id="run-trend-telegram-debug", limit=10)

    from recoleta.rag import agent as rag_agent

    payload = TrendPayload(
        title="Agents bundle retrieval, tools, and planning",
        granularity="day",
        period_start=datetime(2026, 3, 5, tzinfo=UTC).isoformat(),
        period_end=datetime(2026, 3, 6, tzinfo=UTC).isoformat(),
        overview_md="Debug mode should export render intermediates.",
        topics=["agents"],
        clusters=[],
        highlights=["Preview artifacts help visual iteration."],
    )

    def _fake_generate(**_kwargs):  # type: ignore[no-untyped-def]
        return payload, {"tool_calls_total": 0}

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    result = service.trends(
        run_id="run-trend-telegram-debug",
        granularity="day",
        anchor_date=date(2026, 3, 5),
        llm_model="test/fake-model",
        debug_pdf=True,
    )

    assert result.doc_id > 0
    assert len(sender.documents) == 1

    debug_root = settings.markdown_output_dir / "Trends" / ".pdf-debug"
    manifests = sorted(debug_root.glob("*/manifest.json"))
    assert len(manifests) == 1

    metrics = repository.list_metrics(run_id="run-trend-telegram-debug")
    by_name = {metric.name: metric for metric in metrics}
    assert by_name["pipeline.trends.pdf.debug.generated_total"].value == 1
    assert by_name["pipeline.trends.pdf.debug.failed_total"].value == 0


def test_trends_telegram_publish_debug_pdf_failure_is_non_fatal(
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

    debug_root = settings.markdown_output_dir / "Trends" / ".pdf-debug"
    debug_root.parent.mkdir(parents=True, exist_ok=True)
    debug_root.write_text("not-a-directory", encoding="utf-8")

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="trend-telegram-debug-fail-1",
        canonical_url="https://example.com/trend-telegram-debug-fail-1",
        title="Tool-Using Agents",
        authors=["Alice"],
        published_at=datetime(2026, 3, 5, 8, 0, tzinfo=UTC),
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-trend-telegram-debug-fail", drafts=[draft], limit=10)
    service.analyze(run_id="run-trend-telegram-debug-fail", limit=10)

    from recoleta.rag import agent as rag_agent

    payload = TrendPayload(
        title="Agents bundle retrieval, tools, and planning",
        granularity="day",
        period_start=datetime(2026, 3, 5, tzinfo=UTC).isoformat(),
        period_end=datetime(2026, 3, 6, tzinfo=UTC).isoformat(),
        overview_md="Debug export failures must not block Telegram delivery.",
        topics=["agents"],
        clusters=[],
        highlights=["The PDF still needs to go out."],
    )

    def _fake_generate(**_kwargs):  # type: ignore[no-untyped-def]
        return payload, {"tool_calls_total": 0}

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    result = service.trends(
        run_id="run-trend-telegram-debug-fail",
        granularity="day",
        anchor_date=date(2026, 3, 5),
        llm_model="test/fake-model",
        debug_pdf=True,
    )

    assert result.doc_id > 0
    assert len(sender.documents) == 1
    assert debug_root.is_file()

    metrics = repository.list_metrics(run_id="run-trend-telegram-debug-fail")
    by_name = {metric.name: metric for metric in metrics}
    assert by_name["pipeline.trends.pdf.generated_total"].value == 1
    assert by_name["pipeline.trends.pdf.debug.generated_total"].value == 0
    assert by_name["pipeline.trends.pdf.debug.failed_total"].value == 1

    debug_root.unlink()
    shutil.rmtree(settings.markdown_output_dir, ignore_errors=True)


def test_trends_telegram_publish_skips_duplicate_delivery_for_unchanged_period(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Regression: rerunning the same trend period must not resend identical PDFs."""

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

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="trend-telegram-dedupe-1",
        canonical_url="https://example.com/trend-telegram-dedupe-1",
        title="Trend Dedupe",
        authors=["Alice"],
        published_at=datetime(2026, 3, 5, 8, 0, tzinfo=UTC),
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-trend-telegram-dedupe-prepare", drafts=[draft], limit=10)
    service.analyze(run_id="run-trend-telegram-dedupe-analyze", limit=10)

    from recoleta.rag import agent as rag_agent

    payload = TrendPayload(
        title="Agents bundle retrieval, tools, and planning",
        granularity="day",
        period_start=datetime(2026, 3, 5, tzinfo=UTC).isoformat(),
        period_end=datetime(2026, 3, 6, tzinfo=UTC).isoformat(),
        overview_md="The period-level trend content is unchanged.",
        topics=["agents"],
        clusters=[],
        highlights=["This list should not affect delivery dedupe."],
    )

    def _fake_generate(**_kwargs):  # type: ignore[no-untyped-def]
        return payload, {"tool_calls_total": 0}

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    first_result = service.trends(
        run_id="run-trend-telegram-dedupe-first",
        granularity="day",
        anchor_date=date(2026, 3, 5),
        llm_model="test/fake-model",
    )
    second_result = service.trends(
        run_id="run-trend-telegram-dedupe-second",
        granularity="day",
        anchor_date=date(2026, 3, 5),
        llm_model="test/fake-model",
    )

    assert first_result.doc_id > 0
    assert second_result.doc_id == first_result.doc_id
    assert len(sender.documents) == 1

    second_metrics = repository.list_metrics(run_id="run-trend-telegram-dedupe-second")
    second_by_name = {metric.name: metric for metric in second_metrics}
    assert second_by_name["pipeline.trends.telegram.sent_total"].value == 0
    assert second_by_name["pipeline.trends.telegram.failed_total"].value == 0


def test_trends_empty_period_does_not_publish_telegram_message(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Regression: empty trend periods should not create outbound Telegram deliveries."""

    monkeypatch.setenv("PUBLISH_TARGETS", "telegram")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-bot-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "test-chat-id")
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))

    settings, repository = _build_runtime()
    sender = FakeTelegramSender()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=sender,
    )

    result = service.trends(
        run_id="run-trend-telegram-empty",
        granularity="day",
        anchor_date=date(2026, 3, 5),
        llm_model="test/fake-model",
    )

    assert result.doc_id > 0
    assert len(sender.messages) == 0
    assert len(sender.documents) == 0
    assert not (settings.markdown_output_dir / "Trends").exists()

    metrics = repository.list_metrics(run_id="run-trend-telegram-empty")
    by_name = {metric.name: metric for metric in metrics}
    assert by_name["pipeline.trends.pdf.generated_total"].value == 0
    assert by_name["pipeline.trends.pdf.failed_total"].value == 0
    assert by_name["pipeline.trends.telegram.sent_total"].value == 0
    assert by_name["pipeline.trends.telegram.failed_total"].value == 0


def test_trends_telegram_publish_uses_injected_sender_without_telegram_credentials(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Regression: trend Telegram delivery should work with an injected sender alone."""

    monkeypatch.setenv("PUBLISH_TARGETS", "telegram")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)
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

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="trend-telegram-injected-sender-1",
        canonical_url="https://example.com/trend-telegram-injected-sender-1",
        title="Injected Sender Trend",
        authors=["Alice"],
        published_at=datetime(2026, 3, 5, 8, 0, tzinfo=UTC),
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-trend-telegram-injected-sender", drafts=[draft], limit=10)
    service.analyze(run_id="run-trend-telegram-injected-sender", limit=10)

    from recoleta.rag import agent as rag_agent

    def _fake_generate(**_kwargs):  # type: ignore[no-untyped-def]
        return (
            TrendPayload(
                title="Agents bundle retrieval, tools, and planning",
                granularity="day",
                period_start=datetime(2026, 3, 5, tzinfo=UTC).isoformat(),
                period_end=datetime(2026, 3, 6, tzinfo=UTC).isoformat(),
                overview_md="Injected senders should be sufficient for trend delivery.",
                topics=["agents"],
                clusters=[],
                highlights=["No explicit bot credentials should be required here."],
            ),
            {"tool_calls_total": 0},
        )

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    result = service.trends(
        run_id="run-trend-telegram-injected-sender",
        granularity="day",
        anchor_date=date(2026, 3, 5),
        llm_model="test/fake-model",
    )

    assert result.doc_id > 0
    assert len(sender.documents) == 1

    metrics = repository.list_metrics(run_id="run-trend-telegram-injected-sender")
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
                title="Agents bundle retrieval, tools, and planning",
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
