from __future__ import annotations

from datetime import UTC, datetime

from recoleta.rag import agent as rag_agent
from recoleta.trends import build_empty_trend_payload


def test_trend_agent_instructions_include_output_language() -> None:
    instructions = rag_agent._build_trend_instructions(
        output_language="Chinese (Simplified)"
    )
    assert "Use Chinese (Simplified) for all natural language fields" in instructions
    assert "Keep all JSON keys in English" in instructions
    assert "keep topics as concise English tags" in instructions
    assert "under 200 Chinese characters or 200 words" in instructions
    assert "do not add a Topics/主题 section inside overview_md" in instructions


def test_trends_empty_payload_localizes_for_chinese() -> None:
    period_start = datetime(2026, 3, 1, tzinfo=UTC)
    period_end = datetime(2026, 3, 2, tzinfo=UTC)
    payload = build_empty_trend_payload(
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        output_language="zh-CN",
    )
    assert payload.title == "本期暂无可发布研究趋势"
    assert "没有可用文档" in payload.overview_md
