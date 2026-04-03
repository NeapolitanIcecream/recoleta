from __future__ import annotations

from datetime import UTC, datetime
from types import SimpleNamespace
from typing import Any, cast

from recoleta.rag.search_models import SummarySearchRequest


def test_summary_search_request_coerce_preserves_explicit_zero_limits() -> None:
    """Regression: explicit zero search limits must not be rewritten to defaults."""

    request = SummarySearchRequest.coerce(
        repository=cast(Any, SimpleNamespace()),
        vector_store=cast(Any, SimpleNamespace()),
        run_id="run-search-zero",
        doc_type="trend",
        granularity="day",
        period_start=datetime(2026, 3, 2, tzinfo=UTC),
        period_end=datetime(2026, 3, 3, tzinfo=UTC),
        query="agents",
        embedding_model="test/embed",
        embedding_dimensions=None,
        max_batch_inputs=8,
        max_batch_chars=4000,
        limit=0,
        corpus_limit=0,
    )

    assert request.limit == 0
    assert request.corpus_limit == 0
