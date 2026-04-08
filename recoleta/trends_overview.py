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

_HISTORY_WINDOW_ID_RE = re.compile(r"\bprev_\d+\b", flags=re.IGNORECASE)
_HISTORY_WINDOW_TRIM_CHARS = " \t\r\n()[]{}<>.,;:!?\"'`，；：。！？"


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


def _summary_field_line(
    sections: dict[str, str],
    *,
    field_name: str,
    max_chars: int,
) -> str:
    raw = _sanitize_inline_text(str(sections.get(field_name) or ""))
    if max_chars > 0:
        raw = raw[:max_chars]
    return raw


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


def _normalize_history_window_alias(value: Any) -> str:
    return " ".join(str(value or "").split()).strip().lower()


def _trim_history_window_candidate(value: Any) -> str:
    return str(value or "").strip(_HISTORY_WINDOW_TRIM_CHARS)


def _split_history_window_candidates(raw_values: list[str]) -> list[str]:
    candidates: list[str] = []
    for raw in raw_values:
        normalized = " ".join(str(raw or "").split()).strip()
        if not normalized:
            continue
        parts = re.split(r"[,/|;，；]+", normalized)
        if len(parts) == 1:
            candidates.append(normalized)
            continue
        for part in parts:
            candidate = part.strip()
            if candidate:
                candidates.append(candidate)
    return candidates


def _window_alias_lookup(
    *, history_windows: list[Any], available_window_ids: set[str] | None
) -> tuple[dict[str, str], set[str]]:
    alias_to_window_id: dict[str, str] = {}
    allowed_window_ids = {
        str(window.window_id).strip()
        for window in history_windows
        if str(window.window_id).strip()
    }
    if available_window_ids is not None:
        allowed_window_ids &= {
            str(window_id).strip()
            for window_id in available_window_ids
            if str(window_id).strip()
        }
    for window in history_windows:
        window_id = str(window.window_id).strip()
        if not window_id:
            continue
        for alias in {window_id, window.label}:
            normalized_alias = _normalize_history_window_alias(alias)
            if normalized_alias:
                alias_to_window_id.setdefault(normalized_alias, window_id)
    return alias_to_window_id, allowed_window_ids


def _mapped_history_window_id(
    *,
    normalized_candidate: str,
    alias_to_window_id: dict[str, str],
    allowed_window_ids: set[str],
) -> tuple[str | None, bool]:
    direct_match = _HISTORY_WINDOW_ID_RE.search(normalized_candidate)
    if direct_match is not None:
        candidate_window_id = direct_match.group(0).lower()
        if candidate_window_id in allowed_window_ids:
            return candidate_window_id, False
        return None, False
    candidate_window_id = alias_to_window_id.get(normalized_candidate)
    if candidate_window_id is None or candidate_window_id not in allowed_window_ids:
        return None, False
    return candidate_window_id, candidate_window_id != normalized_candidate


def _normalized_history_windows_for_signal(
    *,
    signal: Any,
    alias_to_window_id: dict[str, str],
    allowed_window_ids: set[str],
    current_period_token: str,
    stats: dict[str, int],
) -> list[str]:
    normalized_history_windows: list[str] = []
    seen_history_windows: set[str] = set()
    for candidate in _split_history_window_candidates(
        list(signal.history_windows or [])
    ):
        normalized_candidate = _normalized_history_window_candidate(
            candidate=candidate,
            current_period_token=current_period_token,
            stats=stats,
        )
        if not normalized_candidate:
            continue
        mapped_window_id, was_normalized = _mapped_history_window_id(
            normalized_candidate=normalized_candidate,
            alias_to_window_id=alias_to_window_id,
            allowed_window_ids=allowed_window_ids,
        )
        if mapped_window_id is None:
            stats["history_windows_dropped_total"] += 1
            continue
        if was_normalized:
            stats["history_windows_normalized_total"] += 1
        if mapped_window_id in seen_history_windows:
            continue
        seen_history_windows.add(mapped_window_id)
        normalized_history_windows.append(mapped_window_id)
    return normalized_history_windows


def _normalized_history_window_candidate(
    *,
    candidate: Any,
    current_period_token: str,
    stats: dict[str, int],
) -> str | None:
    normalized_candidate = _normalize_history_window_alias(
        _trim_history_window_candidate(candidate)
    )
    if not normalized_candidate:
        return None
    if normalized_candidate == current_period_token:
        stats["history_windows_dropped_total"] += 1
        return None
    return normalized_candidate


