from __future__ import annotations

import re
from datetime import datetime
from typing import Any, Callable

from recoleta.item_summary import extract_item_summary_sections
from recoleta.ports import TrendRepositoryPort
from recoleta.rag.search_models import SummaryCorpusWindow

_SEARCH_TEXT_TOKEN_RE = re.compile(r"\w+", flags=re.UNICODE)
_SEARCH_TEXT_BACKOFF_MAX_CANDIDATES = 24
_INLINE_SUMMARY_SECTION_RE = re.compile(
    r"(?is)(summary|problem|approach|results)\s*[:：]\s*(.*?)(?=(summary|problem|approach|results)\s*[:：]|$)"
)


def truncate_text(value: str, *, max_chars: int) -> str:
    normalized = str(value or "").strip()
    cap = max(0, int(max_chars))
    if cap <= 0 or len(normalized) <= cap:
        return normalized
    return normalized[:cap].rstrip()


def _clean_summary_section_value(value: str) -> str:
    normalized = str(value or "").strip()
    if normalized.startswith(("- ", "* ")):
        return normalized[2:].strip()
    return normalized


def _inline_summary_sections(value: str) -> dict[str, str] | None:
    inline_sections = {key: "" for key in ("summary", "problem", "approach", "results")}
    matches = list(_INLINE_SUMMARY_SECTION_RE.finditer(str(value or "")))
    if not matches:
        return None
    for match in matches:
        key = str(match.group(1) or "").strip().lower()
        body = _clean_summary_section_value(str(match.group(2) or "").strip())
        if key in inline_sections and body:
            inline_sections[key] = body
    if any(str(inline_sections.get(key) or "").strip() for key in ("problem", "approach", "results")):
        return inline_sections
    return None


def normalize_summary_sections(value: str) -> dict[str, str]:
    sections = extract_item_summary_sections(value)
    only_summary_present = (
        str(sections.get("summary") or "").strip()
        and not str(sections.get("problem") or "").strip()
        and not str(sections.get("approach") or "").strip()
        and not str(sections.get("results") or "").strip()
    )
    if only_summary_present:
        inline_sections = _inline_summary_sections(value)
        if inline_sections is not None:
            return inline_sections
    return {
        key: _clean_summary_section_value(section_value)
        for key, section_value in sections.items()
    }


def _unique_query_tokens(query: str) -> list[str]:
    tokens: list[str] = []
    seen_tokens: set[str] = set()
    for token in _SEARCH_TEXT_TOKEN_RE.findall(str(query or "")):
        normalized = str(token or "").strip()
        lowered = normalized.lower()
        if not lowered or lowered in seen_tokens:
            continue
        seen_tokens.add(lowered)
        tokens.append(normalized)
    return tokens


def _contiguous_query_candidates(tokens: list[str]) -> list[tuple[str, int]]:
    candidates: list[tuple[str, int]] = []
    seen_queries: set[str] = set()
    total = len(tokens)
    for size in range(total, 0, -1):
        for start in range(0, total - size + 1):
            candidate = " ".join(tokens[start : start + size]).strip()
            if not candidate or candidate in seen_queries:
                continue
            seen_queries.add(candidate)
            candidates.append((candidate, total - size))
    return candidates


def _longest_token_candidates(
    tokens: list[str],
    *,
    existing: list[tuple[str, int]],
) -> list[tuple[str, int]]:
    seen_queries = {candidate for candidate, _depth in existing}
    longest_tokens = sorted(tokens, key=lambda token: (-len(token), token.lower()))
    candidates = list(existing)
    total = len(tokens)
    for size in range(min(3, total), 0, -1):
        candidate = " ".join(longest_tokens[:size]).strip()
        if not candidate or candidate in seen_queries:
            continue
        seen_queries.add(candidate)
        candidates.append((candidate, total - size))
    return candidates


def _cap_query_candidates(
    candidates: list[tuple[str, int]],
) -> list[tuple[str, int]]:
    if len(candidates) <= _SEARCH_TEXT_BACKOFF_MAX_CANDIDATES:
        return candidates

    capped_candidates: list[tuple[str, int]] = []
    max_index = len(candidates) - 1
    for ordinal in range(_SEARCH_TEXT_BACKOFF_MAX_CANDIDATES):
        if _SEARCH_TEXT_BACKOFF_MAX_CANDIDATES == 1:
            index = 0
        else:
            index = (ordinal * max_index) // (_SEARCH_TEXT_BACKOFF_MAX_CANDIDATES - 1)
        candidate = candidates[index]
        if candidate in capped_candidates:
            continue
        capped_candidates.append(candidate)
    return capped_candidates


