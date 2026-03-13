from __future__ import annotations

from pathlib import Path

from recoleta.storage import Repository
from recoleta.types import ItemDraft


def test_get_latest_content_texts_for_items_uses_single_query(tmp_path: Path) -> None:
    """Regression: batched latest-content lookup should avoid one query per content type."""

    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()

    first_item, _ = repository.upsert_item(
        ItemDraft.from_values(
            source="rss",
            source_item_id="batch-texts-1",
            canonical_url="https://example.com/batch-texts-1",
            title="Batch Texts One",
        )
    )
    second_item, _ = repository.upsert_item(
        ItemDraft.from_values(
            source="rss",
            source_item_id="batch-texts-2",
            canonical_url="https://example.com/batch-texts-2",
            title="Batch Texts Two",
        )
    )
    assert first_item.id is not None
    assert second_item.id is not None

    first_item_id = int(first_item.id)
    second_item_id = int(second_item.id)

    _ = repository.upsert_content(
        item_id=first_item_id,
        content_type="pdf_text",
        text="older pdf body",
    )
    _ = repository.upsert_content(
        item_id=first_item_id,
        content_type="pdf_text",
        text="latest pdf body",
    )
    _ = repository.upsert_content(
        item_id=first_item_id,
        content_type="html_maintext",
        text="latest html body",
    )
    _ = repository.upsert_content(
        item_id=second_item_id,
        content_type="html_document_md",
        text="latest markdown body",
    )

    with repository.sql_diagnostics() as sql_diag:
        texts_by_item = repository.get_latest_content_texts_for_items(
            item_ids=[first_item_id, second_item_id],
            content_types=["pdf_text", "html_maintext", "html_document_md"],
        )

    assert texts_by_item == {
        first_item_id: {
            "pdf_text": "latest pdf body",
            "html_maintext": "latest html body",
            "html_document_md": None,
        },
        second_item_id: {
            "pdf_text": None,
            "html_maintext": None,
            "html_document_md": "latest markdown body",
        },
    }
    assert sql_diag.queries_total == 1
