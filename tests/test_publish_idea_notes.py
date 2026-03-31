from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

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
