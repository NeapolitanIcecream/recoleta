from __future__ import annotations

from collections.abc import Sequence
from typing import Any

_VALID_SOURCE_TYPES = {
    "paper",
    "benchmark",
    "field_report",
    "product_post",
    "news",
    "forum_post",
    "survey",
    "unknown",
}

_SOURCE_TYPE_BY_SOURCE = {
    "arxiv": "paper",
    "openreview": "paper",
    "hf_daily": "paper",
    "hn": "forum_post",
    "rss": "unknown",
}

_DEFAULT_CONFIDENCE_BY_SOURCE_TYPE = {
    "benchmark": "high",
    "field_report": "high",
    "paper": "high",
    "forum_post": "medium",
    "news": "medium",
    "product_post": "medium",
    "survey": "low",
    "unknown": "low",
}


def _value_from(raw_value: Any, key: str, default: Any = None) -> Any:
    if isinstance(raw_value, dict):
        return raw_value.get(key, default)
    return getattr(raw_value, key, default)


def _single_line(value: Any) -> str:
    return " ".join(str(value or "").split()).strip()


def _normalize_markdown(value: Any) -> str:
    normalized = str(value or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    if not normalized:
        return ""
    lines = [line.rstrip() for line in normalized.split("\n")]
    return "\n".join(lines).strip()


def _int_or_none(value: Any) -> int | None:
    try:
        return int(value)
    except Exception:
        return None


def _float_or_none(value: Any) -> float | None:
    try:
        return float(value)
    except Exception:
        return None


def _normalize_source_type(value: Any) -> str:
    normalized = _single_line(value).lower()
    if normalized in _VALID_SOURCE_TYPES:
        return normalized
    return _SOURCE_TYPE_BY_SOURCE.get(normalized, "unknown")


def _project_source_type(raw_source: Any) -> str:
    explicit = _normalize_source_type(_value_from(raw_source, "source_type", ""))
    if explicit != "unknown":
        return explicit
    return _normalize_source_type(_value_from(raw_source, "source", ""))


def _project_confidence(raw_source: Any, *, source_type: str) -> str:
    explicit = _single_line(_value_from(raw_source, "confidence", "")).lower()
    if explicit in {"high", "medium", "low"}:
        return explicit
    score = _float_or_none(_value_from(raw_source, "score", None))
    if score is None:
        return _DEFAULT_CONFIDENCE_BY_SOURCE_TYPE.get(source_type, "low")
    if score >= 0.8:
        return "high"
    if score >= 0.5:
        return "medium"
    return "low"


def _project_reasons(raw_source: Any) -> tuple[list[str], str | None]:
    reasons = [
        _normalize_markdown(reason)
        for reason in list(_value_from(raw_source, "reasons", []) or [])
        if _normalize_markdown(reason)
    ]
    reason = _normalize_markdown(_value_from(raw_source, "reason", "") or "") or None
    if reason is None and reasons:
        reason = reasons[0]
    return reasons, reason


def _project_title(*, raw_source: Any, fallback_title: str | None) -> tuple[int | None, str]:
    doc_id = _int_or_none(_value_from(raw_source, "doc_id", None))
    title = _single_line(_value_from(raw_source, "title", "") or fallback_title or "")
    if not title and doc_id is not None and doc_id > 0:
        title = f"Document {doc_id}"
    return doc_id, title


def _project_target_href(raw_source: Any) -> tuple[str | None, str | None]:
    href = _single_line(
        _value_from(raw_source, "href", "") or _value_from(raw_source, "note_href", "")
    )
    url = _single_line(_value_from(raw_source, "url", ""))
    return href or url or None, url or None


def _project_authors(raw_source: Any) -> list[str]:
    authors: list[str] = []
    for author in list(_value_from(raw_source, "authors", []) or []):
        normalized = _single_line(author)
        if normalized:
            authors.append(normalized)
    return authors


def project_source_metadata(
    raw_source: Any,
    *,
    fallback_title: str | None = None,
    include_reason: bool = False,
) -> dict[str, Any]:
    doc_id, title = _project_title(raw_source=raw_source, fallback_title=fallback_title)
    chunk_index = _int_or_none(_value_from(raw_source, "chunk_index", 0))
    href, url = _project_target_href(raw_source)
    source_type = _project_source_type(raw_source)
    projected: dict[str, Any] = {
        "title": title,
        "href": href,
        "url": url,
        "authors": _project_authors(raw_source),
        "doc_id": doc_id,
        "chunk_index": 0 if chunk_index is None else chunk_index,
        "source_type": source_type,
        "confidence": _project_confidence(raw_source, source_type=source_type),
    }
    if include_reason:
        reasons, reason = _project_reasons(raw_source)
        if reasons:
            projected["reasons"] = reasons
        if reason:
            projected["reason"] = reason
    return projected


def _ordered_refs_by_doc_id(raw_evidence_refs: Sequence[Any]) -> list[list[Any]]:
    grouped: dict[int | None, list[Any]] = {}
    ordered_keys: list[int | None] = []
    for raw_ref in raw_evidence_refs:
        doc_id = _int_or_none(_value_from(raw_ref, "doc_id", None))
        key = doc_id if doc_id is not None and doc_id > 0 else None
        if key not in grouped:
            grouped[key] = []
            ordered_keys.append(key)
        grouped[key].append(raw_ref)
    return [grouped[key] for key in ordered_keys if grouped.get(key)]


def _dedupe_reason_list(refs: Sequence[Any]) -> list[str]:
    reasons: list[str] = []
    seen_reasons: set[str] = set()
    for ref in refs:
        normalized_reason = _normalize_markdown(_value_from(ref, "reason", "") or "")
        if not normalized_reason or normalized_reason in seen_reasons:
            continue
        seen_reasons.add(normalized_reason)
        reasons.append(normalized_reason)
    return reasons


def project_idea_evidence(raw_evidence_refs: Any) -> list[dict[str, Any]]:
    if not isinstance(raw_evidence_refs, Sequence):
        return []

    projected: list[dict[str, Any]] = []
    for refs in _ordered_refs_by_doc_id(list(raw_evidence_refs)):
        reasons = _dedupe_reason_list(refs)
        projected_ref = project_source_metadata(refs[0], include_reason=True)
        if reasons:
            projected_ref["reasons"] = reasons
            if not _normalize_markdown(projected_ref.get("reason") or ""):
                projected_ref["reason"] = reasons[0]
        projected.append(projected_ref)
    return projected


__all__ = ["project_idea_evidence", "project_source_metadata"]
