from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path

from recoleta.site import (
    _item_action_label,
    export_trend_static_site,
    stage_trend_site_source,
)
from recoleta.publish import write_markdown_note, write_markdown_trend_note


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
    assert (
        _item_action_label(
            source="",
            canonical_url="https://notgithub.com/octocat/example",
        )
        == "Open original"
    )


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
    assert "Static trend site" not in index_html
    assert "A lighter-weight way to browse Recoleta trends." not in index_html
    assert "Research dispatches, not raw system output" not in index_html
    assert "<section class='page-hero'>" not in index_html

    topic_html = (site_dir / "topics" / "agents.html").read_text(encoding="utf-8")
    assert "Agent Systems" in topic_html
    assert "Embodied Systems" in topic_html
    assert "<section class='page-hero'>" not in topic_html

    detail_html = (site_dir / "trends" / f"{note_one.stem}.html").read_text(
        encoding="utf-8"
    )
    assert "Source markdown" in detail_html
    assert "Download PDF" in detail_html
    assert "Telegram-ready PDF brief" not in detail_html
    assert "section-label'>Topics<" not in detail_html
    assert "<section class='page-hero'>" not in detail_html


def test_export_trend_static_site_orders_weekly_briefs_before_latest_daily_child(
    tmp_path: Path,
) -> None:
    """Regression: a weekly brief should render before the latest daily brief it summarizes."""
    output_dir = tmp_path / "notes"
    weekly_note = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=81,
        title="Week 10 roundup",
        granularity="week",
        period_start=datetime(2026, 3, 2, tzinfo=UTC),
        period_end=datetime(2026, 3, 9, tzinfo=UTC),
        run_id="run-site-weekly-first",
        overview_md="## Overview\n\nWeekly synthesis.\n",
        topics=["agents"],
        clusters=[],
        highlights=["Weekly synthesis lands before the child daily brief."],
    )
    daily_note = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=82,
        title="March 8 daily",
        granularity="day",
        period_start=datetime(2026, 3, 8, tzinfo=UTC),
        period_end=datetime(2026, 3, 9, tzinfo=UTC),
        run_id="run-site-daily-second",
        overview_md="## Overview\n\nDaily synthesis.\n",
        topics=["agents"],
        clusters=[],
        highlights=["Daily brief remains visible under the weekly synthesis."],
    )

    site_dir = tmp_path / "site"
    manifest_path = export_trend_static_site(
        input_dir=output_dir / "Trends",
        output_dir=site_dir,
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["files"]["trend_pages"] == [
        f"trends/{weekly_note.stem}.html",
        f"trends/{daily_note.stem}.html",
    ]

    index_html = (site_dir / "index.html").read_text(encoding="utf-8")
    assert index_html.index("Week 10 roundup") < index_html.index("March 8 daily")

    archive_html = (site_dir / "archive.html").read_text(encoding="utf-8")
    assert archive_html.index("Week 10 roundup") < archive_html.index("March 8 daily")


def test_export_trend_static_site_keeps_mobile_shell_rules_within_viewport(
    tmp_path: Path,
) -> None:
    """Regression: the generated mobile stylesheet should stack the header and keep the shell width valid."""
    output_dir = tmp_path / "notes"
    _ = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=83,
        title="Mobile layout check",
        granularity="day",
        period_start=datetime(2026, 3, 8, tzinfo=UTC),
        period_end=datetime(2026, 3, 9, tzinfo=UTC),
        run_id="run-site-mobile-layout",
        overview_md="## Overview\n\nA narrow-screen regression guard.\n",
        topics=["agents"],
        clusters=[],
        highlights=["Small screens should stay inside the viewport."],
    )

    site_dir = tmp_path / "site"
    _ = export_trend_static_site(input_dir=output_dir / "Trends", output_dir=site_dir)

    stylesheet = (site_dir / "assets" / "site.css").read_text(encoding="utf-8")
    assert "width: calc(100% - 16px);" in stylesheet
    assert "flex-direction: column;" in stylesheet
    assert "overflow-wrap: anywhere;" in stylesheet


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


def test_export_trend_static_site_hides_legacy_topics_body_section(
    tmp_path: Path,
) -> None:
    notes_dir = tmp_path / "notes" / "Trends"
    notes_dir.mkdir(parents=True, exist_ok=True)
    legacy_note = notes_dir / "day--2026-03-01--trend--1.md"
    legacy_note.write_text(
        "---\n"
        "kind: trend\n"
        "granularity: day\n"
        "period_start: 2026-03-01T00:00:00+00:00\n"
        "period_end: 2026-03-02T00:00:00+00:00\n"
        "topics:\n"
        "  - agents\n"
        "---\n\n"
        "# 2026-03-01 研究趋势日报：Agent systems get tighter loops\n\n"
        "## Overview\n\n"
        "Tighter loops.\n\n"
        "## Topics\n\n"
        "- agents\n\n"
        "## Clusters\n\n"
        "### Loop closing\n\n"
        "Grounded execution.\n",
        encoding="utf-8",
    )

    site_dir = tmp_path / "site"
    _ = export_trend_static_site(input_dir=notes_dir, output_dir=site_dir)

    detail_html = (site_dir / "trends" / "day--2026-03-01--trend--1.html").read_text(
        encoding="utf-8"
    )
    assert "研究趋势日报" not in detail_html
    assert "Agent systems get tighter loops" in detail_html
    assert "section-label'>Topics<" not in detail_html


