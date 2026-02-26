from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

import pytest
import respx
from huggingface_hub import HfApi
from sqlmodel import Session, select

from recoleta.config import Settings
from recoleta.models import (
    DELIVERY_CHANNEL_TELEGRAM,
    DELIVERY_STATUS_SENT,
    ITEM_STATE_ANALYZED,
    ITEM_STATE_RETRYABLE_FAILED,
    Artifact,
    Content,
    Delivery,
    Item,
    Metric,
)
from recoleta.pipeline import PipelineService
from recoleta.sources import fetch_hf_daily_papers_drafts, fetch_rss_drafts
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


@pytest.fixture()
def configured_env(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    vault_path = tmp_path / "vault"
    vault_path.mkdir(parents=True)

    monkeypatch.setenv("OBSIDIAN_VAULT_PATH", str(vault_path))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-bot-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "test-chat")
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("PUBLISH_TARGETS", json.dumps(["obsidian", "telegram"]))
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


def test_settings_loads_without_obsidian_or_telegram_when_markdown_only(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.delenv("OBSIDIAN_VAULT_PATH", raising=False)
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)

    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("PUBLISH_TARGETS", "markdown")

    settings = Settings()  # pyright: ignore[reportCallIssue]
    assert settings.obsidian_vault_path is None
    assert settings.telegram_bot_token is None
    assert settings.telegram_chat_id is None
    assert settings.publish_targets == ["markdown"]


@pytest.fixture(autouse=True)
def mock_item_html_enrichment(respx_mock: respx.Router, monkeypatch: pytest.MonkeyPatch) -> None:
    respx_mock.get(host="example.com", path__regex=r"^/(?!feed\.xml$).*").respond(
        200,
        text="<html><body><p>mock html</p></body></html>",
        headers={"Content-Type": "text/html; charset=utf-8"},
    )

    import recoleta.pipeline as pipeline

    monkeypatch.setattr(pipeline, "extract_html_maintext", lambda html: "mock maintext")  # noqa: ARG005


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


