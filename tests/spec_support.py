from __future__ import annotations

import json

from recoleta.config import Settings
from recoleta.models import Content, Item
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
            insight="This matters because it aligns with user interests.",
            idea_directions=["Try reproducing the approach.", "Benchmark against a baseline."],
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
                "insight": result.insight,
                "relevance_score": result.relevance_score,
            },
        )
        return result, debug


class FakeTelegramSender:
    def __init__(self) -> None:
        self.messages: list[str] = []

    def send(self, text: str) -> str:
        self.messages.append(text)
        return f"message-{len(self.messages)}"


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
    def __init__(self) -> None:
        self.metrics: list[tuple[str, float, str | None]] = []
        self.artifacts: list[tuple[str, int | None, str, str]] = []

    def upsert_item(self, draft: ItemDraft):  # type: ignore[no-untyped-def]
        raise RuntimeError("simulated repository failure")

    def record_metric(self, *, run_id: str, name: str, value: float, unit: str | None = None) -> None:
        self.metrics.append((name, value, unit))

    def add_artifact(self, *, run_id: str, item_id: int | None, kind: str, path: str) -> None:
        self.artifacts.append((run_id, item_id, kind, path))

    def list_items_for_analysis(self, *, limit: int) -> list[Item]:
        raise NotImplementedError

    def get_latest_content(self, *, item_id: int, content_type: str) -> Content | None:
        raise NotImplementedError

    def get_latest_contents(self, *, item_ids: list[int], content_type: str) -> dict[int, Content]:
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

    def save_analysis(self, *, item_id: int, result: AnalysisResult):  # type: ignore[no-untyped-def]
        raise NotImplementedError

    def mark_item_enriched(self, *, item_id: int) -> None:
        raise NotImplementedError

    def mark_item_failed(self, *, item_id: int) -> None:
        raise NotImplementedError

    def mark_item_retryable_failed(self, *, item_id: int) -> None:
        raise NotImplementedError

    def list_items_for_publish(self, *, limit: int, min_relevance_score: float):  # type: ignore[no-untyped-def]
        raise NotImplementedError

    def has_sent_delivery(self, *, item_id: int, channel: str, destination: str) -> bool:
        raise NotImplementedError

    def count_sent_deliveries_since(self, *, channel: str, destination: str, since):  # type: ignore[no-untyped-def]
        raise NotImplementedError

    def upsert_delivery(  # type: ignore[no-untyped-def]
        self,
        *,
        item_id: int,
        channel: str,
        destination: str,
        message_id: str | None,
        status: str,
        error: str | None = None,
    ):
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
