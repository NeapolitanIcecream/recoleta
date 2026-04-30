from __future__ import annotations

from typing import Any, cast

from recoleta.models import (
    ITEM_STATE_ENRICHED,
    ITEM_STATE_FAILED,
    ITEM_STATE_RETRYABLE_FAILED,
    ITEM_STATE_TRIAGED,
)
from recoleta.pipeline.item_state_updates import update_item_states
from recoleta.types import ItemStateUpdate


class _BatchRepository:
    def __init__(self) -> None:
        self.batch_updates: list[ItemStateUpdate] = []

    def update_item_states_batch(self, *, updates: list[ItemStateUpdate]) -> int:
        self.batch_updates = list(updates)
        return len(updates)

    def mark_item_failed(self, *, item_id: int) -> None:  # pragma: no cover
        raise AssertionError(f"unexpected fallback for {item_id}")


class _FallbackRepository:
    def __init__(self) -> None:
        self.calls: list[tuple[str, int]] = []

    def mark_item_retryable_failed(self, *, item_id: int) -> None:
        self.calls.append(("retryable_failed", item_id))

    def mark_item_failed(self, *, item_id: int) -> None:
        self.calls.append(("failed", item_id))

    def mark_item_triaged(self, *, item_id: int) -> None:
        self.calls.append(("triaged", item_id))

    def mark_item_enriched(self, *, item_id: int) -> None:
        self.calls.append(("enriched", item_id))


class _TypeErrorBatchRepository(_FallbackRepository):
    def update_item_states_batch(self, *, updates: list[ItemStateUpdate]) -> int:
        _ = updates
        raise TypeError("legacy repository signature")


def test_update_item_states_prefers_batch_repository_with_normalized_updates() -> None:
    repository = _BatchRepository()

    updated = update_item_states(
        repository=repository,
        updates=[
            ItemStateUpdate(item_id=1, state=f" {ITEM_STATE_FAILED} "),
            ItemStateUpdate(item_id=0, state=ITEM_STATE_FAILED),
            ItemStateUpdate(item_id=2, state=""),
            ItemStateUpdate(
                item_id=3,
                state=ITEM_STATE_TRIAGED,
                mirror_item_state=True,
            ),
        ],
    )

    assert updated == 2
    assert repository.batch_updates == [
        ItemStateUpdate(
            item_id=1,
            state=ITEM_STATE_FAILED,
            mirror_item_state=False,
        ),
        ItemStateUpdate(
            item_id=3,
            state=ITEM_STATE_TRIAGED,
            mirror_item_state=True,
        ),
    ]


def test_update_item_states_falls_back_to_status_specific_repository_methods() -> None:
    repository = _TypeErrorBatchRepository()

    updated = update_item_states(
        repository=repository,
        updates=[
            ItemStateUpdate(item_id=1, state=ITEM_STATE_RETRYABLE_FAILED),
            ItemStateUpdate(item_id=2, state=ITEM_STATE_FAILED),
            ItemStateUpdate(item_id=3, state=ITEM_STATE_TRIAGED),
            ItemStateUpdate(item_id=4, state=ITEM_STATE_ENRICHED),
            ItemStateUpdate(item_id=5, state="unknown"),
        ],
    )

    assert updated == 5
    assert repository.calls == [
        ("retryable_failed", 1),
        ("failed", 2),
        ("triaged", 3),
        ("enriched", 4),
        ("failed", 5),
    ]


def test_update_item_states_returns_zero_without_valid_updates() -> None:
    repository = _BatchRepository()

    updated = update_item_states(
        repository=repository,
        updates=[
            ItemStateUpdate(item_id=0, state=ITEM_STATE_FAILED),
            ItemStateUpdate(item_id=1, state=cast(Any, None)),
        ],
    )

    assert updated == 0
    assert repository.batch_updates == []
