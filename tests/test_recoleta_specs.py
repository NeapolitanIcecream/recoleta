from __future__ import annotations

import json
from pathlib import Path

import pytest

from recoleta.config import Settings
from recoleta.pipeline import PipelineService
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
    settings = Settings()
    repository = Repository(db_path=settings.recoleta_db_path)
    repository.init_schema()
    return settings, repository


def test_settings_loads_nested_source_configuration(configured_env) -> None:
    settings = Settings()

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
