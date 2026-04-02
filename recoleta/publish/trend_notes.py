from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import os
from pathlib import Path
import re
from typing import Any, TypedDict, Unpack

import yaml

from recoleta.presentation import (
    build_trend_presentation_v2,
    presentation_sidecar_path,
    resolve_presentation_language_code,
    trend_display_labels,
    write_presentation_sidecar,
)
from recoleta.provenance import ProjectionProvenance, build_projection_provenance
from recoleta.publish.trend_render_shared import (
    _trend_date_token,
    sanitize_trend_title,
    sanitize_trend_overview_markdown,
)

__all__ = [
    "resolve_trend_note_href",
    "resolve_trend_note_path",
    "write_markdown_run_index",
    "write_markdown_trend_note",
    "write_obsidian_trend_note",
]

_HISTORY_WINDOW_MENTION_RE = re.compile(
    r"(?<![\w\[])(prev_\d+)(?![\w\]])",
    re.IGNORECASE,
)
_HISTORY_WINDOW_REPEAT_WRAPPERS: tuple[tuple[str, str], ...] = (
    ("《", "》"),
    ("“", "”"),
    ("「", "」"),
    ("『", "』"),
    ('"', '"'),
)


@dataclass(frozen=True, slots=True)
class _TrendNoteRenderContext:
    trend_doc_id: int
    granularity: str
    period_start: datetime
    period_end: datetime
    run_id: str
    topics: list[str]
    projection_provenance: ProjectionProvenance | None
    site_exclude: bool
    language_code: str | None


@dataclass(frozen=True, slots=True)
class _EvolutionLabels:
    change_label: str
    history_label: str
    separator: str
    after_separator: str


@dataclass(frozen=True, slots=True)
class _EvolutionRenderContext:
    note_dir: Path
    history_window_refs: dict[str, dict[str, Any]] | None
    output_language: str | None
    labels: _EvolutionLabels


class _TrendNoteContent(TypedDict):
    title: str
    overview_md: str
    topics: list[str]
    evolution: dict[str, Any] | None
    history_window_refs: dict[str, dict[str, Any]] | None
    counter_signal: dict[str, Any] | None
    clusters: list[dict[str, Any]] | None
    highlights: list[str] | None


class _TrendNoteRenderKwargs(TypedDict):
    trend_doc_id: int
    granularity: str
    period_start: datetime
    period_end: datetime
    run_id: str
    output_language: str | None
    note_dir: Path
    projection_provenance: ProjectionProvenance | None
    site_exclude: bool
    language_code: str | None
    display_language_code: str | None
    content: _TrendNoteContent


class _TrendNoteWriteKwargs(TypedDict, total=False):
    trend_doc_id: int
    title: str
    granularity: str
    period_start: datetime
    period_end: datetime
    run_id: str
    overview_md: str
    topics: list[str]
    evolution: dict[str, Any] | None
    history_window_refs: dict[str, dict[str, Any]] | None
    counter_signal: dict[str, Any] | None
    clusters: list[dict[str, Any]] | None
    highlights: list[str] | None
    output_language: str | None
    pass_output_id: int | None
    pass_kind: str | None
    site_exclude: bool
    language_code: str | None


@dataclass(frozen=True, slots=True)
class _TrendNoteWriteInput:
    note_dir: Path
    trend_doc_id: int
    granularity: str
    period_start: datetime
    period_end: datetime
    run_id: str
    output_language: str | None
    pass_output_id: int | None
    pass_kind: str | None
    site_exclude: bool
    language_code: str | None
    emit_presentation_sidecar: bool
    content: _TrendNoteContent


def _single_line(value: str, *, fallback: str) -> str:
    cleaned = " ".join(str(value or "").split()).strip()
    return cleaned if cleaned else fallback


def _sanitize_obsidian_tag(value: str) -> str:
    raw = str(value or "").strip()
    if not raw:
        return ""
    normalized = "".join(
        ch if (ch.isalnum() or ch in {"-", "_", "/"}) else "-" for ch in raw
    )
    while "--" in normalized:
        normalized = normalized.replace("--", "-")
    normalized = normalized.strip("-")
    return normalized.lower()


