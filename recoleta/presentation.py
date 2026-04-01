from __future__ import annotations

import json
from collections.abc import Sequence
from pathlib import Path
import re
from typing import Any, Mapping

PRESENTATION_SCHEMA_VERSION = 1

_HISTORY_WINDOW_MENTION_RE = re.compile(r"(?<![\w\[])(prev_\d+)(?![\w\]])", re.IGNORECASE)
_PLACEHOLDER_TOKEN_RE = re.compile(r"\bprev_?\d+\b", re.IGNORECASE)
_LOCALIZED_LANGUAGE_SEGMENT_RE = re.compile(r"^[A-Za-z]{2,3}(?:[-_][A-Za-z0-9]{2,8})*$")
_LOCALIZED_SURFACE_DIRS = {"Inbox", "Trends", "Ideas", "site"}
_RAW_IDEA_ENUMS = {
    "new_build",
    "revival",
    "research_gap",
    "tooling_wedge",
    "workflow_shift",
    "now",
    "near",
    "frontier",
}
_RAW_LABEL_PATTERNS = (
    re.compile(r"(?im)(?:^|\n)\s*(?:[-*]\s*)?kind:\s+\S"),
    re.compile(r"(?im)(?:^|\n)\s*(?:[-*]\s*)?time horizon:\s+\S"),
    re.compile(r"(?im)(?:^|\n)\s*(?:[-*]\s*)?user/job:\s+\S"),
    re.compile(r"(?im)(?:^|\n)\s*(?:\*\*)?thesis(?:\.\*\*|\.)\s+\S"),
)
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

_TREND_DISPLAY_LABELS_BY_LANGUAGE = {
    "en": {
        "overview": "Overview",
        "top_shifts": "Top shifts",
        "counter_signal": "Counter-signal",
        "clusters": "Clusters",
        "representative_sources": "Representative sources",
        "source_type": "Source type",
        "confidence": "Confidence",
    },
    "zh-CN": {
        "overview": "概览",
        "top_shifts": "重点变化",
        "counter_signal": "反向信号",
        "clusters": "聚类",
        "representative_sources": "代表来源",
        "source_type": "来源类型",
        "confidence": "置信度",
    },
}

_IDEA_DISPLAY_LABELS_BY_LANGUAGE = {
    "en": {
        "summary": "Summary",
        "opportunities": "Opportunities",
        "best_bet": "Best bet",
        "alternate": "Alternate",
        "type": "Type",
        "horizon": "Horizon",
        "role": "Role",
        "thesis": "Thesis",
        "why_now": "Why now",
        "what_changed": "What changed",
        "validation_next_step": "Validation next step",
        "evidence": "Evidence",
        "source_type": "Source type",
        "confidence": "Confidence",
    },
    "zh-CN": {
        "summary": "摘要",
        "opportunities": "机会",
        "best_bet": "首要机会",
        "alternate": "备选机会",
        "type": "类型",
        "horizon": "时间范围",
        "role": "适用角色",
        "thesis": "核心判断",
        "why_now": "为什么是现在",
        "what_changed": "发生了什么变化",
        "validation_next_step": "下一步验证",
        "evidence": "证据",
        "source_type": "来源类型",
        "confidence": "置信度",
    },
}

TREND_DISPLAY_LABELS_V1 = dict(_TREND_DISPLAY_LABELS_BY_LANGUAGE["en"])
IDEA_DISPLAY_LABELS_V1 = dict(_IDEA_DISPLAY_LABELS_BY_LANGUAGE["en"])

