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
