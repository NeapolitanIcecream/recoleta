from __future__ import annotations

from datetime import datetime

from sqlalchemy import Text, UniqueConstraint
from sqlmodel import Field, SQLModel

from recoleta.types import utc_now

RUN_STATUS_RUNNING = "running"
RUN_STATUS_SUCCEEDED = "succeeded"
RUN_STATUS_FAILED = "failed"

ITEM_STATE_INGESTED = "ingested"
ITEM_STATE_ENRICHED = "enriched"
ITEM_STATE_TRIAGED = "triaged"
ITEM_STATE_ANALYZED = "analyzed"
ITEM_STATE_PUBLISHED = "published"
ITEM_STATE_RETRYABLE_FAILED = "retryable_failed"
ITEM_STATE_FAILED = "failed"

DELIVERY_CHANNEL_TELEGRAM = "telegram"
DELIVERY_STATUS_SENT = "sent"
DELIVERY_STATUS_SKIPPED = "skipped"
DELIVERY_STATUS_FAILED = "failed"

DOC_TYPE_ITEM = "item"
DOC_TYPE_TREND = "trend"


class Run(SQLModel, table=True):
    __tablename__ = "runs"  # pyright: ignore[reportAssignmentType,reportIncompatibleVariableOverride]

    id: str = Field(primary_key=True, max_length=64)
    started_at: datetime = Field(default_factory=utc_now)
    heartbeat_at: datetime = Field(default_factory=utc_now, index=True)
    finished_at: datetime | None = None
    status: str = Field(default=RUN_STATUS_RUNNING, max_length=24, index=True)
    config_fingerprint: str = Field(max_length=128)


class WorkspaceLease(SQLModel, table=True):
    __tablename__ = "workspace_leases"  # pyright: ignore[reportAssignmentType,reportIncompatibleVariableOverride]

    name: str = Field(primary_key=True, max_length=64)
    owner_token: str = Field(max_length=128)
    run_id: str | None = Field(default=None, max_length=64, index=True)
    pid: int | None = Field(default=None)
    hostname: str | None = Field(default=None, max_length=255)
    command: str = Field(max_length=128)
    acquired_at: datetime = Field(default_factory=utc_now)
    heartbeat_at: datetime = Field(default_factory=utc_now, index=True)
    expires_at: datetime = Field(index=True)


class Item(SQLModel, table=True):
    __tablename__ = "items"  # pyright: ignore[reportAssignmentType,reportIncompatibleVariableOverride]
    __table_args__ = (
        UniqueConstraint(
            "source", "source_item_id", name="uq_items_source_source_item_id"
        ),
        UniqueConstraint("canonical_url_hash", name="uq_items_canonical_url_hash"),
    )

    id: int | None = Field(default=None, primary_key=True)
    source: str = Field(index=True, max_length=32)
    source_item_id: str | None = Field(default=None, max_length=256)
    canonical_url: str = Field(sa_type=Text)
    canonical_url_hash: str = Field(max_length=64, index=True)
    title: str = Field(sa_type=Text)
    authors: str | None = Field(default=None, sa_type=Text)
    published_at: datetime | None = Field(default=None, index=True)
    raw_metadata_json: str = Field(default="{}", sa_type=Text)
    state: str = Field(default=ITEM_STATE_INGESTED, max_length=24, index=True)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class Content(SQLModel, table=True):
    __tablename__ = "contents"  # pyright: ignore[reportAssignmentType,reportIncompatibleVariableOverride]

    id: int | None = Field(default=None, primary_key=True)
    item_id: int = Field(foreign_key="items.id", index=True)
    content_type: str = Field(max_length=32)
    text: str | None = Field(default=None, sa_type=Text)
    artifact_path: str | None = Field(default=None, max_length=2048)
    content_hash: str = Field(max_length=64, index=True)
    created_at: datetime = Field(default_factory=utc_now)


