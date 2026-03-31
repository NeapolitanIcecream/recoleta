from __future__ import annotations

from datetime import datetime
from typing import Any

from recoleta.passes.base import PassOutputEnvelope, PassStatus
from recoleta.trends import TrendPayload

TREND_SYNTHESIS_PASS_KIND = "trend_synthesis"
TREND_SYNTHESIS_SCHEMA_VERSION = 1


def build_trend_synthesis_pass_output(
    *,
    run_id: str,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
    payload: TrendPayload,
    diagnostics: dict[str, Any] | None = None,
) -> PassOutputEnvelope:
    normalized_diagnostics = diagnostics if isinstance(diagnostics, dict) else {}
    return PassOutputEnvelope(
        pass_kind=TREND_SYNTHESIS_PASS_KIND,
        schema_version=TREND_SYNTHESIS_SCHEMA_VERSION,
        status=PassStatus.SUCCEEDED,
        granularity=str(granularity or "").strip().lower() or None,
        period_start=period_start.isoformat(),
        period_end=period_end.isoformat(),
        run_id=str(run_id),
        input_refs=[],
        payload=payload.model_dump(mode="json"),
        diagnostics=normalized_diagnostics,
    )
