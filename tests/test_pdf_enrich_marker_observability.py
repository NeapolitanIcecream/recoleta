from __future__ import annotations

import json
from pathlib import Path
from typing import Any

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


def test_pdf_enrich_logs_marker_backend_choice(
    configured_env: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Spec: when PDF extraction uses marker, emit a structured INFO log."""

    monkeypatch.setenv(
        "SOURCES",
        json.dumps(
            {
                "arxiv": {
                    "enabled": True,
                    "queries": ["cat:cs.AI"],
                    "enrich_method": "pdf_text",
                    "enrich_failure_mode": "strict",
                }
            }
        ),
    )

    _settings, repository, service = _build_service(configured_env)
    draft = ItemDraft.from_values(
        source="arxiv",
        source_item_id="1111.2222v1",
        canonical_url="https://arxiv.org/abs/1111.2222v1",
        title="PDF Marker Observability",
    )
    item, _ = repository.upsert_item(draft)
    assert item.id is not None

    blank_pdf = _build_blank_pdf_bytes()

    # Force pymupdf4llm path to yield nothing so marker is chosen deterministically.
    monkeypatch.setattr(
        extract, "_extract_pdf_text_with_pymupdf4llm", lambda _doc: None
    )  # noqa: ARG005

    class FakeRendered:
        markdown = "marker markdown"

    class FakeMarkerConverter:
        def __call__(self, _path: str) -> Any:
            return FakeRendered()

    monkeypatch.setattr(
        extract, "_get_marker_pdf_converter", lambda: FakeMarkerConverter()
    )

    import recoleta.pipeline as pipeline

    monkeypatch.setattr(pipeline, "fetch_url_bytes", lambda _client, _url: blank_pdf)  # noqa: ARG005

    records: list[dict[str, Any]] = []

    def _sink(message):  # type: ignore[no-untyped-def]
        records.append(message.record)

    sink_id = logger.add(_sink, level="INFO")
    try:
        with httpx.Client() as client:
            text, stored = service._ensure_pdf_content_with_optional_html_fallback(  # noqa: SLF001
                client=client,
                source="arxiv",
                item_id=int(item.id),
                canonical_url=str(draft.canonical_url),
                source_item_id=str(draft.source_item_id),
                allow_html_fallback=False,
                log=logger.bind(module="pipeline.enrich", run_id="run-marker-log"),
            )
        assert stored is True
        assert text == "marker markdown"
    finally:
        logger.remove(sink_id)

    assert any(
        r.get("message") == "PDF extracted via marker"
        and r.get("extra", {}).get("pdf_backend") == "marker"
        for r in records
    ), records
