from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from sqlmodel import Session, select
from typer.testing import CliRunner

import recoleta.cli
from recoleta.models import Document, DocumentChunk, Item
from recoleta.storage import Repository
from recoleta.types import ItemDraft


def _seed_item_and_trend_docs(*, repository: Repository) -> None:
    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="db-reset-trends-only-1",
        canonical_url="https://example.com/db-reset-trends-only-1",
        title="T",
        authors=["Alice"],
        raw_metadata={"source": "test"},
        published_at=datetime(2026, 3, 2, tzinfo=UTC),
    )
    item, _ = repository.upsert_item(draft)
    assert item.id is not None

    item_doc = repository.upsert_document_for_item(item=item)
    assert item_doc.id is not None
    repository.upsert_document_chunk(
        doc_id=int(item_doc.id),
        chunk_index=0,
        kind="summary",
        text_value="item summary",
        start_char=0,
        end_char=None,
        source_content_type="analysis_summary",
    )

    period_start = datetime(2026, 3, 2, tzinfo=UTC)
    period_end = datetime(2026, 3, 3, tzinfo=UTC)
    trend_doc = repository.upsert_document_for_trend(
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        title="Daily Trend",
    )
    assert trend_doc.id is not None
    repository.upsert_document_chunk(
        doc_id=int(trend_doc.id),
        chunk_index=0,
        kind="summary",
        text_value="trend overview",
        start_char=0,
        end_char=None,
        source_content_type="trend_overview",
    )


def test_db_reset_trends_only_requires_yes(tmp_path: Path) -> None:
    runner = CliRunner()
    db_path = tmp_path / "recoleta.db"
    repository = Repository(db_path=db_path)
    repository.init_schema()
    _seed_item_and_trend_docs(repository=repository)

    result = runner.invoke(
        recoleta.cli.app,
        ["db", "reset", "--db-path", str(db_path), "--trends-only"],
    )
    assert result.exit_code == 2
    assert "refusing to reset trends without --yes" in result.stdout

    with Session(repository.engine) as session:
        assert list(session.exec(select(Item)))
        assert list(session.exec(select(Document)))
        assert list(session.exec(select(DocumentChunk)))


def test_db_reset_trends_only_deletes_trend_documents_but_keeps_items(
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    db_path = tmp_path / "recoleta.db"
    repository = Repository(db_path=db_path)
    repository.init_schema()
    _seed_item_and_trend_docs(repository=repository)

    result = runner.invoke(
        recoleta.cli.app,
        ["db", "reset", "--db-path", str(db_path), "--trends-only", "--yes"],
    )
    assert result.exit_code == 0
    assert db_path.exists()

    with Session(repository.engine) as session:
        # Items remain.
        assert list(session.exec(select(Item)))

        # Trend-related document index cleared.
        docs = list(session.exec(select(Document)))
        assert not docs
        chunks = list(session.exec(select(DocumentChunk)))
        assert not chunks
