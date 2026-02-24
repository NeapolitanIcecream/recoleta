from __future__ import annotations

import json
from pathlib import Path

import pytest
import respx
from sqlmodel import Session, select

from recoleta.config import Settings
from recoleta.models import (
    DELIVERY_CHANNEL_TELEGRAM,
    DELIVERY_STATUS_SENT,
    ITEM_STATE_ANALYZED,
    Delivery,
    Item,
)
from recoleta.pipeline import PipelineService
from recoleta.sources import fetch_rss_drafts
from recoleta.storage import Repository
from recoleta.types import AnalysisResult, ItemDraft


class FakeAnalyzer:
    def __init__(self, should_fail: bool = False) -> None:
        self.should_fail = should_fail

    def analyze(self, *, title: str, canonical_url: str, user_topics: list[str]) -> AnalysisResult:
        if self.should_fail:
            raise RuntimeError("simulated analyzer failure")

        return AnalysisResult(
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

    def save_analysis(self, *, item_id: int, result: AnalysisResult):  # type: ignore[no-untyped-def]
        raise NotImplementedError

    def mark_item_failed(self, *, item_id: int) -> None:
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


@pytest.fixture()
def configured_env(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    vault_path = tmp_path / "vault"
    vault_path.mkdir(parents=True)

    monkeypatch.setenv("OBSIDIAN_VAULT_PATH", str(vault_path))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-bot-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "test-chat")
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("TOPICS", json.dumps(["agents", "ml-systems"]))
    monkeypatch.setenv(
        "SOURCES",
        json.dumps(
            {
                "hn": {"rss_urls": ["https://news.ycombinator.com/rss"]},
                "rss": {"feeds": ["https://example.com/feed.xml"]},
            }
        ),
    )

    return tmp_path


def _build_runtime() -> tuple[Settings, Repository]:
    settings = Settings()  # pyright: ignore[reportCallIssue]
    repository = Repository(db_path=settings.recoleta_db_path)
    repository.init_schema()
    return settings, repository


def test_settings_loads_nested_source_configuration(configured_env) -> None:
    settings = Settings()  # pyright: ignore[reportCallIssue]

    assert settings.sources.hn.rss_urls == ["https://news.ycombinator.com/rss"]
    assert settings.sources.rss.feeds == ["https://example.com/feed.xml"]
    assert settings.topics == ["agents", "ml-systems"]


def test_ingest_is_idempotent_by_canonical_url_hash(configured_env) -> None:
    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    same_url = "https://example.com/research-item"
    draft_a = ItemDraft.from_values(
        source="rss",
        source_item_id=None,
        canonical_url=same_url,
        title="Research Item A",
        authors=["Alice"],
        raw_metadata={"feed": "example"},
    )
    draft_b = ItemDraft.from_values(
        source="rss",
        source_item_id=None,
        canonical_url=same_url,
        title="Research Item A (updated title)",
        authors=["Alice", "Bob"],
        raw_metadata={"feed": "example"},
    )

    result = service.ingest(run_id="run-ingest-idempotent", drafts=[draft_a, draft_b])

    assert result.inserted == 1
    assert result.updated == 1
    assert repository.count_items() == 1


def test_ingest_deduplicates_near_duplicate_titles_by_merging_alternate_urls(configured_env) -> None:
    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    draft_a = ItemDraft.from_values(
        source="rss",
        source_item_id=None,
        canonical_url="https://example.com/deep-learning-for-agents",
        title="Deep Learning for Agents",
        authors=["Alice"],
        raw_metadata={"feed": "example"},
    )
    draft_b = ItemDraft.from_values(
        source="hn",
        source_item_id="item-b",
        canonical_url="https://news.ycombinator.com/item?id=123",
        title="Deep Learning for Agents survey",
        authors=["Alice"],
        raw_metadata={"feed": "hn"},
    )

    result = service.ingest(run_id="run-ingest-title-dedup", drafts=[draft_a, draft_b])

    assert result.inserted == 1
    assert result.updated == 1
    assert repository.count_items() == 1

    with Session(repository.engine) as session:
        item = session.exec(select(Item)).one()
        assert item.source == "rss"
        assert item.source_item_id is None
        metadata = json.loads(item.raw_metadata_json)
        assert "alternate_urls" in metadata
        assert "https://news.ycombinator.com/item?id=123" in metadata["alternate_urls"]


def test_ingest_does_not_regress_state_for_analyzed_items(configured_env) -> None:
    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    url = "https://example.com/already-analyzed"
    draft_a = ItemDraft.from_values(
        source="rss",
        source_item_id=None,
        canonical_url=url,
        title="Initial Title",
        authors=["Alice"],
        raw_metadata={"feed": "example"},
    )
    service.ingest(run_id="run-ingest-state", drafts=[draft_a])
    analyzed = service.analyze(run_id="run-ingest-state", limit=10)
    assert analyzed.processed == 1

    with Session(repository.engine) as session:
        item = session.exec(select(Item)).one()
        assert item.state == ITEM_STATE_ANALYZED

    draft_b = ItemDraft.from_values(
        source="rss",
        source_item_id=None,
        canonical_url=url,
        title="Updated Title",
        authors=["Alice", "Bob"],
        raw_metadata={"feed": "example"},
    )
    service.ingest(run_id="run-ingest-state-2", drafts=[draft_b])

    # The item should not be queued for analysis again just because metadata changed.
    analyzed_again = service.analyze(run_id="run-ingest-state-3", limit=10)
    assert analyzed_again.processed == 0

    with Session(repository.engine) as session:
        item = session.exec(select(Item)).one()
        assert item.state == ITEM_STATE_ANALYZED


def test_ingest_writes_debug_artifact_on_repository_failure(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    vault_path = tmp_path / "vault"
    vault_path.mkdir(parents=True)
    artifacts_dir = tmp_path / "artifacts"

    monkeypatch.setenv("OBSIDIAN_VAULT_PATH", str(vault_path))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-bot-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "test-chat")
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("TOPICS", json.dumps(["agents"]))
    monkeypatch.setenv("SOURCES", json.dumps({"rss": {"feeds": []}}))
    monkeypatch.setenv("WRITE_DEBUG_ARTIFACTS", "true")
    monkeypatch.setenv("ARTIFACTS_DIR", str(artifacts_dir))

    settings = Settings()  # pyright: ignore[reportCallIssue]
    repository = ExplodingRepository()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="exploding-1",
        canonical_url="https://example.com/exploding",
        title="Exploding Item",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    result = service.ingest(run_id="run-ingest-exploding", drafts=[draft])

    assert result.failed == 1
    assert len(repository.artifacts) == 1
    recorded_run_id, recorded_item_id, recorded_kind, recorded_path = repository.artifacts[0]
    assert recorded_run_id == "run-ingest-exploding"
    assert recorded_item_id is None
    assert recorded_kind == "error_context"
    assert Path(recorded_path).exists()


def test_analyze_failure_emits_failure_metric(configured_env) -> None:
    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(should_fail=True),
        telegram_sender=FakeTelegramSender(),
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="item-1",
        canonical_url="https://example.com/failure-case",
        title="Failure Case",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.ingest(run_id="run-analyze-failure", drafts=[draft])
    analyze_result = service.analyze(run_id="run-analyze-failure", limit=10)

    metrics = repository.list_metrics(run_id="run-analyze-failure")
    failed_metric = [metric for metric in metrics if metric.name == "pipeline.analyze.failed_total"]

    assert analyze_result.failed == 1
    assert len(failed_metric) == 1
    assert failed_metric[0].value == 1


def test_publish_writes_note_and_prevents_duplicate_delivery(configured_env) -> None:
    settings, repository = _build_runtime()
    sender = FakeTelegramSender()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=sender,
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="item-publish-1",
        canonical_url="https://example.com/publish-case",
        title="Publish Case",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.ingest(run_id="run-publish", drafts=[draft])
    service.analyze(run_id="run-publish", limit=10)

    first_publish = service.publish(run_id="run-publish", limit=10)
    second_publish = service.publish(run_id="run-publish-second", limit=10)

    assert first_publish.sent == 1
    assert second_publish.sent == 0
    assert len(sender.messages) == 1
    assert first_publish.note_paths[0].exists()


def test_publish_retries_after_failed_delivery(configured_env) -> None:
    settings, repository = _build_runtime()
    sender = FlakyTelegramSender()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=sender,
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="item-publish-retry-1",
        canonical_url="https://example.com/publish-retry-case",
        title="Publish Retry Case",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.ingest(run_id="run-publish-retry", drafts=[draft])
    service.analyze(run_id="run-publish-retry", limit=10)

    first_publish = service.publish(run_id="run-publish-retry", limit=10)
    second_publish = service.publish(run_id="run-publish-retry-2", limit=10)

    assert first_publish.sent == 0
    assert first_publish.failed == 1
    assert second_publish.sent == 1
    assert second_publish.failed == 0
    assert len(sender.messages) == 1

    with Session(repository.engine) as session:
        deliveries = list(
            session.exec(
                select(Delivery).where(
                    Delivery.channel == DELIVERY_CHANNEL_TELEGRAM,
                )
            )
        )
        assert len(deliveries) == 1
        assert deliveries[0].status == DELIVERY_STATUS_SENT
        assert deliveries[0].message_id is not None


def test_publish_sanitizes_secrets_in_delivery_error(configured_env) -> None:
    from recoleta.observability import mask_value

    settings, repository = _build_runtime()

    class ExplodingTelegramSender:
        def send(self, text: str) -> str:  # noqa: ARG002
            raise RuntimeError(f"token={settings.telegram_bot_token.get_secret_value()} chat={settings.telegram_chat_id.get_secret_value()}")

    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=ExplodingTelegramSender(),
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="item-publish-sanitize-1",
        canonical_url="https://example.com/publish-sanitize-case",
        title="Publish Sanitize Case",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.ingest(run_id="run-publish-sanitize", drafts=[draft])
    service.analyze(run_id="run-publish-sanitize", limit=10)
    publish_result = service.publish(run_id="run-publish-sanitize", limit=10)

    assert publish_result.failed == 1

    with Session(repository.engine) as session:
        delivery = session.exec(select(Delivery)).one()
        assert settings.telegram_bot_token.get_secret_value() not in (delivery.error or "")
        assert settings.telegram_chat_id.get_secret_value() not in (delivery.error or "")
        assert mask_value(settings.telegram_bot_token.get_secret_value()) in (delivery.error or "")
        assert mask_value(settings.telegram_chat_id.get_secret_value()) in (delivery.error or "")


def test_publish_does_not_crash_when_debug_artifact_write_fails(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from recoleta.observability import mask_value

    tmp_path = configured_env
    bad_artifacts_dir = tmp_path / "bad-artifacts"
    bad_artifacts_dir.write_text("not-a-dir", encoding="utf-8")

    monkeypatch.setenv("WRITE_DEBUG_ARTIFACTS", "true")
    monkeypatch.setenv("ARTIFACTS_DIR", str(bad_artifacts_dir))

    settings, repository = _build_runtime()

    class ExplodingTelegramSender:
        def send(self, text: str) -> str:  # noqa: ARG002
            raise RuntimeError(
                f"token={settings.telegram_bot_token.get_secret_value()} chat={settings.telegram_chat_id.get_secret_value()}"
            )

    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=ExplodingTelegramSender(),
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="item-publish-artifact-failure-1",
        canonical_url="https://example.com/publish-artifact-failure-case",
        title="Publish Artifact Failure Case",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.ingest(run_id="run-publish-artifact-failure", drafts=[draft])
    service.analyze(run_id="run-publish-artifact-failure", limit=10)
    publish_result = service.publish(run_id="run-publish-artifact-failure", limit=10)

    assert publish_result.failed == 1

    with Session(repository.engine) as session:
        delivery = session.exec(select(Delivery)).one()
        assert settings.telegram_bot_token.get_secret_value() not in (delivery.error or "")
        assert settings.telegram_chat_id.get_secret_value() not in (delivery.error or "")
        assert mask_value(settings.telegram_bot_token.get_secret_value()) in (delivery.error or "")
        assert mask_value(settings.telegram_chat_id.get_secret_value()) in (delivery.error or "")


@respx.mock
def test_fetch_rss_drafts_fetches_via_httpx_and_parses_feed() -> None:
    rss_xml = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Example Feed</title>
    <item>
      <title>Hello World</title>
      <link>https://example.com/hello</link>
      <guid>guid-hello</guid>
      <pubDate>Mon, 20 Jan 2025 10:00:00 GMT</pubDate>
      <author>Alice</author>
    </item>
  </channel>
</rss>
"""
    respx.get("https://example.com/feed.xml").respond(
        200,
        text=rss_xml,
        headers={"Content-Type": "application/rss+xml; charset=utf-8"},
    )
    drafts = fetch_rss_drafts(feed_urls=["https://example.com/feed.xml"], source="rss", max_items_per_feed=10)
    assert len(drafts) == 1
    assert drafts[0].canonical_url == "https://example.com/hello"
    assert drafts[0].title == "Hello World"
    assert drafts[0].source_item_id == "guid-hello"
    assert drafts[0].raw_metadata["feed_title"] == "Example Feed"
