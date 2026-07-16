from __future__ import annotations

from datetime import UTC, datetime

from recoleta.rag import agent as rag_agent
from recoleta.trends import build_empty_trend_payload, is_empty_trend_payload


def test_trend_agent_instructions_include_output_language() -> None:
    instructions = rag_agent._build_trend_instructions(
        output_language="Chinese (Simplified)"
    )
    assert "Use Chinese (Simplified) for all natural language fields" in instructions
    assert "Keep all JSON keys in English" in instructions
    assert "keep topics as concise English tags" in instructions
    assert "under 200 Chinese characters or 200 words" in instructions
    assert "do not add a Topics/主题 section inside overview_md" in instructions
    assert (
        "The public output should contain only overview_md and 0 to 4 cluster blocks"
        in instructions
    )
    assert "at least two distinct item doc_id values" in instructions
    assert "multiple chunks from one document still count as one source" in instructions
    assert "state the specific finding rather than naming a topic category" in instructions
    assert "at most three named systems, papers, or benchmarks" in instructions
    assert (
        "Do not leave raw prev_n tokens in title, overview_md, or clusters[].content_md"
        in instructions
    )
    assert (
        "The overview should state the finding, its scope, and any uncertainty" in instructions
    )
    assert (
        "continued momentum, or no material change are all valid findings"
        in instructions
    )
    assert (
        "Never infer a move, turn, push, or shift from the current window alone"
        in instructions
    )
    assert "it is valid to publish no clusters" in instructions
    assert "compare the title and opening with recent outputs" in instructions
    assert "Do not give every period the same grammatical frame" in instructions
    assert "omit evidence_refs[].reason" in instructions
    assert (
        "drill into the underlying item documents with get_doc_bundle" in instructions
    )
    assert (
        "overview pack lists representative_doc_id values" in instructions
        and "instead of searching again" in instructions
    )
    assert "normally 6 to 10 representative item documents" in instructions
    assert "do not fetch every listed representative" in instructions
    assert "Use get_doc only for metadata" in instructions
    assert "cite only item documents that you actually inspected" in instructions
    assert "Do not use negative parallelism" in instructions
    assert "Do not use suspense, rhetorical questions, or reveal-style contrasts" in instructions
    assert "Do not preview, restate, and conclude the same point" in instructions


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


def test_is_empty_trend_payload_accepts_legacy_english_placeholder_copy() -> None:
    period_start = datetime(2026, 3, 1, tzinfo=UTC)
    period_end = datetime(2026, 3, 2, tzinfo=UTC)
    payload = build_empty_trend_payload(
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        output_language="English",
    )
    payload.title = "No research trends available for publication this period"

    payload.overview_md = "- No documents were available during this period."
    assert is_empty_trend_payload(payload) is True

    payload.overview_md = "- No documents are available for this period."
    assert is_empty_trend_payload(payload) is True
