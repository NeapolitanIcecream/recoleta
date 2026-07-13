from __future__ import annotations

from typing import Any

import pytest

from recoleta.rag.evidence_reads import successful_evidence_read_doc_ids


def _read_events() -> list[dict[str, Any]]:
    return [
        {
            "kind": "tool-call",
            "tool_name": "get_doc",
            "tool_call_id": "metadata",
            "args": {"doc_id": 10},
        },
        {
            "kind": "tool-return",
            "tool_name": "get_doc",
            "tool_call_id": "metadata",
            "content": {"doc": {"doc_id": 10}},
        },
        {
            "kind": "tool-call",
            "tool_name": "get_doc_bundle",
            "tool_call_id": "bundle",
            "args": "{\"doc_id\": 11}",
        },
        {
            "kind": "tool-return",
            "tool_name": "get_doc_bundle",
            "tool_call_id": "bundle",
            "content": {"bundle": {"doc": {"doc_id": 11}}},
        },
        {
            "kind": "tool-call",
            "tool_name": "read_chunk",
            "tool_call_id": "chunk",
            "args": {"doc_id": 12, "chunk_index": 0},
        },
        {
            "kind": "tool-return",
            "tool_name": "read_chunk",
            "tool_call_id": "chunk",
            "content": "{\"chunk\": {\"doc_id\": 12}}",
        },
    ]


def test_evidence_reads_count_only_completed_body_reads() -> None:
    doc_ids, stats = successful_evidence_read_doc_ids(
        debug={
            "raw_tool_trace": {
                "status": "captured",
                "events_truncated": False,
                "events": _read_events(),
            }
        }
    )

    assert doc_ids == {11, 12}
    assert stats == {
        "trace_status": "captured",
        "trace_events_truncated": False,
        "trace_complete": True,
    }


@pytest.mark.parametrize(
    ("debug", "expected_status", "expected_truncated"),
    [
        (None, "missing", False),
        ({}, "missing", False),
        (
            {"raw_tool_trace": {"status": "unavailable", "events": []}},
            "unavailable",
            False,
        ),
        (
            {
                "raw_tool_trace": {
                    "status": "captured",
                    "events_truncated": False,
                    "events": {},
                }
            },
            "captured",
            False,
        ),
        (
            {
                "raw_tool_trace": {
                    "status": "captured",
                    "events_truncated": True,
                    "events": _read_events(),
                }
            },
            "captured",
            True,
        ),
    ],
)
def test_evidence_reads_fail_closed_for_incomplete_trace(
    debug: dict[str, Any] | None,
    expected_status: str,
    expected_truncated: bool,
) -> None:
    doc_ids, stats = successful_evidence_read_doc_ids(debug=debug)

    assert doc_ids == set()
    assert stats["trace_status"] == expected_status
    assert stats["trace_events_truncated"] is expected_truncated
    assert stats["trace_complete"] is False
