from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from typing import TYPE_CHECKING, Any, TypedDict, Unpack

import yaml

from recoleta.presentation import (
    build_idea_presentation_v2,
    idea_display_labels,
    presentation_sidecar_path,
    resolve_presentation_language_code,
    write_presentation_sidecar,
)
from recoleta.publish.idea_evidence import (
    enrich_evidence_ref as _enrich_evidence_ref,
    format_evidence_ref as _format_evidence_ref,
)
from recoleta.publish.trend_render_shared import _trend_date_token
from recoleta.provenance import build_projection_provenance

if TYPE_CHECKING:
    from recoleta.passes.trend_ideas import TrendIdeasPayload

__all__ = [
    "resolve_ideas_note_path",
    "write_markdown_ideas_note",
    "write_obsidian_ideas_note",
]


@dataclass(frozen=True, slots=True)
class _IdeasNoteWriteInput:
    repository: Any
    root_dir: Path
    note_dir: Path
    pass_output_id: int | None
    upstream_pass_output_id: int | None
    granularity: str
    period_start: datetime
    period_end: datetime
    run_id: str
    status: str
    payload: TrendIdeasPayload
    topics: list[str] | None
    pass_kind: str
    upstream_pass_kind: str | None
    output_language: str | None
    language_code: str | None
    emit_presentation_sidecar: bool


class _IdeasNoteWriteKwargs(TypedDict, total=False):
    pass_output_id: int | None
    upstream_pass_output_id: int | None
    granularity: str
    period_start: datetime
    period_end: datetime
    run_id: str
    status: str
    payload: TrendIdeasPayload
    topics: list[str] | None
    pass_kind: str
    upstream_pass_kind: str | None
    output_language: str | None
    language_code: str | None


_IDEAS_NOTE_REQUIRED_KEYS = (
    "pass_output_id",
    "upstream_pass_output_id",
    "granularity",
    "period_start",
    "period_end",
    "run_id",
    "status",
    "payload",
)
_IDEAS_NOTE_DEFAULTS: dict[str, Any] = {
    "topics": None,
    "pass_kind": "trend_ideas",
    "upstream_pass_kind": "trend_synthesis",
    "output_language": None,
    "language_code": None,
}


def resolve_ideas_note_path(
    *,
    note_dir: Path,
    granularity: str,
    period_start: datetime,
) -> Path:
    token = _trend_date_token(granularity=granularity, period_start=period_start)
    return note_dir / f"{granularity}--{token}--ideas.md"


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


def _ideas_note_tags(topics: list[str] | None) -> list[str]:
    base_tags = ["recoleta/ideas"]
    for topic in list(topics or []):
        normalized = _sanitize_obsidian_tag(topic)
        if normalized:
            base_tags.append(f"topic/{normalized}")
    seen_tags: set[str] = set()
    return [tag for tag in base_tags if not (tag in seen_tags or seen_tags.add(tag))]


def _normalized_payload_ideas(
    payload: TrendIdeasPayload, *, max_count: int = 3
) -> list[Any]:
    return list(payload.ideas or [])[:max_count]


def _render_evidence_lines(
    *,
    repository: Any,
    root_dir: Path,
    note_dir: Path,
    evidence_refs: list[Any],
) -> list[str]:
    lines: list[str] = []
    for ref in evidence_refs:
        rendered = _format_evidence_ref(
            repository=repository,
            root_dir=root_dir,
            note_dir=note_dir,
            ref=ref,
            show_chunk_index=False,
        )
        reason = " ".join(str(getattr(ref, "reason", "") or "").split()).strip()
        if reason:
            lines.append(f"- {rendered}: {reason}")
        else:
            lines.append(f"- {rendered}")
    return lines


def _presentation_ready_ideas(
    *,
    repository: Any,
    root_dir: Path,
    note_dir: Path,
    payload: TrendIdeasPayload,
) -> list[Any]:
    prepared: list[Any] = []
    for idea in _normalized_payload_ideas(payload):
        prepared.append(
            SimpleNamespace(
                title=idea.title,
                content_md=idea.content_md,
                evidence_refs=[
                    _enrich_evidence_ref(
                        repository=repository,
                        root_dir=root_dir,
                        note_dir=note_dir,
                        ref=ref,
                    )
                    for ref in list(idea.evidence_refs or [])
                ],
            )
        )
    return prepared


