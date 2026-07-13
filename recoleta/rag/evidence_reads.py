from __future__ import annotations

from typing import Any, TypedDict

import orjson

_BODY_READ_TOOLS = {"get_doc_bundle", "read_chunk"}
_BodyReadCall = tuple[str, int, int | None]
_ToolEvent = tuple[str, str, str, dict[str, Any]]
EvidenceReadRef = tuple[int, int]


EvidenceReadTraceStats = TypedDict(
    "EvidenceReadTraceStats",
    {
        "trace_status": str,
        "trace_events_truncated": bool,
        "trace_complete": bool,
    },
)


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


def _chunk_ref(value: Any, *, require_body: bool = True) -> EvidenceReadRef | None:
    if not isinstance(value, dict):
        return None
    if require_body and not str(value.get("text") or "").strip():
        return None
    raw_chunk_index = value.get("chunk_index")
    if raw_chunk_index is None:
        return None
    try:
        doc_id = int(value.get("doc_id") or 0)
        chunk_index = int(raw_chunk_index)
    except TypeError, ValueError:
        return None
    if doc_id <= 0 or chunk_index < 0:
        return None
    return doc_id, chunk_index


def _bundle_read_refs(bundle: dict[str, Any]) -> set[EvidenceReadRef]:
    refs: set[EvidenceReadRef] = set()
    summary = bundle.get("summary")
    summary_sections = bundle.get("summary_sections")
    summary_has_body = bool(
        isinstance(summary_sections, dict)
        and any(str(value or "").strip() for value in summary_sections.values())
    )
    summary_ref = _chunk_ref(summary, require_body=not summary_has_body)
    if summary_ref is not None:
        refs.add(summary_ref)
    content_chunks = bundle.get("content_chunks")
    if isinstance(content_chunks, list):
        refs.update(
            ref for value in content_chunks if (ref := _chunk_ref(value)) is not None
        )
    return refs


def _returned_read_refs(*, tool_name: str, content: Any) -> set[EvidenceReadRef]:
    mapping = _mapping_value(content)
    if mapping is None:
        return set()
    if tool_name == "get_doc_bundle":
        bundle = mapping.get("bundle")
        return _bundle_read_refs(bundle) if isinstance(bundle, dict) else set()
    chunk_ref = _chunk_ref(mapping.get("chunk"))
    return {chunk_ref} if tool_name == "read_chunk" and chunk_ref else set()


def _trace_events_and_stats(
    *, debug: dict[str, Any] | None
) -> tuple[list[Any] | None, EvidenceReadTraceStats]:
    trace = debug.get("raw_tool_trace") if isinstance(debug, dict) else None
    if not isinstance(trace, dict):
        return None, {
            "trace_status": "missing",
            "trace_events_truncated": False,
            "trace_complete": False,
        }

    status = str(trace.get("status") or "unknown").strip().lower() or "unknown"
    truncated = bool(trace.get("events_truncated"))
    raw_events = trace.get("events")
    events = raw_events if isinstance(raw_events, list) else None
    complete = status == "captured" and events is not None and not truncated
    return events if complete else None, {
        "trace_status": status,
        "trace_events_truncated": truncated,
        "trace_complete": complete,
    }


def _tool_event(value: Any) -> _ToolEvent | None:
    if not isinstance(value, dict):
        return None
    tool_name = str(value.get("tool_name") or "").strip()
    tool_call_id = str(value.get("tool_call_id") or "").strip()
    if not tool_call_id:
        return None
    kind = str(value.get("kind") or "").strip()
    if kind not in {"tool-call", "tool-return"}:
        return None
    return kind, tool_name, tool_call_id, value


def _called_read(event: dict[str, Any], *, tool_name: str) -> _BodyReadCall | None:
    args = _mapping_value(event.get("args"))
    if args is None:
        return None
    raw_chunk_index = args.get("chunk_index")
    try:
        doc_id = int(args.get("doc_id") or 0)
        chunk_index = None
        if tool_name == "read_chunk":
            if raw_chunk_index is None:
                return None
            chunk_index = int(raw_chunk_index)
    except TypeError, ValueError:
        return None
    if doc_id <= 0 or (chunk_index is not None and chunk_index < 0):
        return None
    return tool_name, doc_id, chunk_index


def _apply_tool_event(
    *, event: _ToolEvent, calls: dict[str, _BodyReadCall]
) -> set[EvidenceReadRef]:
    kind, tool_name, tool_call_id, value = event
    if kind == "tool-call":
        calls.pop(tool_call_id, None)
        if tool_name not in _BODY_READ_TOOLS:
            return set()
        call = _called_read(value, tool_name=tool_name)
        if call is not None:
            calls[tool_call_id] = call
        return set()

    call = calls.pop(tool_call_id, None)
    if call is None or call[0] != tool_name:
        return set()
    returned_refs = _returned_read_refs(
        tool_name=tool_name,
        content=value.get("content"),
    )
    expected_doc_id, expected_chunk_index = call[1], call[2]
    return {
        ref
        for ref in returned_refs
        if ref[0] == expected_doc_id
        and (expected_chunk_index is None or ref[1] == expected_chunk_index)
    }


def _successful_read_refs(events: list[Any]) -> set[EvidenceReadRef]:
    calls: dict[str, _BodyReadCall] = {}
    read_refs: set[EvidenceReadRef] = set()
    for value in events:
        event = _tool_event(value)
        if event is None:
            continue
        read_refs.update(_apply_tool_event(event=event, calls=calls))
    return read_refs


def successful_evidence_read_refs(
    *, debug: dict[str, Any] | None
) -> tuple[set[EvidenceReadRef], EvidenceReadTraceStats]:
    """Return exact chunks observed in complete, successful body-read calls."""

    events, stats = _trace_events_and_stats(debug=debug)
    if events is None:
        return set(), stats
    return _successful_read_refs(events), stats


def successful_evidence_read_doc_ids(
    *, debug: dict[str, Any] | None
) -> tuple[set[int], EvidenceReadTraceStats]:
    """Return documents whose body was read through a complete captured trace.

    Metadata-only ``get_doc`` calls and discovery results do not count. An absent,
    malformed, non-captured, or truncated trace fails closed.
    """

    refs, stats = successful_evidence_read_refs(debug=debug)
    return {doc_id for doc_id, _ in refs}, stats


__all__ = [
    "EvidenceReadRef",
    "EvidenceReadTraceStats",
    "successful_evidence_read_doc_ids",
    "successful_evidence_read_refs",
]
