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


def test_export_trend_static_site_aggregates_topic_stream_inputs_and_writes_stream_pages(
    tmp_path: Path,
) -> None:
    notes_root = tmp_path / "notes"
    agents_root = notes_root / "Streams" / "agents_lab"
    bio_root = notes_root / "Streams" / "bio_watch"

    agents_note = write_markdown_trend_note(
        output_dir=agents_root,
        trend_doc_id=91,
        title="Agent Systems",
        granularity="day",
        period_start=datetime(2026, 2, 25, tzinfo=UTC),
        period_end=datetime(2026, 2, 26, tzinfo=UTC),
        run_id="run-stream-site-1",
        overview_md="## TL;DR\n\n- Agent workflows are getting more production-ready.\n",
        topics=["agents", "tooling"],
        clusters=[],
        highlights=["Agent stacks are stabilizing."],
    )
    agents_note.with_suffix(".pdf").write_bytes(b"%PDF-1.7\n")

    bio_note = write_markdown_trend_note(
        output_dir=bio_root,
        trend_doc_id=92,
        title="Therapeutics Watch",
        granularity="day",
        period_start=datetime(2026, 2, 26, tzinfo=UTC),
        period_end=datetime(2026, 2, 27, tzinfo=UTC),
        run_id="run-stream-site-2",
        overview_md="## Overview\n\nTherapeutics programs are branching into narrower lines.\n",
        topics=["biology", "therapeutics"],
        clusters=[],
        highlights=["Programs are diverging into specialist tracks."],
    )

    site_dir = tmp_path / "site"
    manifest_path = export_trend_static_site(
        input_dir=notes_root,
        output_dir=site_dir,
    )

    assert manifest_path == site_dir / "manifest.json"
    assert (site_dir / "streams" / "index.html").exists()
    assert (site_dir / "streams" / "agents-lab.html").exists()
    assert (site_dir / "streams" / "bio-watch.html").exists()
    assert (site_dir / "trends" / f"{agents_note.stem}.html").exists()
    assert (site_dir / "trends" / f"{bio_note.stem}.html").exists()

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["trends_total"] == 2
    assert manifest["streams_total"] == 2
    assert len(manifest["input_dirs"]) == 2

    index_html = (site_dir / "index.html").read_text(encoding="utf-8")
    assert "agents_lab" in index_html
    assert "bio_watch" in index_html

    stream_html = (site_dir / "streams" / "agents-lab.html").read_text(
        encoding="utf-8"
    )
    assert "Agent Systems" in stream_html

    detail_html = (site_dir / "trends" / f"{agents_note.stem}.html").read_text(
        encoding="utf-8"
    )
    assert "agents_lab" in detail_html


def test_stage_trend_site_source_preserves_topic_stream_directory_layout(
    tmp_path: Path,
) -> None:
    notes_root = tmp_path / "notes"
    agents_root = notes_root / "Streams" / "agents_lab"
    bio_root = notes_root / "Streams" / "bio_watch"

    agents_note = write_markdown_trend_note(
        output_dir=agents_root,
        trend_doc_id=101,
        title="Agent Systems",
        granularity="day",
        period_start=datetime(2026, 2, 25, tzinfo=UTC),
        period_end=datetime(2026, 2, 26, tzinfo=UTC),
        run_id="run-stream-stage-1",
        overview_md="## TL;DR\n\n- Agent workflows are getting more production-ready.\n",
        topics=["agents", "tooling"],
        clusters=[],
        highlights=["Agent stacks are stabilizing."],
    )
    agents_note.with_suffix(".pdf").write_bytes(b"%PDF-1.7\n")

    bio_note = write_markdown_trend_note(
        output_dir=bio_root,
        trend_doc_id=102,
        title="Therapeutics Watch",
        granularity="day",
        period_start=datetime(2026, 2, 26, tzinfo=UTC),
        period_end=datetime(2026, 2, 27, tzinfo=UTC),
        run_id="run-stream-stage-2",
        overview_md="## Overview\n\nTherapeutics programs are branching into narrower lines.\n",
        topics=["biology", "therapeutics"],
        clusters=[],
        highlights=["Programs are diverging into specialist tracks."],
    )

    staged_root = tmp_path / "site-content"
    manifest_path = stage_trend_site_source(
        input_dir=notes_root,
        output_dir=staged_root,
    )

    assert manifest_path == staged_root / "manifest.json"
    assert (
        staged_root / "Streams" / "agents_lab" / "Trends" / agents_note.name
    ).exists()
    assert (
        staged_root
        / "Streams"
        / "agents_lab"
        / "Trends"
        / agents_note.with_suffix(".pdf").name
    ).exists()
    assert (
        staged_root / "Streams" / "bio_watch" / "Trends" / bio_note.name
    ).exists()

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["trends_total"] == 2
    assert manifest["pdf_total"] == 1
    assert manifest["streams_total"] == 2


def test_stage_trend_site_source_places_non_stream_notes_under_trends_when_streams_exist(
    tmp_path: Path,
) -> None:
    notes_root = tmp_path / "notes"
    legacy_note = write_markdown_trend_note(
        output_dir=notes_root,
        trend_doc_id=111,
        title="Legacy Daily Watch",
        granularity="day",
        period_start=datetime(2026, 2, 27, tzinfo=UTC),
        period_end=datetime(2026, 2, 28, tzinfo=UTC),
        run_id="run-mixed-stage-1",
        overview_md="## TL;DR\n\n- Legacy single-stream trend note.\n",
        topics=["agents"],
        clusters=[],
        highlights=["Legacy note stays visible in the staged site."],
    )
    legacy_note.with_suffix(".pdf").write_bytes(b"%PDF-1.7\n")

    stream_root = notes_root / "Streams" / "agents_lab"
    stream_note = write_markdown_trend_note(
        output_dir=stream_root,
        trend_doc_id=112,
        title="Agent Systems",
        granularity="day",
        period_start=datetime(2026, 2, 28, tzinfo=UTC),
        period_end=datetime(2026, 3, 1, tzinfo=UTC),
        run_id="run-mixed-stage-2",
        overview_md="## Overview\n\nStream-local trend note.\n",
        topics=["agents", "tooling"],
        clusters=[],
        highlights=["Stream note should stay under Streams/<name>/Trends."],
    )
    stream_note.with_suffix(".pdf").write_bytes(b"%PDF-1.7\n")

    staged_root = tmp_path / "site-content"
    manifest_path = stage_trend_site_source(
        input_dir=notes_root,
        output_dir=staged_root,
    )

    assert manifest_path == staged_root / "manifest.json"
    assert (staged_root / "Trends" / legacy_note.name).exists()
    assert (staged_root / "Trends" / legacy_note.with_suffix(".pdf").name).exists()
    assert (
        staged_root / "Streams" / "agents_lab" / "Trends" / stream_note.name
    ).exists()

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert "Trends/" + legacy_note.name in manifest["files"]["markdown"]
    assert (
        "Streams/agents_lab/Trends/" + stream_note.name
        in manifest["files"]["markdown"]
    )

    site_dir = tmp_path / "site"
    built_manifest_path = export_trend_static_site(
        input_dir=staged_root,
        output_dir=site_dir,
    )

    assert built_manifest_path == site_dir / "manifest.json"
    built_manifest = json.loads(built_manifest_path.read_text(encoding="utf-8"))
    assert built_manifest["trends_total"] == 2
    assert (site_dir / "trends" / f"{legacy_note.stem}.html").exists()
    assert (site_dir / "trends" / f"{stream_note.stem}.html").exists()
