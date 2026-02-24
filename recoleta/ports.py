from __future__ import annotations

from datetime import datetime
from typing import Protocol

from recoleta.models import Analysis, Delivery, Item
from recoleta.types import AnalysisResult, ItemDraft


class RepositoryPort(Protocol):
    def record_metric(self, *, run_id: str, name: str, value: float, unit: str | None = None) -> None: ...

    def upsert_item(self, draft: ItemDraft) -> tuple[Item, bool]: ...

    def list_items_for_analysis(self, *, limit: int) -> list[Item]: ...

    def save_analysis(self, *, item_id: int, result: AnalysisResult) -> Analysis: ...

    def mark_item_failed(self, *, item_id: int) -> None: ...

    def list_items_for_publish(self, *, limit: int, min_relevance_score: float) -> list[tuple[Item, Analysis]]: ...

    def has_sent_delivery(self, *, item_id: int, channel: str, destination: str) -> bool: ...

    def count_sent_deliveries_since(self, *, channel: str, destination: str, since: datetime) -> int: ...

    def upsert_delivery(
        self,
        *,
        item_id: int,
        channel: str,
        destination: str,
        message_id: str | None,
        status: str,
        error: str | None = None,
    ) -> Delivery: ...

    def mark_item_published(self, *, item_id: int) -> None: ...

    def add_artifact(self, *, run_id: str, item_id: int | None, kind: str, path: str) -> None: ...

    @staticmethod
    def decode_list(value: str | None) -> list[str]: ...

