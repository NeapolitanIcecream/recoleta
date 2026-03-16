from __future__ import annotations

from datetime import datetime, timezone
import os
from pathlib import Path
import re
from typing import Any

import yaml
from slugify import slugify

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
    "write_markdown_stream_index",
    "write_markdown_trend_note",
    "write_obsidian_trend_note",
]

_HISTORY_WINDOW_MENTION_RE = re.compile(r"(?<![\w\[])(prev_\d+)(?![\w\]])")
_HISTORY_WINDOW_REPEAT_WRAPPERS: tuple[tuple[str, str], ...] = (
    ("《", "》"),
    ("“", "”"),
    ("「", "」"),
    ("『", "』"),
    ('"', '"'),
)


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
    ref = (history_window_refs or {}).get(raw)
    if not isinstance(ref, dict):
        return raw
    window_id = _single_line(str(ref.get("window_id") or raw), fallback=raw)
    label = _single_line(str(ref.get("label") or ""), fallback="")
    title = _history_window_title_display(str(ref.get("title") or ""))
    display_base = title or window_id
    display = (
        f"{display_base} ({label})"
        if label and label not in {window_id, display_base}
        else display_base
    )
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
        return display
    href = resolve_trend_note_href(
        note_dir=note_dir,
        from_dir=note_dir,
        trend_doc_id=trend_doc_id,
        granularity=granularity,
        period_start=period_start,
    )
    return f"[{display}]({href})"


def _linkify_history_window_mentions(
    text: str,
    *,
    note_dir: Path,
    history_window_refs: dict[str, dict[str, Any]] | None,
) -> str:
    raw = str(text or "").strip()
    refs = history_window_refs or {}
    if not raw or not refs or "prev_" not in raw:
        return raw

    def _replace(match: re.Match[str]) -> str:
        window = str(match.group(1) or "").strip()
        if window not in refs:
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


