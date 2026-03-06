from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path

from recoleta.site import export_trend_static_site, stage_trend_site_source
from recoleta.publish import write_markdown_trend_note


def test_export_trend_static_site_writes_home_topic_archive_and_detail_pages(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "notes"
    note_one = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=71,
        title="Agent Systems",
        granularity="day",
        period_start=datetime(2026, 2, 25, tzinfo=UTC),
        period_end=datetime(2026, 2, 26, tzinfo=UTC),
        run_id="run-site-1",
        overview_md="## TL;DR\n\n- Agent workflows are getting more production-ready.\n",
        topics=["agents", "tooling"],
        clusters=[],
        highlights=["Agent stacks are stabilizing."],
    )
    note_one.with_suffix(".pdf").write_bytes(b"%PDF-1.7\n")

    note_two = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=72,
        title="Embodied Systems",
        granularity="day",
        period_start=datetime(2026, 2, 26, tzinfo=UTC),
        period_end=datetime(2026, 2, 27, tzinfo=UTC),
        run_id="run-site-2",
        overview_md="## Overview\n\nEmbodied systems are moving toward modular execution.\n",
        topics=["robotics", "agents"],
        clusters=[],
        highlights=["Embodied models are becoming easier to steer."],
    )

    site_dir = tmp_path / "site"
    (site_dir / "trends").mkdir(parents=True, exist_ok=True)
    (site_dir / "trends" / "stale.html").write_text("obsolete\n", encoding="utf-8")
    manifest_path = export_trend_static_site(
        input_dir=output_dir / "Trends",
        output_dir=site_dir,
    )

    assert manifest_path == site_dir / "manifest.json"
    assert (site_dir / "index.html").exists()
    assert (site_dir / "archive.html").exists()
    assert (site_dir / "topics" / "index.html").exists()
    assert (site_dir / "topics" / "agents.html").exists()
    assert (site_dir / "trends" / f"{note_one.stem}.html").exists()
    assert (site_dir / "trends" / f"{note_two.stem}.html").exists()
    assert not (site_dir / "trends" / "stale.html").exists()
    assert (site_dir / "artifacts" / note_one.name).exists()
    assert (site_dir / "artifacts" / note_one.with_suffix(".pdf").name).exists()
    assert (site_dir / "assets" / "site.css").exists()
    assert (site_dir / ".nojekyll").exists()

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["trends_total"] == 2
    assert manifest["topics_total"] == 3

    index_html = (site_dir / "index.html").read_text(encoding="utf-8")
    assert "Recoleta Trends" in index_html
    assert "Agent Systems" in index_html
    assert "Embodied Systems" in index_html

    topic_html = (site_dir / "topics" / "agents.html").read_text(encoding="utf-8")
    assert "Agent Systems" in topic_html
    assert "Embodied Systems" in topic_html

    detail_html = (site_dir / "trends" / f"{note_one.stem}.html").read_text(
        encoding="utf-8"
    )
    assert "Source markdown" in detail_html
    assert "Download PDF" in detail_html


def test_stage_trend_site_source_mirrors_notes_and_cleans_stale_files(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "notes"
    note_one = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=71,
        title="Agent Systems",
        granularity="day",
        period_start=datetime(2026, 2, 25, tzinfo=UTC),
        period_end=datetime(2026, 2, 26, tzinfo=UTC),
        run_id="run-site-stage-1",
        overview_md="## TL;DR\n\n- Agent workflows are getting more production-ready.\n",
        topics=["agents", "tooling"],
        clusters=[],
        highlights=["Agent stacks are stabilizing."],
    )
    note_one.with_suffix(".pdf").write_bytes(b"%PDF-1.7\n")

    note_two = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=72,
        title="Embodied Systems",
        granularity="day",
        period_start=datetime(2026, 2, 26, tzinfo=UTC),
        period_end=datetime(2026, 2, 27, tzinfo=UTC),
        run_id="run-site-stage-2",
        overview_md="## Overview\n\nEmbodied systems are moving toward modular execution.\n",
        topics=["robotics", "agents"],
        clusters=[],
        highlights=["Embodied models are becoming easier to steer."],
    )

    staged_dir = tmp_path / "site-content" / "Trends"
    staged_dir.mkdir(parents=True, exist_ok=True)
    (staged_dir / "stale.md").write_text("obsolete\n", encoding="utf-8")

    manifest_path = stage_trend_site_source(
        input_dir=output_dir / "Trends",
        output_dir=staged_dir,
    )

    assert manifest_path == staged_dir / "manifest.json"
    assert (staged_dir / note_one.name).exists()
    assert (staged_dir / note_one.with_suffix(".pdf").name).exists()
    assert (staged_dir / note_two.name).exists()
    assert not (staged_dir / "stale.md").exists()

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["trends_total"] == 2
    assert manifest["pdf_total"] == 1
