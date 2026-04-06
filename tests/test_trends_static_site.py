from __future__ import annotations

from bs4 import BeautifulSoup
from datetime import UTC, datetime
import json
from pathlib import Path
from types import SimpleNamespace
import pytest

from recoleta.presentation import (
    build_idea_presentation_v1,
    presentation_sidecar_path,
    write_presentation_sidecar,
)
from recoleta.site import (
    RECOLETA_QUICKSTART_URL,
    RECOLETA_REPO_URL,
    TrendSiteInputSpec,
    _item_action_label,
    export_trend_static_site,
    stage_trend_site_source,
)
from recoleta.passes.trend_ideas import TrendIdeasPayload
from recoleta.publish import (
    write_markdown_ideas_note,
    write_markdown_note,
    write_markdown_trend_note,
)
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
    assert (site_dir / "trends" / "index.html").exists()
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
    assert manifest["files"]["trends_index"] == "trends/index.html"

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


def test_export_trend_static_site_renders_v2_counter_signal_and_anti_thesis(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "notes"
    trend_note = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=801,
        title="Agent Systems",
        granularity="day",
        period_start=datetime(2026, 3, 9, tzinfo=UTC),
        period_end=datetime(2026, 3, 10, tzinfo=UTC),
        run_id="run-site-v2-trend",
        overview_md="Teams are tightening release discipline.",
        topics=["agents"],
        counter_signal={
            "title": "Benchmark wins still stall before deployment",
            "summary": "Offline gains do not yet guarantee that teams will operationalize the loop.",
            "evidence": [
                {
                    "title": "Field note",
                    "href": "https://example.com/field-note",
                    "authors": ["Alice"],
                }
            ],
        },
        clusters=[],
        highlights=[],
    )

    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    _ = write_markdown_ideas_note(
        repository=repository,
        output_dir=output_dir,
        pass_output_id=9,
        upstream_pass_output_id=7,
        granularity="day",
        period_start=datetime(2026, 3, 9, tzinfo=UTC),
        period_end=datetime(2026, 3, 10, tzinfo=UTC),
        run_id="run-site-v2-ideas",
        status="succeeded",
        payload=TrendIdeasPayload.model_validate(
            {
                "title": "Operator wedges",
                "granularity": "day",
                "period_start": datetime(2026, 3, 9, tzinfo=UTC).isoformat(),
                "period_end": datetime(2026, 3, 10, tzinfo=UTC).isoformat(),
                "summary_md": "Structured release controls now feel overdue.",
                "ideas": [
                    {
                        "title": "Prompt release gate",
                        "kind": "workflow_shift",
                        "thesis": "Add a prompt release gate before rollout.",
                        "anti_thesis": "This breaks down if failures stay too rare to justify a dedicated lane.",
                        "why_now": "Teams now have enough agent traffic to justify structured release controls.",
                        "what_changed": "More agent traffic means regressions show up faster and cost more.",
                        "user_or_job": "Internal agent platform owners",
                        "evidence_refs": [],
                        "validation_next_step": "Pilot the gate on one high-volume workflow.",
                        "time_horizon": "now",
                    }
                ],
            }
        ),
        topics=["agents"],
    )

    site_dir = tmp_path / "site"
    export_trend_static_site(input_dir=output_dir / "Trends", output_dir=site_dir)

    trend_html = (site_dir / "trends" / f"{trend_note.stem}.html").read_text(
        encoding="utf-8"
    )
    ideas_html = (site_dir / "ideas" / "day--2026-03-09--ideas.html").read_text(
        encoding="utf-8"
    )

    assert "Counter-signal" in trend_html
    assert "Benchmark wins still stall before deployment" in trend_html
    assert "Field note" in trend_html
    assert "Anti-thesis" in ideas_html
    assert "This breaks down if failures stay too rare" in ideas_html
    assert "Summary" in ideas_html
    assert "Opportunities" in ideas_html


def test_export_trend_static_site_home_shell_links_back_to_repo_and_quickstart(
    tmp_path: Path,
) -> None:
    """Spec: the public site home should route readers back to the repo and first-run path."""
    output_dir = tmp_path / "notes"
    _ = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=73,
        title="Agent Systems",
        granularity="day",
        period_start=datetime(2026, 2, 27, tzinfo=UTC),
        period_end=datetime(2026, 2, 28, tzinfo=UTC),
        run_id="run-site-repo-cta-home",
        overview_md="## Overview\n\nAgent workflows are getting easier to operationalize.\n",
        topics=["agents"],
        clusters=[],
        highlights=["Agent workflows are getting easier to operationalize."],
    )

    site_dir = tmp_path / "site"
    _ = export_trend_static_site(input_dir=output_dir / "Trends", output_dir=site_dir)

    index_html = (site_dir / "index.html").read_text(encoding="utf-8")
    assert ">GitHub<" in index_html
    assert f"href='{RECOLETA_REPO_URL}'" in index_html
    assert "nav-link-repo" in index_html
    assert "5-minute quickstart" in index_html
    assert f"href='{RECOLETA_QUICKSTART_URL}'" in index_html


def test_export_trend_static_site_home_hero_prioritizes_browse_actions_over_repo_link(
    tmp_path: Path,
) -> None:
    """Spec: the home hero should keep task actions and avoid repeating the repo CTA."""
    output_dir = tmp_path / "notes"
    _ = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=731,
        title="Agent Systems",
        granularity="day",
        period_start=datetime(2026, 2, 27, tzinfo=UTC),
        period_end=datetime(2026, 2, 28, tzinfo=UTC),
        run_id="run-site-home-hero-actions",
        overview_md="## Overview\n\nAgent workflows are getting easier to operationalize.\n",
        topics=["agents"],
        clusters=[],
        highlights=["Agent workflows are getting easier to operationalize."],
    )

    site_dir = tmp_path / "site"
    _ = export_trend_static_site(input_dir=output_dir / "Trends", output_dir=site_dir)

    index_html = (site_dir / "index.html").read_text(encoding="utf-8")
    soup = BeautifulSoup(index_html, "html.parser")
    hero_actions = soup.select_one(".home-hero-card .hero-actions")

    assert hero_actions is not None
    assert [
        link.get_text(" ", strip=True) for link in hero_actions.select("a.action-link")
    ] == ["Browse trends", "Browse ideas", "5-minute quickstart"]
    quickstart_link = hero_actions.select_one("a.action-link-external")
    assert quickstart_link is not None
    assert quickstart_link.get_text(" ", strip=True) == "5-minute quickstart"


def test_export_trend_static_site_trend_pages_include_built_with_recoleta_cta(
    tmp_path: Path,
) -> None:
    """Spec: trend brief pages should explain the surface and offer a repo return path."""
    output_dir = tmp_path / "notes"
    trend_note = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=74,
        title="Agent Systems",
        granularity="day",
        period_start=datetime(2026, 2, 28, tzinfo=UTC),
        period_end=datetime(2026, 3, 1, tzinfo=UTC),
        run_id="run-site-repo-cta-trend",
        overview_md="## Overview\n\nAgent workflows are tightening.\n",
        topics=["agents"],
        clusters=[],
        highlights=["Agent workflows are tightening."],
    )

    site_dir = tmp_path / "site"
    _ = export_trend_static_site(input_dir=output_dir / "Trends", output_dir=site_dir)

    detail_html = (site_dir / "trends" / f"{trend_note.stem}.html").read_text(
        encoding="utf-8"
    )
    assert "Built with Recoleta" in detail_html
    assert "Run your own research radar" in detail_html
    assert f"href='{RECOLETA_REPO_URL}'" in detail_html
    assert f"href='{RECOLETA_QUICKSTART_URL}'" in detail_html


def test_export_trend_static_site_idea_pages_include_built_with_recoleta_cta(
    tmp_path: Path,
) -> None:
    """Spec: idea brief pages should carry the same repo return CTA as trend briefs."""
    output_dir = tmp_path / "notes"
    _ = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=75,
        title="Agent Systems",
        granularity="day",
        period_start=datetime(2026, 3, 1, tzinfo=UTC),
        period_end=datetime(2026, 3, 2, tzinfo=UTC),
        run_id="run-site-repo-cta-idea-trend",
        overview_md="## Overview\n\nAgent workflows are tightening.\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
    )
    ideas_dir = output_dir / "Ideas"
    ideas_dir.mkdir(parents=True, exist_ok=True)
    idea_note = ideas_dir / "day--2026-03-01--ideas.md"
    idea_note.write_text(
        "---\n"
        "kind: ideas\n"
        "granularity: day\n"
        "period_start: 2026-03-01T00:00:00+00:00\n"
        "period_end: 2026-03-02T00:00:00+00:00\n"
        "status: succeeded\n"
        "topics:\n"
        "  - agents\n"
        "---\n\n"
        "# Verification-first agent rollout\n\n"
        "## Summary\n\n"
        "Ship a prompt release gate.\n",
        encoding="utf-8",
    )

    site_dir = tmp_path / "site"
    _ = export_trend_static_site(input_dir=output_dir / "Trends", output_dir=site_dir)

    detail_html = (site_dir / "ideas" / f"{idea_note.stem}.html").read_text(
        encoding="utf-8"
    )
    assert "Built with Recoleta" in detail_html
    assert "Run your own research radar" in detail_html
    assert f"href='{RECOLETA_REPO_URL}'" in detail_html
    assert f"href='{RECOLETA_QUICKSTART_URL}'" in detail_html


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


def test_export_trend_static_site_adds_medium_header_breakpoint_for_dense_nav(
    tmp_path: Path,
) -> None:
    """Regression: multilingual header should switch to an intentional two-row layout before mobile."""
    output_dir = tmp_path / "notes"
    _ = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=831,
        title="Medium breakpoint check",
        granularity="day",
        period_start=datetime(2026, 3, 8, tzinfo=UTC),
        period_end=datetime(2026, 3, 9, tzinfo=UTC),
        run_id="run-site-medium-header-layout",
        overview_md="## Overview\n\nA medium-width header regression guard.\n",
        topics=["agents"],
        clusters=[],
        highlights=["Dense nav should fold into an intentional second row."],
        language_code="en",
    )
    _ = write_markdown_trend_note(
        output_dir=output_dir / "Localized" / "zh-cn",
        trend_doc_id=831,
        title="中等断点检查",
        granularity="day",
        period_start=datetime(2026, 3, 8, tzinfo=UTC),
        period_end=datetime(2026, 3, 9, tzinfo=UTC),
        run_id="run-site-medium-header-layout-zh",
        overview_md="## Overview\n\n一个中等宽度 header 回归保护。\n",
        topics=["agents"],
        clusters=[],
        highlights=["中等宽度时导航应切成有意的第二行。"],
        language_code="zh-CN",
    )

    site_dir = tmp_path / "site"
    _ = export_trend_static_site(
        input_dir=output_dir,
        output_dir=site_dir,
        default_language_code="en",
    )

    stylesheet = (site_dir / "en" / "assets" / "site.css").read_text(encoding="utf-8")
    assert "@media (max-width: 1040px) {" in stylesheet
    assert "order: 3;" in stylesheet
    assert "border-top: 1px solid rgba(17, 41, 71, 0.08);" in stylesheet
    assert "padding-top: 10px;" in stylesheet
    assert "white-space: nowrap;" in stylesheet


