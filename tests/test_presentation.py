from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from recoleta.presentation import (
    build_idea_presentation_v1,
    build_trend_presentation_v1,
    validate_presentation_v1,
    write_presentation_sidecar,
)


def _idea(
    *,
    title: str,
    kind: str = "tooling_wedge",
    time_horizon: str = "now",
) -> SimpleNamespace:
    return SimpleNamespace(
        title=title,
        kind=kind,
        time_horizon=time_horizon,
        user_or_job="Platform engineers shipping agent changes.",
        thesis="Ship a prompt release gate before production rollout.",
        why_now="Prompt changes now behave like deployable releases.",
        what_changed="Agent teams now manage prompt and tool changes continuously.",
        validation_next_step="Replay 20 prompt changes through the gate.",
        evidence_refs=[
            SimpleNamespace(doc_id=11, chunk_index=0, reason="Trend note captures the shift.")
        ],
    )


def test_validate_presentation_v1_allows_single_ranked_shift_when_evidence_is_thin() -> None:
    presentation = build_trend_presentation_v1(
        source_markdown_path="Trends/day--2026-03-02--trend--7.md",
        title="Verification gets operational",
        overview_md="Teams are tightening release discipline.",
        evolution={
            "signals": [
                {
                    "theme": "Verification loops",
                    "summary": "Teams now quantify release risk.",
                    "history_windows": ["prev_1"],
                }
            ]
        },
        history_window_refs={
            "prev_1": {
                "title": "Earlier verification push",
                "label": "2026-W10",
            }
        },
        clusters=[],
    )

    assert validate_presentation_v1(presentation) == []


def test_validate_presentation_v1_requires_complete_label_sets_and_required_fields() -> None:
    presentation = build_idea_presentation_v1(
        source_markdown_path="Ideas/day--2026-03-02--ideas.md",
        title="Verification-first agent rollout",
        summary_md="Use a prompt release gate before shipping changes.",
        ideas=[_idea(title="Prompt CI gate")],
    )
    del presentation["display_labels"]["role"]
    del presentation["content"]["opportunities"][0]["validation_next_step"]

    errors = validate_presentation_v1(presentation)

    assert "idea display_labels must include: role" in errors
    assert "idea opportunities must include: validation_next_step" in errors


def test_write_presentation_sidecar_rejects_invalid_contracts(tmp_path: Path) -> None:
    presentation = build_idea_presentation_v1(
        source_markdown_path="Ideas/day--2026-03-02--ideas.md",
        title="Verification-first agent rollout",
        summary_md="Use a prompt release gate before shipping changes.",
        ideas=[_idea(title="Prompt CI gate"), _idea(title="Operator review lane")],
    )
    presentation["content"]["opportunities"][1]["tier"] = "best_bet"

    with pytest.raises(ValueError, match="exactly one best_bet"):
        write_presentation_sidecar(
            note_path=tmp_path / "Ideas" / "day--2026-03-02--ideas.md",
            presentation=presentation,
        )


def test_validate_presentation_v1_does_not_treat_synthesis_as_schema_label_leakage() -> None:
    presentation = build_trend_presentation_v1(
        source_markdown_path="Trends/week--2026-W10--trend--81.md",
        title="Week 10 roundup",
        overview_md="Weekly synthesis.",
        evolution=None,
        history_window_refs=None,
        clusters=[],
    )

    assert validate_presentation_v1(presentation) == []


def test_validate_presentation_v1_rejects_case_variants_of_placeholder_tokens() -> None:
    presentation = build_trend_presentation_v1(
        source_markdown_path="Trends/week--2026-W10--trend--81.md",
        title="Week 10 roundup",
        overview_md="Weekly synthesis.",
        evolution=None,
        history_window_refs=None,
        clusters=[],
    )
    presentation["content"]["overview"] = "Compared with PREV_1 and Prev1, teams now gate prompt releases."

    errors = validate_presentation_v1(presentation)

    assert "user-visible fields must not contain raw history placeholder tokens" in errors


def test_build_trend_presentation_v1_renders_history_refs_case_insensitively() -> None:
    presentation = build_trend_presentation_v1(
        source_markdown_path="Trends/week--2026-W10--trend--81.md",
        title="Week 10 roundup",
        overview_md="Compared with Prev_1, teams now gate prompt releases.",
        evolution=None,
        history_window_refs={
            "prev_1": {
                "title": "Earlier verification push",
                "label": "2026-W09",
            }
        },
        clusters=[],
    )

    assert (
        presentation["content"]["overview"]
        == "Compared with Earlier verification push (2026-W09), teams now gate prompt releases."
    )


def test_build_trend_presentation_v1_preserves_markdown_paragraph_breaks() -> None:
    presentation = build_trend_presentation_v1(
        source_markdown_path="Trends/week--2026-W10--trend--81.md",
        title="Week 10 roundup",
        overview_md=(
            "Teams are tightening prompt rollout discipline.\n\n"
            "### Why it matters\n\n"
            "- More teams now gate releases."
        ),
        evolution=None,
        history_window_refs=None,
        clusters=[],
    )

    assert presentation["content"]["overview"] == (
        "Teams are tightening prompt rollout discipline.\n\n"
        "### Why it matters\n\n"
        "- More teams now gate releases."
    )


def test_validate_presentation_v1_rejects_non_mapping_idea_opportunities() -> None:
    presentation = build_idea_presentation_v1(
        source_markdown_path="Ideas/day--2026-03-02--ideas.md",
        title="Verification-first agent rollout",
        summary_md="Use a prompt release gate before shipping changes.",
        ideas=[_idea(title="Prompt CI gate")],
    )
    presentation["content"]["opportunities"].append("oops")

    errors = validate_presentation_v1(presentation)

    assert "idea opportunities entries must be mappings" in errors