def _format_author_suffix(authors: list[str], *, max_authors: int = 6) -> str:
    cleaned = [str(a).strip() for a in (authors or []) if str(a).strip()]
    if not cleaned:
        return ""
    limit = max(0, int(max_authors))
    if limit > 0 and len(cleaned) > limit:
        return f" — {'; '.join(cleaned[:limit])}; …"
    return f" — {'; '.join(cleaned)}"


def _is_chinese_output_language(output_language: str | None) -> bool:
    normalized = str(output_language or "").strip()
    if not normalized:
        return False
    lowered = normalized.lower()
    return lowered.startswith("zh") or "chinese" in lowered or "中文" in normalized


def _format_change_type_display(
    change_type: str, *, output_language: str | None
) -> str:
    normalized = str(change_type or "").strip().lower()
    zh_labels = {
        "continuing": "延续",
        "emerging": "新出现",
        "fading": "降温",
        "shifting": "转向",
        "polarizing": "分歧加剧",
    }
    en_labels = {
        "continuing": "Continuing",
        "emerging": "Emerging",
        "fading": "Fading",
        "shifting": "Shifting",
        "polarizing": "Polarizing",
    }
    if _is_chinese_output_language(output_language):
        return zh_labels.get(normalized, change_type)
    return en_labels.get(normalized, change_type)


def _history_window_title_display(raw_title: str) -> str:
    normalized = _single_line(str(raw_title or ""), fallback="")
    if not normalized:
        return ""
    normalized = normalized.replace("[", "(").replace("]", ")")
    for separator in (":", "："):
        if separator in normalized:
            prefix = normalized.split(separator, 1)[0].strip()
            if 2 <= len(prefix) <= 40:
                normalized = prefix
                break
    if len(normalized) > 48:
        normalized = normalized[:48].rstrip() + "…"
    return normalized


def _resolve_history_window_ref(
    *,
    window: str,
    history_window_refs: dict[str, dict[str, Any]] | None,
) -> dict[str, Any] | None:
    refs = history_window_refs or {}
    ref = refs.get(window)
    if isinstance(ref, dict):
        return ref
    normalized_window = window.lower()
    for candidate_key, candidate_ref in refs.items():
        if str(candidate_key or "").strip().lower() == normalized_window and isinstance(
            candidate_ref, dict
        ):
            return candidate_ref
    return None


def _history_window_display_label(*, raw: str, ref: dict[str, Any]) -> str:
    window_id = _single_line(str(ref.get("window_id") or raw), fallback=raw)
    label = _single_line(str(ref.get("label") or ""), fallback="")
    title = _history_window_title_display(str(ref.get("title") or ""))
    display_base = title or window_id
    if label and label not in {window_id, display_base}:
        return f"{display_base} ({label})"
    return display_base


def _history_window_note_href(*, note_dir: Path, ref: dict[str, Any]) -> str | None:
    try:
        trend_doc_id = int(ref.get("trend_doc_id") or 0)
    except Exception:
        trend_doc_id = 0
    granularity = str(ref.get("granularity") or "").strip().lower()
    raw_period_start = ref.get("period_start")
    try:
        period_start = (
            raw_period_start
            if isinstance(raw_period_start, datetime)
            else datetime.fromisoformat(str(raw_period_start))
        )
    except Exception:
        period_start = None
    if trend_doc_id <= 0 or not granularity or period_start is None:
        return None
    return resolve_trend_note_href(
        note_dir=note_dir,
        from_dir=note_dir,
        trend_doc_id=trend_doc_id,
        granularity=granularity,
        period_start=period_start,
    )


def resolve_trend_note_path(
    *,
    note_dir: Path,
    trend_doc_id: int,
    granularity: str,
    period_start: datetime,
) -> Path:
    token = _trend_date_token(granularity=granularity, period_start=period_start)
    return note_dir / f"{granularity}--{token}--trend--{trend_doc_id}.md"


def resolve_trend_note_href(
    *,
    note_dir: Path,
    from_dir: Path,
    trend_doc_id: int,
    granularity: str,
    period_start: datetime,
) -> str:
    note_path = resolve_trend_note_path(
        note_dir=note_dir,
        trend_doc_id=trend_doc_id,
        granularity=granularity,
        period_start=period_start,
    )
    relative = Path(os.path.relpath(note_path, start=from_dir))
    return relative.as_posix()


