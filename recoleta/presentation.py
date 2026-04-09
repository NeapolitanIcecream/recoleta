from __future__ import annotations

from dataclasses import dataclass
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
_DISALLOWED_EVIDENCE_KEYS = ("source_type", "confidence")


@dataclass(frozen=True, slots=True)
class TrendPresentationBuildRequest:
    source_markdown_path: str
    title: str
    overview_md: str
    clusters: Sequence[Any] | None
    language_code: str | None = None
    display_language_code: str | None = None


@dataclass(frozen=True, slots=True)
class IdeaPresentationBuildRequest:
    source_markdown_path: str
    title: str
    summary_md: str
    ideas: Sequence[Any]
    language_code: str | None = None
    display_language_code: str | None = None


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


def _evidence_groups(raw_sources: Any) -> list[list[Any]]:
    if not isinstance(raw_sources, Sequence) or isinstance(raw_sources, (str, bytes)):
        return []
    grouped_by_doc_id: dict[int, list[Any]] = {}
    ordered_groups: list[list[Any]] = []
    for raw_source in raw_sources:
        doc_id = _int_or_none(_value_from(raw_source, "doc_id", None))
        if doc_id is None or doc_id <= 0:
            ordered_groups.append([raw_source])
            continue
        refs = grouped_by_doc_id.get(doc_id)
        if refs is None:
            refs = []
            grouped_by_doc_id[doc_id] = refs
            ordered_groups.append(refs)
        refs.append(raw_source)
    return ordered_groups


def _merged_evidence_reasons(refs: Sequence[Any]) -> tuple[list[str], str | None]:
    return _normalize_reasons(
        {"reasons": [_value_from(ref, "reason", "") for ref in refs]}
    )


def _project_evidence_group(refs: Sequence[Any]) -> dict[str, Any]:
    entry = _project_evidence_entry(refs[0])
    reasons, reason = _merged_evidence_reasons(refs)
    if reasons:
        entry["reasons"] = reasons
    if reason:
        entry["reason"] = reason
    return entry


def _project_evidence(raw_sources: Any) -> list[dict[str, Any]]:
    return [
        _project_evidence_group(refs)
        for refs in _evidence_groups(raw_sources)
        if refs
    ]


def _canonical_language_code(value: str) -> str:
    normalized = value.lower()
    if normalized == "zh-cn":
        return "zh-CN"
    if normalized == "zh-tw":
        return "zh-TW"
    return value


def _normalized_language_code_candidate(value: Any) -> str | None:
    normalized = _single_line(value)
    if not normalized:
        return None
    normalized = normalized.replace("_", "-")
    if not _LOCALIZED_LANGUAGE_SEGMENT_RE.match(normalized):
        return None
    return _canonical_language_code(normalized)


def _language_code_from_output_language(output_language: Any) -> str | None:
    normalized_output = _single_line(output_language).lower()
    if not normalized_output:
        return None
    mapped = _LANGUAGE_LABEL_TO_CODE.get(normalized_output)
    if mapped is not None:
        return mapped
    return _normalized_language_code_candidate(normalized_output)


def resolve_presentation_language_code(
    *,
    language_code: str | None = None,
    output_language: str | None = None,
) -> str | None:
    return _normalized_language_code_candidate(language_code) or (
        _language_code_from_output_language(output_language)
    )


def trend_display_labels(*, language_code: str | None = None) -> dict[str, str]:
    _ = language_code
    return dict(_TREND_DISPLAY_LABELS)


def idea_display_labels(*, language_code: str | None = None) -> dict[str, str]:
    _ = language_code
    return dict(_IDEA_DISPLAY_LABELS)


def _trend_clusters_content(clusters: Sequence[Any] | None) -> list[dict[str, Any]]:
    return [
        {
            "title": _single_line(_value_from(cluster, "title", "")),
            "content": _normalize_markdown(_value_from(cluster, "content_md", "")),
            "evidence": _project_evidence(_value_from(cluster, "evidence_refs", [])),
        }
        for cluster in list(clusters or [])
    ]


def _idea_blocks_content(ideas: Sequence[Any]) -> list[dict[str, Any]]:
    return [
        {
            "title": _single_line(_value_from(idea, "title", "")),
            "content": _normalize_markdown(_value_from(idea, "content_md", "")),
            "evidence": _project_evidence(_value_from(idea, "evidence_refs", [])),
        }
        for idea in list(ideas or [])[:3]
    ]


def _build_presentation_shell(
    *,
    surface_kind: str,
    source_markdown_path: str,
    language_code: str | None,
    display_labels: dict[str, str],
    content: dict[str, Any],
) -> dict[str, Any]:
    return {
        "presentation_schema_version": PRESENTATION_SCHEMA_VERSION,
        "surface_kind": surface_kind,
        "language_code": language_code,
        "source_markdown_path": _single_line(source_markdown_path),
        "display_labels": display_labels,
        "content": content,
    }