def test_export_trend_static_site_writes_item_pages_and_rewrites_trend_links(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "notes"
    item_note = write_markdown_note(
        output_dir=output_dir,
        item_id=41,
        title="Robometer: Scaling General-Purpose Robotic Reward Models",
        source="rss",
        canonical_url="https://example.com/robometer",
        published_at=datetime(2026, 3, 2, tzinfo=UTC),
        authors=["Alice"],
        topics=["agents", "robotics"],
        relevance_score=0.95,
        run_id="run-item-site-1",
        summary="## Summary\n\nReward models get a stronger comparison signal.\n",
    )
    trend_note = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=74,
        title="Agent Systems",
        granularity="day",
        period_start=datetime(2026, 3, 2, tzinfo=UTC),
        period_end=datetime(2026, 3, 3, tzinfo=UTC),
        run_id="run-site-items-1",
        overview_md=(
            f"## Overview\n\nStart with [Robometer](../Inbox/{item_note.name}).\n"
        ),
        topics=["agents", "robotics"],
        clusters=[
            {
                "name": "Reward models",
                "description": "Trajectory comparisons are improving alignment.",
                "representative_chunks": [
                    {
                        "doc_id": 41,
                        "chunk_index": 0,
                        "title": "Robometer: Scaling General-Purpose Robotic Reward Models",
                        "url": "https://example.com/robometer",
                        "note_href": f"../Inbox/{item_note.name}",
                        "authors": ["Alice"],
                    }
                ],
            }
        ],
        highlights=["Reward modeling is getting easier to operationalize."],
    )

    site_dir = tmp_path / "site"
    manifest_path = export_trend_static_site(
        input_dir=output_dir / "Trends",
        output_dir=site_dir,
    )

    item_page = site_dir / "items" / f"{item_note.stem}.html"
    assert item_page.exists()

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["items_total"] == 1
    assert f"items/{item_note.stem}.html" in manifest["files"]["item_pages"]

    detail_html = (site_dir / "trends" / f"{trend_note.stem}.html").read_text(
        encoding="utf-8"
    )
    assert f"../items/{item_note.stem}.html" in detail_html
    assert "../Inbox/" not in detail_html
    assert "https://example.com/robometer" not in detail_html
    assert "<p class='detail-dek'>Start with Robometer.</p>" in detail_html

    item_html = item_page.read_text(encoding="utf-8")
    assert "Robometer: Scaling General-Purpose Robotic Reward Models" in item_html
    assert "Open original" in item_html
    assert "https://example.com/robometer" in item_html
    assert "Source markdown" in item_html
    assert "document-flow" in item_html
    assert (
        "<p class='detail-dek'>Reward models get a stronger comparison signal.</p>"
        in item_html
    )
    assert "summary-grid summary-grid-single" in item_html
    assert "surface-card section-card summary-card summary-card-primary" in item_html
    assert ">Link</h2>" in item_html


def test_export_trend_static_site_writes_idea_pages_and_rewrites_links(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "notes"
    item_note = write_markdown_note(
        output_dir=output_dir,
        item_id=51,
        title="CodeScout",
        source="rss",
        canonical_url="https://example.com/codescout",
        published_at=datetime(2026, 3, 9, tzinfo=UTC),
        authors=["Alice"],
        topics=["agents"],
        relevance_score=0.91,
        run_id="run-site-ideas-item",
        summary="## Summary\n\nProblem clarification helps.\n",
    )
    trend_note = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=91,
        title="Code agents close the loop",
        granularity="day",
        period_start=datetime(2026, 3, 9, tzinfo=UTC),
        period_end=datetime(2026, 3, 10, tzinfo=UTC),
        run_id="run-site-ideas-trend",
        overview_md="## Overview\n\nAgent workflows keep tightening.\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
    )
    ideas_dir = output_dir / "Ideas"
    ideas_dir.mkdir(parents=True, exist_ok=True)
    idea_note = ideas_dir / "day--2026-03-09--ideas.md"
    idea_note.write_text(
        "---\n"
        "kind: ideas\n"
        "granularity: day\n"
        "period_start: 2026-03-09T00:00:00+00:00\n"
        "period_end: 2026-03-10T00:00:00+00:00\n"
        "status: succeeded\n"
        "topics:\n"
        "  - agents\n"
        "---\n\n"
        "# Verification-first agent rollout\n\n"
        "## Summary\n\n"
        f"Start with [CodeScout](../Inbox/{item_note.name}) and [the daily trend](../Trends/{trend_note.name}).\n\n"
        "## Opportunities\n\n"
        "### Prompt CI gate\n\n"
        "Use a release gate before shipping prompt changes.\n",
        encoding="utf-8",
    )

    site_dir = tmp_path / "site"
    manifest_path = export_trend_static_site(
        input_dir=output_dir / "Trends",
        output_dir=site_dir,
    )

    idea_page = site_dir / "ideas" / f"{idea_note.stem}.html"
    assert idea_page.exists()

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["ideas_total"] == 1
    assert f"ideas/{idea_note.stem}.html" in manifest["files"]["idea_pages"]

    index_html = (site_dir / "index.html").read_text(encoding="utf-8")
    assert "Latest idea briefs" in index_html
    assert "Verification-first agent rollout" in index_html

    ideas_index_html = (site_dir / "ideas" / "index.html").read_text(encoding="utf-8")
    assert "Verification-first agent rollout" in ideas_index_html

    detail_html = idea_page.read_text(encoding="utf-8")
    assert f"../items/{item_note.stem}.html" in detail_html
    assert f"../trends/{trend_note.stem}.html" in detail_html
    assert "../Inbox/" not in detail_html
    assert "../Trends/" not in detail_html
    assert "Source markdown" in detail_html


