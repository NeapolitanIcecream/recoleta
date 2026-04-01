from __future__ import annotations

from datetime import UTC, datetime, timedelta
import json

from recoleta.presentation import presentation_sidecar_path, validate_presentation_v1
from recoleta.publish import write_markdown_trend_note


def test_publish_trend_note_skips_missing_representative_fields(
    tmp_path,
) -> None:
    period_start = datetime(2026, 3, 2, tzinfo=UTC)
    period_end = period_start + timedelta(days=1)

    note_path = write_markdown_trend_note(
        output_dir=tmp_path,
        trend_doc_id=1,
        title="Daily Trend",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        run_id="run-test",
        overview_md="- overview",
        topics=["agents"],
        clusters=[
            {
                "name": "cluster-a",
                "description": "desc",
                "representative_chunks": [
                    {},
                    {"doc_id": None, "chunk_index": None, "score": None},
                    {"doc_id": 1, "chunk_index": 0, "score": 0.9},
                ],
            }
        ],
        highlights=["h"],
    )

    text = note_path.read_text(encoding="utf-8")
    assert "doc_id=None" not in text
    assert "chunk_index=None" not in text


def test_publish_trend_note_normalizes_overview_headings_and_top_n(
    tmp_path,
) -> None:
    """Regression: trend notes should strip duplicate overview headings and align Top-N labels."""

    period_start = datetime(2026, 3, 9, tzinfo=UTC)
    period_end = period_start + timedelta(days=1)

    note_path = write_markdown_trend_note(
        output_dir=tmp_path,
        trend_doc_id=2,
        title="Daily Trend",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        run_id="run-test",
        overview_md=(
            "## 日度概览\n\n"
            "今天有两篇值得关注的论文。\n\n"
            "## Top 10 must-read\n"
            "1. **[Paper A](https://example.com/a)** — 原因。"
            "代表片段：`[Paper A](https://example.com/a)`。\n"
            "   - 参考：[Paper A](https://example.com/a)\n"
            "2. **[Paper B](https://example.com/b)** — Reason. "
            "Representative snippet: `[Paper B](https://example.com/b)`.\n"
        ),
        topics=["agents"],
        clusters=[],
        highlights=["h"],
    )

    text = note_path.read_text(encoding="utf-8")
    assert text.count("## Overview") == 1
    assert "## 日度概览" not in text
    assert "## Top-2 必读" in text
    assert "代表片段" not in text
    assert "Representative snippet" not in text
    assert "- 参考：" not in text


def test_publish_trend_note_strips_multiline_representative_snippets(
    tmp_path,
) -> None:
    """Regression: strip representative-snippet lines that appear below list items."""

    period_start = datetime(2026, 3, 10, tzinfo=UTC)
    period_end = period_start + timedelta(days=1)

    note_path = write_markdown_trend_note(
        output_dir=tmp_path,
        trend_doc_id=3,
        title="Daily Trend",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        run_id="run-test",
        overview_md=(
            "## Top 10 must-read\n"
            "1. **[Paper A](https://example.com/a)**\n"
            "   代表片段：。看点是把工具编排变成可学习决策。\n"
            "2. **[Paper B](https://example.com/b)**\n"
            "   Representative snippet: It closes the loop.\n"
        ),
        topics=["agents"],
        clusters=[],
        highlights=["h"],
    )

    text = note_path.read_text(encoding="utf-8")
    assert "## Top-2 必读" in text
    assert "代表片段" not in text
    assert "Representative snippet" not in text


def test_publish_trend_note_strips_duplicate_trailing_links(
    tmp_path,
) -> None:
    """Regression: ordered Top-N items should not repeat the same link twice."""

    period_start = datetime(2026, 3, 10, tzinfo=UTC)
    period_end = period_start + timedelta(days=1)

    note_path = write_markdown_trend_note(
        output_dir=tmp_path,
        trend_doc_id=4,
        title="Daily Trend",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        run_id="run-test",
        overview_md=(
            "## Top 10 must-read\n"
            "1. [Paper A](https://example.com/a) — Summary. "
            "([Paper A short](https://example.com/a))\n"
            "2. [Paper B](https://example.com/b) — 摘要。"
            "（[Paper B short](https://example.com/b)）\n"
        ),
        topics=["agents"],
        clusters=[],
        highlights=["h"],
    )

    text = note_path.read_text(encoding="utf-8")
    assert text.count("https://example.com/a") == 1
    assert text.count("https://example.com/b") == 1


