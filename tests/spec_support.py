from __future__ import annotations

from dataclasses import dataclass, field
import json
import sys
from types import ModuleType

from datetime import datetime
from typing import Any

from recoleta.config import Settings
from recoleta.models import Analysis, Content, Delivery, Item
from recoleta.storage import Repository
from recoleta.types import AnalysisResult, AnalyzeDebug, ItemDraft


class FakeHuldraCachePolicy:
    CACHE_ONLY = "cache_only"


class FakeHuldraReadinessMode:
    ANALYSIS_READY = "analysis_ready"
    RAW_COMPLETED = "raw_completed"


@dataclass(slots=True)
class FakeHuldraArxivRequest:
    client_id: str
    search_query: str
    submitted_start: datetime
    submitted_end: datetime
    cache_policy: str
    readiness: str
    sort_by: str = "submittedDate"
    sort_order: str = "descending"
    start: int = 0
    max_results: int = 100
    maturity_lag_days: int = 1
    timeout_seconds: float | None = None


@dataclass(slots=True)
class FakeHuldraArxivPaper:
    arxiv_id: str
    version: int | None
    canonical_url: str
    title: str
    abstract: str | None = None
    authors: list[str] = field(default_factory=list)
    primary_category: str | None = None
    categories: list[str] = field(default_factory=list)
    published_at: datetime | None = None
    updated_at: datetime | None = None
    comment: str | None = None
    journal_ref: str | None = None
    doi: str | None = None
    raw_atom: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class FakeHuldraArxivResult:
    serving_mode: str
    status: str
    cache_key: str | None
    cache_readable: bool
    mature: bool
    analysis_ready: bool
    ready: bool
    papers: list[FakeHuldraArxivPaper] = field(default_factory=list)
    papers_total: int = 0
    cached_papers_total: int = 0
    blocked_reason: str | None = None


@dataclass(slots=True)
class FakeHuldraMaintenanceResult:
    requested_total: int = 0
    completed_windows_total: int = 0
    cache_hit_total: int = 0
    cache_miss_total: int = 0
    upstream_requests_total: int = 0
    upstream_429_total: int = 0
    retry_after_seconds: int | None = None
    cooldown_active_total: int = 0
    skipped_windows_total: int = 0
    rate_limited_windows_total: int = 0
    failed_windows_total: int = 0
    papers_total: int = 0


class _UnconfiguredFakeHuldraClient:
    def __init__(self, *_: Any, **__: Any) -> None:
        raise AssertionError("test must install a fake HuldraClient")


def install_fake_huldra(monkeypatch: Any) -> ModuleType:
    package = ModuleType("huldra")
    client_module = ModuleType("huldra.client")
    models_module = ModuleType("huldra.models")
    setattr(client_module, "HuldraClient", _UnconfiguredFakeHuldraClient)
    setattr(models_module, "ArxivRequest", FakeHuldraArxivRequest)
    setattr(models_module, "ArxivPaper", FakeHuldraArxivPaper)
    setattr(models_module, "ArxivResult", FakeHuldraArxivResult)
    setattr(models_module, "CachePolicy", FakeHuldraCachePolicy)
    setattr(models_module, "ReadinessMode", FakeHuldraReadinessMode)
    setattr(models_module, "HuldraMaintenanceResult", FakeHuldraMaintenanceResult)
    package.client = client_module  # type: ignore[attr-defined]
    package.models = models_module  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "huldra", package)
    monkeypatch.setitem(sys.modules, "huldra.client", client_module)
    monkeypatch.setitem(sys.modules, "huldra.models", models_module)
    return package


class FakeAnalyzer:
    def __init__(self, should_fail: bool = False) -> None:
        self.should_fail = should_fail

    def analyze(
        self,
        *,
        title: str,
        canonical_url: str,
        user_topics: list[str],
        content: str | None = None,  # noqa: ARG002
        include_debug: bool = False,
    ) -> tuple[AnalysisResult, AnalyzeDebug | None]:
        if self.should_fail:
            raise RuntimeError("simulated analyzer failure")

        result = AnalysisResult(
            model="test/fake-model",
            provider="test",
            summary=(
                "## Summary\n"
                f"Summary for {title}\n\n"
                "## Problem\n"
                "- Existing workflows are brittle.\n\n"
                "## Approach\n"
                "- Use a structured pipeline.\n\n"
                "## Results\n"
                "- Stronger grounding on the benchmark.\n"
            ),
            topics=user_topics[:2] or ["general"],
            relevance_score=0.92,
            novelty_score=0.55,
            cost_usd=0.0,
            latency_ms=1,
        )
        if not include_debug:
            return result, None

        debug = AnalyzeDebug(
            request={
                "model": result.model,
                "title": title,
                "canonical_url": canonical_url,
                "user_topics": user_topics,
            },
            response={
                "summary": result.summary,
                "relevance_score": result.relevance_score,
            },
        )
        return result, debug