def _format_history_window_display(
    *,
    window: str,
    note_dir: Path,
    history_window_refs: dict[str, dict[str, Any]] | None,
) -> str:
    raw = str(window or "").strip()
    if not raw:
        return ""
    if raw.startswith("[") and "](" in raw:
        return raw
    ref = _resolve_history_window_ref(
        window=raw,
        history_window_refs=history_window_refs,
    )
    if ref is None:
        return raw
    display = _history_window_display_label(raw=raw, ref=ref)
    href = _history_window_note_href(note_dir=note_dir, ref=ref)
    if href is None:
        return display
    return f"[{display}]({href})"


def _linkify_history_window_mentions(
    text: str,
    *,
    note_dir: Path,
    history_window_refs: dict[str, dict[str, Any]] | None,
) -> str:
    raw = str(text or "").strip()
    refs = history_window_refs or {}
    if not raw or not refs or _HISTORY_WINDOW_MENTION_RE.search(raw) is None:
        return raw

    def _replace(match: re.Match[str]) -> str:
        window = str(match.group(1) or "").strip()
        ref_exists = window in refs or any(
            str(candidate_key or "").strip().lower() == window.lower()
            for candidate_key in refs
        )
        if not ref_exists:
            return window
        return _format_history_window_display(
            window=window,
            note_dir=note_dir,
            history_window_refs=history_window_refs,
        )

    return _HISTORY_WINDOW_MENTION_RE.sub(_replace, raw)


def _dedupe_repeated_history_window_titles(
    text: str,
    *,
    note_dir: Path,
    history_window_refs: dict[str, dict[str, Any]] | None,
) -> str:
    cleaned = str(text or "").strip()
    refs = history_window_refs or {}
    if not cleaned or not refs:
        return cleaned

    for window, ref in refs.items():
        rendered = _format_history_window_display(
            window=window,
            note_dir=note_dir,
            history_window_refs=history_window_refs,
        )
        if not rendered:
            continue
        raw_title = _single_line(str(ref.get("title") or ""), fallback="")
        display_title = _history_window_title_display(raw_title)
        titles = tuple(
            dict.fromkeys(title for title in (raw_title, display_title) if title)
        )
        if not titles:
            continue
        for title in titles:
            for open_wrapper, close_wrapper in _HISTORY_WINDOW_REPEAT_WRAPPERS:
                pattern = (
                    rf"({re.escape(rendered)})\s*"
                    rf"{re.escape(open_wrapper)}{re.escape(title)}{re.escape(close_wrapper)}"
                )
                cleaned = re.sub(pattern, r"\1", cleaned)
    return cleaned


def _render_evolution_text(
    text: str,
    *,
    note_dir: Path,
    history_window_refs: dict[str, dict[str, Any]] | None,
) -> str:
    linked = _linkify_history_window_mentions(
        text,
        note_dir=note_dir,
        history_window_refs=history_window_refs,
    )
    return _dedupe_repeated_history_window_titles(
        linked,
        note_dir=note_dir,
        history_window_refs=history_window_refs,
    )


def _trend_tags(topics: list[str]) -> list[str]:
    tags = ["recoleta/trend"]
    for topic in topics or []:
        normalized = _sanitize_obsidian_tag(topic)
        if normalized:
            tags.append(f"topic/{normalized}")
    seen_tags: set[str] = set()
    return [tag for tag in tags if not (tag in seen_tags or seen_tags.add(tag))]


def _build_trend_frontmatter(
    context: _TrendNoteRenderContext,
) -> dict[str, Any]:
    frontmatter = {
        "kind": "trend",
        "trend_doc_id": int(context.trend_doc_id),
        "granularity": str(context.granularity),
        "period_start": context.period_start.isoformat(),
        "period_end": context.period_end.isoformat(),
        "topics": context.topics,
        "run_id": context.run_id,
        "aliases": [f"recoleta-trend-{int(context.trend_doc_id)}"],
        "tags": _trend_tags(context.topics),
    }
    normalized_language_code = str(context.language_code or "").strip()
    if normalized_language_code:
        frontmatter["language_code"] = normalized_language_code
    if context.projection_provenance is not None:
        frontmatter.update(
            context.projection_provenance.model_dump(mode="json", exclude_none=True)
        )
    if context.site_exclude:
        frontmatter["site_exclude"] = True
    return frontmatter


