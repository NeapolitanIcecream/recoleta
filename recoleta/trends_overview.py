from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
import json
import re
from typing import Any

from recoleta.item_summary import extract_item_summary_sections
from recoleta.publish.trend_render_shared import (
    clamp_trend_overview_markdown,
    sanitize_trend_title,
)

@dataclass(slots=True)
class BuildOverviewPackRequest:
    repository: Any
    plan: Any
    overview_pack_max_chars: int
    item_overview_top_k: int
    item_overview_item_max_chars: int
    min_relevance_score: float = 0.0


def coerce_build_overview_pack_request(
    *, request: BuildOverviewPackRequest | None = None, legacy_kwargs: dict[str, Any]
) -> BuildOverviewPackRequest:
    if request is not None:
        return request
    return BuildOverviewPackRequest(
        repository=legacy_kwargs["repository"],
        plan=legacy_kwargs["plan"],
        overview_pack_max_chars=int(legacy_kwargs["overview_pack_max_chars"]),
        item_overview_top_k=int(legacy_kwargs["item_overview_top_k"]),
        item_overview_item_max_chars=int(legacy_kwargs["item_overview_item_max_chars"]),
        min_relevance_score=float(legacy_kwargs.get("min_relevance_score", 0.0)),
    )


def _to_utc_datetime(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def _sanitize_inline_text(value: str) -> str:
    normalized = str(value or "")
    normalized = normalized.replace("\r\n", "\n").replace("\r", "\n")
    normalized = normalized.replace("\n", " ").strip()
    if not normalized:
        return ""
    normalized = " ".join(normalized.split())
    return normalized.replace("|", "\\|")


def _extract_markdown_links(value: str, *, limit: int) -> list[str]:
    links: list[str] = []
    seen: set[str] = set()
    for title, url in re.findall(r"\[([^\]]+)\]\((https?://[^)]+)\)", str(value or "")):
        normalized = f"[{title}]({url})"
        if normalized in seen:
            continue
        seen.add(normalized)
        links.append(normalized)
        if len(links) >= limit:
            break
    return links


def _truncate_chars(value: str, *, max_chars: int) -> tuple[str, bool]:
    cap = int(max_chars)
    if cap <= 0:
        return "", bool(value)
    if len(value) <= cap:
        return value, False
    return value[:cap], True


def _allocate_field_chars(values: list[str], *, max_chars: int) -> list[int]:
    """Distribute a shared character budget without starving shorter fields."""

    allocations = [0] * len(values)
    remaining = max(0, int(max_chars))
    active = [index for index, value in enumerate(values) if value]
    while remaining > 0 and active:
        share = max(1, remaining // len(active))
        next_active: list[int] = []
        for index in active:
            if remaining <= 0:
                break
            available = len(values[index]) - allocations[index]
            take = min(available, share, remaining)
            allocations[index] += take
            remaining -= take
            if allocations[index] < len(values[index]):
                next_active.append(index)
        active = next_active
    return allocations


def _bounded_field_value(value: str, *, allocated_chars: int) -> tuple[str, bool]:
    cap = max(0, int(allocated_chars))
    if len(value) <= cap:
        return value, False
    if cap <= 0:
        return "", bool(value)
    if cap == 1:
        return "…", True
    return f"{value[: cap - 1]}…", True


def _markdown_units(lines: list[str]) -> list[tuple[list[str], bool]]:
    """Group heading-led entries while keeping preamble lines independently usable."""

    units: list[tuple[list[str], bool]] = []
    entry_lines: list[str] = []
    for line in lines:
        if line.startswith("### "):
            if entry_lines:
                units.append((entry_lines, True))
            entry_lines = [line]
            continue
        if entry_lines:
            entry_lines.append(line)
        else:
            units.append(([line], False))
    if entry_lines:
        units.append((entry_lines, True))
    return units


def _render_complete_markdown(
    lines: list[str], *, max_chars: int
) -> tuple[str, bool, int, int]:
    """Render only complete lines and heading-led entries within the hard cap."""

    units = _markdown_units(lines)
    entry_total = sum(1 for _, is_entry in units if is_entry)
    entry_included = 0
    rendered: list[str] = []
    rendered_chars = 0
    cap = max(0, int(max_chars))
    for unit_lines, is_entry in units:
        unit = "\n".join(unit_lines).rstrip() + "\n"
        if rendered_chars + len(unit) > cap:
            break
        rendered.append(unit)
        rendered_chars += len(unit)
        if is_entry:
            entry_included += 1
    return (
        "".join(rendered),
        len(rendered) < len(units),
        entry_total,
        entry_included,
    )


def _cluster_name(cluster: dict[str, Any]) -> str:
    return _sanitize_inline_text(str(cluster.get("title") or "").strip())


def _representative_record(
    *, repository: Any, rep: dict[str, Any]
) -> tuple[int, str] | None:
    try:
        rep_doc_id = int(rep.get("doc_id") or 0)
    except Exception:
        return None
    if rep_doc_id <= 0:
        return None
    rep_doc = repository.get_document(doc_id=rep_doc_id)
    if rep_doc is None:
        return None
    rep_title = str(getattr(rep_doc, "title", "") or "").strip()
    rep_url = str(getattr(rep_doc, "canonical_url", "") or "").strip()
    if not rep_title or not rep_url:
        return None
    return rep_doc_id, f"[{rep_title}]({rep_url})"


def _representative_records_for_cluster(
    *,
    repository: Any,
    cluster: dict[str, Any],
) -> list[tuple[int, str]]:
    reps = cluster.get("evidence_refs") or []
    if not isinstance(reps, list):
        return []
    records: list[tuple[int, str]] = []
    for rep in reps:
        if not isinstance(rep, dict):
            continue
        record = _representative_record(repository=repository, rep=rep)
        if record is not None:
            records.append(record)
    return records


def _representative_records_and_clusters(
    *,
    repository: Any,
    clusters: Any,
) -> tuple[list[tuple[int, str]], list[str]]:
    if not isinstance(clusters, list):
        return [], []
    normalized_clusters = [cluster for cluster in clusters if isinstance(cluster, dict)]
    cluster_names = _dedup_strings(
        _cluster_name(cluster) for cluster in normalized_clusters
    )
    representative_records = [
        record
        for cluster in normalized_clusters
        for record in _representative_records_for_cluster(
            repository=repository,
            cluster=cluster,
        )
    ]
    return representative_records, cluster_names


def _dedup_strings(values: Any) -> list[str]:
    deduped: list[str] = []
    seen: set[str] = set()
    for value in values:
        normalized = str(value or "").strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        deduped.append(normalized)
    return deduped


def _summary_lines_from_meta_chunk(
    *,
    repository: Any,
    doc: Any,
    heading: str,
    meta_chunk: Any,
) -> list[str] | None:
    try:
        payload = json.loads(str(getattr(meta_chunk, "text", "") or ""))
    except Exception:
        payload = None
    if not isinstance(payload, dict):
        return None

    title = sanitize_trend_title(
        str(payload.get("title") or getattr(doc, "title", "") or "").strip(),
        fallback="Trend",
    )
    overview_md = clamp_trend_overview_markdown(
        str(payload.get("overview_md") or "").strip()
    )
    representative_records, cluster_names = _representative_records_and_clusters(
        repository=repository,
        clusters=payload.get("clusters") or [],
    )
    lines = [heading, "- status=ok", f"- title={_sanitize_inline_text(title)}"]
    if overview_md:
        overview_text, _ = _truncate_chars(
            _sanitize_inline_text(overview_md),
            max_chars=280,
        )
        lines.append(f"- overview={overview_text}")
    for link in _extract_markdown_links(overview_md, limit=3):
        lines.append(f"- must_read={link}")
    for cluster_name in cluster_names[:3]:
        lines.append(f"- cluster={cluster_name}")
    seen_representative_doc_ids: set[int] = set()
    for representative_doc_id, representative_link in representative_records:
        if representative_doc_id in seen_representative_doc_ids:
            continue
        seen_representative_doc_ids.add(representative_doc_id)
        lines.append(
            f"- representative_doc_id={representative_doc_id} | "
            f"representative={representative_link}"
        )
        if len(seen_representative_doc_ids) >= 3:
            break
    return lines


def trend_payload_summary_lines_impl(
    *,
    repository: Any,
    doc: Any,
    token: str,
    entry_label: str,
) -> list[str]:
    doc_id = int(getattr(doc, "id", 0) or 0)
    heading = f"### {entry_label} {token}"
    if doc_id <= 0:
        return [heading, "- status=missing"]

    meta_chunk = repository.read_document_chunk(doc_id=doc_id, chunk_index=1)
    if meta_chunk is not None:
        meta_lines = _summary_lines_from_meta_chunk(
            repository=repository,
            doc=doc,
            heading=heading,
            meta_chunk=meta_chunk,
        )
        if meta_lines is not None:
            return meta_lines

    chunk = repository.read_document_chunk(doc_id=doc_id, chunk_index=0)
    if chunk is None:
        return [heading, "- status=missing_chunk"]
    overview = _sanitize_inline_text(str(getattr(chunk, "text", "") or ""))
    if not overview:
        return [heading, "- status=empty"]
    return [
        heading,
        "- status=summary_fallback",
        f"- title={_sanitize_inline_text(sanitize_trend_title(str(getattr(doc, 'title', '') or '').strip(), fallback='Trend'))}",
        f"- overview={overview}",
    ]


def _item_meta_payload(row: dict[str, Any]) -> dict[str, Any] | None:
    try:
        payload = json.loads(str(row.get("text") or ""))
    except Exception:
        return None
    return payload if isinstance(payload, dict) else None


def _meta_relevance_score(payload: dict[str, Any]) -> float:
    raw = payload.get("relevance_score", 0.0)
    try:
        return float(raw)
    except Exception:
        return 0.0


def _meta_novelty_score(payload: dict[str, Any]) -> float:
    raw = payload.get("novelty_score", None)
    if raw is None:
        return -1.0
    try:
        return float(raw)
    except Exception:
        return -1.0


def _trend_overview_lines(
    *,
    request: BuildOverviewPackRequest,
    period_start: datetime,
    period_end: datetime,
) -> list[str]:
    prev_level = str(getattr(request.plan, "prev_level", "") or "").strip().lower()
    lines = [f"- prev_level={prev_level}"]
    docs = request.repository.list_documents(
        doc_type="trend",
        granularity=prev_level or None,
        period_start=period_start,
        period_end=period_end,
        order_by="event_asc",
        limit=500,
    )
    if _is_week_day_overview(request=request, prev_level=prev_level):
        docs_by_start = _docs_by_period_start(docs)
        lines.extend(
            _week_day_overview_lines(
                repository=request.repository,
                docs_by_start=docs_by_start,
                period_start=period_start,
            )
        )
        return lines
    lines.extend(
        _listed_trend_overview_lines(
            repository=request.repository,
            docs=docs,
            entry_label=prev_level or "trend",
        )
    )
    if docs:
        return lines
    lines.extend([f"### {prev_level or 'trend'} -", "- status=missing"])
    return lines


def _docs_by_period_start(docs: list[Any]) -> dict[datetime, Any]:
    docs_by_start: dict[datetime, Any] = {}
    for doc in docs:
        raw_start = getattr(doc, "period_start", None)
        if isinstance(raw_start, datetime):
            docs_by_start[_to_utc_datetime(raw_start)] = doc
    return docs_by_start


def _is_week_day_overview(
    *,
    request: BuildOverviewPackRequest,
    prev_level: str,
) -> bool:
    target_granularity = (
        str(getattr(request.plan, "target_granularity", "") or "").strip().lower()
    )
    return target_granularity == "week" and prev_level == "day"


def _week_day_overview_lines(
    *,
    repository: Any,
    docs_by_start: dict[datetime, Any],
    period_start: datetime,
) -> list[str]:
    lines: list[str] = []
    for i in range(7):
        day_start = _to_utc_datetime(period_start + timedelta(days=i))
        token = day_start.date().isoformat()
        doc = docs_by_start.get(day_start)
        if doc is None:
            lines.extend([f"### day {token}", "- status=missing"])
            continue
        lines.extend(
            trend_payload_summary_lines_impl(
                repository=repository,
                doc=doc,
                token=token,
                entry_label="day",
            )
        )
    return lines


def _listed_trend_overview_lines(
    *,
    repository: Any,
    docs: list[Any],
    entry_label: str,
) -> list[str]:
    lines: list[str] = []
    for doc in docs:
        raw_start = getattr(doc, "period_start", None)
        start = _to_utc_datetime(raw_start) if isinstance(raw_start, datetime) else None
        token = start.date().isoformat() if isinstance(start, datetime) else "-"
        lines.extend(
            trend_payload_summary_lines_impl(
                repository=repository,
                doc=doc,
                token=token,
                entry_label=entry_label,
            )
        )
    return lines


def _selection_key_from_meta(payload: dict[str, Any], *, doc_id: int) -> tuple[str, str]:
    url = str(payload.get("canonical_url") or "").strip()
    if url:
        return ("url", url)
    raw_item_id = payload.get("item_id")
    try:
        item_id = int(raw_item_id or 0)
    except Exception:
        item_id = 0
    if item_id > 0:
        return ("item_id", str(item_id))
    return ("doc_id", str(doc_id))


def _item_candidate_limit(top_k: int) -> int:
    return max(0, min(2000, max(50, top_k * 25)))


def _item_summary_rows_by_doc_id(
    summary_rows: list[dict[str, Any]],
) -> dict[int, dict[str, Any]]:
    rows_by_doc_id: dict[int, dict[str, Any]] = {}
    for row in summary_rows:
        try:
            doc_id = int(row.get("doc_id") or 0)
        except Exception:
            continue
        if doc_id > 0:
            rows_by_doc_id[doc_id] = row
    return rows_by_doc_id


def _item_candidate_from_rows(
    *,
    row: dict[str, Any],
    summary_row: dict[str, Any] | None,
    min_relevance_score: float,
) -> tuple[dict[str, Any] | None, bool]:
    if summary_row is None:
        return None, False
    try:
        doc_id = int(row.get("doc_id") or 0)
    except Exception:
        return None, False
    if doc_id <= 0:
        return None, False
    payload = _item_meta_payload(row)
    if payload is None:
        return None, False
    relevance_score = _meta_relevance_score(payload)
    if relevance_score < min_relevance_score:
        return None, True
    return (
        {
            "doc_id": doc_id,
            "meta": payload,
            "summary_text": str(summary_row.get("text") or ""),
            "relevance_score": relevance_score,
            "novelty_score": _meta_novelty_score(payload),
            "event_start_ts": float(row.get("event_start_ts") or 0.0),
        },
        False,
    )


def _item_candidates_and_filtered_total(
    *,
    meta_rows: list[dict[str, Any]],
    summary_rows_by_doc_id: dict[int, dict[str, Any]],
    min_relevance_score: float,
) -> tuple[list[dict[str, Any]], int]:
    candidates: list[dict[str, Any]] = []
    filtered_out_total = 0
    for row in meta_rows:
        try:
            doc_id = int(row.get("doc_id") or 0)
        except Exception:
            continue
        candidate, filtered_out = _item_candidate_from_rows(
            row=row,
            summary_row=summary_rows_by_doc_id.get(doc_id),
            min_relevance_score=min_relevance_score,
        )
        if filtered_out:
            filtered_out_total += 1
        if candidate is not None:
            candidates.append(candidate)
    return candidates, filtered_out_total


def _sorted_item_candidates(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        candidates,
        key=lambda candidate: (
            -float(candidate["relevance_score"]),
            -float(candidate["novelty_score"]),
            -float(candidate["event_start_ts"]),
            -int(candidate["doc_id"]),
        ),
    )


def _select_item_candidates(
    *,
    sorted_candidates: list[dict[str, Any]],
    top_k: int,
) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    seen_selection_keys: set[tuple[str, str]] = set()
    for candidate in sorted_candidates:
        key = _selection_key_from_meta(candidate["meta"], doc_id=int(candidate["doc_id"]))
        if key in seen_selection_keys:
            continue
        seen_selection_keys.add(key)
        selected.append(candidate)
        if len(selected) >= top_k:
            break
    return selected


def _item_candidate_lines(
    *,
    rank: int,
    candidate: dict[str, Any],
    item_max_chars: int,
) -> tuple[list[str], bool]:
    payload = candidate["meta"]
    title = _sanitize_inline_text(str(payload.get("title") or "")) or "(untitled)"
    url = _sanitize_inline_text(str(payload.get("canonical_url") or "")) or "-"
    sections = extract_item_summary_sections(str(candidate["summary_text"] or ""))
    field_names = ["title", "url", "summary", "problem", "approach", "results"]
    field_values = [
        title,
        url,
        *[
            _sanitize_inline_text(str(sections.get(field_name) or ""))
            for field_name in field_names[2:]
        ],
    ]
    fixed_lines = [
        f"### item rank={rank}",
        f"- doc_id={int(candidate['doc_id'])} | chunk_index=0",
        *[f"- {field_name}=" for field_name in field_names],
    ]
    fixed_chars = len("\n".join(fixed_lines).rstrip() + "\n")
    if fixed_chars > item_max_chars:
        return [], True

    available_chars = item_max_chars - fixed_chars
    metadata_values = field_values[:2]
    metadata_budget_values = [
        value[:preferred_cap]
        for value, preferred_cap in zip(metadata_values, (96, 240), strict=True)
    ]
    metadata_allocations = _allocate_field_chars(
        metadata_budget_values,
        max_chars=available_chars,
    )
    remaining_chars = available_chars - sum(metadata_allocations)
    summary_allocations = _allocate_field_chars(
        field_values[2:],
        max_chars=remaining_chars,
    )
    allocations = [*metadata_allocations, *summary_allocations]
    bounded_values: list[str] = []
    truncated = False
    for value, allocation in zip(field_values, allocations, strict=True):
        bounded_value, field_truncated = _bounded_field_value(
            value,
            allocated_chars=allocation,
        )
        bounded_values.append(bounded_value)
        truncated = truncated or field_truncated
    lines = [
        fixed_lines[0],
        fixed_lines[1],
        *[
            f"- {field_name}={field_value}"
            for field_name, field_value in zip(
                field_names,
                bounded_values,
                strict=True,
            )
        ],
    ]
    return lines, truncated


def _item_top_k_lines(
    *,
    request: BuildOverviewPackRequest,
    period_start: datetime,
    period_end: datetime,
    stats: dict[str, Any],
) -> list[str]:
    top_k = max(0, int(request.item_overview_top_k))
    item_max_chars = max(0, int(request.item_overview_item_max_chars))
    stats["item_max_chars"] = item_max_chars
    if top_k <= 0:
        stats["item_selected_total"] = 0
        stats["item_rendered_total"] = 0
        stats["item_budget_dropped_total"] = 0
        stats["item_truncated_total"] = 0
        return ["- items_total=0 | selected=0"]
    candidate_limit = _item_candidate_limit(top_k)
    summary_rows = request.repository.list_document_chunk_index_rows_in_period(
        period_start=period_start,
        period_end=period_end,
        doc_type="item",
        kind="summary",
        limit=candidate_limit,
    )
    meta_rows = request.repository.list_document_chunk_index_rows_in_period(
        period_start=period_start,
        period_end=period_end,
        doc_type="item",
        kind="meta",
        limit=candidate_limit,
    )
    summary_rows_by_doc_id = _item_summary_rows_by_doc_id(summary_rows)
    candidates, filtered_out_total = _item_candidates_and_filtered_total(
        meta_rows=meta_rows,
        summary_rows_by_doc_id=summary_rows_by_doc_id,
        min_relevance_score=float(request.min_relevance_score or 0.0),
    )
    stats["filtered_out_total"] = filtered_out_total
    selected = _select_item_candidates(
        sorted_candidates=_sorted_item_candidates(candidates),
        top_k=top_k,
    )
    lines = [
        f"- items_total={len(candidates)} | selected={len(selected)} | top_k={top_k}"
    ]
    item_budget_dropped_total = 0
    item_truncated_total = 0
    for rank, candidate in enumerate(selected, start=1):
        item_lines, item_truncated = _item_candidate_lines(
            rank=rank,
            candidate=candidate,
            item_max_chars=item_max_chars,
        )
        if not item_lines:
            item_budget_dropped_total += 1
            continue
        item_truncated_total += int(item_truncated)
        lines.extend(item_lines)
    stats["item_selected_total"] = len(selected)
    stats["item_rendered_total"] = len(selected) - item_budget_dropped_total
    stats["item_budget_dropped_total"] = item_budget_dropped_total
    stats["item_truncated_total"] = item_truncated_total
    return lines


def build_overview_pack_md_impl(
    *,
    request: BuildOverviewPackRequest,
) -> tuple[str, dict[str, Any]]:
    strategy = (
        str(getattr(request.plan, "overview_pack_strategy", "") or "").strip().lower()
    )
    stats: dict[str, Any] = {"strategy": strategy, "truncated": False}
    period_start = _to_utc_datetime(request.plan.period_start)
    period_end = _to_utc_datetime(request.plan.period_end)
    lines = [
        f"## Overview pack (strategy={strategy})",
        f"- period_start={period_start.isoformat()} | period_end={period_end.isoformat()}",
    ]
    if strategy == "trend_overviews":
        lines.extend(
            _trend_overview_lines(
                request=request,
                period_start=period_start,
                period_end=period_end,
            )
        )
    elif strategy == "item_top_k":
        lines.extend(
            _item_top_k_lines(
                request=request,
                period_start=period_start,
                period_end=period_end,
                stats=stats,
            )
        )
    else:
        lines.append(f"- unsupported_strategy={strategy or '(empty)'}")
    md, truncated, entries_total, entries_included = _render_complete_markdown(
        lines,
        max_chars=request.overview_pack_max_chars,
    )
    stats["truncated"] = bool(truncated)
    stats["chars"] = len(md)
    stats["max_chars"] = int(request.overview_pack_max_chars)
    stats["entries_total"] = entries_total
    stats["entries_included"] = entries_included
    stats["entries_dropped"] = entries_total - entries_included
    return md, stats
