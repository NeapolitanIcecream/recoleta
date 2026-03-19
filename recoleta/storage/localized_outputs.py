from __future__ import annotations

from typing import Any, cast

from sqlalchemy import desc
from sqlmodel import Session, select

from recoleta.models import LocalizedOutput
from recoleta.storage_common import _to_json
from recoleta.types import DEFAULT_TOPIC_STREAM, utc_now


class LocalizedOutputStoreMixin:
    engine: Any

    def _commit(self, session: Session) -> None: ...

    def upsert_localized_output(
        self,
        *,
        source_kind: str,
        source_record_id: int,
        scope: str = DEFAULT_TOPIC_STREAM,
        language_code: str,
        status: str,
        source_hash: str,
        payload: dict[str, Any] | list[Any] | None = None,
        diagnostics: dict[str, Any] | list[Any] | None = None,
        variant_role: str = "translation",
        schema_version: int = 1,
    ) -> tuple[LocalizedOutput, bool]:
        normalized_source_kind = str(source_kind or "").strip().lower()
        if not normalized_source_kind:
            raise ValueError("source_kind must not be empty")
        normalized_source_record_id = int(source_record_id)
        if normalized_source_record_id <= 0:
            raise ValueError("source_record_id must be > 0")
        normalized_scope = str(scope or "").strip() or DEFAULT_TOPIC_STREAM
        normalized_language_code = str(language_code or "").strip()
        if not normalized_language_code:
            raise ValueError("language_code must not be empty")
        normalized_status = str(status or "").strip()
        if not normalized_status:
            raise ValueError("status must not be empty")
        normalized_source_hash = str(source_hash or "").strip()
        if not normalized_source_hash:
            raise ValueError("source_hash must not be empty")
        normalized_variant_role = str(variant_role or "").strip().lower()
        if not normalized_variant_role:
            raise ValueError("variant_role must not be empty")

        payload_json = _to_json(payload if payload is not None else {})
        diagnostics_json = _to_json(diagnostics if diagnostics is not None else {})

        with Session(self.engine) as session:
            existing = session.exec(
                select(LocalizedOutput).where(
                    LocalizedOutput.source_kind == normalized_source_kind,
                    LocalizedOutput.source_record_id == normalized_source_record_id,
                    LocalizedOutput.scope == normalized_scope,
                    LocalizedOutput.language_code == normalized_language_code,
                )
            ).first()
            if existing is None:
                row = LocalizedOutput(
                    source_kind=normalized_source_kind,
                    source_record_id=normalized_source_record_id,
                    scope=normalized_scope,
                    language_code=normalized_language_code,
                    status=normalized_status,
                    schema_version=max(1, int(schema_version)),
                    source_hash=normalized_source_hash,
                    variant_role=normalized_variant_role,
                    payload_json=payload_json,
                    diagnostics_json=diagnostics_json,
                )
                session.add(row)
                self._commit(session)
                session.refresh(row)
                return row, True

            existing.status = normalized_status
            existing.schema_version = max(1, int(schema_version))
            existing.source_hash = normalized_source_hash
            existing.variant_role = normalized_variant_role
            existing.payload_json = payload_json
            existing.diagnostics_json = diagnostics_json
            existing.updated_at = utc_now()
            session.add(existing)
            self._commit(session)
            session.refresh(existing)
            return existing, False

    def get_localized_output(
        self,
        *,
        source_kind: str,
        source_record_id: int,
        scope: str = DEFAULT_TOPIC_STREAM,
        language_code: str,
    ) -> LocalizedOutput | None:
        normalized_source_kind = str(source_kind or "").strip().lower()
        normalized_source_record_id = int(source_record_id)
        if not normalized_source_kind or normalized_source_record_id <= 0:
            return None
        normalized_scope = str(scope or "").strip() or DEFAULT_TOPIC_STREAM
        normalized_language_code = str(language_code or "").strip()
        if not normalized_language_code:
            return None
        with Session(self.engine) as session:
            return session.exec(
                select(LocalizedOutput).where(
                    LocalizedOutput.source_kind == normalized_source_kind,
                    LocalizedOutput.source_record_id == normalized_source_record_id,
                    LocalizedOutput.scope == normalized_scope,
                    LocalizedOutput.language_code == normalized_language_code,
                )
            ).first()

    def list_localized_outputs(
        self,
        *,
        scope: str = DEFAULT_TOPIC_STREAM,
        language_code: str | None = None,
        source_kind: str | None = None,
    ) -> list[LocalizedOutput]:
        normalized_scope = str(scope or "").strip() or DEFAULT_TOPIC_STREAM
        normalized_language_code = str(language_code or "").strip()
        normalized_source_kind = str(source_kind or "").strip().lower()
        with Session(self.engine) as session:
            statement = select(LocalizedOutput).where(
                LocalizedOutput.scope == normalized_scope
            )
            if normalized_language_code:
                statement = statement.where(
                    LocalizedOutput.language_code == normalized_language_code
                )
            if normalized_source_kind:
                statement = statement.where(
                    LocalizedOutput.source_kind == normalized_source_kind
                )
            statement = statement.order_by(
                cast(Any, LocalizedOutput.source_kind),
                cast(Any, LocalizedOutput.source_record_id),
                desc(cast(Any, LocalizedOutput.updated_at)),
                desc(cast(Any, LocalizedOutput.id)),
            )
            return list(session.exec(statement))
