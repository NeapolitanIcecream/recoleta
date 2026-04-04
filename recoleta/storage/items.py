from __future__ import annotations

import hashlib
from datetime import datetime
from pathlib import Path
from typing import Any, cast

from rapidfuzz import fuzz
from sqlalchemy import desc, func
from sqlmodel import Session, select

from recoleta.models import (
    Content,
    Item,
    ITEM_STATE_ENRICHED,
    ITEM_STATE_FAILED,
    ITEM_STATE_INGESTED,
    ITEM_STATE_RETRYABLE_FAILED,
    ITEM_STATE_TRIAGED,
)
from recoleta.storage import item_content_queries, item_content_writes, item_dedup_helpers
from recoleta.types import ItemDraft, ItemStateUpdate, sha256_hex, utc_now


class ItemStoreMixin:
    engine: Any
    title_dedup_threshold: float
    title_dedup_max_candidates: int

    def _commit(self, session: Session) -> None: ...

    @staticmethod
    def _normalize_published_at(value: datetime | None) -> datetime | None:
        return item_dedup_helpers.normalize_published_at(value)

    @classmethod
    def _merge_published_at(
        cls, *, existing: datetime | None, incoming: datetime | None
    ) -> datetime | None:
        return item_dedup_helpers.merge_published_at(
            existing=existing,
            incoming=incoming,
        )

    @classmethod
    def _merge_raw_metadata(
        cls, *, existing: dict[str, Any], incoming: dict[str, Any]
    ) -> dict[str, Any]:
        return item_dedup_helpers.merge_raw_metadata(
            existing=existing,
            incoming=incoming,
        )

    def count_items(self) -> int:
        with Session(self.engine) as session:
            statement = select(func.count(cast(Any, Item.id)))
            return int(session.exec(statement).one())

    def _find_near_duplicate_by_title(
        self, session: Session, *, title: str
    ) -> tuple[Item, float] | None:
        match = item_dedup_helpers.find_near_duplicate_by_title(
            session,
            title=title,
            title_dedup_threshold=self.title_dedup_threshold,
            title_dedup_max_candidates=self.title_dedup_max_candidates,
            score_title_similarity=fuzz.token_set_ratio,
        )
        if match is None:
            return None
        return match.item, match.score

    def upsert_item(self, draft: ItemDraft) -> tuple[Item, bool]:
        with Session(self.engine) as session:
            existing = item_dedup_helpers.find_existing_item(session, draft=draft)
            matched_by_title = False
            title_dedup_score: float | None = None
            if existing is None and self.title_dedup_threshold > 0:
                match = self._find_near_duplicate_by_title(session, title=draft.title)
                if match is not None:
                    existing, title_dedup_score = match
                    matched_by_title = True

            if existing is None:
                created = item_dedup_helpers.create_item_from_draft(draft)
                session.add(created)
                self._commit(session)
                session.refresh(created)
                return created, True

            previous_state = existing.state
            if matched_by_title:
                item_dedup_helpers.apply_title_dedup_merge(
                    existing=existing,
                    draft=draft,
                    title_dedup_score=title_dedup_score,
                    merge_published_at_fn=self._merge_published_at,
                )
            else:
                item_dedup_helpers.apply_direct_item_merge(
                    existing=existing,
                    draft=draft,
                    merge_published_at_fn=self._merge_published_at,
                    merge_raw_metadata_fn=self._merge_raw_metadata,
                )
            existing.state = item_dedup_helpers.reset_state_after_upsert(previous_state)
            existing.updated_at = utc_now()
            item_dedup_helpers.maybe_fill_source_item_id(
                existing=existing,
                draft=draft,
                matched_by_title=matched_by_title,
            )
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
        with Session(self.engine) as session:
            return item_content_queries.load_latest_content_texts(
                session=session,
                item_id=item_id,
                content_types=content_types,
            )

    def get_latest_content_texts_for_items(
        self, *, item_ids: list[int], content_types: list[str]
    ) -> dict[int, dict[str, str | None]]:
        request = item_content_queries.coerce_latest_content_texts_request(
            item_ids=item_ids,
            content_types=content_types,
        )
        if request is None:
            return {}
        with Session(self.engine) as session:
            return item_content_queries.load_latest_content_texts_by_item(
                session=session,
                request=request,
            )

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
        spec = item_content_writes.normalize_content_text_upsert(
            item_id=item_id,
            texts_by_type=texts_by_type,
        )
        if spec is None:
            return 0

        with Session(self.engine) as session:
            existing_pairs = item_content_writes.load_existing_content_pairs(
                session=session,
                spec=spec,
            )
            rows = item_content_writes.build_new_content_rows(
                spec=spec,
                existing_pairs=existing_pairs,
            )
            for row in rows:
                session.add(row)
            inserted = len(rows)
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
        seen: dict[int, int] = {}
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
            normalized_update = ItemStateUpdate(
                item_id=item_id,
                state=state,
                mirror_item_state=bool(update.mirror_item_state),
            )
            existing_index = seen.get(item_id)
            if existing_index is None:
                seen[item_id] = len(normalized)
                normalized.append(normalized_update)
            else:
                normalized[existing_index] = normalized_update
        if not normalized:
            return 0

        item_ids = sorted({update.item_id for update in normalized})
        with Session(self.engine) as session:
            items_by_id = {
                int(item.id): item
                for item in session.exec(
                    select(Item).where(cast(Any, Item.id).in_(item_ids))
                )
                if item.id is not None
            }
            applied = 0
            for update in normalized:
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
