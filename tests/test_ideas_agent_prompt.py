from __future__ import annotations

from datetime import UTC, datetime

from recoleta.passes.trend_ideas import TrendIdeasPayload, normalize_trend_ideas_payload
from recoleta.rag.ideas_agent import (
    _build_trend_ideas_instructions,
    build_trend_ideas_prompt_payload,
)
from recoleta.trends import TrendPayload


def test_ideas_instructions_require_finished_prose_without_public_worksheet_fields() -> (
    None
):
    instructions = _build_trend_ideas_instructions(
        output_language="Chinese (Simplified)"
    )

    assert "Do not invent new umbrella terms, branded labels, or slogan-like phrasing." in instructions
    assert "Use internal reasoning to decide why now, what changed, who it helps" in instructions
    assert "Do not expose those axes as separate reader-facing fields." in instructions
    assert "Each idea must be a finished short note." in instructions
    assert "ideas[].content_md for the prose body" in instructions
    assert "Do not use negative parallelism" in instructions
    assert "best bet" not in instructions.lower()
    assert "alternate" not in instructions.lower()
    assert "anti-thesis" not in instructions.lower()


def test_ideas_prompt_payload_reinforces_reader_facing_contract() -> None:
    payload = build_trend_ideas_prompt_payload(
        granularity="day",
        period_start=datetime(2026, 3, 9, tzinfo=UTC),
        period_end=datetime(2026, 3, 10, tzinfo=UTC),
        trend_payload=TrendPayload(
            title="Agent systems",
            granularity="day",
            period_start="2026-03-09T00:00:00+00:00",
            period_end="2026-03-10T00:00:00+00:00",
            overview_md="Execution loops are tightening.",
            topics=["agents"],
            clusters=[],
        ),
        trend_snapshot_pack_md="## Trend snapshot pack\n\nExecution loops are tightening.\n",
    )

    notes = payload["notes"]
    assert "Use idea ordering to express priority; do not emit best-bet or alternate labels." in notes
    assert "Use evidence_refs to point to the strongest supporting documents." in notes
    assert "Return finished short prose in ideas[].content_md instead of labeled method fields." in notes
    assert "Do not restate the trend summary as the final output." in notes


def test_normalize_trend_ideas_payload_caps_to_three_unique_grounded_ideas() -> None:
    payload = TrendIdeasPayload.model_validate(
        {
            "title": "Ideas",
            "granularity": "day",
            "period_start": "2026-03-09T00:00:00+00:00",
            "period_end": "2026-03-10T00:00:00+00:00",
            "summary_md": "Summary",
            "ideas": [
                {
                    "title": "Idea 1",
                    "content_md": "Idea body 1.",
                    "evidence_refs": [{"doc_id": 1, "chunk_index": 0}],
                },
                {
                    "title": "Idea 1",
                    "content_md": "Duplicate title should be dropped.",
                    "evidence_refs": [{"doc_id": 2, "chunk_index": 0}],
                },
                {
                    "title": "Idea 2",
                    "content_md": "Idea body 2.",
                    "evidence_refs": [{"doc_id": 2, "chunk_index": 0}],
                },
                {
                    "title": "Idea 3",
                    "content_md": "Idea body 3.",
                    "evidence_refs": [{"doc_id": 3, "chunk_index": 0}],
                },
                {
                    "title": "Idea 4",
                    "content_md": "Idea body 4.",
                    "evidence_refs": [{"doc_id": 4, "chunk_index": 0}],
                },
            ],
        }
    )

    normalized = normalize_trend_ideas_payload(payload)

    assert [idea.title for idea in normalized.ideas] == ["Idea 1", "Idea 2", "Idea 3"]
    assert [ref.doc_id for ref in normalized.ideas[0].evidence_refs] == [1]