_IDEA_REQUIRED_DISPLAY_LABEL_KEYS = {
    "summary",
    "opportunities",
    "best_bet",
    "alternate",
    "type",
    "horizon",
    "role",
    "thesis",
    "why_now",
    "what_changed",
    "validation_next_step",
    "evidence",
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

_TREND_REQUIRED_CONTENT_KEYS = {
    "title",
    "hero",
    "overview",
    "ranked_shifts",
    "clusters",
    "representative_sources",
}
_TREND_REQUIRED_HERO_KEYS = {"kicker", "dek"}
_TREND_REQUIRED_SHIFT_KEYS = {"rank", "title", "summary", "history_refs", "evidence"}
_IDEA_REQUIRED_CONTENT_KEYS = {"title", "summary", "opportunities"}
_IDEA_REQUIRED_OPPORTUNITY_KEYS = {
    "rank",
    "tier",
    "title",
    "kind",
    "time_horizon",
    "display_kind",
    "display_time_horizon",
    "role",
    "thesis",
    "why_now",
    "what_changed",
    "validation_next_step",
    "evidence",
}


def _single_line(value: Any) -> str:
    return " ".join(str(value or "").split()).strip()


def _normalize_markdown(value: Any) -> str:
    text = str(value or "").replace("\r\n", "\n").strip()
    lines = [line.rstrip() for line in text.splitlines()]
    return "\n".join(lines).strip()


def _value_from(raw: Any, key: str, default: Any = None) -> Any:
    if isinstance(raw, Mapping):
        return raw.get(key, default)
    return getattr(raw, key, default)


def _int_or_none(value: Any) -> int | None:
    try:
        normalized = int(value)
    except Exception:
        return None
    return normalized


def _float_or_none(value: Any) -> float | None:
    try:
        normalized = float(value)
    except Exception:
        return None
    return normalized


def _history_window_display_text(
    *,
    window: str,
    history_window_refs: Mapping[str, Mapping[str, Any]] | None,
) -> str:
    ref = (history_window_refs or {}).get(window)
    if not isinstance(ref, Mapping):
        normalized_window = _single_line(window).lower()
        for candidate_key, candidate_ref in (history_window_refs or {}).items():
            if _single_line(candidate_key).lower() != normalized_window:
                continue
            ref = candidate_ref
            break
    if not isinstance(ref, Mapping):
        return ""
    title = _single_line(ref.get("title") or "")
    label = _single_line(ref.get("label") or "")
    if title and label and label not in title:
        return f"{title} ({label})"
    return title or label


def _render_history_refs_in_text(
    text: Any,
    *,
    history_window_refs: Mapping[str, Mapping[str, Any]] | None = None,
) -> str:
    raw = _normalize_markdown(text)
    if not raw:
        return raw

    def _replace(match: re.Match[str]) -> str:
        token = str(match.group(1) or "").strip()
        display = _history_window_display_text(
            window=token,
            history_window_refs=history_window_refs,
        )
        return display or token

    replaced = _HISTORY_WINDOW_MENTION_RE.sub(_replace, raw)
    normalized_lines: list[str] = []
    for line in replaced.splitlines():
        if not line.strip():
            normalized_lines.append("")
            continue
        indent_match = re.match(r"^[ \t]*", line)
        indent = indent_match.group(0) if indent_match is not None else ""
        body = line[len(indent) :]
        normalized_body = re.sub(r"[ \t]+([,.;:!?])", r"\1", re.sub(r"[ \t]{2,}", " ", body))
        normalized_lines.append(f"{indent}{normalized_body.rstrip()}")
    normalized = "\n".join(normalized_lines)
    normalized = re.sub(r"\n{3,}", "\n\n", normalized)
    return normalized.strip()


def _display_language_family(language_code: str | None) -> str:
    normalized = resolve_presentation_language_code(language_code=language_code)
    if normalized and normalized.lower().startswith("zh"):
        return "zh-CN"
    return "en"


def trend_display_labels(*, language_code: str | None = None) -> dict[str, str]:
    family = _display_language_family(language_code)
    return dict(_TREND_DISPLAY_LABELS_BY_LANGUAGE.get(family, TREND_DISPLAY_LABELS_V1))


def idea_display_labels(*, language_code: str | None = None) -> dict[str, str]:
    family = _display_language_family(language_code)
    return dict(_IDEA_DISPLAY_LABELS_BY_LANGUAGE.get(family, IDEA_DISPLAY_LABELS_V1))


def display_idea_kind(value: str, *, language_code: str | None = None) -> str:
    labels_by_language = {
        "en": {
            "new_build": "New build",
            "revival": "Revival",
            "research_gap": "Research gap",
            "tooling_wedge": "Tooling wedge",
            "workflow_shift": "Workflow shift",
        },
        "zh-CN": {
            "new_build": "新建设想",
            "revival": "重新激活",
            "research_gap": "研究空白",
            "tooling_wedge": "工具切入点",
            "workflow_shift": "工作流转变",
        },
    }
    labels = labels_by_language.get(
        _display_language_family(language_code),
        labels_by_language["en"],
    )
    normalized = _single_line(value).lower()
    return labels.get(normalized, _single_line(value))


def display_idea_time_horizon(value: str, *, language_code: str | None = None) -> str:
    labels_by_language = {
        "en": {
            "now": "Now",
            "near": "Near-term",
            "frontier": "Frontier",
        },
        "zh-CN": {
            "now": "现在",
            "near": "近期",
            "frontier": "前沿",
        },
    }
    labels = labels_by_language.get(
        _display_language_family(language_code),
        labels_by_language["en"],
    )
    normalized = _single_line(value).lower()
    return labels.get(normalized, _single_line(value))


def display_idea_tier(rank: int, *, language_code: str | None = None) -> str:
    labels = idea_display_labels(language_code=language_code)
    return labels["best_bet"] if int(rank) == 1 else labels["alternate"]


def _normalize_source_type(value: Any) -> str:
    normalized = _single_line(value).lower().replace("-", "_").replace(" ", "_")
    if normalized:
        if normalized in _DEFAULT_CONFIDENCE_BY_SOURCE_TYPE:
            return normalized
        return _SOURCE_TYPE_BY_SOURCE.get(normalized, normalized)
    return "unknown"


def _project_source_type(raw_source: Any) -> str:
    explicit = _normalize_source_type(_value_from(raw_source, "source_type", ""))
    if explicit and explicit != "unknown":
        return explicit
    return _normalize_source_type(_value_from(raw_source, "source", ""))


def _project_confidence(raw_source: Any, *, source_type: str) -> str:
    explicit = _single_line(_value_from(raw_source, "confidence", "")).lower()
    if explicit in {"high", "medium", "low"}:
        return explicit
    score = _float_or_none(_value_from(raw_source, "score", None))
    if score is not None:
        if score >= 0.8:
            return "high"
        if score >= 0.5:
            return "medium"
        return "low"
    return _DEFAULT_CONFIDENCE_BY_SOURCE_TYPE.get(source_type, "low")


def _project_source_metadata(
    raw_source: Any,
    *,
    fallback_title: str | None = None,
    include_reason: bool = False,
) -> dict[str, Any]:
    doc_id = _int_or_none(_value_from(raw_source, "doc_id", None))
    chunk_index = _int_or_none(_value_from(raw_source, "chunk_index", 0))
    title = _single_line(_value_from(raw_source, "title", "") or fallback_title or "")
    if not title and doc_id is not None and doc_id > 0:
        title = f"Document {doc_id}"
    source_type = _project_source_type(raw_source)
    href = _single_line(
        _value_from(raw_source, "href", "") or _value_from(raw_source, "note_href", "")
    )
    url = _single_line(_value_from(raw_source, "url", ""))
    projected = {
        "title": title,
        "href": href or url or None,
        "url": url or None,
        "authors": [
            _single_line(author)
            for author in list(_value_from(raw_source, "authors", []) or [])
            if _single_line(author)
        ],
        "doc_id": doc_id,
        "chunk_index": 0 if chunk_index is None else chunk_index,
        "source_type": source_type,
        "confidence": _project_confidence(raw_source, source_type=source_type),
    }
    if include_reason:
        reasons = [
            _normalize_markdown(reason)
            for reason in list(_value_from(raw_source, "reasons", []) or [])
            if _normalize_markdown(reason)
        ]
        reason = _normalize_markdown(_value_from(raw_source, "reason", "") or "")
        if reasons:
            projected["reasons"] = reasons
        if reason:
            projected["reason"] = reason
        elif reasons:
            projected["reason"] = reasons[0]
    return projected


def _canonicalize_language_code(value: Any) -> str | None:
    normalized = _single_line(value).replace("_", "-")
    if not normalized or _LOCALIZED_LANGUAGE_SEGMENT_RE.fullmatch(normalized) is None:
        return None
    parts = normalized.split("-")
    canonical = [parts[0].lower()]
    for part in parts[1:]:
        if len(part) == 2 and part.isalpha():
            canonical.append(part.upper())
        elif len(part) == 4 and part.isalpha():
            canonical.append(part.title())
        else:
            canonical.append(part)
    return "-".join(canonical)


def resolve_presentation_language_code(
    *,
    language_code: Any = None,
    output_language: Any = None,
) -> str | None:
    explicit = _canonicalize_language_code(language_code)
    if explicit is not None:
        return explicit
    direct_output_code = _canonicalize_language_code(output_language)
    if direct_output_code is not None:
        return direct_output_code
    normalized_label = _single_line(output_language).lower()
    mapped_code = _LANGUAGE_LABEL_TO_CODE.get(normalized_label)
    if mapped_code is None:
        return None
    return _canonicalize_language_code(mapped_code)


def presentation_sidecar_path(*, note_path: Path) -> Path:
    return note_path.with_name(f"{note_path.stem}.presentation.json")


def is_localized_output_path(path: Path) -> bool:
    parts = path.expanduser().resolve().parts
    for index, part in enumerate(parts):
        if part != "Localized" or index + 1 >= len(parts):
            continue
        language_segment = parts[index + 1]
        if _LOCALIZED_LANGUAGE_SEGMENT_RE.fullmatch(language_segment) is None:
            continue
        if index + 2 >= len(parts):
            return True
        if parts[index + 2] in _LOCALIZED_SURFACE_DIRS:
            return True
    return False


def write_presentation_sidecar(*, note_path: Path, presentation: Mapping[str, Any]) -> Path:
    errors = validate_presentation_v1(presentation)
    if errors:
        raise ValueError("invalid presentation sidecar: " + "; ".join(errors))
    sidecar_path = presentation_sidecar_path(note_path=note_path)
    payload = json.dumps(presentation, indent=2, ensure_ascii=False) + "\n"
    sidecar_path.write_text(payload, encoding="utf-8")
    return sidecar_path


def _project_cluster_representative_sources(
    raw_representative_chunks: Any,
) -> list[dict[str, Any]]:
    if not isinstance(raw_representative_chunks, Sequence):
        return []
    projected: list[dict[str, Any]] = []
    seen_targets: set[str] = set()
    for raw_rep in list(raw_representative_chunks)[:6]:
        title_value = _single_line(_value_from(raw_rep, "title", "") or "")
        href_value = _single_line(
            _value_from(raw_rep, "href", "") or _value_from(raw_rep, "note_href", "")
        )
        url_value = _single_line(_value_from(raw_rep, "url", "") or "")
        if not title_value:
            continue
        target = href_value or url_value or title_value
        if target in seen_targets:
            continue
        seen_targets.add(target)
        projected.append(_project_source_metadata(raw_rep, fallback_title=title_value))
    return projected


def _project_idea_evidence(raw_evidence_refs: Any) -> list[dict[str, Any]]:
    if not isinstance(raw_evidence_refs, Sequence):
        return []
    ordered: list[tuple[str, Any]] = []
    grouped: dict[int, list[Any]] = {}
    for raw_ref in list(raw_evidence_refs):
        doc_id = _int_or_none(_value_from(raw_ref, "doc_id", None))
        if doc_id is None or doc_id <= 0:
            ordered.append(("raw", raw_ref))
            continue
        if doc_id not in grouped:
            grouped[doc_id] = []
            ordered.append(("doc", doc_id))
        grouped[doc_id].append(raw_ref)

    projected: list[dict[str, Any]] = []
    for kind, value in ordered:
        refs = [value] if kind == "raw" else grouped.get(int(value), [])
        if not refs:
            continue
        reasons: list[str] = []
        seen_reasons: set[str] = set()
        for ref in refs:
            normalized_reason = _normalize_markdown(_value_from(ref, "reason", "") or "")
            if normalized_reason and normalized_reason not in seen_reasons:
                seen_reasons.add(normalized_reason)
                reasons.append(normalized_reason)
        projected_ref = _project_source_metadata(
            refs[0],
            include_reason=True,
        )
        if reasons:
            projected_ref["reasons"] = reasons
            if not _normalize_markdown(projected_ref.get("reason") or ""):
                projected_ref["reason"] = reasons[0]
        projected.append(projected_ref)
    return projected


def build_trend_presentation_v1(
    *,
    source_markdown_path: str,
    title: str,
    overview_md: str,
    evolution: Mapping[str, Any] | None,
    history_window_refs: Mapping[str, Mapping[str, Any]] | None,
    clusters: Sequence[Mapping[str, Any]] | None,
    language_code: str | None = None,
    display_language_code: str | None = None,
) -> dict[str, Any]:
    resolved_language_code = resolve_presentation_language_code(language_code=language_code)
    resolved_display_language_code = resolve_presentation_language_code(
        language_code=display_language_code
    ) or resolved_language_code
    normalized_overview = _render_history_refs_in_text(
        overview_md,
        history_window_refs=history_window_refs,
    )
    hero_dek = _single_line(normalized_overview.split("\n", 1)[0]) or _single_line(title)
    ranked_shifts: list[dict[str, Any]] = []
    for index, raw_signal in enumerate(list((evolution or {}).get("signals") or [])[:3], start=1):
        if not isinstance(raw_signal, Mapping):
            continue
        history_refs = [
            _single_line(window)
            for window in list(raw_signal.get("history_windows") or [])
            if _single_line(window)
        ]
        ranked_shifts.append(
            {
                "rank": index,
                "title": _single_line(raw_signal.get("theme") or "") or f"Shift {index}",
                "summary": _render_history_refs_in_text(
                    raw_signal.get("summary") or "",
                    history_window_refs=history_window_refs,
                ),
                "history_refs": history_refs,
                "evidence": [],
            }
        )

    presentation_clusters: list[dict[str, Any]] = []
    representative_sources: list[dict[str, Any]] = []
    seen_rep_targets: set[str] = set()
    for raw_cluster in list(clusters or []):
        if not isinstance(raw_cluster, Mapping):
            continue
        reps = _project_cluster_representative_sources(
            raw_cluster.get("representative_chunks") or []
        )
        for rep in reps:
            target = (
                _single_line(rep.get("href") or "")
                or _single_line(rep.get("url") or "")
                or _single_line(rep.get("title") or "")
            )
            if target and target not in seen_rep_targets:
                representative_sources.append(rep)
                seen_rep_targets.add(target)
        presentation_clusters.append(
            {
                "title": _single_line(raw_cluster.get("name") or "") or "Cluster",
                "summary": _render_history_refs_in_text(
                    raw_cluster.get("description") or "",
                    history_window_refs=history_window_refs,
                ),
                "representative_sources": reps,
            }
        )

    return {
        "presentation_schema_version": PRESENTATION_SCHEMA_VERSION,
        "surface_kind": "trend",
        "language_code": resolved_language_code,
        "source_markdown_path": source_markdown_path,
        "display_labels": trend_display_labels(
            language_code=resolved_display_language_code
        ),
        "content": {
            "title": _single_line(title),
            "hero": {
                "kicker": "Trend brief",
                "dek": hero_dek,
            },
            "overview": normalized_overview,
            "ranked_shifts": ranked_shifts,
            "counter_signal": None,
            "clusters": presentation_clusters,
            "representative_sources": representative_sources,
        },
    }


def build_idea_presentation_v1(
    *,
    source_markdown_path: str,
    title: str,
    summary_md: str,
    ideas: list[Any],
    language_code: str | None = None,
    display_language_code: str | None = None,
) -> dict[str, Any]:
    resolved_language_code = resolve_presentation_language_code(language_code=language_code)
    resolved_display_language_code = resolve_presentation_language_code(
        language_code=display_language_code
    ) or resolved_language_code
    opportunities: list[dict[str, Any]] = []
    for index, idea in enumerate(list(ideas or [])[:3], start=1):
        opportunities.append(
            {
                "rank": index,
                "tier": "best_bet" if index == 1 else "alternate",
                "title": _single_line(_value_from(idea, "title", "") or ""),
                "kind": _single_line(_value_from(idea, "kind", "") or ""),
                "time_horizon": _single_line(_value_from(idea, "time_horizon", "") or ""),
                "display_kind": display_idea_kind(
                    str(_value_from(idea, "kind", "") or ""),
                    language_code=resolved_display_language_code,
                ),
                "display_time_horizon": display_idea_time_horizon(
                    str(_value_from(idea, "time_horizon", "") or ""),
                    language_code=resolved_display_language_code,
                ),
                "role": _normalize_markdown(_value_from(idea, "user_or_job", "") or ""),
                "thesis": _normalize_markdown(_value_from(idea, "thesis", "") or ""),
                "why_now": _normalize_markdown(_value_from(idea, "why_now", "") or ""),
                "what_changed": _normalize_markdown(
                    _value_from(idea, "what_changed", "") or ""
                ),
                "validation_next_step": _normalize_markdown(
                    _value_from(idea, "validation_next_step", "") or ""
                ),
                "evidence": _project_idea_evidence(
                    list(_value_from(idea, "evidence_refs", []) or [])
                ),
            }
        )

    return {
        "presentation_schema_version": PRESENTATION_SCHEMA_VERSION,
        "surface_kind": "idea",
        "language_code": resolved_language_code,
        "source_markdown_path": source_markdown_path,
        "display_labels": idea_display_labels(
            language_code=resolved_display_language_code
        ),
        "content": {
            "title": _single_line(title),
            "summary": _normalize_markdown(summary_md),
            "opportunities": opportunities,
        },
    }


def _trend_user_visible_strings(presentation: Mapping[str, Any]) -> list[str]:
    content = presentation.get("content")
    if not isinstance(content, Mapping):
        return []
    strings = [
        _single_line(content.get("title") or ""),
        _normalize_markdown(((content.get("hero") or {}) if isinstance(content.get("hero"), Mapping) else {}).get("dek") or ""),
        _normalize_markdown(content.get("overview") or ""),
    ]
    for shift in list(content.get("ranked_shifts") or []):
        if not isinstance(shift, Mapping):
            continue
        strings.append(_single_line(shift.get("title") or ""))
        strings.append(_normalize_markdown(shift.get("summary") or ""))
    for cluster in list(content.get("clusters") or []):
        if not isinstance(cluster, Mapping):
            continue
        strings.append(_single_line(cluster.get("title") or ""))
        strings.append(_normalize_markdown(cluster.get("summary") or ""))
    return [value for value in strings if value]


def _idea_user_visible_strings(presentation: Mapping[str, Any]) -> list[str]:
    content = presentation.get("content")
    if not isinstance(content, Mapping):
        return []
    strings = [
        _single_line(content.get("title") or ""),
        _normalize_markdown(content.get("summary") or ""),
    ]
    for opportunity in list(content.get("opportunities") or []):
        if not isinstance(opportunity, Mapping):
            continue
        for key in (
            "title",
            "display_kind",
            "display_time_horizon",
            "role",
            "thesis",
            "why_now",
            "what_changed",
            "validation_next_step",
        ):
            value = opportunity.get(key)
            if value is not None:
                strings.append(_normalize_markdown(value))
    return [value for value in strings if value]


def _presentation_schema_version(value: Any) -> int | None:
    try:
        return int(value)
    except Exception:
        return None


def _validate_string_field(
    *,
    mapping: Mapping[str, Any],
    key: str,
    field_path: str,
    errors: list[str],
) -> None:
    if not isinstance(mapping.get(key), str):
        errors.append(f"{field_path} must be a string")


def _validate_int_like_field(
    *,
    mapping: Mapping[str, Any],
    key: str,
    field_path: str,
    errors: list[str],
) -> None:
    if _int_or_none(mapping.get(key)) is None:
        errors.append(f"{field_path} must be an integer")


def validate_presentation_v1(presentation: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if (
        _presentation_schema_version(presentation.get("presentation_schema_version"))
        != PRESENTATION_SCHEMA_VERSION
    ):
        errors.append("presentation_schema_version must be 1")
    source_markdown_path = _single_line(presentation.get("source_markdown_path") or "")
    if not source_markdown_path.endswith(".md"):
        errors.append("source_markdown_path must point to a markdown note")
    display_labels = presentation.get("display_labels")
    if not isinstance(display_labels, Mapping):
        errors.append("display_labels must be a mapping")
    elif any(not isinstance(value, str) for value in display_labels.values()):
        errors.append("display_labels values must be strings")
    content = presentation.get("content")
    if not isinstance(content, Mapping):
        errors.append("content must be a mapping")

    surface_kind = _single_line(presentation.get("surface_kind") or "")
    if surface_kind == "trend":
        expected_labels = set(TREND_DISPLAY_LABELS_V1)
        if isinstance(display_labels, Mapping):
            missing_labels = sorted(expected_labels - set(display_labels))
            if missing_labels:
                errors.append(
                    "trend display_labels must include: " + ", ".join(missing_labels)
                )
        if isinstance(content, Mapping):
            missing_content = sorted(_TREND_REQUIRED_CONTENT_KEYS - set(content))
            if missing_content:
                errors.append(
                    "trend content must include: " + ", ".join(missing_content)
                )
            for key in ("title", "overview"):
                _validate_string_field(
                    mapping=content,
                    key=key,
                    field_path=f"trend content.{key}",
                    errors=errors,
                )
            hero = content.get("hero")
            if not isinstance(hero, Mapping):
                errors.append("trend hero must be a mapping")
            else:
                missing_hero = sorted(_TREND_REQUIRED_HERO_KEYS - set(hero))
                if missing_hero:
                    errors.append(
                        "trend hero must include: " + ", ".join(missing_hero)
                    )
                for key in ("kicker", "dek"):
                    _validate_string_field(
                        mapping=hero,
                        key=key,
                        field_path=f"trend hero.{key}",
                        errors=errors,
                    )
            ranked_shifts = list(content.get("ranked_shifts") or [])
        else:
            ranked_shifts = []
        if len(ranked_shifts) > 3:
            errors.append("trend ranked_shifts must not exceed 3 entries")
        for shift in ranked_shifts:
            if not isinstance(shift, Mapping):
                errors.append("trend ranked_shifts entries must be mappings")
                break
            missing_shift = sorted(_TREND_REQUIRED_SHIFT_KEYS - set(shift))
            if missing_shift:
                errors.append(
                    "trend ranked_shifts entries must include: "
                    + ", ".join(missing_shift)
                )
                break
            for key in ("title", "summary"):
                _validate_string_field(
                    mapping=shift,
                    key=key,
                    field_path=f"trend ranked_shifts.{key}",
                    errors=errors,
                )
            _validate_int_like_field(
                mapping=shift,
                key="rank",
                field_path="trend ranked_shifts.rank",
                errors=errors,
            )
            history_refs = shift.get("history_refs")
            if not isinstance(history_refs, list) or any(
                not isinstance(item, str) for item in history_refs
            ):
                errors.append("trend ranked_shifts.history_refs must be a list of strings")
                break
        user_visible_strings = _trend_user_visible_strings(presentation)
    elif surface_kind == "idea":
        expected_labels = set(_IDEA_REQUIRED_DISPLAY_LABEL_KEYS)
        if isinstance(display_labels, Mapping):
            missing_labels = sorted(expected_labels - set(display_labels))
            if missing_labels:
                errors.append(
                    "idea display_labels must include: " + ", ".join(missing_labels)
                )
        if isinstance(content, Mapping):
            missing_content = sorted(_IDEA_REQUIRED_CONTENT_KEYS - set(content))
            if missing_content:
                errors.append(
                    "idea content must include: " + ", ".join(missing_content)
                )
            for key in ("title", "summary"):
                _validate_string_field(
                    mapping=content,
                    key=key,
                    field_path=f"idea content.{key}",
                    errors=errors,
                )
            opportunities = list(content.get("opportunities") or [])
        else:
            opportunities = []
        best_bet_total = sum(
            1
            for opportunity in opportunities
            if isinstance(opportunity, Mapping) and _single_line(opportunity.get("tier") or "") == "best_bet"
        )
        if opportunities and len(opportunities) > 3:
            errors.append("idea opportunities must not exceed 3 entries")
        if opportunities and best_bet_total != 1:
            errors.append("idea opportunities must contain exactly one best_bet")
        for opportunity in opportunities:
            if not isinstance(opportunity, Mapping):
                errors.append("idea opportunities entries must be mappings")
                break
            missing_opportunity = sorted(_IDEA_REQUIRED_OPPORTUNITY_KEYS - set(opportunity))
            if missing_opportunity:
                errors.append(
                    "idea opportunities must include: "
                    + ", ".join(missing_opportunity)
                )
                break
            for key in (
                "title",
                "tier",
                "kind",
                "time_horizon",
                "display_kind",
                "display_time_horizon",
                "role",
                "thesis",
                "why_now",
                "what_changed",
                "validation_next_step",
            ):
                _validate_string_field(
                    mapping=opportunity,
                    key=key,
                    field_path=f"idea opportunities.{key}",
                    errors=errors,
                )
            if _single_line(opportunity.get("display_kind") or "") in _RAW_IDEA_ENUMS:
                errors.append("display_kind must not leak raw idea enums")
                break
            if _single_line(opportunity.get("display_time_horizon") or "") in _RAW_IDEA_ENUMS:
                errors.append("display_time_horizon must not leak raw idea enums")
                break
        user_visible_strings = _idea_user_visible_strings(presentation)
    else:
        errors.append("surface_kind must be trend or idea")
        user_visible_strings = []

    for value in user_visible_strings:
        if _PLACEHOLDER_TOKEN_RE.search(value):
            errors.append("user-visible fields must not contain raw history placeholder tokens")
            break
    lowered_strings = "\n".join(user_visible_strings).lower()
    for pattern in _RAW_LABEL_PATTERNS:
        if pattern.search(lowered_strings):
            errors.append("user-visible fields must not leak raw schema labels")
            break
    return errors


__all__ = [
    "IDEA_DISPLAY_LABELS_V1",
    "PRESENTATION_SCHEMA_VERSION",
    "TREND_DISPLAY_LABELS_V1",
    "build_idea_presentation_v1",
    "build_trend_presentation_v1",
    "display_idea_kind",
    "display_idea_tier",
    "display_idea_time_horizon",
    "idea_display_labels",
    "is_localized_output_path",
    "presentation_sidecar_path",
    "resolve_presentation_language_code",
    "trend_display_labels",
    "validate_presentation_v1",
    "write_presentation_sidecar",
]
