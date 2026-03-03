from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path

import pytest
from sqlmodel import Session, select

from recoleta.models import Document, DocumentChunk
from recoleta.pipeline import PipelineService
from recoleta.trends import day_period_bounds, semantic_search_summaries_in_period
from recoleta.types import ItemDraft, TrendResult, utc_now
from tests.spec_support import FakeAnalyzer, FakeTelegramSender, _build_runtime


def test_trends_day_indexes_items_and_persists_trend_document(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("PUBLISH_TARGETS", "markdown")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("TOPICS", json.dumps(["agents", "ml-systems"]))
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="trend-item-1",
        canonical_url="https://example.com/trend-item-1",
        title="Agents for Software",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-trend-day", drafts=[draft], limit=10)
    service.analyze(run_id="run-trend-day", limit=10)

    anchor = utc_now().date()
    period_start, period_end = day_period_bounds(anchor)
    payload = {
        "title": "Daily Trend",
        "granularity": "day",
        "period_start": period_start.isoformat(),
        "period_end": period_end.isoformat(),
        "overview_md": "- TL;DR: agents everywhere",
        "topics": ["agents"],
        "clusters": [],
        "highlights": ["agents"],
    }
    from recoleta.rag import agent as rag_agent
    from recoleta.trends import TrendPayload

    def _fake_generate(**kwargs):  # type: ignore[no-untyped-def]
        _ = kwargs
        return TrendPayload.model_validate(payload), {"tool_calls_total": 0}

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    result: TrendResult = service.trends(
        run_id="run-trend-day",
        granularity="day",
        anchor_date=anchor,
        llm_model="test/fake-model",
    )
    assert result.doc_id > 0
    assert result.granularity == "day"

    with Session(repository.engine) as session:
        docs = list(session.exec(select(Document)))
        assert any(doc.doc_type == "item" for doc in docs)
        assert any(doc.doc_type == "trend" for doc in docs)

        item_docs = [doc for doc in docs if doc.doc_type == "item"]
        assert len(item_docs) == 1

        summary_chunks = list(
            session.exec(
                select(DocumentChunk).where(
                    DocumentChunk.doc_id == item_docs[0].id,
                    DocumentChunk.chunk_index == 0,
                    DocumentChunk.kind == "summary",
                )
            )
        )
        assert len(summary_chunks) == 1
        assert "Summary for" in summary_chunks[0].text


def test_trends_text_search_can_find_summary_chunks(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("PUBLISH_TARGETS", "markdown")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("TOPICS", json.dumps(["agents", "ml-systems"]))
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="trend-item-2",
        canonical_url="https://example.com/trend-item-2",
        title="ML Systems",
        authors=["Bob"],
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-trend-search", drafts=[draft], limit=10)
    service.analyze(run_id="run-trend-search", limit=10)

    anchor = utc_now().date()
    period_start, period_end = day_period_bounds(anchor)
    payload = {
        "title": "Daily Trend",
        "granularity": "day",
        "period_start": period_start.isoformat(),
        "period_end": period_end.isoformat(),
        "overview_md": "- TL;DR: systems",
        "topics": ["ml-systems"],
        "clusters": [],
        "highlights": [],
    }
    from recoleta.rag import agent as rag_agent
    from recoleta.trends import TrendPayload

    def _fake_generate(**kwargs):  # type: ignore[no-untyped-def]
        _ = kwargs
        return TrendPayload.model_validate(payload), {"tool_calls_total": 0}

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    _ = service.trends(
        run_id="run-trend-search",
        granularity="day",
        anchor_date=anchor,
        llm_model="test/fake-model",
    )

    hits = repository.search_chunks_text(
        query="Summary",
        doc_type="item",
        period_start=period_start,
        period_end=period_end,
        limit=10,
    )
    assert hits
    assert hits[0]["doc_id"] > 0


def test_trends_semantic_search_ranks_relevant_summaries_higher(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))

    _, repository = _build_runtime()

    # Seed two documents + summary chunks (no pipeline needed for semantic search spec).
    with Session(repository.engine) as session:
        doc_a = Document(
            doc_type="item",
            item_id=1,
            title="A",
            published_at=datetime(2026, 1, 1, tzinfo=UTC),
        )
        doc_b = Document(
            doc_type="item",
            item_id=2,
            title="B",
            published_at=datetime(2026, 1, 1, tzinfo=UTC),
        )
        session.add(doc_a)
        session.add(doc_b)
        session.commit()
        session.refresh(doc_a)
        session.refresh(doc_b)
        assert doc_a.id is not None
        assert doc_b.id is not None
        doc_a_id = int(doc_a.id)
        doc_b_id = int(doc_b.id)

    chunk_a, _ = repository.upsert_document_chunk(
        doc_id=doc_a_id,
        chunk_index=0,
        kind="summary",
        text_value="Agents are great.",
        start_char=0,
        end_char=None,
        source_content_type="analysis_summary",
    )
    chunk_b, _ = repository.upsert_document_chunk(
        doc_id=doc_b_id,
        chunk_index=0,
        kind="summary",
        text_value="Gardening tips.",
        start_char=0,
        end_char=None,
        source_content_type="analysis_summary",
    )
    assert chunk_a.id is not None
    assert chunk_b.id is not None

    # Fake embedder: query -> [1,0], texts containing 'agents' -> [1,0], others -> [0,1]
    def fake_embedding(**kwargs):  # type: ignore[no-untyped-def]
        inputs = kwargs.get("input") or []
        data = []
        for text in inputs:
            token = str(text).lower()
            if "query:" in token or "agents" in token:
                data.append({"embedding": [1.0, 0.0]})
            else:
                data.append({"embedding": [0.0, 1.0]})
        return {"data": data, "usage": {"inputs": len(inputs)}}

    import recoleta.rag.embeddings as rag_embeddings

    monkeypatch.setattr(rag_embeddings, "_embedding", fake_embedding)

    period_start = datetime(2026, 1, 1, tzinfo=UTC)
    period_end = datetime(2026, 1, 2, tzinfo=UTC)
    hits = semantic_search_summaries_in_period(
        repository=repository,
        lancedb_dir=Path(str(tmp_path / "lancedb")),
        run_id="run-semantic",
        doc_type="item",
        period_start=period_start,
        period_end=period_end,
        query="agents",
        embedding_model="test/embed",
        embedding_dimensions=None,
        max_batch_inputs=64,
        max_batch_chars=40000,
        limit=5,
        corpus_limit=10,
    )
    assert hits
    assert hits[0].doc_id == doc_a_id
    assert hits[0].chunk_index == 0


def test_trends_semantic_search_reembeds_when_text_hash_changes(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))
    _, repository = _build_runtime()

    with Session(repository.engine) as session:
        doc = Document(
            doc_type="item",
            item_id=42,
            title="Dims",
            published_at=datetime(2026, 1, 1, tzinfo=UTC),
        )
        session.add(doc)
        session.commit()
        session.refresh(doc)
        assert doc.id is not None
        doc_id = int(doc.id)

    chunk, _ = repository.upsert_document_chunk(
        doc_id=doc_id,
        chunk_index=0,
        kind="summary",
        text_value="Agents are great.",
        start_char=0,
        end_char=None,
        source_content_type="analysis_summary",
    )
    assert chunk.id is not None
    # Seed an old vector row with a different text_hash value.
    from recoleta.rag.vector_store import (
        LanceVectorStore,
        VectorRow,
        embedding_table_name,
    )

    store = LanceVectorStore(
        db_dir=tmp_path / "lancedb",
        table_name=embedding_table_name(
            embedding_model="test/embed", embedding_dimensions=2
        ),
    )
    store.upsert_rows(
        rows=[
            VectorRow(
                chunk_id=int(chunk.id),
                doc_id=doc_id,
                doc_type="item",
                chunk_index=0,
                kind="summary",
                text_hash="old_hash",
                text_preview="old",
                event_start_ts=float(datetime(2026, 1, 1, tzinfo=UTC).timestamp()),
                event_end_ts=float(datetime(2026, 1, 1, tzinfo=UTC).timestamp()),
                vector=[0.0, 1.0],
            )
        ]
    )

    def fake_embedding(**kwargs):  # type: ignore[no-untyped-def]
        inputs = kwargs.get("input") or []
        dims = int(kwargs.get("dimensions") or 2)
        data = [{"embedding": [1.0] + [0.0] * (dims - 1)} for _ in inputs]
        return {"data": data, "usage": {"inputs": len(inputs)}}

    import recoleta.rag.embeddings as rag_embeddings

    monkeypatch.setattr(rag_embeddings, "_embedding", fake_embedding)

    period_start = datetime(2026, 1, 1, tzinfo=UTC)
    period_end = datetime(2026, 1, 2, tzinfo=UTC)
    hits = semantic_search_summaries_in_period(
        repository=repository,
        lancedb_dir=Path(str(tmp_path / "lancedb")),
        run_id="run-dims",
        doc_type="item",
        period_start=period_start,
        period_end=period_end,
        query="agents",
        embedding_model="test/embed",
        embedding_dimensions=2,
        max_batch_inputs=64,
        max_batch_chars=40000,
        limit=5,
        corpus_limit=10,
    )
    assert hits
    refreshed = LanceVectorStore(
        db_dir=tmp_path / "lancedb",
        table_name=embedding_table_name(
            embedding_model="test/embed", embedding_dimensions=2
        ),
    )
    existing = refreshed.fetch_existing_hashes(chunk_ids=[int(chunk.id)])
    assert existing.get(int(chunk.id)) == str(getattr(chunk, "text_hash") or "")