def _ideas_note_frontmatter(write_input: _IdeasNoteWriteInput) -> dict[str, Any]:
    frontmatter = {
        "kind": "ideas",
        "granularity": write_input.granularity,
        "period_start": write_input.period_start.isoformat(),
        "period_end": write_input.period_end.isoformat(),
        "run_id": write_input.run_id,
        "status": write_input.status,
        "topics": [
            str(topic).strip()
            for topic in list(write_input.topics or [])
            if str(topic).strip()
        ],
        "tags": _ideas_note_tags(write_input.topics),
    }
    normalized_language_code = str(write_input.language_code or "").strip()
    if normalized_language_code:
        frontmatter["language_code"] = normalized_language_code
    if write_input.pass_output_id is not None:
        frontmatter.update(
            build_projection_provenance(
                pass_output_id=write_input.pass_output_id,
                pass_kind=str(write_input.pass_kind or "").strip() or "trend_ideas",
                upstream_pass_output_id=write_input.upstream_pass_output_id,
                upstream_pass_kind=(
                    str(write_input.upstream_pass_kind or "").strip() or None
                    if write_input.upstream_pass_output_id is not None
                    else None
                ),
            ).model_dump(mode="json", exclude_none=True)
        )
    return frontmatter


def _render_ideas_note_lines(
    *,
    write_input: _IdeasNoteWriteInput,
    presentation: dict[str, Any],
    labels: dict[str, str],
) -> list[str]:
    lines: list[str] = [
        "---",
        yaml.safe_dump(_ideas_note_frontmatter(write_input), sort_keys=False).strip(),
        "---",
        "",
        f"# {str(write_input.payload.title or '').strip() or 'Ideas'}",
        "",
        f"## {labels['summary']}",
        str(presentation["content"].get("summary") or "").strip() or "(empty)",
    ]
    for idea, rendered_idea in zip(
        _normalized_payload_ideas(write_input.payload),
        list(presentation["content"].get("ideas") or []),
        strict=False,
    ):
        lines.extend(
            [
                "",
                f"## {str(rendered_idea.get('title') or '').strip() or idea.title}",
                str(rendered_idea.get("content") or "").strip() or "(empty)",
            ]
        )
        evidence_lines = _render_evidence_lines(
            repository=write_input.repository,
            root_dir=write_input.root_dir,
            note_dir=write_input.note_dir,
            evidence_refs=list(getattr(idea, "evidence_refs", []) or []),
        )
        if evidence_lines:
            lines.extend(["", f"### {labels['evidence']}", *evidence_lines])
    return lines


def _write_ideas_note(*, write_input: _IdeasNoteWriteInput) -> Path:
    write_input.note_dir.mkdir(parents=True, exist_ok=True)
    resolved_language_code = resolve_presentation_language_code(
        language_code=write_input.language_code,
        output_language=write_input.output_language,
    )
    note_path = resolve_ideas_note_path(
        note_dir=write_input.note_dir,
        granularity=write_input.granularity,
        period_start=write_input.period_start,
    )
    presentation = build_idea_presentation_v2(
        source_markdown_path=f"{write_input.note_dir.name}/{note_path.name}",
        title=str(write_input.payload.title or "").strip(),
        summary_md=str(write_input.payload.summary_md or "").strip(),
        ideas=_presentation_ready_ideas(
            repository=write_input.repository,
            root_dir=write_input.root_dir,
            note_dir=write_input.note_dir,
            payload=write_input.payload,
        ),
        language_code=resolved_language_code,
        display_language_code=resolved_language_code,
    )
    labels = idea_display_labels(language_code=resolved_language_code)
    note_path.write_text(
        "\n".join(
            _render_ideas_note_lines(
                write_input=write_input,
                presentation=presentation,
                labels=labels,
            )
        ).rstrip()
        + "\n",
        encoding="utf-8",
    )
    should_emit_sidecar = (
        write_input.emit_presentation_sidecar
        and str(write_input.status or "").strip().lower() == "succeeded"
        and bool(list(write_input.payload.ideas or []))
    )
    if should_emit_sidecar:
        try:
            write_presentation_sidecar(note_path=note_path, presentation=presentation)
        except Exception:
            note_path.unlink(missing_ok=True)
            presentation_sidecar_path(note_path=note_path).unlink(missing_ok=True)
            raise
    elif write_input.emit_presentation_sidecar:
        presentation_sidecar_path(note_path=note_path).unlink(missing_ok=True)
    return note_path


