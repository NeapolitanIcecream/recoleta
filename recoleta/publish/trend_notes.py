from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import os
from pathlib import Path
from types import SimpleNamespace
from typing import Any, NotRequired, Required, TypedDict, Unpack

import yaml

from recoleta.presentation import (
    TrendPresentationBuildRequest,
    build_trend_presentation_v2,
    presentation_sidecar_path,
    resolve_presentation_language_code,
    trend_display_labels,
    write_presentation_sidecar,
)
from recoleta.provenance import ProjectionProvenance, build_projection_provenance
from recoleta.publish.trend_render_shared import (
    _trend_date_token,
    sanitize_trend_overview_markdown,
    sanitize_trend_title,
)

__all__ = [
    "resolve_trend_note_href",
    "resolve_trend_note_path",
    "write_markdown_run_index",
    "write_markdown_trend_note",
    "write_obsidian_trend_note",
]


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


class _TrendNoteContent(TypedDict):
    title: str
    overview_md: str
    topics: list[str]
    clusters: list[dict[str, Any]] | None


class _TrendNoteWriteKwargs(TypedDict, total=False):
    trend_doc_id: Required[int]
    title: Required[str]
    granularity: Required[str]
    period_start: Required[datetime]
    period_end: Required[datetime]
    run_id: Required[str]
    overview_md: Required[str]
    topics: Required[list[str]]
    clusters: NotRequired[list[dict[str, Any]] | None]
    output_language: NotRequired[str | None]
    pass_output_id: NotRequired[int | None]
    pass_kind: NotRequired[str | None]
    site_exclude: NotRequired[bool]
    language_code: NotRequired[str | None]


_TREND_NOTE_REQUIRED_KEYS = (
    "trend_doc_id",
    "title",
    "granularity",
    "period_start",
    "period_end",
    "run_id",
    "overview_md",
    "topics",
)
_TREND_NOTE_DEFAULTS: dict[str, Any] = {
    "clusters": None,
    "output_language": None,
    "pass_output_id": None,
    "pass_kind": None,
    "site_exclude": False,
    "language_code": None,
}


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


def _trend_tags(topics: list[str]) -> list[str]:
    tags = ["recoleta/trend"]
    for topic in topics or []:
        normalized = _sanitize_obsidian_tag(topic)
        if normalized:
            tags.append(f"topic/{normalized}")
    seen_tags: set[str] = set()
    return [tag for tag in tags if not (tag in seen_tags or seen_tags.add(tag))]


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
    return Path(os.path.relpath(note_path, start=from_dir)).as_posix()


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


def _cluster_lines(
    *,
    cluster: dict[str, Any],
    labels: dict[str, str],
) -> list[str]:
    lines = [
        "",
        f"### {_single_line(str(cluster.get('title') or ''), fallback='Cluster')}",
        str(cluster.get("content") or "").strip() or "(empty)",
    ]
    evidence_lines = _cluster_evidence_lines(cluster=cluster)
    if evidence_lines:
        lines.extend(["", f"#### {labels['evidence']}", *evidence_lines])
    return lines


