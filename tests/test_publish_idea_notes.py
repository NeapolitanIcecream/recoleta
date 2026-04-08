from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path
from typing import Any, cast

import pytest

from recoleta.presentation import presentation_sidecar_path, validate_presentation
from recoleta.passes.trend_ideas import TrendIdeasPayload
from recoleta.publish import write_markdown_ideas_note
from recoleta.storage import Repository


def _payload(period_start: datetime, period_end: datetime) -> TrendIdeasPayload:
    return TrendIdeasPayload.model_validate(
        {
            "title": "Why now ideas",
            "granularity": "day",
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat(),
            "summary_md": "Structured release controls now feel overdue.",
            "ideas": [
                {
                    "title": "Prompt release gate",
                    "content_md": (
                        "Add a release gate for prompt and tool changes before rollout."
                    ),
                    "evidence_refs": [
                        {
                            "doc_id": 1,
                            "chunk_index": 0,
                            "reason": "The trend note ties verification to rollout control.",
                        }
                    ],
                }
            ],
        }
    )


def test_write_markdown_ideas_note_renders_new_public_contract(tmp_path: Path) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    period_start = datetime(2026, 3, 2, tzinfo=UTC)
    period_end = datetime(2026, 3, 3, tzinfo=UTC)

    note_path = write_markdown_ideas_note(
        repository=repository,
        output_dir=tmp_path / "notes",
        pass_output_id=7,
        upstream_pass_output_id=3,
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        run_id="run-ideas-shape",
        status="succeeded",
        payload=_payload(period_start, period_end),
        topics=["agents"],
    )

    text = note_path.read_text(encoding="utf-8")
    sidecar = json.loads(
        presentation_sidecar_path(note_path=note_path).read_text(encoding="utf-8")
    )

    assert "# Why now ideas" in text
    assert "## Summary" in text
    assert "## Prompt release gate" in text
    assert "### Evidence" in text
    assert "Best bet" not in text
    assert "Alternate" not in text
    assert "Anti-thesis" not in text
    assert sidecar["content"]["summary"] == "Structured release controls now feel overdue."
    assert [idea["title"] for idea in sidecar["content"]["ideas"]] == [
        "Prompt release gate"
    ]
    assert "opportunities" not in sidecar["content"]
    assert validate_presentation(sidecar) == []


def test_write_markdown_ideas_note_skips_sidecar_when_status_is_not_succeeded(
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    period_start = datetime(2026, 3, 2, tzinfo=UTC)
    period_end = datetime(2026, 3, 3, tzinfo=UTC)

    note_path = write_markdown_ideas_note(
        repository=repository,
        output_dir=tmp_path / "notes",
        pass_output_id=7,
        upstream_pass_output_id=3,
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        run_id="run-ideas-no-sidecar",
        status="failed",
        payload=_payload(period_start, period_end),
        topics=["agents"],
    )

    assert note_path.exists()
    assert not presentation_sidecar_path(note_path=note_path).exists()


def test_write_markdown_ideas_note_rejects_unexpected_keyword_arguments(
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    period_start = datetime(2026, 3, 2, tzinfo=UTC)
    period_end = datetime(2026, 3, 3, tzinfo=UTC)

    with pytest.raises(TypeError, match="unexpected keyword argument 'statsu'"):
        cast(Any, write_markdown_ideas_note)(
            repository=repository,
            output_dir=tmp_path / "notes",
            pass_output_id=7,
            upstream_pass_output_id=3,
            granularity="day",
            period_start=period_start,
            period_end=period_end,
            run_id="run-ideas-typo",
            statsu="succeeded",
            payload=_payload(period_start, period_end),
        )


def test_write_markdown_ideas_note_requires_pass_output_ids(tmp_path: Path) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    period_start = datetime(2026, 3, 2, tzinfo=UTC)
    period_end = datetime(2026, 3, 3, tzinfo=UTC)

    with pytest.raises(
        TypeError,
        match="missing required keyword-only argument[s]?: 'pass_output_id'",
    ):
        write_markdown_ideas_note(
            repository=repository,
            output_dir=tmp_path / "notes",
            granularity="day",
            period_start=period_start,
            period_end=period_end,
            run_id="run-ideas-missing-pass-ids",
            status="succeeded",
            payload=_payload(period_start, period_end),
        )