def build_trend_presentation_v2(
    *,
    request: TrendPresentationBuildRequest,
) -> dict[str, Any]:
    resolved_language_code = resolve_presentation_language_code(
        language_code=request.language_code
    )
    return _build_presentation_shell(
        surface_kind="trend",
        source_markdown_path=request.source_markdown_path,
        language_code=resolved_language_code,
        display_labels=trend_display_labels(
            language_code=request.display_language_code
        ),
        content={
            "title": _single_line(request.title),
            "overview": _normalize_markdown(request.overview_md),
            "clusters": _trend_clusters_content(request.clusters),
        },
    )


def build_idea_presentation_v2(
    *,
    request: IdeaPresentationBuildRequest,
) -> dict[str, Any]:
    resolved_language_code = resolve_presentation_language_code(
        language_code=request.language_code
    )
    return _build_presentation_shell(
        surface_kind="idea",
        source_markdown_path=request.source_markdown_path,
        language_code=resolved_language_code,
        display_labels=idea_display_labels(language_code=request.display_language_code),
        content={
            "title": _single_line(request.title),
            "summary": _normalize_markdown(request.summary_md),
            "ideas": _idea_blocks_content(request.ideas),
        },
    )


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


def _validate_optional_string(
    value: Any,
    *,
    field_path: str,
    errors: list[str],
    allow_empty: bool = True,
) -> None:
    if value is None:
        return
    if not isinstance(value, str) or (not allow_empty and not value.strip()):
        expectation = "a string" if allow_empty else "a non-empty string"
        errors.append(f"{field_path} must be {expectation}")


def _validate_optional_int(
    value: Any,
    *,
    field_path: str,
    minimum: int,
    errors: list[str],
    expectation: str,
) -> None:
    if value is None:
        return
    if not isinstance(value, int) or value < minimum:
        errors.append(f"{field_path} must be {expectation}")


def _validate_optional_string_list(
    value: Any,
    *,
    field_path: str,
    errors: list[str],
    require_non_empty: bool = False,
) -> None:
    if value is None:
        return
    if not isinstance(value, list):
        errors.append(f"{field_path} must be a list of strings")
        return
    for entry in value:
        if not isinstance(entry, str) or (require_non_empty and not entry.strip()):
            errors.append(f"{field_path} must be a list of strings")
            return


def _validate_disallowed_evidence_keys(
    entry: Mapping[str, Any],
    *,
    field_path: str,
    errors: list[str],
) -> None:
    for key in _DISALLOWED_EVIDENCE_KEYS:
        if key in entry:
            errors.append(f"{field_path}.{key} is not allowed")


def _validate_evidence_entry(
    entry: Any,
    *,
    field_path: str,
    errors: list[str],
) -> None:
    if not isinstance(entry, Mapping):
        errors.append(f"{field_path} must be a mapping")
        return
    _validate_required_string(
        entry.get("title"),
        field_path=f"{field_path}.title",
        errors=errors,
    )
    _validate_optional_string(entry.get("href"), field_path=f"{field_path}.href", errors=errors)
    _validate_optional_string(entry.get("url"), field_path=f"{field_path}.url", errors=errors)
    _validate_optional_int(
        entry.get("doc_id"),
        field_path=f"{field_path}.doc_id",
        minimum=1,
        errors=errors,
        expectation="a positive integer",
    )
    _validate_optional_int(
        entry.get("chunk_index"),
        field_path=f"{field_path}.chunk_index",
        minimum=0,
        errors=errors,
        expectation=">= 0",
    )
    _validate_optional_string_list(
        entry.get("authors"),
        field_path=f"{field_path}.authors",
        errors=errors,
    )
    _validate_optional_string_list(
        entry.get("reasons"),
        field_path=f"{field_path}.reasons",
        errors=errors,
        require_non_empty=True,
    )
    _validate_optional_string(
        entry.get("reason"),
        field_path=f"{field_path}.reason",
        errors=errors,
        allow_empty=False,
    )
    _validate_disallowed_evidence_keys(entry, field_path=field_path, errors=errors)


def _validate_evidence_entries(
    entries: Any, *, field_path: str, errors: list[str]
) -> None:
    if not isinstance(entries, list):
        errors.append(f"{field_path} must be a list")
        return
    for index, entry in enumerate(entries):
        _validate_evidence_entry(
            entry,
            field_path=f"{field_path}[{index}]",
            errors=errors,
        )


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
    "IdeaPresentationBuildRequest",
    "PRESENTATION_SCHEMA_VERSION",
    "TrendPresentationBuildRequest",
    "build_idea_presentation_v2",
    "build_trend_presentation_v2",
    "idea_display_labels",
    "presentation_sidecar_path",
    "resolve_presentation_language_code",
    "trend_display_labels",
    "validate_presentation",
    "write_presentation_sidecar",
]