def test_trends_period_overlap_includes_cross_boundary_trend_docs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    _, repository = _build_runtime()

    # Month window: 2026-03-01..2026-04-01
    month_start = datetime(2026, 3, 1, tzinfo=UTC)
    month_end = datetime(2026, 4, 1, tzinfo=UTC)

    # Weekly trend crosses month boundary: 2026-02-24..2026-03-03 (overlaps March).
    trend_start = datetime(2026, 2, 24, tzinfo=UTC)
    trend_end = datetime(2026, 3, 3, tzinfo=UTC)

    with Session(repository.engine) as session:
        doc = Document(
            doc_type="trend",
            granularity="week",
            period_start=trend_start,
            period_end=trend_end,
            title="Cross-boundary week",
        )
        session.add(doc)
        session.commit()
        session.refresh(doc)
        assert doc.id is not None

    chunk, _ = repository.upsert_document_chunk(
        doc_id=int(doc.id),
        chunk_index=0,
        kind="summary",
        text_value="Cross-boundary trend summary.",
        start_char=0,
        end_char=None,
        source_content_type="trend_overview",
    )
    assert chunk.id is not None

    docs = repository.list_documents(
        doc_type="trend",
        granularity="week",
        period_start=month_start,
        period_end=month_end,
        order_by="event_asc",
        limit=50,
    )
    assert any(int(d.id or 0) == int(doc.id) for d in docs)


def test_trends_skips_llm_when_corpus_is_empty(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Spec: when there is no corpus, trends should not call the LLM (token-safe)."""

    monkeypatch.setenv("PUBLISH_TARGETS", "markdown")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    from recoleta.rag import agent as rag_agent

    def _must_not_call_agent(**kwargs):  # type: ignore[no-untyped-def]
        raise AssertionError("Trend agent must not be called for empty corpus")

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _must_not_call_agent)

    result: TrendResult = service.trends(
        run_id="run-trend-empty",
        granularity="day",
        anchor_date=utc_now().date(),
        llm_model="test/fake-model",
    )
    assert result.doc_id > 0

    with Session(repository.engine) as session:
        docs = list(session.exec(select(Document)))
        assert any(doc.doc_type == "trend" for doc in docs)