def candidate_text_queries(query: str) -> list[tuple[str, int]]:
    tokens = _unique_query_tokens(query)
    if not tokens:
        return []
    candidates = _contiguous_query_candidates(tokens)
    return _cap_query_candidates(_longest_token_candidates(tokens, existing=candidates))


def serialize_document(
    *,
    repository: TrendRepositoryPort,
    doc: Any,
) -> dict[str, Any]:
    published_at = getattr(doc, "published_at", None)
    period_start_value = getattr(doc, "period_start", None)
    period_end_value = getattr(doc, "period_end", None)
    raw_item_id = getattr(doc, "item_id", None)
    try:
        item_id = int(raw_item_id) if raw_item_id is not None else None
    except Exception:
        item_id = None
    return {
        "doc_id": int(getattr(doc, "id")),
        "doc_type": str(getattr(doc, "doc_type") or ""),
        "title": str(getattr(doc, "title") or ""),
        "item_id": item_id,
        "source": str(getattr(doc, "source") or ""),
        "canonical_url": str(getattr(doc, "canonical_url") or ""),
        "published_at": published_at.isoformat() if isinstance(published_at, datetime) else None,
        "granularity": str(getattr(doc, "granularity") or ""),
        "period_start": period_start_value.isoformat()
        if isinstance(period_start_value, datetime)
        else None,
        "period_end": period_end_value.isoformat() if isinstance(period_end_value, datetime) else None,
        "authors": decode_item_authors(repository=repository, item_id=item_id),
    }


def document_event_sort_key(doc: Any) -> tuple[float, int]:
    raw_event = getattr(doc, "published_at", None)
    if not isinstance(raw_event, datetime):
        raw_event = getattr(doc, "period_start", None)
    event_ts = raw_event.timestamp() if isinstance(raw_event, datetime) else 0.0
    try:
        doc_id = int(getattr(doc, "id") or 0)
    except Exception:
        doc_id = 0
    return event_ts, doc_id


def decode_item_authors(
    *,
    repository: TrendRepositoryPort,
    item_id: int | None,
) -> list[str]:
    normalized_item_id = _normalized_item_id(item_id)
    if normalized_item_id is None:
        return []
    item = repository.get_item(item_id=normalized_item_id)
    if item is None:
        return []
    raw_authors = getattr(item, "authors", None)
    direct_authors = _normalized_author_names(raw_authors)
    if direct_authors:
        return direct_authors
    decoded_authors = _decoded_author_names(repository=repository, raw_authors=raw_authors)
    if decoded_authors:
        return decoded_authors
    return [raw_authors.strip()] if isinstance(raw_authors, str) and raw_authors.strip() else []


def _normalized_item_id(value: int | None) -> int | None:
    if value is None:
        return None
    try:
        normalized_item_id = int(value)
    except Exception:
        return None
    return normalized_item_id if normalized_item_id > 0 else None


def _normalized_author_names(raw_authors: Any) -> list[str]:
    if not isinstance(raw_authors, list):
        return []
    return [str(author).strip() for author in raw_authors if str(author).strip()]


def _decoded_author_names(
    *,
    repository: TrendRepositoryPort,
    raw_authors: Any,
) -> list[str]:
    decode_list = getattr(repository, "decode_list", None)
    if not callable(decode_list):
        return []
    try:
        decoded = decode_list(raw_authors)
    except Exception:
        return []
    return _normalized_author_names(decoded)


def search_hit_key(row: dict[str, Any]) -> tuple[int, int] | None:
    try:
        raw_doc_id = row.get("doc_id")
        raw_chunk_index = row.get("chunk_index")
        doc_id = int(raw_doc_id) if raw_doc_id is not None else 0
        chunk_index = int(raw_chunk_index) if raw_chunk_index is not None else -1
    except Exception:
        return None
    if doc_id <= 0 or chunk_index < 0:
        return None
    return doc_id, chunk_index


