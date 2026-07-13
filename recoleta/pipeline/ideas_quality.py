from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from typing import Any

from recoleta import trends

_PRIOR_IDEAS_PACK_MAX_CHARS = 6_000
_PRIOR_IDEAS_PEER_WINDOW_COUNT = 3
_PRIOR_IDEAS_SECTION_MAX_ENTRIES = 12
_PRIOR_IDEA_ENTRY_MAX_CHARS = 420
_EVIDENCE_READ_TOOLS = {"get_doc", "get_doc_bundle", "read_chunk"}


@dataclass(frozen=True, slots=True)
class _PriorIdeasSection:
    label: str
    granularity: str
    period_start: datetime
    period_end: datetime


def _prior_ideas_sections(
    *, granularity: str, period_start: datetime, period_end: datetime
) -> list[_PriorIdeasSection]:
    normalized_granularity = str(granularity or "").strip().lower()
    sections: list[_PriorIdeasSection] = []
    lower_granularity = {"week": "day", "month": "week"}.get(
        normalized_granularity
    )
    if lower_granularity is not None:
        sections.append(
            _PriorIdeasSection(
                label=f"Current-period {lower_granularity} ideas",
                granularity=lower_granularity,
                period_start=period_start,
                period_end=period_end,
            )
        )
    for window in trends.peer_history_windows_for_period(
        granularity=normalized_granularity,
        period_start=period_start,
        window_count=_PRIOR_IDEAS_PEER_WINDOW_COUNT,
    ):
        sections.append(
            _PriorIdeasSection(
                label=f"Previous {normalized_granularity} {window.label}",
                granularity=normalized_granularity,
                period_start=window.period_start,
                period_end=window.period_end,
            )
        )
    return sections


def _compact_prior_idea_entry(text_value: Any) -> tuple[str, bool]:
    source_lines = [
        " ".join(str(line or "").split()).strip()
        for line in str(text_value or "").splitlines()
    ]
    retained_lines = [
        line
        for line in source_lines
        if line and not line.lower().startswith("evidence:")
    ]
    compact = " | ".join(retained_lines).strip()
    if len(compact) <= _PRIOR_IDEA_ENTRY_MAX_CHARS:
        return compact, False
    return compact[: _PRIOR_IDEA_ENTRY_MAX_CHARS - 1].rstrip() + "…", True


def _render_prior_pack(lines: list[str]) -> str:
    return "\n".join(lines).rstrip() + "\n" if lines else ""


def _prior_pack_stats(*, sections: list[_PriorIdeasSection], max_chars: int) -> dict[str, Any]:
    return {
        "requested_sections": len(sections),
        "available_sections": 0,
        "candidate_entries_total": 0,
        "retained_entries_total": 0,
        "source_documents_total": 0,
        "section_limit_omitted_total": 0,
        "budget_omitted_total": 0,
        "entry_text_truncated_total": 0,
        "max_chars": max_chars,
        "chars": 0,
        "truncated": False,
    }


def _load_prior_section_entries(
    *,
    repository: Any,
    sections: list[_PriorIdeasSection],
    stats: dict[str, Any],
) -> list[tuple[_PriorIdeasSection, list[tuple[int, str]]]]:
    section_entries: list[tuple[_PriorIdeasSection, list[tuple[int, str]]]] = []
    source_doc_ids: set[int] = set()
    seen_entries: set[str] = set()
    for section in sections:
        rows = repository.list_document_chunk_index_rows_in_period(
            doc_type="idea",
            kind="content",
            granularity=section.granularity,
            period_start=section.period_start,
            period_end=section.period_end,
            limit=_PRIOR_IDEAS_SECTION_MAX_ENTRIES + 1,
            offset=0,
        )
        if len(rows) > _PRIOR_IDEAS_SECTION_MAX_ENTRIES:
            stats["section_limit_omitted_total"] += (
                len(rows) - _PRIOR_IDEAS_SECTION_MAX_ENTRIES
            )
            rows = rows[:_PRIOR_IDEAS_SECTION_MAX_ENTRIES]
        entries: list[tuple[int, str]] = []
        for row in rows:
            compact, text_truncated = _compact_prior_idea_entry(row.get("text"))
            if not compact or compact.casefold() in seen_entries:
                continue
            seen_entries.add(compact.casefold())
            if text_truncated:
                stats["entry_text_truncated_total"] += 1
            try:
                doc_id = int(row.get("doc_id") or 0)
            except Exception:
                doc_id = 0
            if doc_id > 0:
                source_doc_ids.add(doc_id)
            entries.append((doc_id, compact))
        if entries:
            stats["available_sections"] += 1
            stats["candidate_entries_total"] += len(entries)
            section_entries.append((section, entries))
    stats["source_documents_total"] = len(source_doc_ids)
    return section_entries


