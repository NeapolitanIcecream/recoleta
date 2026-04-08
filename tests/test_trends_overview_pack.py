from __future__ import annotations

from datetime import UTC, datetime, timedelta
import json

import pytest

from recoleta.pipeline import PipelineService
from recoleta.trends import (
    TrendGenerationPlan,
    build_overview_pack_md,
    day_period_bounds,
    index_items_as_documents,
    week_period_bounds,
)
from recoleta.trends_overview import BuildOverviewPackRequest
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

    headings = [line for line in md.splitlines() if line.startswith("### day ")]
    assert len(headings) == 7

    def extract_date(line: str) -> str:
        assert line.startswith("### day ")
        return line[len("### day ") :].strip()

    got_dates = [extract_date(line) for line in headings]
    expected_dates = [
        (week_start + timedelta(days=i)).date().isoformat() for i in range(7)
    ]
    assert got_dates == expected_dates

    # Placeholders exist for missing days, and existing days include their overviews.
    assert md.count("- status=missing") >= 5
    assert "- status=summary_fallback" in md
    assert "- overview=overview-0" in md
    assert "- overview=overview-3" in md


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
    assert f"### day {day_start.date().isoformat()}" in md
    assert "- status=missing_chunk" in md


def test_overview_pack_request_entrypoint_matches_legacy_args(configured_env) -> None:
    _ = configured_env
    _, repository = _build_runtime()

    anchor = datetime(2026, 3, 2, tzinfo=UTC).date()
    week_start, week_end = week_period_bounds(anchor)
    plan = TrendGenerationPlan(
        target_granularity="week", period_start=week_start, period_end=week_end
    )

    expected_md, expected_stats = build_overview_pack_md(
        repository,
        plan,
        overview_pack_max_chars=10_000,
        item_overview_top_k=20,
        item_overview_item_max_chars=200,
    )

    request = BuildOverviewPackRequest(
        repository=repository,
        plan=plan,
        overview_pack_max_chars=10_000,
        item_overview_top_k=20,
        item_overview_item_max_chars=200,
    )
    md, stats = build_overview_pack_md(request=request)

    assert md == expected_md
    assert stats == expected_stats


def test_overview_pack_week_prefers_structured_trend_payload_meta_chunks(
    configured_env,
) -> None:
    _ = configured_env
    _, repository = _build_runtime()

    anchor = datetime(2026, 3, 2, tzinfo=UTC).date()  # Monday
    week_start, week_end = week_period_bounds(anchor)
    plan = TrendGenerationPlan(
        target_granularity="week", period_start=week_start, period_end=week_end
    )

    item, _ = repository.upsert_item(
        ItemDraft.from_values(
            source="rss",
            source_item_id="meta-pack-item-1",
            canonical_url="https://example.com/meta-pack-item-1",
            title="Representative Paper",
            authors=["Alice"],
            published_at=week_start,
            raw_metadata={"source": "test"},
        )
    )
    assert item.id is not None
    item_doc = repository.upsert_document_for_item(item=item)
    assert item_doc.id is not None

    day_start = week_start
    day_end = day_start + timedelta(days=1)
    doc = repository.upsert_document_for_trend(
        granularity="day",
        period_start=day_start,
        period_end=day_end,
        title="Day placeholder",
    )
    assert doc.id is not None
    repository.upsert_document_chunk(
        doc_id=int(doc.id),
        chunk_index=1,
        kind="meta",
        text_value=json.dumps(
            {
                "title": "2026-03-02 研究趋势日报：Agent systems get tighter loops",
                "overview_md": (
                    "Agent systems are getting tighter loops.\n\n"
                    "## Top-1 must-read\n"
                    "1. [Must Read Paper](https://example.com/must-read)\n"
                ),
                "clusters": [
                    {
                        "title": "Loop closing",
                        "content_md": "Systems are getting more grounded.",
                        "evidence_refs": [
                            {"doc_id": int(item_doc.id), "chunk_index": 0}
                        ],
                    }
                ],
            },
            ensure_ascii=False,
        ),
        start_char=0,
        end_char=None,
        source_content_type="trend_payload_json",
    )

    md, _ = build_overview_pack_md(
        repository,
        plan,
        overview_pack_max_chars=10_000,
        item_overview_top_k=20,
        item_overview_item_max_chars=200,
    )

    assert "研究趋势日报" not in md
    assert "- title=Agent systems get tighter loops" in md
    assert "- must_read=[Must Read Paper](https://example.com/must-read)" in md
    assert "- cluster=Loop closing" in md
    assert (
        "- representative=[Representative Paper](https://example.com/meta-pack-item-1)"
        in md
    )


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
    _ = index_items_as_documents(
        repository=repository,
        run_id="run-overview-pack-day",
        period_start=day_start,
        period_end=day_end,
    )

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

    item_lines = [line for line in md.splitlines() if line.startswith("### item rank=")]
    assert len(item_lines) == 2
    for line in md.splitlines():
        if not any(
            line.startswith(prefix)
            for prefix in ("- summary=", "- problem=", "- approach=", "- results=")
        ):
            continue
        value = line.split("=", 1)[1].strip()
        assert len(value) <= 5


def test_overview_pack_day_uses_materialized_item_docs_only(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
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
        source_item_id="overview-docs-only",
        canonical_url="https://example.com/overview-docs-only",
        title="Docs Only Overview Item",
        authors=["Alice"],
        published_at=day_start + timedelta(hours=1),
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-overview-docs-only", drafts=[draft], limit=10)
    _ = service.analyze(run_id="run-overview-docs-only", limit=10)
    _ = index_items_as_documents(
        repository=repository,
        run_id="run-overview-docs-only",
        period_start=day_start,
        period_end=day_end,
    )

    def _raise_if_analyzed_pairs_requested(**_kwargs):  # type: ignore[no-untyped-def]
        raise AssertionError("day overview should not read analyses directly")

    monkeypatch.setattr(
        repository,
        "list_analyzed_items_in_period",
        _raise_if_analyzed_pairs_requested,
    )

    plan = TrendGenerationPlan(
        target_granularity="day", period_start=day_start, period_end=day_end
    )
    md, stats = build_overview_pack_md(
        repository,
        plan,
        overview_pack_max_chars=10_000,
        item_overview_top_k=1,
        item_overview_item_max_chars=200,
    )

    assert stats.get("truncated") is False
    assert "title=Docs Only Overview Item" in md


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
    _ = index_items_as_documents(
        repository=repository,
        run_id="run-overview-pack-day-dedup",
        period_start=day_start,
        period_end=day_end,
    )
    meta_rows = repository.list_document_chunk_index_rows_in_period(
        doc_type="item",
        kind="meta",
        period_start=day_start,
        period_end=day_end,
        limit=10,
    )
    assert len(meta_rows) == 2

    original_list_rows = repository.list_document_chunk_index_rows_in_period

    def _duplicate_meta_rows(**kwargs):  # type: ignore[no-untyped-def]
        rows = original_list_rows(**kwargs)
        if kwargs.get("kind") == "meta":
            return [rows[0], rows[0], rows[1]]
        return rows

    monkeypatch.setattr(repository, "list_document_chunk_index_rows_in_period", _duplicate_meta_rows)

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

    item_lines = [line for line in md.splitlines() if line.startswith("### item rank=")]
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
    _ = index_items_as_documents(
        repository=repository,
        run_id="run-overview-pack-trunc",
        period_start=day_start,
        period_end=day_end,
    )

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
