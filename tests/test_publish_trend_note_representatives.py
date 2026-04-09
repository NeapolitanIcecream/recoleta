from __future__ import annotations

from datetime import UTC, datetime, timedelta
import json
from pathlib import Path
from typing import Any, cast

import pytest

from recoleta.presentation import presentation_sidecar_path, validate_presentation
from recoleta.publish import write_markdown_trend_note
from recoleta.publish.trend_notes import resolve_trend_note_href


def test_write_markdown_trend_note_renders_new_public_contract(tmp_path: Path) -> None:
    period_start = datetime(2026, 3, 12, tzinfo=UTC)
    period_end = period_start + timedelta(days=1)

    note_path = write_markdown_trend_note(
        output_dir=tmp_path,
        trend_doc_id=6,
        title="Weekly Trend",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        run_id="run-test",
        overview_md="Teams are tightening release discipline.",
        topics=["agents"],
        clusters=[
            {
                "title": "Release discipline",
                "content_md": "Verification moved into the shipping path.",
                "evidence_refs": [
                    {
                        "doc_id": 1,
                        "chunk_index": 0,
                        "title": "CodeScout",
                        "href": "../Inbox/2026-03-11--codescout.md",
                        "reason": "The note ties verification to rollout control.",
                        "source_type": "paper",
                        "confidence": "high",
                    }
                ],
            }
        ],
    )

    text = note_path.read_text(encoding="utf-8")
    sidecar = json.loads(
        presentation_sidecar_path(note_path=note_path).read_text(encoding="utf-8")
    )

    assert "## Overview" in text
    assert "## Clusters" in text
    assert "### Release discipline" in text
    assert "#### Evidence" in text
    assert "Top shifts" not in text
    assert "Counter-signal" not in text
    assert "Representative sources" not in text
    assert sidecar["content"]["clusters"][0]["title"] == "Release discipline"
    assert sidecar["content"]["clusters"][0]["evidence"][0]["title"] == "CodeScout"
    assert "ranked_shifts" not in sidecar["content"]
    assert "counter_signal" not in sidecar["content"]
    assert "representative_sources" not in sidecar["content"]
    assert validate_presentation(sidecar) == []


def test_write_markdown_trend_note_renders_empty_clusters_list(tmp_path: Path) -> None:
    period_start = datetime(2026, 3, 12, tzinfo=UTC)
    period_end = period_start + timedelta(days=1)

    note_path = write_markdown_trend_note(
        output_dir=tmp_path,
        trend_doc_id=7,
        title="Daily Trend",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        run_id="run-empty",
        overview_md="Nothing strong enough to cluster yet.",
        topics=["agents"],
        clusters=[],
    )

    assert "## Clusters\n- (none)" in note_path.read_text(encoding="utf-8")


def test_resolve_trend_note_href_uses_relative_paths_between_siblings() -> None:
    href = resolve_trend_note_href(
        note_dir=Path("/tmp/site/Trends"),
        from_dir=Path("/tmp/site/Inbox"),
        trend_doc_id=9,
        granularity="day",
        period_start=datetime(2026, 3, 12, tzinfo=UTC),
    )

    assert href == "../Trends/day--2026-03-12--trend--9.md"


def test_write_markdown_trend_note_rejects_unexpected_keyword_arguments(
    tmp_path: Path,
) -> None:
    period_start = datetime(2026, 3, 2, tzinfo=UTC)
    period_end = period_start + timedelta(days=1)

    with pytest.raises(TypeError, match="unexpected keyword argument 'site_exlcude'"):
        cast(Any, write_markdown_trend_note)(
            output_dir=tmp_path,
            trend_doc_id=1,
            title="Daily Trend",
            granularity="day",
            period_start=period_start,
            period_end=period_end,
            run_id="run-test",
            overview_md="overview",
            topics=["agents"],
            site_exlcude=True,
        )
