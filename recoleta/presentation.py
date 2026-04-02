from __future__ import annotations

import json
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any, Mapping, TypedDict, Unpack

PRESENTATION_SCHEMA_VERSION_V1 = 1
PRESENTATION_SCHEMA_VERSION = 2
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
_VALID_CONFIDENCE_LEVELS = {"high", "medium", "low"}

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
    "zh-TW": {
        "overview": "概覽",
        "top_shifts": "重點變化",
        "counter_signal": "反向訊號",
        "clusters": "聚類",
        "representative_sources": "代表來源",
        "source_type": "來源類型",
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
        "anti_thesis": "Anti-thesis",
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
        "anti_thesis": "不成立条件",
        "why_now": "为什么是现在",
        "what_changed": "发生了什么变化",
        "validation_next_step": "下一步验证",
        "evidence": "证据",
        "source_type": "来源类型",
        "confidence": "置信度",
    },
    "zh-TW": {
        "summary": "摘要",
        "opportunities": "機會",
        "best_bet": "首要機會",
        "alternate": "備選機會",
        "type": "類型",
        "horizon": "時間範圍",
        "role": "適用角色",
        "thesis": "核心判斷",
        "anti_thesis": "不成立條件",
        "why_now": "為什麼是現在",
        "what_changed": "發生了什麼變化",
        "validation_next_step": "下一步驗證",
        "evidence": "證據",
        "source_type": "來源類型",
        "confidence": "置信度",
    },
}

TREND_DISPLAY_LABELS_V1 = dict(_TREND_DISPLAY_LABELS_BY_LANGUAGE["en"])
IDEA_DISPLAY_LABELS_V1 = {
    key: value
    for key, value in _IDEA_DISPLAY_LABELS_BY_LANGUAGE["en"].items()
    if key != "anti_thesis"
}
IDEA_DISPLAY_LABELS_V2 = dict(_IDEA_DISPLAY_LABELS_BY_LANGUAGE["en"])

