from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast

import pytest

from recoleta.presentation import (
    IdeaPresentationBuildRequest,
    PRESENTATION_SCHEMA_VERSION,
    TrendPresentationBuildRequest,
    build_idea_presentation_v2,
    build_trend_presentation_v2,
    idea_display_labels,
    presentation_sidecar_path,
    resolve_presentation_language_code,
    trend_display_labels,
    validate_presentation,
    write_presentation_sidecar,
)


def _idea(*, title: str, content_md: str = "Short idea note.") -> SimpleNamespace:
    return SimpleNamespace(
        title=title,
        content_md=content_md,
        evidence_refs=[
            SimpleNamespace(
                doc_id=11,
                chunk_index=0,
                reason="Grounded in the local corpus.",
                title="CodeScout",
                href="../Inbox/2026-03-02--codescout.md",
                authors=["Alice"],
                source_type="paper",
                confidence="high",
            )
        ],
    )


def test_build_trend_presentation_v2_projects_only_public_contract() -> None:
    presentation = build_trend_presentation_v2(
        request=TrendPresentationBuildRequest(
            source_markdown_path="Trends/day--2026-03-02--trend--7.md",
            title="Verification gets operational",
            overview_md="Teams are tightening release discipline.",
            clusters=[
                {
                    "title": "Release discipline",
                    "content_md": "Verification moved into the shipping path.",
                    "evidence_refs": [
                        {
                            "doc_id": 1,
                            "chunk_index": 0,
                            "title": "CodeScout",
                            "href": "../Inbox/2026-03-02--codescout.md",
                            "source_type": "paper",
                            "confidence": "high",
                            "reason": "The note ties verification to rollout control.",
                        }
                    ],
                }
            ],
        ),
    )

    assert presentation["presentation_schema_version"] == PRESENTATION_SCHEMA_VERSION
    assert presentation["display_labels"] == {
        "overview": "Overview",
        "clusters": "Clusters",
        "evidence": "Evidence",
    }
    cluster = presentation["content"]["clusters"][0]
    assert set(cluster) == {"title", "content", "evidence"}
    assert cluster["title"] == "Release discipline"
    assert cluster["content"] == "Verification moved into the shipping path."
    assert cluster["evidence"][0]["title"] == "CodeScout"
    assert cluster["evidence"][0]["reason"] == (
        "The note ties verification to rollout control."
    )
    assert "source_type" not in cluster["evidence"][0]
    assert "confidence" not in cluster["evidence"][0]


def test_build_idea_presentation_v2_caps_to_three_ideas() -> None:
    presentation = build_idea_presentation_v2(
        request=IdeaPresentationBuildRequest(
            source_markdown_path="Ideas/day--2026-03-02--ideas.md",
            title="Verification-first agent rollout",
            summary_md="Release discipline now feels operational.",
            ideas=[
                _idea(title="Idea 1"),
                _idea(title="Idea 2"),
                _idea(title="Idea 3"),
                _idea(title="Idea 4"),
            ],
        ),
    )

    assert presentation["display_labels"] == {
        "summary": "Summary",
        "ideas": "Ideas",
        "evidence": "Evidence",
    }
    assert [idea["title"] for idea in presentation["content"]["ideas"]] == [
        "Idea 1",
        "Idea 2",
        "Idea 3",
    ]


def test_validate_presentation_rejects_removed_reader_facing_fields() -> None:
    presentation = build_idea_presentation_v2(
        request=IdeaPresentationBuildRequest(
            source_markdown_path="Ideas/day--2026-03-02--ideas.md",
            title="Verification-first agent rollout",
            summary_md="Release discipline now feels operational.",
            ideas=[_idea(title="Prompt CI gate")],
        ),
    )
    presentation["display_labels"]["best_bet"] = "Best bet"
    presentation["content"]["ideas"][0]["evidence"][0]["source_type"] = "paper"
    presentation["content"]["ideas"][0]["evidence"][0]["confidence"] = "high"

    errors = validate_presentation(presentation)

    assert "display_labels must contain exactly: evidence, ideas, summary" in errors
    assert "idea content.ideas[0].evidence[0].source_type is not allowed" in errors
    assert "idea content.ideas[0].evidence[0].confidence is not allowed" in errors

def test_write_presentation_sidecar_rejects_invalid_contracts(tmp_path: Path) -> None:
    presentation = build_trend_presentation_v2(
        request=TrendPresentationBuildRequest(
            source_markdown_path="Trends/day--2026-03-02--trend--7.md",
            title="Verification gets operational",
            overview_md="Teams are tightening release discipline.",
            clusters=[],
        ),
    )
    presentation["content"]["clusters"] = "bad"

    with pytest.raises(ValueError, match="trend content.clusters must be a list"):
        write_presentation_sidecar(
            note_path=tmp_path / "Trends" / "day--2026-03-02--trend--7.md",
            presentation=presentation,
        )


def test_build_presentation_v2_rejects_missing_required_keywords() -> None:
    with pytest.raises(
        TypeError,
        match=r"missing 1 required keyword-only argument: 'request'",
    ):
        cast(Any, build_trend_presentation_v2)()

    with pytest.raises(
        TypeError, match=r"missing 1 required keyword-only argument: 'request'"
    ):
        cast(Any, build_idea_presentation_v2)()


def test_presentation_labels_stay_in_english_across_languages() -> None:
    assert trend_display_labels(language_code="zh-TW") == {
        "overview": "Overview",
        "clusters": "Clusters",
        "evidence": "Evidence",
    }
    assert idea_display_labels(language_code="zh-CN") == {
        "summary": "Summary",
        "ideas": "Ideas",
        "evidence": "Evidence",
    }


def test_resolve_presentation_language_code_prefers_explicit_codes() -> None:
    assert resolve_presentation_language_code(language_code="zh_CN") == "zh-CN"
    assert resolve_presentation_language_code(output_language="Chinese (Traditional)") == (
        "zh-TW"
    )
    assert resolve_presentation_language_code(output_language="English") == "en"
    assert resolve_presentation_language_code(output_language="") is None


def test_presentation_sidecar_path_uses_note_stem() -> None:
    note_path = Path("/tmp/Ideas/day--2026-03-02--ideas.md")
    assert presentation_sidecar_path(note_path=note_path) == Path(
        "/tmp/Ideas/day--2026-03-02--ideas.presentation.json"
    )
