from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path
from typing import Any

import pytest
from sqlmodel import Session, select

from recoleta.models import Document, DocumentChunk
from recoleta.pipeline import PipelineService
from recoleta.trends import day_period_bounds, semantic_search_summaries_in_period
from recoleta.types import ItemDraft, TrendResult, utc_now
from tests.spec_support import FakeAnalyzer, FakeTelegramSender, _build_runtime


def _fake_completion_returning_json(payload: dict[str, Any]):
    def _completion(**kwargs):  # type: ignore[no-untyped-def]
        _ = kwargs
        return {"choices": [{"message": {"content": json.dumps(payload)}}]}

    return _completion


def test_trends_day_indexes_items_and_persists_trend_document(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("PUBLISH_TARGETS", "markdown")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("TOPICS", json.dumps(["agents", "ml-systems"]))

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

    import recoleta.trends as trends

    monkeypatch.setattr(
        trends, "_get_completion", lambda: _fake_completion_returning_json(payload)
    )

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
    import recoleta.trends as trends

    monkeypatch.setattr(
        trends, "_get_completion", lambda: _fake_completion_returning_json(payload)
    )

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

    import recoleta.trends as trends

    monkeypatch.setattr(trends, "embedding", fake_embedding)

    period_start = datetime(2026, 1, 1, tzinfo=UTC)
    period_end = datetime(2026, 1, 2, tzinfo=UTC)
    hits = semantic_search_summaries_in_period(
        repository=repository,
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


def test_trends_semantic_search_reembeds_when_embedding_dimensions_change(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
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

    # Seed an old embedding row with a different dimensions value.
    repository.upsert_chunk_embedding(
        chunk_id=int(chunk.id),
        model="test/embed",
        dimensions=2,
        text_hash=str(getattr(chunk, "text_hash") or ""),
        vector=[1.0, 0.0],
    )

    def fake_embedding(**kwargs):  # type: ignore[no-untyped-def]
        inputs = kwargs.get("input") or []
        dims = int(kwargs.get("dimensions") or 3)
        data = [{"embedding": [1.0] + [0.0] * (dims - 1)} for _ in inputs]
        return {"data": data, "usage": {"inputs": len(inputs)}}

    import recoleta.trends as trends

    monkeypatch.setattr(trends, "embedding", fake_embedding)

    period_start = datetime(2026, 1, 1, tzinfo=UTC)
    period_end = datetime(2026, 1, 2, tzinfo=UTC)
    hits = semantic_search_summaries_in_period(
        repository=repository,
        run_id="run-dims",
        doc_type="item",
        period_start=period_start,
        period_end=period_end,
        query="agents",
        embedding_model="test/embed",
        embedding_dimensions=3,
        max_batch_inputs=64,
        max_batch_chars=40000,
        limit=5,
        corpus_limit=10,
    )
    assert hits

    updated = repository.get_chunk_embedding(chunk_id=int(chunk.id), model="test/embed")
    assert updated is not None
    assert updated.dimensions == 3


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
