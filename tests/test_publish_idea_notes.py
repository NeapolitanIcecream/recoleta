from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path

import pytest

import recoleta.publish.idea_notes as idea_notes_module
from recoleta.presentation import presentation_sidecar_path, validate_presentation
from recoleta.passes.trend_ideas import TrendIdeasPayload
from recoleta.publish import write_markdown_ideas_note
from recoleta.publish.item_notes import resolve_item_note_href
from recoleta.storage import Repository
from recoleta.types import ItemDraft


def test_write_markdown_ideas_note_deduplicates_evidence_refs_by_document(
    tmp_path: Path,
) -> None:
    """Regression: one article should render once even if the idea cites multiple chunks."""

    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()

    published_at = datetime(2026, 3, 2, 12, tzinfo=UTC)
    item, _ = repository.upsert_item(
        ItemDraft.from_values(
            source="rss",
            source_item_id="grounded-runtime",
            canonical_url="https://example.com/grounded-runtime",
            title="Grounded Agent Runtime for Long-Horizon Evaluation",
            authors=["Alice"],
            published_at=published_at,
        )
    )
    assert item.id is not None
    persisted_item = repository.get_item(item_id=int(item.id))
    assert persisted_item is not None
    doc = repository.upsert_document_for_item(item=persisted_item)
    assert doc.id is not None
    repository.upsert_document_chunk(
        doc_id=int(doc.id),
        chunk_index=0,
        kind="summary",
        text_value="Grounded runtime traces make long-horizon evaluation auditable.",
        source_content_type="analysis_summary",
    )
    repository.upsert_document_chunk(
        doc_id=int(doc.id),
        chunk_index=1,
        kind="content",
        text_value="The body chunk shows how verifier loops inspect long traces.",
        source_content_type="analysis_body",
    )

    period_start = datetime(2026, 3, 2, tzinfo=UTC)
    period_end = datetime(2026, 3, 3, tzinfo=UTC)
    output_dir = tmp_path / "notes"
    note_path = write_markdown_ideas_note(
        repository=repository,
        output_dir=output_dir,
        pass_output_id=7,
        upstream_pass_output_id=3,
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        run_id="run-ideas-dedup-evidence",
        status="succeeded",
        payload=TrendIdeasPayload.model_validate(
            {
                "title": "Why now ideas",
                "granularity": "day",
                "period_start": period_start.isoformat(),
                "period_end": period_end.isoformat(),
                "summary_md": "One idea is clearly grounded.",
                "ideas": [
                    {
                        "title": "Auditable long-horizon eval workbench",
                        "kind": "tooling_wedge",
                        "thesis": "Build an evaluation workbench around grounded traces.",
                        "anti_thesis": "This thesis weakens if teams refuse to add release gates to the workflow.",
                        "why_now": "Grounded runtime traces are now practical.",
                        "what_changed": "Teams can inspect long multi-step traces.",
                        "user_or_job": "Evaluation teams need auditable agent runs.",
                        "evidence_refs": [
                            {
                                "doc_id": int(doc.id),
                                "chunk_index": 0,
                                "reason": "The summary establishes the need for auditable traces.",
                            },
                            {
                                "doc_id": int(doc.id),
                                "chunk_index": 1,
                                "reason": "The body chunk shows verifier loops over long traces.",
                            },
                        ],
                        "validation_next_step": "Prototype a trace viewer for one benchmark workflow.",
                        "time_horizon": "now",
                    }
                ],
            }
        ),
        topics=["agents"],
    )

    note_text = note_path.read_text(encoding="utf-8")
    href = resolve_item_note_href(
        note_dir=output_dir / "Inbox",
        from_dir=output_dir / "Ideas",
        item_id=int(item.id),
        title=persisted_item.title,
        canonical_url=persisted_item.canonical_url,
        published_at=persisted_item.published_at,
    )

    assert (
        note_text.count(
            f"[Grounded Agent Runtime for Long-Horizon Evaluation]({href})"
        )
        == 1
    )
    assert (
        f"- [Grounded Agent Runtime for Long-Horizon Evaluation]({href})\n"
        "  - The summary establishes the need for auditable traces.\n"
        "  - The body chunk shows verifier loops over long traces."
    ) in note_text
    assert "The summary establishes the need for auditable traces." in note_text
    assert "The body chunk shows verifier loops over long traces." in note_text
    assert "; The body chunk shows verifier loops over long traces." not in note_text
    assert "(chunk 1)" not in note_text


