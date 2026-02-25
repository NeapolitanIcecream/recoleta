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
ITEM_STATE_ANALYZED = "analyzed"
ITEM_STATE_PUBLISHED = "published"
ITEM_STATE_RETRYABLE_FAILED = "retryable_failed"
ITEM_STATE_FAILED = "failed"

DELIVERY_CHANNEL_TELEGRAM = "telegram"
DELIVERY_STATUS_SENT = "sent"
DELIVERY_STATUS_SKIPPED = "skipped"
DELIVERY_STATUS_FAILED = "failed"


class Run(SQLModel, table=True):
    __tablename__ = "runs"  # pyright: ignore[reportAssignmentType,reportIncompatibleVariableOverride]

    id: str = Field(primary_key=True, max_length=64)
    started_at: datetime = Field(default_factory=utc_now)
    finished_at: datetime | None = None
    status: str = Field(default=RUN_STATUS_RUNNING, max_length=24, index=True)
    config_fingerprint: str = Field(max_length=128)


class Item(SQLModel, table=True):
    __tablename__ = "items"  # pyright: ignore[reportAssignmentType,reportIncompatibleVariableOverride]
    __table_args__ = (
        UniqueConstraint("source", "source_item_id", name="uq_items_source_source_item_id"),
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
    __table_args__ = (UniqueConstraint("item_id", name="uq_analyses_item_id"),)

    id: int | None = Field(default=None, primary_key=True)
    item_id: int = Field(foreign_key="items.id", index=True)
    model: str = Field(max_length=128)
    provider: str = Field(max_length=64)
    summary: str = Field(sa_type=Text)
    insight: str = Field(sa_type=Text)
    idea_directions_json: str = Field(default="[]", sa_type=Text)
    topics_json: str = Field(default="[]", sa_type=Text)
    relevance_score: float = 0.0
    novelty_score: float | None = None
    cost_usd: float | None = None
    latency_ms: int | None = None
    created_at: datetime = Field(default_factory=utc_now)


class Delivery(SQLModel, table=True):
    __tablename__ = "deliveries"  # pyright: ignore[reportAssignmentType,reportIncompatibleVariableOverride]
    __table_args__ = (
        UniqueConstraint("item_id", "channel", "destination", name="uq_deliveries_item_channel_destination"),
    )

    id: int | None = Field(default=None, primary_key=True)
    item_id: int = Field(foreign_key="items.id", index=True)
    channel: str = Field(max_length=32)
    destination: str = Field(max_length=128, index=True)
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


class Artifact(SQLModel, table=True):
    __tablename__ = "artifacts"  # pyright: ignore[reportAssignmentType,reportIncompatibleVariableOverride]

    id: int | None = Field(default=None, primary_key=True)
    run_id: str = Field(foreign_key="runs.id", index=True)
    item_id: int | None = Field(default=None, foreign_key="items.id", index=True)
    kind: str = Field(max_length=64, index=True)
    path: str = Field(max_length=2048)
    created_at: datetime = Field(default_factory=utc_now)