def _render_bounded_prior_entries(
    *,
    granularity: str,
    section_entries: list[tuple[_PriorIdeasSection, list[tuple[int, str]]]],
    stats: dict[str, Any],
    max_chars: int,
) -> str:
    lines = [
        "## Prior ideas exclusion pack",
        "- purpose=deduplication_only",
        "- never_cite_as_evidence=true",
        f"- target_granularity={str(granularity or '').strip().lower()}",
    ]
    if len(_render_prior_pack(lines)) > max_chars:
        stats["budget_omitted_total"] = int(stats["candidate_entries_total"])
        return ""
    retained_doc_ids: set[int] = set()
    for section, entries in section_entries:
        section_started = False
        for doc_id, entry in entries:
            prefix = ["", f"### {section.label}"] if not section_started else []
            candidate_lines = [*lines, *prefix, f"- {entry}"]
            if len(_render_prior_pack(candidate_lines)) > max_chars:
                stats["budget_omitted_total"] += 1
                continue
            lines = candidate_lines
            section_started = True
            stats["retained_entries_total"] += 1
            if doc_id > 0:
                retained_doc_ids.add(doc_id)
    stats["source_documents_total"] = len(retained_doc_ids)
    return _render_prior_pack(lines) if retained_doc_ids else ""


def build_prior_ideas_pack_md(
    *,
    repository: Any,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
    max_chars: int = _PRIOR_IDEAS_PACK_MAX_CHARS,
) -> tuple[str, dict[str, Any]]:
    """Build bounded prior-output context used only to reject repeated ideas."""

    normalized_max_chars = max(0, int(max_chars or 0))
    sections = _prior_ideas_sections(
        granularity=granularity,
        period_start=period_start,
        period_end=period_end,
    )
    stats = _prior_pack_stats(sections=sections, max_chars=normalized_max_chars)
    section_entries = _load_prior_section_entries(
        repository=repository,
        sections=sections,
        stats=stats,
    )
    if not section_entries or normalized_max_chars <= 0:
        stats["truncated"] = bool(section_entries)
        return "", stats
    pack_md = _render_bounded_prior_entries(
        granularity=granularity,
        section_entries=section_entries,
        stats=stats,
        max_chars=normalized_max_chars,
    )
    stats["chars"] = len(pack_md)
    stats["truncated"] = bool(
        stats["section_limit_omitted_total"]
        or stats["budget_omitted_total"]
        or stats["entry_text_truncated_total"]
    )
    return pack_md, stats


def _mapping_value(value: Any) -> dict[str, Any] | None:
    if isinstance(value, dict):
        return value
    if not isinstance(value, str):
        return None
    try:
        parsed = json.loads(value)
    except Exception:
        return None
    return parsed if isinstance(parsed, dict) else None


def _returned_read_doc_id(*, tool_name: str, content: Any) -> int | None:
    mapping = _mapping_value(content)
    if mapping is None:
        return None
    nested: Any
    if tool_name == "get_doc":
        nested = mapping.get("doc")
    elif tool_name == "get_doc_bundle":
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
    except Exception:
        return None
    return doc_id if doc_id > 0 else None


def successful_read_doc_ids(
    *, debug: dict[str, Any]
) -> tuple[set[int], dict[str, Any]]:
    """Return documents from completed explicit read calls, excluding search hits."""

    trace = debug.get("raw_tool_trace")
    if not isinstance(trace, dict):
        return set(), {
            "trace_status": "unavailable",
            "trace_events_truncated": False,
        }
    trace_status = str(trace.get("status") or "unavailable").strip().lower()
    events = trace.get("events")
    if trace_status != "captured" or not isinstance(events, list):
        return set(), {
            "trace_status": trace_status or "unavailable",
            "trace_events_truncated": bool(trace.get("events_truncated")),
        }

    calls: dict[str, tuple[str, int]] = {}
    read_doc_ids: set[int] = set()
    for event in events:
        if not isinstance(event, dict):
            continue
        tool_name = str(event.get("tool_name") or "").strip()
        tool_call_id = str(event.get("tool_call_id") or "").strip()
        if tool_name not in _EVIDENCE_READ_TOOLS or not tool_call_id:
            continue
        if str(event.get("kind") or "") == "tool-call":
            args = _mapping_value(event.get("args"))
            if args is None:
                continue
            try:
                doc_id = int(args.get("doc_id") or 0)
            except Exception:
                continue
            if doc_id > 0:
                calls[tool_call_id] = (tool_name, doc_id)
            continue
        if str(event.get("kind") or "") != "tool-return":
            continue
        call = calls.get(tool_call_id)
        if call is None or call[0] != tool_name:
            continue
        returned_doc_id = _returned_read_doc_id(
            tool_name=tool_name,
            content=event.get("content"),
        )
        if returned_doc_id is not None and returned_doc_id == call[1]:
            read_doc_ids.add(returned_doc_id)
    return read_doc_ids, {
        "trace_status": trace_status,
        "trace_events_truncated": bool(trace.get("events_truncated")),
    }


def item_document_ids(*, repository: Any, doc_ids: set[int]) -> set[int]:
    item_doc_ids: set[int] = set()
    for doc_id in sorted(doc_ids):
        doc = repository.get_document(doc_id=doc_id)
        if str(getattr(doc, "doc_type", "") or "").strip().lower() == "item":
            item_doc_ids.add(doc_id)
    return item_doc_ids


__all__ = [
    "build_prior_ideas_pack_md",
    "item_document_ids",
    "successful_read_doc_ids",
]
