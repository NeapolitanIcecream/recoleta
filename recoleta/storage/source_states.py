from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sqlmodel import Session, select

from recoleta.models import SourcePullState
from recoleta.sources import SourcePullStateSnapshot, SourcePullStateUpdate
from recoleta.storage_common import _from_json_object, _to_json
from recoleta.types import utc_now


class SourcePullStateStoreMixin:
    engine: Any

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

    def get_source_pull_state(
        self,
        *,
        source: str,
        scope_kind: str,
        scope_key: str,
    ) -> SourcePullStateSnapshot | None:
        with Session(self.engine) as session:
            statement = select(SourcePullState).where(
                SourcePullState.source == source,
                SourcePullState.scope_kind == scope_kind,
                SourcePullState.scope_key == scope_key,
            )
            state = session.exec(statement).first()
            if state is None:
                return None
            return SourcePullStateSnapshot(
                scope_kind=state.scope_kind,
                scope_key=state.scope_key,
                etag=state.etag,
                last_modified=state.last_modified,
                watermark_published_at=self._normalize_published_at(
                    state.watermark_published_at
                ),
                cursor=_from_json_object(state.cursor_json),
            )

    def upsert_source_pull_state(
        self,
        *,
        source: str,
        update: SourcePullStateUpdate,
    ) -> None:
        normalized_source = str(source or "").strip().lower()
        normalized_scope_kind = str(update.scope_kind or "").strip().lower()
        normalized_scope_key = str(update.scope_key or "").strip()
        if (
            not normalized_source
            or not normalized_scope_kind
            or not normalized_scope_key
        ):
            return

        with Session(self.engine) as session:
            statement = select(SourcePullState).where(
                SourcePullState.source == normalized_source,
                SourcePullState.scope_kind == normalized_scope_kind,
                SourcePullState.scope_key == normalized_scope_key,
            )
            existing = session.exec(statement).first()
            normalized_watermark = self._normalize_published_at(
                update.watermark_published_at
            )
            now = utc_now()

            if existing is None:
                session.add(
                    SourcePullState(
                        source=normalized_source,
                        scope_kind=normalized_scope_kind,
                        scope_key=normalized_scope_key,
                        etag=str(update.etag or "").strip() or None,
                        last_modified=str(update.last_modified or "").strip() or None,
                        watermark_published_at=normalized_watermark,
                        cursor_json=_to_json(update.cursor or {}),
                        created_at=now,
                        updated_at=now,
                    )
                )
                self._commit(session)
                return

            if update.etag is not None:
                existing.etag = str(update.etag or "").strip() or None
            if update.last_modified is not None:
                existing.last_modified = str(update.last_modified or "").strip() or None
            if normalized_watermark is not None:
                current_watermark = self._normalize_published_at(
                    existing.watermark_published_at
                )
                if (
                    current_watermark is None
                    or normalized_watermark > current_watermark
                ):
                    existing.watermark_published_at = normalized_watermark
            if update.cursor:
                current_cursor = _from_json_object(existing.cursor_json)
                current_cursor.update(update.cursor)
                existing.cursor_json = _to_json(current_cursor)
            existing.updated_at = now
            session.add(existing)
            self._commit(session)