_IDEA_REQUIRED_DISPLAY_LABEL_KEYS = {
    "summary",
    "opportunities",
    "best_bet",
    "alternate",
    "type",
    "horizon",
    "role",
    "thesis",
    "anti_thesis",
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

_TREND_REQUIRED_CONTENT_KEYS_V1 = {
    "title",
    "hero",
    "overview",
    "ranked_shifts",
    "clusters",
    "representative_sources",
}
_TREND_REQUIRED_CONTENT_KEYS_V2 = _TREND_REQUIRED_CONTENT_KEYS_V1 | {"counter_signal"}
_TREND_REQUIRED_HERO_KEYS = {"kicker", "dek"}
_TREND_REQUIRED_SHIFT_KEYS = {"rank", "title", "summary", "history_refs", "evidence"}
_IDEA_REQUIRED_CONTENT_KEYS = {"title", "summary", "opportunities"}
_IDEA_REQUIRED_OPPORTUNITY_KEYS_V1 = {
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
_IDEA_REQUIRED_OPPORTUNITY_KEYS_V2 = _IDEA_REQUIRED_OPPORTUNITY_KEYS_V1 | {
    "anti_thesis"
}


class _TrendPresentationKwargs(TypedDict):
    source_markdown_path: str
    title: str
    overview_md: str
    evolution: Mapping[str, Any] | None
    history_window_refs: Mapping[str, Mapping[str, Any]] | None
    clusters: Sequence[Mapping[str, Any]] | None
    language_code: str | None
    display_language_code: str | None


class _TrendPresentationV2Kwargs(_TrendPresentationKwargs, total=False):
    counter_signal: Mapping[str, Any] | None


class _IdeaPresentationKwargs(TypedDict):
    source_markdown_path: str
    title: str
    summary_md: str
    ideas: list[Any]
    language_code: str | None
    display_language_code: str | None


_TREND_PRESENTATION_REQUIRED_KEYS = (
    "source_markdown_path",
    "title",
    "overview_md",
    "evolution",
    "history_window_refs",
    "clusters",
)
_TREND_PRESENTATION_V1_DEFAULTS: dict[str, Any] = {
    "language_code": None,
    "display_language_code": None,
}
_TREND_PRESENTATION_V2_DEFAULTS: dict[str, Any] = {
    **_TREND_PRESENTATION_V1_DEFAULTS,
    "counter_signal": None,
}
_IDEA_PRESENTATION_REQUIRED_KEYS = (
    "source_markdown_path",
    "title",
    "summary_md",
    "ideas",
)
_IDEA_PRESENTATION_DEFAULTS: dict[str, Any] = {
    "language_code": None,
    "display_language_code": None,
}


@dataclass(frozen=True, slots=True)
class _TrendPresentationBuildInput:
    source_markdown_path: str
    title: str
    overview_md: str
    evolution: Mapping[str, Any] | None
    history_window_refs: Mapping[str, Mapping[str, Any]] | None
    clusters: Sequence[Mapping[str, Any]] | None
    counter_signal: Mapping[str, Any] | None
    schema_version: int
    language_code: str | None
    display_language_code: str | None


@dataclass(frozen=True, slots=True)
class _IdeaPresentationBuildInput:
    source_markdown_path: str
    title: str
    summary_md: str
    ideas: list[Any]
    schema_version: int
    language_code: str | None
    display_language_code: str | None


def _single_line(value: Any) -> str:
    return " ".join(str(value or "").split()).strip()


def _normalize_markdown(value: Any) -> str:
    text = str(value or "").replace("\r\n", "\n").strip()
    lines = [line.rstrip() for line in text.splitlines()]
    return "\n".join(lines).strip()


def _first_markdown_paragraph(value: Any) -> str:
    normalized = _normalize_markdown(value)
    if not normalized:
        return ""
    for part in re.split(r"\n\s*\n", normalized):
        candidate = _normalize_markdown(part)
        if candidate and not candidate.startswith("#"):
            return candidate
    return normalized


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
    if normalized:
        lowered = normalized.lower()
        if lowered.startswith("zh-tw") or "-hant" in lowered or lowered.startswith(
            ("zh-hk", "zh-mo")
        ):
            return "zh-TW"
    if normalized and normalized.lower().startswith("zh"):
        return "zh-CN"
    return "en"


def trend_display_labels(*, language_code: str | None = None) -> dict[str, str]:
    family = _display_language_family(language_code)
    return dict(_TREND_DISPLAY_LABELS_BY_LANGUAGE.get(family, TREND_DISPLAY_LABELS_V1))


def idea_display_labels(
    *,
    language_code: str | None = None,
    schema_version: int = PRESENTATION_SCHEMA_VERSION,
) -> dict[str, str]:
    family = _display_language_family(language_code)
    labels = dict(_IDEA_DISPLAY_LABELS_BY_LANGUAGE.get(family, IDEA_DISPLAY_LABELS_V2))
    if int(schema_version) <= PRESENTATION_SCHEMA_VERSION_V1:
        labels.pop("anti_thesis", None)
    return labels


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
        "zh-TW": {
            "new_build": "新建設想",
            "revival": "重新激活",
            "research_gap": "研究空白",
            "tooling_wedge": "工具切入點",
            "workflow_shift": "工作流轉變",
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
        "zh-TW": {
            "now": "現在",
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
    errors = validate_presentation(presentation)
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


def _project_counter_signal(raw_counter_signal: Any) -> dict[str, Any] | None:
    if not isinstance(raw_counter_signal, Mapping):
        return None
    title = _single_line(raw_counter_signal.get("title") or "")
    summary = _normalize_markdown(raw_counter_signal.get("summary") or "")
    evidence = _project_idea_evidence(
        raw_counter_signal.get("evidence_refs")
        or raw_counter_signal.get("evidence")
        or []
    )
    if not title and not summary and not evidence:
        return None
    return {
        "title": title,
        "summary": summary,
        "evidence": evidence,
    }


def _fallback_ranked_shift(
    *,
    title: str,
    overview_md: str,
    clusters: Sequence[Mapping[str, Any]] | None,
    history_window_refs: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any] | None:
    for raw_cluster in list(clusters or []):
        if not isinstance(raw_cluster, Mapping):
            continue
        cluster_title = _single_line(raw_cluster.get("name") or "")
        cluster_summary = _render_history_refs_in_text(
            raw_cluster.get("description") or "",
            history_window_refs=history_window_refs,
        )
        if cluster_title and cluster_summary:
            return {
                "rank": 1,
                "title": cluster_title,
                "summary": cluster_summary,
                "history_refs": [],
                "evidence": [],
            }
    summary = _first_markdown_paragraph(overview_md)
    if not summary:
        return None
    return {
        "rank": 1,
        "title": _single_line(title) or "Key shift",
        "summary": summary,
        "history_refs": [],
        "evidence": [],
    }


def _resolve_presentation_languages(
    *,
    language_code: str | None,
    display_language_code: str | None,
) -> tuple[str | None, str | None]:
    resolved_language_code = resolve_presentation_language_code(
        language_code=language_code
    )
    resolved_display_language_code = resolve_presentation_language_code(
        language_code=display_language_code
    ) or resolved_language_code
    return resolved_language_code, resolved_display_language_code


def _trend_hero_dek(*, title: str, overview_md: str) -> str:
    return _single_line(overview_md.split("\n", 1)[0]) or _single_line(title)


def _trend_ranked_shifts(
    *,
    title: str,
    overview_md: str,
    evolution: Mapping[str, Any] | None,
    clusters: Sequence[Mapping[str, Any]] | None,
    history_window_refs: Mapping[str, Mapping[str, Any]] | None,
) -> list[dict[str, Any]]:
    ranked_shifts: list[dict[str, Any]] = []
    for index, raw_signal in enumerate(list((evolution or {}).get("signals") or [])[:3], start=1):
        projected = _project_ranked_shift(
            index=index,
            raw_signal=raw_signal,
            history_window_refs=history_window_refs,
        )
        if projected is not None:
            ranked_shifts.append(projected)
    if ranked_shifts:
        return ranked_shifts
    fallback_shift = _fallback_ranked_shift(
        title=title,
        overview_md=overview_md,
        clusters=clusters,
        history_window_refs=history_window_refs,
    )
    return [fallback_shift] if fallback_shift is not None else []


def _project_ranked_shift(
    *,
    index: int,
    raw_signal: Any,
    history_window_refs: Mapping[str, Mapping[str, Any]] | None,
) -> dict[str, Any] | None:
    if not isinstance(raw_signal, Mapping):
        return None
    history_refs = [
        _single_line(window)
        for window in list(raw_signal.get("history_windows") or [])
        if _single_line(window)
    ]
    return {
        "rank": index,
        "title": _single_line(raw_signal.get("theme") or "") or f"Shift {index}",
        "summary": _render_history_refs_in_text(
            raw_signal.get("summary") or "",
            history_window_refs=history_window_refs,
        ),
        "history_refs": history_refs,
        "evidence": [],
    }


def _trend_cluster_presentations(
    *,
    clusters: Sequence[Mapping[str, Any]] | None,
    history_window_refs: Mapping[str, Mapping[str, Any]] | None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    presentation_clusters: list[dict[str, Any]] = []
    representative_sources: list[dict[str, Any]] = []
    seen_rep_targets: set[str] = set()
    for raw_cluster in list(clusters or []):
        if not isinstance(raw_cluster, Mapping):
            continue
        reps = _project_cluster_representative_sources(
            raw_cluster.get("representative_chunks") or []
        )
        representative_sources.extend(
            _deduped_representative_sources(reps, seen_rep_targets=seen_rep_targets)
        )
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
    return presentation_clusters, representative_sources


def _deduped_representative_sources(
    reps: list[dict[str, Any]],
    *,
    seen_rep_targets: set[str],
) -> list[dict[str, Any]]:
    deduped: list[dict[str, Any]] = []
    for rep in reps:
        target = (
            _single_line(rep.get("href") or "")
            or _single_line(rep.get("url") or "")
            or _single_line(rep.get("title") or "")
        )
        if target and target not in seen_rep_targets:
            deduped.append(rep)
            seen_rep_targets.add(target)
    return deduped


def _build_trend_presentation_content(
    build_input: _TrendPresentationBuildInput,
    *,
    normalized_overview: str,
) -> dict[str, Any]:
    presentation_clusters, representative_sources = _trend_cluster_presentations(
        clusters=build_input.clusters,
        history_window_refs=build_input.history_window_refs,
    )
    return {
        "title": _single_line(build_input.title),
        "hero": {
            "kicker": "Trend brief",
            "dek": _trend_hero_dek(
                title=build_input.title,
                overview_md=normalized_overview,
            ),
        },
        "overview": normalized_overview,
        "ranked_shifts": _trend_ranked_shifts(
            title=build_input.title,
            overview_md=normalized_overview,
            evolution=build_input.evolution,
            clusters=build_input.clusters,
            history_window_refs=build_input.history_window_refs,
        ),
        "counter_signal": _project_counter_signal(build_input.counter_signal),
        "clusters": presentation_clusters,
        "representative_sources": representative_sources,
    }


def _build_trend_presentation(
    build_input: _TrendPresentationBuildInput,
) -> dict[str, Any]:
    resolved_language_code, resolved_display_language_code = _resolve_presentation_languages(
        language_code=build_input.language_code,
        display_language_code=build_input.display_language_code,
    )
    normalized_overview = _render_history_refs_in_text(
        build_input.overview_md,
        history_window_refs=build_input.history_window_refs,
    )

    return {
        "presentation_schema_version": build_input.schema_version,
        "surface_kind": "trend",
        "language_code": resolved_language_code,
        "source_markdown_path": build_input.source_markdown_path,
        "display_labels": trend_display_labels(
            language_code=resolved_display_language_code
        ),
        "content": _build_trend_presentation_content(
            build_input,
            normalized_overview=normalized_overview,
        ),
    }


def _validated_presentation_kwargs(
    *,
    function_name: str,
    kwargs: Mapping[str, Any],
    required_keys: tuple[str, ...],
    defaults: Mapping[str, Any],
) -> dict[str, Any]:
    allowed_keys = set(required_keys) | set(defaults)
    unexpected = [key for key in kwargs if key not in allowed_keys]
    if unexpected:
        raise TypeError(
            f"{function_name}() got an unexpected keyword argument {unexpected[0]!r}"
        )
    missing = [key for key in required_keys if key not in kwargs]
    if missing:
        missing_repr = ", ".join(repr(key) for key in missing)
        plural = "s" if len(missing) != 1 else ""
        raise TypeError(
            f"{function_name}() missing required keyword-only argument{plural}: {missing_repr}"
        )
    return {**defaults, **kwargs}


def build_trend_presentation_v1(
    **kwargs: Unpack[_TrendPresentationKwargs],
) -> dict[str, Any]:
    normalized_kwargs = _validated_presentation_kwargs(
        function_name="build_trend_presentation_v1",
        kwargs=kwargs,
        required_keys=_TREND_PRESENTATION_REQUIRED_KEYS,
        defaults=_TREND_PRESENTATION_V1_DEFAULTS,
    )
    build_input = _TrendPresentationBuildInput(
        source_markdown_path=normalized_kwargs["source_markdown_path"],
        title=normalized_kwargs["title"],
        overview_md=normalized_kwargs["overview_md"],
        evolution=normalized_kwargs["evolution"],
        history_window_refs=normalized_kwargs["history_window_refs"],
        clusters=normalized_kwargs["clusters"],
        counter_signal=None,
        schema_version=PRESENTATION_SCHEMA_VERSION_V1,
        language_code=normalized_kwargs["language_code"],
        display_language_code=normalized_kwargs["display_language_code"],
    )
    presentation = _build_trend_presentation(
        build_input
    )
    presentation["content"]["counter_signal"] = None
    return presentation


def build_trend_presentation_v2(
    **kwargs: Unpack[_TrendPresentationV2Kwargs],
) -> dict[str, Any]:
    normalized_kwargs = _validated_presentation_kwargs(
        function_name="build_trend_presentation_v2",
        kwargs=kwargs,
        required_keys=_TREND_PRESENTATION_REQUIRED_KEYS,
        defaults=_TREND_PRESENTATION_V2_DEFAULTS,
    )
    build_input = _TrendPresentationBuildInput(
        source_markdown_path=normalized_kwargs["source_markdown_path"],
        title=normalized_kwargs["title"],
        overview_md=normalized_kwargs["overview_md"],
        evolution=normalized_kwargs["evolution"],
        history_window_refs=normalized_kwargs["history_window_refs"],
        clusters=normalized_kwargs["clusters"],
        counter_signal=normalized_kwargs["counter_signal"],
        schema_version=PRESENTATION_SCHEMA_VERSION,
        language_code=normalized_kwargs["language_code"],
        display_language_code=normalized_kwargs["display_language_code"],
    )
    presentation = _build_trend_presentation(
        build_input
    )
    presentation["content"]["counter_signal"] = _project_counter_signal(
        build_input.counter_signal
    )
    return presentation


def _idea_opportunity_presentation(
    *,
    index: int,
    idea: Any,
    display_language_code: str | None,
) -> dict[str, Any]:
    return {
        "rank": index,
        "tier": "best_bet" if index == 1 else "alternate",
        "title": _single_line(_value_from(idea, "title", "") or ""),
        "kind": _single_line(_value_from(idea, "kind", "") or ""),
        "time_horizon": _single_line(_value_from(idea, "time_horizon", "") or ""),
        "display_kind": display_idea_kind(
            str(_value_from(idea, "kind", "") or ""),
            language_code=display_language_code,
        ),
        "display_time_horizon": display_idea_time_horizon(
            str(_value_from(idea, "time_horizon", "") or ""),
            language_code=display_language_code,
        ),
        "role": _normalize_markdown(_value_from(idea, "user_or_job", "") or ""),
        "thesis": _normalize_markdown(_value_from(idea, "thesis", "") or ""),
        "anti_thesis": _normalize_markdown(_value_from(idea, "anti_thesis", "") or ""),
        "why_now": _normalize_markdown(_value_from(idea, "why_now", "") or ""),
        "what_changed": _normalize_markdown(_value_from(idea, "what_changed", "") or ""),
        "validation_next_step": _normalize_markdown(
            _value_from(idea, "validation_next_step", "") or ""
        ),
        "evidence": _project_idea_evidence(
            list(_value_from(idea, "evidence_refs", []) or [])
        ),
    }


def _idea_opportunities(
    *,
    ideas: list[Any],
    display_language_code: str | None,
) -> list[dict[str, Any]]:
    return [
        _idea_opportunity_presentation(
            index=index,
            idea=idea,
            display_language_code=display_language_code,
        )
        for index, idea in enumerate(list(ideas or [])[:3], start=1)
    ]


def _build_idea_presentation(
    build_input: _IdeaPresentationBuildInput,
) -> dict[str, Any]:
    resolved_language_code, resolved_display_language_code = _resolve_presentation_languages(
        language_code=build_input.language_code,
        display_language_code=build_input.display_language_code,
    )

    return {
        "presentation_schema_version": build_input.schema_version,
        "surface_kind": "idea",
        "language_code": resolved_language_code,
        "source_markdown_path": build_input.source_markdown_path,
        "display_labels": idea_display_labels(
            language_code=resolved_display_language_code,
            schema_version=build_input.schema_version,
        ),
        "content": {
            "title": _single_line(build_input.title),
            "summary": _normalize_markdown(build_input.summary_md),
            "opportunities": _idea_opportunities(
                ideas=build_input.ideas,
                display_language_code=resolved_display_language_code,
            ),
        },
    }


def build_idea_presentation_v1(
    **kwargs: Unpack[_IdeaPresentationKwargs],
) -> dict[str, Any]:
    normalized_kwargs = _validated_presentation_kwargs(
        function_name="build_idea_presentation_v1",
        kwargs=kwargs,
        required_keys=_IDEA_PRESENTATION_REQUIRED_KEYS,
        defaults=_IDEA_PRESENTATION_DEFAULTS,
    )
    build_input = _IdeaPresentationBuildInput(
        source_markdown_path=normalized_kwargs["source_markdown_path"],
        title=normalized_kwargs["title"],
        summary_md=normalized_kwargs["summary_md"],
        ideas=normalized_kwargs["ideas"],
        schema_version=PRESENTATION_SCHEMA_VERSION_V1,
        language_code=normalized_kwargs["language_code"],
        display_language_code=normalized_kwargs["display_language_code"],
    )
    presentation = _build_idea_presentation(
        build_input
    )
    for opportunity in list(presentation["content"].get("opportunities") or []):
        if isinstance(opportunity, dict):
            opportunity.pop("anti_thesis", None)
    return presentation


def build_idea_presentation_v2(
    **kwargs: Unpack[_IdeaPresentationKwargs],
) -> dict[str, Any]:
    normalized_kwargs = _validated_presentation_kwargs(
        function_name="build_idea_presentation_v2",
        kwargs=kwargs,
        required_keys=_IDEA_PRESENTATION_REQUIRED_KEYS,
        defaults=_IDEA_PRESENTATION_DEFAULTS,
    )
    return _build_idea_presentation(
        _IdeaPresentationBuildInput(
            source_markdown_path=normalized_kwargs["source_markdown_path"],
            title=normalized_kwargs["title"],
            summary_md=normalized_kwargs["summary_md"],
            ideas=normalized_kwargs["ideas"],
            schema_version=PRESENTATION_SCHEMA_VERSION,
            language_code=normalized_kwargs["language_code"],
            display_language_code=normalized_kwargs["display_language_code"],
        )
    )


def _trend_user_visible_strings(presentation: Mapping[str, Any]) -> list[str]:
    content = presentation.get("content")
    if not isinstance(content, Mapping):
        return []
    strings = [
        _single_line(content.get("title") or ""),
        _normalize_markdown(((content.get("hero") or {}) if isinstance(content.get("hero"), Mapping) else {}).get("dek") or ""),
        _normalize_markdown(content.get("overview") or ""),
    ]
    _append_mapping_text_fields(
        strings,
        values=list(content.get("ranked_shifts") or []),
        keys=("title", "summary"),
    )
    _append_mapping_text_fields(
        strings,
        values=list(content.get("clusters") or []),
        keys=("title", "summary"),
    )
    _append_mapping_text_fields(
        strings,
        values=[content.get("counter_signal")],
        keys=("title", "summary"),
    )
    return [value for value in strings if value]


def _append_mapping_text_fields(
    strings: list[str],
    *,
    values: list[Any],
    keys: tuple[str, ...],
) -> None:
    for value in values:
        if not isinstance(value, Mapping):
            continue
        for key in keys:
            strings.append(_normalize_markdown(value.get(key) or ""))


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
            "anti_thesis",
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


def _validate_presentation_common_fields(
    presentation: Mapping[str, Any],
    *,
    allowed_schema_versions: set[int],
    errors: list[str],
) -> tuple[int | None, str, Mapping[str, Any] | None, Mapping[str, Any] | None]:
    schema_version = _presentation_schema_version(
        presentation.get("presentation_schema_version")
    )
    if schema_version not in allowed_schema_versions:
        errors.append(
            "presentation_schema_version must be "
            + " or ".join(str(version) for version in sorted(allowed_schema_versions))
        )
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
    normalized_display_labels = (
        display_labels if isinstance(display_labels, Mapping) else None
    )
    normalized_content = content if isinstance(content, Mapping) else None
    return schema_version, surface_kind, normalized_display_labels, normalized_content


def _validate_required_labels(
    *,
    surface_kind: str,
    display_labels: Mapping[str, Any] | None,
    expected_labels: set[str],
    errors: list[str],
) -> None:
    if display_labels is None:
        return
    missing_labels = sorted(expected_labels - set(display_labels))
    if missing_labels:
        errors.append(
            f"{surface_kind} display_labels must include: " + ", ".join(missing_labels)
        )


def _validate_required_content_keys(
    *,
    surface_kind: str,
    content: Mapping[str, Any] | None,
    required_keys: set[str],
    errors: list[str],
) -> None:
    if content is None:
        return
    missing_content = sorted(required_keys - set(content))
    if missing_content:
        errors.append(
            f"{surface_kind} content must include: " + ", ".join(missing_content)
        )


def _validate_trend_hero(
    *,
    content: Mapping[str, Any] | None,
    errors: list[str],
) -> None:
    if content is None:
        return
    hero = content.get("hero")
    if not isinstance(hero, Mapping):
        errors.append("trend hero must be a mapping")
        return
    missing_hero = sorted(_TREND_REQUIRED_HERO_KEYS - set(hero))
    if missing_hero:
        errors.append("trend hero must include: " + ", ".join(missing_hero))
    for key in ("kicker", "dek"):
        _validate_string_field(
            mapping=hero,
            key=key,
            field_path=f"trend hero.{key}",
            errors=errors,
        )


def _validate_trend_ranked_shifts(
    ranked_shifts: list[Any],
    *,
    allow_empty: bool,
    errors: list[str],
) -> None:
    if not ranked_shifts:
        if not allow_empty:
            errors.append("trend ranked_shifts must contain at least 1 entry")
        return
    if len(ranked_shifts) > 3:
        errors.append("trend ranked_shifts must not exceed 3 entries")
    normalized_ranks: list[int] = []
    for shift in ranked_shifts:
        if not _validate_trend_ranked_shift_entry(shift, errors=errors):
            break
        normalized_rank = _int_or_none(shift.get("rank"))
        if normalized_rank is not None:
            normalized_ranks.append(normalized_rank)
    if _ranks_break_consecutive_order(normalized_ranks, expected_total=len(ranked_shifts)):
        errors.append(
            "trend ranked_shifts ranks must be consecutive integers starting at 1"
        )


def _validate_trend_ranked_shift_entry(shift: Any, *, errors: list[str]) -> bool:
    if not isinstance(shift, Mapping):
        errors.append("trend ranked_shifts entries must be mappings")
        return False
    missing_shift = sorted(_TREND_REQUIRED_SHIFT_KEYS - set(shift))
    if missing_shift:
        errors.append(
            "trend ranked_shifts entries must include: " + ", ".join(missing_shift)
        )
        return False
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
    return _validate_trend_ranked_shift_collections(shift, errors=errors)


def _validate_trend_ranked_shift_collections(
    shift: Mapping[str, Any],
    *,
    errors: list[str],
) -> bool:
    history_refs = shift.get("history_refs")
    if not isinstance(history_refs, list) or any(
        not isinstance(item, str) for item in history_refs
    ):
        errors.append("trend ranked_shifts.history_refs must be a list of strings")
        return False
    evidence = shift.get("evidence")
    if not isinstance(evidence, list):
        errors.append("trend ranked_shifts.evidence must be a list")
        return False
    return True


def _ranks_break_consecutive_order(
    normalized_ranks: list[int],
    *,
    expected_total: int,
) -> bool:
    if len(normalized_ranks) != expected_total:
        return False
    expected_ranks = list(range(1, expected_total + 1))
    return normalized_ranks != expected_ranks


def _validate_string_list_field(
    *,
    mapping: Mapping[str, Any],
    key: str,
    field_path: str,
    errors: list[str],
) -> None:
    value = mapping.get(key)
    if value is None:
        return
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        errors.append(f"{field_path} must be a list of strings")


def _validate_source_metadata_entry(
    entry: Any,
    *,
    field_path: str,
    errors: list[str],
) -> None:
    if not isinstance(entry, Mapping):
        errors.append(f"{field_path} entries must be mappings")
        return
    _validate_source_metadata_text_fields(entry, field_path=field_path, errors=errors)
    _validate_source_metadata_numeric_fields(
        entry,
        field_path=field_path,
        errors=errors,
    )
    _validate_string_list_field(
        mapping=entry,
        key="authors",
        field_path=f"{field_path}.authors",
        errors=errors,
    )
    _validate_string_list_field(
        mapping=entry,
        key="reasons",
        field_path=f"{field_path}.reasons",
        errors=errors,
    )
    _validate_source_metadata_reason_field(entry, field_path=field_path, errors=errors)
    _validate_source_metadata_enum_fields(entry, field_path=field_path, errors=errors)


def _validate_source_metadata_text_fields(
    entry: Mapping[str, Any],
    *,
    field_path: str,
    errors: list[str],
) -> None:
    if "title" in entry and not isinstance(entry.get("title"), str):
        errors.append(f"{field_path}.title must be a string")
    for key in ("href", "url"):
        value = entry.get(key)
        if key in entry and value is not None and not isinstance(value, str):
            errors.append(f"{field_path}.{key} must be a string")


def _validate_source_metadata_numeric_fields(
    entry: Mapping[str, Any],
    *,
    field_path: str,
    errors: list[str],
) -> None:
    for key in ("doc_id", "chunk_index"):
        value = entry.get(key)
        if value not in {None, ""} and _int_or_none(value) is None:
            errors.append(f"{field_path}.{key} must be an integer")


def _validate_source_metadata_reason_field(
    entry: Mapping[str, Any],
    *,
    field_path: str,
    errors: list[str],
) -> None:
    if "reason" in entry and entry.get("reason") is not None and not isinstance(
        entry.get("reason"), str
    ):
        errors.append(f"{field_path}.reason must be a string")


def _validate_source_metadata_enum_fields(
    entry: Mapping[str, Any],
    *,
    field_path: str,
    errors: list[str],
) -> None:
    _validate_metadata_enum_field(
        value=_single_line(entry.get("source_type") or "").lower(),
        allowed=_VALID_SOURCE_TYPES,
        field_path=f"{field_path}.source_type",
        errors=errors,
    )
    _validate_metadata_enum_field(
        value=_single_line(entry.get("confidence") or "").lower(),
        allowed=_VALID_CONFIDENCE_LEVELS,
        field_path=f"{field_path}.confidence",
        errors=errors,
    )


def _validate_metadata_enum_field(
    *,
    value: str,
    allowed: set[str],
    field_path: str,
    errors: list[str],
) -> None:
    if value and value not in allowed:
        errors.append(
            f"{field_path} must be one of: " + ", ".join(sorted(allowed))
        )


def _validate_source_metadata_list(
    value: Any,
    *,
    field_path: str,
    errors: list[str],
) -> None:
    if not isinstance(value, list):
        errors.append(f"{field_path} must be a list")
        return
    for entry in value:
        _validate_source_metadata_entry(entry, field_path=field_path, errors=errors)


def _validate_counter_signal(
    value: Any,
    *,
    field_path: str,
    errors: list[str],
) -> None:
    if value is None:
        return
    if not isinstance(value, Mapping):
        errors.append(f"{field_path} must be a mapping")
        return
    for key in ("title", "summary"):
        _validate_string_field(
            mapping=value,
            key=key,
            field_path=f"{field_path}.{key}",
            errors=errors,
        )
    _validate_source_metadata_list(
        value.get("evidence"),
        field_path=f"{field_path}.evidence",
        errors=errors,
    )


def _validate_trend_presentation(
    presentation: Mapping[str, Any],
    *,
    schema_version: int,
    display_labels: Mapping[str, Any] | None,
    content: Mapping[str, Any] | None,
    errors: list[str],
) -> list[str]:
    _validate_required_labels(
        surface_kind="trend",
        display_labels=display_labels,
        expected_labels=set(TREND_DISPLAY_LABELS_V1),
        errors=errors,
    )
    _validate_required_content_keys(
        surface_kind="trend",
        content=content,
        required_keys=(
            _TREND_REQUIRED_CONTENT_KEYS_V2
            if schema_version >= PRESENTATION_SCHEMA_VERSION
            else _TREND_REQUIRED_CONTENT_KEYS_V1
        ),
        errors=errors,
    )
    _validate_trend_content_scalars(content=content, errors=errors)
    _validate_trend_hero(content=content, errors=errors)
    ranked_shifts = list(content.get("ranked_shifts") or []) if content is not None else []
    _validate_trend_ranked_shifts(
        ranked_shifts,
        allow_empty=schema_version < PRESENTATION_SCHEMA_VERSION,
        errors=errors,
    )
    _validate_trend_content_structures(
        content=content,
        schema_version=schema_version,
        errors=errors,
    )
    return _trend_user_visible_strings(presentation)


def _validate_trend_content_scalars(
    *,
    content: Mapping[str, Any] | None,
    errors: list[str],
) -> None:
    if content is None:
        return
    for key in ("title", "overview"):
        _validate_string_field(
            mapping=content,
            key=key,
            field_path=f"trend content.{key}",
            errors=errors,
        )


def _validate_trend_content_structures(
    *,
    content: Mapping[str, Any] | None,
    schema_version: int,
    errors: list[str],
) -> None:
    if content is None:
        return
    _validate_source_metadata_list(
        content.get("representative_sources"),
        field_path="trend content.representative_sources",
        errors=errors,
    )
    if schema_version >= PRESENTATION_SCHEMA_VERSION:
        _validate_counter_signal(
            content.get("counter_signal"),
            field_path="trend content.counter_signal",
            errors=errors,
        )
    _validate_trend_clusters(
        clusters=content.get("clusters"),
        errors=errors,
    )


def _validate_trend_clusters(
    *,
    clusters: Any,
    errors: list[str],
) -> None:
    if not isinstance(clusters, list):
        errors.append("trend content.clusters must be a list")
        return
    for index, cluster in enumerate(clusters):
        if not isinstance(cluster, Mapping):
            errors.append("trend content.clusters entries must be mappings")
            break
        _validate_source_metadata_list(
            cluster.get("representative_sources"),
            field_path=f"trend content.clusters[{index}].representative_sources",
            errors=errors,
        )


def _validate_idea_opportunities(
    opportunities: list[Any],
    *,
    schema_version: int,
    errors: list[str],
) -> None:
    if not opportunities:
        if schema_version >= PRESENTATION_SCHEMA_VERSION:
            errors.append("idea opportunities must contain at least 1 entry")
        return
    best_bet_total = sum(
        1 for opportunity in opportunities if _is_best_bet_opportunity(opportunity)
    )
    if len(opportunities) > 3:
        errors.append("idea opportunities must not exceed 3 entries")
    if best_bet_total != 1:
        errors.append("idea opportunities must contain exactly one best_bet")
    normalized_ranks: list[int] = []
    normalized_tiers: list[str] = []
    for opportunity in opportunities:
        if not _validate_idea_opportunity(
            opportunity,
            schema_version=schema_version,
            errors=errors,
        ):
            break
        normalized_rank = _int_or_none(opportunity.get("rank"))
        if normalized_rank is not None:
            normalized_ranks.append(normalized_rank)
        normalized_tiers.append(_single_line(opportunity.get("tier") or ""))
    if _ranks_break_consecutive_order(normalized_ranks, expected_total=len(opportunities)):
        errors.append(
            "idea opportunities ranks must be consecutive integers starting at 1"
        )
    _validate_opportunity_tier_order(normalized_tiers, errors=errors)


def _validate_opportunity_tier_order(
    normalized_tiers: list[str],
    *,
    errors: list[str],
) -> None:
    if not normalized_tiers:
        return
    if normalized_tiers[0] != "best_bet":
        errors.append("idea opportunities[0] must be best_bet")
    if any(tier != "alternate" for tier in normalized_tiers[1:]):
        errors.append("idea opportunities after the first must be alternate")


def _is_best_bet_opportunity(opportunity: Any) -> bool:
    return isinstance(opportunity, Mapping) and _single_line(
        opportunity.get("tier") or ""
    ) == "best_bet"


def _validate_idea_opportunity(
    opportunity: Any,
    *,
    schema_version: int,
    errors: list[str],
) -> bool:
    if not isinstance(opportunity, Mapping):
        errors.append("idea opportunities entries must be mappings")
        return False
    missing_opportunity = sorted(
        (
            _IDEA_REQUIRED_OPPORTUNITY_KEYS_V2
            if schema_version >= PRESENTATION_SCHEMA_VERSION
            else _IDEA_REQUIRED_OPPORTUNITY_KEYS_V1
        )
        - set(opportunity)
    )
    if missing_opportunity:
        errors.append("idea opportunities must include: " + ", ".join(missing_opportunity))
        return False
    _validate_idea_opportunity_string_fields(
        opportunity,
        schema_version=schema_version,
        errors=errors,
    )
    if _single_line(opportunity.get("display_kind") or "") in _RAW_IDEA_ENUMS:
        errors.append("display_kind must not leak raw idea enums")
        return False
    if _single_line(opportunity.get("display_time_horizon") or "") in _RAW_IDEA_ENUMS:
        errors.append("display_time_horizon must not leak raw idea enums")
        return False
    _validate_source_metadata_list(
        opportunity.get("evidence"),
        field_path="idea opportunities.evidence",
        errors=errors,
    )
    return True


def _validate_idea_opportunity_string_fields(
    opportunity: Mapping[str, Any],
    *,
    schema_version: int,
    errors: list[str],
) -> None:
    keys = [
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
    ]
    if schema_version >= PRESENTATION_SCHEMA_VERSION:
        keys.insert(7, "anti_thesis")
    for key in keys:
        _validate_string_field(
            mapping=opportunity,
            key=key,
            field_path=f"idea opportunities.{key}",
            errors=errors,
        )


def _validate_idea_presentation(
    presentation: Mapping[str, Any],
    *,
    schema_version: int,
    display_labels: Mapping[str, Any] | None,
    content: Mapping[str, Any] | None,
    errors: list[str],
) -> list[str]:
    _validate_required_labels(
        surface_kind="idea",
        display_labels=display_labels,
        expected_labels=(
            set(_IDEA_REQUIRED_DISPLAY_LABEL_KEYS)
            if schema_version >= PRESENTATION_SCHEMA_VERSION
            else set(IDEA_DISPLAY_LABELS_V1)
        ),
        errors=errors,
    )
    _validate_required_content_keys(
        surface_kind="idea",
        content=content,
        required_keys=_IDEA_REQUIRED_CONTENT_KEYS,
        errors=errors,
    )
    if content is not None:
        for key in ("title", "summary"):
            _validate_string_field(
                mapping=content,
                key=key,
                field_path=f"idea content.{key}",
                errors=errors,
            )
    opportunities = list(content.get("opportunities") or []) if content is not None else []
    _validate_idea_opportunities(
        opportunities,
        schema_version=schema_version,
        errors=errors,
    )
    return _idea_user_visible_strings(presentation)


def _validate_user_visible_strings(
    user_visible_strings: list[str],
    *,
    errors: list[str],
) -> None:
    for value in user_visible_strings:
        if _PLACEHOLDER_TOKEN_RE.search(value):
            errors.append(
                "user-visible fields must not contain raw history placeholder tokens"
            )
            break
    lowered_strings = "\n".join(user_visible_strings).lower()
    for pattern in _RAW_LABEL_PATTERNS:
        if pattern.search(lowered_strings):
            errors.append("user-visible fields must not leak raw schema labels")
            break


def validate_presentation_v1(presentation: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    schema_version, surface_kind, display_labels, content = _validate_presentation_common_fields(
        presentation,
        allowed_schema_versions={PRESENTATION_SCHEMA_VERSION_V1},
        errors=errors,
    )
    _ = schema_version

    if surface_kind == "trend":
        user_visible_strings = _validate_trend_presentation(
            presentation,
            schema_version=PRESENTATION_SCHEMA_VERSION_V1,
            display_labels=display_labels,
            content=content,
            errors=errors,
        )
    elif surface_kind == "idea":
        user_visible_strings = _validate_idea_presentation(
            presentation,
            schema_version=PRESENTATION_SCHEMA_VERSION_V1,
            display_labels=display_labels,
            content=content,
            errors=errors,
        )
    else:
        errors.append("surface_kind must be trend or idea")
        user_visible_strings = []

    _validate_user_visible_strings(user_visible_strings, errors=errors)
    return errors


def validate_presentation_v2(presentation: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    schema_version, surface_kind, display_labels, content = _validate_presentation_common_fields(
        presentation,
        allowed_schema_versions={PRESENTATION_SCHEMA_VERSION},
        errors=errors,
    )
    normalized_schema_version = (
        schema_version if isinstance(schema_version, int) else PRESENTATION_SCHEMA_VERSION
    )

    if surface_kind == "trend":
        user_visible_strings = _validate_trend_presentation(
            presentation,
            schema_version=normalized_schema_version,
            display_labels=display_labels,
            content=content,
            errors=errors,
        )
    elif surface_kind == "idea":
        user_visible_strings = _validate_idea_presentation(
            presentation,
            schema_version=normalized_schema_version,
            display_labels=display_labels,
            content=content,
            errors=errors,
        )
    else:
        errors.append("surface_kind must be trend or idea")
        user_visible_strings = []

    _validate_user_visible_strings(user_visible_strings, errors=errors)
    return errors


def validate_presentation(presentation: Mapping[str, Any]) -> list[str]:
    schema_version = _presentation_schema_version(
        presentation.get("presentation_schema_version")
    )
    if schema_version == PRESENTATION_SCHEMA_VERSION_V1:
        return validate_presentation_v1(presentation)
    if schema_version == PRESENTATION_SCHEMA_VERSION:
        return validate_presentation_v2(presentation)
    return [
        "presentation_schema_version must be 1 or 2"
    ]


__all__ = [
    "IDEA_DISPLAY_LABELS_V2",
    "IDEA_DISPLAY_LABELS_V1",
    "PRESENTATION_SCHEMA_VERSION",
    "PRESENTATION_SCHEMA_VERSION_V1",
    "TREND_DISPLAY_LABELS_V1",
    "build_idea_presentation_v2",
    "build_idea_presentation_v1",
    "build_trend_presentation_v2",
    "build_trend_presentation_v1",
    "display_idea_kind",
    "display_idea_tier",
    "display_idea_time_horizon",
    "idea_display_labels",
    "is_localized_output_path",
    "presentation_sidecar_path",
    "resolve_presentation_language_code",
    "trend_display_labels",
    "validate_presentation",
    "validate_presentation_v2",
    "validate_presentation_v1",
    "write_presentation_sidecar",
]
