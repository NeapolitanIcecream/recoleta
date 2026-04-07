from __future__ import annotations

from datetime import datetime
from typing import Any, Protocol

from recoleta.models import (
    Analysis,
    Content,
    Delivery,
    Document,
    DocumentChunk,
    Item,
    PassOutput,
    TrendDelivery,
)
from recoleta.types import (
    AnalysisResult,
    AnalysisWrite,
    ItemDraft,
    ItemStateUpdate,
    MetricPoint,
)


class RepositoryPort(Protocol):
    engine: Any

    def sql_diagnostics(self) -> Any: ...

    def record_metric(
        self, *, run_id: str, name: str, value: float, unit: str | None = None
    ) -> None: ...

    def record_metrics_batch(
        self, *, run_id: str, metrics: list[MetricPoint]
    ) -> int: ...

    def upsert_item(self, draft: ItemDraft) -> tuple[Item, bool]: ...

    def list_items_for_analysis(
        self,
        *,
        limit: int,
        period_start: datetime | None = None,
        period_end: datetime | None = None,
    ) -> list[Item]: ...

    def list_items_for_llm_analysis(
        self,
        *,
        limit: int,
        triage_required: bool,
        period_start: datetime | None = None,
        period_end: datetime | None = None,
    ) -> list[Item]: ...

    def get_latest_content(
        self, *, item_id: int, content_type: str
    ) -> Content | None: ...

    def get_latest_content_texts(
        self, *, item_id: int, content_types: list[str]
    ) -> dict[str, str | None]: ...

    def get_latest_content_texts_for_items(
        self, *, item_ids: list[int], content_types: list[str]
    ) -> dict[int, dict[str, str | None]]: ...

    def get_latest_contents(
        self, *, item_ids: list[int], content_type: str
    ) -> dict[int, Content]: ...

    def upsert_contents_texts(
        self, *, item_id: int, texts_by_type: dict[str, str]
    ) -> int: ...

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

    def save_analysis(
        self,
        *,
        item_id: int,
        result: AnalysisResult,
        mirror_item_state: bool = True,
    ) -> Analysis: ...

    def save_analyses_batch(self, *, analyses: list[AnalysisWrite]) -> int: ...

    def mark_item_enriched(self, *, item_id: int) -> None: ...

    def mark_item_triaged(self, *, item_id: int) -> None: ...

    def mark_item_failed(self, *, item_id: int) -> None: ...

    def mark_item_retryable_failed(self, *, item_id: int) -> None: ...

    def update_item_states_batch(self, *, updates: list[ItemStateUpdate]) -> int: ...

    def list_items_for_publish(
        self,
        *,
        limit: int,
        min_relevance_score: float,
        period_start: datetime | None = None,
        period_end: datetime | None = None,
    ) -> list[tuple[Item, Analysis]]: ...

    def has_sent_delivery(
        self, *, item_id: int, channel: str, destination: str
    ) -> bool: ...

    def count_sent_deliveries_since(
        self, *, channel: str, destination: str, since: datetime
    ) -> int: ...

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

    def has_sent_trend_delivery(
        self, *, doc_id: int, channel: str, destination: str, content_hash: str
    ) -> bool: ...

    def upsert_trend_delivery(
        self,
        *,
        doc_id: int,
        channel: str,
        destination: str,
        content_hash: str,
        message_id: str | None,
        status: str,
        error: str | None = None,
    ) -> TrendDelivery: ...

    def mark_item_published(self, *, item_id: int) -> None: ...

    def add_artifact(
        self,
        *,
        run_id: str,
        item_id: int | None,
        kind: str,
        path: str,
        details: dict[str, Any] | None = None,
    ) -> None: ...

    def update_run_context(
        self,
        *,
        run_id: str,
        command: str | None = None,
        scope: str | None = None,
        granularity: str | None = None,
        period_start: datetime | None = None,
        period_end: datetime | None = None,
    ) -> None: ...

    def create_pass_output(
        self,
        *,
        run_id: str,
        pass_kind: str,
        status: str,
        granularity: str | None = None,
        period_start: datetime | None = None,
        period_end: datetime | None = None,
        schema_version: int = 1,
        payload: dict[str, Any] | list[Any] | None = None,
        diagnostics: dict[str, Any] | list[Any] | None = None,
        input_refs: list[dict[str, Any]] | None = None,
        content_hash: str | None = None,
    ) -> PassOutput: ...

    def get_pass_output(self, *, pass_output_id: int) -> PassOutput | None: ...

    def get_latest_pass_output(
        self,
        *,
        pass_kind: str,
        status: str | None = None,
        granularity: str | None = None,
        period_start: datetime | None = None,
        period_end: datetime | None = None,
    ) -> PassOutput | None: ...

    @staticmethod
    def decode_list(value: str | None) -> list[str]: ...

    def list_analyzed_items_in_period(
        self,
        *,
        period_start: datetime,
        period_end: datetime,
        limit: int,
        offset: int = 0,
    ) -> list[tuple[Item, Analysis]]: ...

    def upsert_document_for_item(self, *, item: Item) -> Document: ...

    def upsert_document_for_trend(
        self,
        *,
        granularity: str,
        period_start: datetime,
        period_end: datetime,
        title: str,
    ) -> Document: ...

    def upsert_document_for_idea(
        self,
        *,
        granularity: str,
        period_start: datetime,
        period_end: datetime,
        title: str,
    ) -> Document: ...

    def upsert_document_chunk(
        self,
        *,
        doc_id: int,
        chunk_index: int,
        kind: str,
        text_value: str,
        start_char: int | None = None,
        end_char: int | None = None,
        source_content_type: str | None = None,
    ) -> tuple[DocumentChunk, bool]: ...

    def delete_document_chunks(
        self,
        *,
        doc_id: int,
        kind: str | None = None,
        chunk_index_gte: int | None = None,
    ) -> int: ...

    def list_documents(
        self,
        *,
        doc_type: str,
        period_start: datetime,
        period_end: datetime,
        granularity: str | None = None,
        order_by: str = "event_desc",
        offset: int = 0,
        limit: int = 50,
    ) -> list[Document]: ...

    def get_document(self, *, doc_id: int) -> Document | None: ...

    def get_item(self, *, item_id: int) -> Item | None: ...

    def read_document_chunk(
        self, *, doc_id: int, chunk_index: int
    ) -> DocumentChunk | None: ...

    def search_chunks_text(
        self,
        *,
        query: str,
        doc_type: str,
        granularity: str | None = None,
        period_start: datetime,
        period_end: datetime,
        limit: int = 10,
    ) -> list[dict[str, Any]]: ...

    def list_summary_chunks_in_period(
        self,
        *,
        doc_type: str,
        period_start: datetime,
        period_end: datetime,
        limit: int = 500,
        offset: int = 0,
    ) -> list[DocumentChunk]: ...

    def list_document_chunks_in_period(
        self,
        *,
        doc_type: str,
        kind: str,
        period_start: datetime,
        period_end: datetime,
        granularity: str | None = None,
        limit: int = 500,
        offset: int = 0,
    ) -> list[DocumentChunk]: ...

    def list_summary_chunk_index_rows_in_period(
        self,
        *,
        doc_type: str,
        granularity: str | None = None,
        period_start: datetime,
        period_end: datetime,
        limit: int = 500,
        offset: int = 0,
    ) -> list[dict[str, Any]]: ...

    def list_document_chunk_index_rows_in_period(
        self,
        *,
        doc_type: str,
        kind: str,
        granularity: str | None = None,
        period_start: datetime,
        period_end: datetime,
        limit: int = 500,
        offset: int = 0,
    ) -> list[dict[str, Any]]: ...


