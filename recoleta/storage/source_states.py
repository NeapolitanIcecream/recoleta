from __future__ import annotations

from dataclasses import dataclass
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
        return _normalize_published_at(value)

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
        request: UpsertSourcePullStateRequest | None = None,
        **legacy_kwargs: Any,
    ) -> None:
        normalized_request = _coerce_source_pull_state_request(
            request=request,
            legacy_kwargs=legacy_kwargs,
        )
        normalized_source, normalized_scope_kind, normalized_scope_key = (
            _normalized_source_pull_state_request(normalized_request)
        )
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
                normalized_request.update.watermark_published_at
            )
            now = utc_now()

            if existing is None:
                session.add(
                    _new_source_pull_state(
                        request=normalized_request,
                        normalized_identity=(
                            normalized_source,
                            normalized_scope_kind,
                            normalized_scope_key,
                        ),
                        normalized_watermark=normalized_watermark,
                        now=now,
                    )
                )
                self._commit(session)
                return

            _apply_source_pull_state_update(
                existing=existing,
                update=normalized_request.update,
                normalized_watermark=normalized_watermark,
                now=now,
            )
            session.add(existing)
            self._commit(session)


@dataclass(frozen=True, slots=True)
class UpsertSourcePullStateRequest:
    source: str
    update: SourcePullStateUpdate

    @staticmethod
    def _normalize_published_at(value: datetime | None) -> datetime | None:
        return _normalize_published_at(value)


def _normalize_published_at(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    return (
        value.replace(tzinfo=timezone.utc)
        if value.tzinfo is None
        else value.astimezone(timezone.utc)
    )


def _normalized_source_pull_state_request(
    request: UpsertSourcePullStateRequest,
) -> tuple[str, str, str]:
    normalized_source = str(request.source or "").strip().lower()
    normalized_scope_kind = str(request.update.scope_kind or "").strip().lower()
    normalized_scope_key = str(request.update.scope_key or "").strip()
    return normalized_source, normalized_scope_kind, normalized_scope_key


def _coerce_source_pull_state_request(
    *,
    request: UpsertSourcePullStateRequest | None,
    legacy_kwargs: dict[str, Any],
) -> UpsertSourcePullStateRequest:
    if request is not None:
        return request
    return UpsertSourcePullStateRequest(
        source=legacy_kwargs["source"],
        update=legacy_kwargs["update"],
    )


def _normalized_state_text(value: str | None) -> str | None:
    return str(value or "").strip() or None


def _merged_cursor_json(
    *,
    existing: SourcePullState,
    update: SourcePullStateUpdate,
) -> str:
    if not update.cursor:
        return str(existing.cursor_json or "{}")
    current_cursor = _from_json_object(existing.cursor_json)
    current_cursor.update(update.cursor)
    return _to_json(current_cursor)


def _new_source_pull_state(
    *,
    request: UpsertSourcePullStateRequest,
    normalized_identity: tuple[str, str, str],
    normalized_watermark: datetime | None,
    now: datetime,
) -> SourcePullState:
    normalized_source, normalized_scope_kind, normalized_scope_key = normalized_identity
    return SourcePullState(
        source=normalized_source,
        scope_kind=normalized_scope_kind,
        scope_key=normalized_scope_key,
        etag=_normalized_state_text(request.update.etag),
        last_modified=_normalized_state_text(request.update.last_modified),
        watermark_published_at=normalized_watermark,
        cursor_json=_to_json(request.update.cursor or {}),
        created_at=now,
        updated_at=now,
    )


def _apply_source_pull_state_update(
    *,
    existing: SourcePullState,
    update: SourcePullStateUpdate,
    normalized_watermark: datetime | None,
    now: datetime,
) -> None:
    if update.etag is not None:
        existing.etag = _normalized_state_text(update.etag)
    if update.last_modified is not None:
        existing.last_modified = _normalized_state_text(update.last_modified)
    if normalized_watermark is not None:
        current_watermark = _normalize_published_at(existing.watermark_published_at)
        if current_watermark is None or normalized_watermark > current_watermark:
            existing.watermark_published_at = normalized_watermark
    existing.cursor_json = _merged_cursor_json(existing=existing, update=update)
    existing.updated_at = now