class Analysis(SQLModel, table=True):
    __tablename__ = "analyses"  # pyright: ignore[reportAssignmentType,reportIncompatibleVariableOverride]
    __table_args__ = (
        UniqueConstraint("item_id", "scope", name="uq_analyses_item_scope"),
    )

    id: int | None = Field(default=None, primary_key=True)
    item_id: int = Field(foreign_key="items.id", index=True)
    scope: str = Field(default="default", max_length=64, index=True)
    model: str = Field(max_length=128)
    provider: str = Field(max_length=64)
    summary: str = Field(sa_type=Text)
    topics_json: str = Field(default="[]", sa_type=Text)
    relevance_score: float = 0.0
    novelty_score: float | None = None
    cost_usd: float | None = None
    latency_ms: int | None = None
    created_at: datetime = Field(default_factory=utc_now)


class ItemStreamState(SQLModel, table=True):
    __tablename__ = "item_stream_states"  # pyright: ignore[reportAssignmentType,reportIncompatibleVariableOverride]
    __table_args__ = (
        UniqueConstraint(
            "item_id",
            "stream",
            name="uq_item_stream_states_item_stream",
        ),
    )

    id: int | None = Field(default=None, primary_key=True)
    item_id: int = Field(foreign_key="items.id", index=True)
    stream: str = Field(max_length=64, index=True)
    state: str = Field(max_length=24, index=True)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class Delivery(SQLModel, table=True):
    __tablename__ = "deliveries"  # pyright: ignore[reportAssignmentType,reportIncompatibleVariableOverride]
    __table_args__ = (
        UniqueConstraint(
            "item_id",
            "channel",
            "destination",
            name="uq_deliveries_item_channel_destination",
        ),
    )

    id: int | None = Field(default=None, primary_key=True)
    item_id: int = Field(foreign_key="items.id", index=True)
    channel: str = Field(max_length=32)
    destination: str = Field(max_length=128, index=True)
    message_id: str | None = Field(default=None, max_length=128)
    status: str = Field(default=DELIVERY_STATUS_SENT, max_length=24, index=True)
    error: str | None = Field(default=None, sa_type=Text)
    sent_at: datetime | None = None


class TrendDelivery(SQLModel, table=True):
    __tablename__ = "trend_deliveries"  # pyright: ignore[reportAssignmentType,reportIncompatibleVariableOverride]
    __table_args__ = (
        UniqueConstraint(
            "doc_id",
            "channel",
            "destination",
            name="uq_trend_deliveries_doc_channel_destination",
        ),
    )

    id: int | None = Field(default=None, primary_key=True)
    doc_id: int = Field(foreign_key="documents.id", index=True)
    channel: str = Field(max_length=32)
    destination: str = Field(max_length=128, index=True)
    content_hash: str = Field(max_length=64, index=True)
    message_id: str | None = Field(default=None, max_length=128)
    status: str = Field(default=DELIVERY_STATUS_SENT, max_length=24, index=True)
    error: str | None = Field(default=None, sa_type=Text)
    sent_at: datetime | None = None


class Metric(SQLModel, table=True):
    __tablename__ = "metrics"  # pyright: ignore[reportAssignmentType,reportIncompatibleVariableOverride]

    id: int | None = Field(default=None, primary_key=True)
    run_id: str = Field(foreign_key="runs.id", index=True)
    name: str = Field(max_length=128, index=True)
    value: float
    unit: str | None = Field(default=None, max_length=32)
    created_at: datetime = Field(default_factory=utc_now)


class PassOutput(SQLModel, table=True):
    __tablename__ = "pass_outputs"  # pyright: ignore[reportAssignmentType,reportIncompatibleVariableOverride]

    id: int | None = Field(default=None, primary_key=True)
    run_id: str = Field(foreign_key="runs.id", index=True)
    scope: str = Field(default="default", max_length=64, index=True)
    pass_kind: str = Field(max_length=64, index=True)
    status: str = Field(max_length=24, index=True)
    granularity: str | None = Field(default=None, max_length=16, index=True)
    period_start: datetime | None = Field(default=None, index=True)
    period_end: datetime | None = Field(default=None, index=True)
    schema_version: int = Field(default=1)
    content_hash: str = Field(max_length=64, index=True)
    payload_json: str = Field(default="{}", sa_type=Text)
    diagnostics_json: str = Field(default="{}", sa_type=Text)
    input_refs_json: str = Field(default="[]", sa_type=Text)
    created_at: datetime = Field(default_factory=utc_now, index=True)


