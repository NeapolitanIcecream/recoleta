from __future__ import annotations

from recoleta.passes.trend_ideas import (
    TrendIdeasPayload,
    normalize_trend_ideas_payload_with_stats,
)
from recoleta.rag.evidence_reads import successful_evidence_read_doc_ids


def test_ideas_quality_gate_does_not_treat_search_hits_as_read_evidence() -> None:
    read_doc_ids, trace_stats = successful_evidence_read_doc_ids(
        debug={
            "raw_tool_trace": {
                "status": "captured",
                "events_truncated": False,
                "events": [
                    {
                        "kind": "tool-call",
                        "tool_name": "search_hybrid",
                        "tool_call_id": "search-1",
                        "args": {"query": "runtime checks", "doc_type": "item"},
                    },
                    {
                        "kind": "tool-return",
                        "tool_name": "search_hybrid",
                        "tool_call_id": "search-1",
                        "content": {"hits": [{"doc_id": 22}]},
                    },
                    {
                        "kind": "tool-call",
                        "tool_name": "get_doc_bundle",
                        "tool_call_id": "read-1",
                        "args": {"doc_id": 11},
                    },
                    {
                        "kind": "tool-return",
                        "tool_name": "get_doc_bundle",
                        "tool_call_id": "read-1",
                        "content": {
                            "bundle": {
                                "doc": {"doc_id": 11},
                                "summary": {
                                    "chunk_id": 111,
                                    "doc_id": 11,
                                    "chunk_index": 0,
                                    "text": "Inspected summary.",
                                },
                            }
                        },
                    },
                ],
            }
        }
    )

    assert read_doc_ids == {11}
    assert trace_stats["trace_status"] == "captured"
    assert trace_stats["trace_complete"] is True


def test_ideas_quality_gate_rejects_existing_but_unread_evidence() -> None:
    payload = TrendIdeasPayload.model_validate(
        {
            "title": "Ideas",
            "granularity": "day",
            "period_start": "2026-03-09T00:00:00+00:00",
            "period_end": "2026-03-10T00:00:00+00:00",
            "summary_md": "Summary",
            "ideas": [
                {
                    "title": "Cross-source claim without cross-source reading",
                    "content_md": "The second source was found but never inspected.",
                    "evidence_refs": [
                        {"doc_id": 11, "chunk_index": 0},
                        {"doc_id": 22, "chunk_index": 0},
                    ],
                }
            ],
        }
    )

    normalized, stats = normalize_trend_ideas_payload_with_stats(
        payload,
        min_distinct_docs=2,
        allowed_doc_ids={11, 22},
        read_doc_ids={11},
    )

    assert normalized.ideas == []
    assert stats["dropped_unread_ref_total"] == 1
    assert stats["dropped_insufficient_distinct_docs_total"] == 1


def test_ideas_quality_gate_rejects_unread_chunk_indices() -> None:
    payload = TrendIdeasPayload.model_validate(
        {
            "title": "Ideas",
            "granularity": "day",
            "period_start": "2026-03-09T00:00:00+00:00",
            "period_end": "2026-03-10T00:00:00+00:00",
            "summary_md": "Summary",
            "ideas": [
                {
                    "title": "Correct documents with fabricated chunks",
                    "content_md": "Neither cited chunk was returned by a body-read tool.",
                    "evidence_refs": [
                        {"doc_id": 11, "chunk_index": 999},
                        {"doc_id": 22, "chunk_index": 888},
                    ],
                }
            ],
        }
    )

    normalized, stats = normalize_trend_ideas_payload_with_stats(
        payload,
        min_distinct_docs=2,
        allowed_doc_ids={11, 22},
        read_refs={(11, 0), (22, 0)},
    )

    assert normalized.ideas == []
    assert stats["dropped_unread_ref_total"] == 2
    assert stats["dropped_insufficient_distinct_docs_total"] == 1