def _cluster_evidence_lines(*, cluster: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for entry in list(cluster.get("evidence") or []):
        line = _cluster_evidence_line(entry)
        if line:
            lines.append(line)
    return lines


def _cluster_evidence_line(entry: Any) -> str | None:
    if not isinstance(entry, dict):
        return None
    entry_title = _single_line(str(entry.get("title") or ""), fallback="Document")
    href = _single_line(str(entry.get("href") or entry.get("url") or ""), fallback="")
    reason = _single_line(str(entry.get("reason") or ""), fallback="")
    line = f"- [{entry_title}]({href})" if href else f"- {entry_title}"
    if reason:
        line += f": {reason}"
    return line


def _render_trend_note_lines(
    *,
    write_input: _TrendNoteWriteInput,
    presentation: dict[str, Any],
) -> list[str]:
    title = sanitize_trend_title(write_input.content["title"])
    overview_md = sanitize_trend_overview_markdown(write_input.content["overview_md"])
    render_context = _TrendNoteRenderContext(
        trend_doc_id=write_input.trend_doc_id,
        granularity=write_input.granularity,
        period_start=write_input.period_start,
        period_end=write_input.period_end,
        run_id=write_input.run_id,
        topics=write_input.content["topics"],
        projection_provenance=(
            build_projection_provenance(
                pass_output_id=write_input.pass_output_id,
                pass_kind=str(write_input.pass_kind or "").strip()
                or "trend_synthesis",
            )
            if write_input.pass_output_id is not None
            else None
        ),
        site_exclude=bool(write_input.site_exclude),
        language_code=write_input.language_code,
    )
    labels = trend_display_labels(language_code=write_input.language_code)
    lines = [
        "---",
        yaml.safe_dump(_build_trend_frontmatter(render_context), sort_keys=False).strip(),
        "---",
        "",
        f"# {title}",
        "",
        f"## {labels['overview']}",
        overview_md,
        "",
        f"## {labels['clusters']}",
    ]
    clusters = list(presentation["content"].get("clusters") or [])
    if not clusters:
        lines.append("- (none)")
        return lines
    for cluster in clusters:
        if isinstance(cluster, dict):
            lines.extend(_cluster_lines(cluster=cluster, labels=labels))
    return lines


def _render_trend_note_content(
    **kwargs: Unpack[_TrendNoteWriteKwargs],
) -> _TrendNoteContent:
    return {
        "title": kwargs["title"],
        "overview_md": kwargs["overview_md"],
        "topics": kwargs["topics"],
        "clusters": kwargs.get("clusters"),
    }


def _validated_trend_note_write_kwargs(
    *,
    function_name: str,
    kwargs: _TrendNoteWriteKwargs,
) -> dict[str, Any]:
    allowed_keys = set(_TREND_NOTE_REQUIRED_KEYS) | set(_TREND_NOTE_DEFAULTS)
    unexpected = [key for key in kwargs if key not in allowed_keys]
    if unexpected:
        raise TypeError(
            f"{function_name}() got an unexpected keyword argument {unexpected[0]!r}"
        )
    missing = [key for key in _TREND_NOTE_REQUIRED_KEYS if key not in kwargs]
    if missing:
        missing_repr = ", ".join(repr(key) for key in missing)
        plural = "s" if len(missing) != 1 else ""
        raise TypeError(
            f"{function_name}() missing required keyword-only argument{plural}: {missing_repr}"
        )
    return {**_TREND_NOTE_DEFAULTS, **kwargs}


def _presentation_ready_clusters(
    clusters: list[dict[str, Any]] | None,
) -> list[Any]:
    prepared: list[Any] = []
    for cluster in list(clusters or []):
        if not isinstance(cluster, dict):
            continue
        prepared.append(
            SimpleNamespace(
                title=str(cluster.get("title") or "").strip(),
                content_md=str(cluster.get("content_md") or cluster.get("content") or "").strip(),
                evidence_refs=list(cluster.get("evidence_refs") or cluster.get("evidence") or []),
            )
        )
    return prepared


def _write_trend_note(
    *,
    write_input: _TrendNoteWriteInput,
) -> Path:
    write_input.note_dir.mkdir(parents=True, exist_ok=True)
    resolved_language_code = resolve_presentation_language_code(
        language_code=write_input.language_code,
        output_language=write_input.output_language,
    )
    note_path = resolve_trend_note_path(
        note_dir=write_input.note_dir,
        trend_doc_id=write_input.trend_doc_id,
        granularity=write_input.granularity,
        period_start=write_input.period_start,
    )
    presentation = build_trend_presentation_v2(
        request=TrendPresentationBuildRequest(
            source_markdown_path=f"{write_input.note_dir.name}/{note_path.name}",
            title=sanitize_trend_title(write_input.content["title"]),
            overview_md=sanitize_trend_overview_markdown(
                write_input.content["overview_md"]
            ),
            clusters=_presentation_ready_clusters(write_input.content["clusters"]),
            language_code=resolved_language_code,
            display_language_code=resolved_language_code,
        ),
    )
    note_path.write_text(
        "\n".join(
            _render_trend_note_lines(
                write_input=_TrendNoteWriteInput(
                    note_dir=write_input.note_dir,
                    trend_doc_id=write_input.trend_doc_id,
                    granularity=write_input.granularity,
                    period_start=write_input.period_start,
                    period_end=write_input.period_end,
                    run_id=write_input.run_id,
                    output_language=write_input.output_language,
                    pass_output_id=write_input.pass_output_id,
                    pass_kind=write_input.pass_kind,
                    site_exclude=write_input.site_exclude,
                    language_code=resolved_language_code,
                    emit_presentation_sidecar=write_input.emit_presentation_sidecar,
                    content=write_input.content,
                ),
                presentation=presentation,
            )
        ).strip()
        + "\n",
        encoding="utf-8",
    )
    if write_input.emit_presentation_sidecar:
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
    normalized_kwargs = _validated_trend_note_write_kwargs(
        function_name="write_obsidian_trend_note",
        kwargs=kwargs,
    )
    return _write_trend_note(
        write_input=_TrendNoteWriteInput(
            note_dir=vault_path / base_folder / "Trends",
            trend_doc_id=normalized_kwargs["trend_doc_id"],
            granularity=normalized_kwargs["granularity"],
            period_start=normalized_kwargs["period_start"],
            period_end=normalized_kwargs["period_end"],
            run_id=normalized_kwargs["run_id"],
            output_language=normalized_kwargs["output_language"],
            pass_output_id=normalized_kwargs["pass_output_id"],
            pass_kind=normalized_kwargs["pass_kind"],
            site_exclude=bool(normalized_kwargs["site_exclude"]),
            language_code=normalized_kwargs["language_code"],
            emit_presentation_sidecar=False,
            content=_render_trend_note_content(**normalized_kwargs),
        )
    )


def write_markdown_trend_note(
    *,
    output_dir: Path,
    **kwargs: Unpack[_TrendNoteWriteKwargs],
) -> Path:
    normalized_kwargs = _validated_trend_note_write_kwargs(
        function_name="write_markdown_trend_note",
        kwargs=kwargs,
    )
    output_dir = output_dir.expanduser().resolve()
    if output_dir.exists() and not output_dir.is_dir():
        raise ValueError("MARKDOWN_OUTPUT_DIR must be a directory")
    return _write_trend_note(
        write_input=_TrendNoteWriteInput(
            note_dir=output_dir / "Trends",
            trend_doc_id=normalized_kwargs["trend_doc_id"],
            granularity=normalized_kwargs["granularity"],
            period_start=normalized_kwargs["period_start"],
            period_end=normalized_kwargs["period_end"],
            run_id=normalized_kwargs["run_id"],
            output_language=normalized_kwargs["output_language"],
            pass_output_id=normalized_kwargs["pass_output_id"],
            pass_kind=normalized_kwargs["pass_kind"],
            site_exclude=bool(normalized_kwargs["site_exclude"]),
            language_code=normalized_kwargs["language_code"],
            emit_presentation_sidecar=True,
            content=_render_trend_note_content(**normalized_kwargs),
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
