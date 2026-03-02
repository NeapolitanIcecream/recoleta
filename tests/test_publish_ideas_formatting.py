from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from recoleta.publish import write_markdown_note, write_obsidian_note


def test_write_markdown_note_formats_structured_ideas(tmp_path: Path) -> None:
    note_path = write_markdown_note(
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
        insight="I",
        ideas=[
            "Opportunity: Better evaluation | Why now: Tools matured | Example bet: Build a harness",
            "Plain fallback idea",
        ],
    )

    text = note_path.read_text(encoding="utf-8")
    assert "## Ideas" in text
    assert "- **Opportunity**: Better evaluation" in text
    assert "  - **Why now**: Tools matured" in text
    assert "  - **Example bet**: Build a harness" in text
    assert "- Plain fallback idea" in text


def test_write_obsidian_note_formats_structured_ideas(tmp_path: Path) -> None:
    vault_path = tmp_path / "vault"
    note_path = write_obsidian_note(
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
        insight="I",
        ideas=[
            "Opportunity: Better evaluation | Why now: Tools matured | Example bet: Build a harness",
        ],
    )

    text = note_path.read_text(encoding="utf-8")
    assert "- **Opportunity**: Better evaluation" in text
    assert "  - **Why now**: Tools matured" in text
    assert "  - **Example bet**: Build a harness" in text
