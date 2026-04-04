from __future__ import annotations

import re

_ITEM_SECTION_ORDER: tuple[tuple[str, str], ...] = (
    ("summary", "Summary"),
    ("problem", "Problem"),
    ("approach", "Approach"),
    ("results", "Results"),
)

_SECTION_ALIAS_TO_KEY = {
    "summary": "summary",
    "tl;dr": "summary",
    "tldr": "summary",
    "problem": "problem",
    "approach": "approach",
    "results": "results",
}

_SECTION_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s*(?P<label>[^#\n]+?)\s*$")
_LEGACY_LABEL_RE = re.compile(
    r"^\s*(?:[-*]\s*)?(?:\d+\.\s*)?"
    r"(?P<label>tl;dr|tldr|summary|problem|approach|results)\s*[:：]\s*"
    r"(?P<body>.*)$",
    re.IGNORECASE,
)


def _section_key(label: str) -> str | None:
    normalized = " ".join(str(label or "").split()).strip().lower()
    if not normalized:
        return None
    return _SECTION_ALIAS_TO_KEY.get(normalized)


def _blank_sections() -> dict[str, str]:
    return {key: "" for key, _label in _ITEM_SECTION_ORDER}


def _normalize_summary_text(value: str) -> str:
    return str(value or "").replace("\r\n", "\n").replace("\r", "\n").strip()


def _find_first_heading_key(lines: list[str]) -> str | None:
    for line in lines:
        match = _SECTION_HEADING_RE.match(line)
        if match is None:
            continue
        key = _section_key(match.group("label"))
        if key is not None:
            return key
    return None


def _extract_heading_sections(
    lines: list[str], *, normalized: str
) -> dict[str, str] | None:
    if _find_first_heading_key(lines) is None:
        return None

    sections = _blank_sections()
    buffers = {key: [] for key, _label in _ITEM_SECTION_ORDER}
    current_key: str | None = None
    for line in lines:
        match = _SECTION_HEADING_RE.match(line)
        if match is not None:
            key = _section_key(match.group("label"))
            if key is not None:
                current_key = key
                continue
        if current_key is None:
            sections["summary"] = normalized
            return sections
        buffers[current_key].append(line)

    for key, values in buffers.items():
        sections[key] = "\n".join(values).strip()
    return sections


def _legacy_line_parts(line: str) -> tuple[str | None, str]:
    match = _LEGACY_LABEL_RE.match(line)
    if match is None:
        return None, ""
    return _section_key(match.group("label")), str(match.group("body") or "").strip()


def _append_legacy_section_body(buffers: dict[str, list[str]], *, key: str, body: str) -> None:
    if not body:
        return
    if key == "summary":
        buffers[key].append(body)
        return
    prefix = body if body.startswith(("-", "*")) else f"- {body}"
    buffers[key].append(prefix)


def _extract_legacy_sections(lines: list[str], *, normalized: str) -> dict[str, str]:
    sections = _blank_sections()
    buffers = {key: [] for key, _label in _ITEM_SECTION_ORDER}
    current_key: str | None = None
    summary_fallback: list[str] = []

    for line in lines:
        key, body = _legacy_line_parts(line)
        if key is not None:
            current_key = key
            _append_legacy_section_body(buffers, key=key, body=body)
            continue
        if current_key is not None:
            buffers[current_key].append(line)
            continue
        summary_fallback.append(line)

    for key, values in buffers.items():
        sections[key] = "\n".join(values).strip()

    if any(sections.values()):
        if summary_fallback and not sections["summary"]:
            sections["summary"] = "\n".join(summary_fallback).strip()
        return sections

    sections["summary"] = normalized
    return sections


def extract_item_summary_sections(value: str) -> dict[str, str]:
    normalized = _normalize_summary_text(value)
    sections = _blank_sections()
    if not normalized:
        return sections

    lines = normalized.split("\n")
    heading_sections = _extract_heading_sections(lines, normalized=normalized)
    if heading_sections is not None:
        return heading_sections
    return _extract_legacy_sections(lines, normalized=normalized)


def normalize_item_summary_markdown(value: str) -> str:
    sections = extract_item_summary_sections(value)
    lines: list[str] = []
    for key, label in _ITEM_SECTION_ORDER:
        lines.extend([f"## {label}"])
        body = str(sections.get(key) or "").strip()
        if body:
            lines.append(body)
        lines.append("")
    return "\n".join(lines).strip()
