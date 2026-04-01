from __future__ import annotations

import json
from collections.abc import Sequence
from pathlib import Path
import re
from typing import Any, Mapping

PRESENTATION_SCHEMA_VERSION = 1

_HISTORY_WINDOW_MENTION_RE = re.compile(r"(?<![\w\[])(prev_\d+)(?![\w\]])", re.IGNORECASE)
_PLACEHOLDER_TOKEN_RE = re.compile(r"\b(?:Prev_\d+|prev\d+|prev_\d+)\b")
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

TREND_DISPLAY_LABELS_V1 = {
    "overview": "Overview",
    "top_shifts": "Top shifts",
    "counter_signal": "Counter-signal",
    "clusters": "Clusters",
    "representative_sources": "Representative sources",
    "source_type": "Source type",
    "confidence": "Confidence",
}

IDEA_DISPLAY_LABELS_V1 = {
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


def _history_window_display_text(
    *,
    window: str,
    history_window_refs: Mapping[str, Mapping[str, Any]] | None,
) -> str:
    ref = (history_window_refs or {}).get(window)
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
        return display or ""

    replaced = _HISTORY_WINDOW_MENTION_RE.sub(_replace, raw)
    return re.sub(r"\s{2,}", " ", replaced).strip()


def display_idea_kind(value: str) -> str:
    labels = {
        "new_build": "New build",
        "revival": "Revival",
        "research_gap": "Research gap",
        "tooling_wedge": "Tooling wedge",
        "workflow_shift": "Workflow shift",
    }
    normalized = _single_line(value).lower()
    return labels.get(normalized, _single_line(value))


def display_idea_time_horizon(value: str) -> str:
    labels = {
        "now": "Now",
        "near": "Near-term",
        "frontier": "Frontier",
    }
    normalized = _single_line(value).lower()
    return labels.get(normalized, _single_line(value))


def display_idea_tier(rank: int) -> str:
    return "Best bet" if int(rank) == 1 else "Alternate"


def presentation_sidecar_path(*, note_path: Path) -> Path:
    return note_path.with_name(f"{note_path.stem}.presentation.json")


def is_localized_output_path(path: Path) -> bool:
    return "Localized" in path.expanduser().resolve().parts


def write_presentation_sidecar(*, note_path: Path, presentation: Mapping[str, Any]) -> Path:
    errors = validate_presentation_v1(presentation)
    if errors:
        raise ValueError("invalid presentation sidecar: " + "; ".join(errors))
    sidecar_path = presentation_sidecar_path(note_path=note_path)
    payload = json.dumps(presentation, indent=2, ensure_ascii=False) + "\n"
    sidecar_path.write_text(payload, encoding="utf-8")
    return sidecar_path


def build_trend_presentation_v1(
    *,
    source_markdown_path: str,
    title: str,
    overview_md: str,
    evolution: Mapping[str, Any] | None,
    history_window_refs: Mapping[str, Mapping[str, Any]] | None,
    clusters: Sequence[Mapping[str, Any]] | None,
    language_code: str | None = None,
) -> dict[str, Any]:
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
        reps: list[dict[str, Any]] = []
        for raw_rep in list(raw_cluster.get("representative_chunks") or []):
            if not isinstance(raw_rep, Mapping):
                continue
            title_value = _single_line(raw_rep.get("title") or "")
            href_value = _single_line(raw_rep.get("note_href") or "")
            url_value = _single_line(raw_rep.get("url") or "")
            if not title_value:
                continue
            rep = {
                "title": title_value,
                "href": href_value or None,
                "url": url_value or None,
                "authors": [
                    _single_line(author)
                    for author in list(raw_rep.get("authors") or [])
                    if _single_line(author)
                ],
            }
            reps.append(rep)
            target = href_value or url_value or title_value
            if target and target not in seen_rep_targets:
                representative_sources.append(rep)
                seen_rep_targets.add(target)
        presentation_clusters.append(
            {
                "title": _single_line(raw_cluster.get("name") or "") or "Cluster",
                "summary": _normalize_markdown(raw_cluster.get("description") or ""),
                "representative_sources": reps,
            }
        )

    return {
        "presentation_schema_version": PRESENTATION_SCHEMA_VERSION,
        "surface_kind": "trend",
        "language_code": _single_line(language_code or "en") or "en",
        "source_markdown_path": source_markdown_path,
        "display_labels": dict(TREND_DISPLAY_LABELS_V1),
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
) -> dict[str, Any]:
    opportunities: list[dict[str, Any]] = []
    for index, idea in enumerate(list(ideas or [])[:3], start=1):
        opportunities.append(
            {
                "rank": index,
                "tier": "best_bet" if index == 1 else "alternate",
                "title": _single_line(getattr(idea, "title", "") or ""),
                "kind": _single_line(getattr(idea, "kind", "") or ""),
                "time_horizon": _single_line(getattr(idea, "time_horizon", "") or ""),
                "display_kind": display_idea_kind(str(getattr(idea, "kind", "") or "")),
                "display_time_horizon": display_idea_time_horizon(
                    str(getattr(idea, "time_horizon", "") or "")
                ),
                "role": _normalize_markdown(getattr(idea, "user_or_job", "") or ""),
                "thesis": _normalize_markdown(getattr(idea, "thesis", "") or ""),
                "why_now": _normalize_markdown(getattr(idea, "why_now", "") or ""),
                "what_changed": _normalize_markdown(
                    getattr(idea, "what_changed", "") or ""
                ),
                "validation_next_step": _normalize_markdown(
                    getattr(idea, "validation_next_step", "") or ""
                ),
                "evidence": [
                    {
                        "doc_id": int(getattr(ref, "doc_id")),
                        "chunk_index": int(getattr(ref, "chunk_index", 0)),
                        "reason": _normalize_markdown(getattr(ref, "reason", "") or ""),
                    }
                    for ref in list(getattr(idea, "evidence_refs", []) or [])
                    if getattr(ref, "doc_id", None) is not None
                ],
            }
        )

    return {
        "presentation_schema_version": PRESENTATION_SCHEMA_VERSION,
        "surface_kind": "idea",
        "language_code": _single_line(language_code or "en") or "en",
        "source_markdown_path": source_markdown_path,
        "display_labels": dict(IDEA_DISPLAY_LABELS_V1),
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


def validate_presentation_v1(presentation: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if int(presentation.get("presentation_schema_version") or 0) != PRESENTATION_SCHEMA_VERSION:
        errors.append("presentation_schema_version must be 1")
    source_markdown_path = _single_line(presentation.get("source_markdown_path") or "")
    if not source_markdown_path.endswith(".md"):
        errors.append("source_markdown_path must point to a markdown note")
    display_labels = presentation.get("display_labels")
    if not isinstance(display_labels, Mapping):
        errors.append("display_labels must be a mapping")
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
            hero = content.get("hero")
            if not isinstance(hero, Mapping):
                errors.append("trend hero must be a mapping")
            else:
                missing_hero = sorted(_TREND_REQUIRED_HERO_KEYS - set(hero))
                if missing_hero:
                    errors.append(
                        "trend hero must include: " + ", ".join(missing_hero)
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
        user_visible_strings = _trend_user_visible_strings(presentation)
    elif surface_kind == "idea":
        expected_labels = set(IDEA_DISPLAY_LABELS_V1)
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
                continue
            missing_opportunity = sorted(_IDEA_REQUIRED_OPPORTUNITY_KEYS - set(opportunity))
            if missing_opportunity:
                errors.append(
                    "idea opportunities must include: "
                    + ", ".join(missing_opportunity)
                )
                break
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
    "is_localized_output_path",
    "presentation_sidecar_path",
    "validate_presentation_v1",
    "write_presentation_sidecar",
]
