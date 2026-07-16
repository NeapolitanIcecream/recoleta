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
    remove_note_projection_artifacts,
    resolve_presentation_language_code,
    trend_display_labels,
    validate_presentation,
    write_presentation_sidecar,
)


def test_remove_note_projection_artifacts_hides_note_first_and_attempts_all_cleanup(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    note_path = tmp_path / "Trends" / "day--2026-03-02--trend--7.md"
    note_path.parent.mkdir(parents=True)
    note_path.write_text("stale", encoding="utf-8")
    sidecar_path = presentation_sidecar_path(note_path=note_path)
    sidecar_path.write_text("{}", encoding="utf-8")
    pdf_path = note_path.with_suffix(".pdf")
    pdf_path.write_bytes(b"stale")
    debug_dir = note_path.parent / ".pdf-debug" / note_path.stem
    debug_dir.mkdir(parents=True)
    (debug_dir / "page.png").write_bytes(b"stale")

    real_unlink = Path.unlink
    attempted: list[Path] = []

    def _unlink(path: Path, *, missing_ok: bool = False) -> None:
        attempted.append(path)
        if path == note_path:
            raise OSError("simulated note cleanup failure")
        real_unlink(path, missing_ok=missing_ok)

    monkeypatch.setattr(Path, "unlink", _unlink)

    with pytest.raises(ExceptionGroup, match="failed to remove projection artifacts"):
        remove_note_projection_artifacts(note_path=note_path, include_pdf=True)

    assert attempted[0] == note_path
    assert note_path.exists()
    assert not sidecar_path.exists()
    assert not pdf_path.exists()
    assert not debug_dir.exists()


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
        "clusters": "Findings",
        "evidence": "Sources",
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
        "ideas": "Research ideas",
        "evidence": "Sources",
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


def test_presentation_labels_follow_the_reader_language() -> None:
    assert trend_display_labels(language_code="zh-TW") == {
        "overview": "概覽",
        "clusters": "研究發現",
        "evidence": "資料來源",
    }
    assert idea_display_labels(language_code="zh-CN") == {
        "summary": "摘要",
        "ideas": "研究想法",
        "evidence": "资料来源",
    }
    assert trend_display_labels(language_code="ja") == {
        "overview": "概要",
        "clusters": "主な発見",
        "evidence": "情報源",
    }
    assert idea_display_labels(language_code="ko") == {
        "summary": "요약",
        "ideas": "연구 아이디어",
        "evidence": "출처",
    }
    assert trend_display_labels(language_code="zh") == {
        "overview": "概览",
        "clusters": "研究发现",
        "evidence": "资料来源",
    }
    assert idea_display_labels(language_code="zh-Hant") == {
        "summary": "摘要",
        "ideas": "研究想法",
        "evidence": "資料來源",
    }
    assert trend_display_labels(language_code="zh-Hant-TW")["overview"] == "概覽"
    assert trend_display_labels(language_code="zh-Hans-CN")["overview"] == "概览"
    assert trend_display_labels(language_code="JA")["overview"] == "概要"


def test_resolve_presentation_language_code_prefers_explicit_codes() -> None:
    assert resolve_presentation_language_code(language_code="zh_CN") == "zh-CN"
    assert resolve_presentation_language_code(language_code="zh_hant_tw") == (
        "zh-Hant-TW"
    )
    assert resolve_presentation_language_code(language_code="JA") == "ja"
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
