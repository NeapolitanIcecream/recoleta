from __future__ import annotations

import json
from pathlib import Path

import pytest
from sqlmodel import Session, select

from recoleta.config import Settings
from recoleta.models import ITEM_STATE_ANALYZED, Item
from recoleta.pipeline import PipelineService
from recoleta.types import ItemDraft
from tests.spec_support import ExplodingRepository, FakeAnalyzer, FakeTelegramSender, _build_runtime

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