def _render_trend_note_lines(
    *,
    title: str,
    trend_doc_id: int,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
    run_id: str,
    overview_md: str,
    topics: list[str],
    evolution: dict[str, Any] | None,
    history_window_refs: dict[str, dict[str, Any]] | None,
    clusters: list[dict[str, Any]] | None,
    highlights: list[str] | None,
    output_language: str | None,
    note_dir: Path,
    projection_provenance: ProjectionProvenance | None,
    site_exclude: bool,
) -> list[str]:
    _ = highlights
    title = sanitize_trend_title(title)
    overview_md = sanitize_trend_overview_markdown(overview_md)
    tags = ["recoleta/trend"]
    for topic in topics or []:
        normalized = _sanitize_obsidian_tag(topic)
        if normalized:
            tags.append(f"topic/{normalized}")
    seen_tags: set[str] = set()
    tags = [t for t in tags if not (t in seen_tags or seen_tags.add(t))]

    frontmatter = {
        "kind": "trend",
        "trend_doc_id": int(trend_doc_id),
        "granularity": str(granularity),
        "period_start": period_start.isoformat(),
        "period_end": period_end.isoformat(),
        "topics": topics,
        "run_id": run_id,
        "aliases": [f"recoleta-trend-{int(trend_doc_id)}"],
        "tags": tags,
    }
    if projection_provenance is not None:
        frontmatter.update(
            projection_provenance.model_dump(mode="json", exclude_none=True)
        )
    if site_exclude:
        frontmatter["site_exclude"] = True

    lines: list[str] = [
        "---",
        yaml.safe_dump(frontmatter, sort_keys=False).strip(),
        "---",
        "",
        f"# {title}",
        "",
    ]
    lines.extend(
        [
            "## Overview",
            (overview_md or "").strip(),
        ]
    )

    evolution = evolution or {}
    summary_md = str(evolution.get("summary_md") or "").strip()
    signals = evolution.get("signals") or []
    if summary_md or signals:
        chinese_output = _is_chinese_output_language(output_language)
        change_label = "变化" if chinese_output else "Change"
        history_label = (
            "历史窗口" if chinese_output else "History windows"
        )
        separator = "：" if chinese_output else ":"
        after_separator = "" if chinese_output else " "
        lines.extend(["", "## Evolution"])
        if summary_md:
            lines.extend(
                [
                    "",
                    _render_evolution_text(
                        summary_md,
                        note_dir=note_dir,
                        history_window_refs=history_window_refs,
                    ),
                ]
            )
        if isinstance(signals, list):
            for signal in signals:
                if not isinstance(signal, dict):
                    continue
                theme = _single_line(str(signal.get("theme") or ""), fallback="Signal")
                change_type = _single_line(
                    _format_change_type_display(
                        str(signal.get("change_type") or ""),
                        output_language=output_language,
                    ),
                    fallback="unspecified",
                )
                summary = _render_evolution_text(
                    str(signal.get("summary") or "").strip(),
                    note_dir=note_dir,
                    history_window_refs=history_window_refs,
                )
                history_windows = signal.get("history_windows") or []
                lines.extend(["", f"### {theme}", ""])
                lines.append(
                    f"- {change_label}{separator}{after_separator}{change_type}"
                )
                if isinstance(history_windows, list):
                    windows = [
                        _format_history_window_display(
                            window=str(window).strip(),
                            note_dir=note_dir,
                            history_window_refs=history_window_refs,
                        )
                        for window in history_windows
                        if str(window).strip()
                    ]
                    if windows:
                        lines.append(
                            f"- {history_label}{separator}{after_separator}{', '.join(windows)}"
                        )
                if summary:
                    lines.extend(["", summary])

    lines.extend(["", "## Clusters"])
    clusters = clusters or []
    if clusters:
        for cluster in clusters:
            name = _single_line(str(cluster.get("name") or ""), fallback="Cluster")
            desc = str(cluster.get("description") or "").strip()
            lines.extend(["", f"### {name}", ""])
            if desc:
                lines.append(desc)
                lines.append("")
            reps = cluster.get("representative_chunks") or []
            if isinstance(reps, list) and reps:
                lines.append("#### Representative sources")
                seen_rep_targets: set[str] = set()
                for rep in reps[:6]:
                    if not isinstance(rep, dict):
                        continue
                    rep_title = str(rep.get("title") or "").strip()
                    if not rep_title:
                        continue
                    note_href = str(rep.get("note_href") or "").strip()
                    url = str(rep.get("url") or "").strip()
                    authors_raw = rep.get("authors")
                    authors: list[str] = []
                    if isinstance(authors_raw, list):
                        authors = [
                            str(a).strip() for a in authors_raw if str(a).strip()
                        ]
                    author_suffix = _format_author_suffix(authors, max_authors=6)
                    rep_target = note_href or url or rep_title
                    if rep_target in seen_rep_targets:
                        continue
                    seen_rep_targets.add(rep_target)
                    if note_href:
                        lines.append(f"- [{rep_title}]({note_href}){author_suffix}")
                    elif url:
                        lines.append(f"- [{rep_title}]({url}){author_suffix}")
                    else:
                        lines.append(f"- {rep_title}{author_suffix}")
                lines.append("")
    else:
        lines.append("- (none)")

    return lines


def _write_trend_note(
    *,
    note_dir: Path,
    trend_doc_id: int,
    title: str,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
    run_id: str,
    overview_md: str,
    topics: list[str],
    evolution: dict[str, Any] | None,
    history_window_refs: dict[str, dict[str, Any]] | None,
    clusters: list[dict[str, Any]] | None,
    highlights: list[str] | None,
    output_language: str | None,
    pass_output_id: int | None = None,
    pass_kind: str | None = None,
    site_exclude: bool = False,
) -> Path:
    note_dir.mkdir(parents=True, exist_ok=True)
    note_path = resolve_trend_note_path(
        note_dir=note_dir,
        trend_doc_id=trend_doc_id,
        granularity=granularity,
        period_start=period_start,
    )
    lines = _render_trend_note_lines(
        title=title,
        trend_doc_id=trend_doc_id,
        granularity=granularity,
        period_start=period_start,
        period_end=period_end,
        run_id=run_id,
        overview_md=overview_md,
        topics=topics,
        evolution=evolution,
        history_window_refs=history_window_refs,
        clusters=clusters,
        highlights=highlights,
        output_language=output_language,
        note_dir=note_dir,
        projection_provenance=(
            build_projection_provenance(
                pass_output_id=pass_output_id,
                pass_kind=str(pass_kind or "").strip() or "trend_synthesis",
            )
            if pass_output_id is not None
            else None
        ),
        site_exclude=bool(site_exclude),
    )
    note_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    return note_path


