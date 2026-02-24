from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def sha256_hex(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()


@dataclass(slots=True)
class ItemDraft:
    source: str
    source_item_id: str | None
    canonical_url: str
    canonical_url_hash: str
    title: str
    authors: list[str] = field(default_factory=list)
    published_at: datetime | None = None
    raw_metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_values(
        cls,
        *,
        source: str,
        source_item_id: str | None,
        canonical_url: str,
        title: str,
        authors: list[str] | None = None,
        published_at: datetime | None = None,
        raw_metadata: dict[str, Any] | None = None,
    ) -> "ItemDraft":
        normalized_url = canonical_url.strip()
        if not normalized_url:
            raise ValueError("canonical_url must not be empty")
        normalized_title = title.strip()
        if not normalized_title:
            raise ValueError("title must not be empty")
        return cls(
            source=source,
            source_item_id=source_item_id,
            canonical_url=normalized_url,
            canonical_url_hash=sha256_hex(normalized_url),
            title=normalized_title,
            authors=authors or [],
            published_at=published_at,
            raw_metadata=raw_metadata or {},
        )


@dataclass(slots=True)
class AnalysisResult:
    model: str
    provider: str
    summary: str
    insight: str
    idea_directions: list[str]
    topics: list[str]
    relevance_score: float
    novelty_score: float | None
    cost_usd: float | None
    latency_ms: int | None


@dataclass(slots=True)
class IngestResult:
    inserted: int = 0
    updated: int = 0
    failed: int = 0


@dataclass(slots=True)
class AnalyzeResult:
    processed: int = 0
    failed: int = 0


@dataclass(slots=True)
class PublishResult:
    sent: int = 0
    skipped: int = 0
    failed: int = 0
    note_paths: list[Path] = field(default_factory=list)