def _evolution_section_labels(
    *, output_language: str | None
) -> _EvolutionLabels:
    chinese_output = _is_chinese_output_language(output_language)
    return _EvolutionLabels(
        change_label="变化" if chinese_output else "Change",
        history_label="历史窗口" if chinese_output else "History windows",
        separator="：" if chinese_output else ":",
        after_separator="" if chinese_output else " ",
    )


def _append_evolution_section(
    *,
    lines: list[str],
    evolution: dict[str, Any] | None,
    note_dir: Path,
    history_window_refs: dict[str, dict[str, Any]] | None,
    output_language: str | None,
) -> None:
    evolution = evolution or {}
    summary_md = str(evolution.get("summary_md") or "").strip()
    signals = evolution.get("signals") or []
    if not summary_md and not signals:
        return
    labels = _evolution_section_labels(output_language=output_language)
    render_context = _EvolutionRenderContext(
        note_dir=note_dir,
        history_window_refs=history_window_refs,
        output_language=output_language,
        labels=labels,
    )
    lines.extend(["", "## Evolution"])
    if summary_md:
        lines.extend(
            [
                "",
                _render_evolution_text(
                    summary_md,
                    note_dir=render_context.note_dir,
                    history_window_refs=render_context.history_window_refs,
                ),
            ]
        )
    if not isinstance(signals, list):
        return
    for signal in signals:
        _append_evolution_signal_section(
            lines=lines,
            signal=signal,
            render_context=render_context,
        )


def _evolution_signal_windows(
    *,
    signal: dict[str, Any],
    render_context: _EvolutionRenderContext,
) -> list[str]:
    history_windows = signal.get("history_windows") or []
    if not isinstance(history_windows, list):
        return []
    return [
        _format_history_window_display(
            window=str(window).strip(),
            note_dir=render_context.note_dir,
            history_window_refs=render_context.history_window_refs,
        )
        for window in history_windows
        if str(window).strip()
    ]


def _append_evolution_signal_section(
    *,
    lines: list[str],
    signal: Any,
    render_context: _EvolutionRenderContext,
) -> None:
    if not isinstance(signal, dict):
        return
    theme = _single_line(str(signal.get("theme") or ""), fallback="Signal")
    change_type = _single_line(
        _format_change_type_display(
            str(signal.get("change_type") or ""),
            output_language=render_context.output_language,
        ),
        fallback="unspecified",
    )
    lines.extend(["", f"### {theme}", ""])
    _append_evolution_change_line(
        lines=lines,
        change_type=change_type,
        labels=render_context.labels,
    )
    windows = _evolution_signal_windows(
        signal=signal,
        render_context=render_context,
    )
    _append_evolution_history_line(
        lines=lines,
        windows=windows,
        labels=render_context.labels,
    )
    _append_evolution_summary(
        lines=lines,
        signal=signal,
        render_context=render_context,
    )


def _append_evolution_change_line(
    *,
    lines: list[str],
    change_type: str,
    labels: _EvolutionLabels,
) -> None:
    lines.append(
        f"- {labels.change_label}{labels.separator}{labels.after_separator}{change_type}"
    )


def _append_evolution_history_line(
    *,
    lines: list[str],
    windows: list[str],
    labels: _EvolutionLabels,
) -> None:
    if not windows:
        return
    lines.append(
        f"- {labels.history_label}{labels.separator}{labels.after_separator}{', '.join(windows)}"
    )


def _append_evolution_summary(
    *,
    lines: list[str],
    signal: dict[str, Any],
    render_context: _EvolutionRenderContext,
) -> None:
    summary = _render_evolution_text(
        str(signal.get("summary") or "").strip(),
        note_dir=render_context.note_dir,
        history_window_refs=render_context.history_window_refs,
    )
    if summary:
        lines.extend(["", summary])


def _cluster_representative_lines(
    *,
    reps: list[dict[str, Any]],
) -> list[str]:
    lines: list[str] = []
    seen_rep_targets: set[str] = set()
    for rep in reps[:6]:
        rendered_line, rep_target = _cluster_representative_line(rep)
        if rendered_line is None or rep_target is None:
            continue
        if rep_target in seen_rep_targets:
            continue
        seen_rep_targets.add(rep_target)
        lines.append(rendered_line)
    return lines