class AnalysisRepositoryPort(Protocol):
    def record_metric(
        self, *, run_id: str, name: str, value: float, unit: str | None = None
    ) -> None: ...

    def list_items_for_llm_analysis(
        self,
        *,
        limit: int,
        triage_required: bool,
        period_start: datetime | None = None,
        period_end: datetime | None = None,
    ) -> list[Item]: ...

    def get_latest_content_texts(
        self, *, item_id: int, content_types: list[str]
    ) -> dict[str, str | None]: ...

    def save_analysis(
        self,
        *,
        item_id: int,
        result: AnalysisResult,
        mirror_item_state: bool = True,
    ) -> Analysis: ...

    def mark_item_failed(self, *, item_id: int) -> None: ...

    def mark_item_retryable_failed(self, *, item_id: int) -> None: ...

    def add_artifact(
        self,
        *,
        run_id: str,
        item_id: int | None,
        kind: str,
        path: str,
        details: dict[str, Any] | None = None,
    ) -> None: ...

    def create_pass_output(
        self,
        *,
        run_id: str,
        pass_kind: str,
        status: str,
        granularity: str | None = None,
        period_start: datetime | None = None,
        period_end: datetime | None = None,
        schema_version: int = 1,
        payload: dict[str, Any] | list[Any] | None = None,
        diagnostics: dict[str, Any] | list[Any] | None = None,
        input_refs: list[dict[str, Any]] | None = None,
        content_hash: str | None = None,
    ) -> PassOutput: ...

    def get_pass_output(self, *, pass_output_id: int) -> PassOutput | None: ...

    def get_latest_pass_output(
        self,
        *,
        pass_kind: str,
        status: str | None = None,
        granularity: str | None = None,
        period_start: datetime | None = None,
        period_end: datetime | None = None,
    ) -> PassOutput | None: ...


class PublishRepositoryPort(Protocol):
    def record_metric(
        self, *, run_id: str, name: str, value: float, unit: str | None = None
    ) -> None: ...

    def list_items_for_publish(
        self,
        *,
        limit: int,
        min_relevance_score: float,
        period_start: datetime | None = None,
        period_end: datetime | None = None,
    ) -> list[tuple[Item, Analysis]]: ...

    def has_sent_delivery(
        self, *, item_id: int, channel: str, destination: str
    ) -> bool: ...

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

    def add_artifact(
        self,
        *,
        run_id: str,
        item_id: int | None,
        kind: str,
        path: str,
        details: dict[str, Any] | None = None,
    ) -> None: ...

    @staticmethod
    def decode_list(value: str | None) -> list[str]: ...


