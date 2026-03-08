from __future__ import annotations

import json

from datetime import datetime
from typing import Any

from recoleta.config import Settings
from recoleta.models import Analysis, Content, Delivery, Item
from recoleta.storage import Repository
from recoleta.types import AnalysisResult, AnalyzeDebug, ItemDraft


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
            summary=f"Summary for {title}",
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

    def list_items_for_stream_analysis(
        self, *, stream: str, limit: int, selected_only: bool = False
    ) -> list[Item]:
        raise NotImplementedError

    def save_analysis(
        self,
        *,
        item_id: int,
        result: AnalysisResult,
        scope: str = "default",
        mirror_item_state: bool = True,
    ) -> Analysis:
        raise NotImplementedError

    def mark_item_enriched(self, *, item_id: int) -> None:
        raise NotImplementedError

    def mark_item_triaged(self, *, item_id: int) -> None:
        raise NotImplementedError

    def mark_item_stream_state(
        self,
        *,
        item_id: int,
        stream: str,
        state: str,
        mirror_item_state: bool = False,
    ) -> None:
        raise NotImplementedError

    def mark_item_failed(self, *, item_id: int) -> None:
        raise NotImplementedError

    def mark_item_retryable_failed(self, *, item_id: int) -> None:
        raise NotImplementedError

    def list_items_for_publish(
        self, *, limit: int, min_relevance_score: float, scope: str = "default"
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