def _cluster_representative_line(rep: Any) -> tuple[str | None, str | None]:
    if not isinstance(rep, dict):
        return None, None
    rep_title = str(rep.get("title") or "").strip()
    if not rep_title:
        return None, None
    note_href = str(rep.get("note_href") or "").strip()
    url = str(rep.get("url") or "").strip()
    authors = _cluster_representative_authors(rep)
    author_suffix = _format_author_suffix(authors, max_authors=6)
    rep_target = note_href or url or rep_title
    if note_href:
        return f"- [{rep_title}]({note_href}){author_suffix}", rep_target
    if url:
        return f"- [{rep_title}]({url}){author_suffix}", rep_target
    return f"- {rep_title}{author_suffix}", rep_target


def _cluster_representative_authors(rep: dict[str, Any]) -> list[str]:
    authors_raw = rep.get("authors")
    if not isinstance(authors_raw, list):
        return []
    return [str(author).strip() for author in authors_raw if str(author).strip()]


def _append_cluster_sections(
    *,
    lines: list[str],
    clusters: list[dict[str, Any]] | None,
    display_labels: dict[str, str],
    note_dir: Path,
    history_window_refs: dict[str, dict[str, Any]] | None,
) -> None:
    lines.extend(["", f"## {display_labels['clusters']}"])
    normalized_clusters = clusters or []
    if not normalized_clusters:
        lines.append("- (none)")
        return
    for cluster in normalized_clusters:
        name = _single_line(str(cluster.get("name") or ""), fallback="Cluster")
        desc = _render_evolution_text(
            str(cluster.get("description") or "").strip(),
            note_dir=note_dir,
            history_window_refs=history_window_refs,
        )
        lines.extend(["", f"### {name}", ""])
        if desc:
            lines.append(desc)
            lines.append("")
        reps = cluster.get("representative_chunks") or []
        if not isinstance(reps, list) or not reps:
            continue
        representative_lines = _cluster_representative_lines(reps=reps)
        if not representative_lines:
            continue
        lines.append(f"#### {display_labels['representative_sources']}")
        lines.extend(representative_lines)
        lines.append("")


def _append_counter_signal_section(
    *,
    lines: list[str],
    counter_signal: dict[str, Any] | None,
    display_labels: dict[str, str],
    note_dir: Path,
    history_window_refs: dict[str, dict[str, Any]] | None,
) -> None:
    if not isinstance(counter_signal, dict):
        return
    title = _single_line(str(counter_signal.get("title") or ""), fallback="")
    summary = _render_evolution_text(
        str(counter_signal.get("summary") or "").strip(),
        note_dir=note_dir,
        history_window_refs=history_window_refs,
    )
    evidence = counter_signal.get("evidence") or []
    if not title and not summary and not evidence:
        return
    lines.extend(["", f"## {display_labels['counter_signal']}"])
    if title:
        lines.extend(["", f"### {title}"])
    if summary:
        lines.extend(["", summary])
    evidence_lines = _counter_signal_evidence_lines(evidence=evidence)
    if evidence_lines:
        lines.extend(["", f"#### {display_labels['representative_sources']}"])
        lines.extend(evidence_lines)


def _counter_signal_evidence_lines(*, evidence: Any) -> list[str]:
    if not isinstance(evidence, list):
        return []
    lines: list[str] = []
    for entry in evidence:
        rendered_line, _ = _cluster_representative_line(
            {
                "title": entry.get("title"),
                "note_href": entry.get("note_href") or entry.get("href"),
                "url": entry.get("url"),
                "authors": entry.get("authors"),
            }
        )
        if rendered_line is not None:
            lines.append(rendered_line)
    return lines