def test_export_trend_static_site_renders_idea_opportunities_as_cards(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "notes"
    item_note = write_markdown_note(
        output_dir=output_dir,
        item_id=52,
        title="CodeScout",
        source="rss",
        canonical_url="https://example.com/codescout",
        published_at=datetime(2026, 3, 9, tzinfo=UTC),
        authors=["Alice"],
        topics=["agents"],
        relevance_score=0.88,
        run_id="run-site-ideas-structured-item",
        summary="## Summary\n\nPrompt release notes.\n",
    )
    trend_note = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=92,
        title="Agent systems",
        granularity="day",
        period_start=datetime(2026, 3, 9, tzinfo=UTC),
        period_end=datetime(2026, 3, 10, tzinfo=UTC),
        run_id="run-site-ideas-structured-trend",
        overview_md="## Overview\n\nTrend note.\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
    )
    ideas_dir = output_dir / "Ideas"
    ideas_dir.mkdir(parents=True, exist_ok=True)
    idea_note = ideas_dir / "day--2026-03-09--ideas.md"
    idea_note.write_text(
        "---\n"
        "kind: ideas\n"
        "granularity: day\n"
        "period_start: 2026-03-09T00:00:00+00:00\n"
        "period_end: 2026-03-10T00:00:00+00:00\n"
        "status: succeeded\n"
        "topics:\n"
        "  - agents\n"
        "---\n\n"
        "# Verification-first agent rollout\n\n"
        "## Summary\n\n"
        "Start with "
        f"[CodeScout](../Inbox/{item_note.name}) and "
        f"[the daily trend](../Trends/{trend_note.name}).\n\n"
        "## Opportunities\n\n"
        "### Prompt CI gate\n"
        "- Kind: Workflow\n"
        "- Time horizon: Now\n"
        "- User/job: Internal agent platform owners responsible for prompt rollout safety\n\n"
        "**Thesis.** Add a prompt release gate before rollout.\n\n"
        "**Why now.** Teams now have enough agent activity to justify structured release controls.\n\n"
        "**What changed.** More agent traffic means regressions show up faster and cost more.\n\n"
        "**Validation next step.** Pilot the gate on one high-volume internal workflow.\n\n"
        "#### Evidence\n"
        f"- [CodeScout](../Inbox/{item_note.name})\n"
        f"- [Daily trend](../Trends/{trend_note.name})\n\n"
        "### Operator review lane\n"
        "- Kind: Product\n"
        "- Time horizon: Near-term\n"
        "- User/job: Applied AI ops\n\n"
        "**Thesis.** Give operators a queue that isolates low-confidence agent runs.\n\n"
        "**Why now.** Teams are crossing the threshold where manual review no longer fits ad hoc chat.\n\n"
        "**What changed.** Higher usage produces repeated edge cases and repeatable review heuristics.\n\n"
        "**Validation next step.** Track acceptance rate and review latency for two weeks.\n",
        encoding="utf-8",
    )

    site_dir = tmp_path / "site"
    export_trend_static_site(
        input_dir=output_dir / "Trends",
        output_dir=site_dir,
    )

    detail_html = (site_dir / "ideas" / f"{idea_note.stem}.html").read_text(
        encoding="utf-8"
    )
    assert "summary-grid summary-grid-single" in detail_html
    assert "idea-opportunity-grid" in detail_html
    assert detail_html.count("idea-opportunity-card") == 2
    assert "idea-opportunity-meta-row" in detail_html
    assert "idea-opportunity-block-role" in detail_html
    assert "idea-evidence-list" in detail_html
    assert "2 opportunities" in detail_html
    assert "User/job" not in detail_html
    assert ">Role<" in detail_html
    assert f"../items/{item_note.stem}.html" in detail_html
    assert f"../trends/{trend_note.stem}.html" in detail_html


