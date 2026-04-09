from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path

from recoleta.materialize import MaterializeTargetSpec, materialize_outputs
from recoleta.passes.base import PassInputRef
from recoleta.passes.trend_ideas import TrendIdeasPayload
from recoleta.presentation import presentation_sidecar_path, validate_presentation
from recoleta.storage import Repository
from recoleta.trends import TrendPayload, persist_trend_payload


def _seed_trend_and_ideas(repository: Repository) -> tuple[int, int]:
    period_start = datetime(2026, 3, 16, tzinfo=UTC)
    period_end = datetime(2026, 3, 23, tzinfo=UTC)

    trend_payload = TrendPayload.model_validate(
        {
            "title": "Verification gets operational",
            "granularity": "week",
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat(),
            "overview_md": "Release discipline is moving into the main workflow.",
            "topics": ["agents", "tooling"],
            "clusters": [
                {
                    "title": "Release discipline",
                    "content_md": "Verification and rollout now share the same operational lane.",
                    "evidence_refs": [
                        {
                            "doc_id": 1,
                            "chunk_index": 0,
                            "title": "CodeScout",
                            "href": "../Inbox/2026-03-16--codescout.md",
                            "reason": "The corpus ties verification to rollout control.",
                        }
                    ],
                }
            ],
        }
    )
    trend_row = repository.create_pass_output(
        run_id="run-w12-trend",
        pass_kind="trend_synthesis",
        status="succeeded",
        granularity="week",
        period_start=period_start,
        period_end=period_end,
        payload=trend_payload.model_dump(mode="json"),
    )
    assert trend_row.id is not None
    trend_doc_id = persist_trend_payload(
        repository=repository,
        granularity="week",
        period_start=period_start,
        period_end=period_end,
        payload=trend_payload,
        pass_output_id=int(trend_row.id),
    )

    ideas_payload = TrendIdeasPayload.model_validate(
        {
            "title": "Verification-first agent rollout",
            "granularity": "week",
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat(),
            "summary_md": "Structured release controls now feel overdue.",
            "ideas": [
                {
                    "title": "Prompt release gate",
                    "content_md": "Add a release gate before prompt rollout.",
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
    ideas_row = repository.create_pass_output(
        run_id="run-w12-ideas",
        pass_kind="trend_ideas",
        status="succeeded",
        granularity="week",
        period_start=period_start,
        period_end=period_end,
        payload=ideas_payload.model_dump(mode="json"),
        input_refs=[
            PassInputRef(
                ref_kind="pass_output",
                pass_kind="trend_synthesis",
                granularity="week",
                period_start=period_start.isoformat(),
                period_end=period_end.isoformat(),
                pass_output_id=int(trend_row.id),
            ).model_dump(mode="json")
        ],
    )
    assert ideas_row.id is not None
    idea_doc = repository.upsert_document_for_idea(
        granularity="week",
        period_start=period_start,
        period_end=period_end,
        title="Verification-first agent rollout",
    )
    assert idea_doc.id is not None
    repository.upsert_document_chunk(
        doc_id=int(idea_doc.id),
        chunk_index=0,
        kind="summary",
        text_value=ideas_payload.summary_md,
        source_content_type="trend_ideas_summary",
    )
    repository.upsert_document_chunk(
        doc_id=int(idea_doc.id),
        chunk_index=1,
        kind="meta",
        text_value=json.dumps(ideas_payload.model_dump(mode="json"), ensure_ascii=False),
        source_content_type="trend_ideas_payload_json",
    )
    return int(trend_doc_id), int(idea_doc.id)


def test_materialize_outputs_uses_new_reader_facing_contracts(tmp_path: Path) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    trend_doc_id, _idea_doc_id = _seed_trend_and_ideas(repository)
    output_dir = tmp_path / "outputs"

    result = materialize_outputs(
        repository=repository,
        target_spec=MaterializeTargetSpec(output_dir=output_dir),
        site_input_dir=output_dir,
        site_output_dir=output_dir / "site",
    )

    assert result.site_manifest_path is not None

    trend_note = output_dir / "Trends" / f"week--2026-W12--trend--{trend_doc_id}.md"
    idea_note = output_dir / "Ideas" / "week--2026-W12--ideas.md"
    trend_sidecar = json.loads(
        presentation_sidecar_path(note_path=trend_note).read_text(encoding="utf-8")
    )
    idea_sidecar = json.loads(
        presentation_sidecar_path(note_path=idea_note).read_text(encoding="utf-8")
    )
    trend_text = trend_note.read_text(encoding="utf-8")
    idea_text = idea_note.read_text(encoding="utf-8")
    trend_html = (output_dir / "site" / "trends" / f"{trend_note.stem}.html").read_text(
        encoding="utf-8"
    )
    idea_html = (output_dir / "site" / "ideas" / f"{idea_note.stem}.html").read_text(
        encoding="utf-8"
    )

    assert validate_presentation(trend_sidecar) == []
    assert validate_presentation(idea_sidecar) == []

    assert "## Overview" in trend_text
    assert "## Clusters" in trend_text
    assert "Top shifts" not in trend_text
    assert "Counter-signal" not in trend_text
    assert "Representative sources" not in trend_text
    assert "## Summary" in idea_text
    assert "## Prompt release gate" in idea_text
    assert "Idea brief" not in idea_html
    assert "Opportunities" not in idea_html
    assert "Idea notes from the trend snapshot" not in idea_html
    assert "Evidence-grounded idea notes" not in idea_html
    assert "Best bet" not in idea_text
    assert "Alternate" not in idea_text
    assert "Anti-thesis" not in idea_text

    assert "ranked_shifts" not in trend_sidecar["content"]
    assert "counter_signal" not in trend_sidecar["content"]
    assert "representative_sources" not in trend_sidecar["content"]
    assert "opportunities" not in idea_sidecar["content"]

    assert "Overview" in trend_html
    assert "Clusters" in trend_html
    assert "Trend brief" not in trend_html
    assert "Trends · 2026-W12" in trend_html
    assert "Top shifts" not in trend_html
    assert "Summary" in idea_html
    assert "Ideas" in idea_html
    assert "Best bet" not in idea_html
