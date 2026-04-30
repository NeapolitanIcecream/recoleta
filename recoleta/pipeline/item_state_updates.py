from __future__ import annotations

from typing import Any, cast

from recoleta.models import (
    ITEM_STATE_ENRICHED,
    ITEM_STATE_FAILED,
    ITEM_STATE_RETRYABLE_FAILED,
    ITEM_STATE_TRIAGED,
)
from recoleta.types import ItemStateUpdate


def normalize_item_state_updates(
    *, updates: list[ItemStateUpdate]
) -> list[ItemStateUpdate]:
    return [
        ItemStateUpdate(
            item_id=int(update.item_id),
            state=str(update.state or "").strip(),
            mirror_item_state=bool(update.mirror_item_state),
        )
        for update in updates
        if int(getattr(update, "item_id", 0) or 0) > 0
        and str(getattr(update, "state", "") or "").strip()
    ]


def update_item_states(
    *,
    repository: Any,
    updates: list[ItemStateUpdate],
) -> int:
    normalized = normalize_item_state_updates(updates=updates)
    if not normalized:
        return 0
    batch_updater = getattr(repository, "update_item_states_batch", None)
    if callable(batch_updater):
        try:
            return cast(int, batch_updater(updates=normalized))
        except TypeError:
            pass
    for update in normalized:
        _mark_item_state(repository=repository, update=update)
    return len(normalized)


def _mark_item_state(*, repository: Any, update: ItemStateUpdate) -> None:
    if update.state == ITEM_STATE_RETRYABLE_FAILED:
        repository.mark_item_retryable_failed(item_id=update.item_id)
    elif update.state == ITEM_STATE_FAILED:
        repository.mark_item_failed(item_id=update.item_id)
    elif update.state == ITEM_STATE_TRIAGED:
        repository.mark_item_triaged(item_id=update.item_id)
    elif update.state == ITEM_STATE_ENRICHED:
        repository.mark_item_enriched(item_id=update.item_id)
    else:
        repository.mark_item_failed(item_id=update.item_id)