def test_export_trend_static_site_hides_empty_topics_for_ideas(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "notes"
    _ = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=93,
        title="Agent systems",
        granularity="day",
        period_start=datetime(2026, 3, 9, tzinfo=UTC),
        period_end=datetime(2026, 3, 10, tzinfo=UTC),
        run_id="run-site-ideas-no-topic-trend",
        overview_md="## Overview\n\nTrend note.\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
    )
    ideas_dir = output_dir / "Ideas"
    ideas_dir.mkdir(parents=True, exist_ok=True)
    idea_note = ideas_dir / "day--2026-03-09--ideas.md"
    idea_note.write_text(
        "---\n"
        "kind: ideas\n"
        "granularity: day\n"
        "period_start: 2026-03-09T00:00:00+00:00\n"
        "period_end: 2026-03-10T00:00:00+00:00\n"
        "status: succeeded\n"
        "---\n\n"
        "# Verification-first agent rollout\n\n"
        "## Summary\n\n"
        "Ship a prompt release gate.\n",
        encoding="utf-8",
    )

    site_dir = tmp_path / "site"
    export_trend_static_site(
        input_dir=output_dir / "Trends",
        output_dir=site_dir,
    )

    index_html = (site_dir / "index.html").read_text(encoding="utf-8")
    ideas_index_html = (site_dir / "ideas" / "index.html").read_text(encoding="utf-8")
    detail_html = (site_dir / "ideas" / f"{idea_note.stem}.html").read_text(
        encoding="utf-8"
    )
    assert "No tracked topics" not in index_html
    assert "No tracked topics" not in ideas_index_html
    assert "No tracked topics" not in detail_html


def test_stage_trend_site_source_mirrors_idea_markdown_and_manifest_entries(
    tmp_path: Path,
) -> None:
    notes_root = tmp_path / "notes"
    _ = write_markdown_trend_note(
        output_dir=notes_root,
        trend_doc_id=92,
        title="Agent systems",
        granularity="day",
        period_start=datetime(2026, 3, 9, tzinfo=UTC),
        period_end=datetime(2026, 3, 10, tzinfo=UTC),
        run_id="run-stage-ideas-trend",
        overview_md="## Overview\n\nTrend note.\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
    )
    ideas_dir = notes_root / "Ideas"
    ideas_dir.mkdir(parents=True, exist_ok=True)
    idea_note = ideas_dir / "day--2026-03-09--ideas.md"
    idea_note.write_text(
        "---\n"
        "kind: ideas\n"
        "granularity: day\n"
        "period_start: 2026-03-09T00:00:00+00:00\n"
        "period_end: 2026-03-10T00:00:00+00:00\n"
        "status: succeeded\n"
        "---\n\n"
        "# Verification-first agent rollout\n",
        encoding="utf-8",
    )

    staged_dir = tmp_path / "site-content" / "Trends"
    manifest_path = stage_trend_site_source(
        input_dir=notes_root / "Trends",
        output_dir=staged_dir,
    )

    assert (staged_dir.parent / "Ideas" / idea_note.name).exists()

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["ideas_total"] == 1
    assert f"Ideas/{idea_note.name}" in manifest["files"]["ideas_markdown"]


def test_export_trend_static_site_rewrites_history_trend_links_to_html(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "notes"
    previous_note = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=80,
        title="Previous Daily Trend: Verification Gets Tighter",
        granularity="day",
        period_start=datetime(2026, 3, 4, tzinfo=UTC),
        period_end=datetime(2026, 3, 5, tzinfo=UTC),
        run_id="run-site-history-1",
        overview_md="## Overview\n\nPrevious note.\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
    )
    current_note = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=81,
        title="Current Daily Trend",
        granularity="day",
        period_start=datetime(2026, 3, 5, tzinfo=UTC),
        period_end=datetime(2026, 3, 6, tzinfo=UTC),
        run_id="run-site-history-2",
        overview_md="## Overview\n\nCurrent note.\n",
        topics=["agents"],
        evolution={
            "summary_md": "Compared with prev_1, execution is becoming more explicit.",
            "signals": [
                {
                    "theme": "Verification",
                    "change_type": "continuing",
                    "summary": (
                        "Compared with prev_1, validation loops now include "
                        "more explicit runtime checks."
                    ),
                    "history_windows": ["prev_1"],
                }
            ],
        },
        history_window_refs={
            "prev_1": {
                "window_id": "prev_1",
                "label": "2026-03-04",
                "title": "Previous Daily Trend: Verification Gets Tighter",
                "granularity": "day",
                "period_start": "2026-03-04T00:00:00+00:00",
                "trend_doc_id": 80,
            }
        },
        clusters=[],
        highlights=[],
    )

    site_dir = tmp_path / "site"
    _ = export_trend_static_site(
        input_dir=output_dir / "Trends",
        output_dir=site_dir,
    )

    detail_html = (site_dir / "trends" / f"{current_note.stem}.html").read_text(
        encoding="utf-8"
    )
    assert f"{previous_note.stem}.html" in detail_html
    assert f"{previous_note.name}" not in detail_html
    assert "Previous Daily Trend (2026-03-04)" in detail_html


