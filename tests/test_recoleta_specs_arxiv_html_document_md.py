from __future__ import annotations

import json
from pathlib import Path

import pytest
import respx
from sqlmodel import Session, select

from recoleta.config import Settings
from recoleta.models import Item
from recoleta.pipeline import PipelineService
from recoleta.storage import Repository
from recoleta.types import ItemDraft


def _build_service(tmp_path: Path) -> tuple[Settings, Repository, PipelineService]:
    settings = Settings()  # pyright: ignore[reportCallIssue]
    repository = Repository(
        db_path=tmp_path / "recoleta.db",
        title_dedup_threshold=settings.title_dedup_threshold,
        title_dedup_max_candidates=settings.title_dedup_max_candidates,
    )
    repository.init_schema()
    service = PipelineService(settings=settings, repository=repository)
    return settings, repository, service


def test_enrich_arxiv_html_document_writes_html_document_md(
    configured_env: Path,
    monkeypatch: pytest.MonkeyPatch,
    respx_mock: respx.Router,
) -> None:
    monkeypatch.setenv(
        "SOURCES",
        json.dumps(
            {
                "arxiv": {
                    "enabled": True,
                    "queries": ["cat:cs.AI"],
                    "enrich_method": "html_document",
                    "enrich_failure_mode": "strict",
                }
            }
        ),
    )

    arxiv_id = "1234.5678v1"
    html_url = f"https://arxiv.org/html/{arxiv_id}"
    respx_mock.get(html_url).respond(
        200,
        text=(
            "<html><body><main>"
            "<h1>Title</h1><p>Hello <b>world</b>.</p>"
            "<h2>References</h2><ol><li>Ref A</li><li>Ref B</li></ol>"
            "</main></body></html>"
        ),
        headers={"Content-Type": "text/html; charset=utf-8"},
    )

    import recoleta.pipeline as pipeline_module

    monkeypatch.setattr(
        pipeline_module,
        "convert_html_document_to_markdown",
        lambda html, **_: ("# Title\n\nHello world.\n", 7, None),  # noqa: ARG005
    )

    _, repository, service = _build_service(configured_env)
    draft = ItemDraft.from_values(
        source="arxiv",
        source_item_id=arxiv_id,
        canonical_url=f"https://arxiv.org/abs/{arxiv_id}",
        title="Test Paper",
    )
    service.ingest(run_id="run-html-md-1", drafts=[draft])
    service.enrich(run_id="run-html-md-1", limit=10)

    with Session(repository.engine) as session:
        item = session.exec(select(Item).where(Item.source_item_id == arxiv_id)).first()
        assert item is not None
        assert item.id is not None
        md = repository.get_latest_content(
            item_id=int(item.id), content_type="html_document_md"
        )
        assert md is not None
        assert (md.text or "").strip() == "# Title\n\nHello world."
        refs = repository.get_latest_content(
            item_id=int(item.id), content_type="html_references"
        )
        assert refs is not None
        assert "Ref A" in (refs.text or "")