def test_publish_trend_note_prefers_item_note_links_over_source_urls(
    tmp_path,
) -> None:
    period_start = datetime(2026, 3, 11, tzinfo=UTC)
    period_end = period_start + timedelta(days=1)

    note_path = write_markdown_trend_note(
        output_dir=tmp_path,
        trend_doc_id=5,
        title="Daily Trend",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        run_id="run-test",
        overview_md="- overview",
        topics=["agents"],
        clusters=[
            {
                "name": "cluster-a",
                "description": "desc",
                "representative_chunks": [
                    {
                        "doc_id": 1,
                        "chunk_index": 0,
                        "title": "Paper A",
                        "url": "https://example.com/a",
                        "note_href": "../Inbox/2026-03-11--paper-a.md",
                    }
                ],
            }
        ],
        highlights=["h"],
    )

    text = note_path.read_text(encoding="utf-8")
    assert "- [Paper A](../Inbox/2026-03-11--paper-a.md)" in text
    assert "- [Paper A](https://example.com/a)" not in text


def test_publish_trend_note_renders_evolution_section(tmp_path) -> None:
    period_start = datetime(2026, 3, 12, tzinfo=UTC)
    period_end = period_start + timedelta(days=7)

    note_path = write_markdown_trend_note(
        output_dir=tmp_path,
        trend_doc_id=6,
        title="Weekly Trend",
        granularity="week",
        period_start=period_start,
        period_end=period_end,
        run_id="run-test",
        overview_md="- overview",
        topics=["agents"],
        clusters=[],
        highlights=[],
        evolution={
            "summary_md": "Agent workflows are stabilizing rather than just expanding.",
            "signals": [
                {
                    "theme": "Tool-using agents",
                    "change_type": "continuing",
                    "summary": "The theme remains central, but the discussion is shifting toward operational discipline.",
                    "history_windows": ["prev_1", "prev_2"],
                }
            ],
        },
    )

    text = note_path.read_text(encoding="utf-8")
    assert "## Evolution" in text
    assert "### Tool-using agents" in text
    assert "- Change: Continuing" in text
    assert "- History windows: prev_1, prev_2" in text


def test_publish_trend_note_localizes_evolution_labels_and_links_history_windows(
    tmp_path,
) -> None:
    period_start = datetime(2026, 3, 12, tzinfo=UTC)
    period_end = period_start + timedelta(days=7)

    note_path = write_markdown_trend_note(
        output_dir=tmp_path,
        trend_doc_id=7,
        title="Weekly Trend",
        granularity="week",
        period_start=period_start,
        period_end=period_end,
        run_id="run-test",
        overview_md="- overview",
        topics=["agents"],
        clusters=[],
        highlights=[],
        evolution={
            "summary_md": "相比 prev_1，今天更强调可运行环境与验证闭环。",
            "signals": [
                {
                    "theme": "Tool-using agents",
                    "change_type": "continuing",
                    "summary": "相比 prev_1，RepoLaunch reports a roughly 70% build success rate.",
                    "history_windows": ["prev_1"],
                }
            ],
        },
        history_window_refs={
            "prev_1": {
                "window_id": "prev_1",
                "label": "2026-W10",
                "title": "Previous Weekly Trend: Verification Gets Tighter",
                "granularity": "week",
                "period_start": "2026-03-02T00:00:00+00:00",
                "trend_doc_id": 5,
            }
        },
        output_language="Chinese (Simplified)",
    )

    text = note_path.read_text(encoding="utf-8")
    assert "- 变化：延续" in text
    assert (
        "相比 [Previous Weekly Trend (2026-W10)](week--2026-W10--trend--5.md)，今天更强调可运行环境与验证闭环。"
        in text
    )
    assert (
        "相比 [Previous Weekly Trend (2026-W10)](week--2026-W10--trend--5.md)，RepoLaunch reports a roughly 70% build success rate."
        in text
    )
    assert (
        "- 历史窗口：[Previous Weekly Trend (2026-W10)](week--2026-W10--trend--5.md)"
        in text
    )


def test_publish_trend_note_deduplicates_history_window_title_after_link(
    tmp_path,
) -> None:
    """Regression: history window links should not be followed by the same raw title."""

    period_start = datetime(2026, 3, 12, tzinfo=UTC)
    period_end = period_start + timedelta(days=1)

    note_path = write_markdown_trend_note(
        output_dir=tmp_path,
        trend_doc_id=8,
        title="Daily Trend",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        run_id="run-test",
        overview_md="- overview",
        topics=["agents"],
        clusters=[],
        highlights=[],
        evolution={
            "summary_md": (
                "延续了 prev_1《机器人具身智能转向轻量适配、长时序增强与部署一致性》的主线，"
                "但更强调部署一致性。"
            ),
            "signals": [
                {
                    "theme": "具身部署",
                    "change_type": "continuing",
                    "summary": (
                        "相比 prev_1《机器人具身智能转向轻量适配、长时序增强与部署一致性》，"
                        "这次把量化与长时序控制放在同一条工程链路里。"
                    ),
                    "history_windows": ["prev_1"],
                }
            ],
        },
        history_window_refs={
            "prev_1": {
                "window_id": "prev_1",
                "label": "2026-03-08",
                "title": "机器人具身智能转向轻量适配、长时序增强与部署一致性",
                "granularity": "day",
                "period_start": "2026-03-08T00:00:00+00:00",
                "trend_doc_id": 69,
            }
        },
        output_language="Chinese (Simplified)",
    )

    text = note_path.read_text(encoding="utf-8")
    assert (
        "[机器人具身智能转向轻量适配、长时序增强与部署一致性 (2026-03-08)]"
        "(day--2026-03-08--trend--69.md)"
        in text
    )
    assert "](day--2026-03-08--trend--69.md)《机器人具身智能转向轻量适配、长时序增强与部署一致性》" not in text