class SourcePullState(SQLModel, table=True):
    __tablename__ = "source_pull_states"  # pyright: ignore[reportAssignmentType,reportIncompatibleVariableOverride]
    __table_args__ = (
        UniqueConstraint(
            "source",
            "scope_kind",
            "scope_key",
            name="uq_source_pull_states_source_scope",
        ),
    )

    id: int | None = Field(default=None, primary_key=True)
    source: str = Field(index=True, max_length=32)
    scope_kind: str = Field(index=True, max_length=32)
    scope_key: str = Field(index=True, max_length=512)
    etag: str | None = Field(default=None, max_length=512)
    last_modified: str | None = Field(default=None, max_length=512)
    watermark_published_at: datetime | None = Field(default=None, index=True)
    cursor_json: str = Field(default="{}", sa_type=Text)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class Artifact(SQLModel, table=True):
    __tablename__ = "artifacts"  # pyright: ignore[reportAssignmentType,reportIncompatibleVariableOverride]

    id: int | None = Field(default=None, primary_key=True)
    run_id: str = Field(foreign_key="runs.id", index=True)
    item_id: int | None = Field(default=None, foreign_key="items.id", index=True)
    kind: str = Field(max_length=64, index=True)
    path: str = Field(max_length=2048)
    created_at: datetime = Field(default_factory=utc_now)


class Document(SQLModel, table=True):
    __tablename__ = "documents"  # pyright: ignore[reportAssignmentType,reportIncompatibleVariableOverride]
    __table_args__ = (
        UniqueConstraint(
            "doc_type",
            "item_id",
            "scope",
            name="uq_documents_doc_type_item_scope",
        ),
        UniqueConstraint(
            "doc_type",
            "scope",
            "granularity",
            "period_start",
            "period_end",
            name="uq_documents_doc_type_scope_granularity_period",
        ),
    )

    id: int | None = Field(default=None, primary_key=True)
    doc_type: str = Field(index=True, max_length=16)
    scope: str = Field(default="default", max_length=64, index=True)

    # For doc_type == "item"
    item_id: int | None = Field(default=None, foreign_key="items.id", index=True)
    source: str | None = Field(default=None, max_length=32)
    canonical_url: str | None = Field(default=None, sa_type=Text)
    title: str | None = Field(default=None, sa_type=Text)
    published_at: datetime | None = Field(default=None, index=True)

    # For doc_type == "trend"
    granularity: str | None = Field(default=None, max_length=16, index=True)
    period_start: datetime | None = Field(default=None, index=True)
    period_end: datetime | None = Field(default=None, index=True)

    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class DocumentChunk(SQLModel, table=True):
    __tablename__ = "document_chunks"  # pyright: ignore[reportAssignmentType,reportIncompatibleVariableOverride]
    __table_args__ = (
        UniqueConstraint("doc_id", "chunk_index", name="uq_document_chunks_doc_chunk"),
    )

    id: int | None = Field(default=None, primary_key=True)
    doc_id: int = Field(foreign_key="documents.id", index=True)
    chunk_index: int = Field(index=True)
    kind: str = Field(max_length=16, index=True)  # summary|content|meta
    text: str = Field(sa_type=Text)
    start_char: int | None = None
    end_char: int | None = None
    text_hash: str = Field(max_length=64, index=True)
    source_content_type: str | None = Field(default=None, max_length=32)
    created_at: datetime = Field(default_factory=utc_now)


class ChunkEmbedding(SQLModel, table=True):
    __tablename__ = "chunk_embeddings"  # pyright: ignore[reportAssignmentType,reportIncompatibleVariableOverride]
    __table_args__ = (
        UniqueConstraint("chunk_id", "model", name="uq_chunk_embeddings_chunk_model"),
    )

    id: int | None = Field(default=None, primary_key=True)
    chunk_id: int = Field(foreign_key="document_chunks.id", index=True)
    model: str = Field(max_length=128, index=True)
    dimensions: int | None = Field(default=None)
    vector_json: str = Field(sa_type=Text)
    text_hash: str = Field(max_length=64, index=True)
    created_at: datetime = Field(default_factory=utc_now)
