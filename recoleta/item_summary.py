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


def extract_item_summary_sections(value: str) -> dict[str, str]:
    normalized = str(value or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    sections = {key: "" for key, _label in _ITEM_SECTION_ORDER}
    if not normalized:
        return sections

    lines = normalized.split("\n")
    current_key: str | None = None
    saw_heading = False
    for line in lines:
        match = _SECTION_HEADING_RE.match(line)
        if match is None:
            continue
        key = _section_key(match.group("label"))
        if key is None:
            continue
        current_key = key
        saw_heading = True
        break

    if saw_heading:
        current_key = None
        buffers = {key: [] for key, _label in _ITEM_SECTION_ORDER}
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

    buffers = {key: [] for key, _label in _ITEM_SECTION_ORDER}
    current_key = None
    summary_fallback: list[str] = []
    for line in lines:
        match = _LEGACY_LABEL_RE.match(line)
        if match is not None:
            key = _section_key(match.group("label"))
            if key is None:
                continue
            body = str(match.group("body") or "").strip()
            current_key = key
            if body:
                if key == "summary":
                    buffers[key].append(body)
                else:
                    prefix = body if body.startswith(("-", "*")) else f"- {body}"
                    buffers[key].append(prefix)
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