def test_write_markdown_ideas_note_rejects_unexpected_keyword_arguments(
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    period_start = datetime(2026, 3, 2, tzinfo=UTC)
    period_end = datetime(2026, 3, 3, tzinfo=UTC)

    with pytest.raises(TypeError, match="unexpected keyword argument 'statsu'"):
        write_markdown_ideas_note(
            repository=repository,
            output_dir=tmp_path / "notes",
            granularity="day",
            period_start=period_start,
            period_end=period_end,
            run_id="run-ideas-typo",
            statsu="succeeded",
            payload=TrendIdeasPayload.model_validate(
                {
                    "title": "Why now ideas",
                    "granularity": "day",
                    "period_start": period_start.isoformat(),
                    "period_end": period_end.isoformat(),
                    "summary_md": "One idea is clearly grounded.",
                    "ideas": [],
                }
            ),
        )


def test_write_markdown_ideas_note_rejects_missing_required_keywords(
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    period_start = datetime(2026, 3, 2, tzinfo=UTC)
    period_end = datetime(2026, 3, 3, tzinfo=UTC)

    with pytest.raises(
        TypeError,
        match="missing required keyword-only arguments: 'pass_output_id', 'upstream_pass_output_id', 'status'",
    ):
        write_markdown_ideas_note(
            repository=repository,
            output_dir=tmp_path / "notes",
            granularity="day",
            period_start=period_start,
            period_end=period_end,
            run_id="run-ideas-missing-status",
            payload=TrendIdeasPayload.model_validate(
                {
                    "title": "Why now ideas",
                    "granularity": "day",
                    "period_start": period_start.isoformat(),
                    "period_end": period_end.isoformat(),
                    "summary_md": "One idea is clearly grounded.",
                    "ideas": [],
                }
            ),
        )


def test_write_markdown_ideas_note_requires_pass_output_ids(
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    period_start = datetime(2026, 3, 2, tzinfo=UTC)
    period_end = datetime(2026, 3, 3, tzinfo=UTC)

    with pytest.raises(
        TypeError,
        match="missing required keyword-only arguments: 'pass_output_id', 'upstream_pass_output_id'",
    ):
        write_markdown_ideas_note(
            repository=repository,
            output_dir=tmp_path / "notes",
            granularity="day",
            period_start=period_start,
            period_end=period_end,
            run_id="run-ideas-missing-pass-ids",
            status="succeeded",
            payload=TrendIdeasPayload.model_validate(
                {
                    "title": "Why now ideas",
                    "granularity": "day",
                    "period_start": period_start.isoformat(),
                    "period_end": period_end.isoformat(),
                    "summary_md": "One idea is clearly grounded.",
                    "ideas": [],
                }
            ),
        )


def test_write_markdown_ideas_note_emits_reader_facing_markdown_and_sidecar(
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
        run_id="run-ideas-sidecar",
        status="succeeded",
        payload=TrendIdeasPayload.model_validate(
            {
                "title": "Why now ideas",
                "granularity": "day",
                "period_start": period_start.isoformat(),
                "period_end": period_end.isoformat(),
                "summary_md": "One idea is clearly grounded.",
                "ideas": [
                    {
                        "title": "Auditable long-horizon eval workbench",
                        "kind": "tooling_wedge",
                        "thesis": "Build an evaluation workbench around grounded traces.",
                        "anti_thesis": "This thesis weakens if teams refuse to add release gates to the workflow.",
                        "why_now": "Grounded runtime traces are now practical.",
                        "what_changed": "Teams can inspect long multi-step traces.",
                        "user_or_job": "Evaluation teams need auditable agent runs.",
                        "evidence_refs": [
                            {
                                "doc_id": 11,
                                "chunk_index": 0,
                                "reason": "Trace quality is visible in the corpus.",
                            }
                        ],
                        "validation_next_step": "Prototype a trace viewer for one benchmark workflow.",
                        "time_horizon": "now",
                    },
                    {
                        "title": "Review queue for flaky eval regressions",
                        "kind": "workflow_shift",
                        "thesis": "Route unstable eval runs into a structured triage lane.",
                        "anti_thesis": "This thesis weakens if flaky failures stay too rare to justify a dedicated queue.",
                        "why_now": "Teams are seeing repeated long-horizon failures.",
                        "what_changed": "Higher usage creates recurring review patterns.",
                        "user_or_job": "Applied AI ops",
                        "evidence_refs": [
                            {
                                "doc_id": 12,
                                "chunk_index": 0,
                                "reason": "Repeated failures are visible in the corpus.",
                            }
                        ],
                        "validation_next_step": "Pilot the queue on one benchmark family.",
                        "time_horizon": "near",
                    },
                ],
            }
        ),
        topics=["agents"],
    )

    note_text = note_path.read_text(encoding="utf-8")
    sidecar_path = presentation_sidecar_path(note_path=note_path)
    sidecar = json.loads(sidecar_path.read_text(encoding="utf-8"))

    assert "### Best bet: Auditable long-horizon eval workbench" in note_text
    assert "### Alternate: Review queue for flaky eval regressions" in note_text
    assert "- Type: Tooling wedge" in note_text
    assert "- Horizon: Near-term" in note_text
    assert "- Role: Evaluation teams need auditable agent runs." in note_text
    assert (
        "**Anti-thesis.** This thesis weakens if teams refuse to add release gates to the workflow."
        in note_text
    )
    assert "Kind:" not in note_text
    assert "Time horizon:" not in note_text
    assert "User/job:" not in note_text

    assert sidecar_path.exists()
    assert sidecar["presentation_schema_version"] == 2
    assert sidecar["surface_kind"] == "idea"
    assert sidecar["source_markdown_path"] == f"Ideas/{note_path.name}"
    assert sidecar["display_labels"]["best_bet"] == "Best bet"
    assert sidecar["display_labels"]["anti_thesis"] == "Anti-thesis"
    assert sidecar["content"]["opportunities"][0]["tier"] == "best_bet"
    assert sidecar["content"]["opportunities"][1]["tier"] == "alternate"
    assert sidecar["content"]["opportunities"][0]["display_kind"] == "Tooling wedge"
    assert sidecar["content"]["opportunities"][1]["display_time_horizon"] == "Near-term"
    assert sidecar["content"]["opportunities"][0]["anti_thesis"].startswith(
        "This thesis weakens if teams refuse"
    )
    assert sidecar["content"]["opportunities"][0]["evidence"][0]["doc_id"] == 11
    assert sidecar["content"]["opportunities"][0]["evidence"][0]["chunk_index"] == 0
    assert sidecar["content"]["opportunities"][0]["evidence"][0]["source_type"] == "unknown"
    assert sidecar["content"]["opportunities"][0]["evidence"][0]["confidence"] == "low"
    assert validate_presentation(sidecar) == []


def test_write_markdown_ideas_note_skips_sidecar_for_suppressed_empty_payload(
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
        run_id="run-ideas-suppressed-sidecar",
        status="suppressed",
        payload=TrendIdeasPayload.model_validate(
            {
                "title": "No publishable ideas for this period",
                "granularity": "day",
                "period_start": period_start.isoformat(),
                "period_end": period_end.isoformat(),
                "summary_md": "Evidence is too thin for a durable opportunity brief.",
                "ideas": [],
            }
        ),
        topics=["agents"],
    )

    assert note_path.exists()
    assert not presentation_sidecar_path(note_path=note_path).exists()


def test_write_markdown_ideas_note_keeps_markdown_and_sidecar_opportunities_in_sync(
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    period_start = datetime(2026, 3, 2, tzinfo=UTC)
    period_end = datetime(2026, 3, 3, tzinfo=UTC)

    payload = TrendIdeasPayload.model_validate(
        {
            "title": "Why now ideas",
            "granularity": "day",
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat(),
            "summary_md": "Several ideas are available.",
            "ideas": [
                {
                    "title": "Idea one",
                    "kind": "tooling_wedge",
                    "thesis": "First idea.",
                    "why_now": "Now.",
                    "what_changed": "Change one.",
                    "user_or_job": "Role one",
                    "evidence_refs": [],
                    "validation_next_step": "Test one.",
                    "time_horizon": "now",
                },
                {
                    "title": "Idea two",
                    "kind": "workflow_shift",
                    "thesis": "Second idea.",
                    "why_now": "Now.",
                    "what_changed": "Change two.",
                    "user_or_job": "Role two",
                    "evidence_refs": [],
                    "validation_next_step": "Test two.",
                    "time_horizon": "near",
                },
                {
                    "title": "Idea three",
                    "kind": "research_gap",
                    "thesis": "Third idea.",
                    "why_now": "Now.",
                    "what_changed": "Change three.",
                    "user_or_job": "Role three",
                    "evidence_refs": [],
                    "validation_next_step": "Test three.",
                    "time_horizon": "frontier",
                },
                {
                    "title": "Idea four",
                    "kind": "new_build",
                    "thesis": "Fourth idea.",
                    "why_now": "Now.",
                    "what_changed": "Change four.",
                    "user_or_job": "Role four",
                    "evidence_refs": [],
                    "validation_next_step": "Test four.",
                    "time_horizon": "near",
                },
            ],
        }
    )

    note_path = write_markdown_ideas_note(
        repository=repository,
        output_dir=tmp_path / "notes",
        pass_output_id=7,
        upstream_pass_output_id=3,
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        run_id="run-ideas-sync",
        status="succeeded",
        payload=payload,
        topics=["agents"],
    )

    note_text = note_path.read_text(encoding="utf-8")
    sidecar = json.loads(
        presentation_sidecar_path(note_path=note_path).read_text(encoding="utf-8")
    )

    assert "### Best bet: Idea one" in note_text
    assert "### Alternate: Idea two" in note_text
    assert "### Alternate: Idea three" in note_text
    assert "Idea four" not in note_text
    assert [entry["title"] for entry in sidecar["content"]["opportunities"]] == [
        "Idea one",
        "Idea two",
        "Idea three",
    ]


def test_write_markdown_ideas_note_infers_sidecar_language_code_from_output_language(
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
        run_id="run-ideas-language",
        status="succeeded",
        payload=TrendIdeasPayload.model_validate(
            {
                "title": "机会判断",
                "granularity": "day",
                "period_start": period_start.isoformat(),
                "period_end": period_end.isoformat(),
                "summary_md": "一个机会已经足够清晰。",
                "ideas": [
                    {
                        "title": "可审计评测工作台",
                        "kind": "tooling_wedge",
                        "thesis": "先把长链路轨迹做成可审计工作台。",
                        "why_now": "长时序 trace 终于足够稳定。",
                        "what_changed": "团队现在会反复回看同一条代理轨迹。",
                        "user_or_job": "评测团队需要可追责的 agent 运行记录。",
                        "evidence_refs": [],
                        "validation_next_step": "先在一个 benchmark 工作流上试跑。",
                        "time_horizon": "now",
                    }
                ],
            }
        ),
        topics=["agents"],
        output_language="Chinese (Simplified)",
    )

    note_text = note_path.read_text(encoding="utf-8")
    sidecar = json.loads(
        presentation_sidecar_path(note_path=note_path).read_text(encoding="utf-8")
    )

    assert "language_code: zh-CN" in note_text
    assert "## Summary" in note_text
    assert "## 摘要" not in note_text
    assert "### Best bet:" in note_text
    assert sidecar["language_code"] == "zh-CN"
    assert sidecar["display_labels"]["summary"] == "Summary"
    assert sidecar["display_labels"]["best_bet"] == "Best bet"


def test_write_markdown_ideas_note_emits_localized_labels_and_sidecar_in_localized_tree(
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    period_start = datetime(2026, 3, 2, tzinfo=UTC)
    period_end = datetime(2026, 3, 3, tzinfo=UTC)

    note_path = write_markdown_ideas_note(
        repository=repository,
        output_dir=tmp_path / "Localized" / "zh-cn",
        pass_output_id=7,
        upstream_pass_output_id=3,
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        run_id="run-ideas-zh-localized",
        status="succeeded",
        payload=TrendIdeasPayload.model_validate(
            {
                "title": "验证优先的智能体发布",
                "granularity": "day",
                "period_start": period_start.isoformat(),
                "period_end": period_end.isoformat(),
                "summary_md": "先把提示词变更纳入可审计发布流程。",
                "ideas": [
                    {
                        "title": "提示词发布闸门",
                        "kind": "tooling_wedge",
                        "thesis": "先在生产前加一层提示词发布闸门。",
                        "why_now": "提示词和工具配置已经变成连续发布对象。",
                        "what_changed": "团队现在会持续回滚和复盘代理改动。",
                        "user_or_job": "负责代理发布的平台工程团队。",
                        "evidence_refs": [],
                        "validation_next_step": "先拿一个高频工作流回放 20 次改动。",
                        "time_horizon": "now",
                    }
                ],
            }
        ),
        topics=["agents"],
        output_language="Chinese (Simplified)",
        language_code="zh-CN",
    )

    note_text = note_path.read_text(encoding="utf-8")
    sidecar_path = presentation_sidecar_path(note_path=note_path)
    sidecar = json.loads(sidecar_path.read_text(encoding="utf-8"))

    assert "### 首要机会: 提示词发布闸门" in note_text
    assert "- 类型: 工具切入点" in note_text
    assert "- 时间范围: 现在" in note_text
    assert "- 适用角色: 负责代理发布的平台工程团队。" in note_text
    assert "**核心判断" in note_text
    assert "**下一步验证" in note_text
    assert "Type:" not in note_text
    assert "Horizon:" not in note_text
    assert "Role:" not in note_text

    assert sidecar_path.exists()
    assert sidecar["language_code"] == "zh-CN"
    assert sidecar["display_labels"]["best_bet"] == "首要机会"
    assert sidecar["content"]["opportunities"][0]["display_kind"] == "工具切入点"
    assert sidecar["content"]["opportunities"][0]["display_time_horizon"] == "现在"


def test_write_markdown_ideas_note_rolls_back_markdown_when_sidecar_write_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    period_start = datetime(2026, 3, 2, tzinfo=UTC)
    period_end = datetime(2026, 3, 3, tzinfo=UTC)
    note_path = idea_notes_module.resolve_ideas_note_path(
        note_dir=tmp_path / "notes" / "Ideas",
        granularity="day",
        period_start=period_start,
    )

    def _explode_sidecar(*, note_path, presentation):  # type: ignore[no-untyped-def]
        _ = (note_path, presentation)
        raise ValueError("invalid presentation sidecar")

    monkeypatch.setattr(
        idea_notes_module,
        "write_presentation_sidecar",
        _explode_sidecar,
    )

    with pytest.raises(ValueError, match="invalid presentation sidecar"):
        write_markdown_ideas_note(
            repository=repository,
            output_dir=tmp_path / "notes",
            pass_output_id=7,
            upstream_pass_output_id=3,
            granularity="day",
            period_start=period_start,
            period_end=period_end,
            run_id="run-ideas-rollback",
            status="succeeded",
            payload=TrendIdeasPayload.model_validate(
                {
                    "title": "Why now ideas",
                    "granularity": "day",
                    "period_start": period_start.isoformat(),
                    "period_end": period_end.isoformat(),
                    "summary_md": "One idea is clearly grounded.",
                    "ideas": [
                        {
                            "title": "Auditable long-horizon eval workbench",
                            "kind": "tooling_wedge",
                            "thesis": "Build an evaluation workbench around grounded traces.",
                            "why_now": "Grounded runtime traces are now practical.",
                            "what_changed": "Teams can inspect long multi-step traces.",
                            "user_or_job": "Evaluation teams need auditable agent runs.",
                            "evidence_refs": [],
                            "validation_next_step": "Prototype a trace viewer for one benchmark workflow.",
                            "time_horizon": "now",
                        }
                    ],
                }
            ),
            topics=["agents"],
        )

    assert not note_path.exists()
    assert not presentation_sidecar_path(note_path=note_path).exists()