def test_settings_loads_sources_from_yaml_env_string(configured_env, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(
        "SOURCES",
        "\n".join(
            [
                "hn:",
                "  rss_urls:",
                "    - https://news.ycombinator.com/rss",
                "rss:",
                "  feeds:",
                "    - https://example.com/feed.xml",
            ]
        ),
    )
    settings = Settings()  # pyright: ignore[reportCallIssue]
    assert settings.sources.hn.rss_urls == ["https://news.ycombinator.com/rss"]
    assert settings.sources.rss.feeds == ["https://example.com/feed.xml"]


def test_settings_loads_topics_from_yaml_env_string(configured_env, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TOPICS", "\n".join(["- agents", "- ml-systems"]))
    settings = Settings()  # pyright: ignore[reportCallIssue]
    assert settings.topics == ["agents", "ml-systems"]


def test_settings_loads_allow_and_deny_tags_from_env_strings(configured_env, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ALLOW_TAGS", "agents, ml-systems")
    monkeypatch.setenv("DENY_TAGS", json.dumps(["crypto"]))
    settings = Settings()  # pyright: ignore[reportCallIssue]
    assert settings.allow_tags == ["agents", "ml-systems"]
    assert settings.deny_tags == ["crypto"]


def test_settings_loads_llm_output_language_from_env(configured_env, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LLM_OUTPUT_LANGUAGE", "  zh-CN  ")
    settings = Settings()  # pyright: ignore[reportCallIssue]
    assert settings.llm_output_language == "zh-CN"


def test_settings_rejects_multiline_llm_output_language(configured_env, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LLM_OUTPUT_LANGUAGE", "zh\nCN")
    with pytest.raises(ValueError, match="single-line"):
        Settings()  # pyright: ignore[reportCallIssue]


def test_settings_loads_from_config_file_and_env(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    vault_path = tmp_path / "vault"
    vault_path.mkdir(parents=True)
    config_path = tmp_path / "recoleta.yaml"
    config_path.write_text(
        "\n".join(
            [
                f'OBSIDIAN_VAULT_PATH: "{vault_path}"',
                f'RECOLETA_DB_PATH: "{tmp_path / "recoleta.db"}"',
                'LLM_MODEL: "openai/gpt-4o-mini"',
                "TOPICS:",
                "  - agents",
                "SOURCES:",
                "  rss:",
                "    feeds:",
                "      - https://example.com/feed.xml",
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.setenv("RECOLETA_CONFIG_PATH", str(config_path))
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-bot-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "test-chat")

    settings = Settings()  # pyright: ignore[reportCallIssue]
    assert settings.obsidian_vault_path == vault_path.resolve()
    assert settings.recoleta_db_path == (tmp_path / "recoleta.db").resolve()
    assert settings.llm_model == "openai/gpt-4o-mini"
    assert settings.topics == ["agents"]
    assert settings.sources.rss.feeds == ["https://example.com/feed.xml"]


def test_settings_loads_llm_output_language_from_config_file(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    vault_path = tmp_path / "vault"
    vault_path.mkdir(parents=True)
    config_path = tmp_path / "recoleta.yaml"
    config_path.write_text(
        "\n".join(
            [
                f'OBSIDIAN_VAULT_PATH: "{vault_path}"',
                f'RECOLETA_DB_PATH: "{tmp_path / "recoleta.db"}"',
                'LLM_MODEL: "openai/gpt-4o-mini"',
                'LLM_OUTPUT_LANGUAGE: "Chinese (Simplified)"',
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.setenv("RECOLETA_CONFIG_PATH", str(config_path))
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-bot-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "test-chat")

    settings = Settings()  # pyright: ignore[reportCallIssue]
    assert settings.llm_output_language == "Chinese (Simplified)"


def test_settings_loads_from_config_file_via_init_arg(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    vault_path = tmp_path / "vault"
    vault_path.mkdir(parents=True)
    config_path = tmp_path / "recoleta.yaml"
    config_path.write_text(
        "\n".join(
            [
                f'OBSIDIAN_VAULT_PATH: "{vault_path}"',
                f'RECOLETA_DB_PATH: "{tmp_path / "recoleta.db"}"',
                'LLM_MODEL: "openai/gpt-4o-mini"',
                "TOPICS:",
                "  - agents",
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.delenv("RECOLETA_CONFIG_PATH", raising=False)
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-bot-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "test-chat")

    settings = Settings(config_path=config_path)  # pyright: ignore[reportCallIssue]
    assert settings.obsidian_vault_path == vault_path.resolve()
    assert settings.recoleta_db_path == (tmp_path / "recoleta.db").resolve()
    assert settings.llm_model == "openai/gpt-4o-mini"
    assert settings.topics == ["agents"]


def test_settings_env_overrides_config_file(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    vault_path = tmp_path / "vault"
    vault_path.mkdir(parents=True)
    config_path = tmp_path / "recoleta.json"
    config_path.write_text(
        json.dumps(
            {
                "OBSIDIAN_VAULT_PATH": str(vault_path),
                "RECOLETA_DB_PATH": str(tmp_path / "recoleta.db"),
                "LLM_MODEL": "openai/gpt-4o-mini",
                "OBSIDIAN_BASE_FOLDER": "FromConfig",
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setenv("RECOLETA_CONFIG_PATH", str(config_path))
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-bot-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "test-chat")
    monkeypatch.setenv("OBSIDIAN_BASE_FOLDER", "FromEnv")

    settings = Settings()  # pyright: ignore[reportCallIssue]
    assert settings.obsidian_base_folder == "FromEnv"


def test_settings_rejects_secrets_in_config_file(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    vault_path = tmp_path / "vault"
    vault_path.mkdir(parents=True)
    config_path = tmp_path / "recoleta.yaml"
    config_path.write_text(
        "\n".join(
            [
                f'OBSIDIAN_VAULT_PATH: "{vault_path}"',
                f'RECOLETA_DB_PATH: "{tmp_path / "recoleta.db"}"',
                'LLM_MODEL: "openai/gpt-4o-mini"',
                'TELEGRAM_BOT_TOKEN: "do-not-allow"',
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.setenv("RECOLETA_CONFIG_PATH", str(config_path))
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-bot-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "test-chat")

    with pytest.raises(ValueError, match="Secrets must come from environment variables only"):
        Settings()  # pyright: ignore[reportCallIssue]


def test_settings_requires_artifacts_dir_when_debug_artifacts_enabled(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    vault_path = tmp_path / "vault"
    vault_path.mkdir(parents=True)

    monkeypatch.setenv("OBSIDIAN_VAULT_PATH", str(vault_path))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-bot-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "test-chat")
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("WRITE_DEBUG_ARTIFACTS", "true")
    monkeypatch.delenv("ARTIFACTS_DIR", raising=False)

    with pytest.raises(ValueError, match=r"ARTIFACTS_DIR.*WRITE_DEBUG_ARTIFACTS"):
        Settings()  # pyright: ignore[reportCallIssue]


def test_ingest_pulls_all_configured_sources_without_network(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    vault_path = tmp_path / "vault"
    vault_path.mkdir(parents=True)

    monkeypatch.setenv("OBSIDIAN_VAULT_PATH", str(vault_path))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-bot-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "test-chat")
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("TOPICS", json.dumps(["agents"]))
    monkeypatch.setenv(
        "SOURCES",
        json.dumps(
            {
                "hn": {"rss_urls": []},
                "rss": {"feeds": []},
                "arxiv": {"queries": ["cat:cs.AI"], "max_results_per_run": 10},
                "openreview": {"venues": ["NeurIPS.cc/2026/Conference"]},
                "hf_daily": {"enabled": True},
            }
        ),
    )

    import recoleta.sources as source_connectors

    draft_arxiv = ItemDraft.from_values(
        source="arxiv",
        source_item_id="arxiv-1",
        canonical_url="https://arxiv.org/abs/1605.08386v1",
        title="Arxiv Item",
    )
    draft_openreview = ItemDraft.from_values(
        source="openreview",
        source_item_id="openreview-1",
        canonical_url="https://openreview.net/forum?id=openreview-1",
        title="OpenReview Item",
    )
    draft_hf = ItemDraft.from_values(
        source="hf_daily",
        source_item_id="papers/1",
        canonical_url="https://huggingface.co/papers/1",
        title="HF Daily Item",
    )

    monkeypatch.setattr(source_connectors, "fetch_arxiv_drafts", lambda **_: [draft_arxiv])
    monkeypatch.setattr(source_connectors, "fetch_openreview_drafts", lambda **_: [draft_openreview])
    monkeypatch.setattr(source_connectors, "fetch_hf_daily_papers_drafts", lambda **_: [draft_hf])

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    result = service.ingest(run_id="run-ingest-sources")
    assert result.inserted == 3
    assert repository.count_items() == 3


def test_ingest_does_not_crash_on_source_failure_and_records_metric(configured_env, monkeypatch: pytest.MonkeyPatch) -> None:
    import recoleta.sources as source_connectors

    settings, repository = _build_runtime()

    draft_rss = ItemDraft.from_values(
        source="rss",
        source_item_id="rss-1",
        canonical_url="https://example.com/source-failure-ok",
        title="Source Failure Still Ingests",
    )

    def fake_fetch_rss_drafts(*, feed_urls: list[str], source: str, max_items_per_feed: int = 50) -> list[ItemDraft]:  # noqa: ARG001
        if source == "hn":
            raise RuntimeError("simulated HN connector failure")
        return [draft_rss]

    monkeypatch.setattr(source_connectors, "fetch_rss_drafts", fake_fetch_rss_drafts)

    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    result = service.ingest(run_id="run-ingest-source-failure")
    assert result.inserted == 1

    metrics = repository.list_metrics(run_id="run-ingest-source-failure")
    source_failures = [metric for metric in metrics if metric.name == "pipeline.ingest.source_failures_total"]
    assert len(source_failures) == 1
    assert source_failures[0].value == 1


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
    assert (artifacts_dir / recorded_path).exists()


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


def test_analyze_marks_retryable_enrich_failures_and_allows_retry(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import httpx
    import recoleta.pipeline as pipeline

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="item-retryable-enrich-1",
        canonical_url="https://example.com/retryable-enrich-case",
        title="Retryable Enrich Case",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.ingest(run_id="run-retryable-enrich", drafts=[draft])

    calls = 0

    def flaky_fetch_url_html(_client: httpx.Client, url: str) -> str:
        nonlocal calls
        calls += 1
        if calls == 1:
            request = httpx.Request("GET", url)
            response = httpx.Response(503, request=request, text="service unavailable")
            raise httpx.HTTPStatusError("service unavailable", request=request, response=response)
        return "<html><body><p>mock html</p></body></html>"

    monkeypatch.setattr(pipeline, "fetch_url_html", flaky_fetch_url_html)

    first = service.analyze(run_id="run-retryable-enrich", limit=10)
    assert first.processed == 0
    assert first.failed == 1

    with Session(repository.engine) as session:
        item = session.exec(select(Item)).one()
        assert item.state == ITEM_STATE_RETRYABLE_FAILED

    second = service.analyze(run_id="run-retryable-enrich-2", limit=10)
    assert second.processed == 1
    assert second.failed == 0

    with Session(repository.engine) as session:
        item = session.exec(select(Item)).one()
        assert item.state == ITEM_STATE_ANALYZED


def test_analyze_persists_enriched_content_and_emits_enrich_metrics(configured_env) -> None:
    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="item-enrich-1",
        canonical_url="https://example.com/enrich-case",
        title="Enrich Case",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.ingest(run_id="run-enrich", drafts=[draft])
    analyze_result = service.analyze(run_id="run-enrich", limit=10)

    assert analyze_result.processed == 1

    with Session(repository.engine) as session:
        content = session.exec(select(Content)).one()
        assert content.content_type == "html_maintext"
        assert content.text == "mock maintext"

    metrics = repository.list_metrics(run_id="run-enrich")
    by_name: dict[str, Metric] = {metric.name: metric for metric in metrics}
    assert by_name["pipeline.enrich.processed_total"].value == 1
    assert by_name["pipeline.enrich.skipped_total"].value == 0
    assert by_name["pipeline.enrich.failed_total"].value == 0


def test_analyze_prefers_pdf_enrichment_for_arxiv_items(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import recoleta.pipeline as pipeline

    settings, repository = _build_runtime()

    class CapturingAnalyzer:
        def __init__(self) -> None:
            self.contents: list[str | None] = []

        def analyze(
            self,
            *,
            title: str,
            canonical_url: str,  # noqa: ARG002
            user_topics: list[str],
            content: str | None = None,
            include_debug: bool = False,  # noqa: ARG002
        ) -> tuple[AnalysisResult, AnalyzeDebug | None]:
            self.contents.append(content)
            return (
                AnalysisResult(
                    model="test/fake-model",
                    provider="test",
                    summary=f"Summary for {title}",
                    insight="This matters because it aligns with user interests.",
                    idea_directions=["Try reproducing the approach."],
                    topics=user_topics[:2] or ["general"],
                    relevance_score=0.9,
                    novelty_score=0.4,
                    cost_usd=0.0,
                    latency_ms=1,
                ),
                None,
            )

    analyzer = CapturingAnalyzer()

    expected_pdf_url = "https://arxiv.org/pdf/1605.08386v1.pdf"

    def fake_fetch_url_bytes(_client, url: str) -> bytes:  # noqa: ARG001
        assert url == expected_pdf_url
        return b"%PDF-mock"

    def fail_fetch_url_html(*_args, **_kwargs):  # type: ignore[no-untyped-def]
        raise AssertionError("html fetch should not be used")

    monkeypatch.setattr(pipeline, "fetch_url_bytes", fake_fetch_url_bytes)
    monkeypatch.setattr(pipeline, "extract_pdf_text", lambda _bytes: "mock pdf text")  # noqa: ARG005
    monkeypatch.setattr(pipeline, "fetch_url_html", fail_fetch_url_html)

    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=analyzer,
        telegram_sender=FakeTelegramSender(),
    )
    draft = ItemDraft.from_values(
        source="arxiv",
        source_item_id="1605.08386v1",
        canonical_url="https://arxiv.org/abs/1605.08386v1",
        title="Arxiv PDF Case",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.ingest(run_id="run-pdf-enrich", drafts=[draft])
    analyze_result = service.analyze(run_id="run-pdf-enrich", limit=10)
    assert analyze_result.processed == 1

    assert analyzer.contents == ["mock pdf text"]

    with Session(repository.engine) as session:
        contents = list(session.exec(select(Content).order_by(cast(Any, Content.id))))
        assert contents
        assert any(content.content_type == "pdf_text" and content.text == "mock pdf text" for content in contents)


def test_analyze_writes_llm_request_and_response_artifacts(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    tmp_path = configured_env
    artifacts_dir = tmp_path / "artifacts"

    monkeypatch.setenv("WRITE_DEBUG_ARTIFACTS", "true")
    monkeypatch.setenv("ARTIFACTS_DIR", str(artifacts_dir))

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="item-llm-artifacts-1",
        canonical_url="https://example.com/llm-artifacts-case",
        title="LLM Artifacts Case",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.ingest(run_id="run-llm-artifacts", drafts=[draft])
    analyze_result = service.analyze(run_id="run-llm-artifacts", limit=10)
    assert analyze_result.processed == 1

    with Session(repository.engine) as session:
        artifacts = list(
            session.exec(
                select(Artifact)
                .where(Artifact.run_id == "run-llm-artifacts")
                .order_by(cast(Any, Artifact.id))
            )
        )
        kinds = {artifact.kind for artifact in artifacts}
        assert {"llm_request", "llm_response"}.issubset(kinds)
        for artifact in artifacts:
            assert not Path(artifact.path).is_absolute()
            assert (artifacts_dir / artifact.path).exists()


def test_analyze_sanitizes_debug_artifact_paths(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    tmp_path = configured_env
    artifacts_dir = tmp_path / "artifacts"

    monkeypatch.setenv("WRITE_DEBUG_ARTIFACTS", "true")
    monkeypatch.setenv("ARTIFACTS_DIR", str(artifacts_dir))

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="item-llm-artifacts-2",
        canonical_url="https://example.com/llm-artifacts-case-2",
        title="LLM Artifacts Case 2",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.ingest(run_id="run-llm-artifacts-2", drafts=[draft])

    malicious_run_id = "../run-llm-artifacts-2"
    analyze_result = service.analyze(run_id=malicious_run_id, limit=10)
    assert analyze_result.processed == 1

    base_dir = artifacts_dir.resolve()
    with Session(repository.engine) as session:
        artifacts = list(
            session.exec(
                select(Artifact)
                .where(Artifact.run_id == malicious_run_id)
                .order_by(cast(Any, Artifact.id))
            )
        )
        assert artifacts
        for artifact in artifacts:
            artifact_rel = Path(artifact.path)
            assert ".." not in artifact_rel.parts
            assert not artifact_rel.is_absolute()
            artifact_abs = (artifacts_dir / artifact_rel).resolve()
            assert artifact_abs.is_relative_to(base_dir)
            assert artifact_abs.exists()


def test_pipeline_records_duration_metrics_for_each_stage(configured_env) -> None:
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
        source_item_id="item-durations-1",
        canonical_url="https://example.com/durations-case",
        title="Durations Case",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.ingest(run_id="run-durations", drafts=[draft])
    service.analyze(run_id="run-durations", limit=10)
    service.publish(run_id="run-durations", limit=10)

    metrics = repository.list_metrics(run_id="run-durations")
    metric_names = {metric.name for metric in metrics}
    assert "pipeline.ingest.duration_ms" in metric_names
    assert "pipeline.enrich.duration_ms_total" in metric_names
    assert "pipeline.analyze.duration_ms" in metric_names
    assert "pipeline.publish.duration_ms" in metric_names


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


def test_publish_writes_local_markdown_notes_without_obsidian_or_telegram(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.delenv("OBSIDIAN_VAULT_PATH", raising=False)
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)

    markdown_dir = tmp_path / "markdown-output"
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(markdown_dir))
    monkeypatch.setenv("PUBLISH_TARGETS", "markdown")
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="item-publish-markdown-1",
        canonical_url="https://example.com/publish-markdown-case",
        title="Publish Markdown Case",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.ingest(run_id="run-publish-markdown", drafts=[draft])
    service.analyze(run_id="run-publish-markdown", limit=10)

    result = service.publish(run_id="run-publish-markdown", limit=10)
    assert result.sent == 1
    assert result.failed == 0
    assert result.note_paths and result.note_paths[0].exists()
    assert (markdown_dir / "latest.md").exists()

    latest = (markdown_dir / "latest.md").read_text(encoding="utf-8")
    assert "run-publish-markdown" in latest
    assert "Inbox/" in latest

    with Session(repository.engine) as session:
        assert session.exec(select(Delivery)).first() is None


def test_publish_writes_markdown_index_when_telegram_daily_cap_reached(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.delenv("OBSIDIAN_VAULT_PATH", raising=False)

    markdown_dir = tmp_path / "markdown-output"
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(markdown_dir))
    monkeypatch.setenv("PUBLISH_TARGETS", "markdown,telegram")
    monkeypatch.setenv("MAX_DELIVERIES_PER_DAY", "0")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-bot-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "test-chat")
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")

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
        source_item_id="item-publish-cap-1",
        canonical_url="https://example.com/publish-cap-case",
        title="Publish Cap Case",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.ingest(run_id="run-publish-cap", drafts=[draft])
    service.analyze(run_id="run-publish-cap", limit=10)

    result = service.publish(run_id="run-publish-cap", limit=10)
    assert result.sent == 0
    assert result.failed == 0
    assert len(sender.messages) == 0
    assert (markdown_dir / "latest.md").exists()

    latest = (markdown_dir / "latest.md").read_text(encoding="utf-8")
    assert "run-publish-cap" in latest
    assert "No items published in this run" in latest

    with Session(repository.engine) as session:
        assert session.exec(select(Item).where(Item.state == ITEM_STATE_ANALYZED)).first() is not None
        assert session.exec(select(Delivery)).first() is None


def test_publish_filters_by_allow_tags_and_records_metric(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("ALLOW_TAGS", json.dumps(["non-matching-tag"]))

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
        source_item_id="item-publish-filter-allow-1",
        canonical_url="https://example.com/publish-filter-allow-case",
        title="Publish Filter Allow Case",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.ingest(run_id="run-publish-filter-allow", drafts=[draft])
    service.analyze(run_id="run-publish-filter-allow", limit=10)
    result = service.publish(run_id="run-publish-filter-allow", limit=10)

    assert result.sent == 0
    assert result.skipped == 1
    assert len(sender.messages) == 0

    metrics = repository.list_metrics(run_id="run-publish-filter-allow")
    by_name: dict[str, Metric] = {metric.name: metric for metric in metrics}
    assert by_name["pipeline.publish.filtered_total"].value == 1


def test_publish_filters_by_deny_tags_and_records_metric(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DENY_TAGS", json.dumps(["agents"]))

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
        source_item_id="item-publish-filter-deny-1",
        canonical_url="https://example.com/publish-filter-deny-case",
        title="Publish Filter Deny Case",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.ingest(run_id="run-publish-filter-deny", drafts=[draft])
    service.analyze(run_id="run-publish-filter-deny", limit=10)
    result = service.publish(run_id="run-publish-filter-deny", limit=10)

    assert result.sent == 0
    assert result.skipped == 1
    assert len(sender.messages) == 0

    metrics = repository.list_metrics(run_id="run-publish-filter-deny")
    by_name: dict[str, Metric] = {metric.name: metric for metric in metrics}
    assert by_name["pipeline.publish.filtered_total"].value == 1


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
    assert settings.obsidian_vault_path is not None
    note_dir = settings.obsidian_vault_path / settings.obsidian_base_folder / "Inbox"
    note_paths_after_first = list(note_dir.glob("*.md"))
    assert len(note_paths_after_first) == 1
    first_note_path = note_paths_after_first[0]
    assert first_note_path.exists()
    second_publish = service.publish(run_id="run-publish-retry-2", limit=10)
    note_paths_after_second = list(note_dir.glob("*.md"))
    assert len(note_paths_after_second) == 1
    assert second_publish.note_paths and second_publish.note_paths[0] == first_note_path

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


def test_publish_sanitizes_secrets_in_delivery_error(configured_env, monkeypatch: pytest.MonkeyPatch) -> None:
    from urllib.parse import quote

    from recoleta.observability import mask_value

    settings, repository = _build_runtime()
    assert settings.telegram_bot_token is not None
    assert settings.telegram_chat_id is not None
    token = settings.telegram_bot_token.get_secret_value()
    chat = settings.telegram_chat_id.get_secret_value()
    token_encoded = quote(token, safe="")
    chat_encoded = quote(chat, safe="")
    openai_key = "sk-test-openai-key"
    monkeypatch.setenv("OPENAI_API_KEY", openai_key)
    openai_key_encoded = quote(openai_key, safe="")

    class ExplodingTelegramSender:
        def send(self, text: str) -> str:  # noqa: ARG002
            raise RuntimeError(
                " ".join(
                    [
                        f"token={token}",
                        f"token_encoded={token_encoded}",
                        f"chat={chat}",
                        f"chat_encoded={chat_encoded}",
                        f"openai_key={openai_key}",
                        f"openai_key_encoded={openai_key_encoded}",
                    ]
                )
            )

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
        assert token not in (delivery.error or "")
        assert token_encoded not in (delivery.error or "")
        assert chat not in (delivery.error or "")
        assert chat_encoded not in (delivery.error or "")
        assert openai_key not in (delivery.error or "")
        assert openai_key_encoded not in (delivery.error or "")
        assert mask_value(token) in (delivery.error or "")
        assert mask_value(chat) in (delivery.error or "")
        assert mask_value(openai_key) in (delivery.error or "")


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
    assert settings.telegram_bot_token is not None
    assert settings.telegram_chat_id is not None
    token = settings.telegram_bot_token.get_secret_value()
    chat = settings.telegram_chat_id.get_secret_value()

    class ExplodingTelegramSender:
        def send(self, text: str) -> str:  # noqa: ARG002
            raise RuntimeError(
                f"token={token} chat={chat}"
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
        assert token not in (delivery.error or "")
        assert chat not in (delivery.error or "")
        assert mask_value(token) in (delivery.error or "")
        assert mask_value(chat) in (delivery.error or "")


def test_fetch_rss_drafts_fetches_via_httpx_and_parses_feed(respx_mock: respx.Router) -> None:
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
    respx_mock.get("https://example.com/feed.xml").respond(
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


def test_fetch_hf_daily_papers_drafts_fetches_index_and_parses_items(respx_mock: respx.Router) -> None:
    base_url = HfApi().endpoint.rstrip("/")
    index_url = f"{base_url}/papers"
    html = """<html><body>
<a href="/papers/1">Paper One</a>
<a href="/papers/1">Paper One Duplicate</a>
<a href="/papers/2"> Paper Two </a>
<a href="/models/bert-base-uncased">Not a paper</a>
<a href="/papers/3"></a>
</body></html>"""
    route = respx_mock.get(index_url).respond(
        200,
        text=html,
        headers={"Content-Type": "text/html; charset=utf-8"},
    )
    drafts = fetch_hf_daily_papers_drafts(max_items=2)
    assert route.called
    request_headers = {k.lower() for k in route.calls[0].request.headers.keys()}
    assert "user-agent" in request_headers

    assert [d.source_item_id for d in drafts] == ["papers/1", "papers/2"]
    assert [d.canonical_url for d in drafts] == [
        f"{base_url}/papers/1",
        f"{base_url}/papers/2",
    ]
    assert [d.title for d in drafts] == ["Paper One", "Paper Two"]


def test_fetch_hf_daily_papers_drafts_raises_on_http_error(respx_mock: respx.Router) -> None:
    base_url = HfApi().endpoint.rstrip("/")
    index_url = f"{base_url}/papers"
    import httpx

    respx_mock.get(index_url).respond(
        503,
        text="service unavailable",
        headers={"Content-Type": "text/plain; charset=utf-8"},
    )
    with pytest.raises(httpx.HTTPStatusError):
        fetch_hf_daily_papers_drafts(max_items=10)
