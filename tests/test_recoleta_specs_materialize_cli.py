from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest
from sqlmodel import Session, select
from typer.testing import CliRunner

import recoleta.cli
import recoleta.materialize as materialize_module
from recoleta.materialize import MaterializeScopeSpec, materialize_outputs
from recoleta.models import DocumentChunk, Item
from recoleta.publish.item_notes import resolve_item_note_path
from recoleta.storage import Repository
from recoleta.trends import TrendPayload, persist_trend_payload
from recoleta.types import AnalysisResult, ItemDraft


def _seed_materialize_fixture(
    *,
    repository: Repository,
) -> tuple[int, Path]:
    published_at = datetime(2026, 3, 2, 12, tzinfo=UTC)
    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="robometer-1",
        canonical_url="https://example.com/robometer",
        title="Robometer: Scaling General-Purpose Robotic Reward Models",
        authors=["Alice"],
        published_at=published_at,
    )
    item, _ = repository.upsert_item(draft)
    assert item.id is not None
    repository.save_analysis(
        item_id=item.id,
        result=AnalysisResult(
            model="test/materialize",
            provider="test",
            summary="## Summary\n\nReward models get a stronger comparison signal.\n",
            topics=["agents", "robotics"],
            relevance_score=0.95,
            novelty_score=0.44,
            cost_usd=0.0,
            latency_ms=1,
        ),
    )
    repository.mark_item_published(item_id=item.id)
    persisted_item = repository.get_item(item_id=item.id)
    assert persisted_item is not None
    item_doc = repository.upsert_document_for_item(item=persisted_item)
    assert item_doc.id is not None

    payload = TrendPayload(
        title="Agent Systems",
        granularity="day",
        period_start=datetime(2026, 3, 2, tzinfo=UTC).isoformat(),
        period_end=datetime(2026, 3, 3, tzinfo=UTC).isoformat(),
        overview_md=(
            "## Overview\n\n"
            "Start with "
            "[Robometer](https://example.com/robometer).\n"
        ),
        topics=["agents", "robotics"],
        clusters=[
            {
                "name": "Reward models",
                "description": (
                    "Follow "
                    "[Robometer](https://example.com/robometer)."
                ),
                "representative_chunks": [
                    {
                        "doc_id": item_doc.id,
                        "chunk_index": 0,
                    }
                ],
            }
        ],
        highlights=[],
    )
    trend_doc_id = persist_trend_payload(
        repository=repository,
        granularity="day",
        period_start=datetime(2026, 3, 2, tzinfo=UTC),
        period_end=datetime(2026, 3, 3, tzinfo=UTC),
        payload=payload,
    )

    output_dir = Path("/tmp/placeholder")
    item_note_path = resolve_item_note_path(
        note_dir=output_dir / "Inbox",
        item_id=item.id,
        title=persisted_item.title,
        canonical_url=persisted_item.canonical_url,
        published_at=persisted_item.published_at,
    )
    return trend_doc_id, item_note_path


def test_materialize_outputs_backfills_item_notes_rerenders_trend_links_and_keeps_db_unchanged(
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    trend_doc_id, placeholder_item_note_path = _seed_materialize_fixture(
        repository=repository
    )
    output_dir = tmp_path / "outputs"

    with Session(repository.engine) as session:
        item_before = session.exec(select(Item)).one()
        meta_before = session.exec(
            select(DocumentChunk).where(
                DocumentChunk.doc_id == trend_doc_id,
                DocumentChunk.chunk_index == 1,
            )
        ).one()
        item_state_before = item_before.state
        meta_text_before = meta_before.text

    result = materialize_outputs(
        repository=repository,
        scope_specs=[
            MaterializeScopeSpec(scope="default", output_dir=output_dir),
        ],
        site_input_dir=output_dir,
        site_output_dir=output_dir / "site",
    )

    item_note_path = output_dir / "Inbox" / placeholder_item_note_path.name
    trend_note_path = output_dir / "Trends" / f"day--2026-03-02--trend--{trend_doc_id}.md"
    assert result.site_manifest_path == output_dir / "site" / "manifest.json"
    assert item_note_path.exists()
    assert trend_note_path.exists()

    trend_markdown = trend_note_path.read_text(encoding="utf-8")
    assert (
        "## Overview\nStart with "
        f"[Robometer](../Inbox/{item_note_path.name})."
    ) in trend_markdown
    assert f"[Robometer](../Inbox/{item_note_path.name})" in trend_markdown
    assert "https://example.com/robometer" not in trend_markdown
    assert "#### Representative sources" in trend_markdown
    assert "Robometer: Scaling General-Purpose Robotic Reward Models" in trend_markdown
    assert f"(../Inbox/{item_note_path.name})" in trend_markdown

    trend_html = (
        output_dir
        / "site"
        / "trends"
        / f"day--2026-03-02--trend--{trend_doc_id}.html"
    ).read_text(encoding="utf-8")
    assert f"../items/{item_note_path.stem}.html" in trend_html
    assert "https://example.com/robometer" not in trend_html

    item_html = (
        output_dir / "site" / "items" / f"{item_note_path.stem}.html"
    ).read_text(encoding="utf-8")
    assert "Open original" in item_html
    assert "https://example.com/robometer" in item_html

    with Session(repository.engine) as session:
        item_after = session.exec(select(Item)).one()
        meta_after = session.exec(
            select(DocumentChunk).where(
                DocumentChunk.doc_id == trend_doc_id,
                DocumentChunk.chunk_index == 1,
            )
        ).one()
        assert item_after.state == item_state_before
        assert meta_after.text == meta_text_before
        assert "https://example.com/robometer" in meta_after.text
        assert "../Inbox/" not in meta_after.text


def test_materialize_outputs_cli_can_regenerate_pdfs_with_explicit_paths(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    trend_doc_id, _ = _seed_materialize_fixture(repository=repository)
    output_dir = tmp_path / "outputs"
    pdf_calls: list[Path] = []

    class _FakePrepared:
        renderer = "story"

    class _FakePdfResult:
        def __init__(self, path: Path) -> None:
            self.path = path
            self.prepared = _FakePrepared()

    def _fake_render_trend_note_pdf_result(*, markdown_path, **_: object):  # type: ignore[no-untyped-def]
        pdf_calls.append(markdown_path)
        pdf_path = markdown_path.with_suffix(".pdf")
        pdf_path.write_bytes(b"%PDF-1.7\n")
        return _FakePdfResult(pdf_path)

    monkeypatch.setattr(
        materialize_module,
        "render_trend_note_pdf_result",
        _fake_render_trend_note_pdf_result,
    )

    result = runner.invoke(
        recoleta.cli.app,
        [
            "materialize",
            "outputs",
            "--db-path",
            str(repository.db_path),
            "--output-dir",
            str(output_dir),
            "--pdf",
        ],
    )

    assert result.exit_code == 0
    assert "materialize outputs completed" in result.stdout
    assert len(pdf_calls) == 1
    assert pdf_calls[0].name == f"day--2026-03-02--trend--{trend_doc_id}.md"
    assert (output_dir / "Trends" / f"day--2026-03-02--trend--{trend_doc_id}.pdf").exists()
