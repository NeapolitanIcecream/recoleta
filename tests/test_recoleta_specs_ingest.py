from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path

import pytest
from sqlmodel import Session, select

from recoleta.config import Settings
from recoleta.models import ITEM_STATE_ANALYZED, Item
from recoleta.pipeline.service import PipelineService
from recoleta.sources import SourcePullResult
from recoleta.types import ItemDraft
from tests.spec_support import (
    ExplodingRepository,
    FakeAnalyzer,
    FakeTelegramSender,
    _build_runtime,
)


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
                "arxiv": {
                    "enabled": True,
                    "queries": ["cat:cs.AI"],
                    "max_results_per_run": 10,
                },
                "openreview": {
                    "enabled": True,
                    "venues": ["NeurIPS.cc/2026/Conference"],
                },
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

    monkeypatch.setattr(
        source_connectors, "fetch_arxiv_drafts", lambda **_: [draft_arxiv]
    )
    monkeypatch.setattr(
        source_connectors, "fetch_openreview_drafts", lambda **_: [draft_openreview]
    )
    monkeypatch.setattr(
        source_connectors, "fetch_hf_daily_papers_drafts", lambda **_: [draft_hf]
    )

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


def test_ingest_passes_configured_source_pull_limits_to_connectors(
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
                "arxiv": {
                    "enabled": True,
                    "queries": ["cat:cs.AI"],
                    "max_results_per_run": 2,
                },
                "hn": {
                    "enabled": True,
                    "rss_urls": ["https://news.ycombinator.com/rss"],
                    "max_items_per_feed": 1,
                },
                "rss": {
                    "enabled": True,
                    "feeds": ["https://jack.example/"],
                    "max_items_per_feed": 3,
                },
                "hf_daily": {"enabled": True, "max_items_per_run": 4},
                "openreview": {
                    "enabled": True,
                    "venues": ["ICLR.cc/2026/Conference"],
                    "max_results_per_venue": 5,
                },
            }
        ),
    )

    import recoleta.sources as source_connectors

    calls: dict[str, object] = {}

    def fake_fetch_hf_daily_papers_drafts(*, max_items: int = 50) -> list[ItemDraft]:
        calls["hf_daily"] = max_items
        return []

    def fake_fetch_rss_drafts(
        *, feed_urls: list[str], source: str, max_items_per_feed: int = 50
    ) -> list[ItemDraft]:
        calls[source] = {
            "feed_urls": list(feed_urls),
            "max_items_per_feed": max_items_per_feed,
        }
        return []

    def fake_fetch_arxiv_drafts(
        *, queries: list[str], max_results_per_run: int = 50
    ) -> list[ItemDraft]:
        calls["arxiv"] = {
            "queries": list(queries),
            "max_results_per_run": max_results_per_run,
        }
        return []

    def fake_fetch_openreview_drafts(
        *, venues: list[str], max_results_per_venue: int = 50
    ) -> list[ItemDraft]:
        calls["openreview"] = {
            "venues": list(venues),
            "max_results_per_venue": max_results_per_venue,
        }
        return []

    monkeypatch.setattr(
        source_connectors,
        "fetch_hf_daily_papers_drafts",
        fake_fetch_hf_daily_papers_drafts,
    )
    monkeypatch.setattr(source_connectors, "fetch_rss_drafts", fake_fetch_rss_drafts)
    monkeypatch.setattr(
        source_connectors, "fetch_arxiv_drafts", fake_fetch_arxiv_drafts
    )
    monkeypatch.setattr(
        source_connectors, "fetch_openreview_drafts", fake_fetch_openreview_drafts
    )

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    result = service.ingest(run_id="run-ingest-source-limits")

    assert result.inserted == 0
    assert calls["hf_daily"] == 4
    assert calls["hn"] == {
        "feed_urls": ["https://news.ycombinator.com/rss"],
        "max_items_per_feed": 1,
    }
    assert calls["rss"] == {
        "feed_urls": ["https://jack.example/"],
        "max_items_per_feed": 3,
    }
    assert calls["arxiv"] == {
        "queries": ["cat:cs.AI"],
        "max_results_per_run": 2,
    }
    assert calls["openreview"] == {
        "venues": ["ICLR.cc/2026/Conference"],
        "max_results_per_venue": 5,
    }


