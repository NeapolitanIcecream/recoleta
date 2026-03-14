from __future__ import annotations

from typing import Any

from pydantic import BaseModel, field_validator


class ProjectionProvenance(BaseModel):
    pass_output_id: int
    pass_kind: str
    upstream_pass_output_id: int | None = None
    upstream_pass_kind: str | None = None

    @field_validator("pass_output_id", "upstream_pass_output_id")
    @classmethod
    def _validate_optional_positive_int(cls, value: int | None) -> int | None:
        if value is None:
            return None
        normalized = int(value)
        if normalized <= 0:
            raise ValueError("projection provenance ids must be > 0")
        return normalized

    @field_validator("pass_kind", "upstream_pass_kind")
    @classmethod
    def _validate_optional_kind(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = str(value or "").strip()
        if not normalized:
            raise ValueError("projection provenance kinds must not be empty")
        return normalized


def build_projection_provenance(
    *,
    pass_output_id: int,
    pass_kind: str,
    upstream_pass_output_id: int | None = None,
    upstream_pass_kind: str | None = None,
) -> ProjectionProvenance:
    return ProjectionProvenance(
        pass_output_id=pass_output_id,
        pass_kind=pass_kind,
        upstream_pass_output_id=upstream_pass_output_id,
        upstream_pass_kind=upstream_pass_kind,
    )


def inject_projection_provenance(
    *,
    payload: dict[str, Any],
    provenance: ProjectionProvenance | None,
    key: str = "_projection",
) -> dict[str, Any]:
    normalized_payload = dict(payload or {})
    if provenance is None:
        return normalized_payload
    normalized_payload[str(key or "_projection")] = provenance.model_dump(
        mode="json",
        exclude_none=True,
    )
    return normalized_payload


def projection_provenance_from_mapping(
    value: Any,
    *,
    key: str = "_projection",
) -> ProjectionProvenance | None:
    if not isinstance(value, dict):
        return None
    raw = value.get(str(key or "_projection"))
    if not isinstance(raw, dict):
        return None
    try:
        return ProjectionProvenance.model_validate(raw)
    except Exception:
        return None


__all__ = [
    "ProjectionProvenance",
    "build_projection_provenance",
    "inject_projection_provenance",
    "projection_provenance_from_mapping",
]