def test_export_trend_static_site_adds_bridge_header_breakpoint_before_mobile_stack(
    tmp_path: Path,
) -> None:
    """Regression: the header utility row should get its own line before the full mobile nav stack."""
    output_dir = tmp_path / "notes"
    _ = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=832,
        title="Bridge breakpoint check",
        granularity="day",
        period_start=datetime(2026, 3, 8, tzinfo=UTC),
        period_end=datetime(2026, 3, 9, tzinfo=UTC),
        run_id="run-site-bridge-header-layout",
        overview_md="## Overview\n\nA bridge-width header regression guard.\n",
        topics=["agents"],
        clusters=[],
        highlights=["Utility controls should separate before the full mobile stack."],
        language_code="en",
    )
    _ = write_markdown_trend_note(
        output_dir=output_dir / "Localized" / "zh-cn",
        trend_doc_id=832,
        title="桥接断点检查",
        granularity="day",
        period_start=datetime(2026, 3, 8, tzinfo=UTC),
        period_end=datetime(2026, 3, 9, tzinfo=UTC),
        run_id="run-site-bridge-header-layout-zh",
        overview_md="## Overview\n\n一个桥接宽度 header 回归保护。\n",
        topics=["agents"],
        clusters=[],
        highlights=["在完整 mobile 栈之前，utility controls 应先独立成行。"],
        language_code="zh-CN",
    )

    site_dir = tmp_path / "site"
    _ = export_trend_static_site(
        input_dir=output_dir,
        output_dir=site_dir,
        default_language_code="en",
    )

    stylesheet = (site_dir / "en" / "assets" / "site.css").read_text(encoding="utf-8")
    assert "@media (max-width: 820px) {" in stylesheet
    assert "width: 100%;" in stylesheet
    assert "margin-left: 0;" in stylesheet
    assert "justify-content: space-between;" in stylesheet


def test_export_trend_static_site_uses_single_card_columns_and_equal_width_pairs(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "notes"
    _ = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=84,
        title="Single-column layout check",
        granularity="day",
        period_start=datetime(2026, 3, 8, tzinfo=UTC),
        period_end=datetime(2026, 3, 9, tzinfo=UTC),
        run_id="run-site-home-single-column",
        overview_md="## Overview\n\nA home layout regression guard.\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
    )
    ideas_dir = output_dir / "Ideas"
    ideas_dir.mkdir(parents=True, exist_ok=True)
    (ideas_dir / "day--2026-03-08--ideas.md").write_text(
        "---\n"
        "kind: ideas\n"
        "granularity: day\n"
        "period_start: 2026-03-08T00:00:00+00:00\n"
        "period_end: 2026-03-09T00:00:00+00:00\n"
        "status: succeeded\n"
        "---\n\n"
        "# Layout guard ideas\n\n"
        "## Summary\n\n"
        "Idea-side layout check.\n",
        encoding="utf-8",
    )

    site_dir = tmp_path / "site"
    _ = export_trend_static_site(input_dir=output_dir / "Trends", output_dir=site_dir)

    stylesheet = (site_dir / "assets" / "site.css").read_text(encoding="utf-8")
    assert ".paired-collection-layout {" in stylesheet
    assert "grid-template-columns: repeat(2, minmax(0, 1fr));" in stylesheet
    assert ".collection-section .trend-grid {" in stylesheet
    assert "grid-template-columns: 1fr;" in stylesheet


def test_export_trend_static_site_home_window_uses_idea_only_range(
    tmp_path: Path,
) -> None:
    """Regression: idea-only exports should not show an empty home-window summary."""
    notes_root = tmp_path / "notes"
    trends_dir = notes_root / "Trends"
    trends_dir.mkdir(parents=True, exist_ok=True)
    ideas_dir = notes_root / "Ideas"
    ideas_dir.mkdir(parents=True, exist_ok=True)
    (ideas_dir / "day--2026-03-09--ideas.md").write_text(
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
        "Ship a prompt release gate.\n",
        encoding="utf-8",
    )

    site_dir = tmp_path / "site"
    _ = export_trend_static_site(input_dir=trends_dir, output_dir=site_dir)

    index_html = (site_dir / "index.html").read_text(encoding="utf-8")
    assert (
        "<div class='meta-panel-label'>Window</div>"
        "<div class='meta-panel-value'>2026-03-09 to 2026-03-09</div>" in index_html
    )
    assert "<div class='meta-panel-value'>n/a</div>" not in index_html


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


