from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path

from recoleta.site import (
    RECOLETA_QUICKSTART_URL,
    RECOLETA_REPO_URL,
    _item_action_label,
    export_trend_static_site,
)
from recoleta.passes.trend_ideas import TrendIdeasPayload
from recoleta.publish import write_markdown_ideas_note, write_markdown_trend_note
from recoleta.storage import Repository


def test_item_action_label_uses_known_source_hosts() -> None:
    assert (
        _item_action_label(
            source="",
            canonical_url="https://arxiv.org/abs/2603.02115",
        )
        == "Open arXiv"
    )
    assert (
        _item_action_label(
            source="",
            canonical_url="https://api.openreview.net/forum?id=test",
        )
        == "Open OpenReview"
    )
    assert (
        _item_action_label(
            source="",
            canonical_url="https://gist.github.com/octocat/example",
        )
        == "Open GitHub"
    )


def test_item_action_label_ignores_partial_domain_suffix_matches() -> None:
    assert (
        _item_action_label(
            source="",
            canonical_url="https://notarxiv.org/abs/2603.02115",
        )
        == "Open original"
    )
    assert (
        _item_action_label(
            source="",
            canonical_url="https://mirroropenreview.net/forum?id=test",
        )
        == "Open original"
    )


def test_export_trend_static_site_renders_new_trend_and_idea_contracts(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "notes"
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()

    trend_note = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=71,
        title="Agent systems",
        granularity="day",
        period_start=datetime(2026, 2, 25, tzinfo=UTC),
        period_end=datetime(2026, 2, 26, tzinfo=UTC),
        run_id="run-site-1",
        overview_md="Agent workflows are getting more production-ready.",
        topics=["agents", "tooling"],
        clusters=[
            {
                "title": "Release discipline",
                "content_md": "Verification moved into the shipping path.",
                "evidence_refs": [
                    {
                        "doc_id": 1,
                        "chunk_index": 0,
                        "title": "CodeScout",
                        "href": "../Inbox/2026-02-25--codescout.md",
                        "reason": "The note grounds release discipline in the corpus.",
                    }
                ],
            }
        ],
    )
    trend_note.with_suffix(".pdf").write_bytes(b"%PDF-1.7\n")

    _ = write_markdown_ideas_note(
        repository=repository,
        output_dir=output_dir,
        pass_output_id=9,
        upstream_pass_output_id=7,
        granularity="day",
        period_start=datetime(2026, 2, 25, tzinfo=UTC),
        period_end=datetime(2026, 2, 26, tzinfo=UTC),
        run_id="run-site-ideas",
        status="succeeded",
        payload=TrendIdeasPayload.model_validate(
            {
                "title": "Operator wedges",
                "granularity": "day",
                "period_start": datetime(2026, 2, 25, tzinfo=UTC).isoformat(),
                "period_end": datetime(2026, 2, 26, tzinfo=UTC).isoformat(),
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
        ),
        topics=["agents"],
    )

    site_dir = tmp_path / "site"
    manifest_path = export_trend_static_site(
        input_dir=output_dir / "Trends",
        output_dir=site_dir,
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    trend_html = (site_dir / "trends" / f"{trend_note.stem}.html").read_text(
        encoding="utf-8"
    )
    ideas_html = (site_dir / "ideas" / "day--2026-02-25--ideas.html").read_text(
        encoding="utf-8"
    )
    index_html = (site_dir / "index.html").read_text(encoding="utf-8")

    assert manifest["trends_total"] == 1
    assert "Overview" in trend_html
    assert "Clusters" in trend_html
    assert "Evidence" in trend_html
    assert "Top shifts" not in trend_html
    assert "Counter-signal" not in trend_html
    assert "Representative sources" not in trend_html
    assert "Summary" in ideas_html
    assert "Ideas" in ideas_html
    assert "Prompt release gate" in ideas_html
    assert "Best bet" not in ideas_html
    assert "Alternate" not in ideas_html
    assert "Anti-thesis" not in ideas_html
    assert "Agent systems" in index_html
    assert RECOLETA_REPO_URL in index_html
    assert RECOLETA_QUICKSTART_URL in index_html
