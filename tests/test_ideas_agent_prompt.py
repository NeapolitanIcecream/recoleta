from __future__ import annotations

from datetime import UTC, datetime

from recoleta.passes.trend_ideas import TrendIdeasPayload, normalize_trend_ideas_payload
from recoleta.rag.ideas_agent import (
    _TrendIdeasBundleTitle,
    _build_trend_ideas_instructions,
    _build_trend_ideas_title_instructions,
    build_trend_ideas_prompt_payload,
    build_trend_ideas_title_prompt_payload,
)
from recoleta.trends import TrendPayload


def test_ideas_instructions_require_finished_prose_without_public_worksheet_fields() -> (
    None
):
    instructions = _build_trend_ideas_instructions(
        output_language="Chinese (Simplified)"
    )

    assert "You are a research editor writing short reader-facing pieces from a local evidence pack." in instructions
    assert "Use internal reasoning to judge whether a concrete case now has enough evidence" in instructions
    assert "Do not expose those axes as separate reader-facing fields." in instructions
    assert "Each idea must be a finished short piece." in instructions
    assert "ideas[].content_md for the prose body" in instructions
    assert "Do not let task language leak into public prose." in instructions
    assert "the strongest notes" in instructions
    assert "the near-term job is not" in instructions
    assert "the result does not say" in instructions
    assert "away from X and toward Y" in instructions
    assert "X is not Y. It is Z." in instructions
    assert "Do not call the output publishable, grounded, retained, or strong." in instructions
    assert "Do not describe the set as ideas, notes, directions, pieces, or retained items inside summary_md." in instructions
    assert "shifting from" in instructions
    assert "turns from" in instructions
    assert "Do not use negative parallelism" in instructions
    assert "why-now" not in instructions.lower()
    assert "opportunity" not in instructions.lower()
    assert "wedge" not in instructions.lower()
    assert "buyer trigger" not in instructions.lower()
    assert "best bet" not in instructions.lower()
    assert "alternate" not in instructions.lower()
    assert "anti-thesis" not in instructions.lower()
    assert "trend snapshot" not in instructions.lower()
    assert "idea notes" not in instructions.lower()
    assert "evidence-grounded" not in instructions.lower()
    assert "publishable piece" not in instructions.lower()


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

    assert payload["task"] == "Draft up to three concrete short pieces from the supplied evidence pack."
    notes = payload["notes"]
    assert "Use idea ordering to express priority; do not emit best-bet or alternate labels." in notes
    assert "Use evidence_refs to point to the strongest supporting documents." in notes
    assert "Return finished short prose in ideas[].content_md instead of labeled method fields." in notes
    assert "Do not restate the trend summary as the final output." in notes
    assert "Do not let task labels or collection labels leak into public prose." in notes
    assert "Do not describe the output as publishable, grounded, retained, or strong." in notes
    assert any(
        note.startswith("Do not use formulas such as 'the strongest notes'")
        for note in notes
    )


def test_ideas_title_instructions_define_second_pass_bundle_title_contract() -> None:
    instructions = _build_trend_ideas_title_instructions(
        output_language="Chinese (Simplified)"
    )

    assert "Write a single bundle title for the retained set." in instructions
    assert "The title must be a short literal noun phrase" in instructions
    assert "Do not use labels such as idea, ideas, notes, evidence-grounded, trend snapshot, opportunity, or why now." in instructions
    assert "Do not use counts, dates, colons, slogans, or rhetorical questions." in instructions
    assert "Do not use negative parallelism" in instructions
    assert "Do not serialize JSON inside the title field." in instructions


def test_ideas_title_prompt_payload_only_uses_final_summary_and_retained_ideas() -> None:
    payload = build_trend_ideas_title_prompt_payload(
        summary_md="Release controls and runtime checks now travel together.",
        ideas=[
            {
                "title": "Prompt release gate",
                "content_md": "Add a release gate before prompt rollout.",
            },
            {
                "title": "Runtime policy enforcement",
                "content_md": "Enforce tool policies in the live execution path.",
            },
        ],
    )

    assert payload["task"] == "Write one short bundle title for the retained set. Return plain text in the title field."
    assert payload["summary_md"] == (
        "Release controls and runtime checks now travel together."
    )
    assert payload["ideas"] == [
        {
            "title": "Prompt release gate",
            "content_md": "Add a release gate before prompt rollout.",
        },
        {
            "title": "Runtime policy enforcement",
            "content_md": "Enforce tool policies in the live execution path.",
        },
    ]


def test_bundle_title_validation_unwraps_nested_json_string() -> None:
    payload = _TrendIdeasBundleTitle.model_validate(
        {"title": '{"title":"Robotics Control Evaluation Stack"}'}
    )

    assert payload.title == "Robotics Control Evaluation Stack"


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


def test_trend_idea_content_md_preserves_markdown_structure() -> None:
    content_md = "First paragraph.\n\n- Bullet one\n- Bullet two"
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
                    "content_md": content_md,
                    "evidence_refs": [{"doc_id": 1, "chunk_index": 0}],
                }
            ],
        }
    )

    assert payload.ideas[0].content_md == content_md
