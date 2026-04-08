from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from pathlib import Path
import re
from typing import Any

from recoleta.presentation_projectors import project_source_metadata

PRESENTATION_SCHEMA_VERSION = 2

_LOCALIZED_LANGUAGE_SEGMENT_RE = re.compile(r"^[A-Za-z]{2,3}(?:[-_][A-Za-z0-9]{2,8})*$")
_LANGUAGE_LABEL_TO_CODE = {
    "arabic": "ar",
    "brazilian portuguese": "pt-BR",
    "chinese": "zh",
    "chinese (simplified)": "zh-CN",
    "chinese (traditional)": "zh-TW",
    "english": "en",
    "french": "fr",
    "german": "de",
    "italian": "it",
    "japanese": "ja",
    "korean": "ko",
    "portuguese": "pt",
    "portuguese (brazil)": "pt-BR",
    "russian": "ru",
    "simplified chinese": "zh-CN",
    "spanish": "es",
    "traditional chinese": "zh-TW",
}

_TREND_DISPLAY_LABELS = {
    "overview": "Overview",
    "clusters": "Clusters",
    "evidence": "Evidence",
}
_IDEA_DISPLAY_LABELS = {
    "summary": "Summary",
    "ideas": "Ideas",
    "evidence": "Evidence",
}


def _single_line(value: Any) -> str:
    return " ".join(str(value or "").split()).strip()


