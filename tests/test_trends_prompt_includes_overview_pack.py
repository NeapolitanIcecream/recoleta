from __future__ import annotations

import importlib
from datetime import UTC, datetime
from typing import Any

rag_agent: Any = importlib.import_module("recoleta.rag.agent")


def test_trend_prompt_includes_overview_pack_ranking_and_rep_source_when_provided() -> (
    None
):
    prompt_payload = rag_agent.build_trend_prompt_payload(
        granularity="week",
        period_start=datetime(2026, 3, 1, tzinfo=UTC),
        period_end=datetime(2026, 3, 8, tzinfo=UTC),
        corpus_doc_type="trend",
        corpus_granularity="day",
        overview_pack_md="## Overview pack\n- x\n",
        rag_sources=[
            {"doc_type": "item", "granularity": None},
            {"doc_type": "trend", "granularity": "day"},
        ],
        ranking_n=7,
        rep_source_doc_type="item",
        history_pack_md="## History pack\n- prev_1\n",
        evolution_max_signals=4,
    )

    assert prompt_payload.get("overview_pack_md") == "## Overview pack\n- x\n"
    assert prompt_payload.get("history_pack_md") == "## History pack\n- prev_1\n"
    assert prompt_payload.get("rag_sources") == [
        {"doc_type": "item", "granularity": None},
        {"doc_type": "trend", "granularity": "day"},
    ]
    assert prompt_payload.get("ranking_n") == 7
    assert prompt_payload.get("rep_source_doc_type") == "item"
    assert prompt_payload.get("evolution_max_signals") == 4
    assert prompt_payload.get("evolution_change_types") == [
        "continuing",
        "emerging",
        "fading",
        "shifting",
        "polarizing",
    ]
    assert prompt_payload.get("evolution_requirements") == {
        "avoid_generic_summary": True,
        "prefer_concrete_titles": True,
        "prefer_named_history_anchors": True,
        "prefer_quantitative_details": True,
        "render_history_window_mentions": True,
        "use_fewer_signals_if_evidence_is_thin": True,
    }
    notes = prompt_payload.get("notes") or []
    assert any(
        "use the exact prev_n token" in str(note) and "do not manually repeat" in str(note)
        for note in notes
    )


def test_resolve_rag_query_sources_limits_week_trend_searches_to_day_docs() -> None:
    sources = rag_agent.resolve_rag_query_sources(
        doc_type="trend",
        granularity=None,
        rag_sources=[
            {"doc_type": "item", "granularity": None},
            {"doc_type": "trend", "granularity": "day"},
        ],
    )

    assert sources == [("trend", "day")]


def test_resolve_rag_query_sources_rejects_disallowed_trend_granularity() -> None:
    sources = rag_agent.resolve_rag_query_sources(
        doc_type="trend",
        granularity="month",
        rag_sources=[
            {"doc_type": "item", "granularity": None},
            {"doc_type": "trend", "granularity": "day"},
        ],
    )

    assert sources == []
