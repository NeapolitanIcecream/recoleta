from __future__ import annotations

from dataclasses import dataclass
from typing import Any, cast

from sqlalchemy import desc
from sqlmodel import Session, select

from recoleta.models import LocalizedOutput
from recoleta.storage_common import _to_json
from recoleta.types import utc_now


class LocalizedOutputStoreMixin:
    engine: Any

    def _commit(self, session: Session) -> None: ...

    def upsert_localized_output(
        self,
        *,
        request: LocalizedOutputUpsertRequest | None = None,
        **legacy_kwargs: Any,
    ) -> tuple[LocalizedOutput, bool]:
        normalized_request = _normalized_localized_output(
            coerce_localized_output_request(
                request=request,
                legacy_kwargs=legacy_kwargs,
            )
        )
        payload_json = _to_json(
            normalized_request.payload if normalized_request.payload is not None else {}
        )
        diagnostics_json = _to_json(
            normalized_request.diagnostics
            if normalized_request.diagnostics is not None
            else {}
        )

        with Session(self.engine) as session:
            existing = session.exec(
                select(LocalizedOutput).where(
                    LocalizedOutput.source_kind == normalized_request.source_kind,
                    LocalizedOutput.source_record_id
                    == normalized_request.source_record_id,
                    LocalizedOutput.language_code == normalized_request.language_code,
                )
            ).first()
            if existing is None:
                row = LocalizedOutput(
                    source_kind=normalized_request.source_kind,
                    source_record_id=normalized_request.source_record_id,
                    language_code=normalized_request.language_code,
                    status=normalized_request.status,
                    schema_version=normalized_request.schema_version,
                    source_hash=normalized_request.source_hash,
                    variant_role=normalized_request.variant_role,
                    payload_json=payload_json,
                    diagnostics_json=diagnostics_json,
                )
                session.add(row)
                self._commit(session)
                session.refresh(row)
                return row, True

            existing.status = normalized_request.status
            existing.schema_version = normalized_request.schema_version
            existing.source_hash = normalized_request.source_hash
            existing.variant_role = normalized_request.variant_role
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
        language_code: str,
    ) -> LocalizedOutput | None:
        normalized_source_kind = str(source_kind or "").strip().lower()
        normalized_source_record_id = int(source_record_id)
        if not normalized_source_kind or normalized_source_record_id <= 0:
            return None
        normalized_language_code = str(language_code or "").strip()
        if not normalized_language_code:
            return None
        with Session(self.engine) as session:
            return session.exec(
                select(LocalizedOutput).where(
                    LocalizedOutput.source_kind == normalized_source_kind,
                    LocalizedOutput.source_record_id == normalized_source_record_id,
                    LocalizedOutput.language_code == normalized_language_code,
                )
            ).first()

    def list_localized_outputs(
        self,
        *,
        language_code: str | None = None,
        source_kind: str | None = None,
    ) -> list[LocalizedOutput]:
        normalized_language_code = str(language_code or "").strip()
        normalized_source_kind = str(source_kind or "").strip().lower()
        with Session(self.engine) as session:
            statement = select(LocalizedOutput)
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


@dataclass(frozen=True, slots=True)
class LocalizedOutputUpsertRequest:
    source_kind: str
    source_record_id: int
    language_code: str
    status: str
    source_hash: str
    payload: dict[str, Any] | list[Any] | None = None
    diagnostics: dict[str, Any] | list[Any] | None = None
    variant_role: str = "translation"
    schema_version: int = 1


def coerce_localized_output_request(
    *,
    request: LocalizedOutputUpsertRequest | None = None,
    legacy_kwargs: dict[str, Any],
) -> LocalizedOutputUpsertRequest:
    if request is not None:
        return request
    return LocalizedOutputUpsertRequest(
        source_kind=legacy_kwargs["source_kind"],
        source_record_id=int(legacy_kwargs["source_record_id"]),
        language_code=legacy_kwargs["language_code"],
        status=legacy_kwargs["status"],
        source_hash=legacy_kwargs["source_hash"],
        payload=legacy_kwargs.get("payload"),
        diagnostics=legacy_kwargs.get("diagnostics"),
        variant_role=str(legacy_kwargs.get("variant_role", "translation")),
        schema_version=int(legacy_kwargs.get("schema_version", 1)),
    )


def _normalized_localized_output(
    request: LocalizedOutputUpsertRequest,
) -> LocalizedOutputUpsertRequest:
    normalized_source_kind = str(request.source_kind or "").strip().lower()
    if not normalized_source_kind:
        raise ValueError("source_kind must not be empty")
    if int(request.source_record_id) <= 0:
        raise ValueError("source_record_id must be > 0")
    normalized_language_code = str(request.language_code or "").strip()
    if not normalized_language_code:
        raise ValueError("language_code must not be empty")
    normalized_status = str(request.status or "").strip()
    if not normalized_status:
        raise ValueError("status must not be empty")
    normalized_source_hash = str(request.source_hash or "").strip()
    if not normalized_source_hash:
        raise ValueError("source_hash must not be empty")
    normalized_variant_role = str(request.variant_role or "").strip().lower()
    if not normalized_variant_role:
        raise ValueError("variant_role must not be empty")
    return LocalizedOutputUpsertRequest(
        source_kind=normalized_source_kind,
        source_record_id=int(request.source_record_id),
        language_code=normalized_language_code,
        status=normalized_status,
        source_hash=normalized_source_hash,
        payload=request.payload,
        diagnostics=request.diagnostics,
        variant_role=normalized_variant_role,
        schema_version=max(1, int(request.schema_version)),
    )
