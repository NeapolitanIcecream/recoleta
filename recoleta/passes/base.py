from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field, field_validator

class PassStatus(StrEnum):
    SUCCEEDED = "succeeded"
    SUPPRESSED = "suppressed"
    FAILED = "failed"


class PassInputRef(BaseModel):
    ref_kind: str
    pass_kind: str | None = None
    granularity: str | None = None
    period_start: str | None = None
    period_end: str | None = None
    pass_output_id: int | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("ref_kind")
    @classmethod
    def _validate_ref_kind(cls, value: str) -> str:
        normalized = str(value or "").strip()
        if not normalized:
            raise ValueError("ref_kind must not be empty")
        return normalized


class PassOutputEnvelope(BaseModel):
    pass_kind: str
    schema_version: int = 1
    status: PassStatus
    granularity: str | None = None
    period_start: str | None = None
    period_end: str | None = None
    run_id: str
    input_refs: list[PassInputRef] = Field(default_factory=list)
    payload: dict[str, Any] = Field(default_factory=dict)
    diagnostics: dict[str, Any] = Field(default_factory=dict)

    @field_validator("pass_kind", "run_id")
    @classmethod
    def _validate_required_text(cls, value: str) -> str:
        normalized = str(value or "").strip()
        if not normalized:
            raise ValueError("required text field must not be empty")
        return normalized
