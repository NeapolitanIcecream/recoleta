from __future__ import annotations

from typing import Any

import pytest

from recoleta.rag.evidence_reads import (
    successful_evidence_read_doc_ids,
    successful_evidence_read_refs,
)


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
            "args": '{"doc_id": 11}',
        },
        {
            "kind": "tool-return",
            "tool_name": "get_doc_bundle",
            "tool_call_id": "bundle",
            "content": {
                "bundle": {
                    "doc": {"doc_id": 11},
                    "summary": {
                        "chunk_id": 110,
                        "doc_id": 11,
                        "chunk_index": 0,
                        "text": "Summary body.",
                    },
                    "content_chunks": [
                        {
                            "chunk_id": 111,
                            "doc_id": 11,
                            "chunk_index": 1,
                            "text": "Main-text body.",
                        }
                    ],
                }
            },
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
            "content": (
                '{"chunk": {"chunk_id": 120, "doc_id": 12, '
                '"chunk_index": 0, "text": "Chunk body."}}'
            ),
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

    refs, _ = successful_evidence_read_refs(
        debug={
            "raw_tool_trace": {
                "status": "captured",
                "events_truncated": False,
                "events": _read_events(),
            }
        }
    )
    assert refs == {(11, 0), (11, 1), (12, 0)}


def test_evidence_reads_reject_doc_metadata_without_returned_chunks() -> None:
    refs, stats = successful_evidence_read_refs(
        debug={
            "raw_tool_trace": {
                "status": "captured",
                "events_truncated": False,
                "events": [
                    {
                        "kind": "tool-call",
                        "tool_name": "get_doc_bundle",
                        "tool_call_id": "empty-bundle",
                        "args": {"doc_id": 11},
                    },
                    {
                        "kind": "tool-return",
                        "tool_name": "get_doc_bundle",
                        "tool_call_id": "empty-bundle",
                        "content": {"bundle": {"doc": {"doc_id": 11}}},
                    },
                    {
                        "kind": "tool-call",
                        "tool_name": "read_chunk",
                        "tool_call_id": "missing-chunk",
                        "args": {"doc_id": 12, "chunk_index": 999},
                    },
                    {
                        "kind": "tool-return",
                        "tool_name": "read_chunk",
                        "tool_call_id": "missing-chunk",
                        "content": {"chunk": None},
                    },
                ],
            }
        }
    )

    assert refs == set()
    assert stats["trace_complete"] is True


def test_evidence_reads_reject_chunks_with_ids_but_no_body_text() -> None:
    refs, _ = successful_evidence_read_refs(
        debug={
            "raw_tool_trace": {
                "status": "captured",
                "events_truncated": False,
                "events": [
                    {
                        "kind": "tool-call",
                        "tool_name": "get_doc_bundle",
                        "tool_call_id": "bundle",
                        "args": {"doc_id": 11},
                    },
                    {
                        "kind": "tool-return",
                        "tool_name": "get_doc_bundle",
                        "tool_call_id": "bundle",
                        "content": {
                            "bundle": {
                                "summary": {
                                    "chunk_id": 110,
                                    "doc_id": 11,
                                    "chunk_index": 0,
                                    "text": "  ",
                                },
                                "content_chunks": [
                                    {
                                        "chunk_id": 111,
                                        "doc_id": 11,
                                        "chunk_index": 1,
                                        "text": "",
                                    }
                                ],
                            }
                        },
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
                        "content": {
                            "chunk": {
                                "chunk_id": 120,
                                "doc_id": 12,
                                "chunk_index": 0,
                                "text": "\n",
                            }
                        },
                    },
                ],
            }
        }
    )

    assert refs == set()


def test_evidence_reads_accept_nonempty_bundle_summary_sections() -> None:
    refs, _ = successful_evidence_read_refs(
        debug={
            "raw_tool_trace": {
                "status": "captured",
                "events_truncated": False,
                "events": [
                    {
                        "kind": "tool-call",
                        "tool_name": "get_doc_bundle",
                        "tool_call_id": "bundle",
                        "args": {"doc_id": 11},
                    },
                    {
                        "kind": "tool-return",
                        "tool_name": "get_doc_bundle",
                        "tool_call_id": "bundle",
                        "content": {
                            "bundle": {
                                "summary": {
                                    "chunk_id": 110,
                                    "doc_id": 11,
                                    "chunk_index": 0,
                                    "text": "",
                                },
                                "summary_sections": {
                                    "key_findings": "Verified summary body."
                                },
                            }
                        },
                    },
                ],
            }
        }
    )

    assert refs == {(11, 0)}


def test_evidence_reads_consume_a_call_on_its_first_return() -> None:
    refs, _ = successful_evidence_read_refs(
        debug={
            "raw_tool_trace": {
                "status": "captured",
                "events_truncated": False,
                "events": [
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
                        "content": {"chunk": None},
                    },
                    {
                        "kind": "tool-return",
                        "tool_name": "read_chunk",
                        "tool_call_id": "chunk",
                        "content": {
                            "chunk": {
                                "chunk_id": 120,
                                "doc_id": 12,
                                "chunk_index": 0,
                                "text": "Late replayed body.",
                            }
                        },
                    },
                ],
            }
        }
    )

    assert refs == set()


def test_evidence_reads_replace_a_pending_call_when_its_id_is_reused() -> None:
    refs, _ = successful_evidence_read_refs(
        debug={
            "raw_tool_trace": {
                "status": "captured",
                "events_truncated": False,
                "events": [
                    {
                        "kind": "tool-call",
                        "tool_name": "read_chunk",
                        "tool_call_id": "reused",
                        "args": {"doc_id": 11, "chunk_index": 0},
                    },
                    {
                        "kind": "tool-call",
                        "tool_name": "read_chunk",
                        "tool_call_id": "reused",
                        "args": {"doc_id": 12, "chunk_index": 1},
                    },
                    {
                        "kind": "tool-return",
                        "tool_name": "read_chunk",
                        "tool_call_id": "reused",
                        "content": {
                            "chunk": {
                                "chunk_id": 121,
                                "doc_id": 12,
                                "chunk_index": 1,
                                "text": "Replacement call body.",
                            }
                        },
                    },
                    {
                        "kind": "tool-return",
                        "tool_name": "read_chunk",
                        "tool_call_id": "reused",
                        "content": {
                            "chunk": {
                                "chunk_id": 110,
                                "doc_id": 11,
                                "chunk_index": 0,
                                "text": "Stale call body.",
                            }
                        },
                    },
                ],
            }
        }
    )

    assert refs == {(12, 1)}


def test_evidence_reads_clear_a_pending_call_when_reused_id_is_invalid() -> None:
    refs, _ = successful_evidence_read_refs(
        debug={
            "raw_tool_trace": {
                "status": "captured",
                "events_truncated": False,
                "events": [
                    {
                        "kind": "tool-call",
                        "tool_name": "read_chunk",
                        "tool_call_id": "reused",
                        "args": {"doc_id": 11, "chunk_index": 0},
                    },
                    {
                        "kind": "tool-call",
                        "tool_name": "read_chunk",
                        "tool_call_id": "reused",
                        "args": {"doc_id": 0, "chunk_index": 0},
                    },
                    {
                        "kind": "tool-return",
                        "tool_name": "read_chunk",
                        "tool_call_id": "reused",
                        "content": {
                            "chunk": {
                                "chunk_id": 110,
                                "doc_id": 11,
                                "chunk_index": 0,
                                "text": "Stale call body.",
                            }
                        },
                    },
                ],
            }
        }
    )

    assert refs == set()


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
