from __future__ import annotations

from typing import Any

from recoleta.rag.search_models import (
    SemanticSearchHit,
    SummarySearchRequest,
    SummaryVectorSyncRequest,
)
from recoleta.rag.search_runtime import (
    ensure_summary_vectors_for_period as _ensure_summary_vectors_for_period,
)
from recoleta.rag.search_runtime import (
    semantic_search_summaries_in_period as _semantic_search_summaries_in_period,
)


def ensure_summary_vectors_for_period(
    *,
    request: SummaryVectorSyncRequest | None = None,
    **legacy_kwargs: Any,
) -> dict[str, Any]:
    return _ensure_summary_vectors_for_period(
        SummaryVectorSyncRequest.coerce(request, **legacy_kwargs)
    )


def semantic_search_summaries_in_period(
    *,
    request: SummarySearchRequest | None = None,
    **legacy_kwargs: Any,
) -> list[SemanticSearchHit]:
    return _semantic_search_summaries_in_period(
        SummarySearchRequest.coerce(request, **legacy_kwargs)
    )


__all__ = [
    "SemanticSearchHit",
    "SummarySearchRequest",
    "SummaryVectorSyncRequest",
    "ensure_summary_vectors_for_period",
    "semantic_search_summaries_in_period",
]