class TrendRepositoryPort(Protocol):
    engine: Any

    def record_metric(
        self, *, run_id: str, name: str, value: float, unit: str | None = None
    ) -> None: ...

    def list_analyzed_items_in_period(
        self,
        *,
        period_start: datetime,
        period_end: datetime,
        limit: int,
        offset: int = 0,
    ) -> list[tuple[Item, Analysis]]: ...

    def upsert_document_for_item(self, *, item: Item) -> Document: ...

    def upsert_document_for_trend(
        self,
        *,
        granularity: str,
        period_start: datetime,
        period_end: datetime,
        title: str,
    ) -> Document: ...

    def upsert_document_for_idea(
        self,
        *,
        granularity: str,
        period_start: datetime,
        period_end: datetime,
        title: str,
    ) -> Document: ...

    def upsert_document_chunk(
        self,
        *,
        doc_id: int,
        chunk_index: int,
        kind: str,
        text_value: str,
        start_char: int | None = None,
        end_char: int | None = None,
        source_content_type: str | None = None,
    ) -> tuple[DocumentChunk, bool]: ...

    def delete_document_chunks(
        self,
        *,
        doc_id: int,
        kind: str | None = None,
        chunk_index_gte: int | None = None,
    ) -> int: ...

    def list_documents(
        self,
        *,
        doc_type: str,
        period_start: datetime,
        period_end: datetime,
        granularity: str | None = None,
        order_by: str = "event_desc",
        offset: int = 0,
        limit: int = 50,
    ) -> list[Document]: ...

    def get_document(self, *, doc_id: int) -> Document | None: ...

    def get_item(self, *, item_id: int) -> Item | None: ...

    def read_document_chunk(
        self, *, doc_id: int, chunk_index: int
    ) -> DocumentChunk | None: ...

    def search_chunks_text(
        self,
        *,
        query: str,
        doc_type: str,
        granularity: str | None = None,
        period_start: datetime,
        period_end: datetime,
        limit: int = 10,
    ) -> list[dict[str, Any]]: ...

    def list_summary_chunks_in_period(
        self,
        *,
        doc_type: str,
        period_start: datetime,
        period_end: datetime,
        limit: int = 500,
        offset: int = 0,
    ) -> list[DocumentChunk]: ...

    def list_document_chunks_in_period(
        self,
        *,
        doc_type: str,
        kind: str,
        period_start: datetime,
        period_end: datetime,
        granularity: str | None = None,
        limit: int = 500,
        offset: int = 0,
    ) -> list[DocumentChunk]: ...

    def list_summary_chunk_index_rows_in_period(
        self,
        *,
        doc_type: str,
        granularity: str | None = None,
        period_start: datetime,
        period_end: datetime,
        limit: int = 500,
        offset: int = 0,
    ) -> list[dict[str, Any]]: ...

    def list_document_chunk_index_rows_in_period(
        self,
        *,
        doc_type: str,
        kind: str,
        granularity: str | None = None,
        period_start: datetime,
        period_end: datetime,
        limit: int = 500,
        offset: int = 0,
    ) -> list[dict[str, Any]]: ...

    def get_latest_content_texts(
        self, *, item_id: int, content_types: list[str]
    ) -> dict[str, str | None]: ...

    def get_latest_content_texts_for_items(
        self, *, item_ids: list[int], content_types: list[str]
    ) -> dict[int, dict[str, str | None]]: ...

    def get_latest_contents(
        self, *, item_ids: list[int], content_type: str
    ) -> dict[int, Content]: ...


class TrendStageRepositoryPort(TrendRepositoryPort, Protocol):
    def add_artifact(
        self,
        *,
        run_id: str,
        item_id: int | None,
        kind: str,
        path: str,
        details: dict[str, Any] | None = None,
    ) -> None: ...

    def create_pass_output(
        self,
        *,
        run_id: str,
        pass_kind: str,
        status: str,
        granularity: str | None = None,
        period_start: datetime | None = None,
        period_end: datetime | None = None,
        schema_version: int = 1,
        payload: dict[str, Any] | list[Any] | None = None,
        diagnostics: dict[str, Any] | list[Any] | None = None,
        input_refs: list[dict[str, Any]] | None = None,
        content_hash: str | None = None,
    ) -> PassOutput: ...

    def get_pass_output(self, *, pass_output_id: int) -> PassOutput | None: ...

    def get_latest_pass_output(
        self,
        *,
        pass_kind: str,
        status: str | None = None,
        granularity: str | None = None,
        period_start: datetime | None = None,
        period_end: datetime | None = None,
    ) -> PassOutput | None: ...

    def has_sent_trend_delivery(
        self, *, doc_id: int, channel: str, destination: str, content_hash: str
    ) -> bool: ...

    def upsert_trend_delivery(
        self,
        *,
        doc_id: int,
        channel: str,
        destination: str,
        content_hash: str,
        message_id: str | None,
        status: str,
        error: str | None = None,
    ) -> TrendDelivery: ...
