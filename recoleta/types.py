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
    topics: list[str]
    relevance_score: float
    novelty_score: float | None
    cost_usd: float | None
    latency_ms: int | None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None


@dataclass(slots=True)
class AnalyzeDebug:
    request: dict[str, Any]
    response: dict[str, Any]


@dataclass(slots=True)
class AnalysisWrite:
    item_id: int
    result: AnalysisResult
    mirror_item_state: bool = True


@dataclass(slots=True)
class ItemStateUpdate:
    item_id: int
    state: str
    mirror_item_state: bool = False


@dataclass(slots=True)
class MetricPoint:
    name: str
    value: float
    unit: str | None = None


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


@dataclass(slots=True)
class TrendResult:
    doc_id: int
    granularity: str
    period_start: datetime
    period_end: datetime
    title: str
    pass_output_id: int | None = None


@dataclass(slots=True)
class IdeasResult:
    pass_output_id: int | None
    granularity: str
    period_start: datetime
    period_end: datetime
    title: str
    status: str
    note_path: Path | None = None
    upstream_pass_output_id: int | None = None
