from __future__ import annotations

from pathlib import Path

from recoleta.storage import Repository
from recoleta.types import ItemDraft


def test_upsert_content_with_inserted_reports_inserted(tmp_path: Path) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()

    draft = ItemDraft.from_values(
        source="arxiv",
        source_item_id="0000.0000v1",
        canonical_url="https://arxiv.org/abs/0000.0000",
        title="Test Paper",
    )
    item, _ = repository.upsert_item(draft)
    assert item.id is not None

    first, inserted_first = repository.upsert_content_with_inserted(
        item_id=int(item.id),
        content_type="html_document",
        text="<main><p>hello</p></main>",
    )
    assert inserted_first is True
    assert first.id is not None

    second, inserted_second = repository.upsert_content_with_inserted(
        item_id=int(item.id),
        content_type="html_document",
        text="<main><p>hello</p></main>",
    )
    assert inserted_second is False
    assert second.id == first.id
