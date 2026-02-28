from __future__ import annotations

from datetime import datetime
from typing import Any, Protocol

from recoleta.models import Analysis, Content, Delivery, Item
from recoleta.types import AnalysisResult, ItemDraft


class RepositoryPort(Protocol):
    engine: Any

    def sql_diagnostics(self) -> Any: ...

    def record_metric(self, *, run_id: str, name: str, value: float, unit: str | None = None) -> None: ...

    def upsert_item(self, draft: ItemDraft) -> tuple[Item, bool]: ...

    def list_items_for_analysis(self, *, limit: int) -> list[Item]: ...

    def list_items_for_llm_analysis(self, *, limit: int, triage_required: bool) -> list[Item]: ...

    def get_latest_content(self, *, item_id: int, content_type: str) -> Content | None: ...

    def get_latest_content_texts(self, *, item_id: int, content_types: list[str]) -> dict[str, str | None]: ...

    def get_latest_contents(self, *, item_ids: list[int], content_type: str) -> dict[int, Content]: ...

    def upsert_contents_texts(self, *, item_id: int, texts_by_type: dict[str, str]) -> int: ...

    def upsert_content(
        self,
        *,
        item_id: int,
        content_type: str,
        text: str | None,
        artifact_path: str | None = None,
    ) -> Content: ...

    def upsert_content_with_inserted(
        self,
        *,
        item_id: int,
        content_type: str,
        text: str | None,
        artifact_path: str | None = None,
    ) -> tuple[Content, bool]: ...

    def save_analysis(self, *, item_id: int, result: AnalysisResult) -> Analysis: ...

    def mark_item_enriched(self, *, item_id: int) -> None: ...

    def mark_item_triaged(self, *, item_id: int) -> None: ...

    def mark_item_failed(self, *, item_id: int) -> None: ...

    def mark_item_retryable_failed(self, *, item_id: int) -> None: ...

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

