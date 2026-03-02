from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from recoleta.publish import (
    build_telegram_message,
    write_markdown_note,
    write_obsidian_note,
)


def test_notes_include_only_summary_and_links(tmp_path: Path) -> None:
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
        summary="S",
    )
    md = md_path.read_text(encoding="utf-8")
    assert "## Summary" in md
    assert "## Links" in md
    assert "## Insight" not in md
    assert "## Ideas" not in md

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
        summary="S",
    )
    obs = obs_path.read_text(encoding="utf-8")
    assert "## Summary" in obs
    assert "## Links" in obs
    assert "## Insight" not in obs
    assert "## Ideas" not in obs


def test_telegram_message_includes_title_summary_and_link() -> None:
    msg = build_telegram_message(title="T", summary="S", url="https://example.com")
    assert "T" in msg
    assert "Summary:" in msg
    assert "Link:" in msg
    assert "Why it matters:" not in msg