def _validated_ideas_note_write_kwargs(
    *,
    function_name: str,
    kwargs: _IdeasNoteWriteKwargs,
) -> dict[str, Any]:
    allowed_keys = set(_IDEAS_NOTE_REQUIRED_KEYS) | set(_IDEAS_NOTE_DEFAULTS)
    unexpected = [key for key in kwargs if key not in allowed_keys]
    if unexpected:
        raise TypeError(
            f"{function_name}() got an unexpected keyword argument {unexpected[0]!r}"
        )
    missing = [key for key in _IDEAS_NOTE_REQUIRED_KEYS if key not in kwargs]
    if missing:
        missing_repr = ", ".join(repr(key) for key in missing)
        plural = "s" if len(missing) != 1 else ""
        raise TypeError(
            f"{function_name}() missing required keyword-only argument{plural}: {missing_repr}"
        )
    return {**_IDEAS_NOTE_DEFAULTS, **kwargs}


def write_markdown_ideas_note(
    *,
    repository: Any,
    output_dir: Path,
    **kwargs: Unpack[_IdeasNoteWriteKwargs],
) -> Path:
    normalized_kwargs = _validated_ideas_note_write_kwargs(
        function_name="write_markdown_ideas_note",
        kwargs=kwargs,
    )
    root_dir = output_dir.expanduser().resolve()
    return _write_ideas_note(
        write_input=_IdeasNoteWriteInput(
            repository=repository,
            root_dir=root_dir,
            note_dir=root_dir / "Ideas",
            pass_output_id=normalized_kwargs["pass_output_id"],
            upstream_pass_output_id=normalized_kwargs["upstream_pass_output_id"],
            granularity=normalized_kwargs["granularity"],
            period_start=normalized_kwargs["period_start"],
            period_end=normalized_kwargs["period_end"],
            run_id=normalized_kwargs["run_id"],
            status=normalized_kwargs["status"],
            payload=normalized_kwargs["payload"],
            topics=normalized_kwargs["topics"],
            pass_kind=normalized_kwargs["pass_kind"],
            upstream_pass_kind=normalized_kwargs["upstream_pass_kind"],
            output_language=normalized_kwargs["output_language"],
            language_code=normalized_kwargs["language_code"],
            emit_presentation_sidecar=True,
        )
    )


def write_obsidian_ideas_note(
    *,
    repository: Any,
    vault_path: Path,
    base_folder: str,
    **kwargs: Unpack[_IdeasNoteWriteKwargs],
) -> Path:
    normalized_kwargs = _validated_ideas_note_write_kwargs(
        function_name="write_obsidian_ideas_note",
        kwargs=kwargs,
    )
    root_dir = vault_path / base_folder
    return _write_ideas_note(
        write_input=_IdeasNoteWriteInput(
            repository=repository,
            root_dir=root_dir,
            note_dir=root_dir / "Ideas",
            pass_output_id=normalized_kwargs["pass_output_id"],
            upstream_pass_output_id=normalized_kwargs["upstream_pass_output_id"],
            granularity=normalized_kwargs["granularity"],
            period_start=normalized_kwargs["period_start"],
            period_end=normalized_kwargs["period_end"],
            run_id=normalized_kwargs["run_id"],
            status=normalized_kwargs["status"],
            payload=normalized_kwargs["payload"],
            topics=normalized_kwargs["topics"],
            pass_kind=normalized_kwargs["pass_kind"],
            upstream_pass_kind=normalized_kwargs["upstream_pass_kind"],
            output_language=normalized_kwargs["output_language"],
            language_code=normalized_kwargs["language_code"],
            emit_presentation_sidecar=False,
        )
    )
