from __future__ import annotations

from dataclasses import dataclass
from typing import Any, cast

from sqlalchemy import func
from sqlmodel import Session, select

from recoleta.models import Content


@dataclass(frozen=True, slots=True)
class LatestContentTextsRequest:
    item_ids: list[int]
    content_types: list[str]


def _normalized_positive_int(value: Any) -> int | None:
    try:
        normalized = int(value)
    except Exception:
        return None
    return normalized if normalized > 0 else None


def normalize_item_ids(item_ids: list[int]) -> list[int]:
    normalized_ids: list[int] = []
    seen_ids: set[int] = set()
    for raw_item_id in item_ids:
        item_id = _normalized_positive_int(raw_item_id)
        if item_id is None or item_id in seen_ids:
            continue
        seen_ids.add(item_id)
        normalized_ids.append(item_id)
    return normalized_ids


def normalize_content_types(content_types: list[str]) -> list[str]:
    normalized_types: list[str] = []
    seen_types: set[str] = set()
    for raw_type in content_types:
        content_type = str(raw_type or "").strip()
        if not content_type or content_type in seen_types:
            continue
        seen_types.add(content_type)
        normalized_types.append(content_type)
    return normalized_types


def coerce_latest_content_texts_request(
    *,
    item_ids: list[int],
    content_types: list[str],
) -> LatestContentTextsRequest | None:
    normalized_ids = normalize_item_ids(item_ids)
    normalized_types = normalize_content_types(content_types)
    if not normalized_ids or not normalized_types:
        return None
    return LatestContentTextsRequest(
        item_ids=normalized_ids,
        content_types=normalized_types,
    )


def empty_latest_content_texts(
    request: LatestContentTextsRequest,
) -> dict[int, dict[str, str | None]]:
    return {
        item_id: {content_type: None for content_type in request.content_types}
        for item_id in request.item_ids
    }


def _latest_content_ids_subquery(request: LatestContentTextsRequest) -> Any:
    return (
        select(
            cast(Any, Content.item_id).label("item_id"),
            cast(Any, Content.content_type).label("content_type"),
            func.max(cast(Any, Content.id)).label("max_id"),
        )
        .where(
            cast(Any, Content.item_id).in_(request.item_ids),
            cast(Any, Content.content_type).in_(request.content_types),
        )
        .group_by(
            cast(Any, Content.item_id),
            cast(Any, Content.content_type),
        )
        .subquery()
    )


def _normalized_content_text(content: Content) -> str | None:
    text = getattr(content, "text", None)
    return text if isinstance(text, str) and text.strip() else None


def load_latest_content_texts_by_item(
    *,
    session: Session,
    request: LatestContentTextsRequest,
) -> dict[int, dict[str, str | None]]:
    out = empty_latest_content_texts(request)
    latest_ids = _latest_content_ids_subquery(request)
    statement = select(Content).join(
        latest_ids,
        cast(Any, Content.id) == latest_ids.c.max_id,
    )
    for content in session.exec(statement):
        item_id = int(getattr(content, "item_id"))
        content_type = str(getattr(content, "content_type", "") or "").strip()
        out[item_id][content_type] = _normalized_content_text(content)
    return out


def load_latest_content_texts(
    *,
    session: Session,
    item_id: int,
    content_types: list[str],
) -> dict[str, str | None]:
    request = coerce_latest_content_texts_request(
        item_ids=[item_id],
        content_types=content_types,
    )
    if request is None:
        return {}
    results = load_latest_content_texts_by_item(session=session, request=request)
    return results.get(request.item_ids[0], {})