def _render_trend_note_lines(*, kwargs: _TrendNoteRenderKwargs) -> list[str]:
    content = kwargs["content"]
    _ = content.get("highlights")
    title = sanitize_trend_title(content["title"])
    overview_md = sanitize_trend_overview_markdown(content["overview_md"])
    render_context = _TrendNoteRenderContext(
        trend_doc_id=kwargs["trend_doc_id"],
        granularity=kwargs["granularity"],
        period_start=kwargs["period_start"],
        period_end=kwargs["period_end"],
        run_id=kwargs["run_id"],
        topics=content["topics"],
        projection_provenance=kwargs["projection_provenance"],
        site_exclude=kwargs["site_exclude"],
        language_code=kwargs["language_code"],
    )
    frontmatter = _build_trend_frontmatter(render_context)

    lines: list[str] = [
        "---",
        yaml.safe_dump(frontmatter, sort_keys=False).strip(),
        "---",
        "",
        f"# {title}",
        "",
    ]
    display_labels = trend_display_labels(language_code=kwargs["display_language_code"])
    rendered_overview_md = _render_evolution_text(
        overview_md,
        note_dir=kwargs["note_dir"],
        history_window_refs=content["history_window_refs"],
    )
    lines.extend(
        [
            f"## {display_labels['overview']}",
            rendered_overview_md,
        ]
    )
    _append_evolution_section(
        lines=lines,
        evolution=content["evolution"],
        note_dir=kwargs["note_dir"],
        history_window_refs=content["history_window_refs"],
        output_language=kwargs["output_language"],
    )
    _append_counter_signal_section(
        lines=lines,
        counter_signal=content["counter_signal"],
        display_labels=display_labels,
        note_dir=kwargs["note_dir"],
        history_window_refs=content["history_window_refs"],
    )
    _append_cluster_sections(
        lines=lines,
        clusters=content["clusters"],
        display_labels=display_labels,
        note_dir=kwargs["note_dir"],
        history_window_refs=content["history_window_refs"],
    )

    return lines


def _render_trend_note_content(**kwargs: Unpack[_TrendNoteWriteKwargs]) -> _TrendNoteContent:
    return {
        "title": kwargs["title"],
        "overview_md": kwargs["overview_md"],
        "topics": kwargs["topics"],
        "evolution": kwargs.get("evolution"),
        "history_window_refs": kwargs.get("history_window_refs"),
        "counter_signal": kwargs.get("counter_signal"),
        "clusters": kwargs.get("clusters"),
        "highlights": kwargs.get("highlights"),
    }


def _write_trend_note(
    *,
    write_input: _TrendNoteWriteInput,
) -> Path:
    note_dir = write_input.note_dir
    note_dir.mkdir(parents=True, exist_ok=True)
    resolved_language_code = resolve_presentation_language_code(
        language_code=write_input.language_code,
        output_language=write_input.output_language,
    )
    resolved_display_language_code = (
        resolve_presentation_language_code(language_code=write_input.language_code) or "en"
    )
    sanitized_title = sanitize_trend_title(write_input.content["title"])
    sanitized_overview_md = sanitize_trend_overview_markdown(
        write_input.content["overview_md"]
    )
    note_path = resolve_trend_note_path(
        note_dir=note_dir,
        trend_doc_id=write_input.trend_doc_id,
        granularity=write_input.granularity,
        period_start=write_input.period_start,
    )
    lines = _render_trend_note_lines(
        kwargs={
            "trend_doc_id": write_input.trend_doc_id,
            "granularity": write_input.granularity,
            "period_start": write_input.period_start,
            "period_end": write_input.period_end,
            "run_id": write_input.run_id,
            "output_language": write_input.output_language,
            "note_dir": note_dir,
            "projection_provenance": (
                build_projection_provenance(
                    pass_output_id=write_input.pass_output_id,
                    pass_kind=str(write_input.pass_kind or "").strip() or "trend_synthesis",
                )
                if write_input.pass_output_id is not None
                else None
            ),
            "site_exclude": bool(write_input.site_exclude),
            "language_code": resolved_language_code,
            "display_language_code": resolved_display_language_code,
            "content": write_input.content,
        }
    )
    note_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    if not write_input.emit_presentation_sidecar:
        return note_path

    presentation = build_trend_presentation_v2(
        source_markdown_path=f"{note_dir.name}/{note_path.name}",
        title=sanitized_title,
        overview_md=sanitized_overview_md,
        evolution=write_input.content["evolution"],
        history_window_refs=write_input.content["history_window_refs"],
        clusters=write_input.content["clusters"],
        counter_signal=write_input.content["counter_signal"],
        language_code=resolved_language_code,
        display_language_code=resolved_display_language_code,
    )
    try:
        write_presentation_sidecar(note_path=note_path, presentation=presentation)
    except Exception:
        note_path.unlink(missing_ok=True)
        presentation_sidecar_path(note_path=note_path).unlink(missing_ok=True)
        raise
    return note_path


