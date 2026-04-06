from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import os
from pathlib import Path
from typing import Any

import yaml
from slugify import slugify

from recoleta.publish.item_note_writer import (
    ItemNoteSpec,
    render_item_note_lines,
    write_item_note,
)

__all__ = [
    "resolve_item_note_path",
    "resolve_item_note_href",
    "write_markdown_note",
    "write_obsidian_note",
]


@dataclass(frozen=True, slots=True)
class _ItemNoteHrefRequest:
    note_dir: Path
    from_dir: Path
    item_id: int
    title: str
    canonical_url: str
    published_at: datetime | None


def _read_yaml_frontmatter(path: Path) -> dict[str, Any] | None:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception:
        return None

    if not lines or lines[0].strip() != "---":
        return None

    end_idx: int | None = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_idx = idx
            break
    if end_idx is None:
        return None

    raw = "\n".join(lines[1:end_idx]).strip()
    if not raw:
        return None

    try:
        loaded = yaml.safe_load(raw)
    except Exception:
        return None
    return loaded if isinstance(loaded, dict) else None


def _item_note_path(
    *,
    note_dir: Path,
    item_id: int,
    title: str,
    canonical_url: str,
    published_at: datetime | None,
) -> Path:
    date_prefix = (published_at or datetime.now(timezone.utc)).strftime("%Y-%m-%d")
    slug = slugify(title, lowercase=True) or "untitled-item"
    note_path = note_dir / f"{date_prefix}--{slug}.md"
    if note_path.exists():
        frontmatter = _read_yaml_frontmatter(note_path) or {}
        existing_url = str(frontmatter.get("url") or "").strip()
        if existing_url != canonical_url.strip():
            note_path = note_dir / f"{date_prefix}--{slug}--{item_id}.md"
    return note_path


def resolve_item_note_path(
    *,
    note_dir: Path,
    item_id: int,
    title: str,
    canonical_url: str,
    published_at: datetime | None,
) -> Path:
    return _item_note_path(
        note_dir=note_dir,
        item_id=item_id,
        title=title,
        canonical_url=canonical_url,
        published_at=published_at,
    )


def _coerce_item_note_href_request(
    *,
    request: _ItemNoteHrefRequest | None = None,
    legacy_kwargs: dict[str, Any] | None = None,
) -> _ItemNoteHrefRequest:
    if request is not None:
        return request
    values = dict(legacy_kwargs or {})
    return _ItemNoteHrefRequest(
        note_dir=values["note_dir"],
        from_dir=values["from_dir"],
        item_id=int(values["item_id"]),
        title=str(values["title"]),
        canonical_url=str(values["canonical_url"]),
        published_at=values.get("published_at"),
    )


def resolve_item_note_href(
    *,
    request: _ItemNoteHrefRequest | None = None,
    **legacy_kwargs: Any,
) -> str:
    normalized_request = _coerce_item_note_href_request(
        request=request,
        legacy_kwargs=legacy_kwargs,
    )
    note_path = resolve_item_note_path(
        note_dir=normalized_request.note_dir,
        item_id=normalized_request.item_id,
        title=normalized_request.title,
        canonical_url=normalized_request.canonical_url,
        published_at=normalized_request.published_at,
    )
    relative = Path(os.path.relpath(note_path, start=normalized_request.from_dir))
    return relative.as_posix()


def _coerce_item_note_spec(
    *, spec: ItemNoteSpec | None = None, legacy_kwargs: dict[str, Any] | None = None
) -> ItemNoteSpec:
    if spec is not None:
        return spec
    values = dict(legacy_kwargs or {})
    return ItemNoteSpec(
        item_id=int(values.pop("item_id")),
        title=str(values.pop("title")),
        source=str(values.pop("source")),
        canonical_url=str(values.pop("canonical_url")),
        published_at=values.pop("published_at"),
        authors=list(values.pop("authors")),
        topics=list(values.pop("topics")),
        relevance_score=float(values.pop("relevance_score")),
        run_id=str(values.pop("run_id")),
        summary=str(values.pop("summary")),
        language_code=values.pop("language_code", None),
    )


def _render_item_note_lines(
    *, spec: ItemNoteSpec | None = None, **legacy_kwargs: Any
) -> list[str]:
    return render_item_note_lines(
        spec=_coerce_item_note_spec(spec=spec, legacy_kwargs=legacy_kwargs)
    )


def _write_item_note(
    *,
    note_dir: Path,
    spec: ItemNoteSpec | None = None,
    **legacy_kwargs: Any,
) -> Path:
    normalized_spec = _coerce_item_note_spec(spec=spec, legacy_kwargs=legacy_kwargs)
    return write_item_note(
        note_dir=note_dir,
        spec=normalized_spec,
        resolve_note_path=_item_note_path,
        lines=_render_item_note_lines(spec=normalized_spec),
    )


def write_obsidian_note(
    *,
    vault_path: Path,
    base_folder: str,
    spec: ItemNoteSpec | None = None,
    **legacy_kwargs: Any,
) -> Path:
    note_dir = vault_path / base_folder / "Inbox"
    return _write_item_note(
        note_dir=note_dir,
        spec=spec,
        **legacy_kwargs,
    )


def write_markdown_note(
    *,
    output_dir: Path,
    spec: ItemNoteSpec | None = None,
    **legacy_kwargs: Any,
) -> Path:
    output_dir = output_dir.expanduser().resolve()
    if output_dir.exists() and not output_dir.is_dir():
        raise ValueError("MARKDOWN_OUTPUT_DIR must be a directory")

    note_dir = output_dir / "Inbox"
    return _write_item_note(
        note_dir=note_dir,
        spec=spec,
        **legacy_kwargs,
    )
