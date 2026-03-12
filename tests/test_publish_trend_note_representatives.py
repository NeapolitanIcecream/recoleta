from __future__ import annotations

from datetime import UTC, datetime, timedelta

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
