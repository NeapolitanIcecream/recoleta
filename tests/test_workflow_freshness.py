from __future__ import annotations

from recoleta.workflow_freshness import workflow_freshness_diagnostics_view


def test_diagnostics_view_preserves_fingerprint_contract_without_chunk_details() -> None:
    freshness = {
        "schema_version": 1,
        "kind": "trend_synthesis",
        "key": "full-fingerprint-key",
        "components": {
            "schema_version": 1,
            "kind": "trend_synthesis",
            "granularity": "day",
            "period_start": "2026-03-02T00:00:00+00:00",
            "period_end": "2026-03-03T00:00:00+00:00",
            "settings_fingerprint": "settings-key",
            "llm_model": "test/trends-model",
            "analysis_model": "test/analyze-model",
            "upstream_sources": {
                "schema_version": 1,
                "key": "source-fingerprint-key",
                "documents_total": 2,
                "chunks_total": 4,
                "source_scopes": [{"doc_type": "item", "granularity": None}],
                "chunks": [
                    {"doc_id": 1, "chunk_index": 0},
                    {"doc_id": 2, "chunk_index": 0},
                ],
            },
        },
    }

    persisted = workflow_freshness_diagnostics_view(freshness)

    assert persisted["key"] == freshness["key"]
    assert persisted["components"]["llm_model"] == "test/trends-model"
    assert persisted["components"]["analysis_model"] == "test/analyze-model"
    persisted_sources = persisted["components"]["upstream_sources"]
    assert persisted_sources == {
        "schema_version": 1,
        "key": "source-fingerprint-key",
        "documents_total": 2,
        "chunks_total": 4,
        "source_scopes": [{"doc_type": "item", "granularity": None}],
    }
    assert "chunks" in freshness["components"]["upstream_sources"]
