from __future__ import annotations

from datetime import UTC, datetime

from recoleta.rag.ideas_agent import (
    _build_trend_ideas_instructions,
    build_trend_ideas_prompt_payload,
)
from recoleta.trends import TrendPayload


def test_ideas_instructions_require_consensus_terminology_and_plain_language() -> None:
    instructions = _build_trend_ideas_instructions(
        output_language="Chinese (Simplified)"
    )

    assert "Do not invent new umbrella terms, branded labels, or slogan-like phrasing." in instructions
    assert "If a technical term does not have a stable translation" in instructions
    assert "prefer the original source-language term" in instructions
    assert "Prefer plain, literal wording" in instructions


def test_ideas_prompt_payload_reinforces_readability_constraints() -> None:
    payload = build_trend_ideas_prompt_payload(
        granularity="day",
        period_start=datetime(2026, 3, 9, tzinfo=UTC),
        period_end=datetime(2026, 3, 10, tzinfo=UTC),
        trend_payload=TrendPayload(
            title="Agent systems",
            granularity="day",
            period_start="2026-03-09T00:00:00+00:00",
            period_end="2026-03-10T00:00:00+00:00",
            overview_md="## Overview\n\nExecution loops are tightening.\n",
            topics=["agents"],
            clusters=[],
            highlights=[],
        ),
        trend_snapshot_pack_md="## Trend snapshot pack\n\nExecution loops are tightening.\n",
    )

    notes = payload["notes"]
    assert "Do not coin new umbrella terms or marketing-style labels." in notes
    assert (
        "If a technical term lacks a stable translation in the requested output language, keep the original term."
        in notes
    )
    assert "Prefer direct, readable phrasing over compressed jargon." in notes
