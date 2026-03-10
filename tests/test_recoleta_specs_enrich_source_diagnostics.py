from __future__ import annotations

import pytest

from recoleta.pipeline import PipelineService
from recoleta.types import ItemDraft
from tests.spec_support import FakeAnalyzer, FakeTelegramSender, _build_runtime


def test_enrich_records_source_metrics_for_html_and_pdf_paths(
    configured_env, monkeypatch: pytest.MonkeyPatch
) -> None:
    import recoleta.pipeline as pipeline_module

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    drafts = [
        ItemDraft.from_values(
            source="rss",
            source_item_id="rss-1",
            canonical_url="https://example.com/rss-1",
            title="RSS Item",
        ),
        ItemDraft.from_values(
            source="hn",
            source_item_id="hn-1",
            canonical_url="https://example.com/hn-1",
            title="HN Item",
        ),
        ItemDraft.from_values(
            source="hf_daily",
            source_item_id="papers/1",
            canonical_url="https://example.com/hf-1",
            title="HF Daily Item",
        ),
        ItemDraft.from_values(
            source="openreview",
            source_item_id="openreview-1",
            canonical_url="https://openreview.net/forum?id=openreview-1",
            title="OpenReview Item",
        ),
    ]

    service.ingest(run_id="run-source-enrich-diag", drafts=drafts)

    monkeypatch.setattr(
        pipeline_module,
        "extract_html_maintext",
        lambda html: "clean html maintext " * 20,  # noqa: ARG005
    )
    monkeypatch.setattr(
        pipeline_module,
        "fetch_url_bytes",
        lambda client, url: b"%PDF-1.7 fake",  # noqa: ARG005
    )

    def _fake_extract_pdf_text(
        pdf_bytes: bytes, *, diag: dict[str, object] | None = None
    ) -> str | None:
        if diag is not None:
            diag["pdf_backend"] = "pymupdf4llm"
        return "clean pdf text " * 25

    monkeypatch.setattr(pipeline_module, "extract_pdf_text", _fake_extract_pdf_text)

    service.enrich(run_id="run-source-enrich-diag", limit=10)

    metrics = repository.list_metrics(run_id="run-source-enrich-diag")
    by_name = {
        str(getattr(metric, "name", "") or ""): float(getattr(metric, "value", 0) or 0)
        for metric in metrics
    }

    assert by_name["pipeline.enrich.source.rss.processed_total"] == 1
    assert by_name["pipeline.enrich.source.hn.processed_total"] == 1
    assert by_name["pipeline.enrich.source.hf_daily.processed_total"] == 1
    assert by_name["pipeline.enrich.source.openreview.processed_total"] == 1
    assert by_name["pipeline.enrich.source.rss.content_type.html_maintext_total"] == 1
    assert by_name["pipeline.enrich.source.hn.content_type.html_maintext_total"] == 1
    assert (
        by_name["pipeline.enrich.source.hf_daily.content_type.html_maintext_total"]
        == 1
    )
    assert (
        by_name["pipeline.enrich.source.openreview.content_type.pdf_text_total"] == 1
    )
    assert by_name["pipeline.enrich.source.rss.content_chars_sum"] > 0
    assert by_name["pipeline.enrich.source.openreview.content_chars_sum"] > 0

