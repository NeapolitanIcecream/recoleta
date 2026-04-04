from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from recoleta.passes.base import PassOutputEnvelope, PassStatus
from recoleta.trends import TrendPayload

TREND_SYNTHESIS_PASS_KIND = "trend_synthesis"
TREND_SYNTHESIS_SCHEMA_VERSION = 1


@dataclass(frozen=True, slots=True)
class _TrendSynthesisPassOutputRequest:
    run_id: str
    granularity: str
    period_start: datetime
    period_end: datetime
    payload: TrendPayload
    diagnostics: dict[str, Any] | None = None


def _coerce_trend_synthesis_pass_output_request(
    *,
    request: _TrendSynthesisPassOutputRequest | None = None,
    legacy_kwargs: dict[str, Any] | None = None,
) -> _TrendSynthesisPassOutputRequest:
    if request is not None:
        return request
    values = dict(legacy_kwargs or {})
    return _TrendSynthesisPassOutputRequest(
        run_id=str(values["run_id"]),
        granularity=str(values["granularity"]),
        period_start=values["period_start"],
        period_end=values["period_end"],
        payload=values["payload"],
        diagnostics=values.get("diagnostics"),
    )


def build_trend_synthesis_pass_output(
    *,
    request: _TrendSynthesisPassOutputRequest | None = None,
    **legacy_kwargs: Any,
) -> PassOutputEnvelope:
    normalized_request = _coerce_trend_synthesis_pass_output_request(
        request=request,
        legacy_kwargs=legacy_kwargs,
    )
    normalized_diagnostics = (
        normalized_request.diagnostics
        if isinstance(normalized_request.diagnostics, dict)
        else {}
    )
    return PassOutputEnvelope(
        pass_kind=TREND_SYNTHESIS_PASS_KIND,
        schema_version=TREND_SYNTHESIS_SCHEMA_VERSION,
        status=PassStatus.SUCCEEDED,
        granularity=str(normalized_request.granularity or "").strip().lower() or None,
        period_start=normalized_request.period_start.isoformat(),
        period_end=normalized_request.period_end.isoformat(),
        run_id=str(normalized_request.run_id),
        input_refs=[],
        payload=normalized_request.payload.model_dump(mode="json"),
        diagnostics=normalized_diagnostics,
    )
