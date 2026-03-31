from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import re
from typing import Any

from recoleta.publish.item_notes import resolve_item_note_href
from recoleta.publish.trend_render_shared import (
    clamp_trend_overview_markdown,
    sanitize_trend_title,
)
from recoleta.trends import (
    TrendPayload,
    peer_history_windows_for_period,
)


@dataclass(slots=True)
class TrendNoteRewriteStats:
    doc_ref_occurrences_total: int = 0
    doc_ref_resolved_total: int = 0
    doc_ref_unresolved_total: int = 0
    canonical_link_rewrites_total: int = 0


@dataclass(slots=True)
class MaterializedTrendNotePayload:
    title: str
    overview_md: str
    topics: list[str]
    evolution: dict[str, Any] | None
    history_window_refs: dict[str, dict[str, Any]]
    clusters: list[dict[str, Any]]
    highlights: list[str]
    rewrite_stats: TrendNoteRewriteStats


_DOC_REF_PATTERN = re.compile(
    r"\bdoc_id\s*(?:[:=#-]\s*|\s+)([0-9][0-9,\s]*)\b",
    re.IGNORECASE,
)
_DOC_SHORT_PATTERN = re.compile(
    r"\bdoc\s*(?:[:=#-]\s*|\s+)(\d+)\b",
    re.IGNORECASE,
)
_CHUNK_SUFFIX_PATTERN = re.compile(
    r"\s*[,;，；]?\s*chunk(?:_index)?\s*(?:[:=]\s*|\s+)\d+",
    re.IGNORECASE,
)
_MARKDOWN_LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_HISTORY_WINDOW_ID_PATTERN = re.compile(r"\b(prev_\d+)\b", re.IGNORECASE)


def _parse_authors(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(a).strip() for a in value if str(a).strip()]
    if isinstance(value, str):
        raw = value.strip()
        if not raw:
            return []
        try:
            loaded = json.loads(raw)
        except Exception:
            return []
        if isinstance(loaded, list):
            return [str(a).strip() for a in loaded if str(a).strip()]
    return []


def _citation_label_from_title(raw_title: str) -> str:
    normalized = " ".join(str(raw_title or "").split()).strip()
    if not normalized:
        return "Paper"
    normalized = normalized.replace("[", "(").replace("]", ")")
    for separator in (":", "："):
        if separator in normalized:
            prefix = normalized.split(separator, 1)[0].strip()
            if 2 <= len(prefix) <= 40:
                normalized = prefix
                break
    if len(normalized) > 60:
        normalized = normalized[:60].rstrip() + "…"
    return normalized


def _history_window_title_label(raw_title: str) -> str:
    normalized = " ".join(str(raw_title or "").split()).strip()
    if not normalized:
        return ""
    normalized = normalized.replace("[", "(").replace("]", ")")
    for separator in (":", "："):
        if separator in normalized:
            prefix = normalized.split(separator, 1)[0].strip()
            if 2 <= len(prefix) <= 40:
                normalized = prefix
                break
    if len(normalized) > 48:
        normalized = normalized[:48].rstrip() + "…"
    return normalized


def _split_markdown_link_target(target: str) -> tuple[str, str]:
    stripped = str(target or "").strip()
    if not stripped:
        return "", ""
    if " " not in stripped:
        return stripped, ""
    url, suffix = stripped.split(" ", 1)
    return url.strip(), suffix.strip()


