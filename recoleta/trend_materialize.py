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


def _parse_period_start(value: Any) -> datetime | None:
    try:
        return datetime.fromisoformat(str(value))
    except Exception:
        return None


def _parse_positive_unique_doc_ids(raw_numbers: str) -> list[int]:
    seen: set[int] = set()
    doc_ids: list[int] = []
    for number in (int(x) for x in re.findall(r"\d+", raw_numbers or "")):
        if number <= 0 or number in seen:
            continue
        seen.add(number)
        doc_ids.append(number)
    return doc_ids


@dataclass(slots=True)
class _TrendNoteMaterializer:
    repository: Any
    payload: TrendPayload
    markdown_output_dir: Path
    output_language: str | None
    language_code: str | None
    note_href_by_url: dict[str, str]
    stats: TrendNoteRewriteStats
    doc_cache: dict[int, Any | None]
    item_cache: dict[int, Any | None]
    history_window_refs: dict[str, dict[str, Any]]
    current_period_start: datetime | None

    def get_doc(self, doc_id_value: int) -> Any | None:
        if doc_id_value not in self.doc_cache:
            self.doc_cache[doc_id_value] = self.repository.get_document(
                doc_id=doc_id_value
            )
        return self.doc_cache[doc_id_value]

    def get_item(self, item_id_value: int) -> Any | None:
        if item_id_value not in self.item_cache:
            self.item_cache[item_id_value] = self.repository.get_item(
                item_id=item_id_value
            )
        return self.item_cache[item_id_value]

    def localized_trend_title_for_doc(self, doc_id_value: int) -> str | None:
        normalized_language_code = str(self.language_code or "").strip()
        if not normalized_language_code:
            return None
        localized_output = self.repository.get_localized_output(
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

    def item_note_href_for_doc(self, doc: Any) -> str | None:
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
        item = self.get_item(item_id_int)
        if item is None:
            return None
        href = resolve_item_note_href(
            note_dir=self.markdown_output_dir / "Inbox",
            from_dir=self.markdown_output_dir / "Trends",
            item_id=item_id_int,
            title=str(getattr(item, "title", "") or ""),
            canonical_url=str(getattr(item, "canonical_url", "") or ""),
            published_at=getattr(item, "published_at", None),
        )
        canonical_url = str(getattr(item, "canonical_url", "") or "").strip()
        if canonical_url:
            self.note_href_by_url.setdefault(canonical_url, href)
        return href

    def citation_for_doc_id(self, doc_id_value: int) -> str | None:
        doc = self.get_doc(doc_id_value)
        if doc is None:
            return None
        title = str(getattr(doc, "title", "") or "").strip()
        note_href = self.item_note_href_for_doc(doc)
        url = str(getattr(doc, "canonical_url", "") or "").strip()
        label = _citation_label_from_title(title)
        if note_href:
            return f"[{label}]({note_href})"
        if url:
            return f"[{label}]({url})"
        return label

    def _rewrite_doc_id_match(self, match: re.Match[str]) -> str:
        doc_ids = _parse_positive_unique_doc_ids(match.group(1) or "")
        if not doc_ids:
            return match.group(0)
        self.stats.doc_ref_occurrences_total += 1
        citations: list[str] = []
        for doc_id_inner in doc_ids:
            cite = self.citation_for_doc_id(doc_id_inner)
            if cite is None:
                self.stats.doc_ref_unresolved_total += 1
                citations.append("Paper")
            else:
                self.stats.doc_ref_resolved_total += 1
                citations.append(cite)
        return "、".join(citations)

    def _rewrite_doc_short_match(self, match: re.Match[str]) -> str:
        raw_id = match.group(1) or ""
        try:
            doc_id_inner = int(raw_id)
        except Exception:
            return match.group(0)
        if doc_id_inner <= 0:
            return match.group(0)
        cite = self.citation_for_doc_id(doc_id_inner)
        if cite is None:
            self.stats.doc_ref_unresolved_total += 1
            return match.group(0)
        self.stats.doc_ref_occurrences_total += 1
        self.stats.doc_ref_resolved_total += 1
        return cite

    def rewrite_doc_refs(self, value: str) -> str:
        raw = str(value or "")
        if not raw.strip():
            return raw
        rewritten = _DOC_REF_PATTERN.sub(self._rewrite_doc_id_match, raw)
        rewritten = _DOC_SHORT_PATTERN.sub(self._rewrite_doc_short_match, rewritten)
        return _CHUNK_SUFFIX_PATTERN.sub("", rewritten)

    def rewrite_canonical_item_links(self, value: str) -> str:
        raw = str(value or "")
        if not raw.strip() or not self.note_href_by_url:
            return raw

        def _replace_markdown_link(match: re.Match[str]) -> str:
            label = match.group(1) or ""
            raw_target = match.group(2) or ""
            href, suffix = _split_markdown_link_target(raw_target)
            mapped_href = self.note_href_by_url.get(href)
            if mapped_href is None:
                return match.group(0)
            self.stats.canonical_link_rewrites_total += 1
            suffix_segment = f" {suffix}" if suffix else ""
            return f"[{label}]({mapped_href}{suffix_segment})"

        return _MARKDOWN_LINK_PATTERN.sub(_replace_markdown_link, raw)

    def rewrite_text(self, value: str) -> str:
        return self.rewrite_canonical_item_links(self.rewrite_doc_refs(value))

    def collect_history_window_refs_from_text(self, value: str) -> None:
        raw = str(value or "").strip()
        if not raw:
            return
        seen_window_ids: set[str] = set()
        for match in _HISTORY_WINDOW_ID_PATTERN.finditer(raw):
            window_id = str(match.group(1) or "").strip().lower()
            if not window_id or window_id in seen_window_ids:
                continue
            seen_window_ids.add(window_id)
            self.history_window_ref(window_id)

    def _history_window_index(self, normalized_window_id: str) -> int | None:
        match = re.fullmatch(r"prev_(\d+)", normalized_window_id)
        if match is None:
            return None
        return max(1, int(match.group(1)))

    def _history_window_doc(self, *, index: int) -> tuple[Any | None, Any | None]:
        period_start = self.current_period_start
        if period_start is None:
            return None, None
        windows = peer_history_windows_for_period(
            granularity=self.payload.granularity,
            period_start=period_start,
            window_count=index,
        )
        if len(windows) < index:
            return None, None
        window = windows[index - 1]
        docs = self.repository.list_documents(
            doc_type="trend",
            granularity=self.payload.granularity,
            period_start=window.period_start,
            period_end=window.period_end,
            order_by="event_desc",
            limit=1,
        )
        return window, (docs[0] if docs else None)

    def _build_history_window_ref(
        self,
        *,
        window: Any,
        doc: Any | None,
    ) -> dict[str, Any]:
        localized_title = (
            self.localized_trend_title_for_doc(int(getattr(doc, "id") or 0))
            if doc is not None
            else None
        )
        return {
            "window_id": window.window_id,
            "label": window.label,
            "title": (
                _history_window_title_label(
                    localized_title or str(getattr(doc, "title", "") or "")
                )
                if doc is not None
                else ""
            ),
            "granularity": self.payload.granularity,
            "period_start": window.period_start.isoformat(),
            "trend_doc_id": int(getattr(doc, "id") or 0) if doc is not None else 0,
        }

    def history_window_ref(self, window_id: str) -> dict[str, Any] | None:
        normalized_window_id = str(window_id or "").strip().lower()
        if not normalized_window_id or self.current_period_start is None:
            return None
        if normalized_window_id in self.history_window_refs:
            return self.history_window_refs[normalized_window_id]
        index = self._history_window_index(normalized_window_id)
        if index is None:
            return None
        window, doc = self._history_window_doc(index=index)
        if window is None:
            return None
        ref = self._build_history_window_ref(window=window, doc=doc)
        self.history_window_refs[normalized_window_id] = ref
        return ref

    def _normalized_history_windows(self, history_windows: Any) -> list[str]:
        if not isinstance(history_windows, list):
            return []
        normalized = [str(window).strip() for window in history_windows if str(window).strip()]
        for window in normalized:
            self.history_window_ref(window)
        return normalized

    def _materialize_evolution_signal(self, signal: Any) -> dict[str, Any] | None:
        if not isinstance(signal, dict):
            return None
        normalized_signal = dict(signal)
        normalized_signal["theme"] = self.rewrite_text(
            str(normalized_signal.get("theme") or "").strip()
        )
        normalized_signal["summary"] = self.rewrite_text(
            str(normalized_signal.get("summary") or "").strip()
        )
        self.collect_history_window_refs_from_text(
            str(normalized_signal.get("summary") or "")
        )
        normalized_signal["history_windows"] = self._normalized_history_windows(
            normalized_signal.get("history_windows") or []
        )
        return normalized_signal

    def materialize_evolution(self) -> dict[str, Any] | None:
        if self.payload.evolution is None:
            return None
        evolution_for_notes = self.payload.evolution.model_dump(mode="json")
        evolution_for_notes["summary_md"] = clamp_trend_overview_markdown(
            self.rewrite_text(str(evolution_for_notes.get("summary_md") or "")),
            output_language=self.output_language,
        )
        self.collect_history_window_refs_from_text(
            str(evolution_for_notes.get("summary_md") or "")
        )
        normalized_signals: list[dict[str, Any]] = []
        for signal in evolution_for_notes.get("signals") or []:
            normalized_signal = self._materialize_evolution_signal(signal)
            if normalized_signal is None:
                continue
            normalized_signals.append(normalized_signal)
        evolution_for_notes["signals"] = normalized_signals
        return evolution_for_notes

    def materialize_highlights(self) -> list[str]:
        return [
            self.rewrite_text(str(highlight))
            for highlight in (list(self.payload.highlights) or [])
        ]

    def _representative_authors_for_doc(self, doc: Any) -> list[str]:
        doc_type = str(getattr(doc, "doc_type", "") or "").strip().lower()
        if doc_type != "item":
            return []
        raw_item_id = getattr(doc, "item_id", None)
        try:
            item_id_int = int(raw_item_id) if raw_item_id is not None else 0
        except Exception:
            item_id_int = 0
        if item_id_int <= 0:
            return []
        item = self.get_item(item_id_int)
        if item is None:
            return []
        return _parse_authors(getattr(item, "authors", None))

    def _materialize_representative_chunk(
        self,
        rep: dict[str, Any],
        *,
        seen_rep_doc_ids: set[int],
    ) -> dict[str, Any] | None:
        raw_doc_id = rep.get("doc_id")
        raw_chunk_index = rep.get("chunk_index")
        if raw_doc_id is None or raw_chunk_index is None:
            return None
        try:
            doc_id_int = int(raw_doc_id)
            chunk_index_int = int(raw_chunk_index)
        except Exception:
            return None
        if doc_id_int <= 0 or chunk_index_int < 0:
            return None
        if doc_id_int in seen_rep_doc_ids:
            return None
        seen_rep_doc_ids.add(doc_id_int)

        doc = self.get_doc(doc_id_int)
        if doc is None:
            return None
        title = str(getattr(doc, "title", "") or "").strip()
        if not title:
            return None
        note_href = self.item_note_href_for_doc(doc)
        url = str(getattr(doc, "canonical_url", "") or "").strip()
        authors = self._representative_authors_for_doc(doc)

        enriched = dict(rep)
        enriched["title"] = title
        if note_href:
            enriched["note_href"] = note_href
        if url:
            enriched["url"] = url
        if authors:
            enriched["authors"] = authors
        return enriched

    def _materialize_cluster(self, cluster: Any) -> dict[str, Any]:
        cluster_dict = cluster.model_dump(mode="json")
        cluster_dict["name"] = self.rewrite_text(
            str(cluster_dict.get("name") or "").strip()
        )
        cluster_dict["description"] = self.rewrite_text(
            str(cluster_dict.get("description") or "").strip()
        )
        reps = cluster_dict.get("representative_chunks") or []
        enriched_reps: list[dict[str, Any]] = []
        seen_rep_doc_ids: set[int] = set()
        if isinstance(reps, list):
            for rep in reps:
                if not isinstance(rep, dict):
                    continue
                enriched = self._materialize_representative_chunk(
                    rep,
                    seen_rep_doc_ids=seen_rep_doc_ids,
                )
                if enriched is not None:
                    enriched_reps.append(enriched)
        cluster_dict["representative_chunks"] = enriched_reps
        return cluster_dict

    def materialize_clusters(self) -> list[dict[str, Any]]:
        return [
            self._materialize_cluster(cluster)
            for cluster in self.payload.clusters or []
        ]


def materialize_trend_note_payload(
    *,
    repository: Any,
    payload: TrendPayload,
    markdown_output_dir: Path,
    output_language: str | None,
    language_code: str | None = None,
    item_note_href_by_url: dict[str, str] | None = None,
) -> MaterializedTrendNotePayload:
    materializer = _TrendNoteMaterializer(
        repository=repository,
        payload=payload,
        markdown_output_dir=markdown_output_dir,
        output_language=output_language,
        language_code=language_code,
        note_href_by_url={
            str(url).strip(): str(href).strip()
            for url, href in (item_note_href_by_url or {}).items()
            if str(url).strip() and str(href).strip()
        },
        stats=TrendNoteRewriteStats(),
        doc_cache={},
        item_cache={},
        history_window_refs={},
        current_period_start=_parse_period_start(payload.period_start),
    )
    title_for_notes = sanitize_trend_title(
        materializer.rewrite_text(str(payload.title)),
        fallback="Trend",
    )
    overview_md_for_notes = clamp_trend_overview_markdown(
        materializer.rewrite_text(str(payload.overview_md)),
        output_language=output_language,
    )
    evolution_for_notes = materializer.materialize_evolution()
    highlights_for_notes = materializer.materialize_highlights()
    clusters_for_notes = materializer.materialize_clusters()

    return MaterializedTrendNotePayload(
        title=title_for_notes,
        overview_md=overview_md_for_notes,
        topics=list(payload.topics),
        evolution=evolution_for_notes,
        history_window_refs=materializer.history_window_refs,
        clusters=clusters_for_notes,
        highlights=highlights_for_notes,
        rewrite_stats=materializer.stats,
    )
