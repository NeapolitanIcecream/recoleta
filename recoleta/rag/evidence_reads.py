from __future__ import annotations

from typing import Any, TypedDict

import orjson

_BODY_READ_TOOLS = {"get_doc_bundle", "read_chunk"}


class EvidenceReadTraceStats(TypedDict):
    trace_status: str
    trace_events_truncated: bool
    trace_complete: bool


def _mapping_value(value: Any) -> dict[str, Any] | None:
    if isinstance(value, dict):
        return value
    if not isinstance(value, (str, bytes)):
        return None
    try:
        parsed = orjson.loads(value)
    except orjson.JSONDecodeError:
        return None
    return parsed if isinstance(parsed, dict) else None


def _returned_doc_id(*, tool_name: str, content: Any) -> int | None:
    mapping = _mapping_value(content)
    if mapping is None:
        return None
    if tool_name == "get_doc_bundle":
        bundle = mapping.get("bundle")
        nested = bundle.get("doc") if isinstance(bundle, dict) else None
    elif tool_name == "read_chunk":
        nested = mapping.get("chunk")
    else:
        return None
    if not isinstance(nested, dict):
        return None
    try:
        doc_id = int(nested.get("doc_id") or 0)
    except (TypeError, ValueError):
        return None
    return doc_id if doc_id > 0 else None


def successful_evidence_read_doc_ids(
    *, debug: dict[str, Any] | None
) -> tuple[set[int], EvidenceReadTraceStats]:
    """Return documents whose body was read through a complete captured trace.

    Metadata-only ``get_doc`` calls and discovery results do not count. An absent,
    malformed, non-captured, or truncated trace fails closed.
    """

    trace = debug.get("raw_tool_trace") if isinstance(debug, dict) else None
    status = "missing"
    truncated = False
    events: Any = None
    if isinstance(trace, dict):
        status = str(trace.get("status") or "unknown").strip().lower() or "unknown"
        truncated = bool(trace.get("events_truncated"))
        events = trace.get("events")
    complete = status == "captured" and isinstance(events, list) and not truncated
    stats: EvidenceReadTraceStats = {
        "trace_status": status,
        "trace_events_truncated": truncated,
        "trace_complete": complete,
    }
    if not complete:
        return set(), stats

    calls: dict[str, tuple[str, int]] = {}
    read_doc_ids: set[int] = set()
    for event in events:
        if not isinstance(event, dict):
            continue
        tool_name = str(event.get("tool_name") or "").strip()
        tool_call_id = str(event.get("tool_call_id") or "").strip()
        if tool_name not in _BODY_READ_TOOLS or not tool_call_id:
            continue
        kind = str(event.get("kind") or "").strip()
        if kind == "tool-call":
            args = _mapping_value(event.get("args"))
            if args is None:
                continue
            try:
                doc_id = int(args.get("doc_id") or 0)
            except (TypeError, ValueError):
                continue
            if doc_id > 0:
                calls[tool_call_id] = (tool_name, doc_id)
            continue
        if kind != "tool-return":
            continue
        call = calls.get(tool_call_id)
        if call is None or call[0] != tool_name:
            continue
        returned_doc_id = _returned_doc_id(
            tool_name=tool_name,
            content=event.get("content"),
        )
        if returned_doc_id is not None and returned_doc_id == call[1]:
            read_doc_ids.add(returned_doc_id)
    return read_doc_ids, stats


__all__ = ["EvidenceReadTraceStats", "successful_evidence_read_doc_ids"]
