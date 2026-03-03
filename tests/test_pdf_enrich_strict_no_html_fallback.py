from __future__ import annotations

import json
from pathlib import Path

import httpx
import pytest
from loguru import logger

import recoleta.extract as extract
from recoleta.config import Settings
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


def _build_blank_pdf_bytes() -> bytes:
    try:
        import pymupdf  # type: ignore[import-not-found]
    except Exception:  # pragma: no cover
        import fitz as pymupdf  # type: ignore[import-not-found]

    doc = pymupdf.open()
    try:
        doc.new_page()
        return doc.tobytes()
    finally:
        doc.close()


def test_pdf_enrich_is_strict_and_does_not_fallback_to_html(
    configured_env: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Spec: PDF enrich is strict and never falls back to HTML."""

    monkeypatch.setenv(
        "SOURCES",
        json.dumps(
            {
                "arxiv": {
                    "enabled": True,
                    "queries": ["cat:cs.AI"],
                    "enrich_method": "pdf_text",
                    "enrich_failure_mode": "fallback",
                }
            }
        ),
    )

    _settings, repository, service = _build_service(configured_env)
    draft = ItemDraft.from_values(
        source="arxiv",
        source_item_id="1111.2222v1",
        canonical_url="https://arxiv.org/abs/1111.2222v1",
        title="PDF strict enrich",
    )
    item, _ = repository.upsert_item(draft)
    assert item.id is not None

    blank_pdf = _build_blank_pdf_bytes()

    monkeypatch.setattr(extract, "extract_pdf_text", lambda *_a, **_k: None)

    import recoleta.pipeline as pipeline

    monkeypatch.setattr(pipeline, "fetch_url_bytes", lambda _client, _url: blank_pdf)  # noqa: ARG005
    monkeypatch.setattr(
        pipeline,
        "fetch_url_html",
        lambda *_a, **_k: (_ for _ in ()).throw(  # noqa: ARG005
            AssertionError("HTML fallback must not be used for pdf_text enrich")
        ),
    )

    with pytest.raises(RuntimeError, match="empty pdf text extraction"):
        with httpx.Client() as client:
            _text, _stored = service._ensure_pdf_content(  # noqa: SLF001
                client=client,
                source="arxiv",
                item_id=int(item.id),
                canonical_url=str(draft.canonical_url),
                source_item_id=str(draft.source_item_id),
                log=logger.bind(module="pipeline.enrich", run_id="run-pdf-strict"),
            )

    assert (
        repository.get_latest_content(
            item_id=int(item.id), content_type="html_maintext"
        )
        is None
    )