def test_export_trend_static_site_prioritizes_evolution_section_and_renders_signal_cards(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "notes"
    note = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=82,
        title="Evolution-first trend",
        granularity="day",
        period_start=datetime(2026, 3, 5, tzinfo=UTC),
        period_end=datetime(2026, 3, 6, tzinfo=UTC),
        run_id="run-site-evolution-cards",
        overview_md="## Overview\n\nA brief with explicit historical comparison.\n",
        topics=["agents", "verification"],
        evolution={
            "summary_md": "Compared with prev_1 and prev_2, execution is easier to audit.",
            "signals": [
                {
                    "theme": "Runtime verification gets explicit",
                    "change_type": "continuing",
                    "summary": "Compared with prev_1, the validation loop now exposes runtime checks.",
                    "history_windows": ["prev_1"],
                },
                {
                    "theme": "Terminal-native agent shells emerge",
                    "change_type": "emerging",
                    "summary": "Compared with prev_2, shell-native workflows become a first-class system surface.",
                    "history_windows": ["prev_2"],
                },
            ],
        },
        history_window_refs={
            "prev_1": {
                "window_id": "prev_1",
                "label": "2026-03-04",
                "title": "Previous Daily Trend",
                "granularity": "day",
                "period_start": "2026-03-04T00:00:00+00:00",
                "trend_doc_id": 80,
            },
            "prev_2": {
                "window_id": "prev_2",
                "label": "2026-03-03",
                "title": "Older Daily Trend",
                "granularity": "day",
                "period_start": "2026-03-03T00:00:00+00:00",
                "trend_doc_id": 79,
            },
        },
        clusters=[
            {
                "name": "Execution loops",
                "description": "Execution is converging on stronger validation surfaces.",
                "representative_chunks": [],
            }
        ],
        highlights=[],
    )

    previous_note = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=80,
        title="Previous Daily Trend",
        granularity="day",
        period_start=datetime(2026, 3, 4, tzinfo=UTC),
        period_end=datetime(2026, 3, 5, tzinfo=UTC),
        run_id="run-site-evolution-cards-prev-1",
        overview_md="## Overview\n\nPrevious note.\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
    )
    older_note = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=79,
        title="Older Daily Trend",
        granularity="day",
        period_start=datetime(2026, 3, 3, tzinfo=UTC),
        period_end=datetime(2026, 3, 4, tzinfo=UTC),
        run_id="run-site-evolution-cards-prev-2",
        overview_md="## Overview\n\nOlder note.\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
    )

    site_dir = tmp_path / "site"
    _ = export_trend_static_site(
        input_dir=output_dir / "Trends",
        output_dir=site_dir,
    )

    detail_html = (site_dir / "trends" / f"{note.stem}.html").read_text(
        encoding="utf-8"
    )
    assert detail_html.index(">Evolution</h2>") < detail_html.index(">Clusters</h2>")
    assert "evolution-section" in detail_html
    assert "evolution-grid" in detail_html
    assert "evolution-card" in detail_html
    assert "history-pill" in detail_html
    assert f"{previous_note.stem}.html" in detail_html
    assert f"{older_note.stem}.html" in detail_html


def test_export_trend_static_site_surfaces_evolution_insight_in_detail_hero_and_home_cards(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "notes"
    note = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=83,
        title="Evolution insight trend",
        granularity="day",
        period_start=datetime(2026, 3, 6, tzinfo=UTC),
        period_end=datetime(2026, 3, 7, tzinfo=UTC),
        run_id="run-site-evolution-insight",
        overview_md="## Overview\n\nOperational loops are becoming easier to compare.\n",
        topics=["agents", "verification"],
        evolution={
            "summary_md": "Compared with prev_1, validation keeps moving earlier in the loop.",
            "signals": [
                {
                    "theme": "Verification moves earlier",
                    "change_type": "continuing",
                    "summary": "Compared with prev_1, verification happens before deployment.",
                    "history_windows": ["prev_1"],
                },
                {
                    "theme": "Terminal harnesses solidify",
                    "change_type": "emerging",
                    "summary": "Compared with prev_1, shell-native harnesses are now a distinct design surface.",
                    "history_windows": ["prev_1"],
                },
            ],
        },
        history_window_refs={
            "prev_1": {
                "window_id": "prev_1",
                "label": "2026-03-05",
                "title": "Previous Insight Trend",
                "granularity": "day",
                "period_start": "2026-03-05T00:00:00+00:00",
                "trend_doc_id": 78,
            }
        },
        clusters=[],
        highlights=[],
    )
    _ = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=78,
        title="Previous Insight Trend",
        granularity="day",
        period_start=datetime(2026, 3, 5, tzinfo=UTC),
        period_end=datetime(2026, 3, 6, tzinfo=UTC),
        run_id="run-site-evolution-insight-prev",
        overview_md="## Overview\n\nPrevious note.\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
    )

    site_dir = tmp_path / "site"
    _ = export_trend_static_site(
        input_dir=output_dir / "Trends",
        output_dir=site_dir,
    )

    index_html = (site_dir / "index.html").read_text(encoding="utf-8")
    detail_html = (site_dir / "trends" / f"{note.stem}.html").read_text(
        encoding="utf-8"
    )

    assert "trend-insight-row" in index_html
    assert "2 signals" in index_html
    assert "Continuing 1" in index_html
    assert "Emerging 1" in index_html

    assert "detail-insight-row" in detail_html
    assert "2 signals" in detail_html
    assert "Continuing 1" in detail_html
    assert "Emerging 1" in detail_html


