from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from recoleta import trends
from recoleta.pass_output_selection import (
    is_suppressed_pass_output,
    latest_idea_pass_output_states_by_window,
)

_PRIOR_IDEAS_PACK_MAX_CHARS = 6_000
_PRIOR_IDEAS_PEER_WINDOW_COUNT = 3
_PRIOR_IDEAS_SECTION_MAX_ENTRIES = 12
_PRIOR_IDEA_ENTRY_MAX_CHARS = 420


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
    lower_granularity = {"week": "day", "month": "week"}.get(normalized_granularity)
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


def _prior_pack_stats(
    *, sections: list[_PriorIdeasSection], max_chars: int
) -> dict[str, Any]:
    return {
        "requested_sections": len(sections),
        "available_sections": 0,
        "candidate_entries_total": 0,
        "retained_entries_total": 0,
        "source_documents_total": 0,
        "section_limit_omitted_total": 0,
        "budget_omitted_total": 0,
        "entry_text_truncated_total": 0,
        "inactive_entries_omitted_total": 0,
        "suppressed_entries_omitted_total": 0,
        "max_chars": max_chars,
        "chars": 0,
        "truncated": False,
    }


def _bounded_prior_rows(
    *, repository: Any, section: _PriorIdeasSection, stats: dict[str, Any]
) -> list[dict[str, Any]]:
    page_size = _PRIOR_IDEAS_SECTION_MAX_ENTRIES + 1
    offset = 0
    rows: list[dict[str, Any]] = []
    while len(rows) < page_size:
        page = list(
            repository.list_document_chunk_index_rows_in_period(
                doc_type="idea",
                kind="content",
                granularity=section.granularity,
                period_start=section.period_start,
                period_end=section.period_end,
                limit=page_size,
                offset=offset,
            )
        )
        if not page:
            break
        rows.extend(
            _exclude_inactive_prior_rows(
                repository=repository,
                rows=page,
                stats=stats,
            )
        )
        if len(page) < page_size:
            break
        offset += len(page)
    omitted = max(0, len(rows) - _PRIOR_IDEAS_SECTION_MAX_ENTRIES)
    stats["section_limit_omitted_total"] += omitted
    return list(rows[:_PRIOR_IDEAS_SECTION_MAX_ENTRIES])


def _exclude_inactive_prior_rows(
    *, repository: Any, rows: list[dict[str, Any]], stats: dict[str, Any]
) -> list[dict[str, Any]]:
    windows = {
        doc_id: (
            str(row.get("granularity") or "").strip().lower() or None,
            datetime.fromtimestamp(float(row["event_start_ts"]), tz=UTC),
            datetime.fromtimestamp(float(row["event_end_ts"]), tz=UTC),
        )
        for row in rows
        if (doc_id := _prior_entry_doc_id(row)) > 0
    }
    states_by_window = latest_idea_pass_output_states_by_window(
        repository=repository,
        windows=windows.values(),
    )
    filtered: list[dict[str, Any]] = []
    for row in rows:
        window = windows.get(_prior_entry_doc_id(row))
        state = states_by_window.get(window) if window is not None else None
        if state is None or state.active:
            filtered.append(row)
            continue
        stats["inactive_entries_omitted_total"] += 1
        stats["suppressed_entries_omitted_total"] += int(
            is_suppressed_pass_output(state.row)
        )
    return filtered


def _prior_entry_doc_id(row: dict[str, Any]) -> int:
    try:
        return max(0, int(row.get("doc_id") or 0))
    except TypeError, ValueError:
        return 0


def _unique_prior_entries(
    *,
    rows: list[dict[str, Any]],
    seen_entries: set[str],
    source_doc_ids: set[int],
    stats: dict[str, Any],
) -> list[tuple[int, str]]:
    entries: list[tuple[int, str]] = []
    for row in rows:
        compact, text_truncated = _compact_prior_idea_entry(row.get("text"))
        entry_key = compact.casefold()
        if not compact or entry_key in seen_entries:
            continue
        seen_entries.add(entry_key)
        stats["entry_text_truncated_total"] += int(text_truncated)
        doc_id = _prior_entry_doc_id(row)
        if doc_id > 0:
            source_doc_ids.add(doc_id)
        entries.append((doc_id, compact))
    return entries


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
        rows = _bounded_prior_rows(
            repository=repository,
            section=section,
            stats=stats,
        )
        entries = _unique_prior_entries(
            rows=rows,
            seen_entries=seen_entries,
            source_doc_ids=source_doc_ids,
            stats=stats,
        )
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
]
