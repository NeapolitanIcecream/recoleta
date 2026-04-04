from __future__ import annotations

from dataclasses import dataclass
from typing import Any, cast

from sqlmodel import Session, select

from recoleta.models import Content
from recoleta.types import sha256_hex


@dataclass(frozen=True, slots=True)
class ContentTextUpsertSpec:
    item_id: int
    texts_by_type: dict[str, str]
    hashes_by_type: dict[str, str]


def normalize_content_text_upsert(
    *,
    item_id: int,
    texts_by_type: dict[str, str],
) -> ContentTextUpsertSpec | None:
    normalized_item_id = int(item_id)
    if normalized_item_id <= 0:
        raise ValueError("item_id must be > 0")
    if not isinstance(texts_by_type, dict) or not texts_by_type:
        return None

    normalized: dict[str, str] = {}
    for raw_type, raw_text in texts_by_type.items():
        content_type = str(raw_type or "").strip()
        if not content_type or not isinstance(raw_text, str):
            continue
        text_value = raw_text.strip()
        if not text_value:
            continue
        normalized[content_type] = text_value
    if not normalized:
        return None

    hashes_by_type = {
        content_type: sha256_hex(text_value)
        for content_type, text_value in normalized.items()
    }
    return ContentTextUpsertSpec(
        item_id=normalized_item_id,
        texts_by_type=normalized,
        hashes_by_type=hashes_by_type,
    )


def load_existing_content_pairs(
    *,
    session: Session,
    spec: ContentTextUpsertSpec,
) -> set[tuple[str, str]]:
    statement = select(Content.content_type, Content.content_hash).where(
        Content.item_id == spec.item_id,
        cast(Any, Content.content_type).in_(spec.texts_by_type.keys()),
        cast(Any, Content.content_hash).in_(set(spec.hashes_by_type.values())),
    )
    return {
        (str(content_type), str(content_hash))
        for content_type, content_hash in session.exec(statement)
    }


def build_new_content_rows(
    *,
    spec: ContentTextUpsertSpec,
    existing_pairs: set[tuple[str, str]],
) -> list[Content]:
    rows: list[Content] = []
    for content_type, text_value in spec.texts_by_type.items():
        content_hash = spec.hashes_by_type[content_type]
        if (content_type, content_hash) in existing_pairs:
            continue
        rows.append(
            Content(
                item_id=spec.item_id,
                content_type=content_type,
                text=text_value,
                artifact_path=None,
                content_hash=content_hash,
            )
        )
    return rows