def test_export_trend_static_site_uses_overview_summary_in_detail_hero(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "notes"
    note = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=84,
        title="Hero summary trend",
        granularity="day",
        period_start=datetime(2026, 3, 7, tzinfo=UTC),
        period_end=datetime(2026, 3, 8, tzinfo=UTC),
        run_id="run-site-evolution-hero",
        overview_md="## Overview\n\nOverview copy should remain the page summary.\n",
        topics=["agents"],
        evolution={
            "summary_md": "Evolution summary should stay in the comparison section because it explains the historical delta.",
            "signals": [
                {
                    "theme": "Verification moves earlier",
                    "change_type": "continuing",
                    "summary": "Verification starts before deployment.",
                    "history_windows": [],
                }
            ],
        },
        clusters=[],
        highlights=[],
    )

    site_dir = tmp_path / "site"
    _ = export_trend_static_site(
        input_dir=output_dir / "Trends",
        output_dir=site_dir,
    )

    detail_html = (site_dir / "trends" / f"{note.stem}.html").read_text(
        encoding="utf-8"
    )
    assert (
        "<p class='detail-dek'>Overview copy should remain the page summary.</p>"
        in detail_html
    )
    assert (
        "Evolution summary should stay in the comparison section because it explains the historical delta."
        in detail_html
    )


def test_export_trend_static_site_keeps_overview_summary_when_evolution_has_no_signals(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "notes"
    note = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=88,
        title="Summary-only evolution trend",
        granularity="day",
        period_start=datetime(2026, 3, 10, tzinfo=UTC),
        period_end=datetime(2026, 3, 11, tzinfo=UTC),
        run_id="run-site-evolution-summary-only",
        overview_md="## Overview\n\nOverview copy should remain the page summary.\n",
        topics=["agents"],
        evolution={
            "summary_md": "Evolution summary should still render in the comparison section when the run emits zero signals.",
            "signals": [],
        },
        clusters=[],
        highlights=[],
    )

    site_dir = tmp_path / "site"
    _ = export_trend_static_site(
        input_dir=output_dir / "Trends",
        output_dir=site_dir,
    )

    detail_html = (site_dir / "trends" / f"{note.stem}.html").read_text(
        encoding="utf-8"
    )
    assert (
        "<p class='detail-dek'>Overview copy should remain the page summary.</p>"
        in detail_html
    )
    assert (
        "Evolution summary should still render in the comparison section when the run emits zero signals."
        in detail_html
    )
    assert "detail-insight-row" not in detail_html


def test_export_trend_static_site_wraps_long_evolution_signal_copy_in_disclosure(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "notes"
    note = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=85,
        title="Long evolution signal trend",
        granularity="day",
        period_start=datetime(2026, 3, 8, tzinfo=UTC),
        period_end=datetime(2026, 3, 9, tzinfo=UTC),
        run_id="run-site-evolution-disclosure",
        overview_md="## Overview\n\nOverview copy.\n",
        topics=["agents"],
        evolution={
            "summary_md": "A compact historical bridge.",
            "signals": [
                {
                    "theme": "Long-form runtime verification rationale",
                    "change_type": "continuing",
                    "summary": (
                        "This signal summary is intentionally long so the site renderer "
                        "has to switch from a dense always-open paragraph into a compact "
                        "preview with a native disclosure control. The content keeps going "
                        "to mimic a real historical comparison paragraph with multiple "
                        "clauses, tradeoffs, and references that would otherwise turn the "
                        "mobile layout into a wall of text."
                    ),
                    "history_windows": [],
                }
            ],
        },
        clusters=[],
        highlights=[],
    )

    site_dir = tmp_path / "site"
    _ = export_trend_static_site(
        input_dir=output_dir / "Trends",
        output_dir=site_dir,
    )

    detail_html = (site_dir / "trends" / f"{note.stem}.html").read_text(
        encoding="utf-8"
    )
    assert "evolution-expand" in detail_html
    assert "evolution-expand-toggle" in detail_html
    assert "evolution-expand-summary-copy" in detail_html
    assert "evolution-preview" not in detail_html


def test_export_trend_static_site_keeps_medium_evolution_signal_copy_inline(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "notes"
    note = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=89,
        title="Medium evolution signal trend",
        granularity="day",
        period_start=datetime(2026, 3, 9, tzinfo=UTC),
        period_end=datetime(2026, 3, 10, tzinfo=UTC),
        run_id="run-site-evolution-inline-medium",
        overview_md="## Overview\n\nOverview copy.\n",
        topics=["agents"],
        evolution={
            "summary_md": "A medium-length historical bridge.",
            "signals": [
                {
                    "theme": "Medium-length implementation rationale",
                    "change_type": "continuing",
                    "summary": (
                        "This rationale is long enough to exceed a short paragraph, "
                        "but it should still remain inline because the truncation "
                        "benefit is too small. The goal is to avoid showing a collapsed "
                        "preview and then effectively repeating the same amount of text "
                        "again after expansion."
                    ),
                    "history_windows": [],
                }
            ],
        },
        clusters=[],
        highlights=[],
    )

    site_dir = tmp_path / "site"
    _ = export_trend_static_site(
        input_dir=output_dir / "Trends",
        output_dir=site_dir,
    )

    detail_html = (site_dir / "trends" / f"{note.stem}.html").read_text(
        encoding="utf-8"
    )
    assert "evolution-copy" in detail_html
    assert "evolution-expand" not in detail_html


