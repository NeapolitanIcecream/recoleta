from __future__ import annotations

from datetime import datetime
from typing import Any, cast

from sqlalchemy import desc
from sqlmodel import Session, select

from recoleta.models import PassOutput
from recoleta.storage_common import _to_json
from recoleta.types import sha256_hex


class PassOutputStoreMixin:
    engine: Any

    def _commit(self, session: Session) -> None: ...

    def create_pass_output(
        self,
        *,
        run_id: str,
        pass_kind: str,
        status: str,
        granularity: str | None = None,
        period_start: datetime | None = None,
        period_end: datetime | None = None,
        schema_version: int = 1,
        payload: dict[str, Any] | list[Any] | None = None,
        diagnostics: dict[str, Any] | list[Any] | None = None,
        input_refs: list[dict[str, Any]] | None = None,
        content_hash: str | None = None,
    ) -> PassOutput:
        normalized_run_id = str(run_id or "").strip()
        if not normalized_run_id:
            raise ValueError("run_id must not be empty")
        normalized_pass_kind = str(pass_kind or "").strip()
        if not normalized_pass_kind:
            raise ValueError("pass_kind must not be empty")
        normalized_status = str(status or "").strip()
        if not normalized_status:
            raise ValueError("status must not be empty")
        normalized_granularity = (
            str(granularity or "").strip().lower() or None
            if granularity is not None
            else None
        )
        payload_obj = payload if payload is not None else {}
        diagnostics_obj = diagnostics if diagnostics is not None else {}
        input_refs_obj = list(input_refs or [])
        payload_json = _to_json(payload_obj)
        diagnostics_json = _to_json(diagnostics_obj)
        input_refs_json = _to_json(input_refs_obj)
        normalized_content_hash = (
            str(content_hash or "").strip() or sha256_hex(payload_json)
        )

        with Session(self.engine) as session:
            row = PassOutput(
                run_id=normalized_run_id,
                pass_kind=normalized_pass_kind,
                status=normalized_status,
                granularity=normalized_granularity,
                period_start=period_start,
                period_end=period_end,
                schema_version=max(1, int(schema_version)),
                content_hash=normalized_content_hash,
                payload_json=payload_json,
                diagnostics_json=diagnostics_json,
                input_refs_json=input_refs_json,
            )
            session.add(row)
            self._commit(session)
            session.refresh(row)
            return row

    def get_pass_output(self, *, pass_output_id: int) -> PassOutput | None:
        normalized_id = int(pass_output_id)
        if normalized_id <= 0:
            return None
        with Session(self.engine) as session:
            return session.get(PassOutput, normalized_id)

    def get_latest_pass_output(
        self,
        *,
        pass_kind: str,
        status: str | None = None,
        granularity: str | None = None,
        period_start: datetime | None = None,
        period_end: datetime | None = None,
    ) -> PassOutput | None:
        normalized_pass_kind = str(pass_kind or "").strip()
        if not normalized_pass_kind:
            raise ValueError("pass_kind must not be empty")
        normalized_status = str(status or "").strip() if status is not None else ""
        normalized_granularity = (
            str(granularity or "").strip().lower() if granularity is not None else ""
        )
        with Session(self.engine) as session:
            statement = select(PassOutput).where(
                PassOutput.pass_kind == normalized_pass_kind
            )
            if normalized_status:
                statement = statement.where(PassOutput.status == normalized_status)
            if normalized_granularity:
                statement = statement.where(
                    PassOutput.granularity == normalized_granularity
                )
            if period_start is not None:
                statement = statement.where(PassOutput.period_start == period_start)
            if period_end is not None:
                statement = statement.where(PassOutput.period_end == period_end)
            statement = statement.order_by(
                desc(cast(Any, PassOutput.created_at)),
                desc(cast(Any, PassOutput.id)),
            ).limit(1)
            return session.exec(statement).first()

    def list_pass_outputs_for_run(self, *, run_id: str) -> list[PassOutput]:
        normalized_run_id = str(run_id or "").strip()
        if not normalized_run_id:
            return []
        with Session(self.engine) as session:
            statement = (
                select(PassOutput)
                .where(PassOutput.run_id == normalized_run_id)
                .order_by(
                    desc(cast(Any, PassOutput.created_at)),
                    desc(cast(Any, PassOutput.id)),
                )
            )
            return list(session.exec(statement))