def _normalize_markdown(value: Any) -> str:
    normalized = str(value or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    if not normalized:
        return ""
    return "\n".join(line.rstrip() for line in normalized.split("\n")).strip()


def _value_from(raw_value: Any, key: str, default: Any = None) -> Any:
    if isinstance(raw_value, Mapping):
        return raw_value.get(key, default)
    return getattr(raw_value, key, default)


def _int_or_none(value: Any) -> int | None:
    try:
        return int(value)
    except Exception:
        return None


def _normalize_reasons(raw_source: Any) -> tuple[list[str], str | None]:
    reasons: list[str] = []
    seen: set[str] = set()
    for raw_reason in list(_value_from(raw_source, "reasons", []) or []):
        normalized = _normalize_markdown(raw_reason)
        if normalized and normalized not in seen:
            seen.add(normalized)
            reasons.append(normalized)
    reason = _normalize_markdown(_value_from(raw_source, "reason", "") or "") or None
    if reason is not None and reason not in seen:
        reasons.insert(0, reason)
    if reason is None and reasons:
        reason = reasons[0]
    return reasons, reason


def _project_evidence_entry(raw_source: Any) -> dict[str, Any]:
    projected = project_source_metadata(raw_source, include_reason=True)
    reasons, reason = _normalize_reasons(raw_source)
    entry: dict[str, Any] = {
        "title": _single_line(projected.get("title") or ""),
        "href": _single_line(projected.get("href") or ""),
        "url": _single_line(projected.get("url") or ""),
        "authors": [
            _single_line(author)
            for author in list(projected.get("authors") or [])
            if _single_line(author)
        ],
        "doc_id": _int_or_none(projected.get("doc_id")),
        "chunk_index": _int_or_none(projected.get("chunk_index")) or 0,
    }
    if reasons:
        entry["reasons"] = reasons
    if reason:
        entry["reason"] = reason
    return entry


def _project_evidence(raw_sources: Any) -> list[dict[str, Any]]:
    if not isinstance(raw_sources, Sequence) or isinstance(raw_sources, (str, bytes)):
        return []
    grouped: dict[int, list[Any]] = {}
    ordered: list[tuple[str, Any]] = []
    for raw_source in raw_sources:
        doc_id = _int_or_none(_value_from(raw_source, "doc_id", None))
        if doc_id is None or doc_id <= 0:
            ordered.append(("raw", raw_source))
            continue
        if doc_id not in grouped:
            grouped[doc_id] = []
            ordered.append(("doc", doc_id))
        grouped[doc_id].append(raw_source)

    projected: list[dict[str, Any]] = []
    for kind, value in ordered:
        if kind == "raw":
            projected.append(_project_evidence_entry(value))
            continue
        refs = grouped.get(int(value), [])
        if not refs:
            continue
        entry = _project_evidence_entry(refs[0])
        reasons, reason = _normalize_reasons({"reasons": [
            _value_from(ref, "reason", "") for ref in refs
        ]})
        if reasons:
            entry["reasons"] = reasons
        if reason:
            entry["reason"] = reason
        projected.append(entry)
    return projected


def resolve_presentation_language_code(
    *,
    language_code: str | None = None,
    output_language: str | None = None,
) -> str | None:
    normalized = _single_line(language_code)
    if normalized:
        normalized = normalized.replace("_", "-")
        if _LOCALIZED_LANGUAGE_SEGMENT_RE.match(normalized):
            if normalized.lower() == "zh-cn":
                return "zh-CN"
            if normalized.lower() == "zh-tw":
                return "zh-TW"
            return normalized
    normalized_output = _single_line(output_language).lower()
    if not normalized_output:
        return None
    if normalized_output in _LANGUAGE_LABEL_TO_CODE:
        return _LANGUAGE_LABEL_TO_CODE[normalized_output]
    normalized_output = normalized_output.replace("_", "-")
    if _LOCALIZED_LANGUAGE_SEGMENT_RE.match(normalized_output):
        if normalized_output == "zh-cn":
            return "zh-CN"
        if normalized_output == "zh-tw":
            return "zh-TW"
        return normalized_output
    return None


def trend_display_labels(*, language_code: str | None = None) -> dict[str, str]:
    _ = language_code
    return dict(_TREND_DISPLAY_LABELS)


def idea_display_labels(*, language_code: str | None = None) -> dict[str, str]:
    _ = language_code
    return dict(_IDEA_DISPLAY_LABELS)


def build_trend_presentation_v2(
    *,
    source_markdown_path: str,
    title: str,
    overview_md: str,
    clusters: Sequence[Any] | None,
    language_code: str | None = None,
    display_language_code: str | None = None,
) -> dict[str, Any]:
    resolved_language_code = resolve_presentation_language_code(
        language_code=language_code
    )
    labels = trend_display_labels(language_code=display_language_code)
    return {
        "presentation_schema_version": PRESENTATION_SCHEMA_VERSION,
        "surface_kind": "trend",
        "language_code": resolved_language_code,
        "source_markdown_path": _single_line(source_markdown_path),
        "display_labels": labels,
        "content": {
            "title": _single_line(title),
            "overview": _normalize_markdown(overview_md),
            "clusters": [
                {
                    "title": _single_line(_value_from(cluster, "title", "")),
                    "content": _normalize_markdown(
                        _value_from(cluster, "content_md", "")
                    ),
                    "evidence": _project_evidence(
                        _value_from(cluster, "evidence_refs", [])
                    ),
                }
                for cluster in list(clusters or [])
            ],
        },
    }


def build_idea_presentation_v2(
    *,
    source_markdown_path: str,
    title: str,
    summary_md: str,
    ideas: list[Any],
    language_code: str | None = None,
    display_language_code: str | None = None,
) -> dict[str, Any]:
    resolved_language_code = resolve_presentation_language_code(
        language_code=language_code
    )
    labels = idea_display_labels(language_code=display_language_code)
    return {
        "presentation_schema_version": PRESENTATION_SCHEMA_VERSION,
        "surface_kind": "idea",
        "language_code": resolved_language_code,
        "source_markdown_path": _single_line(source_markdown_path),
        "display_labels": labels,
        "content": {
            "title": _single_line(title),
            "summary": _normalize_markdown(summary_md),
            "ideas": [
                {
                    "title": _single_line(_value_from(idea, "title", "")),
                    "content": _normalize_markdown(
                        _value_from(idea, "content_md", "")
                    ),
                    "evidence": _project_evidence(
                        _value_from(idea, "evidence_refs", [])
                    ),
                }
                for idea in list(ideas or [])[:3]
            ],
        },
    }


def presentation_sidecar_path(*, note_path: Path) -> Path:
    return note_path.with_name(f"{note_path.stem}.presentation.json")


def _validate_required_string(
    value: Any, *, field_path: str, errors: list[str]
) -> str | None:
    if not isinstance(value, str):
        errors.append(f"{field_path} must be a string")
        return None
    normalized = value.strip()
    if not normalized:
        errors.append(f"{field_path} must not be empty")
        return None
    return normalized


def _validate_evidence_entries(
    entries: Any, *, field_path: str, errors: list[str]
) -> None:
    if not isinstance(entries, list):
        errors.append(f"{field_path} must be a list")
        return
    for index, entry in enumerate(entries):
        if not isinstance(entry, Mapping):
            errors.append(f"{field_path}[{index}] must be a mapping")
            continue
        _validate_required_string(
            entry.get("title"),
            field_path=f"{field_path}[{index}].title",
            errors=errors,
        )
        href = entry.get("href")
        url = entry.get("url")
        if href is not None and not isinstance(href, str):
            errors.append(f"{field_path}[{index}].href must be a string")
        if url is not None and not isinstance(url, str):
            errors.append(f"{field_path}[{index}].url must be a string")
        doc_id = entry.get("doc_id")
        if doc_id is not None:
            if not isinstance(doc_id, int) or doc_id <= 0:
                errors.append(f"{field_path}[{index}].doc_id must be a positive integer")
        chunk_index = entry.get("chunk_index")
        if chunk_index is not None:
            if not isinstance(chunk_index, int) or chunk_index < 0:
                errors.append(f"{field_path}[{index}].chunk_index must be >= 0")
        authors = entry.get("authors")
        if authors is not None and (
            not isinstance(authors, list)
            or any(not isinstance(author, str) for author in authors)
        ):
            errors.append(f"{field_path}[{index}].authors must be a list of strings")
        reasons = entry.get("reasons")
        if reasons is not None and (
            not isinstance(reasons, list)
            or any(not isinstance(reason, str) or not reason.strip() for reason in reasons)
        ):
            errors.append(f"{field_path}[{index}].reasons must be a list of strings")
        reason = entry.get("reason")
        if reason is not None and (not isinstance(reason, str) or not reason.strip()):
            errors.append(f"{field_path}[{index}].reason must be a non-empty string")
        if "source_type" in entry:
            errors.append(f"{field_path}[{index}].source_type is not allowed")
        if "confidence" in entry:
            errors.append(f"{field_path}[{index}].confidence is not allowed")


def _validate_display_labels(
    labels: Any, *, expected_keys: set[str], field_path: str, errors: list[str]
) -> None:
    if not isinstance(labels, Mapping):
        errors.append(f"{field_path} must be a mapping")
        return
    actual_keys = set(labels)
    if actual_keys != expected_keys:
        errors.append(
            f"{field_path} must contain exactly: {', '.join(sorted(expected_keys))}"
        )
    for key in expected_keys:
        _validate_required_string(
            labels.get(key), field_path=f"{field_path}.{key}", errors=errors
        )


def _validate_trend_presentation(content: Any, errors: list[str]) -> None:
    if not isinstance(content, Mapping):
        errors.append("trend content must be a mapping")
        return
    _validate_required_string(content.get("title"), field_path="trend content.title", errors=errors)
    _validate_required_string(content.get("overview"), field_path="trend content.overview", errors=errors)
    clusters = content.get("clusters")
    if not isinstance(clusters, list):
        errors.append("trend content.clusters must be a list")
        return
    for index, cluster in enumerate(clusters):
        if not isinstance(cluster, Mapping):
            errors.append(f"trend content.clusters[{index}] must be a mapping")
            continue
        _validate_required_string(
            cluster.get("title"),
            field_path=f"trend content.clusters[{index}].title",
            errors=errors,
        )
        _validate_required_string(
            cluster.get("content"),
            field_path=f"trend content.clusters[{index}].content",
            errors=errors,
        )
        _validate_evidence_entries(
            cluster.get("evidence"),
            field_path=f"trend content.clusters[{index}].evidence",
            errors=errors,
        )


def _validate_idea_presentation(content: Any, errors: list[str]) -> None:
    if not isinstance(content, Mapping):
        errors.append("idea content must be a mapping")
        return
    _validate_required_string(content.get("title"), field_path="idea content.title", errors=errors)
    _validate_required_string(content.get("summary"), field_path="idea content.summary", errors=errors)
    ideas = content.get("ideas")
    if not isinstance(ideas, list):
        errors.append("idea content.ideas must be a list")
        return
    for index, idea in enumerate(ideas):
        if not isinstance(idea, Mapping):
            errors.append(f"idea content.ideas[{index}] must be a mapping")
            continue
        _validate_required_string(
            idea.get("title"),
            field_path=f"idea content.ideas[{index}].title",
            errors=errors,
        )
        _validate_required_string(
            idea.get("content"),
            field_path=f"idea content.ideas[{index}].content",
            errors=errors,
        )
        _validate_evidence_entries(
            idea.get("evidence"),
            field_path=f"idea content.ideas[{index}].evidence",
            errors=errors,
        )


def validate_presentation(presentation: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(presentation, Mapping):
        return ["presentation must be a mapping"]
    schema_version = presentation.get("presentation_schema_version")
    if schema_version != PRESENTATION_SCHEMA_VERSION:
        errors.append(f"presentation_schema_version must be {PRESENTATION_SCHEMA_VERSION}")
    surface_kind = _single_line(presentation.get("surface_kind") or "")
    if surface_kind not in {"trend", "idea"}:
        errors.append("surface_kind must be one of: trend, idea")
        return errors
    _validate_required_string(
        presentation.get("source_markdown_path"),
        field_path="source_markdown_path",
        errors=errors,
    )
    language_code = presentation.get("language_code")
    if language_code is not None and not isinstance(language_code, str):
        errors.append("language_code must be a string")

    if surface_kind == "trend":
        _validate_display_labels(
            presentation.get("display_labels"),
            expected_keys=set(_TREND_DISPLAY_LABELS),
            field_path="display_labels",
            errors=errors,
        )
        _validate_trend_presentation(presentation.get("content"), errors)
    else:
        _validate_display_labels(
            presentation.get("display_labels"),
            expected_keys=set(_IDEA_DISPLAY_LABELS),
            field_path="display_labels",
            errors=errors,
        )
        _validate_idea_presentation(presentation.get("content"), errors)
    return errors


def write_presentation_sidecar(*, note_path: Path, presentation: Mapping[str, Any]) -> Path:
    errors = validate_presentation(presentation)
    if errors:
        raise ValueError("invalid presentation sidecar: " + "; ".join(errors))
    sidecar_path = presentation_sidecar_path(note_path=note_path)
    payload = json.dumps(presentation, ensure_ascii=False, indent=2, sort_keys=False)
    sidecar_path.write_text(payload + "\n", encoding="utf-8")
    return sidecar_path


__all__ = [
    "PRESENTATION_SCHEMA_VERSION",
    "build_idea_presentation_v2",
    "build_trend_presentation_v2",
    "idea_display_labels",
    "presentation_sidecar_path",
    "resolve_presentation_language_code",
    "trend_display_labels",
    "validate_presentation",
    "write_presentation_sidecar",
]
