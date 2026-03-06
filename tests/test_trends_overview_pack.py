from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from recoleta.pipeline import PipelineService
from recoleta.trends import (
    TrendGenerationPlan,
    build_overview_pack_md,
    day_period_bounds,
    week_period_bounds,
)
from recoleta.types import ItemDraft
from tests.spec_support import FakeAnalyzer, FakeTelegramSender, _build_runtime


def test_overview_pack_week_includes_7_day_entries_with_placeholders(
    configured_env,
) -> None:
    _ = configured_env
    _, repository = _build_runtime()

    anchor = datetime(2026, 3, 2, tzinfo=UTC).date()  # Monday
    week_start, week_end = week_period_bounds(anchor)
    plan = TrendGenerationPlan(
        target_granularity="week", period_start=week_start, period_end=week_end
    )
    assert plan.overview_pack_strategy == "trend_overviews"
    assert plan.prev_level == "day"

    # Only create 2 out of 7 daily trend docs to force placeholders.
    for offset_days in (0, 3):
        day_start = week_start + timedelta(days=offset_days)
        day_end = day_start + timedelta(days=1)
        doc = repository.upsert_document_for_trend(
            granularity="day",
            period_start=day_start,
            period_end=day_end,
            title=f"Day {offset_days}",
        )
        assert doc.id is not None
        repository.upsert_document_chunk(
            doc_id=int(doc.id),
            chunk_index=0,
            kind="summary",
            text_value=f"overview-{offset_days}",
            start_char=0,
            end_char=None,
            source_content_type="trend_overview",
        )

    md, stats = build_overview_pack_md(
        repository,
        plan,
        overview_pack_max_chars=10_000,
        item_overview_top_k=20,
        item_overview_item_max_chars=200,
    )
    assert stats.get("truncated") is False
    assert "doc_id" not in md

    lines = [line for line in md.splitlines() if line.startswith("- day ")]
    assert len(lines) == 7

    def extract_date(line: str) -> str:
        assert line.startswith("- day ")
        rest = line[len("- day ") :]
        return rest.split(" |", 1)[0].strip()

    got_dates = [extract_date(line) for line in lines]
    expected_dates = [
        (week_start + timedelta(days=i)).date().isoformat() for i in range(7)
    ]
    assert got_dates == expected_dates

    # Placeholders exist for missing days, and existing days include their overviews.
    assert any("| missing |" in line for line in lines)
    assert any("overview-0" in line for line in lines)
    assert any("overview-3" in line for line in lines)


def test_overview_pack_week_marks_missing_chunk_when_trend_doc_has_no_summary_chunk(
    configured_env,
) -> None:
    _ = configured_env
    _, repository = _build_runtime()

    anchor = datetime(2026, 3, 2, tzinfo=UTC).date()  # Monday
    week_start, week_end = week_period_bounds(anchor)
    plan = TrendGenerationPlan(
        target_granularity="week", period_start=week_start, period_end=week_end
    )

    # Create a daily trend doc but do NOT insert chunk_index=0.
    day_start = week_start + timedelta(days=1)
    day_end = day_start + timedelta(days=1)
    doc = repository.upsert_document_for_trend(
        granularity="day",
        period_start=day_start,
        period_end=day_end,
        title="Day missing chunk",
    )
    assert doc.id is not None

    md, _ = build_overview_pack_md(
        repository,
        plan,
        overview_pack_max_chars=10_000,
        item_overview_top_k=20,
        item_overview_item_max_chars=200,
    )
    assert "doc_id" not in md
    assert f"- day {day_start.date().isoformat()} | missing_chunk |" in md