def test_load_arxiv_content_prefers_html_document_md_for_analysis(
    configured_env: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(
        "SOURCES",
        json.dumps(
            {
                "arxiv": {
                    "enabled": True,
                    "queries": ["cat:cs.AI"],
                    "enrich_method": "html_document",
                    "enrich_failure_mode": "fallback",
                }
            }
        ),
    )

    arxiv_id = "9999.0001v1"
    _, repository, service = _build_service(configured_env)
    draft = ItemDraft.from_values(
        source="arxiv",
        source_item_id=arxiv_id,
        canonical_url=f"https://arxiv.org/abs/{arxiv_id}",
        title="Test Paper 2",
    )
    item, _ = repository.upsert_item(draft)
    assert item.id is not None
    repository.upsert_content(
        item_id=int(item.id),
        content_type="html_document",
        text="<main><p>html</p></main>",
    )
    repository.upsert_content(
        item_id=int(item.id), content_type="html_document_md", text="# md preferred"
    )

    loaded = service._load_arxiv_content_for_analysis(item_id=int(item.id))  # noqa: SLF001
    assert loaded == "# md preferred"


def test_enrich_arxiv_html_document_records_pandoc_warning_metrics(
    configured_env: Path,
    monkeypatch: pytest.MonkeyPatch,
    respx_mock: respx.Router,
) -> None:
    monkeypatch.setenv(
        "SOURCES",
        json.dumps(
            {
                "arxiv": {
                    "enabled": True,
                    "queries": ["cat:cs.AI"],
                    "enrich_method": "html_document",
                    "enrich_failure_mode": "strict",
                }
            }
        ),
    )

    arxiv_id = "2345.6789v1"
    html_url = f"https://arxiv.org/html/{arxiv_id}"
    respx_mock.get(html_url).respond(
        200,
        text="<html><body><main><h1>Title</h1><p>Hello world.</p></main></body></html>",
        headers={"Content-Type": "text/html; charset=utf-8"},
    )

    import recoleta.pipeline as pipeline_module

    def fake_convert_html_document_to_markdown(
        html: str, **kwargs: object
    ) -> tuple[str | None, int, str | None]:
        assert "<p>Hello world.</p>" in html
        diag = kwargs.get("diag")
        if isinstance(diag, dict):
            diag["pandoc_warning_count"] = 2
            diag["pandoc_warning_tex_math_convert_failed"] = 2
            diag["pandoc_math_replaced_total"] = 1
        return "# Title\n\nHello world.\n", 9, None

    monkeypatch.setattr(
        pipeline_module,
        "convert_html_document_to_markdown",
        fake_convert_html_document_to_markdown,
    )

    _, repository, service = _build_service(configured_env)
    draft = ItemDraft.from_values(
        source="arxiv",
        source_item_id=arxiv_id,
        canonical_url=f"https://arxiv.org/abs/{arxiv_id}",
        title="Pandoc Warning Metrics",
    )
    service.ingest(run_id="run-html-md-warning-metrics", drafts=[draft])
    service.enrich(run_id="run-html-md-warning-metrics", limit=10)

    metrics = repository.list_metrics(run_id="run-html-md-warning-metrics")
    by_name = {metric.name: metric for metric in metrics}
    assert (
        by_name["pipeline.enrich.arxiv.html_document.pandoc_warning_items_total"].value
        == 1
    )
    assert (
        by_name["pipeline.enrich.arxiv.html_document.pandoc_warning_count_sum"].value
        == 2
    )
    assert (
        by_name[
            "pipeline.enrich.arxiv.html_document.pandoc_warning_tex_math_convert_failed_sum"
        ].value
        == 2
    )
    assert (
        by_name["pipeline.enrich.arxiv.html_document.pandoc_math_replaced_sum"].value
        == 1
    )


def test_enrich_arxiv_html_document_records_pandoc_failure_metric_without_failing_item(
    configured_env: Path,
    monkeypatch: pytest.MonkeyPatch,
    respx_mock: respx.Router,
) -> None:
    monkeypatch.setenv(
        "SOURCES",
        json.dumps(
            {
                "arxiv": {
                    "enabled": True,
                    "queries": ["cat:cs.AI"],
                    "enrich_method": "html_document",
                    "enrich_failure_mode": "strict",
                }
            }
        ),
    )

    arxiv_id = "2345.6790v1"
    html_url = f"https://arxiv.org/html/{arxiv_id}"
    respx_mock.get(html_url).respond(
        200,
        text="<html><body><main><h1>Title</h1><p>Hello world.</p></main></body></html>",
        headers={"Content-Type": "text/html; charset=utf-8"},
    )

    import recoleta.pipeline as pipeline_module

    def fake_convert_html_document_to_markdown(
        html: str, **kwargs: object
    ) -> tuple[str | None, int, str | None]:
        assert "<p>Hello world.</p>" in html
        diag = kwargs.get("diag")
        if isinstance(diag, dict):
            diag["pandoc_failed"] = 1
        return None, 11, "pandoc_convert_failed exit_code=64"

    monkeypatch.setattr(
        pipeline_module,
        "convert_html_document_to_markdown",
        fake_convert_html_document_to_markdown,
    )

    _, repository, service = _build_service(configured_env)
    draft = ItemDraft.from_values(
        source="arxiv",
        source_item_id=arxiv_id,
        canonical_url=f"https://arxiv.org/abs/{arxiv_id}",
        title="Pandoc Soft Failure Metric",
    )
    service.ingest(run_id="run-html-md-soft-failure", drafts=[draft])
    service.enrich(run_id="run-html-md-soft-failure", limit=10)

    metrics = repository.list_metrics(run_id="run-html-md-soft-failure")
    by_name = {metric.name: metric for metric in metrics}
    assert by_name["pipeline.enrich.failed_total"].value == 0
    assert by_name["pipeline.enrich.arxiv.html_document.pandoc_failed_total"].value == 1


def test_enrich_arxiv_html_document_records_pdf_fallback_metric(
    configured_env: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv(
        "SOURCES",
        json.dumps(
            {
                "arxiv": {
                    "enabled": True,
                    "queries": ["cat:cs.AI"],
                    "enrich_method": "html_document",
                    "enrich_failure_mode": "fallback",
                }
            }
        ),
    )

    import httpx
    import recoleta.pipeline as pipeline_module

    arxiv_id = "2345.6791v1"

    def fail_fetch_url_html(_client: httpx.Client, url: str) -> str:
        request = httpx.Request("GET", url)
        response = httpx.Response(404, request=request, text="not found")
        raise httpx.HTTPStatusError("not found", request=request, response=response)

    monkeypatch.setattr(pipeline_module, "fetch_url_html", fail_fetch_url_html)
    monkeypatch.setattr(
        pipeline_module, "fetch_url_bytes", lambda *_args, **_kwargs: b"%PDF-1.7"
    )
    monkeypatch.setattr(
        pipeline_module,
        "extract_pdf_text",
        lambda *_args, **_kwargs: "pdf recovered",
    )

    _, repository, service = _build_service(configured_env)
    draft = ItemDraft.from_values(
        source="arxiv",
        source_item_id=arxiv_id,
        canonical_url=f"https://arxiv.org/abs/{arxiv_id}",
        title="Pandoc HTML Fallback Metric",
    )
    service.ingest(run_id="run-html-md-pdf-fallback", drafts=[draft])
    service.enrich(run_id="run-html-md-pdf-fallback", limit=10)

    metrics = repository.list_metrics(run_id="run-html-md-pdf-fallback")
    by_name = {metric.name: metric for metric in metrics}
    assert by_name["pipeline.enrich.failed_total"].value == 0
    assert (
        by_name["pipeline.enrich.arxiv.html_document.fallback_to_pdf_total"].value == 1
    )
    assert (
        by_name[
            "pipeline.enrich.arxiv.html_document.fallback_to_pdf_reason.http_404_total"
        ].value
        == 1
    )

    with Session(repository.engine) as session:
        item = session.exec(select(Item).where(Item.source_item_id == arxiv_id)).first()
        assert item is not None
        assert item.id is not None
        pdf = repository.get_latest_content(
            item_id=int(item.id), content_type="pdf_text"
        )
        assert pdf is not None
        assert pdf.text == "pdf recovered"