def test_ingest_passes_target_period_to_connectors(
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
                "arxiv": {
                    "enabled": True,
                    "queries": ["cat:cs.AI"],
                },
                "hn": {
                    "enabled": True,
                    "rss_urls": ["https://news.ycombinator.com/rss"],
                },
                "rss": {
                    "enabled": True,
                    "feeds": ["https://jack.example/"],
                },
                "hf_daily": {"enabled": True},
                "openreview": {
                    "enabled": True,
                    "venues": ["ICLR.cc/2026/Conference"],
                },
            }
        ),
    )

    import recoleta.sources as source_connectors

    calls: dict[str, dict[str, object]] = {}

    def fake_fetch_hf_daily_papers_drafts(
        *,
        max_items: int = 50,
        period_start=None,
        period_end=None,  # noqa: ANN001
    ) -> list[ItemDraft]:
        calls["hf_daily"] = {
            "max_items": max_items,
            "period_start": period_start,
            "period_end": period_end,
        }
        return []

    def fake_fetch_rss_drafts(
        *,
        feed_urls: list[str],
        source: str,
        max_items_per_feed: int = 50,
        period_start=None,  # noqa: ANN001
        period_end=None,  # noqa: ANN001
    ) -> list[ItemDraft]:
        calls[source] = {
            "feed_urls": list(feed_urls),
            "max_items_per_feed": max_items_per_feed,
            "period_start": period_start,
            "period_end": period_end,
        }
        return []

    def fake_fetch_arxiv_drafts(
        *,
        queries: list[str],
        max_results_per_run: int = 50,
        period_start=None,  # noqa: ANN001
        period_end=None,  # noqa: ANN001
    ) -> list[ItemDraft]:
        calls["arxiv"] = {
            "queries": list(queries),
            "max_results_per_run": max_results_per_run,
            "period_start": period_start,
            "period_end": period_end,
        }
        return []

    def fake_fetch_openreview_drafts(
        *,
        venues: list[str],
        max_results_per_venue: int = 50,
        period_start=None,  # noqa: ANN001
        period_end=None,  # noqa: ANN001
    ) -> list[ItemDraft]:
        calls["openreview"] = {
            "venues": list(venues),
            "max_results_per_venue": max_results_per_venue,
            "period_start": period_start,
            "period_end": period_end,
        }
        return []

    monkeypatch.setattr(
        source_connectors,
        "fetch_hf_daily_papers_drafts",
        fake_fetch_hf_daily_papers_drafts,
    )
    monkeypatch.setattr(source_connectors, "fetch_rss_drafts", fake_fetch_rss_drafts)
    monkeypatch.setattr(
        source_connectors, "fetch_arxiv_drafts", fake_fetch_arxiv_drafts
    )
    monkeypatch.setattr(
        source_connectors, "fetch_openreview_drafts", fake_fetch_openreview_drafts
    )

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    period_start = datetime(2025, 1, 20, tzinfo=UTC)
    period_end = datetime(2025, 1, 21, tzinfo=UTC)

    service.ingest(
        run_id="run-ingest-source-window",
        period_start=period_start,
        period_end=period_end,
    )

    assert calls["hf_daily"]["period_start"] == period_start
    assert calls["hf_daily"]["period_end"] == period_end
    assert calls["hn"]["period_start"] == period_start
    assert calls["hn"]["period_end"] == period_end
    assert calls["rss"]["period_start"] == period_start
    assert calls["rss"]["period_end"] == period_end
    assert calls["arxiv"]["period_start"] == period_start
    assert calls["arxiv"]["period_end"] == period_end
    assert calls["openreview"]["period_start"] == period_start
    assert calls["openreview"]["period_end"] == period_end