def test_overview_pack_day_item_top_k_and_per_item_max_chars(configured_env) -> None:
    _ = configured_env
    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    anchor = datetime(2026, 3, 5, tzinfo=UTC).date()
    day_start, day_end = day_period_bounds(anchor)

    drafts = [
        ItemDraft.from_values(
            source="rss",
            source_item_id="overview-item-old",
            canonical_url="https://example.com/overview-item-old",
            title="Item Oldest",
            authors=["Alice"],
            published_at=day_start + timedelta(hours=1),
            raw_metadata={"source": "test"},
        ),
        ItemDraft.from_values(
            source="rss",
            source_item_id="overview-item-mid",
            canonical_url="https://example.com/overview-item-mid",
            title="Item Middle",
            authors=["Alice"],
            published_at=day_start + timedelta(hours=2),
            raw_metadata={"source": "test"},
        ),
        ItemDraft.from_values(
            source="rss",
            source_item_id="overview-item-new",
            canonical_url="https://example.com/overview-item-new",
            title="Item Newest",
            authors=["Alice"],
            published_at=day_start + timedelta(hours=3),
            raw_metadata={"source": "test"},
        ),
    ]

    service.prepare(run_id="run-overview-pack-day", drafts=drafts, limit=10)
    _ = service.analyze(run_id="run-overview-pack-day", limit=10)

    plan = TrendGenerationPlan(
        target_granularity="day", period_start=day_start, period_end=day_end
    )
    assert plan.overview_pack_strategy == "item_top_k"

    md, stats = build_overview_pack_md(
        repository,
        plan,
        overview_pack_max_chars=10_000,
        item_overview_top_k=2,
        item_overview_item_max_chars=5,
    )
    assert stats.get("truncated") is False

    assert "title=Item Newest" in md
    assert "title=Item Middle" in md
    assert "title=Item Oldest" not in md

    item_lines = [line for line in md.splitlines() if line.startswith("- rank=")]
    assert len(item_lines) == 2
    for line in item_lines:
        assert "| summary=" in line
        summary = line.split("| summary=", 1)[1].strip()
        assert len(summary) <= 5


def test_overview_pack_day_item_top_k_deduplicates_duplicate_urls(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Regression: top-k overview input should not repeat the same paper URL."""

    _ = configured_env
    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    anchor = datetime(2026, 3, 5, tzinfo=UTC).date()
    day_start, day_end = day_period_bounds(anchor)

    drafts = [
        ItemDraft.from_values(
            source="rss",
            source_item_id="overview-item-dup-a",
            canonical_url="https://example.com/overview-item-dup-a",
            title="Toolformer Planning for Browser Agents",
            authors=["Alice"],
            published_at=day_start + timedelta(hours=3),
            raw_metadata={"source": "test"},
        ),
        ItemDraft.from_values(
            source="rss",
            source_item_id="overview-item-dup-b",
            canonical_url="https://example.com/overview-item-dup-b",
            title="Diffusion Policies for Dexterous Robot Hands",
            authors=["Bob"],
            published_at=day_start + timedelta(hours=2),
            raw_metadata={"source": "test"},
        ),
    ]

    service.prepare(run_id="run-overview-pack-day-dedup", drafts=drafts, limit=10)
    _ = service.analyze(run_id="run-overview-pack-day-dedup", limit=10)

    pairs = repository.list_analyzed_items_in_period(
        period_start=day_start,
        period_end=day_end,
        limit=10,
    )
    assert len(pairs) == 2

    def _duplicate_first_pair(**_kwargs):  # type: ignore[no-untyped-def]
        return [pairs[0], pairs[0], pairs[1]]

    monkeypatch.setattr(repository, "list_analyzed_items_in_period", _duplicate_first_pair)

    plan = TrendGenerationPlan(
        target_granularity="day", period_start=day_start, period_end=day_end
    )

    md, stats = build_overview_pack_md(
        repository,
        plan,
        overview_pack_max_chars=10_000,
        item_overview_top_k=2,
        item_overview_item_max_chars=200,
    )
    assert stats.get("truncated") is False

    item_lines = [line for line in md.splitlines() if line.startswith("- rank=")]
    assert len(item_lines) == 2
    assert md.count("url=https://example.com/overview-item-dup-a") == 1
    assert md.count("url=https://example.com/overview-item-dup-b") == 1


def test_overview_pack_truncation_sets_stats_flag(configured_env) -> None:
    _ = configured_env
    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    anchor = datetime(2026, 3, 5, tzinfo=UTC).date()
    day_start, day_end = day_period_bounds(anchor)
    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="overview-item-trunc",
        canonical_url="https://example.com/overview-item-trunc",
        title="Item With A Very Long Title For Truncation",
        authors=["Alice"],
        published_at=day_start + timedelta(hours=1),
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-overview-pack-trunc", drafts=[draft], limit=10)
    _ = service.analyze(run_id="run-overview-pack-trunc", limit=10)

    plan = TrendGenerationPlan(
        target_granularity="day", period_start=day_start, period_end=day_end
    )

    full_md, _ = build_overview_pack_md(
        repository,
        plan,
        overview_pack_max_chars=10_000,
        item_overview_top_k=1,
        item_overview_item_max_chars=200,
    )
    assert len(full_md) > 80

    truncated_md, stats = build_overview_pack_md(
        repository,
        plan,
        overview_pack_max_chars=80,
        item_overview_top_k=1,
        item_overview_item_max_chars=200,
    )
    assert stats.get("truncated") is True
    assert len(truncated_md) == 80
    assert truncated_md == full_md[:80]