def _append_text_hits(
    *,
    seen_hits: set[tuple[int, int]],
    rows: list[dict[str, Any]],
    matched_query: str,
    backoff_depth: int,
    limit: int,
) -> tuple[list[dict[str, Any]], bool]:
    hits: list[dict[str, Any]] = []
    matched_in_candidate = False
    for row in rows:
        if not isinstance(row, dict):
            continue
        key = search_hit_key(row)
        if key is None or key in seen_hits:
            continue
        seen_hits.add(key)
        enriched = dict(row)
        enriched["matched_query"] = matched_query
        enriched["backoff_depth"] = backoff_depth
        hits.append(enriched)
        matched_in_candidate = True
        if len(hits) >= limit:
            break
    return hits, matched_in_candidate


def collect_text_hits_with_backoff(
    *,
    window: SummaryCorpusWindow,
    query: str,
    limit: int,
) -> tuple[list[dict[str, Any]], list[str]]:
    normalized_limit = max(1, int(limit or 1))
    hits: list[dict[str, Any]] = []
    seen_hits: set[tuple[int, int]] = set()
    matched_queries: list[str] = []
    for candidate_query, backoff_depth in candidate_text_queries(query):
        rows = window.repository.search_chunks_text(
            query=candidate_query,
            doc_type=window.doc_type,
            granularity=window.granularity,
            period_start=window.period_start,
            period_end=window.period_end,
            limit=normalized_limit,
        )
        candidate_hits, matched = _append_text_hits(
            seen_hits=seen_hits,
            rows=rows,
            matched_query=candidate_query,
            backoff_depth=int(backoff_depth),
            limit=normalized_limit - len(hits),
        )
        hits.extend(candidate_hits)
        if matched:
            matched_queries.append(candidate_query)
        if len(hits) >= normalized_limit:
            break
    return hits, matched_queries


def read_doc_content_chunks(
    *,
    repository: TrendRepositoryPort,
    doc_id: int,
    limit: int,
    text_max_chars: int,
) -> list[dict[str, Any]]:
    normalized_limit = max(0, int(limit or 0))
    if normalized_limit <= 0:
        return []
    out: list[dict[str, Any]] = []
    consecutive_misses = 0
    chunk_index = 1
    while len(out) < normalized_limit and consecutive_misses < 2 and chunk_index <= 12:
        chunk = repository.read_document_chunk(doc_id=doc_id, chunk_index=chunk_index)
        if chunk is None:
            consecutive_misses += 1
            chunk_index += 1
            continue
        consecutive_misses = 0
        if str(getattr(chunk, "kind", "") or "").strip().lower() != "content":
            chunk_index += 1
            continue
        text_value = truncate_text(str(getattr(chunk, "text", "") or ""), max_chars=text_max_chars)
        if not text_value:
            chunk_index += 1
            continue
        out.append(
            {
                "chunk_id": int(getattr(chunk, "id")),
                "doc_id": int(getattr(chunk, "doc_id")),
                "chunk_index": int(getattr(chunk, "chunk_index")),
                "kind": str(getattr(chunk, "kind") or ""),
                "start_char": getattr(chunk, "start_char", None),
                "end_char": getattr(chunk, "end_char", None),
                "source_content_type": str(getattr(chunk, "source_content_type") or ""),
                "text": text_value,
            }
        )
        chunk_index += 1
    return out


def _cached_document_metadata(
    *,
    repository: TrendRepositoryPort,
    serializer: Callable[[TrendRepositoryPort, Any], dict[str, Any]],
    doc_cache: dict[int, dict[str, Any] | None],
    doc_id: int,
) -> dict[str, Any] | None:
    if doc_id not in doc_cache:
        doc = repository.get_document(doc_id=doc_id)
        doc_cache[doc_id] = serializer(repository, doc) if doc is not None else None
    return doc_cache.get(doc_id)


def attach_doc_metadata(
    *,
    repository: TrendRepositoryPort,
    rows: list[dict[str, Any]],
    serializer: Callable[[TrendRepositoryPort, Any], dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    if not rows:
        return []
    serialize = serializer or (lambda repo, doc: serialize_document(repository=repo, doc=doc))
    doc_cache: dict[int, dict[str, Any] | None] = {}
    out: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        doc_id = search_hit_key(row)
        metadata = None
        if doc_id is not None:
            metadata = _cached_document_metadata(
                repository=repository,
                serializer=serialize,
                doc_cache=doc_cache,
                doc_id=doc_id[0],
            )
        enriched = dict(row)
        if metadata is not None:
            for key, value in metadata.items():
                enriched.setdefault(key, value)
        out.append(enriched)
    return out