def normalize_trend_evolution_impl(
    evolution: Any,
    *,
    granularity: str,
    period_start: datetime,
    history_windows: list[Any] | None,
    available_window_ids: set[str] | None = None,
) -> tuple[Any | None, dict[str, int]]:
    from recoleta import trends as trends_module

    stats = {
        "history_windows_normalized_total": 0,
        "history_windows_dropped_total": 0,
        "signals_dropped_total": 0,
    }
    if evolution is None:
        return None, stats

    all_windows = list(history_windows or [])
    alias_to_window_id, allowed_window_ids = _window_alias_lookup(
        history_windows=all_windows,
        available_window_ids=available_window_ids,
    )
    current_period_token = _normalize_history_window_alias(
        trends_module._period_token_for_granularity(granularity, period_start)
    )

    normalized_signals: list[Any] = []
    for signal in evolution.signals or []:
        normalized_history_windows = _normalized_history_windows_for_signal(
            signal=signal,
            alias_to_window_id=alias_to_window_id,
            allowed_window_ids=allowed_window_ids,
            current_period_token=current_period_token,
            stats=stats,
        )
        if allowed_window_ids and not normalized_history_windows:
            stats["signals_dropped_total"] += 1
            continue
        normalized_signals.append(
            trends_module.TrendEvolutionSignal(
                theme=str(signal.theme or "").strip(),
                change_type=signal.change_type,
                summary=str(signal.summary or "").strip(),
                history_windows=normalized_history_windows,
            )
        )

    summary_md = str(evolution.summary_md or "").strip()
    if not summary_md and not normalized_signals:
        return None, stats
    return (
        trends_module.TrendEvolutionSection(
            summary_md=summary_md,
            signals=normalized_signals,
        ),
        stats,
    )


def _cluster_name(cluster: dict[str, Any]) -> str:
    return _sanitize_inline_text(str(cluster.get("title") or "").strip())


def _representative_link(*, repository: Any, rep: dict[str, Any]) -> str | None:
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
    return f"[{rep_title}]({rep_url})"


def _representative_links_for_cluster(
    *,
    repository: Any,
    cluster: dict[str, Any],
) -> list[str]:
    reps = cluster.get("evidence_refs") or []
    if not isinstance(reps, list):
        return []
    links: list[str] = []
    for rep in reps:
        if not isinstance(rep, dict):
            continue
        link = _representative_link(repository=repository, rep=rep)
        if link is not None:
            links.append(link)
    return links


def _representative_links_and_clusters(
    *,
    repository: Any,
    clusters: Any,
) -> tuple[list[str], list[str]]:
    if not isinstance(clusters, list):
        return [], []
    normalized_clusters = [cluster for cluster in clusters if isinstance(cluster, dict)]
    cluster_names = _dedup_strings(
        _cluster_name(cluster) for cluster in normalized_clusters
    )
    representative_links = [
        link
        for cluster in normalized_clusters
        for link in _representative_links_for_cluster(
            repository=repository,
            cluster=cluster,
        )
    ]
    return representative_links, cluster_names


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
    representative_links, cluster_names = _representative_links_and_clusters(
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
    seen_representatives: set[str] = set()
    for representative_link in representative_links:
        if representative_link in seen_representatives:
            continue
        seen_representatives.add(representative_link)
        lines.append(f"- representative={representative_link}")
        if len(seen_representatives) >= 3:
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
) -> list[str]:
    payload = candidate["meta"]
    title = _sanitize_inline_text(str(payload.get("title") or "")) or "(untitled)"
    url = _sanitize_inline_text(str(payload.get("canonical_url") or "")) or "-"
    sections = extract_item_summary_sections(str(candidate["summary_text"] or ""))
    return [
        f"### item rank={rank}",
        f"- title={title}",
        f"- url={url}",
        f"- summary={_summary_field_line(sections, field_name='summary', max_chars=item_max_chars)}",
        f"- problem={_summary_field_line(sections, field_name='problem', max_chars=item_max_chars)}",
        f"- approach={_summary_field_line(sections, field_name='approach', max_chars=item_max_chars)}",
        f"- results={_summary_field_line(sections, field_name='results', max_chars=item_max_chars)}",
    ]


def _item_top_k_lines(
    *,
    request: BuildOverviewPackRequest,
    period_start: datetime,
    period_end: datetime,
    stats: dict[str, Any],
) -> list[str]:
    top_k = max(0, int(request.item_overview_top_k))
    item_max_chars = max(0, int(request.item_overview_item_max_chars))
    if top_k <= 0:
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
    for rank, candidate in enumerate(selected, start=1):
        lines.extend(
            _item_candidate_lines(
                rank=rank,
                candidate=candidate,
                item_max_chars=item_max_chars,
            )
        )
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
    md = "\n".join(lines).rstrip() + "\n"
    md, truncated = _truncate_chars(md, max_chars=request.overview_pack_max_chars)
    stats["truncated"] = bool(truncated)
    stats["chars"] = len(md)
    stats["max_chars"] = int(request.overview_pack_max_chars)
    return md, stats
