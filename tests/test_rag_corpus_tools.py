from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from recoleta.rag.corpus_tools import CorpusSpec
from recoleta.rag.corpus_tools import SearchService
from recoleta.rag.vector_store import LanceVectorStore
from recoleta.storage import Repository


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
    assert spec.resolve_sources(doc_type="idea", granularity=None) == [
        ("idea", "week")
    ]


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
