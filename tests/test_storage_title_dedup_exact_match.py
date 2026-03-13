from __future__ import annotations

from pathlib import Path

import pytest

import recoleta.storage.items as item_store
from recoleta.storage import Repository
from recoleta.types import ItemDraft


def test_upsert_item_skips_fuzzy_scoring_for_exact_title_match(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Regression: exact title matches should short-circuit before fuzzy scoring."""

    repository = Repository(
        db_path=tmp_path / "recoleta.db",
        title_dedup_threshold=92.0,
        title_dedup_max_candidates=10,
    )
    repository.init_schema()

    exact_item, _ = repository.upsert_item(
        ItemDraft.from_values(
            source="rss",
            source_item_id=None,
            canonical_url="https://example.com/exact-title",
            title="Exact Duplicate Title",
            authors=["Alice"],
        )
    )
    assert exact_item.id is not None

    neighbor_item, _ = repository.upsert_item(
        ItemDraft.from_values(
            source="rss",
            source_item_id="neighbor-0",
            canonical_url="https://example.com/neighbor-0",
            title="Quantum Error Bars for Bioacoustics",
            authors=["Alice"],
        )
    )
    assert neighbor_item.id is not None

    def _raise_if_fuzzy_called(*_args, **_kwargs):  # type: ignore[no-untyped-def]
        raise AssertionError("fuzzy scorer should not run for exact title matches")

    monkeypatch.setattr(item_store.fuzz, "token_set_ratio", _raise_if_fuzzy_called)

    matched_item, created = repository.upsert_item(
        ItemDraft.from_values(
            source="hn",
            source_item_id="hn-exact-title",
            canonical_url="https://news.ycombinator.com/item?id=1",
            title="Exact Duplicate Title",
            authors=["Bob"],
        )
    )

    assert created is False
    assert matched_item.id == exact_item.id
    assert repository.count_items() == 2


def test_upsert_item_exact_title_match_respects_threshold_above_100(
    tmp_path: Path,
) -> None:
    """Regression: exact-title shortcut must still honor disabled title dedup."""

    repository = Repository(
        db_path=tmp_path / "recoleta.db",
        title_dedup_threshold=101.0,
        title_dedup_max_candidates=10,
    )
    repository.init_schema()

    first_item, _ = repository.upsert_item(
        ItemDraft.from_values(
            source="rss",
            source_item_id="exact-threshold-a",
            canonical_url="https://example.com/exact-threshold-a",
            title="Exact Duplicate Title",
            authors=["Alice"],
        )
    )
    assert first_item.id is not None

    second_item, created = repository.upsert_item(
        ItemDraft.from_values(
            source="hn",
            source_item_id="exact-threshold-b",
            canonical_url="https://example.com/exact-threshold-b",
            title="Exact Duplicate Title",
            authors=["Bob"],
        )
    )

    assert created is True
    assert second_item.id != first_item.id
    assert repository.count_items() == 2
