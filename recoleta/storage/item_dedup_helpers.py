from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable, cast

from sqlalchemy import desc
from sqlmodel import Session, select

from recoleta.models import (
    Item,
    ITEM_STATE_FAILED,
    ITEM_STATE_INGESTED,
    ITEM_STATE_RETRYABLE_FAILED,
)
from recoleta.storage_common import _from_json_object, _to_json
from recoleta.types import ItemDraft


@dataclass(frozen=True, slots=True)
class TitleDedupMatch:
    item: Item
    score: float


def normalize_published_at(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    return (
        value.replace(tzinfo=timezone.utc)
        if value.tzinfo is None
        else value.astimezone(timezone.utc)
    )


def merge_published_at(
    *, existing: datetime | None, incoming: datetime | None
) -> datetime | None:
    normalized_existing = normalize_published_at(existing)
    normalized_incoming = normalize_published_at(incoming)
    if normalized_existing is None:
        return normalized_incoming
    if normalized_incoming is None:
        return normalized_existing
    return (
        normalized_incoming
        if normalized_incoming < normalized_existing
        else normalized_existing
    )


def merge_raw_metadata_values(existing: Any, incoming: Any) -> Any:
    if incoming is None:
        return existing
    if isinstance(existing, dict) and isinstance(incoming, dict):
        merged = dict(existing)
        for key, value in incoming.items():
            merged[key] = merge_raw_metadata_values(merged.get(key), value)
        return merged
    if isinstance(existing, list) and isinstance(incoming, list):
        merged = list(existing)
        for value in incoming:
            if value not in merged:
                merged.append(value)
        return merged
    return incoming


def merge_raw_metadata(
    *, existing: dict[str, Any], incoming: dict[str, Any]
) -> dict[str, Any]:
    merged = dict(existing)
    for key, value in incoming.items():
        merged[key] = merge_raw_metadata_values(merged.get(key), value)
    return merged


def find_existing_item(session: Session, *, draft: ItemDraft) -> Item | None:
    if draft.source_item_id:
        statement = select(Item).where(
            Item.source == draft.source,
            Item.source_item_id == draft.source_item_id,
        )
        existing = session.exec(statement).first()
        if existing is not None:
            return existing

    by_url_hash = select(Item).where(
        Item.canonical_url_hash == draft.canonical_url_hash
    )
    return session.exec(by_url_hash).first()


def _title_match_candidates(
    session: Session,
    *,
    title_dedup_max_candidates: int,
) -> list[Item]:
    statement = (
        select(Item)
        .order_by(desc(cast(Any, Item.created_at)))
        .limit(title_dedup_max_candidates)
    )
    return list(session.exec(statement))


def _exact_title_match_candidate(
    candidates: list[Item],
    *,
    normalized_title: str,
) -> Item | None:
    for candidate in candidates:
        candidate_title = str(getattr(candidate, "title", "") or "").strip()
        if candidate_title == normalized_title:
            return candidate
    return None


def _best_fuzzy_title_match(
    candidates: list[Item],
    *,
    normalized_title: str,
    title_dedup_threshold: float,
    score_title_similarity: Callable[[str, str], float],
) -> TitleDedupMatch | None:
    best_match: TitleDedupMatch | None = None
    for candidate in candidates:
        score = float(score_title_similarity(normalized_title, candidate.title))
        if best_match is None or score > best_match.score:
            best_match = TitleDedupMatch(item=candidate, score=score)
        if score >= 100.0:
            return TitleDedupMatch(item=candidate, score=score)
    if best_match is None or best_match.score < title_dedup_threshold:
        return None
    return best_match


def find_near_duplicate_by_title(
    session: Session,
    *,
    title: str,
    title_dedup_threshold: float,
    title_dedup_max_candidates: int,
    score_title_similarity: Callable[[str, str], float],
) -> TitleDedupMatch | None:
    normalized_title = title.strip()
    if not normalized_title or title_dedup_max_candidates <= 0:
        return None

    candidates = _title_match_candidates(
        session,
        title_dedup_max_candidates=title_dedup_max_candidates,
    )
    exact_candidate = _exact_title_match_candidate(
        candidates,
        normalized_title=normalized_title,
    )
    if exact_candidate is not None:
        if 100.0 < title_dedup_threshold:
            return None
        return TitleDedupMatch(item=exact_candidate, score=100.0)
    return _best_fuzzy_title_match(
        candidates,
        normalized_title=normalized_title,
        title_dedup_threshold=title_dedup_threshold,
        score_title_similarity=score_title_similarity,
    )


def create_item_from_draft(draft: ItemDraft) -> Item:
    return Item(
        source=draft.source,
        source_item_id=draft.source_item_id,
        canonical_url=draft.canonical_url,
        canonical_url_hash=draft.canonical_url_hash,
        title=draft.title,
        authors=_to_json(draft.authors),
        published_at=draft.published_at,
        raw_metadata_json=_to_json(draft.raw_metadata),
        state=ITEM_STATE_INGESTED,
    )


def _merged_alternate_urls(
    *,
    existing_url: str,
    draft_url: str,
    alternate_urls: Any,
) -> list[str]:
    normalized_urls = alternate_urls if isinstance(alternate_urls, list) else []
    if draft_url == existing_url or draft_url in normalized_urls:
        return normalized_urls
    return [*normalized_urls, draft_url]


def _merged_dedup_events(
    *,
    dedup_events: Any,
    draft: ItemDraft,
    title_dedup_score: float | None,
) -> list[dict[str, Any]]:
    normalized_events = dedup_events if isinstance(dedup_events, list) else []
    normalized_events.append(
        {
            "source": draft.source,
            "source_item_id": draft.source_item_id,
            "canonical_url_hash": draft.canonical_url_hash,
            "title_similarity": round(float(title_dedup_score or 0.0), 2),
        }
    )
    return normalized_events[-20:]


def apply_title_dedup_merge(
    *,
    existing: Item,
    draft: ItemDraft,
    title_dedup_score: float | None,
    merge_published_at_fn: Callable[..., datetime | None],
) -> None:
    current_metadata = _from_json_object(existing.raw_metadata_json)
    current_metadata["alternate_urls"] = _merged_alternate_urls(
        existing_url=existing.canonical_url,
        draft_url=draft.canonical_url,
        alternate_urls=current_metadata.get("alternate_urls"),
    )
    current_metadata["dedup_events"] = _merged_dedup_events(
        dedup_events=current_metadata.get("dedup_events"),
        draft=draft,
        title_dedup_score=title_dedup_score,
    )
    existing.raw_metadata_json = _to_json(current_metadata)
    existing.published_at = merge_published_at_fn(
        existing=existing.published_at,
        incoming=draft.published_at,
    )


def apply_direct_item_merge(
    *,
    existing: Item,
    draft: ItemDraft,
    merge_published_at_fn: Callable[..., datetime | None],
    merge_raw_metadata_fn: Callable[..., dict[str, Any]],
) -> None:
    existing.canonical_url = draft.canonical_url
    existing.canonical_url_hash = draft.canonical_url_hash
    existing.title = draft.title
    existing.authors = _to_json(draft.authors)
    existing.published_at = merge_published_at_fn(
        existing=existing.published_at,
        incoming=draft.published_at,
    )
    existing_metadata = _from_json_object(existing.raw_metadata_json)
    existing.raw_metadata_json = _to_json(
        merge_raw_metadata_fn(
            existing=existing_metadata,
            incoming=draft.raw_metadata,
        )
    )


def reset_state_after_upsert(previous_state: str) -> str:
    if previous_state in {ITEM_STATE_FAILED, ITEM_STATE_RETRYABLE_FAILED}:
        return ITEM_STATE_INGESTED
    return previous_state


def maybe_fill_source_item_id(
    *,
    existing: Item,
    draft: ItemDraft,
    matched_by_title: bool,
) -> None:
    if matched_by_title:
        return
    if existing.source != draft.source:
        return
    if existing.source_item_id is not None or draft.source_item_id is None:
        return
    existing.source_item_id = draft.source_item_id