def write_obsidian_trend_note(
    *,
    vault_path: Path,
    base_folder: str,
    **kwargs: Unpack[_TrendNoteWriteKwargs],
) -> Path:
    note_dir = vault_path / base_folder / "Trends"
    return _write_trend_note(
        write_input=_TrendNoteWriteInput(
            note_dir=note_dir,
            trend_doc_id=kwargs["trend_doc_id"],
            granularity=kwargs["granularity"],
            period_start=kwargs["period_start"],
            period_end=kwargs["period_end"],
            run_id=kwargs["run_id"],
            output_language=kwargs.get("output_language"),
            pass_output_id=kwargs.get("pass_output_id"),
            pass_kind=kwargs.get("pass_kind"),
            site_exclude=bool(kwargs.get("site_exclude", False)),
            language_code=kwargs.get("language_code"),
            emit_presentation_sidecar=False,
            content=_render_trend_note_content(**kwargs),
        )
    )


def write_markdown_trend_note(
    *,
    output_dir: Path,
    **kwargs: Unpack[_TrendNoteWriteKwargs],
) -> Path:
    output_dir = output_dir.expanduser().resolve()
    if output_dir.exists() and not output_dir.is_dir():
        raise ValueError("MARKDOWN_OUTPUT_DIR must be a directory")
    trends_dir = output_dir / "Trends"
    return _write_trend_note(
        write_input=_TrendNoteWriteInput(
            note_dir=trends_dir,
            trend_doc_id=kwargs["trend_doc_id"],
            granularity=kwargs["granularity"],
            period_start=kwargs["period_start"],
            period_end=kwargs["period_end"],
            run_id=kwargs["run_id"],
            output_language=kwargs.get("output_language"),
            pass_output_id=kwargs.get("pass_output_id"),
            pass_kind=kwargs.get("pass_kind"),
            site_exclude=bool(kwargs.get("site_exclude", False)),
            language_code=kwargs.get("language_code"),
            emit_presentation_sidecar=True,
            content=_render_trend_note_content(**kwargs),
        )
    )


def write_markdown_run_index(
    *,
    output_dir: Path,
    run_id: str,
    generated_at: datetime,
    notes: list[tuple[str, Path]],
) -> Path:
    output_dir = output_dir.expanduser().resolve()
    if output_dir.exists() and not output_dir.is_dir():
        raise ValueError("MARKDOWN_OUTPUT_DIR must be a directory")
    output_dir.mkdir(parents=True, exist_ok=True)

    def sanitize_segment(
        value: str, *, max_len: int = 72, fallback: str = "unknown"
    ) -> str:
        cleaned = str(value).strip()
        normalized = "".join(
            ch if (ch.isalnum() or ch in {"-", "_"}) else "_" for ch in cleaned
        )
        while "__" in normalized:
            normalized = normalized.replace("__", "_")
        normalized = normalized.strip("_")
        if not normalized:
            return fallback
        return normalized[:max_len]

    safe_run_id = sanitize_segment(run_id, fallback="run")
    runs_dir = output_dir / "Runs"
    runs_dir.mkdir(parents=True, exist_ok=True)
    run_index_path = runs_dir / f"{safe_run_id}.md"
    latest_path = output_dir / "latest.md"

    lines: list[str] = [
        "# Recoleta publish output",
        "",
        f"- Run ID: `{run_id}`",
        f"- Generated at (UTC): `{generated_at.astimezone(timezone.utc).isoformat()}`",
        "",
        "## Notes",
    ]
    if not notes:
        lines.extend(["", "_No items published in this run._", ""])
    else:
        for title, note_path in notes:
            rel: str
            try:
                rel = str(note_path.resolve().relative_to(output_dir))
            except Exception:
                rel = str(note_path)
            lines.append(f"- [{title}]({rel})")
        lines.append("")

    payload = "\n".join(lines).strip() + "\n"
    run_index_path.write_text(payload, encoding="utf-8")
    latest_path.write_text(payload, encoding="utf-8")
    return latest_path
