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
    )

    assert prompt_payload.get("overview_pack_md") == "## Overview pack\n- x\n"
    assert prompt_payload.get("rag_sources") == [
        {"doc_type": "item", "granularity": None},
        {"doc_type": "trend", "granularity": "day"},
    ]
    assert prompt_payload.get("ranking_n") == 7
    assert prompt_payload.get("rep_source_doc_type") == "item"


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