def test_stage_trend_site_source_preserves_localized_roots_for_round_trip(
    tmp_path: Path,
) -> None:
    notes_root = tmp_path / "notes"
    trend_note = write_markdown_trend_note(
        output_dir=notes_root,
        trend_doc_id=81,
        title="Agent Systems",
        granularity="day",
        period_start=datetime(2026, 3, 2, tzinfo=UTC),
        period_end=datetime(2026, 3, 3, tzinfo=UTC),
        run_id="run-stage-multilang-en",
        overview_md="## Overview\n\nEnglish note.\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
        language_code="en",
    )
    write_markdown_trend_note(
        output_dir=notes_root / "Localized" / "zh-cn",
        trend_doc_id=81,
        title="智能体系统",
        granularity="day",
        period_start=datetime(2026, 3, 2, tzinfo=UTC),
        period_end=datetime(2026, 3, 3, tzinfo=UTC),
        run_id="run-stage-multilang-zh",
        overview_md="## Overview\n\n中文笔记。\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
        language_code="zh-CN",
    )

    staged_dir = tmp_path / "site-content" / "Trends"
    manifest_path = stage_trend_site_source(
        input_dir=notes_root,
        output_dir=staged_dir,
        default_language_code="en",
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["languages"] == ["en", "zh-cn"]
    assert manifest["default_language_code"] == "en"
    assert (staged_dir / trend_note.name).exists()
    assert (
        tmp_path / "site-content" / "Localized" / "zh-cn" / "Trends" / trend_note.name
    ).exists()

    site_dir = tmp_path / "site"
    export_trend_static_site(
        input_dir=tmp_path / "site-content",
        output_dir=site_dir,
        default_language_code="en",
    )
    assert (site_dir / "en" / "trends" / f"{trend_note.stem}.html").exists()
    assert (site_dir / "zh-cn" / "trends" / f"{trend_note.stem}.html").exists()


def test_export_trend_static_site_discovers_legacy_grouped_localized_roots(
    tmp_path: Path,
) -> None:
    notes_root = tmp_path / "notes"
    en_embodied = notes_root / "Streams" / "embodied_ai"
    zh_embodied = en_embodied / "Localized" / "zh-cn"
    en_software = notes_root / "Streams" / "software_intelligence"
    zh_software = en_software / "Localized" / "zh-cn"

    _ = write_markdown_trend_note(
        output_dir=en_embodied,
        trend_doc_id=181,
        title="Embodied Weekly",
        granularity="week",
        period_start=datetime(2026, 3, 9, tzinfo=UTC),
        period_end=datetime(2026, 3, 16, tzinfo=UTC),
        run_id="run-stream-en-embodied",
        overview_md="## Overview\n\nEnglish embodied note.\n",
        topics=["robotics"],
        clusters=[],
        highlights=[],
        language_code="en",
    )
    write_markdown_trend_note(
        output_dir=zh_embodied,
        trend_doc_id=181,
        title="具身周报",
        granularity="week",
        period_start=datetime(2026, 3, 9, tzinfo=UTC),
        period_end=datetime(2026, 3, 16, tzinfo=UTC),
        run_id="run-stream-zh-embodied",
        overview_md="## Overview\n\n中文具身笔记。\n",
        topics=["robotics"],
        clusters=[],
        highlights=[],
        language_code="zh-CN",
    )
    _ = write_markdown_trend_note(
        output_dir=en_software,
        trend_doc_id=182,
        title="Software Weekly",
        granularity="week",
        period_start=datetime(2026, 3, 9, tzinfo=UTC),
        period_end=datetime(2026, 3, 16, tzinfo=UTC),
        run_id="run-stream-en-software",
        overview_md="## Overview\n\nEnglish software note.\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
        language_code="en",
    )
    write_markdown_trend_note(
        output_dir=zh_software,
        trend_doc_id=182,
        title="软件周报",
        granularity="week",
        period_start=datetime(2026, 3, 9, tzinfo=UTC),
        period_end=datetime(2026, 3, 16, tzinfo=UTC),
        run_id="run-stream-zh-software",
        overview_md="## Overview\n\n中文软件笔记。\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
        language_code="zh-CN",
    )

    site_dir = tmp_path / "site"
    with pytest.raises(ValueError, match="legacy Streams layouts"):
        export_trend_static_site(
            input_dir=notes_root,
            output_dir=site_dir,
            default_language_code="en",
        )


def test_export_trend_static_site_preserves_explicit_instance_names_across_languages(
    tmp_path: Path,
) -> None:
    embodied_root = tmp_path / "embodied"
    embodied_zh_root = embodied_root / "Localized" / "zh-cn"
    software_root = tmp_path / "software"
    software_zh_root = software_root / "Localized" / "zh-cn"

    embodied_en = write_markdown_trend_note(
        output_dir=embodied_root,
        trend_doc_id=601,
        title="Embodied Weekly",
        granularity="week",
        period_start=datetime(2026, 3, 9, tzinfo=UTC),
        period_end=datetime(2026, 3, 16, tzinfo=UTC),
        run_id="run-instance-en-embodied",
        overview_md="## Overview\n\nEnglish embodied note.\n",
        topics=["robotics"],
        clusters=[],
        highlights=[],
        language_code="en",
    )
    write_markdown_trend_note(
        output_dir=embodied_zh_root,
        trend_doc_id=601,
        title="具身周报",
        granularity="week",
        period_start=datetime(2026, 3, 9, tzinfo=UTC),
        period_end=datetime(2026, 3, 16, tzinfo=UTC),
        run_id="run-instance-zh-embodied",
        overview_md="## Overview\n\n中文具身笔记。\n",
        topics=["robotics"],
        clusters=[],
        highlights=[],
        language_code="zh-CN",
    )
    software_en = write_markdown_trend_note(
        output_dir=software_root,
        trend_doc_id=601,
        title="Software Weekly",
        granularity="week",
        period_start=datetime(2026, 3, 9, tzinfo=UTC),
        period_end=datetime(2026, 3, 16, tzinfo=UTC),
        run_id="run-instance-en-software",
        overview_md="## Overview\n\nEnglish software note.\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
        language_code="en",
    )
    write_markdown_trend_note(
        output_dir=software_zh_root,
        trend_doc_id=601,
        title="软件周报",
        granularity="week",
        period_start=datetime(2026, 3, 9, tzinfo=UTC),
        period_end=datetime(2026, 3, 16, tzinfo=UTC),
        run_id="run-instance-zh-software",
        overview_md="## Overview\n\n中文软件笔记。\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
        language_code="zh-CN",
    )

    site_dir = tmp_path / "site"
    manifest_path = export_trend_static_site(
        input_dir=[
            TrendSiteInputSpec(path=embodied_root, instance="embodied_ai"),
            TrendSiteInputSpec(path=software_root, instance="software_intelligence"),
        ],
        output_dir=site_dir,
        default_language_code="en",
    )

    assert (
        site_dir / "en" / "trends" / f"embodied-ai--{embodied_en.stem}.html"
    ).exists()
    assert (
        site_dir / "en" / "trends" / f"software-intelligence--{software_en.stem}.html"
    ).exists()
    assert (
        site_dir / "zh-cn" / "trends" / f"embodied-ai--{embodied_en.stem}.html"
    ).exists()
    assert (
        site_dir
        / "zh-cn"
        / "trends"
        / f"software-intelligence--{software_en.stem}.html"
    ).exists()

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["languages"] == ["en", "zh-cn"]
    assert manifest["files"]["by_language"]["en"]["trend_pages"] == [
        f"trends/embodied-ai--{embodied_en.stem}.html",
        f"trends/software-intelligence--{software_en.stem}.html",
    ]
    assert manifest["files"]["by_language"]["zh-cn"]["trend_pages"] == [
        f"trends/embodied-ai--{embodied_en.stem}.html",
        f"trends/software-intelligence--{software_en.stem}.html",
    ]

    en_manifest = json.loads(
        (site_dir / "en" / "manifest.json").read_text(encoding="utf-8")
    )
    assert [entry["instance"] for entry in en_manifest["input_dirs"]] == [
        "embodied_ai",
        "software_intelligence",
    ]
    assert all("stream" not in entry for entry in en_manifest["input_dirs"])


def test_stage_trend_site_source_rejects_legacy_stream_localized_roots(
    tmp_path: Path,
) -> None:
    """Regression: legacy localized Streams trees must be rejected outright."""
    notes_root = tmp_path / "notes"
    en_stream = notes_root / "Streams" / "agents_lab"
    zh_stream = en_stream / "Localized" / "zh-cn"

    _ = write_markdown_trend_note(
        output_dir=en_stream,
        trend_doc_id=281,
        title="Agent Systems",
        granularity="week",
        period_start=datetime(2026, 3, 9, tzinfo=UTC),
        period_end=datetime(2026, 3, 16, tzinfo=UTC),
        run_id="run-stage-stream-en",
        overview_md="## Overview\n\nEnglish stream note.\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
        language_code="en",
    )
    _ = write_markdown_trend_note(
        output_dir=zh_stream,
        trend_doc_id=281,
        title="智能体系统",
        granularity="week",
        period_start=datetime(2026, 3, 9, tzinfo=UTC),
        period_end=datetime(2026, 3, 16, tzinfo=UTC),
        run_id="run-stage-stream-zh",
        overview_md="## Overview\n\n中文流笔记。\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
        language_code="zh-CN",
    )

    staged_root = tmp_path / "site-content"
    with pytest.raises(ValueError, match="legacy Streams layouts"):
        stage_trend_site_source(
            input_dir=notes_root,
            output_dir=staged_root,
            default_language_code="en",
        )


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
    assert manifest["item_export_scope"] == "linked"
    assert manifest["items_total"] == 1
    assert manifest["items_available_total"] == 1
    assert manifest["items_unreferenced_total"] == 0
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


def test_export_trend_static_site_skips_unreferenced_item_pages_by_default(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "notes"
    linked_item = write_markdown_note(
        output_dir=output_dir,
        item_id=61,
        title="Linked Item",
        source="rss",
        canonical_url="https://example.com/linked-item",
        published_at=datetime(2026, 3, 3, tzinfo=UTC),
        authors=["Alice"],
        topics=["agents"],
        relevance_score=0.93,
        run_id="run-linked-item-1",
        summary="## Summary\n\nThe linked note should survive export.\n",
    )
    unlinked_item = write_markdown_note(
        output_dir=output_dir,
        item_id=62,
        title="Unlinked Item",
        source="rss",
        canonical_url="https://example.com/unlinked-item",
        published_at=datetime(2026, 3, 3, tzinfo=UTC),
        authors=["Bob"],
        topics=["agents"],
        relevance_score=0.31,
        run_id="run-unlinked-item-1",
        summary="## Summary\n\nThis note should stay out of the site build.\n",
    )
    trend_note = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=75,
        title="Agent Systems",
        granularity="day",
        period_start=datetime(2026, 3, 3, tzinfo=UTC),
        period_end=datetime(2026, 3, 4, tzinfo=UTC),
        run_id="run-site-items-filtered-1",
        overview_md=f"## Overview\n\nStart with [Linked Item](../Inbox/{linked_item.name}).\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
    )

    site_dir = tmp_path / "site"
    manifest_path = export_trend_static_site(
        input_dir=output_dir / "Trends",
        output_dir=site_dir,
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["item_export_scope"] == "linked"
    assert manifest["items_total"] == 1
    assert manifest["items_available_total"] == 2
    assert manifest["items_unreferenced_total"] == 1
    assert f"items/{linked_item.stem}.html" in manifest["files"]["item_pages"]
    assert f"items/{unlinked_item.stem}.html" not in manifest["files"]["item_pages"]

    assert (site_dir / "items" / f"{linked_item.stem}.html").exists()
    assert not (site_dir / "items" / f"{unlinked_item.stem}.html").exists()
    assert (site_dir / "artifacts" / "items" / linked_item.name).exists()
    assert not (site_dir / "artifacts" / "items" / unlinked_item.name).exists()

    detail_html = (site_dir / "trends" / f"{trend_note.stem}.html").read_text(
        encoding="utf-8"
    )
    assert f"../items/{linked_item.stem}.html" in detail_html
    assert "../Inbox/" not in detail_html


def test_export_trend_static_site_item_export_scope_all_preserves_full_item_export(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "notes"
    linked_item = write_markdown_note(
        output_dir=output_dir,
        item_id=63,
        title="Linked Item",
        source="rss",
        canonical_url="https://example.com/linked-item-all",
        published_at=datetime(2026, 3, 4, tzinfo=UTC),
        authors=["Alice"],
        topics=["agents"],
        relevance_score=0.94,
        run_id="run-linked-item-all-1",
        summary="## Summary\n\nThe linked note should survive export.\n",
    )
    unlinked_item = write_markdown_note(
        output_dir=output_dir,
        item_id=64,
        title="Unlinked Item",
        source="rss",
        canonical_url="https://example.com/unlinked-item-all",
        published_at=datetime(2026, 3, 4, tzinfo=UTC),
        authors=["Bob"],
        topics=["agents"],
        relevance_score=0.28,
        run_id="run-unlinked-item-all-1",
        summary="## Summary\n\nThe compatibility mode should still export this note.\n",
    )
    _ = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=76,
        title="Agent Systems",
        granularity="day",
        period_start=datetime(2026, 3, 4, tzinfo=UTC),
        period_end=datetime(2026, 3, 5, tzinfo=UTC),
        run_id="run-site-items-all-1",
        overview_md=f"## Overview\n\nStart with [Linked Item](../Inbox/{linked_item.name}).\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
    )

    site_dir = tmp_path / "site"
    manifest_path = export_trend_static_site(
        input_dir=output_dir / "Trends",
        output_dir=site_dir,
        item_export_scope="all",
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["item_export_scope"] == "all"
    assert manifest["items_total"] == 2
    assert manifest["items_available_total"] == 2
    assert manifest["items_unreferenced_total"] == 0
    assert f"items/{linked_item.stem}.html" in manifest["files"]["item_pages"]
    assert f"items/{unlinked_item.stem}.html" in manifest["files"]["item_pages"]

    assert (site_dir / "items" / f"{linked_item.stem}.html").exists()
    assert (site_dir / "items" / f"{unlinked_item.stem}.html").exists()
    assert (site_dir / "artifacts" / "items" / linked_item.name).exists()
    assert (site_dir / "artifacts" / "items" / unlinked_item.name).exists()


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
    assert manifest["files"]["trends_index"] == "trends/index.html"

    index_html = (site_dir / "index.html").read_text(encoding="utf-8")
    assert "Browse trends" in index_html
    assert "Trend briefs" in index_html
    assert "Idea briefs" in index_html
    assert "Verification-first agent rollout" in index_html

    trends_index_html = (site_dir / "trends" / "index.html").read_text(encoding="utf-8")
    assert "Code agents close the loop" in trends_index_html

    ideas_index_html = (site_dir / "ideas" / "index.html").read_text(encoding="utf-8")
    assert "Verification-first agent rollout" in ideas_index_html

    detail_html = idea_page.read_text(encoding="utf-8")
    assert f"../items/{item_note.stem}.html" in detail_html
    assert f"../trends/{trend_note.stem}.html" in detail_html
    assert "../Inbox/" not in detail_html
    assert "../Trends/" not in detail_html
    assert "Source markdown" in detail_html


def test_export_trend_static_site_builds_item_page_when_only_idea_links_it(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "notes"
    item_note = write_markdown_note(
        output_dir=output_dir,
        item_id=65,
        title="Idea-linked Item",
        source="rss",
        canonical_url="https://example.com/idea-linked-item",
        published_at=datetime(2026, 3, 10, tzinfo=UTC),
        authors=["Alice"],
        topics=["agents"],
        relevance_score=0.92,
        run_id="run-site-idea-only-item",
        summary="## Summary\n\nIdeas can be the only referrer.\n",
    )
    trend_note = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=94,
        title="Code agents close the loop",
        granularity="day",
        period_start=datetime(2026, 3, 10, tzinfo=UTC),
        period_end=datetime(2026, 3, 11, tzinfo=UTC),
        run_id="run-site-idea-only-trend",
        overview_md="## Overview\n\nNo direct item links here.\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
    )
    ideas_dir = output_dir / "Ideas"
    ideas_dir.mkdir(parents=True, exist_ok=True)
    idea_note = ideas_dir / "day--2026-03-10--ideas.md"
    idea_note.write_text(
        "---\n"
        "kind: ideas\n"
        "granularity: day\n"
        "period_start: 2026-03-10T00:00:00+00:00\n"
        "period_end: 2026-03-11T00:00:00+00:00\n"
        "status: succeeded\n"
        "topics:\n"
        "  - agents\n"
        "---\n\n"
        "# Verification-first agent rollout\n\n"
        "## Summary\n\n"
        f"Start with [Idea-linked Item](../Inbox/{item_note.name}) and [the daily trend](../Trends/{trend_note.name}).\n",
        encoding="utf-8",
    )

    site_dir = tmp_path / "site"
    manifest_path = export_trend_static_site(
        input_dir=output_dir / "Trends",
        output_dir=site_dir,
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["item_export_scope"] == "linked"
    assert manifest["items_total"] == 1
    assert manifest["items_available_total"] == 1
    assert manifest["items_unreferenced_total"] == 0
    assert (site_dir / "items" / f"{item_note.stem}.html").exists()

    idea_html = (site_dir / "ideas" / f"{idea_note.stem}.html").read_text(
        encoding="utf-8"
    )
    assert f"../items/{item_note.stem}.html" in idea_html
    assert "../Inbox/" not in idea_html


def test_export_trend_static_site_limit_applies_before_item_reference_selection(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "notes"
    older_item = write_markdown_note(
        output_dir=output_dir,
        item_id=66,
        title="Older linked item",
        source="rss",
        canonical_url="https://example.com/older-linked-item",
        published_at=datetime(2026, 3, 9, tzinfo=UTC),
        authors=["Alice"],
        topics=["agents"],
        relevance_score=0.9,
        run_id="run-site-limit-old-item",
        summary="## Summary\n\nOlder trend evidence.\n",
    )
    newer_item = write_markdown_note(
        output_dir=output_dir,
        item_id=67,
        title="Newer linked item",
        source="rss",
        canonical_url="https://example.com/newer-linked-item",
        published_at=datetime(2026, 3, 10, tzinfo=UTC),
        authors=["Bob"],
        topics=["agents"],
        relevance_score=0.95,
        run_id="run-site-limit-new-item",
        summary="## Summary\n\nNewer trend evidence.\n",
    )
    older_trend = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=95,
        title="Older day",
        granularity="day",
        period_start=datetime(2026, 3, 9, tzinfo=UTC),
        period_end=datetime(2026, 3, 10, tzinfo=UTC),
        run_id="run-site-limit-old-trend",
        overview_md=f"## Overview\n\nSee [Older linked item](../Inbox/{older_item.name}).\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
    )
    newer_trend = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=96,
        title="Newer day",
        granularity="day",
        period_start=datetime(2026, 3, 10, tzinfo=UTC),
        period_end=datetime(2026, 3, 11, tzinfo=UTC),
        run_id="run-site-limit-new-trend",
        overview_md=f"## Overview\n\nSee [Newer linked item](../Inbox/{newer_item.name}).\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
    )

    site_dir = tmp_path / "site"
    manifest_path = export_trend_static_site(
        input_dir=output_dir / "Trends",
        output_dir=site_dir,
        limit=1,
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["item_export_scope"] == "linked"
    assert manifest["trends_total"] == 1
    assert manifest["items_total"] == 1
    assert manifest["items_available_total"] == 2
    assert manifest["items_unreferenced_total"] == 1
    assert (site_dir / "trends" / f"{newer_trend.stem}.html").exists()
    assert not (site_dir / "trends" / f"{older_trend.stem}.html").exists()
    assert (site_dir / "items" / f"{newer_item.stem}.html").exists()
    assert not (site_dir / "items" / f"{older_item.stem}.html").exists()


def test_export_trend_static_site_builds_peer_trend_navigation_and_detail_context(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "notes"
    trend_note = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=93,
        title="Code agents close the loop",
        granularity="day",
        period_start=datetime(2026, 3, 9, tzinfo=UTC),
        period_end=datetime(2026, 3, 10, tzinfo=UTC),
        run_id="run-site-trends-peer-nav",
        overview_md="## Overview\n\nAgent workflows keep tightening.\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
    )
    ideas_dir = output_dir / "Ideas"
    ideas_dir.mkdir(parents=True, exist_ok=True)
    (ideas_dir / "day--2026-03-09--ideas.md").write_text(
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
    manifest_path = export_trend_static_site(
        input_dir=output_dir / "Trends",
        output_dir=site_dir,
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["files"]["trends_index"] == "trends/index.html"

    home_html = (site_dir / "index.html").read_text(encoding="utf-8")
    assert "Browse trends" in home_html
    assert "Trend briefs" in home_html
    assert "Idea briefs" in home_html

    detail_html = (site_dir / "trends" / f"{trend_note.stem}.html").read_text(
        encoding="utf-8"
    )
    assert "href='index.html'>Trends</a>" in detail_html
    assert "Trend brief" in detail_html


def test_export_trend_static_site_aggregates_idea_topics_into_home_and_topic_pages(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "notes"
    _ = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=94,
        title="Code agents close the loop",
        granularity="day",
        period_start=datetime(2026, 3, 9, tzinfo=UTC),
        period_end=datetime(2026, 3, 10, tzinfo=UTC),
        run_id="run-site-topic-aggregation-trend",
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
        "  - deployment\n"
        "---\n\n"
        "# Verification-first agent rollout\n\n"
        "## Summary\n\n"
        "Ship a prompt release gate.\n",
        encoding="utf-8",
    )

    site_dir = tmp_path / "site"
    manifest_path = export_trend_static_site(
        input_dir=output_dir / "Trends",
        output_dir=site_dir,
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["topics_total"] == 2
    assert "topics/deployment.html" in manifest["files"]["topic_pages"]

    home_html = (site_dir / "index.html").read_text(encoding="utf-8")
    assert "topics/deployment.html" in home_html

    ideas_index_html = (site_dir / "ideas" / "index.html").read_text(encoding="utf-8")
    assert "topics/deployment.html" in ideas_index_html

    topic_html = (site_dir / "topics" / "deployment.html").read_text(encoding="utf-8")
    assert "Verification-first agent rollout" in topic_html
    assert ">Topic summary<" in topic_html
    assert ">Trend briefs<" in topic_html
    assert ">Idea briefs<" in topic_html
    assert f"../ideas/{idea_note.stem}.html" in topic_html


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
        "### Best bet: Prompt CI gate\n"
        "- Type: Workflow shift\n"
        "- Horizon: Now\n"
        "- Role: Internal agent platform owners responsible for prompt rollout safety\n\n"
        "**Thesis.** Add a prompt release gate before rollout.\n\n"
        "**Why now.** Teams now have enough agent activity to justify structured release controls.\n\n"
        "**What changed.** More agent traffic means regressions show up faster and cost more.\n\n"
        "**Validation next step.** Pilot the gate on one high-volume internal workflow.\n\n"
        "#### Evidence\n"
        f"- [CodeScout](../Inbox/{item_note.name})\n"
        f"- [Daily trend](../Trends/{trend_note.name})\n\n"
        "### Alternate: Operator review lane\n"
        "- Type: Workflow shift\n"
        "- Horizon: Near-term\n"
        "- Role: Applied AI ops\n\n"
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
    stylesheet = (site_dir / "assets" / "site.css").read_text(encoding="utf-8")
    assert "summary-grid summary-grid-single" in detail_html
    assert "idea-opportunity-grid" in detail_html
    assert detail_html.count("idea-opportunity-card") == 2
    assert "idea-opportunity-meta-row" in detail_html
    assert "idea-opportunity-block-role" in detail_html
    assert "idea-evidence-list" in detail_html
    assert "2 opportunities" in detail_html
    assert "Best bet: Prompt CI gate" in detail_html
    assert "Alternate: Operator review lane" in detail_html
    assert "User/job" not in detail_html
    assert ">Role<" in detail_html
    assert f"../items/{item_note.stem}.html" in detail_html
    assert f"../trends/{trend_note.stem}.html" in detail_html
    assert ".detail-content .idea-opportunity-role-value {" in stylesheet
    assert "-webkit-line-clamp: 2;" not in stylesheet


def test_export_trend_static_site_prefers_presentation_sidecar_for_trend_detail_pages(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "notes"
    note_path = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=94,
        title="Agent systems",
        granularity="day",
        period_start=datetime(2026, 3, 9, tzinfo=UTC),
        period_end=datetime(2026, 3, 10, tzinfo=UTC),
        run_id="run-site-trend-sidecar-first",
        overview_md="Sidecar overview should win.",
        topics=["agents"],
        clusters=[
            {
                "name": "Reward models",
                "description": "Cluster summary from sidecar.",
                "representative_chunks": [
                    {
                        "title": "CodeScout",
                        "note_href": "../Inbox/2026-03-09--codescout.md",
                        "url": "https://example.com/codescout",
                        "authors": ["Alice"],
                    }
                ],
            }
        ],
        highlights=[],
    )
    sidecar_path = presentation_sidecar_path(note_path=note_path)
    trend_sidecar = json.loads(sidecar_path.read_text(encoding="utf-8"))
    representative = trend_sidecar["content"]["representative_sources"][0]
    representative["doc_id"] = 52
    representative["chunk_index"] = 0
    representative["source_type"] = "paper"
    representative["confidence"] = "high"
    trend_sidecar["content"]["clusters"][0]["representative_sources"][0].update(
        {
            "doc_id": 52,
            "chunk_index": 0,
            "source_type": "paper",
            "confidence": "high",
        }
    )
    sidecar_path.write_text(
        json.dumps(trend_sidecar, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    note_path.write_text(
        "---\n"
        "kind: trend\n"
        "granularity: day\n"
        "period_start: 2026-03-09T00:00:00+00:00\n"
        "period_end: 2026-03-10T00:00:00+00:00\n"
        "topics:\n"
        "  - agents\n"
        "---\n\n"
        "# Markdown title should lose\n\n"
        "## Overview\n\n"
        "This markdown overview should be ignored.\n",
        encoding="utf-8",
    )

    site_dir = tmp_path / "site"
    export_trend_static_site(input_dir=output_dir / "Trends", output_dir=site_dir)

    detail_html = (site_dir / "trends" / f"{note_path.stem}.html").read_text(
        encoding="utf-8"
    )
    assert "Agent systems" in detail_html
    assert "Sidecar overview should win." in detail_html
    assert "Reward models" in detail_html
    assert "CodeScout" in detail_html
    assert "Source type" in detail_html
    assert "paper" in detail_html.lower()
    assert "Confidence" in detail_html
    assert "high" in detail_html.lower()
    assert "Markdown title should lose" not in detail_html
    assert "This markdown overview should be ignored." not in detail_html


def test_export_trend_static_site_falls_back_when_trend_sidecar_shift_rank_is_invalid(
    tmp_path: Path,
) -> None:
    """Regression: malformed trend shift ranks must not abort markdown fallback."""
    output_dir = tmp_path / "notes"
    note_path = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=198,
        title="Markdown trend title wins",
        granularity="day",
        period_start=datetime(2026, 3, 13, tzinfo=UTC),
        period_end=datetime(2026, 3, 14, tzinfo=UTC),
        run_id="run-site-invalid-trend-shift-rank",
        overview_md="## Overview\n\nMarkdown trend overview should remain readable.\n",
        topics=["agents"],
        evolution={
            "summary_md": "Markdown evolution summary should remain readable.",
            "signals": [
                {
                    "theme": "Verification moves earlier",
                    "change_type": "continuing",
                    "summary": "Markdown shift summary should remain readable.",
                    "history_windows": [],
                }
            ],
        },
        clusters=[],
        highlights=[],
    )
    sidecar_path = presentation_sidecar_path(note_path=note_path)
    trend_sidecar = json.loads(sidecar_path.read_text(encoding="utf-8"))
    trend_sidecar["content"]["title"] = "Broken sidecar title should lose"
    trend_sidecar["content"]["overview"] = "Broken sidecar overview should lose."
    trend_sidecar["content"]["ranked_shifts"][0]["rank"] = "first"
    sidecar_path.write_text(
        json.dumps(trend_sidecar, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    site_dir = tmp_path / "site"
    export_trend_static_site(input_dir=output_dir / "Trends", output_dir=site_dir)

    detail_html = (site_dir / "trends" / f"{note_path.stem}.html").read_text(
        encoding="utf-8"
    )
    assert "Markdown trend title wins" in detail_html
    assert "Markdown trend overview should remain readable." in detail_html
    assert "Markdown evolution summary should remain readable." in detail_html
    assert "Broken sidecar title should lose" not in detail_html
    assert "Broken sidecar overview should lose." not in detail_html


def test_export_trend_static_site_prefers_presentation_sidecar_for_idea_detail_pages(
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
        run_id="run-site-ideas-sidecar-item",
        summary="## Summary\n\nPrompt release notes.\n",
    )
    trend_note = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=95,
        title="Agent systems",
        granularity="day",
        period_start=datetime(2026, 3, 9, tzinfo=UTC),
        period_end=datetime(2026, 3, 10, tzinfo=UTC),
        run_id="run-site-ideas-sidecar-trend",
        overview_md="Trend note.",
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
        "# Markdown idea title should lose\n\n"
        "## Summary\n\n"
        "This markdown summary should be ignored.\n",
        encoding="utf-8",
    )
    idea_presentation = build_idea_presentation_v1(
        source_markdown_path=f"Ideas/{idea_note.name}",
        title="Verification-first agent rollout",
        summary_md="Start with structured release controls.",
        ideas=[
            SimpleNamespace(
                title="Prompt CI gate",
                kind="workflow_shift",
                time_horizon="now",
                user_or_job="Internal agent platform owners responsible for prompt rollout safety",
                thesis="Add a prompt release gate before rollout.",
                why_now="Teams now have enough agent activity to justify structured release controls.",
                what_changed="More agent traffic means regressions show up faster and cost more.",
                validation_next_step="Pilot the gate on one high-volume internal workflow.",
                evidence_refs=[
                    SimpleNamespace(
                        doc_id=52,
                        chunk_index=0,
                        title="CodeScout",
                        href=f"../Inbox/{item_note.name}",
                        authors=["Alice"],
                        source="arxiv",
                        score=0.91,
                        reason="Prompt release notes.",
                    ),
                    SimpleNamespace(
                        doc_id=95,
                        chunk_index=0,
                        title="Daily trend",
                        href=f"../Trends/{trend_note.name}",
                        authors=[],
                        source="rss",
                        score=0.62,
                        reason="Daily trend summary.",
                    ),
                ],
            )
        ],
    )
    opportunity = idea_presentation["content"]["opportunities"][0]
    opportunity["evidence"][0].update(
        {
            "title": "CodeScout",
            "href": f"../Inbox/{item_note.name}",
            "authors": ["Alice"],
            "source_type": "paper",
            "confidence": "high",
        }
    )
    opportunity["evidence"][1].update(
        {
            "title": "Daily trend",
            "href": f"../Trends/{trend_note.name}",
            "authors": [],
            "source_type": "unknown",
            "confidence": "medium",
        }
    )
    write_presentation_sidecar(note_path=idea_note, presentation=idea_presentation)

    site_dir = tmp_path / "site"
    export_trend_static_site(input_dir=output_dir / "Trends", output_dir=site_dir)

    detail_html = (site_dir / "ideas" / f"{idea_note.stem}.html").read_text(
        encoding="utf-8"
    )
    assert "Verification-first agent rollout" in detail_html
    assert "Start with structured release controls." in detail_html
    assert "Prompt CI gate" in detail_html
    assert "Prompt release notes." in detail_html
    assert "Source type" in detail_html
    assert "paper" in detail_html.lower()
    assert "Confidence" in detail_html
    assert "high" in detail_html.lower()
    assert f"../items/{item_note.stem}.html" in detail_html
    assert f"../trends/{trend_note.stem}.html" in detail_html
    assert "Markdown idea title should lose" not in detail_html
    assert "This markdown summary should be ignored." not in detail_html

    soup = BeautifulSoup(detail_html, "html.parser")
    evidence_lists = soup.select(
        ".idea-opportunity-block-evidence .idea-evidence-list > ul"
    )
    assert len(evidence_lists) == 1
    top_level_items = evidence_lists[0].find_all("li", recursive=False)
    assert len(top_level_items) == 2
    assert all(not item.find_all("li", recursive=False) for item in top_level_items)


def test_export_trend_static_site_keeps_phase1_idea_sidecar_evidence_without_titles(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "notes"
    _ = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=196,
        title="Agent systems",
        granularity="day",
        period_start=datetime(2026, 3, 9, tzinfo=UTC),
        period_end=datetime(2026, 3, 10, tzinfo=UTC),
        run_id="run-site-ideas-phase1-sidecar-trend",
        overview_md="Trend note.",
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
        "# Legacy phase 1 idea note\n\n"
        "## Summary\n\n"
        "Legacy markdown should only be fallback.\n",
        encoding="utf-8",
    )
    idea_presentation = build_idea_presentation_v1(
        source_markdown_path=f"Ideas/{idea_note.name}",
        title="Verification-first agent rollout",
        summary_md="Start with structured release controls.",
        ideas=[
            SimpleNamespace(
                title="Prompt CI gate",
                kind="workflow_shift",
                time_horizon="now",
                user_or_job="Internal agent platform owners",
                thesis="Add a prompt release gate before rollout.",
                why_now="Teams now have enough agent activity to justify structured release controls.",
                what_changed="More agent traffic means regressions show up faster and cost more.",
                validation_next_step="Pilot the gate on one high-volume internal workflow.",
                evidence_refs=[
                    SimpleNamespace(
                        doc_id=196,
                        chunk_index=0,
                        reason="Historical sidecars only preserved doc ids and reasons.",
                    )
                ],
            )
        ],
    )
    opportunity = idea_presentation["content"]["opportunities"][0]
    opportunity["evidence"][0].pop("title", None)
    opportunity["evidence"][0].pop("href", None)
    opportunity["evidence"][0].pop("url", None)
    opportunity["evidence"][0].pop("authors", None)
    opportunity["evidence"][0].pop("source_type", None)
    opportunity["evidence"][0].pop("confidence", None)
    write_presentation_sidecar(note_path=idea_note, presentation=idea_presentation)

    site_dir = tmp_path / "site"
    export_trend_static_site(input_dir=output_dir / "Trends", output_dir=site_dir)

    detail_html = (site_dir / "ideas" / f"{idea_note.stem}.html").read_text(
        encoding="utf-8"
    )
    assert "Verification-first agent rollout" in detail_html
    assert "Document 196" in detail_html
    assert "Historical sidecars only preserved doc ids and reasons." in detail_html
    assert "Legacy markdown should only be fallback." not in detail_html


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


def test_export_trend_static_site_skips_site_excluded_trend_and_idea_notes(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "notes"
    _ = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=94,
        title="No publishable research trend for this period",
        granularity="day",
        period_start=datetime(2026, 3, 13, tzinfo=UTC),
        period_end=datetime(2026, 3, 14, tzinfo=UTC),
        run_id="run-site-excluded-trend",
        overview_md="- No documents available for this period.\n",
        topics=[],
        clusters=[],
        highlights=[],
        site_exclude=True,
    )
    ideas_dir = output_dir / "Ideas"
    ideas_dir.mkdir(parents=True, exist_ok=True)
    excluded_idea = ideas_dir / "day--2026-03-13--ideas.md"
    excluded_idea.write_text(
        "---\n"
        "kind: ideas\n"
        "granularity: day\n"
        "period_start: 2026-03-13T00:00:00+00:00\n"
        "period_end: 2026-03-14T00:00:00+00:00\n"
        "status: suppressed\n"
        "site_exclude: true\n"
        "---\n\n"
        "# No publishable ideas for this period\n\n"
        "## Summary\n\n"
        "No documents available for this period.\n",
        encoding="utf-8",
    )

    site_dir = tmp_path / "site"
    manifest_path = export_trend_static_site(
        input_dir=output_dir / "Trends",
        output_dir=site_dir,
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["trends_total"] == 0
    assert manifest["ideas_total"] == 0
    assert manifest["files"]["trend_pages"] == []
    assert manifest["files"]["idea_pages"] == []


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


def test_export_trend_static_site_falls_back_when_sidecar_schema_version_is_invalid_string(
    tmp_path: Path,
) -> None:
    """Regression: malformed sidecar schema versions must not abort markdown fallback."""
    output_dir = tmp_path / "notes"
    note = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=189,
        title="Markdown title wins",
        granularity="day",
        period_start=datetime(2026, 3, 11, tzinfo=UTC),
        period_end=datetime(2026, 3, 12, tzinfo=UTC),
        run_id="run-site-invalid-sidecar-schema-version",
        overview_md="## Overview\n\nMarkdown overview should remain readable.\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
    )
    sidecar_path = presentation_sidecar_path(note_path=note)
    sidecar_payload = json.loads(sidecar_path.read_text(encoding="utf-8"))
    sidecar_payload["presentation_schema_version"] = "v1"
    sidecar_payload["content"]["title"] = "Broken sidecar title should lose"
    sidecar_payload["content"]["overview"] = "Broken sidecar overview should lose."
    sidecar_path.write_text(
        json.dumps(sidecar_payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    site_dir = tmp_path / "site"
    export_trend_static_site(input_dir=output_dir / "Trends", output_dir=site_dir)

    detail_html = (site_dir / "trends" / f"{note.stem}.html").read_text(
        encoding="utf-8"
    )
    assert "Markdown title wins" in detail_html
    assert "Markdown overview should remain readable." in detail_html
    assert "Broken sidecar title should lose" not in detail_html
    assert "Broken sidecar overview should lose." not in detail_html


def test_export_trend_static_site_falls_back_when_sidecar_payload_shape_is_invalid(
    tmp_path: Path,
) -> None:
    """Regression: malformed sidecars must not abort site export."""
    output_dir = tmp_path / "notes"
    _ = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=197,
        title="Agent systems",
        granularity="day",
        period_start=datetime(2026, 3, 12, tzinfo=UTC),
        period_end=datetime(2026, 3, 13, tzinfo=UTC),
        run_id="run-site-invalid-sidecar-shape-trend",
        overview_md="Trend note.",
        topics=["agents"],
        clusters=[],
        highlights=[],
    )
    ideas_dir = output_dir / "Ideas"
    ideas_dir.mkdir(parents=True, exist_ok=True)
    idea_note = ideas_dir / "day--2026-03-12--ideas.md"
    idea_note.write_text(
        "---\n"
        "kind: ideas\n"
        "granularity: day\n"
        "period_start: 2026-03-12T00:00:00+00:00\n"
        "period_end: 2026-03-13T00:00:00+00:00\n"
        "status: succeeded\n"
        "---\n\n"
        "# Markdown idea title wins\n\n"
        "## Summary\n\n"
        "Markdown summary should remain readable.\n",
        encoding="utf-8",
    )
    idea_presentation = build_idea_presentation_v1(
        source_markdown_path=f"Ideas/{idea_note.name}",
        title="Broken sidecar title should lose",
        summary_md="Broken sidecar summary should lose.",
        ideas=[
            SimpleNamespace(
                title="Prompt CI gate",
                kind="workflow_shift",
                time_horizon="now",
                user_or_job="Internal agent platform owners",
                thesis="Add a prompt release gate before rollout.",
                why_now="Teams now have enough agent activity to justify structured release controls.",
                what_changed="More agent traffic means regressions show up faster and cost more.",
                validation_next_step="Pilot the gate on one high-volume internal workflow.",
                evidence_refs=[],
            )
        ],
    )
    sidecar_path = presentation_sidecar_path(note_path=idea_note)
    write_presentation_sidecar(note_path=idea_note, presentation=idea_presentation)
    sidecar_payload = json.loads(sidecar_path.read_text(encoding="utf-8"))
    sidecar_payload["content"]["title"] = "Broken sidecar title should lose"
    sidecar_payload["content"]["summary"] = "Broken sidecar summary should lose."
    sidecar_payload["content"]["opportunities"][0]["display_kind"] = 1
    sidecar_path.write_text(
        json.dumps(sidecar_payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    site_dir = tmp_path / "site"
    export_trend_static_site(input_dir=output_dir / "Trends", output_dir=site_dir)

    detail_html = (site_dir / "ideas" / f"{idea_note.stem}.html").read_text(
        encoding="utf-8"
    )
    assert "Markdown idea title wins" in detail_html
    assert "Markdown summary should remain readable." in detail_html
    assert "Broken sidecar title should lose" not in detail_html
    assert "Broken sidecar summary should lose." not in detail_html


def test_export_trend_static_site_uses_sidecar_even_when_markdown_contains_evolution(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "notes"
    note = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=188,
        title="Verification-first trend",
        granularity="day",
        period_start=datetime(2026, 3, 10, tzinfo=UTC),
        period_end=datetime(2026, 3, 11, tzinfo=UTC),
        run_id="run-site-sidecar-with-evolution",
        overview_md="## Overview\n\nCanonical overview from the sidecar should win.\n",
        topics=["agents"],
        evolution={
            "summary_md": "Evolution summary should remain visible even when sidecar rendering wins.",
            "signals": [
                {
                    "theme": "Runtime verification gets explicit",
                    "change_type": "continuing",
                    "summary": "The validation loop now exposes runtime checks earlier in the workflow.",
                    "history_windows": [],
                }
            ],
        },
        clusters=[
            {
                "name": "Verification loops",
                "description": "Sidecar cluster summary should win.",
                "representative_chunks": [
                    {
                        "doc_id": 42,
                        "chunk_index": 0,
                        "title": "CodeScout",
                        "href": "../Inbox/2026-03-10--codescout.md",
                        "authors": ["Alice"],
                        "source": "arxiv",
                        "score": 0.91,
                    }
                ],
            }
        ],
        highlights=[],
    )
    note.write_text(
        note.read_text(encoding="utf-8")
        .replace("# Verification-first trend", "# Markdown title should lose")
        .replace(
            "Canonical overview from the sidecar should win.",
            "Markdown overview should be ignored in favor of the sidecar.",
        ),
        encoding="utf-8",
    )

    site_dir = tmp_path / "site"
    export_trend_static_site(input_dir=output_dir / "Trends", output_dir=site_dir)

    detail_html = (site_dir / "trends" / f"{note.stem}.html").read_text(
        encoding="utf-8"
    )
    assert "Verification-first trend" in detail_html
    assert "Markdown title should lose" not in detail_html
    assert "Canonical overview from the sidecar should win." in detail_html
    assert (
        "Markdown overview should be ignored in favor of the sidecar."
        not in detail_html
    )
    assert (
        "Evolution summary should remain visible even when sidecar rendering wins."
        in detail_html
    )
    assert "Runtime verification gets explicit" in detail_html
    assert "Verification loops" in detail_html
    assert "CodeScout" in detail_html
    assert "Source type" in detail_html
    assert "paper" in detail_html.lower()


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


def test_export_trend_static_site_rejects_legacy_grouped_inputs(
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

    _ = write_markdown_trend_note(
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
    with pytest.raises(ValueError, match="legacy Streams layouts"):
        export_trend_static_site(
            input_dir=notes_root,
            output_dir=site_dir,
        )


def test_export_trend_static_site_rejects_legacy_grouped_idea_inputs(
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
    with pytest.raises(ValueError, match="legacy Streams layouts"):
        export_trend_static_site(
            input_dir=notes_root,
            output_dir=site_dir,
        )


def test_export_trend_static_site_namespaces_duplicate_pages_and_artifacts_by_instance(
    tmp_path: Path,
) -> None:
    period_start = datetime(2026, 3, 16, tzinfo=UTC)
    period_end = datetime(2026, 3, 23, tzinfo=UTC)

    def write_instance_notes(
        *,
        output_dir: Path,
        instance_label: str,
        topic: str,
    ) -> tuple[Path, Path, Path]:
        item_note = write_markdown_note(
            output_dir=output_dir,
            item_id=41,
            title="Shared Item",
            source="rss",
            canonical_url="https://example.com/shared-item",
            published_at=period_start,
            authors=["Alice"],
            topics=[topic],
            relevance_score=0.91,
            run_id=f"run-{instance_label.lower().replace(' ', '-')}-item",
            summary=f"## Summary\n\n{instance_label} item summary.\n",
        )
        trend_note = write_markdown_trend_note(
            output_dir=output_dir,
            trend_doc_id=501,
            title=f"{instance_label} Weekly",
            granularity="week",
            period_start=period_start,
            period_end=period_end,
            run_id=f"run-{instance_label.lower().replace(' ', '-')}-trend",
            overview_md=(
                "## Overview\n\n"
                f"{instance_label} trend note.\n\n"
                f"See [Shared Item](../Inbox/{item_note.name}).\n"
            ),
            topics=[topic],
            clusters=[],
            highlights=[f"{instance_label} signal."],
        )
        trend_note.with_suffix(".pdf").write_bytes(b"%PDF-1.7\n")

        ideas_dir = output_dir / "Ideas"
        ideas_dir.mkdir(parents=True, exist_ok=True)
        idea_note = ideas_dir / "week--2026-W12--ideas.md"
        idea_note.write_text(
            "---\n"
            "kind: ideas\n"
            "granularity: week\n"
            "period_start: 2026-03-16T00:00:00+00:00\n"
            "period_end: 2026-03-23T00:00:00+00:00\n"
            "status: succeeded\n"
            f"topics:\n  - {topic}\n"
            "---\n\n"
            f"# {instance_label} ideas\n\n"
            "## Summary\n\n"
            f"Derived from [the weekly trend](../Trends/{trend_note.name}) and "
            f"[the shared item](../Inbox/{item_note.name}).\n",
            encoding="utf-8",
        )
        return trend_note, idea_note, item_note

    alpha_root = tmp_path / "alpha"
    beta_root = tmp_path / "beta"
    alpha_trend, alpha_idea, alpha_item = write_instance_notes(
        output_dir=alpha_root,
        instance_label="Alpha Lab",
        topic="agents",
    )
    beta_trend, beta_idea, beta_item = write_instance_notes(
        output_dir=beta_root,
        instance_label="Beta Lab",
        topic="robotics",
    )

    site_dir = tmp_path / "site"
    manifest_path = export_trend_static_site(
        input_dir=[
            TrendSiteInputSpec(path=alpha_root, instance="alpha_lab"),
            TrendSiteInputSpec(path=beta_root, instance="beta_lab"),
        ],
        output_dir=site_dir,
    )

    alpha_trend_page = site_dir / "trends" / f"alpha-lab--{alpha_trend.stem}.html"
    beta_trend_page = site_dir / "trends" / f"beta-lab--{beta_trend.stem}.html"
    alpha_idea_page = site_dir / "ideas" / f"alpha-lab--{alpha_idea.stem}.html"
    beta_idea_page = site_dir / "ideas" / f"beta-lab--{beta_idea.stem}.html"
    alpha_item_page = site_dir / "items" / f"alpha-lab--{alpha_item.stem}.html"
    beta_item_page = site_dir / "items" / f"beta-lab--{beta_item.stem}.html"

    assert alpha_trend_page.exists()
    assert beta_trend_page.exists()
    assert alpha_idea_page.exists()
    assert beta_idea_page.exists()
    assert alpha_item_page.exists()
    assert beta_item_page.exists()

    assert (site_dir / "artifacts" / f"alpha-lab--{alpha_trend.name}").exists()
    assert (site_dir / "artifacts" / f"beta-lab--{beta_trend.name}").exists()
    assert (
        site_dir / "artifacts" / f"alpha-lab--{alpha_trend.with_suffix('.pdf').name}"
    ).exists()
    assert (
        site_dir / "artifacts" / f"beta-lab--{beta_trend.with_suffix('.pdf').name}"
    ).exists()
    assert (site_dir / "artifacts" / "ideas" / f"alpha-lab--{alpha_idea.name}").exists()
    assert (site_dir / "artifacts" / "ideas" / f"beta-lab--{beta_idea.name}").exists()
    assert (site_dir / "artifacts" / "items" / f"alpha-lab--{alpha_item.name}").exists()
    assert (site_dir / "artifacts" / "items" / f"beta-lab--{beta_item.name}").exists()

    alpha_trend_html = alpha_trend_page.read_text(encoding="utf-8")
    beta_idea_html = beta_idea_page.read_text(encoding="utf-8")
    ideas_index_html = (site_dir / "ideas" / "index.html").read_text(encoding="utf-8")
    assert "<div class='meta-panel-label'>Instance</div>" in alpha_trend_html
    assert "<div class='meta-panel-value'>Alpha Lab</div>" in alpha_trend_html
    assert "Beta Lab" in beta_idea_html
    assert "Alpha Lab" not in beta_idea_html
    assert "Alpha Lab" in ideas_index_html
    assert "Beta Lab" in ideas_index_html

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["trends_total"] == 2
    assert manifest["ideas_total"] == 2
    assert manifest["items_total"] == 2
    assert len(set(manifest["files"]["trend_pages"])) == manifest["trends_total"]
    assert len(set(manifest["files"]["idea_pages"])) == manifest["ideas_total"]
    assert len(set(manifest["files"]["item_pages"])) == manifest["items_total"]
    assert manifest["files"]["trend_pages"] == [
        f"trends/alpha-lab--{alpha_trend.stem}.html",
        f"trends/beta-lab--{beta_trend.stem}.html",
    ]
    assert manifest["files"]["idea_pages"] == [
        f"ideas/alpha-lab--{alpha_idea.stem}.html",
        f"ideas/beta-lab--{beta_idea.stem}.html",
    ]
    assert manifest["files"]["item_pages"] == [
        f"items/alpha-lab--{alpha_item.stem}.html",
        f"items/beta-lab--{beta_item.stem}.html",
    ]
    assert [entry["instance"] for entry in manifest["input_dirs"]] == [
        "alpha_lab",
        "beta_lab",
    ]
    assert all("stream" not in entry for entry in manifest["input_dirs"])


def test_export_trend_static_site_keeps_duplicate_root_instances_separate(
    tmp_path: Path,
) -> None:
    notes_root = tmp_path / "notes"
    item_note = write_markdown_note(
        output_dir=notes_root,
        item_id=91,
        title="Shared Root Item",
        source="rss",
        canonical_url="https://example.com/shared-root-item",
        published_at=datetime(2026, 3, 18, tzinfo=UTC),
        authors=["Alice"],
        topics=["agents"],
        relevance_score=0.88,
        run_id="run-shared-root-item",
        summary="## Summary\n\nShared-root item note.\n",
    )
    trend_note = write_markdown_trend_note(
        output_dir=notes_root,
        trend_doc_id=811,
        title="Shared Root Trend",
        granularity="day",
        period_start=datetime(2026, 3, 18, tzinfo=UTC),
        period_end=datetime(2026, 3, 19, tzinfo=UTC),
        run_id="run-shared-root-trend",
        overview_md=(
            f"## Overview\n\nSee [Shared Root Item](../Inbox/{item_note.name}).\n"
        ),
        topics=["agents"],
        clusters=[],
        highlights=[],
    )
    ideas_dir = notes_root / "Ideas"
    ideas_dir.mkdir(parents=True, exist_ok=True)
    idea_note = ideas_dir / "day--2026-03-18--ideas.md"
    idea_note.write_text(
        "---\n"
        "kind: ideas\n"
        "granularity: day\n"
        "period_start: 2026-03-18T00:00:00+00:00\n"
        "period_end: 2026-03-19T00:00:00+00:00\n"
        "status: succeeded\n"
        "---\n\n"
        "# Shared root ideas\n\n"
        "## Summary\n\n"
        f"See [the shared trend](../Trends/{trend_note.name}) and "
        f"[the shared item](../Inbox/{item_note.name}).\n",
        encoding="utf-8",
    )

    site_dir = tmp_path / "site"
    manifest_path = export_trend_static_site(
        input_dir=[
            TrendSiteInputSpec(path=notes_root, instance="alpha"),
            TrendSiteInputSpec(path=notes_root, instance="beta"),
        ],
        output_dir=site_dir,
    )

    alpha_trend_page = site_dir / "trends" / f"alpha--{trend_note.stem}.html"
    beta_trend_page = site_dir / "trends" / f"beta--{trend_note.stem}.html"
    alpha_idea_page = site_dir / "ideas" / f"alpha--{idea_note.stem}.html"
    beta_idea_page = site_dir / "ideas" / f"beta--{idea_note.stem}.html"
    alpha_item_page = site_dir / "items" / f"alpha--{item_note.stem}.html"
    beta_item_page = site_dir / "items" / f"beta--{item_note.stem}.html"

    assert alpha_trend_page.exists()
    assert beta_trend_page.exists()
    assert alpha_idea_page.exists()
    assert beta_idea_page.exists()
    assert alpha_item_page.exists()
    assert beta_item_page.exists()

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["trends_total"] == 2
    assert manifest["ideas_total"] == 2
    assert manifest["items_total"] == 2
    assert len(set(manifest["files"]["trend_pages"])) == 2
    assert len(set(manifest["files"]["idea_pages"])) == 2
    assert len(set(manifest["files"]["item_pages"])) == 2

    beta_trend_html = beta_trend_page.read_text(encoding="utf-8")
    beta_idea_html = beta_idea_page.read_text(encoding="utf-8")
    assert f"../items/beta--{item_note.stem}.html" in beta_trend_html
    assert f"../items/alpha--{item_note.stem}.html" not in beta_trend_html
    assert f"../items/beta--{item_note.stem}.html" in beta_idea_html
    assert f"../trends/beta--{trend_note.stem}.html" in beta_idea_html
    assert f"../items/alpha--{item_note.stem}.html" not in beta_idea_html


def test_export_trend_static_site_preserves_grouped_child_identities_under_explicit_parent_instance(
    tmp_path: Path,
) -> None:
    notes_root = tmp_path / "notes"
    agents_root = notes_root / "Streams" / "agents_lab"
    research_root = notes_root / "Streams" / "research_ops"
    period_start = datetime(2026, 3, 21, tzinfo=UTC)
    period_end = datetime(2026, 3, 22, tzinfo=UTC)

    def write_grouped_child_notes(
        *,
        output_dir: Path,
        label: str,
    ) -> tuple[Path, Path, Path]:
        item_note = write_markdown_note(
            output_dir=output_dir,
            item_id=101,
            title="Grouped Root Item",
            source="rss",
            canonical_url="https://example.com/grouped-root-item",
            published_at=period_start,
            authors=["Alice"],
            topics=["agents"],
            relevance_score=0.9,
            run_id=f"run-{label.lower()}-item",
            summary=f"## Summary\n\n{label} grouped-root item summary.\n",
        )
        trend_note = write_markdown_trend_note(
            output_dir=output_dir,
            trend_doc_id=601,
            title=f"{label} grouped-root trend",
            granularity="day",
            period_start=period_start,
            period_end=period_end,
            run_id=f"run-{label.lower()}-trend",
            overview_md=(
                f"## Overview\n\nSee [the grouped item](../Inbox/{item_note.name}).\n"
            ),
            topics=["agents"],
            clusters=[],
            highlights=[f"{label} grouped highlight."],
        )
        trend_note.with_suffix(".pdf").write_bytes(b"%PDF-1.7\n")

        ideas_dir = output_dir / "Ideas"
        ideas_dir.mkdir(parents=True, exist_ok=True)
        idea_note = ideas_dir / "day--2026-03-21--ideas.md"
        idea_note.write_text(
            "---\n"
            "kind: ideas\n"
            "granularity: day\n"
            "period_start: 2026-03-21T00:00:00+00:00\n"
            "period_end: 2026-03-22T00:00:00+00:00\n"
            "status: succeeded\n"
            "---\n\n"
            f"# {label} grouped-root ideas\n\n"
            "## Summary\n\n"
            f"See [the grouped trend](../Trends/{trend_note.name}) and "
            f"[the grouped item](../Inbox/{item_note.name}).\n",
            encoding="utf-8",
        )
        return trend_note, idea_note, item_note

    agents_trend, agents_idea, agents_item = write_grouped_child_notes(
        output_dir=agents_root,
        label="Agents",
    )
    research_trend, research_idea, research_item = write_grouped_child_notes(
        output_dir=research_root,
        label="Research",
    )

    site_dir = tmp_path / "site"
    with pytest.raises(ValueError, match="legacy Streams layouts"):
        export_trend_static_site(
            input_dir=TrendSiteInputSpec(path=notes_root, instance="alpha"),
            output_dir=site_dir,
        )


def test_export_trend_static_site_preserves_explicit_default_instance_name(
    tmp_path: Path,
) -> None:
    notes_root = tmp_path / "notes"
    trend_note = write_markdown_trend_note(
        output_dir=notes_root,
        trend_doc_id=711,
        title="Default Instance Weekly",
        granularity="day",
        period_start=datetime(2026, 3, 20, tzinfo=UTC),
        period_end=datetime(2026, 3, 21, tzinfo=UTC),
        run_id="run-default-instance-trend",
        overview_md="## Overview\n\nDefault-named fleet child.\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
    )
    ideas_dir = notes_root / "Ideas"
    ideas_dir.mkdir(parents=True, exist_ok=True)
    idea_note = ideas_dir / "day--2026-03-20--ideas.md"
    idea_note.write_text(
        "---\n"
        "kind: ideas\n"
        "granularity: day\n"
        "period_start: 2026-03-20T00:00:00+00:00\n"
        "period_end: 2026-03-21T00:00:00+00:00\n"
        "status: succeeded\n"
        "---\n\n"
        "# Default instance ideas\n\n"
        "## Summary\n\n"
        "Default-named child should still namespace pages.\n",
        encoding="utf-8",
    )

    site_dir = tmp_path / "site"
    manifest_path = export_trend_static_site(
        input_dir=TrendSiteInputSpec(path=notes_root, instance="default"),
        output_dir=site_dir,
    )

    trend_page = site_dir / "trends" / f"default--{trend_note.stem}.html"
    idea_page = site_dir / "ideas" / f"default--{idea_note.stem}.html"
    assert trend_page.exists()
    assert idea_page.exists()

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["input_dirs"][0]["instance"] == "default"
    assert f"trends/default--{trend_note.stem}.html" in manifest["files"]["trend_pages"]
    assert f"ideas/default--{idea_note.stem}.html" in manifest["files"]["idea_pages"]

    trend_html = trend_page.read_text(encoding="utf-8")
    idea_html = idea_page.read_text(encoding="utf-8")
    assert "<div class='meta-panel-value'>Default</div>" in trend_html
    assert "<div class='meta-panel-value'>Default</div>" in idea_html


def test_export_trend_static_site_rejects_slug_colliding_instance_names(
    tmp_path: Path,
) -> None:
    alpha_root = tmp_path / "agents-lab-spaced"
    beta_root = tmp_path / "agents-lab-slug"
    period_start = datetime(2026, 3, 24, tzinfo=UTC)
    period_end = datetime(2026, 3, 25, tzinfo=UTC)

    for output_dir, label in (
        (alpha_root, "Agents Lab"),
        (beta_root, "agents-lab"),
    ):
        trend_note = write_markdown_trend_note(
            output_dir=output_dir,
            trend_doc_id=901,
            title=f"{label} daily",
            granularity="day",
            period_start=period_start,
            period_end=period_end,
            run_id=f"run-{label.lower().replace(' ', '-')}-trend",
            overview_md="## Overview\n\nSlug-colliding instance names.\n",
            topics=["agents"],
            clusters=[],
            highlights=[],
        )
        trend_note.with_suffix(".pdf").write_bytes(b"%PDF-1.7\n")

    with pytest.raises(ValueError, match="agents-lab"):
        export_trend_static_site(
            input_dir=[
                TrendSiteInputSpec(path=alpha_root, instance="Agents Lab"),
                TrendSiteInputSpec(path=beta_root, instance="agents-lab"),
            ],
            output_dir=tmp_path / "site",
        )


def test_stage_trend_site_source_rejects_legacy_topic_stream_directory_layout(
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

    _ = write_markdown_trend_note(
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
    with pytest.raises(ValueError, match="legacy Streams layouts"):
        stage_trend_site_source(
            input_dir=notes_root,
            output_dir=staged_root,
        )


def test_stage_trend_site_source_rejects_mixed_legacy_stream_layouts(
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
    with pytest.raises(ValueError, match="legacy Streams layouts"):
        stage_trend_site_source(
            input_dir=notes_root,
            output_dir=staged_root,
        )


def test_stage_trend_site_source_round_trips_explicit_default_instance_without_overwriting_root_pages(
    tmp_path: Path,
) -> None:
    legacy_root = tmp_path / "legacy-notes"
    default_root = tmp_path / "default-notes"

    legacy_note = write_markdown_trend_note(
        output_dir=legacy_root,
        trend_doc_id=1,
        title="Legacy Daily",
        granularity="day",
        period_start=datetime(2026, 3, 20, tzinfo=UTC),
        period_end=datetime(2026, 3, 21, tzinfo=UTC),
        run_id="run-legacy-default-roundtrip",
        overview_md="## Overview\n\nLegacy root daily note.\n",
        topics=["agents"],
        clusters=[],
        highlights=["Legacy page must stay at the root namespace."],
    )
    default_note = write_markdown_trend_note(
        output_dir=default_root,
        trend_doc_id=1,
        title="Default Daily",
        granularity="day",
        period_start=datetime(2026, 3, 20, tzinfo=UTC),
        period_end=datetime(2026, 3, 21, tzinfo=UTC),
        run_id="run-explicit-default-roundtrip",
        overview_md="## Overview\n\nExplicit default instance note.\n",
        topics=["agents"],
        clusters=[],
        highlights=["Default instance must keep its own namespace."],
    )

    staged_root = tmp_path / "site-content"
    manifest_path = stage_trend_site_source(
        input_dir=[
            legacy_root,
            TrendSiteInputSpec(path=default_root, instance="default"),
        ],
        output_dir=staged_root,
    )

    assert manifest_path == staged_root / "manifest.json"
    assert (staged_root / "Trends" / legacy_note.name).exists()
    assert (staged_root / "Streams" / "default" / "Trends" / default_note.name).exists()

    site_dir = tmp_path / "site"
    built_manifest_path = export_trend_static_site(
        input_dir=staged_root,
        output_dir=site_dir,
    )

    legacy_page = site_dir / "trends" / f"{legacy_note.stem}.html"
    default_page = site_dir / "trends" / f"default--{default_note.stem}.html"
    assert legacy_page.exists()
    assert default_page.exists()

    built_manifest = json.loads(built_manifest_path.read_text(encoding="utf-8"))
    assert built_manifest["trends_total"] == 2
    assert len(set(built_manifest["files"]["trend_pages"])) == 2
    assert f"trends/{legacy_note.stem}.html" in built_manifest["files"]["trend_pages"]
    assert (
        f"trends/default--{default_note.stem}.html"
        in built_manifest["files"]["trend_pages"]
    )

    legacy_html = legacy_page.read_text(encoding="utf-8")
    default_html = default_page.read_text(encoding="utf-8")
    assert "<title>Legacy Daily" in legacy_html
    assert "<title>Default Daily" not in legacy_html
    assert "<title>Default Daily" in default_html
    assert "<title>Legacy Daily" not in default_html


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
    assert manifest["item_export_scope"] == "linked"
    assert manifest["items_total"] == 1
    assert manifest["items_available_total"] == 1
    assert manifest["items_unreferenced_total"] == 0
    assert f"Inbox/{item_note.name}" in manifest["files"]["items_markdown"]


def test_stage_trend_site_source_skips_unreferenced_item_notes_by_default(
    tmp_path: Path,
) -> None:
    notes_root = tmp_path / "notes"
    linked_item = write_markdown_note(
        output_dir=notes_root,
        item_id=68,
        title="Linked stage item",
        source="rss",
        canonical_url="https://example.com/linked-stage-item",
        published_at=datetime(2026, 3, 11, tzinfo=UTC),
        authors=["Alice"],
        topics=["agents"],
        relevance_score=0.93,
        run_id="run-stage-linked-item",
        summary="## Summary\n\nThis staged note is referenced.\n",
    )
    unlinked_item = write_markdown_note(
        output_dir=notes_root,
        item_id=69,
        title="Unlinked stage item",
        source="rss",
        canonical_url="https://example.com/unlinked-stage-item",
        published_at=datetime(2026, 3, 11, tzinfo=UTC),
        authors=["Bob"],
        topics=["agents"],
        relevance_score=0.22,
        run_id="run-stage-unlinked-item",
        summary="## Summary\n\nThis staged note should be skipped.\n",
    )
    trend_note = write_markdown_trend_note(
        output_dir=notes_root,
        trend_doc_id=114,
        title="Agent Systems",
        granularity="day",
        period_start=datetime(2026, 3, 11, tzinfo=UTC),
        period_end=datetime(2026, 3, 12, tzinfo=UTC),
        run_id="run-stage-items-filtered",
        overview_md=f"## Overview\n\nSee [Linked stage item](../Inbox/{linked_item.name}).\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
    )

    staged_trends_dir = tmp_path / "site-content" / "Trends"
    manifest_path = stage_trend_site_source(
        input_dir=notes_root / "Trends",
        output_dir=staged_trends_dir,
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["item_export_scope"] == "linked"
    assert manifest["items_total"] == 1
    assert manifest["items_available_total"] == 2
    assert manifest["items_unreferenced_total"] == 1
    assert (staged_trends_dir / trend_note.name).exists()
    assert (staged_trends_dir.parent / "Inbox" / linked_item.name).exists()
    assert not (staged_trends_dir.parent / "Inbox" / unlinked_item.name).exists()
    assert f"Inbox/{linked_item.name}" in manifest["files"]["items_markdown"]
    assert f"Inbox/{unlinked_item.name}" not in manifest["files"]["items_markdown"]


def test_stage_trend_site_source_item_export_scope_all_preserves_full_staging(
    tmp_path: Path,
) -> None:
    notes_root = tmp_path / "notes"
    linked_item = write_markdown_note(
        output_dir=notes_root,
        item_id=70,
        title="Linked stage item",
        source="rss",
        canonical_url="https://example.com/linked-stage-item-all",
        published_at=datetime(2026, 3, 12, tzinfo=UTC),
        authors=["Alice"],
        topics=["agents"],
        relevance_score=0.93,
        run_id="run-stage-linked-item-all",
        summary="## Summary\n\nThis staged note is referenced.\n",
    )
    unlinked_item = write_markdown_note(
        output_dir=notes_root,
        item_id=71,
        title="Unlinked stage item",
        source="rss",
        canonical_url="https://example.com/unlinked-stage-item-all",
        published_at=datetime(2026, 3, 12, tzinfo=UTC),
        authors=["Bob"],
        topics=["agents"],
        relevance_score=0.22,
        run_id="run-stage-unlinked-item-all",
        summary="## Summary\n\nCompatibility mode should still stage this note.\n",
    )
    _ = write_markdown_trend_note(
        output_dir=notes_root,
        trend_doc_id=115,
        title="Agent Systems",
        granularity="day",
        period_start=datetime(2026, 3, 12, tzinfo=UTC),
        period_end=datetime(2026, 3, 13, tzinfo=UTC),
        run_id="run-stage-items-all",
        overview_md=f"## Overview\n\nSee [Linked stage item](../Inbox/{linked_item.name}).\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
    )

    staged_trends_dir = tmp_path / "site-content" / "Trends"
    manifest_path = stage_trend_site_source(
        input_dir=notes_root / "Trends",
        output_dir=staged_trends_dir,
        item_export_scope="all",
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["item_export_scope"] == "all"
    assert manifest["items_total"] == 2
    assert manifest["items_available_total"] == 2
    assert manifest["items_unreferenced_total"] == 0
    assert (staged_trends_dir.parent / "Inbox" / linked_item.name).exists()
    assert (staged_trends_dir.parent / "Inbox" / unlinked_item.name).exists()


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
