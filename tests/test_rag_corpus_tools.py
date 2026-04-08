from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from recoleta.rag.corpus_tools import CorpusSpec
from recoleta.rag.corpus_tools import SearchService
from recoleta.rag.vector_store import LanceVectorStore
from recoleta.storage import Repository
from recoleta.trends import day_period_bounds, index_items_as_documents
from recoleta.types import AnalysisResult, ItemDraft


def test_corpus_spec_resolves_only_allowed_sources() -> None:
    spec = CorpusSpec.from_rag_sources(
        [
            {"doc_type": "item", "granularity": None},
            {"doc_type": "trend", "granularity": "day"},
            {"doc_type": "idea", "granularity": "week"},
        ]
    )

    assert spec.resolve_sources(doc_type="item", granularity=None) == [("item", None)]
    assert spec.resolve_sources(doc_type="trend", granularity=None) == [
        ("trend", "day")
    ]
    assert spec.resolve_sources(doc_type="trend", granularity="month") == []
    assert spec.resolve_sources(doc_type="idea", granularity=None) == [("idea", "week")]


def test_search_text_excludes_meta_chunks_from_agent_visible_hits(
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()

    period_start = datetime(2026, 3, 2, tzinfo=UTC)
    period_end = datetime(2026, 3, 3, tzinfo=UTC)
    doc = repository.upsert_document_for_idea(
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        title="Workflow wedges",
    )
    assert doc.id is not None
    repository.upsert_document_chunk(
        doc_id=int(doc.id),
        chunk_index=0,
        kind="summary",
        text_value="Auditable workflow wedge for long-horizon evaluation.",
        source_content_type="trend_ideas_summary",
    )
    repository.upsert_document_chunk(
        doc_id=int(doc.id),
        chunk_index=1,
        kind="meta",
        text_value=(
            '{"_projection":{"pass_output_id":7,"pass_kind":"trend_ideas",'
            '"upstream_pass_output_id":3,"upstream_pass_kind":"trend_synthesis"}}'
        ),
        source_content_type="trend_ideas_payload_json",
    )

    service = SearchService(
        repository=repository,
        vector_store=LanceVectorStore(
            db_dir=tmp_path / "lancedb",
            table_name="test_meta_filter",
        ),
        run_id="run-meta-filter",
        period_start=period_start,
        period_end=period_end,
        corpus_spec=CorpusSpec.from_rag_sources(
            [{"doc_type": "idea", "granularity": "day"}]
        ),
        embedding_model="test/fake-embedding",
        embedding_dimensions=None,
        embedding_batch_max_inputs=8,
        embedding_batch_max_chars=2000,
    )

    provenance_hits = service.search_text(
        query="trend_synthesis",
        doc_type="idea",
        granularity="day",
        limit=5,
    )
    assert provenance_hits["hits"] == []

    summary_hits = service.search_text(
        query="long-horizon evaluation",
        doc_type="idea",
        granularity="day",
        limit=5,
    )
    assert summary_hits["returned"] == 1
    assert summary_hits["hits"][0]["kind"] == "summary"
    assert service.read_chunk(doc_id=int(doc.id), chunk_index=1) == {"chunk": None}


def test_item_meta_chunks_stay_stored_but_not_searchable(
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()

    anchor = datetime(2026, 3, 5, tzinfo=UTC).date()
    day_start, day_end = day_period_bounds(anchor)
    item, _ = repository.upsert_item(
        ItemDraft.from_values(
            source="rss",
            source_item_id="item-meta-filter",
            canonical_url="https://example.com/item-meta-filter",
            title="Item Meta Filter",
            authors=["Alice"],
            published_at=day_start,
            raw_metadata={"source": "test"},
        )
    )
    assert item.id is not None
    repository.save_analysis(
        item_id=int(item.id),
        result=AnalysisResult(
            model="test/fake-model",
            provider="test",
            summary="Planning loops stay grounded in retrieved summaries.",
            topics=["agents"],
            relevance_score=0.9,
            novelty_score=0.4,
            cost_usd=0.0,
            latency_ms=1,
        ),
    )
    _ = index_items_as_documents(
        repository=repository,
        run_id="run-item-meta-filter",
        period_start=day_start,
        period_end=day_end,
    )

    meta_chunks = repository.list_document_chunks_in_period(
        doc_type="item",
        kind="meta",
        period_start=day_start,
        period_end=day_end,
        limit=10,
    )
    assert len(meta_chunks) == 1
    meta_chunk = meta_chunks[0]
    assert meta_chunk.id is not None

    service = SearchService(
        repository=repository,
        vector_store=LanceVectorStore(
            db_dir=tmp_path / "lancedb",
            table_name="test_item_meta_filter",
        ),
        run_id="run-item-meta-filter",
        period_start=day_start,
        period_end=day_end,
        corpus_spec=CorpusSpec.from_rag_sources([{"doc_type": "item", "granularity": None}]),
        embedding_model="test/fake-embedding",
        embedding_dimensions=None,
        embedding_batch_max_inputs=8,
        embedding_batch_max_chars=2000,
    )

    provenance_hits = service.search_text(
        query="relevance_score",
        doc_type="item",
        limit=5,
    )
    assert provenance_hits["hits"] == []
    assert service.read_chunk(
        doc_id=int(getattr(meta_chunk, "doc_id")),
        chunk_index=int(getattr(meta_chunk, "chunk_index")),
    ) == {"chunk": None}

    summary_rows = repository.list_summary_chunk_index_rows_in_period(
        doc_type="item",
        period_start=day_start,
        period_end=day_end,
        limit=10,
    )
    assert len(summary_rows) == 1
    assert summary_rows[0]["kind"] == "summary"
    assert summary_rows[0]["chunk_id"] != int(meta_chunk.id)


def test_doc_id_helpers_respect_active_corpus_bounds(
    tmp_path: Path,
) -> None:
    """Regression: instance-local corpus helpers must still hide out-of-window docs."""
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()

    period_start = datetime(2026, 3, 2, tzinfo=UTC)
    period_end = datetime(2026, 3, 3, tzinfo=UTC)
    visible_doc = repository.upsert_document_for_idea(
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        title="Visible idea",
    )
    hidden_scope_doc = repository.upsert_document_for_idea(
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        title="Other stream idea",
    )
    hidden_window_doc = repository.upsert_document_for_idea(
        granularity="day",
        period_start=datetime(2026, 2, 1, tzinfo=UTC),
        period_end=datetime(2026, 2, 2, tzinfo=UTC),
        title="Older idea",
    )
    assert visible_doc.id is not None
    assert hidden_scope_doc.id is not None
    assert hidden_window_doc.id is not None
    assert int(hidden_scope_doc.id) == int(visible_doc.id)

    repository.upsert_document_chunk(
        doc_id=int(visible_doc.id),
        chunk_index=0,
        kind="summary",
        text_value="Visible summary.",
        source_content_type="trend_ideas_summary",
    )
    repository.upsert_document_chunk(
        doc_id=int(hidden_window_doc.id),
        chunk_index=0,
        kind="summary",
        text_value="Older summary.",
        source_content_type="trend_ideas_summary",
    )

    service = SearchService(
        repository=repository,
        vector_store=LanceVectorStore(
            db_dir=tmp_path / "lancedb",
            table_name="test_doc_visibility",
        ),
        run_id="run-doc-visibility",
        period_start=period_start,
        period_end=period_end,
        corpus_spec=CorpusSpec.from_rag_sources(
            [{"doc_type": "idea", "granularity": "day"}]
        ),
        embedding_model="test/fake-embedding",
        embedding_dimensions=None,
        embedding_batch_max_inputs=8,
        embedding_batch_max_chars=2000,
    )

    listed = service.list_docs(doc_type="idea", granularity="day", limit=10)
    assert [doc["doc_id"] for doc in listed["docs"]] == [int(visible_doc.id)]

    visible_doc_result = service.get_doc(doc_id=int(visible_doc.id))
    assert visible_doc_result["doc"] is not None
    assert visible_doc_result["doc"]["doc_id"] == int(visible_doc.id)
    assert service.get_doc(doc_id=int(hidden_window_doc.id)) == {"doc": None}

    visible_bundle = service.get_doc_bundle(doc_id=int(visible_doc.id))
    assert visible_bundle["bundle"] is not None
    assert visible_bundle["bundle"]["doc"]["doc_id"] == int(visible_doc.id)
    assert service.get_doc_bundle(doc_id=int(hidden_window_doc.id)) == {"bundle": None}

    visible_chunk = service.read_chunk(doc_id=int(visible_doc.id), chunk_index=0)
    assert visible_chunk["chunk"] is not None
    assert visible_chunk["chunk"]["text"] == "Visible summary."
    assert service.read_chunk(doc_id=int(hidden_window_doc.id), chunk_index=0) == {
        "chunk": None
    }
