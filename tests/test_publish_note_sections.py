from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from recoleta.publish import (
    build_telegram_message,
    write_markdown_note,
    write_obsidian_note,
)


_STRUCTURED_SUMMARY = (
    "## Summary\n"
    "Short summary.\n\n"
    "## Problem\n"
    "- Hard setup.\n\n"
    "## Approach\n"
    "- Use a structured agent.\n\n"
    "## Results\n"
    "- +12% on eval.\n"
)


def test_notes_render_fixed_sections_and_single_link(tmp_path: Path) -> None:
    md_path = write_markdown_note(
        output_dir=tmp_path,
        item_id=1,
        title="Title",
        source="arxiv",
        canonical_url="https://example.com",
        published_at=datetime(2026, 1, 1, tzinfo=UTC),
        authors=["Alice"],
        topics=["tool-use-agents"],
        relevance_score=0.9,
        run_id="run-1",
        summary=_STRUCTURED_SUMMARY,
    )
    md = md_path.read_text(encoding="utf-8")
    assert "## Summary" in md
    assert "## Problem" in md
    assert "## Approach" in md
    assert "## Results" in md
    assert "## Link" in md
    assert "## Links" not in md

    vault_path = tmp_path / "vault"
    obs_path = write_obsidian_note(
        vault_path=vault_path,
        base_folder="Recoleta",
        item_id=1,
        title="Title",
        source="arxiv",
        canonical_url="https://example.com",
        published_at=datetime(2026, 1, 1, tzinfo=UTC),
        authors=["Alice"],
        topics=["tool-use-agents"],
        relevance_score=0.9,
        run_id="run-1",
        summary=_STRUCTURED_SUMMARY,
    )
    obs = obs_path.read_text(encoding="utf-8")
    assert "## Summary" in obs
    assert "## Problem" in obs
    assert "## Approach" in obs
    assert "## Results" in obs
    assert "## Link" in obs
    assert "## Links" not in obs


def test_notes_normalize_legacy_tldr_style_summary(tmp_path: Path) -> None:
    md_path = write_markdown_note(
        output_dir=tmp_path,
        item_id=1,
        title="Legacy Title",
        source="arxiv",
        canonical_url="https://example.com",
        published_at=datetime(2026, 1, 1, tzinfo=UTC),
        authors=["Alice"],
        topics=["tool-use-agents"],
        relevance_score=0.9,
        run_id="run-legacy",
        summary=(
            "- TL;DR: Short summary.\n"
            "- Problem: Hard setup.\n"
            "- Approach: Use a structured agent.\n"
            "- Results: +12% on eval.\n"
        ),
    )
    md = md_path.read_text(encoding="utf-8")
    assert "## Summary" in md
    assert "## Problem" in md
    assert "## Approach" in md
    assert "## Results" in md
    assert "TL;DR" not in md


def test_telegram_message_renders_structured_sections_without_outer_summary_wrapper() -> None:
    msg = build_telegram_message(
        title="T",
        summary=_STRUCTURED_SUMMARY,
        url="https://example.com",
    )
    assert "T" in msg
    assert "<b>Summary</b>" in msg
    assert "<b>Problem</b>" in msg
    assert "<b>Approach</b>" in msg
    assert "<b>Results</b>" in msg
    assert "<b>Summary:</b>" not in msg
    assert "<b>Link</b>" in msg
    assert "<b>Link:</b>" not in msg


def test_telegram_message_uses_html_and_escapes() -> None:
    msg = build_telegram_message(
        title='T & <x> "q"',
        summary="## Summary\nS <b>bad</b> & more\n",
        url="https://example.com/path?a=1&b=2",
    )
    assert msg.startswith("<b>")
    assert "<b>T &amp; &lt;x&gt; &quot;q&quot;</b>" in msg
    assert "<b>Summary</b>" in msg
    assert "&lt;b&gt;bad&lt;/b&gt;" in msg
    assert "<b>Link</b>" in msg
    assert 'href="https://example.com/path?a=1&amp;b=2"' in msg
    assert ">example.com<" in msg


def test_telegram_message_truncates_long_summary() -> None:
    msg = build_telegram_message(
        title="T",
        summary="## Summary\n" + ("a" * 10_000),
        url="https://example.com",
    )
    assert len(msg) <= 4096
    assert "…" in msg


def test_telegram_message_normalizes_markdownish_summary() -> None:
    msg = build_telegram_message(
        title="T",
        summary=(
            "## Summary\n"
            "### Section\n"
            "- item 1\n"
            "* item 2\n"
            "This is *italic* and **bold** and `code`.\n"
            "[link](https://example.com/x?a=1&b=2)\n"
        ),
        url="https://example.com",
    )
    assert "###" not in msg
    assert "- item" not in msg
    assert "*italic*" not in msg
    assert "**bold**" not in msg
    assert "<b>Section</b>" in msg
    assert "\n• item 1" in msg
    assert "\n• item 2" in msg
    assert "<i>italic</i>" in msg
    assert "<b>bold</b>" in msg
    assert "<code>code</code>" in msg
    assert 'href="https://example.com/x?a=1&amp;b=2"' in msg


def test_telegram_message_does_not_emphasize_inside_link_href() -> None:
    msg = build_telegram_message(
        title="T",
        summary="[x](https://example.com/_foo_)",
        url="https://example.com",
    )
    assert 'href="https://example.com/_foo_"' in msg
    assert "<i>" not in msg


def test_telegram_message_rejects_non_http_links_in_summary() -> None:
    msg = build_telegram_message(
        title="T",
        summary="[x](javascript:alert(1))",
        url="https://example.com",
    )
    assert 'href="javascript:alert(1)"' not in msg
