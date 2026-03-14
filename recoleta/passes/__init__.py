from __future__ import annotations

from recoleta.passes.base import PassInputRef, PassOutputEnvelope, PassStatus
from recoleta.passes.trend_synthesis import (
    TREND_SYNTHESIS_PASS_KIND,
    TREND_SYNTHESIS_SCHEMA_VERSION,
    build_trend_synthesis_pass_output,
)

__all__ = [
    "PassInputRef",
    "PassOutputEnvelope",
    "PassStatus",
    "TREND_SYNTHESIS_PASS_KIND",
    "TREND_SYNTHESIS_SCHEMA_VERSION",
    "build_trend_synthesis_pass_output",
]
