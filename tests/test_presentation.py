from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from recoleta.presentation import (
    build_idea_presentation_v1,
    build_trend_presentation_v1,
    display_idea_kind,
    display_idea_time_horizon,
    idea_display_labels,
    is_localized_output_path,
    resolve_presentation_language_code,
    trend_display_labels,
    validate_presentation_v1,
    write_presentation_sidecar,
)


def _idea(
    *,
    title: str,
    kind: str = "tooling_wedge",
    time_horizon: str = "now",
    language_code: str | None = None,
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
            SimpleNamespace(
                doc_id=11,
                chunk_index=0,
                reason="Trend note captures the shift.",
                title="CodeScout",
                href="../Inbox/2026-03-02--codescout.md",
                authors=["Alice"],
                source="arxiv",
                score=0.91,
            )
        ],
        language_code=language_code,
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


def test_build_trend_presentation_v1_preserves_unresolved_history_placeholders() -> None:
    presentation = build_trend_presentation_v1(
        source_markdown_path="Trends/week--2026-W10--trend--81.md",
        title="Week 10 roundup",
        overview_md="Compared with prev_2, teams now gate prompt releases.",
        evolution=None,
        history_window_refs={"prev_1": {"title": "Earlier verification push", "label": "2026-W09"}},
        clusters=[],
    )

    assert (
        presentation["content"]["overview"]
        == "Compared with prev_2, teams now gate prompt releases."
    )
    assert "user-visible fields must not contain raw history placeholder tokens" in (
        validate_presentation_v1(presentation)
    )


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


def test_build_trend_presentation_v1_preserves_indented_markdown_lines() -> None:
    presentation = build_trend_presentation_v1(
        source_markdown_path="Trends/week--2026-W10--trend--81.md",
        title="Week 10 roundup",
        overview_md=(
            "- Parent item\n"
            "  - Compared with prev_1, nested item now matters more.\n"
        ),
        evolution=None,
        history_window_refs={
            "prev_1": {
                "title": "Earlier verification push",
                "label": "2026-W09",
            }
        },
        clusters=[],
    )

    assert presentation["content"]["overview"] == (
        "- Parent item\n"
        "  - Compared with Earlier verification push (2026-W09), nested item now matters more."
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


def test_presentation_labels_preserve_traditional_chinese_family() -> None:
    assert trend_display_labels(language_code="zh-TW")["overview"] == "概覽"
    assert idea_display_labels(language_code="zh-TW")["best_bet"] == "首要機會"
    assert display_idea_kind("workflow_shift", language_code="zh-TW") == "工作流轉變"
    assert display_idea_time_horizon("near", language_code="zh-TW") == "近期"


def test_build_presentation_v1_does_not_guess_english_language_code() -> None:
    trend_presentation = build_trend_presentation_v1(
        source_markdown_path="Trends/week--2026-W10--trend--81.md",
        title="Week 10 roundup",
        overview_md="Weekly synthesis.",
        evolution=None,
        history_window_refs=None,
        clusters=[],
    )
    idea_presentation = build_idea_presentation_v1(
        source_markdown_path="Ideas/day--2026-03-02--ideas.md",
        title="Verification-first agent rollout",
        summary_md="Use a prompt release gate before shipping changes.",
        ideas=[_idea(title="Prompt CI gate")],
    )

    assert trend_presentation["language_code"] is None
    assert idea_presentation["language_code"] is None


def test_resolve_presentation_language_code_maps_common_output_language_labels() -> None:
    assert (
        resolve_presentation_language_code(output_language="Chinese (Simplified)")
        == "zh-CN"
    )
    assert resolve_presentation_language_code(output_language="English") == "en"
    assert resolve_presentation_language_code(output_language="zh_cn") == "zh-CN"


def test_is_localized_output_path_requires_localized_language_layout(tmp_path: Path) -> None:
    canonical_under_localized_name = tmp_path / "Localized" / "project" / "outputs"
    localized_root = tmp_path / "outputs" / "Localized" / "zh-cn"
    localized_surface = localized_root / "Trends"

    assert not is_localized_output_path(canonical_under_localized_name)
    assert is_localized_output_path(localized_root)
    assert is_localized_output_path(localized_surface)


def test_build_idea_presentation_v1_localizes_labels_and_reader_facing_enums() -> None:
    presentation = build_idea_presentation_v1(
        source_markdown_path="Localized/zh-cn/Ideas/day--2026-03-02--ideas.md",
        title="验证优先的智能体发布",
        summary_md="先把提示词变更纳入可审计发布流程。",
        ideas=[_idea(title="提示词发布闸门", language_code="zh-CN")],
        language_code="zh-CN",
    )

    opportunity = presentation["content"]["opportunities"][0]

    assert presentation["display_labels"]["best_bet"] == "首要机会"
    assert presentation["display_labels"]["validation_next_step"] == "下一步验证"
    assert opportunity["display_kind"] == "工具切入点"
    assert opportunity["display_time_horizon"] == "现在"


def test_build_idea_presentation_v1_uses_traditional_chinese_display_labels() -> None:
    presentation = build_idea_presentation_v1(
        source_markdown_path="Localized/zh-tw/Ideas/day--2026-03-02--ideas.md",
        title="驗證優先的智能體發佈",
        summary_md="先把提示詞變更納入可審計發佈流程。",
        ideas=[_idea(title="提示詞發佈閘門", language_code="zh-TW")],
        language_code="zh-TW",
    )

    opportunity = presentation["content"]["opportunities"][0]

    assert presentation["display_labels"]["best_bet"] == "首要機會"
    assert presentation["display_labels"]["validation_next_step"] == "下一步驗證"
    assert opportunity["display_kind"] == "工具切入點"
    assert opportunity["display_time_horizon"] == "現在"


def test_build_idea_presentation_v1_projects_evidence_source_metadata() -> None:
    presentation = build_idea_presentation_v1(
        source_markdown_path="Ideas/day--2026-03-02--ideas.md",
        title="Verification-first agent rollout",
        summary_md="Use a prompt release gate before shipping changes.",
        ideas=[_idea(title="Prompt CI gate")],
    )

    evidence = presentation["content"]["opportunities"][0]["evidence"][0]

    assert evidence["title"] == "CodeScout"
    assert evidence["href"] == "../Inbox/2026-03-02--codescout.md"
    assert evidence["authors"] == ["Alice"]
    assert evidence["source_type"] == "paper"
    assert evidence["confidence"] == "high"


def test_build_trend_presentation_v1_projects_representative_source_metadata() -> None:
    presentation = build_trend_presentation_v1(
        source_markdown_path="Trends/day--2026-03-02--trend--7.md",
        title="Verification gets operational",
        overview_md="Teams are tightening release discipline.",
        evolution=None,
        history_window_refs=None,
        clusters=[
            {
                "name": "Verification loops",
                "description": "Teams now quantify release risk.",
                "representative_chunks": [
                    {
                        "doc_id": 11,
                        "chunk_index": 0,
                        "score": 0.91,
                        "title": "CodeScout",
                        "note_href": "../Inbox/2026-03-02--codescout.md",
                        "url": "https://example.com/codescout",
                        "authors": ["Alice"],
                        "source": "arxiv",
                    }
                ],
            }
        ],
    )

    representative = presentation["content"]["representative_sources"][0]

    assert representative["doc_id"] == 11
    assert representative["chunk_index"] == 0
    assert representative["href"] == "../Inbox/2026-03-02--codescout.md"
    assert representative["source_type"] == "paper"
    assert representative["confidence"] == "high"
