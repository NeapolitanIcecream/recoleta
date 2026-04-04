from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from recoleta.storage import Repository
from recoleta.types import ItemDraft


def _seed_summary_chunk(*, repository: Repository) -> tuple[int, str]:
    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="storage-embedding-1",
        canonical_url="https://example.com/storage-embedding-1",
        title="Storage Embedding Item",
        authors=["Alice"],
        published_at=datetime(2026, 3, 2, tzinfo=UTC),
    )
    item, _ = repository.upsert_item(draft)
    assert item.id is not None
    document = repository.upsert_document_for_item(item=item)
    assert document.id is not None
    chunk, _ = repository.upsert_document_chunk(
        doc_id=int(document.id),
        chunk_index=0,
        kind="summary",
        text_value="Embedding summary chunk.",
        source_content_type="analysis_summary",
    )
    assert chunk.id is not None
    return int(chunk.id), str(chunk.text_hash)


def test_upsert_chunk_embedding_skips_commit_when_payload_is_unchanged(
    tmp_path: Path,
) -> None:
    """Regression: idempotent embedding writes must not add extra SQL commits."""

    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    chunk_id, text_hash = _seed_summary_chunk(repository=repository)

    created = repository.upsert_chunk_embedding(
        chunk_id=chunk_id,
        model="text-embedding-3-small",
        dimensions=3,
        text_hash=text_hash,
        vector=[0.1, 0.2, 0.3],
    )
    assert created.id is not None

    with repository.sql_diagnostics() as sql_diag:
        repeated = repository.upsert_chunk_embedding(
            chunk_id=chunk_id,
            model="text-embedding-3-small",
            dimensions=3,
            text_hash=text_hash,
            vector=[0.1, 0.2, 0.3],
        )

    assert repeated.id == created.id
    assert sql_diag.commits_total == 0