class FakeTelegramSender:
    def __init__(self) -> None:
        self.messages: list[str] = []
        self.documents: list[dict[str, Any]] = []

    def send(self, text: str) -> str:
        self.messages.append(text)
        return f"message-{len(self.messages)}"

    def send_document(
        self,
        *,
        filename: str,
        content: bytes,
        caption: str | None = None,
    ) -> str:
        self.documents.append(
            {
                "filename": filename,
                "content": content,
                "caption": caption,
            }
        )
        return f"document-{len(self.documents)}"


class FlakyTelegramSender:
    def __init__(self, *, fail_first: bool = True) -> None:
        self.fail_first = fail_first
        self.attempts = 0
        self.messages: list[str] = []

    def send(self, text: str) -> str:
        self.attempts += 1
        if self.fail_first and self.attempts == 1:
            raise RuntimeError("simulated telegram failure")
        self.messages.append(text)
        return f"message-{len(self.messages)}"


class ExplodingRepository:
    engine: Any

    def __init__(self) -> None:
        self.engine = None
        self.metrics: list[tuple[str, float, str | None]] = []
        self.artifacts: list[tuple[str, int | None, str, str]] = []

    def sql_diagnostics(self) -> Any:
        return {}

    def upsert_item(self, draft: ItemDraft) -> tuple[Item, bool]:
        raise RuntimeError("simulated repository failure")

    def record_metric(
        self, *, run_id: str, name: str, value: float, unit: str | None = None
    ) -> None:
        self.metrics.append((name, value, unit))

    def add_artifact(
        self, *, run_id: str, item_id: int | None, kind: str, path: str
    ) -> None:
        self.artifacts.append((run_id, item_id, kind, path))

    def list_items_for_analysis(self, *, limit: int) -> list[Item]:
        raise NotImplementedError

    def list_items_for_llm_analysis(
        self, *, limit: int, triage_required: bool
    ) -> list[Item]:
        raise NotImplementedError

    def get_latest_content(self, *, item_id: int, content_type: str) -> Content | None:
        raise NotImplementedError

    def get_latest_content_texts(
        self, *, item_id: int, content_types: list[str]
    ) -> dict[str, str | None]:
        raise NotImplementedError

    def get_latest_content_texts_for_items(
        self, *, item_ids: list[int], content_types: list[str]
    ) -> dict[int, dict[str, str | None]]:
        raise NotImplementedError

    def get_latest_contents(
        self, *, item_ids: list[int], content_type: str
    ) -> dict[int, Content]:
        raise NotImplementedError

    def upsert_contents_texts(
        self, *, item_id: int, texts_by_type: dict[str, str]
    ) -> int:
        raise NotImplementedError

    def upsert_content(
        self,
        *,
        item_id: int,
        content_type: str,
        text: str | None,
        artifact_path: str | None = None,
    ) -> Content:
        raise NotImplementedError

    def upsert_content_with_inserted(
        self,
        *,
        item_id: int,
        content_type: str,
        text: str | None,
        artifact_path: str | None = None,
    ) -> tuple[Content, bool]:
        raise NotImplementedError

    def save_analysis(
        self,
        *,
        item_id: int,
        result: AnalysisResult,
        mirror_item_state: bool = True,
    ) -> Analysis:
        raise NotImplementedError

    def mark_item_enriched(self, *, item_id: int) -> None:
        raise NotImplementedError

    def mark_item_triaged(self, *, item_id: int) -> None:
        raise NotImplementedError

    def mark_item_failed(self, *, item_id: int) -> None:
        raise NotImplementedError

    def mark_item_retryable_failed(self, *, item_id: int) -> None:
        raise NotImplementedError

    def list_items_for_publish(
        self, *, limit: int, min_relevance_score: float
    ) -> list[tuple[Item, Analysis]]:
        raise NotImplementedError

    def has_sent_delivery(
        self, *, item_id: int, channel: str, destination: str
    ) -> bool:
        raise NotImplementedError

    def count_sent_deliveries_since(
        self, *, channel: str, destination: str, since: datetime
    ) -> int:
        raise NotImplementedError

    def upsert_delivery(
        self,
        *,
        item_id: int,
        channel: str,
        destination: str,
        message_id: str | None,
        status: str,
        error: str | None = None,
    ) -> Delivery:
        raise NotImplementedError

    def mark_item_published(self, *, item_id: int) -> None:
        raise NotImplementedError

    @staticmethod
    def decode_list(value: str | None) -> list[str]:
        if not value:
            return []
        loaded = json.loads(value)
        if isinstance(loaded, list):
            return [str(item) for item in loaded]
        return []


def _build_runtime() -> tuple[Settings, Repository]:
    settings = Settings()  # pyright: ignore[reportCallIssue]
    repository = Repository(db_path=settings.recoleta_db_path)
    repository.init_schema()
    return settings, repository