def test_export_trend_static_site_keeps_fixed_evolution_ui_terms_in_english_for_chinese_notes(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "notes"
    previous_note = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=86,
        title="Earlier Window",
        granularity="day",
        period_start=datetime(2026, 3, 8, tzinfo=UTC),
        period_end=datetime(2026, 3, 9, tzinfo=UTC),
        run_id="run-site-ui-english-prev",
        overview_md="## Overview\n\nEarlier note.\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
        output_language="zh-CN",
    )
    note = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=87,
        title="Chinese note with fixed English chrome",
        granularity="day",
        period_start=datetime(2026, 3, 9, tzinfo=UTC),
        period_end=datetime(2026, 3, 10, tzinfo=UTC),
        run_id="run-site-ui-english-current",
        overview_md="## Overview\n\n正文仍然可以是中文。\n",
        topics=["agents"],
        evolution={
            "summary_md": "这里仍然是中文正文，但固定 UI 术语应该保持英文。",
            "signals": [
                {
                    "theme": "验证继续前移",
                    "change_type": "continuing",
                    "summary": "相较 prev_1，验证发生得更早。",
                    "history_windows": ["prev_1"],
                }
            ],
        },
        history_window_refs={
            "prev_1": {
                "window_id": "prev_1",
                "label": "2026-03-08",
                "title": "Earlier Window",
                "granularity": "day",
                "period_start": "2026-03-08T00:00:00+00:00",
                "trend_doc_id": 86,
            }
        },
        clusters=[],
        highlights=[],
        output_language="zh-CN",
    )

    site_dir = tmp_path / "site"
    _ = export_trend_static_site(
        input_dir=output_dir / "Trends",
        output_dir=site_dir,
    )

    detail_html = (site_dir / "trends" / f"{note.stem}.html").read_text(
        encoding="utf-8"
    )
    assert "1 signal" in detail_html
    assert "Continuing 1" in detail_html
    assert ">History<" in detail_html
    assert ">Read full rationale<" not in detail_html
    assert "Earlier Window" in detail_html
    assert f"{previous_note.stem}.html" in detail_html
    assert "延续 1" not in detail_html
    assert "历史窗口" not in detail_html


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

    stream_html = (site_dir / "streams" / "agents-lab.html").read_text(encoding="utf-8")
    assert "Agent Systems" in stream_html

    detail_html = (site_dir / "trends" / f"{agents_note.stem}.html").read_text(
        encoding="utf-8"
    )
    assert "agents_lab" in detail_html


def test_export_trend_static_site_keeps_same_day_idea_pages_distinct_per_stream(
    tmp_path: Path,
) -> None:
    notes_root = tmp_path / "notes"
    agents_root = notes_root / "Streams" / "agents_lab"
    research_root = notes_root / "Streams" / "research_ops"

    _ = write_markdown_trend_note(
        output_dir=agents_root,
        trend_doc_id=111,
        title="Agent systems",
        granularity="day",
        period_start=datetime(2026, 3, 9, tzinfo=UTC),
        period_end=datetime(2026, 3, 10, tzinfo=UTC),
        run_id="run-stream-ideas-1",
        overview_md="## Overview\n\nAgent stream trend.\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
    )
    _ = write_markdown_trend_note(
        output_dir=research_root,
        trend_doc_id=112,
        title="Research ops",
        granularity="day",
        period_start=datetime(2026, 3, 9, tzinfo=UTC),
        period_end=datetime(2026, 3, 10, tzinfo=UTC),
        run_id="run-stream-ideas-2",
        overview_md="## Overview\n\nResearch stream trend.\n",
        topics=["operations"],
        clusters=[],
        highlights=[],
    )

    agents_ideas_dir = agents_root / "Ideas"
    agents_ideas_dir.mkdir(parents=True, exist_ok=True)
    agents_idea_note = agents_ideas_dir / "day--2026-03-09--ideas.md"
    agents_idea_note.write_text(
        "---\n"
        "kind: ideas\n"
        "granularity: day\n"
        "period_start: 2026-03-09T00:00:00+00:00\n"
        "period_end: 2026-03-10T00:00:00+00:00\n"
        "status: succeeded\n"
        "stream: agents_lab\n"
        "---\n\n"
        "# Agents lane\n\n"
        "## Summary\n\n"
        "Agent-side idea summary.\n",
        encoding="utf-8",
    )

    research_ideas_dir = research_root / "Ideas"
    research_ideas_dir.mkdir(parents=True, exist_ok=True)
    research_idea_note = research_ideas_dir / "day--2026-03-09--ideas.md"
    research_idea_note.write_text(
        "---\n"
        "kind: ideas\n"
        "granularity: day\n"
        "period_start: 2026-03-09T00:00:00+00:00\n"
        "period_end: 2026-03-10T00:00:00+00:00\n"
        "status: succeeded\n"
        "stream: research_ops\n"
        "---\n\n"
        "# Research ops lane\n\n"
        "## Summary\n\n"
        "Research-side idea summary.\n",
        encoding="utf-8",
    )

    site_dir = tmp_path / "site"
    manifest_path = export_trend_static_site(
        input_dir=notes_root,
        output_dir=site_dir,
    )

    agents_page = site_dir / "ideas" / "agents-lab--day--2026-03-09--ideas.html"
    research_page = site_dir / "ideas" / "research-ops--day--2026-03-09--ideas.html"
    assert agents_page.exists()
    assert research_page.exists()

    agents_html = agents_page.read_text(encoding="utf-8")
    research_html = research_page.read_text(encoding="utf-8")
    assert "Agents lane" in agents_html
    assert "Research ops lane" not in agents_html
    assert "Research ops lane" in research_html
    assert "Agents lane" not in research_html

    stream_html = (site_dir / "streams" / "agents-lab.html").read_text(encoding="utf-8")
    assert "../ideas/agents-lab--day--2026-03-09--ideas.html" in stream_html
    assert "../ideas/research-ops--day--2026-03-09--ideas.html" not in stream_html

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert "ideas/agents-lab--day--2026-03-09--ideas.html" in manifest["files"]["idea_pages"]
    assert (
        "ideas/research-ops--day--2026-03-09--ideas.html"
        in manifest["files"]["idea_pages"]
    )


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
    assert (staged_root / "Streams" / "bio_watch" / "Trends" / bio_note.name).exists()

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
        "Streams/agents_lab/Trends/" + stream_note.name in manifest["files"]["markdown"]
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


