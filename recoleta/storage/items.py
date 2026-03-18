from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, cast

from rapidfuzz import fuzz
from sqlalchemy import and_, desc, func, or_
from sqlalchemy.orm import aliased
from sqlmodel import Session, select

from recoleta.models import (
    Content,
    Item,
    ItemStreamState,
    ITEM_STATE_ANALYZED,
    ITEM_STATE_ENRICHED,
    ITEM_STATE_FAILED,
    ITEM_STATE_INGESTED,
    ITEM_STATE_PUBLISHED,
    ITEM_STATE_RETRYABLE_FAILED,
    ITEM_STATE_TRIAGED,
)
from recoleta.storage_common import _from_json_object, _to_json
from recoleta.types import ItemDraft, ItemStateUpdate, sha256_hex, utc_now


class ItemStoreMixin:
    engine: Any
    title_dedup_threshold: float
    title_dedup_max_candidates: int

    def _commit(self, session: Session) -> None: ...

    @staticmethod
    def _normalize_published_at(value: datetime | None) -> datetime | None:
        if value is None:
            return None
        return (
            value.replace(tzinfo=timezone.utc)
            if value.tzinfo is None
            else value.astimezone(timezone.utc)
        )

    @classmethod
    def _merge_published_at(
        cls, *, existing: datetime | None, incoming: datetime | None
    ) -> datetime | None:
        normalized_existing = cls._normalize_published_at(existing)
        normalized_incoming = cls._normalize_published_at(incoming)
        if normalized_existing is None:
            return normalized_incoming
        if normalized_incoming is None:
            return normalized_existing
        return (
            normalized_incoming
            if normalized_incoming < normalized_existing
            else normalized_existing
        )

    @classmethod
    def _merge_raw_metadata_values(cls, existing: Any, incoming: Any) -> Any:
        if incoming is None:
            return existing
        if isinstance(existing, dict) and isinstance(incoming, dict):
            merged = dict(existing)
            for key, value in incoming.items():
                merged[key] = cls._merge_raw_metadata_values(merged.get(key), value)
            return merged
        if isinstance(existing, list) and isinstance(incoming, list):
            merged = list(existing)
            for value in incoming:
                if value not in merged:
                    merged.append(value)
            return merged
        return incoming

    @classmethod
    def _merge_raw_metadata(
        cls, *, existing: dict[str, Any], incoming: dict[str, Any]
    ) -> dict[str, Any]:
        merged = dict(existing)
        for key, value in incoming.items():
            merged[key] = cls._merge_raw_metadata_values(merged.get(key), value)
        return merged

    def count_items(self) -> int:
        with Session(self.engine) as session:
            statement = select(func.count(cast(Any, Item.id)))
            return int(session.exec(statement).one())

    def _find_near_duplicate_by_title(
        self, session: Session, *, title: str
    ) -> tuple[Item, float] | None:
        normalized_title = title.strip()
        if not normalized_title:
            return None
        if self.title_dedup_max_candidates <= 0:
            return None

        statement = (
            select(Item)
            .order_by(desc(cast(Any, Item.created_at)))
            .limit(self.title_dedup_max_candidates)
        )
        candidates = list(session.exec(statement))
        for candidate in candidates:
            candidate_title = str(getattr(candidate, "title", "") or "").strip()
            if candidate_title == normalized_title:
                if 100.0 < self.title_dedup_threshold:
                    return None
                return candidate, 100.0

        best_item: Item | None = None
        best_score = -1.0
        for candidate in candidates:
            score = float(fuzz.token_set_ratio(normalized_title, candidate.title))
            if score > best_score:
                best_score = score
                best_item = candidate
                if best_score >= 100.0:
                    return candidate, best_score
        if best_item is None:
            return None
        if best_score < self.title_dedup_threshold:
            return None
        return best_item, best_score

    def upsert_item(self, draft: ItemDraft) -> tuple[Item, bool]:
        with Session(self.engine) as session:
            existing: Item | None = None
            matched_by_title = False
            title_dedup_score: float | None = None
            if draft.source_item_id:
                statement = select(Item).where(
                    Item.source == draft.source,
                    Item.source_item_id == draft.source_item_id,
                )
                existing = session.exec(statement).first()

            if existing is None:
                by_url_hash = select(Item).where(
                    Item.canonical_url_hash == draft.canonical_url_hash
                )
                existing = session.exec(by_url_hash).first()

            if existing is None and self.title_dedup_threshold > 0:
                match = self._find_near_duplicate_by_title(session, title=draft.title)
                if match is not None:
                    existing, title_dedup_score = match
                    matched_by_title = True

            if existing is None:
                created = Item(
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
                session.add(created)
                self._commit(session)
                session.refresh(created)
                return created, True

            previous_state = existing.state
            if matched_by_title:
                current_metadata = _from_json_object(existing.raw_metadata_json)
                alternate_urls = current_metadata.get("alternate_urls")
                if not isinstance(alternate_urls, list):
                    alternate_urls = []
                if (
                    draft.canonical_url != existing.canonical_url
                    and draft.canonical_url not in alternate_urls
                ):
                    alternate_urls.append(draft.canonical_url)
                current_metadata["alternate_urls"] = alternate_urls

                dedup_events = current_metadata.get("dedup_events")
                if not isinstance(dedup_events, list):
                    dedup_events = []
                dedup_events.append(
                    {
                        "source": draft.source,
                        "source_item_id": draft.source_item_id,
                        "canonical_url_hash": draft.canonical_url_hash,
                        "title_similarity": round(float(title_dedup_score or 0.0), 2),
                    }
                )
                current_metadata["dedup_events"] = dedup_events[-20:]
                existing.raw_metadata_json = _to_json(current_metadata)
                existing.published_at = self._merge_published_at(
                    existing=existing.published_at,
                    incoming=draft.published_at,
                )
            else:
                existing.canonical_url = draft.canonical_url
                existing.canonical_url_hash = draft.canonical_url_hash
                existing.title = draft.title
                existing.authors = _to_json(draft.authors)
                existing.published_at = self._merge_published_at(
                    existing=existing.published_at,
                    incoming=draft.published_at,
                )
                existing_metadata = _from_json_object(existing.raw_metadata_json)
                existing.raw_metadata_json = _to_json(
                    self._merge_raw_metadata(
                        existing=existing_metadata,
                        incoming=draft.raw_metadata,
                    )
                )
            if previous_state in {ITEM_STATE_FAILED, ITEM_STATE_RETRYABLE_FAILED}:
                existing.state = ITEM_STATE_INGESTED
            existing.updated_at = utc_now()
            if (
                (not matched_by_title)
                and existing.source == draft.source
                and existing.source_item_id is None
                and draft.source_item_id is not None
            ):
                existing.source_item_id = draft.source_item_id
            session.add(existing)
            self._commit(session)
            session.refresh(existing)
            return existing, False

    def list_items_for_analysis(
        self,
        *,
        limit: int,
        period_start: datetime | None = None,
        period_end: datetime | None = None,
    ) -> list[Item]:
        with Session(self.engine) as session:
            event_at = func.coalesce(
                cast(Any, Item.published_at), cast(Any, Item.created_at)
            )
            statement = select(Item).where(
                cast(Any, Item.state).in_(
                    [
                        ITEM_STATE_INGESTED,
                        ITEM_STATE_ENRICHED,
                        ITEM_STATE_RETRYABLE_FAILED,
                    ]
                )
            )
            if period_start is not None and period_end is not None:
                statement = statement.where(
                    event_at >= period_start, event_at < period_end
                )
                statement = statement.order_by(
                    desc(cast(Any, event_at)),
                    desc(cast(Any, Item.updated_at)),
                    desc(cast(Any, Item.created_at)),
                )
            else:
                statement = statement.order_by(
                    desc(cast(Any, Item.updated_at)),
                    desc(cast(Any, Item.created_at)),
                )
            statement = statement.limit(limit)
            return list(session.exec(statement))

    def get_latest_content(self, *, item_id: int, content_type: str) -> Content | None:
        with Session(self.engine) as session:
            statement = (
                select(Content)
                .where(Content.item_id == item_id, Content.content_type == content_type)
                .order_by(desc(cast(Any, Content.id)))
            )
            return session.exec(statement).first()

    def get_latest_content_texts(
        self, *, item_id: int, content_types: list[str]
    ) -> dict[str, str | None]:
        normalized_item_id = int(item_id)
        types = [str(t or "").strip() for t in (content_types or [])]
        types = [t for t in types if t]
        if normalized_item_id <= 0 or not types:
            return {}

        wanted = set(types)
        out: dict[str, str | None] = {t: None for t in types}
        with Session(self.engine) as session:
            statement = (
                select(Content)
                .where(
                    Content.item_id == normalized_item_id,
                    cast(Any, Content.content_type).in_(types),
                )
                .order_by(desc(cast(Any, Content.id)))
            )
            for content in session.exec(statement):
                ctype = str(getattr(content, "content_type", "") or "").strip()
                if ctype in wanted and out.get(ctype) is None:
                    text = getattr(content, "text", None)
                    out[ctype] = (
                        text if isinstance(text, str) and text.strip() else None
                    )
                    wanted.discard(ctype)
                    if not wanted:
                        break
        return out

    def get_latest_content_texts_for_items(
        self, *, item_ids: list[int], content_types: list[str]
    ) -> dict[int, dict[str, str | None]]:
        normalized_ids: list[int] = []
        seen_ids: set[int] = set()
        for raw_item_id in item_ids:
            try:
                item_id = int(raw_item_id)
            except Exception:
                continue
            if item_id <= 0 or item_id in seen_ids:
                continue
            seen_ids.add(item_id)
            normalized_ids.append(item_id)

        normalized_types: list[str] = []
        seen_types: set[str] = set()
        for raw_type in content_types:
            content_type = str(raw_type or "").strip()
            if not content_type or content_type in seen_types:
                continue
            seen_types.add(content_type)
            normalized_types.append(content_type)

        if not normalized_ids or not normalized_types:
            return {}

        out: dict[int, dict[str, str | None]] = {
            item_id: {content_type: None for content_type in normalized_types}
            for item_id in normalized_ids
        }
        with Session(self.engine) as session:
            latest_ids = (
                select(
                    cast(Any, Content.item_id).label("item_id"),
                    cast(Any, Content.content_type).label("content_type"),
                    func.max(cast(Any, Content.id)).label("max_id"),
                )
                .where(
                    cast(Any, Content.item_id).in_(normalized_ids),
                    cast(Any, Content.content_type).in_(normalized_types),
                )
                .group_by(
                    cast(Any, Content.item_id),
                    cast(Any, Content.content_type),
                )
                .subquery()
            )
            statement = select(Content).join(
                latest_ids, cast(Any, Content.id) == latest_ids.c.max_id
            )
            for content in session.exec(statement):
                item_id = int(getattr(content, "item_id"))
                content_type = str(getattr(content, "content_type", "") or "").strip()
                text = getattr(content, "text", None)
                out[item_id][content_type] = (
                    text if isinstance(text, str) and text.strip() else None
                )
        return out

    def get_latest_contents(
        self, *, item_ids: list[int], content_type: str
    ) -> dict[int, Content]:
        normalized_ids: list[int] = []
        seen: set[int] = set()
        for raw_item_id in item_ids:
            try:
                item_id = int(raw_item_id)
            except Exception:
                continue
            if item_id <= 0 or item_id in seen:
                continue
            seen.add(item_id)
            normalized_ids.append(item_id)
        normalized_type = str(content_type or "").strip()
        if not normalized_ids or not normalized_type:
            return {}

        with Session(self.engine) as session:
            latest_ids = (
                select(
                    cast(Any, Content.item_id),
                    func.max(cast(Any, Content.id)).label("max_id"),
                )
                .where(
                    cast(Any, Content.item_id).in_(normalized_ids),
                    Content.content_type == normalized_type,
                )
                .group_by(cast(Any, Content.item_id))
                .subquery()
            )
            statement = select(Content).join(
                latest_ids, cast(Any, Content.id) == latest_ids.c.max_id
            )
            contents = list(session.exec(statement))
            return {content.item_id: content for content in contents}

    def upsert_contents_texts(
        self, *, item_id: int, texts_by_type: dict[str, str]
    ) -> int:
        normalized_item_id = int(item_id)
        if normalized_item_id <= 0:
            raise ValueError("item_id must be > 0")
        if not isinstance(texts_by_type, dict) or not texts_by_type:
            return 0

        normalized: dict[str, str] = {}
        for raw_type, raw_text in texts_by_type.items():
            content_type = str(raw_type or "").strip()
            if not content_type:
                continue
            if not isinstance(raw_text, str):
                continue
            text_value = raw_text.strip()
            if not text_value:
                continue
            normalized[content_type] = text_value
        if not normalized:
            return 0

        hashes_by_type: dict[str, str] = {
            ctype: sha256_hex(text_value) for ctype, text_value in normalized.items()
        }
        target_types = list(hashes_by_type.keys())
        target_hashes = list(set(hashes_by_type.values()))

        inserted = 0
        with Session(self.engine) as session:
            existing_pairs: set[tuple[str, str]] = set()
            statement = select(Content.content_type, Content.content_hash).where(
                Content.item_id == normalized_item_id,
                cast(Any, Content.content_type).in_(target_types),
                cast(Any, Content.content_hash).in_(target_hashes),
            )
            for ctype, chash in session.exec(statement):
                existing_pairs.add((str(ctype), str(chash)))

            for ctype, text_value in normalized.items():
                chash = hashes_by_type[ctype]
                if (ctype, chash) in existing_pairs:
                    continue
                session.add(
                    Content(
                        item_id=normalized_item_id,
                        content_type=ctype,
                        text=text_value,
                        artifact_path=None,
                        content_hash=chash,
                    )
                )
                inserted += 1

            if inserted > 0:
                self._commit(session)
        return inserted

    def upsert_content(
        self,
        *,
        item_id: int,
        content_type: str,
        text: str | None,
        artifact_path: str | None = None,
    ) -> Content:
        if text is None and artifact_path is None:
            raise ValueError("Either text or artifact_path must be provided")
        normalized_text = text.strip() if isinstance(text, str) else None
        if normalized_text == "":
            raise ValueError("text must not be empty")

        if normalized_text is not None:
            content_hash = sha256_hex(normalized_text)
        else:
            resolved = Path(str(artifact_path)).expanduser().resolve()
            content_hash = hashlib.sha256(resolved.read_bytes()).hexdigest()

        with Session(self.engine) as session:
            existing = session.exec(
                select(Content).where(
                    Content.item_id == item_id,
                    Content.content_type == content_type,
                    Content.content_hash == content_hash,
                )
            ).first()
            if existing is not None:
                return existing

            content = Content(
                item_id=item_id,
                content_type=content_type,
                text=normalized_text,
                artifact_path=artifact_path,
                content_hash=content_hash,
            )
            session.add(content)
            self._commit(session)
            session.refresh(content)
            return content

    def upsert_content_with_inserted(
        self,
        *,
        item_id: int,
        content_type: str,
        text: str | None,
        artifact_path: str | None = None,
    ) -> tuple[Content, bool]:
        if text is None and artifact_path is None:
            raise ValueError("Either text or artifact_path must be provided")
        normalized_text = text.strip() if isinstance(text, str) else None
        if normalized_text == "":
            raise ValueError("text must not be empty")

        if normalized_text is not None:
            content_hash = sha256_hex(normalized_text)
        else:
            resolved = Path(str(artifact_path)).expanduser().resolve()
            content_hash = hashlib.sha256(resolved.read_bytes()).hexdigest()

        with Session(self.engine) as session:
            existing = session.exec(
                select(Content).where(
                    Content.item_id == item_id,
                    Content.content_type == content_type,
                    Content.content_hash == content_hash,
                )
            ).first()
            if existing is not None:
                return existing, False

            content = Content(
                item_id=item_id,
                content_type=content_type,
                text=normalized_text,
                artifact_path=artifact_path,
                content_hash=content_hash,
            )
            session.add(content)
            self._commit(session)
            session.refresh(content)
            return content, True

    def _upsert_item_stream_state(
        self,
        *,
        session: Session,
        item_id: int,
        stream: str,
        state: str,
        existing_states: dict[tuple[int, str], ItemStreamState] | None = None,
    ) -> ItemStreamState:
        key = (int(item_id), str(stream))
        existing = existing_states.get(key) if existing_states is not None else None
        if existing is None:
            existing = session.exec(
                select(ItemStreamState).where(
                    ItemStreamState.item_id == item_id,
                    ItemStreamState.stream == stream,
                )
            ).first()
        now = utc_now()
        if existing is None:
            existing = ItemStreamState(
                item_id=item_id,
                stream=stream,
                state=state,
                created_at=now,
                updated_at=now,
            )
        else:
            existing.state = state
            existing.updated_at = now
        session.add(existing)
        if existing_states is not None:
            existing_states[key] = existing
        return existing

    def list_items_for_stream_analysis(
        self,
        *,
        stream: str,
        limit: int,
        selected_only: bool = False,
        period_start: datetime | None = None,
        period_end: datetime | None = None,
    ) -> list[Item]:
        stream_state = aliased(ItemStreamState)
        with Session(self.engine) as session:
            event_at = func.coalesce(
                cast(Any, Item.published_at), cast(Any, Item.created_at)
            )
            statement = (
                select(Item)
                .outerjoin(
                    stream_state,
                    and_(
                        cast(Any, stream_state.item_id) == cast(Any, Item.id),
                        cast(Any, stream_state.stream) == stream,
                    ),
                )
                .where(
                    cast(Any, Item.state).in_(
                        [
                            ITEM_STATE_ENRICHED,
                            ITEM_STATE_TRIAGED,
                            ITEM_STATE_ANALYZED,
                            ITEM_STATE_PUBLISHED,
                            ITEM_STATE_RETRYABLE_FAILED,
                            ITEM_STATE_FAILED,
                        ]
                    )
                )
            )
            if period_start is not None and period_end is not None:
                statement = statement.where(
                    event_at >= period_start, event_at < period_end
                )
                statement = statement.order_by(
                    desc(cast(Any, event_at)),
                    desc(cast(Any, Item.updated_at)),
                    desc(cast(Any, Item.created_at)),
                )
            else:
                statement = statement.order_by(
                    desc(cast(Any, Item.updated_at)),
                    desc(cast(Any, Item.created_at)),
                )
            if selected_only:
                statement = statement.where(
                    cast(Any, stream_state.state).in_(
                        [ITEM_STATE_TRIAGED, ITEM_STATE_RETRYABLE_FAILED]
                    )
                )
            else:
                statement = statement.where(
                    or_(
                        cast(Any, stream_state.id).is_(None),
                        cast(Any, stream_state.state) == ITEM_STATE_RETRYABLE_FAILED,
                    )
                )
            statement = statement.limit(limit)
            return list(session.exec(statement))

    def mark_item_enriched(self, *, item_id: int) -> None:
        with Session(self.engine) as session:
            item = session.get(Item, item_id)
            if item is None:
                return
            item.state = ITEM_STATE_ENRICHED
            item.updated_at = utc_now()
            session.add(item)
            self._commit(session)

    def mark_item_triaged(self, *, item_id: int) -> None:
        with Session(self.engine) as session:
            item = session.get(Item, item_id)
            if item is None:
                return
            item.state = ITEM_STATE_TRIAGED
            item.updated_at = utc_now()
            session.add(item)
            self._commit(session)

    def mark_item_stream_state(
        self,
        *,
        item_id: int,
        stream: str,
        state: str,
        mirror_item_state: bool = False,
    ) -> None:
        with Session(self.engine) as session:
            self._upsert_item_stream_state(
                session=session,
                item_id=item_id,
                stream=stream,
                state=state,
            )
            if mirror_item_state:
                item = session.get(Item, item_id)
                if item is not None:
                    item.state = state
                    item.updated_at = utc_now()
                    session.add(item)
            self._commit(session)

    def mark_item_failed(self, *, item_id: int) -> None:
        with Session(self.engine) as session:
            item = session.get(Item, item_id)
            if item is None:
                return
            item.state = ITEM_STATE_FAILED
            item.updated_at = utc_now()
            session.add(item)
            self._commit(session)

    def mark_item_retryable_failed(self, *, item_id: int) -> None:
        with Session(self.engine) as session:
            item = session.get(Item, item_id)
            if item is None:
                return
            item.state = ITEM_STATE_RETRYABLE_FAILED
            item.updated_at = utc_now()
            session.add(item)
            self._commit(session)

    def update_item_states_batch(self, *, updates: list[ItemStateUpdate]) -> int:
        normalized: list[ItemStateUpdate] = []
        seen: dict[tuple[int, str | None], int] = {}
        for update in updates:
            try:
                item_id = int(update.item_id)
            except Exception:
                continue
            if item_id <= 0:
                continue
            state = str(update.state or "").strip()
            if not state:
                continue
            stream = str(update.stream).strip() if update.stream is not None else None
            key = (item_id, stream)
            normalized_update = ItemStateUpdate(
                item_id=item_id,
                state=state,
                stream=stream,
                mirror_item_state=bool(update.mirror_item_state),
            )
            existing_index = seen.get(key)
            if existing_index is None:
                seen[key] = len(normalized)
                normalized.append(normalized_update)
            else:
                normalized[existing_index] = normalized_update
        if not normalized:
            return 0

        item_ids = sorted({update.item_id for update in normalized})
        stream_names = sorted(
            {
                cast(str, update.stream)
                for update in normalized
                if isinstance(update.stream, str) and update.stream
            }
        )
        with Session(self.engine) as session:
            items_by_id = {
                int(item.id): item
                for item in session.exec(
                    select(Item).where(cast(Any, Item.id).in_(item_ids))
                )
                if item.id is not None
            }
            existing_states: dict[tuple[int, str], ItemStreamState] = {}
            if stream_names:
                statement = select(ItemStreamState).where(
                    cast(Any, ItemStreamState.item_id).in_(item_ids),
                    cast(Any, ItemStreamState.stream).in_(stream_names),
                )
                for stream_state in session.exec(statement):
                    existing_states[(stream_state.item_id, stream_state.stream)] = (
                        stream_state
                    )

            applied = 0
            for update in normalized:
                if update.stream is not None:
                    self._upsert_item_stream_state(
                        session=session,
                        item_id=update.item_id,
                        stream=update.stream,
                        state=update.state,
                        existing_states=existing_states,
                    )
                    if update.mirror_item_state:
                        item = items_by_id.get(update.item_id)
                        if item is not None:
                            item.state = update.state
                            item.updated_at = utc_now()
                            session.add(item)
                    applied += 1
                    continue

                item = items_by_id.get(update.item_id)
                if item is None:
                    continue
                item.state = update.state
                item.updated_at = utc_now()
                session.add(item)
                applied += 1

            if applied > 0:
                self._commit(session)
            return applied
