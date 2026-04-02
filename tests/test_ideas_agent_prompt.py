from __future__ import annotations

from datetime import UTC, datetime

from recoleta.passes.trend_ideas import TrendIdeasPayload, normalize_trend_ideas_payload
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
    assert "Do not translate paper titles, framework names, product names, or acronyms" in instructions
    assert "Idea titles should be factual descriptive noun phrases" in instructions
    assert "Emit 0 to 3 ideas total" in instructions
    assert "The first idea must be the clear best bet" in instructions
    assert "anti-thesis" in instructions.lower()
    assert "buyer trigger or operational pain" in instructions
    assert "The goal is not to ban every phrase once." in instructions
    assert "Avoid negative parallelism" in instructions
    assert "Avoid false suspense" in instructions
    assert "Avoid fractal summaries" in instructions
    assert "return an empty ideas list" in instructions


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
    assert (
        "Keep paper titles, framework names, product names, and acronyms in their original form unless a widely accepted translation exists."
        in notes
    )
    assert (
        "Idea titles should read like factual descriptive labels, not slogans, coined categories, or rhetorical questions."
        in notes
    )
    assert "Prefer 0-3 ideas; omit weak ideas instead of filling the list." in notes
    assert (
        "the first one must be the clear best bet and any later ones must be explicit alternates."
        in " ".join(notes)
    )
    assert "Each emitted idea should also name the clearest condition under which the thesis breaks." in notes
    assert "Name the buyer trigger or operational pain directly instead of using generic platform language." in notes


def test_normalize_trend_ideas_payload_caps_to_three_ranked_ideas() -> None:
    payload = TrendIdeasPayload.model_validate(
        {
            "title": "Ideas",
            "granularity": "day",
            "period_start": "2026-03-09T00:00:00+00:00",
            "period_end": "2026-03-10T00:00:00+00:00",
            "summary_md": "Summary",
            "ideas": [
                {
                    "title": f"Idea {index}",
                    "kind": "tooling_wedge",
                    "thesis": f"Thesis {index}",
                    "why_now": f"Why now {index}",
                    "what_changed": f"What changed {index}",
                    "user_or_job": f"Role {index}",
                    "evidence_refs": [{"doc_id": index, "chunk_index": 0}],
                    "validation_next_step": f"Validation {index}",
                    "time_horizon": "now",
                }
                for index in range(1, 5)
            ],
        }
    )

    normalized = normalize_trend_ideas_payload(payload)

    assert [idea.title for idea in normalized.ideas] == ["Idea 1", "Idea 2", "Idea 3"]