def materialize_trend_note_payload(
    *,
    repository: Any,
    payload: TrendPayload,
    markdown_output_dir: Path,
    output_language: str | None,
    language_code: str | None = None,
    item_note_href_by_url: dict[str, str] | None = None,
) -> MaterializedTrendNotePayload:
    doc_cache: dict[int, Any | None] = {}
    item_cache: dict[int, Any | None] = {}
    note_href_by_url = {
        str(url).strip(): str(href).strip()
        for url, href in (item_note_href_by_url or {}).items()
        if str(url).strip() and str(href).strip()
    }
    stats = TrendNoteRewriteStats()
    history_window_refs: dict[str, dict[str, Any]] = {}
    try:
        current_period_start = datetime.fromisoformat(str(payload.period_start))
    except Exception:
        current_period_start = None

    def _get_doc(doc_id_value: int) -> Any | None:
        if doc_id_value not in doc_cache:
            doc_cache[doc_id_value] = repository.get_document(doc_id=doc_id_value)
        return doc_cache[doc_id_value]

    def _localized_trend_title_for_doc(doc_id_value: int) -> str | None:
        normalized_language_code = str(language_code or "").strip()
        if not normalized_language_code:
            return None
        localized_output = repository.get_localized_output(
            source_kind="trend_synthesis",
            source_record_id=doc_id_value,
            language_code=normalized_language_code,
        )
        if localized_output is None:
            return None
        try:
            localized_payload = json.loads(
                str(getattr(localized_output, "payload_json", "") or "{}")
            )
        except Exception:
            return None
        if not isinstance(localized_payload, dict):
            return None
        localized_title = str(localized_payload.get("title") or "").strip()
        return localized_title or None

    def _item_note_href_for_doc(doc: Any) -> str | None:
        doc_type = str(getattr(doc, "doc_type", "") or "").strip().lower()
        if doc_type != "item":
            return None
        raw_item_id = getattr(doc, "item_id", None)
        try:
            item_id_int = int(raw_item_id) if raw_item_id is not None else 0
        except Exception:
            item_id_int = 0
        if item_id_int <= 0:
            return None
        if item_id_int not in item_cache:
            item_cache[item_id_int] = repository.get_item(item_id=item_id_int)
        item = item_cache.get(item_id_int)
        if item is None:
            return None
        href = resolve_item_note_href(
            note_dir=markdown_output_dir / "Inbox",
            from_dir=markdown_output_dir / "Trends",
            item_id=item_id_int,
            title=str(getattr(item, "title", "") or ""),
            canonical_url=str(getattr(item, "canonical_url", "") or ""),
            published_at=getattr(item, "published_at", None),
        )
        canonical_url = str(getattr(item, "canonical_url", "") or "").strip()
        if canonical_url:
            note_href_by_url.setdefault(canonical_url, href)
        return href

    def _citation_for_doc_id(doc_id_value: int) -> str | None:
        doc = _get_doc(doc_id_value)
        if doc is None:
            return None
        title = str(getattr(doc, "title", "") or "").strip()
        note_href = _item_note_href_for_doc(doc)
        url = str(getattr(doc, "canonical_url", "") or "").strip()
        label = _citation_label_from_title(title)
        if note_href:
            return f"[{label}]({note_href})"
        if url:
            return f"[{label}]({url})"
        return label

    def _rewrite_doc_refs(value: str) -> str:
        raw = str(value or "")
        if not raw.strip():
            return raw

        def _replace_doc_id_match(match: re.Match[str]) -> str:
            numbers = [int(x) for x in re.findall(r"\d+", match.group(1) or "")]
            seen: set[int] = set()
            doc_ids: list[int] = []
            for number in numbers:
                if number <= 0 or number in seen:
                    continue
                seen.add(number)
                doc_ids.append(number)
            if not doc_ids:
                return match.group(0)

            stats.doc_ref_occurrences_total += 1
            citations: list[str] = []
            for doc_id_inner in doc_ids:
                cite = _citation_for_doc_id(doc_id_inner)
                if cite is None:
                    stats.doc_ref_unresolved_total += 1
                    citations.append("Paper")
                else:
                    stats.doc_ref_resolved_total += 1
                    citations.append(cite)
            return "、".join(citations)

        def _replace_doc_short_match(match: re.Match[str]) -> str:
            raw_id = match.group(1) or ""
            try:
                doc_id_inner = int(raw_id)
            except Exception:
                return match.group(0)
            if doc_id_inner <= 0:
                return match.group(0)
            cite = _citation_for_doc_id(doc_id_inner)
            if cite is None:
                stats.doc_ref_unresolved_total += 1
                return match.group(0)
            stats.doc_ref_occurrences_total += 1
            stats.doc_ref_resolved_total += 1
            return cite

        rewritten = _DOC_REF_PATTERN.sub(_replace_doc_id_match, raw)
        rewritten = _DOC_SHORT_PATTERN.sub(_replace_doc_short_match, rewritten)
        return _CHUNK_SUFFIX_PATTERN.sub("", rewritten)

    def _rewrite_canonical_item_links(value: str) -> str:
        raw = str(value or "")
        if not raw.strip() or not note_href_by_url:
            return raw

        def _replace_markdown_link(match: re.Match[str]) -> str:
            label = match.group(1) or ""
            raw_target = match.group(2) or ""
            href, suffix = _split_markdown_link_target(raw_target)
            mapped_href = note_href_by_url.get(href)
            if mapped_href is None:
                return match.group(0)
            stats.canonical_link_rewrites_total += 1
            suffix_segment = f" {suffix}" if suffix else ""
            return f"[{label}]({mapped_href}{suffix_segment})"

        return _MARKDOWN_LINK_PATTERN.sub(_replace_markdown_link, raw)

    def _rewrite_text(value: str) -> str:
        return _rewrite_canonical_item_links(_rewrite_doc_refs(value))

    def _collect_history_window_refs_from_text(value: str) -> None:
        raw = str(value or "").strip()
        if not raw:
            return
        seen_window_ids: set[str] = set()
        for match in _HISTORY_WINDOW_ID_PATTERN.finditer(raw):
            window_id = str(match.group(1) or "").strip().lower()
            if not window_id or window_id in seen_window_ids:
                continue
            seen_window_ids.add(window_id)
            _history_window_ref(window_id)

    def _history_window_ref(window_id: str) -> dict[str, Any] | None:
        normalized_window_id = str(window_id or "").strip().lower()
        if not normalized_window_id or current_period_start is None:
            return None
        if normalized_window_id in history_window_refs:
            return history_window_refs[normalized_window_id]
        match = re.fullmatch(r"prev_(\d+)", normalized_window_id)
        if match is None:
            return None
        index = max(1, int(match.group(1)))
        windows = peer_history_windows_for_period(
            granularity=payload.granularity,
            period_start=current_period_start,
            window_count=index,
        )
        if len(windows) < index:
            return None
        window = windows[index - 1]
        docs = repository.list_documents(
            doc_type="trend",
            granularity=payload.granularity,
            period_start=window.period_start,
            period_end=window.period_end,
            order_by="event_desc",
            limit=1,
        )
        doc = docs[0] if docs else None
        localized_title = (
            _localized_trend_title_for_doc(int(getattr(doc, "id") or 0))
            if doc is not None
            else None
        )
        ref = {
            "window_id": window.window_id,
            "label": window.label,
            "title": (
                _history_window_title_label(
                    localized_title or str(getattr(doc, "title", "") or "")
                )
                if doc is not None
                else ""
            ),
            "granularity": payload.granularity,
            "period_start": window.period_start.isoformat(),
            "trend_doc_id": int(getattr(doc, "id") or 0) if doc is not None else 0,
        }
        history_window_refs[normalized_window_id] = ref
        return ref

    title_for_notes = sanitize_trend_title(
        _rewrite_text(str(payload.title)),
        fallback="Trend",
    )
    overview_md_for_notes = clamp_trend_overview_markdown(
        _rewrite_text(str(payload.overview_md)),
        output_language=output_language,
    )
    evolution_for_notes: dict[str, Any] | None = None
    if payload.evolution is not None:
        evolution_for_notes = payload.evolution.model_dump(mode="json")
        evolution_for_notes["summary_md"] = clamp_trend_overview_markdown(
            _rewrite_text(str(evolution_for_notes.get("summary_md") or "")),
            output_language=output_language,
        )
        _collect_history_window_refs_from_text(
            str(evolution_for_notes.get("summary_md") or "")
        )
        normalized_signals: list[dict[str, Any]] = []
        for signal in evolution_for_notes.get("signals") or []:
            if not isinstance(signal, dict):
                continue
            normalized_signal = dict(signal)
            normalized_signal["theme"] = _rewrite_text(
                str(normalized_signal.get("theme") or "").strip()
            )
            normalized_signal["summary"] = _rewrite_text(
                str(normalized_signal.get("summary") or "").strip()
            )
            _collect_history_window_refs_from_text(
                str(normalized_signal.get("summary") or "")
            )
            history_windows = normalized_signal.get("history_windows") or []
            if isinstance(history_windows, list):
                normalized_signal["history_windows"] = [
                    str(window).strip()
                    for window in history_windows
                    if str(window).strip()
                ]
                for window in normalized_signal["history_windows"]:
                    _history_window_ref(window)
            else:
                normalized_signal["history_windows"] = []
            normalized_signals.append(normalized_signal)
        evolution_for_notes["signals"] = normalized_signals
    highlights_for_notes = [
        _rewrite_text(str(highlight)) for highlight in (list(payload.highlights) or [])
    ]

    clusters_for_notes: list[dict[str, Any]] = []
    for cluster in payload.clusters or []:
        cluster_dict = cluster.model_dump(mode="json")
        cluster_dict["name"] = _rewrite_text(str(cluster_dict.get("name") or "").strip())
        cluster_dict["description"] = _rewrite_text(
            str(cluster_dict.get("description") or "").strip()
        )
        reps = cluster_dict.get("representative_chunks") or []
        enriched_reps: list[dict[str, Any]] = []
        seen_rep_doc_ids: set[int] = set()
        if isinstance(reps, list):
            for rep in reps:
                if not isinstance(rep, dict):
                    continue
                raw_doc_id = rep.get("doc_id")
                raw_chunk_index = rep.get("chunk_index")
                if raw_doc_id is None or raw_chunk_index is None:
                    continue
                try:
                    doc_id_int = int(raw_doc_id)
                    chunk_index_int = int(raw_chunk_index)
                except Exception:
                    continue
                if doc_id_int <= 0 or chunk_index_int < 0:
                    continue
                if doc_id_int in seen_rep_doc_ids:
                    continue
                seen_rep_doc_ids.add(doc_id_int)

                doc = _get_doc(doc_id_int)
                if doc is None:
                    continue
                title = str(getattr(doc, "title", "") or "").strip()
                if not title:
                    continue
                note_href = _item_note_href_for_doc(doc)
                url = str(getattr(doc, "canonical_url", "") or "").strip()
                authors: list[str] = []
                doc_type = str(getattr(doc, "doc_type", "") or "").strip().lower()
                if doc_type == "item":
                    raw_item_id = getattr(doc, "item_id", None)
                    try:
                        item_id_int = int(raw_item_id) if raw_item_id is not None else 0
                    except Exception:
                        item_id_int = 0
                    if item_id_int > 0:
                        if item_id_int not in item_cache:
                            item_cache[item_id_int] = repository.get_item(
                                item_id=item_id_int
                            )
                        item = item_cache.get(item_id_int)
                        if item is not None:
                            authors = _parse_authors(getattr(item, "authors", None))

                enriched = dict(rep)
                enriched["title"] = title
                if note_href:
                    enriched["note_href"] = note_href
                if url:
                    enriched["url"] = url
                if authors:
                    enriched["authors"] = authors
                enriched_reps.append(enriched)
        cluster_dict["representative_chunks"] = enriched_reps
        clusters_for_notes.append(cluster_dict)

    return MaterializedTrendNotePayload(
        title=title_for_notes,
        overview_md=overview_md_for_notes,
        topics=list(payload.topics),
        evolution=evolution_for_notes,
        history_window_refs=history_window_refs,
        clusters=clusters_for_notes,
        highlights=highlights_for_notes,
        rewrite_stats=stats,
    )