def test_publish_trend_note_emits_presentation_sidecar_with_rendered_history_refs(
    tmp_path,
) -> None:
    period_start = datetime(2026, 3, 12, tzinfo=UTC)
    period_end = period_start + timedelta(days=7)

    note_path = write_markdown_trend_note(
        output_dir=tmp_path,
        trend_doc_id=9,
        title="Weekly Trend",
        granularity="week",
        period_start=period_start,
        period_end=period_end,
        run_id="run-test",
        overview_md="This week shifted from prev_1 toward evaluation discipline.",
        topics=["agents"],
        clusters=[
            {
                "name": "Verification loops",
                "description": "Teams are using tighter release controls.",
                "representative_chunks": [
                    {
                        "doc_id": 1,
                        "chunk_index": 0,
                        "title": "CodeScout",
                        "url": "https://example.com/codescout",
                    }
                ],
            }
        ],
        highlights=[],
        evolution={
            "summary_md": "Compared with prev_1, the conversation is more operational.",
            "signals": [
                {
                    "theme": "Verification loops",
                    "change_type": "continuing",
                    "summary": "Compared with prev_1, teams now quantify release risk.",
                    "history_windows": ["prev_1"],
                },
                {
                    "theme": "Operator lanes",
                    "change_type": "emerging",
                    "summary": "Review queues are moving into the main workflow.",
                    "history_windows": [],
                },
            ],
        },
        history_window_refs={
            "prev_1": {
                "window_id": "prev_1",
                "label": "2026-W10",
                "title": "Verification Gets Tighter",
                "granularity": "week",
                "period_start": "2026-03-02T00:00:00+00:00",
                "trend_doc_id": 7,
            }
        },
    )

    sidecar_path = presentation_sidecar_path(note_path=note_path)
    sidecar = json.loads(sidecar_path.read_text(encoding="utf-8"))

    assert sidecar_path.exists()
    assert sidecar["presentation_schema_version"] == 1
    assert sidecar["surface_kind"] == "trend"
    assert sidecar["source_markdown_path"] == f"Trends/{note_path.name}"
    assert sidecar["content"]["hero"]["kicker"] == "Trend brief"
    assert sidecar["content"]["ranked_shifts"][0]["history_refs"] == ["prev_1"]
    assert "prev_1" not in sidecar["content"]["overview"]
    assert "Verification Gets Tighter" in sidecar["content"]["overview"]
    assert sidecar["content"]["representative_sources"][0]["title"] == "CodeScout"
    assert validate_presentation_v1(sidecar) == []


def test_publish_trend_note_sidecar_matches_sanitized_markdown_surface(tmp_path) -> None:
    period_start = datetime(2026, 3, 12, tzinfo=UTC)
    period_end = period_start + timedelta(days=7)

    note_path = write_markdown_trend_note(
        output_dir=tmp_path,
        trend_doc_id=10,
        title="2026-03-12 Daily Trend: Verification gets operational",
        granularity="week",
        period_start=period_start,
        period_end=period_end,
        run_id="run-test",
        overview_md="## Overview\n\nTeams are tightening release discipline.\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
    )

    note_text = note_path.read_text(encoding="utf-8")
    sidecar = json.loads(
        presentation_sidecar_path(note_path=note_path).read_text(encoding="utf-8")
    )

    assert "# Verification gets operational" in note_text
    assert note_text.count("## Overview") == 1
    assert sidecar["content"]["title"] == "Verification gets operational"
    assert sidecar["content"]["overview"] == "Teams are tightening release discipline."


def test_publish_trend_note_infers_sidecar_language_code_from_output_language(tmp_path) -> None:
    period_start = datetime(2026, 3, 12, tzinfo=UTC)
    period_end = period_start + timedelta(days=7)

    note_path = write_markdown_trend_note(
        output_dir=tmp_path,
        trend_doc_id=11,
        title="周趋势",
        granularity="week",
        period_start=period_start,
        period_end=period_end,
        run_id="run-test",
        overview_md="团队开始把验证闭环前置到发布流程里。",
        topics=["agents"],
        clusters=[],
        highlights=[],
        output_language="Chinese (Simplified)",
    )

    note_text = note_path.read_text(encoding="utf-8")
    sidecar = json.loads(
        presentation_sidecar_path(note_path=note_path).read_text(encoding="utf-8")
    )

    assert "language_code: zh-CN" in note_text
    assert sidecar["language_code"] == "zh-CN"