def write_obsidian_trend_note(
    *,
    vault_path: Path,
    base_folder: str,
    trend_doc_id: int,
    title: str,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
    run_id: str,
    overview_md: str,
    topics: list[str],
    evolution: dict[str, Any] | None = None,
    history_window_refs: dict[str, dict[str, Any]] | None = None,
    clusters: list[dict[str, Any]] | None = None,
    highlights: list[str] | None = None,
    output_language: str | None = None,
    pass_output_id: int | None = None,
    pass_kind: str | None = None,
    site_exclude: bool = False,
) -> Path:
    note_dir = vault_path / base_folder / "Trends"
    return _write_trend_note(
        note_dir=note_dir,
        trend_doc_id=trend_doc_id,
        title=title,
        granularity=granularity,
        period_start=period_start,
        period_end=period_end,
        run_id=run_id,
        overview_md=overview_md,
        topics=topics,
        evolution=evolution,
        history_window_refs=history_window_refs,
        clusters=clusters,
        highlights=highlights,
        output_language=output_language,
        pass_output_id=pass_output_id,
        pass_kind=pass_kind,
        site_exclude=site_exclude,
    )


def write_markdown_trend_note(
    *,
    output_dir: Path,
    trend_doc_id: int,
    title: str,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
    run_id: str,
    overview_md: str,
    topics: list[str],
    evolution: dict[str, Any] | None = None,
    history_window_refs: dict[str, dict[str, Any]] | None = None,
    clusters: list[dict[str, Any]] | None = None,
    highlights: list[str] | None = None,
    output_language: str | None = None,
    pass_output_id: int | None = None,
    pass_kind: str | None = None,
    site_exclude: bool = False,
) -> Path:
    output_dir = output_dir.expanduser().resolve()
    if output_dir.exists() and not output_dir.is_dir():
        raise ValueError("MARKDOWN_OUTPUT_DIR must be a directory")
    trends_dir = output_dir / "Trends"
    return _write_trend_note(
        note_dir=trends_dir,
        trend_doc_id=trend_doc_id,
        title=title,
        granularity=granularity,
        period_start=period_start,
        period_end=period_end,
        run_id=run_id,
        overview_md=overview_md,
        topics=topics,
        evolution=evolution,
        history_window_refs=history_window_refs,
        clusters=clusters,
        highlights=highlights,
        output_language=output_language,
        pass_output_id=pass_output_id,
        pass_kind=pass_kind,
        site_exclude=site_exclude,
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


def write_markdown_stream_index(
    *,
    output_dir: Path,
    run_id: str,
    generated_at: datetime,
    streams: list[tuple[str, Path]],
) -> Path:
    output_dir = output_dir.expanduser().resolve()
    if output_dir.exists() and not output_dir.is_dir():
        raise ValueError("MARKDOWN_OUTPUT_DIR must be a directory")
    output_dir.mkdir(parents=True, exist_ok=True)

    safe_run_id = slugify(run_id, lowercase=True) or "run"
    runs_dir = output_dir / "Runs"
    runs_dir.mkdir(parents=True, exist_ok=True)
    run_index_path = runs_dir / f"{safe_run_id}--streams.md"
    latest_path = output_dir / "latest.md"

    lines: list[str] = [
        "# Recoleta topic streams",
        "",
        f"- Run ID: `{run_id}`",
        f"- Generated at (UTC): `{generated_at.astimezone(timezone.utc).isoformat()}`",
        "",
        "## Streams",
    ]
    if not streams:
        lines.extend(["", "_No topic streams published in this run._", ""])
    else:
        for stream_name, latest_stream_path in streams:
            rel: str
            try:
                rel = str(latest_stream_path.resolve().relative_to(output_dir))
            except Exception:
                rel = str(latest_stream_path)
            lines.append(f"- [{stream_name}]({rel})")
        lines.append("")

    payload = "\n".join(lines).strip() + "\n"
    run_index_path.write_text(payload, encoding="utf-8")
    latest_path.write_text(payload, encoding="utf-8")
    return latest_path