def test_ingest_does_not_crash_on_source_failure_and_records_metric(
    configured_env, monkeypatch: pytest.MonkeyPatch
) -> None:
    import recoleta.sources as source_connectors

    settings, repository = _build_runtime()

    draft_rss = ItemDraft.from_values(
        source="rss",
        source_item_id="rss-1",
        canonical_url="https://example.com/source-failure-ok",
        title="Source Failure Still Ingests",
    )

    def fake_fetch_rss_drafts(
        *, feed_urls: list[str], source: str, max_items_per_feed: int = 50
    ) -> list[ItemDraft]:  # noqa: ARG001
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
    source_failures = [
        metric
        for metric in metrics
        if metric.name == "pipeline.ingest.source_failures_total"
    ]
    assert len(source_failures) == 1
    assert source_failures[0].value == 1
    by_name = {metric.name: metric for metric in metrics}
    assert by_name["pipeline.ingest.source.hn.pull_failed_total"].value == 1
    assert by_name["pipeline.ingest.source.hn.drafts_total"].value == 0
    assert by_name["pipeline.ingest.source.rss.pull_failed_total"].value == 0
    assert by_name["pipeline.ingest.source.rss.drafts_total"].value == 1


def test_ingest_records_source_window_diagnostics(
    configured_env, monkeypatch: pytest.MonkeyPatch
) -> None:
    import recoleta.sources as source_connectors

    monkeypatch.setenv(
        "SOURCES",
        json.dumps(
            {
                "arxiv": {
                    "enabled": True,
                    "queries": ["cat:cs.AI"],
                }
            }
        ),
    )

    draft = ItemDraft.from_values(
        source="arxiv",
        source_item_id="arxiv-1",
        canonical_url="https://arxiv.org/abs/1605.08386",
        title="Windowed Item",
        published_at=datetime(2025, 1, 20, 12, tzinfo=UTC),
    )

    monkeypatch.setattr(
        source_connectors,
        "fetch_arxiv_drafts",
        lambda **_: SourcePullResult(
            drafts=[draft],
            filtered_out_total=7,
            in_window_total=1,
            missing_published_at_total=2,
        ),
    )

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    result = service.ingest(run_id="run-ingest-window-diagnostics")

    assert result.inserted == 1

    metrics = repository.list_metrics(run_id="run-ingest-window-diagnostics")
    by_name = {metric.name: metric for metric in metrics}
    assert by_name["pipeline.ingest.source.arxiv.filtered_out_total"].value == 7
    assert by_name["pipeline.ingest.source.arxiv.in_window_total"].value == 1
    assert by_name["pipeline.ingest.source.arxiv.missing_published_at_total"].value == 2
    assert by_name["pipeline.ingest.source.arxiv.inserted_total"].value == 1


