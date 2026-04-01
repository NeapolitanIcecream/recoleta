from __future__ import annotations

from pathlib import Path

from recoleta.prompt_style import reader_facing_ai_tropes_prompt


REPO_ROOT = Path(__file__).resolve().parents[1]


def _normalize(value: str) -> str:
    return value.rstrip("\n")


def test_reader_facing_ai_tropes_prompt_matches_docs_asset() -> None:
    docs_asset = REPO_ROOT / "docs" / "assets" / "ai-tropes.md"

    assert docs_asset.exists()
    assert _normalize(docs_asset.read_text(encoding="utf-8")) == _normalize(
        reader_facing_ai_tropes_prompt()
    )
