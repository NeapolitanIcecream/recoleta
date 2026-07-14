from __future__ import annotations

from datetime import UTC, datetime, timedelta

from recoleta.pipeline.ideas_quality import build_prior_ideas_pack_md
from tests.spec_support import _build_runtime


def _seed_idea_document(
    *,
    repository,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
    entries: list[tuple[str, str]],
) -> None:
    doc = repository.upsert_document_for_idea(
        granularity=granularity,
        period_start=period_start,
        period_end=period_end,
        title=f"{granularity} prior ideas",
    )
    assert doc.id is not None
    for chunk_index, (title, content) in enumerate(entries, start=1):
        repository.upsert_document_chunk(
            doc_id=int(doc.id),
            chunk_index=chunk_index,
            kind="content",
            text_value=f"Title: {title}\nContent: {content}",
            source_content_type="trend_idea",
        )


def _seed_idea_pass_state(
    *, repository, period_start: datetime, period_end: datetime, status: str
) -> None:
    trend = repository.create_pass_output(
        run_id=f"run-trend-{period_start.date()}-{status}",
        pass_kind="trend_synthesis",
        status="succeeded",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload={},
    )
    assert trend.id is not None
    repository.create_pass_output(
        run_id=f"run-ideas-{period_start.date()}-{status}",
        pass_kind="trend_ideas",
        status=status,
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload={},
        input_refs=[
            {
                "ref_kind": "pass_output",
                "pass_kind": "trend_synthesis",
                "pass_output_id": trend.id,
            }
        ],
    )


def test_prior_ideas_pack_uses_only_bounded_previous_same_granularity_windows(
    configured_env,
) -> None:
    _ = configured_env
    _, repository = _build_runtime()
    period_start = datetime(2026, 3, 10, tzinfo=UTC)
    period_end = period_start + timedelta(days=1)
    _seed_idea_document(
        repository=repository,
        granularity="day",
        period_start=period_start - timedelta(days=1),
        period_end=period_start,
        entries=[("Adjacent idea", "A concept from the immediately prior day.")],
    )
    _seed_idea_document(
        repository=repository,
        granularity="day",
        period_start=period_start - timedelta(days=4),
        period_end=period_start - timedelta(days=3),
        entries=[("Too old", "This lies outside the three-window history boundary.")],
    )
    _seed_idea_document(
        repository=repository,
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        entries=[("Current rerun", "The current same-level projection is excluded.")],
    )

    pack_md, stats = build_prior_ideas_pack_md(
        repository=repository,
        granularity="day",
        period_start=period_start,
        period_end=period_end,
    )

    assert "Adjacent idea" in pack_md
    assert "Too old" not in pack_md
    assert "Current rerun" not in pack_md
    assert stats["requested_sections"] == 3
    assert stats["retained_entries_total"] == 1
    assert stats["chars"] == len(pack_md)


def test_prior_ideas_pack_includes_current_lower_level_and_respects_char_budget(
    configured_env,
) -> None:
    _ = configured_env
    _, repository = _build_runtime()
    period_start = datetime(2026, 3, 9, tzinfo=UTC)
    period_end = period_start + timedelta(days=7)
    _seed_idea_document(
        repository=repository,
        granularity="day",
        period_start=period_start + timedelta(days=1),
        period_end=period_start + timedelta(days=2),
        entries=[
            (f"Daily concept {index}", "x" * 700)
            for index in range(1, 7)
        ],
    )
    _seed_idea_document(
        repository=repository,
        granularity="week",
        period_start=period_start - timedelta(days=7),
        period_end=period_start,
        entries=[("Previous weekly concept", "A neighboring weekly hypothesis.")],
    )
    _seed_idea_document(
        repository=repository,
        granularity="week",
        period_start=period_start,
        period_end=period_end,
        entries=[("Current weekly rerun", "This same-level output is excluded.")],
    )

    pack_md, stats = build_prior_ideas_pack_md(
        repository=repository,
        granularity="week",
        period_start=period_start,
        period_end=period_end,
        max_chars=700,
    )

    assert len(pack_md) <= 700
    assert pack_md.endswith("\n")
    assert "Daily concept" in pack_md
    assert "Current weekly rerun" not in pack_md
    assert stats["budget_omitted_total"] > 0
    assert stats["entry_text_truncated_total"] > 0
    assert stats["truncated"] is True


def test_prior_ideas_pack_excludes_documents_with_latest_suppressed_output(
    configured_env,
) -> None:
    _ = configured_env
    _, repository = _build_runtime()
    period_start = datetime(2026, 3, 10, tzinfo=UTC)
    prior_start = period_start - timedelta(days=1)
    _seed_idea_document(
        repository=repository,
        granularity="day",
        period_start=prior_start,
        period_end=period_start,
        entries=[("Retired idea", "This must no longer suppress future ideation.")],
    )
    for status in ("succeeded", "suppressed"):
        repository.create_pass_output(
            run_id=f"run-prior-{status}",
            pass_kind="trend_ideas",
            status=status,
            granularity="day",
            period_start=prior_start,
            period_end=period_start,
            payload={"ideas": []},
        )

    pack_md, stats = build_prior_ideas_pack_md(
        repository=repository,
        granularity="day",
        period_start=period_start,
        period_end=period_start + timedelta(days=1),
    )

    assert "Retired idea" not in pack_md
    assert stats["retained_entries_total"] == 0
    assert stats["suppressed_entries_omitted_total"] == 1


def test_prior_ideas_pack_pages_past_suppressed_rows(
    configured_env,
) -> None:
    _ = configured_env
    _, repository = _build_runtime()
    period_start = datetime(2026, 3, 9, tzinfo=UTC)
    period_end = period_start + timedelta(days=7)
    suppressed_start = period_start + timedelta(days=5)
    suppressed_end = suppressed_start + timedelta(days=1)
    _seed_idea_document(
        repository=repository,
        granularity="day",
        period_start=suppressed_start,
        period_end=suppressed_end,
        entries=[
            (f"Retired concept {index}", "This row must be skipped.")
            for index in range(13)
        ],
    )
    _seed_idea_pass_state(
        repository=repository,
        period_start=suppressed_start,
        period_end=suppressed_end,
        status="suppressed",
    )
    valid_start = period_start + timedelta(days=1)
    valid_end = valid_start + timedelta(days=1)
    _seed_idea_document(
        repository=repository,
        granularity="day",
        period_start=valid_start,
        period_end=valid_end,
        entries=[("Still useful", "This active idea should survive pagination.")],
    )
    _seed_idea_pass_state(
        repository=repository,
        period_start=valid_start,
        period_end=valid_end,
        status="succeeded",
    )

    pack_md, stats = build_prior_ideas_pack_md(
        repository=repository,
        granularity="week",
        period_start=period_start,
        period_end=period_end,
    )

    assert "Still useful" in pack_md
    assert "Retired concept" not in pack_md
    assert stats["suppressed_entries_omitted_total"] == 13
