from __future__ import annotations

from datetime import UTC, datetime
from inspect import signature


def test_huldra_public_arxiv_models_expose_recoleta_contract() -> None:
    from huldra.models import (
        ArxivRequest,
        ArxivResult,
        HuldraMaintenanceRequestResult,
    )

    assert "maturity_lag_days" in ArxivRequest.model_fields
    assert "cache_readable" in ArxivResult.model_fields
    assert "mature" in ArxivResult.model_fields
    assert "serving_mode" in ArxivResult.model_fields
    assert "raw_cache_status" in HuldraMaintenanceRequestResult.model_fields
    assert "serving_status" in HuldraMaintenanceRequestResult.model_fields

    result = ArxivResult.model_validate(
        {
            "serving_mode": "analysis_ready",
            "status": "ready",
            "cache_key": "huldra:v1:demo",
            "cache_readable": True,
            "mature": True,
            "analysis_ready": True,
            "ready": True,
            "papers": [],
            "extra_future_field": "ignored-by-recoleta",
        }
    )

    assert result.cache_readable is True
    assert result.mature is True
    assert result.serving_mode == "analysis_ready"


def test_huldra_client_exposes_sync_and_backfill_methods() -> None:
    from huldra.client import HuldraClient
    from huldra.models import ArxivRequest, CachePolicy, ReadinessMode

    assert hasattr(HuldraClient, "sync_windows")
    assert hasattr(HuldraClient, "backfill_windows")
    assert "wait_timeout_seconds" in signature(HuldraClient.sync_windows).parameters
    assert "wait_timeout_seconds" in signature(HuldraClient.backfill_windows).parameters

    request = ArxivRequest(
        client_id="recoleta:contract",
        search_query="cat:cs.AI",
        submitted_start=datetime(2026, 5, 20, tzinfo=UTC),
        submitted_end=datetime(2026, 5, 21, tzinfo=UTC),
        cache_policy=CachePolicy.CACHE_ONLY,
        readiness=ReadinessMode.ANALYSIS_READY,
        maturity_lag_days=1,
    )

    assert request.maturity_lag_days == 1
    assert request.cache_policy == "cache_only"
    assert request.readiness == "analysis_ready"
