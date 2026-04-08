from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any

from recoleta.publish.item_notes import resolve_item_note_href
from recoleta.publish.trend_render_shared import (
    clamp_trend_overview_markdown,
    sanitize_trend_title,
)
from recoleta.trends import TrendPayload


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
    clusters: list[dict[str, Any]]
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


def _split_markdown_link_target(target: str) -> tuple[str, str]:
    stripped = str(target or "").strip()
    if not stripped:
        return "", ""
    if " " not in stripped:
        return stripped, ""
    url, suffix = stripped.split(" ", 1)
    return url.strip(), suffix.strip()

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
    note_href_by_url: dict[str, str]
    stats: TrendNoteRewriteStats
    doc_cache: dict[int, Any | None]
    item_cache: dict[int, Any | None]

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
        cluster_dict = (
            cluster.model_dump(mode="json")
            if hasattr(cluster, "model_dump")
            else dict(cluster)
        )
        evidence_entries: list[dict[str, Any]] = []
        seen_rep_doc_ids: set[int] = set()
        for ref in list(cluster_dict.get("evidence_refs") or []):
            if not isinstance(ref, dict):
                continue
            enriched = self._materialize_representative_chunk(
                ref,
                seen_rep_doc_ids=seen_rep_doc_ids,
            )
            if enriched is None:
                continue
            reason = str(ref.get("reason") or "").strip()
            if reason:
                enriched["reason"] = self.rewrite_text(reason)
            evidence_entries.append(enriched)
        return {
            "title": self.rewrite_text(str(cluster_dict.get("title") or "").strip()),
            "content_md": self.rewrite_text(
                str(cluster_dict.get("content_md") or "").strip()
            ),
            "evidence_refs": evidence_entries,
        }

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
        note_href_by_url=_normalized_note_href_by_url(item_note_href_by_url),
        stats=TrendNoteRewriteStats(),
        doc_cache={},
        item_cache={},
    )
    title_for_notes = sanitize_trend_title(
        materializer.rewrite_text(str(payload.title)),
        fallback="Trend",
    )
    overview_md_for_notes = clamp_trend_overview_markdown(
        materializer.rewrite_text(str(payload.overview_md)),
        output_language=output_language,
    )
    clusters_for_notes = materializer.materialize_clusters()

    return MaterializedTrendNotePayload(
        title=title_for_notes,
        overview_md=overview_md_for_notes,
        topics=list(payload.topics),
        clusters=clusters_for_notes,
        rewrite_stats=materializer.stats,
    )


def _normalized_note_href_by_url(
    item_note_href_by_url: dict[str, str] | None,
) -> dict[str, str]:
    return {
        str(url).strip(): str(href).strip()
        for url, href in (item_note_href_by_url or {}).items()
        if str(url).strip() and str(href).strip()
    }