def test_stage_trend_site_source_stages_item_notes_next_to_trends(
    tmp_path: Path,
) -> None:
    notes_root = tmp_path / "notes"
    item_note = write_markdown_note(
        output_dir=notes_root,
        item_id=51,
        title="Agentic Testing",
        source="rss",
        canonical_url="https://example.com/agentic-testing",
        published_at=datetime(2026, 3, 9, tzinfo=UTC),
        authors=["Alice"],
        topics=["agents"],
        relevance_score=0.93,
        run_id="run-stage-item-1",
        summary="## Summary\n\nA compact item note.\n",
    )
    trend_note = write_markdown_trend_note(
        output_dir=notes_root,
        trend_doc_id=113,
        title="Agent Systems",
        granularity="day",
        period_start=datetime(2026, 3, 9, tzinfo=UTC),
        period_end=datetime(2026, 3, 10, tzinfo=UTC),
        run_id="run-stage-item-1",
        overview_md=f"## Overview\n\nSee [Agentic Testing](../Inbox/{item_note.name}).\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
    )
    trend_note.with_suffix(".pdf").write_bytes(b"%PDF-1.7\n")

    staged_trends_dir = tmp_path / "site-content" / "Trends"
    manifest_path = stage_trend_site_source(
        input_dir=notes_root / "Trends",
        output_dir=staged_trends_dir,
    )

    assert manifest_path == staged_trends_dir / "manifest.json"
    assert (staged_trends_dir / trend_note.name).exists()
    assert (staged_trends_dir.parent / "Inbox" / item_note.name).exists()

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["items_total"] == 1
    assert f"Inbox/{item_note.name}" in manifest["files"]["items_markdown"]


def test_stage_trend_site_source_preserves_unrelated_parent_files_for_trends_output_dir(
    tmp_path: Path,
) -> None:
    notes_root = tmp_path / "notes"
    trend_note = write_markdown_trend_note(
        output_dir=notes_root,
        trend_doc_id=118,
        title="Agent Systems",
        granularity="day",
        period_start=datetime(2026, 3, 9, tzinfo=UTC),
        period_end=datetime(2026, 3, 10, tzinfo=UTC),
        run_id="run-stage-root-guard-1",
        overview_md="## Overview\n\nA compact trend note.\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
    )

    stage_root = tmp_path / "site-content"
    stage_root.mkdir(parents=True, exist_ok=True)
    keep_path = stage_root / "keep.txt"
    keep_path.write_text("keep\n", encoding="utf-8")
    stale_inbox_path = stage_root / "Inbox" / "stale.md"
    stale_inbox_path.parent.mkdir(parents=True, exist_ok=True)
    stale_inbox_path.write_text("stale\n", encoding="utf-8")

    staged_trends_dir = stage_root / "Trends"
    manifest_path = stage_trend_site_source(
        input_dir=notes_root / "Trends",
        output_dir=staged_trends_dir,
    )

    assert manifest_path == staged_trends_dir / "manifest.json"
    assert keep_path.exists()
    assert keep_path.read_text(encoding="utf-8") == "keep\n"
    assert not stale_inbox_path.exists()
    assert (staged_trends_dir / trend_note.name).exists()