def test_ingest_progress_starts_before_source_pull_and_sets_total(
    configured_env, monkeypatch: pytest.MonkeyPatch
) -> None:
    import recoleta.pipeline as pipeline_module
    import recoleta.sources as source_connectors

    timeline: list[str] = []
    progress_updates: list[dict[str, object]] = []
    progress_columns: list[str] = []

    class FakeProgress:
        def __init__(self, *columns, **kwargs) -> None:  # noqa: ANN002, ANN003
            timeline.append("progress_init")
            progress_columns.extend(type(column).__name__ for column in columns)

        def __enter__(self) -> "FakeProgress":
            timeline.append("progress_enter")
            return self

        def __exit__(self, exc_type, exc, tb) -> None:  # noqa: ANN001, ANN201
            timeline.append("progress_exit")

        def add_task(self, description: str, total: int | None = None, **kwargs) -> int:  # noqa: ANN003
            timeline.append("progress_add_task")
            progress_updates.append({"description": description, "total": total})
            return 1

        def update(self, task_id: int, **kwargs) -> None:  # noqa: ANN003
            timeline.append("progress_update")
            update_payload: dict[str, object] = {"task_id": task_id}
            update_payload.update(kwargs)
            progress_updates.append(update_payload)

        def advance(self, task_id: int, advance: int = 1) -> None:
            timeline.append("progress_advance")
            progress_updates.append({"task_id": task_id, "advance": advance})

    monkeypatch.setattr(pipeline_module, "Progress", FakeProgress, raising=False)

    def fake_fetch_rss_drafts(
        *, feed_urls: list[str], source: str, max_items_per_feed: int = 50
    ) -> list[ItemDraft]:  # noqa: ARG001
        timeline.append(f"source_pull_{source}")
        return [
            ItemDraft.from_values(
                source=source,
                source_item_id=f"{source}-1",
                canonical_url=f"https://example.com/{source}-1",
                title=f"{source} item",
            )
        ]

    monkeypatch.setattr(source_connectors, "fetch_rss_drafts", fake_fetch_rss_drafts)

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )
    result = service.ingest(run_id="run-ingest-progress-source-pull")

    assert result.inserted == 2
    assert "progress_add_task" in timeline
    first_source_pull_index = min(
        index
        for index, marker in enumerate(timeline)
        if marker.startswith("source_pull_")
    )
    assert timeline.index("progress_add_task") < first_source_pull_index
    assert "TimeElapsedColumn" in progress_columns
    assert {"description": "Ingesting items", "total": None} in progress_updates
    assert any(
        update.get("total") == 2 and update.get("completed") == 0
        for update in progress_updates
        if "total" in update
    )


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


def test_ingest_deduplicates_near_duplicate_titles_by_merging_alternate_urls(
    configured_env,
) -> None:
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
    service.prepare(run_id="run-ingest-state", drafts=[draft_a], limit=10)
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


def test_ingest_preserves_existing_published_at_when_update_omits_it(
    configured_env,
) -> None:
    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    original_published_at = datetime(2025, 1, 20, 8, tzinfo=UTC)
    draft_a = ItemDraft.from_values(
        source="rss",
        source_item_id="published-preserve",
        canonical_url="https://example.com/published-preserve",
        title="Published Preserve",
        published_at=original_published_at,
        raw_metadata={"matched_feed_urls": ["https://feed-a.example/rss.xml"]},
    )
    draft_b = ItemDraft.from_values(
        source="rss",
        source_item_id="published-preserve",
        canonical_url="https://example.com/published-preserve",
        title="Published Preserve Updated",
        published_at=None,
        raw_metadata={"matched_feed_urls": ["https://feed-b.example/rss.xml"]},
    )

    service.ingest(run_id="run-published-preserve-1", drafts=[draft_a])
    service.ingest(run_id="run-published-preserve-2", drafts=[draft_b])

    with Session(repository.engine) as session:
        item = session.exec(
            select(Item).where(Item.source_item_id == "published-preserve")
        ).one()
        assert item.published_at == original_published_at.replace(tzinfo=None)
        metadata = json.loads(item.raw_metadata_json)
        assert metadata["matched_feed_urls"] == [
            "https://feed-a.example/rss.xml",
            "https://feed-b.example/rss.xml",
        ]


def test_ingest_writes_debug_artifact_on_repository_failure(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    vault_path = tmp_path / "vault"
    vault_path.mkdir(parents=True)
    artifacts_dir = tmp_path / "artifacts"

    monkeypatch.setenv("OBSIDIAN_VAULT_PATH", str(vault_path))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-bot-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "test-chat")
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("TOPICS", json.dumps(["agents"]))
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
    recorded_run_id, recorded_item_id, recorded_kind, recorded_path = (
        repository.artifacts[0]
    )
    assert recorded_run_id == "run-ingest-exploding"
    assert recorded_item_id is None
    assert recorded_kind == "error_context"
    assert (artifacts_dir / recorded_path).exists()
