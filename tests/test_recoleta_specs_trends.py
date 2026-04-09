from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
import io
import json
from pathlib import Path

import pytest
from sqlmodel import Session, select

from recoleta.models import Document, DocumentChunk
from recoleta.pipeline.service import PipelineService
from recoleta.trends import (
    TrendPayload,
    build_empty_trend_payload,
    day_period_bounds,
    index_items_as_documents,
    is_empty_trend_payload,
    persist_trend_payload,
    semantic_search_summaries_in_period,
    week_period_bounds,
)
from recoleta.types import (
    AnalyzeResult,
    AnalysisResult,
    IngestResult,
    ItemDraft,
    TrendResult,
    utc_now,
)
from tests.spec_support import FakeAnalyzer, FakeTelegramSender, _build_runtime


def test_trends_day_indexes_items_and_persists_trend_document(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("PUBLISH_TARGETS", "markdown")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("LLM_OUTPUT_LANGUAGE", "Chinese (Simplified)")
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
        assert kwargs.get("output_language") == "Chinese (Simplified)"
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


def test_trends_day_prepares_target_period_backlog_before_indexing(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("PUBLISH_TARGETS", "markdown")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("TOPICS", json.dumps(["agents"]))
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    period_calls: list[tuple[str, datetime, datetime]] = []
    item_id_holder: dict[str, int] = {}

    def fake_prepare(
        *,
        run_id: str,
        drafts=None,  # noqa: ANN001
        limit=None,  # noqa: ANN001
        period_start=None,  # noqa: ANN001
        period_end=None,  # noqa: ANN001
    ) -> IngestResult:
        _ = drafts, limit
        assert isinstance(period_start, datetime)
        assert isinstance(period_end, datetime)
        period_calls.append(("prepare", period_start, period_end))
        item, _ = repository.upsert_item(
            ItemDraft.from_values(
                source="rss",
                source_item_id="target-period-item",
                canonical_url="https://example.com/target-period-item",
                title="Target Period Item",
                authors=["Alice"],
                published_at=period_start,
                raw_metadata={"source": "test"},
            )
        )
        assert item.id is not None
        item_id_holder["item_id"] = int(item.id)
        _ = repository.upsert_content(
            item_id=int(item.id),
            content_type="html_maintext",
            text="Target period content " * 20,
        )
        repository.mark_item_enriched(item_id=int(item.id))
        return IngestResult(inserted=1)

    def fake_analyze(
        *,
        run_id: str,
        limit=None,  # noqa: ANN001
        period_start=None,  # noqa: ANN001
        period_end=None,  # noqa: ANN001
    ) -> AnalyzeResult:
        _ = run_id, limit
        assert isinstance(period_start, datetime)
        assert isinstance(period_end, datetime)
        period_calls.append(("analyze", period_start, period_end))
        repository.save_analysis(
            item_id=item_id_holder["item_id"],
            result=AnalysisResult(
                model="test/fake-model",
                provider="test",
                summary="Summary for Target Period Item",
                topics=["agents"],
                relevance_score=0.95,
                novelty_score=0.5,
                cost_usd=0.0,
                latency_ms=1,
            ),
        )
        return AnalyzeResult(processed=1)

    monkeypatch.setattr(service, "prepare", fake_prepare)
    monkeypatch.setattr(service, "analyze", fake_analyze)

    from recoleta.rag import agent as rag_agent
    from recoleta.trends import TrendPayload

    anchor = date(2026, 1, 1)
    period_start, period_end = day_period_bounds(anchor)
    payload = {
        "title": "Daily Trend",
        "granularity": "day",
        "period_start": period_start.isoformat(),
        "period_end": period_end.isoformat(),
        "overview_md": "- TL;DR: target period coverage",
        "topics": ["agents"],
        "clusters": [],
        "highlights": ["agents"],
    }

    def _fake_generate(**kwargs):  # type: ignore[no-untyped-def]
        _ = kwargs
        return TrendPayload.model_validate(payload), {"tool_calls_total": 0}

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    result = service.trends(
        run_id="run-trend-target-period",
        granularity="day",
        anchor_date=anchor,
        llm_model="test/fake-model",
    )

    assert result.doc_id > 0
    assert period_calls == [
        ("prepare", period_start, period_end),
        ("analyze", period_start, period_end),
    ]
    docs = repository.list_documents(
        doc_type="item",
        period_start=period_start,
        period_end=period_end,
        limit=10,
    )
    assert [str(getattr(doc, "title") or "") for doc in docs] == ["Target Period Item"]


def test_trends_index_items_clears_stale_content_chunks_when_content_shrinks(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Regression: re-indexing an item should not leave stale content chunks behind."""

    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))

    _, repository = _build_runtime()

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="stale-content-1",
        canonical_url="https://example.com/stale-content-1",
        title="Stale Content Chunks",
        authors=["Alice"],
        published_at=datetime(2026, 1, 1, tzinfo=UTC),
        raw_metadata={"source": "test"},
    )
    item, _ = repository.upsert_item(draft)
    assert item.id is not None
    item_id = int(item.id)

    analyzer = FakeAnalyzer()
    analysis, _ = analyzer.analyze(
        title=str(item.title),
        canonical_url=str(item.canonical_url),
        user_topics=["agents"],
        include_debug=False,
    )
    _ = repository.save_analysis(item_id=item_id, result=analysis)

    # First run: content splits into 2 chunks (200 + remainder).
    _ = repository.upsert_content(
        item_id=item_id, content_type="pdf_text", text="A" * 350
    )
    period_start = datetime(2026, 1, 1, tzinfo=UTC)
    period_end = datetime(2026, 1, 2, tzinfo=UTC)
    from recoleta.trends import index_items_as_documents

    _ = index_items_as_documents(
        repository=repository,
        run_id="run-stale-content-1",
        period_start=period_start,
        period_end=period_end,
        limit=10,
        content_chunk_chars=200,
        max_content_chunks_per_item=8,
    )

    with Session(repository.engine) as session:
        doc = session.exec(
            select(Document).where(
                Document.doc_type == "item", Document.item_id == item_id
            )
        ).first()
        assert doc is not None
        assert doc.id is not None
        doc_id = int(doc.id)

        chunks = list(
            session.exec(
                select(DocumentChunk).where(
                    DocumentChunk.doc_id == doc_id,
                    DocumentChunk.kind == "content",
                )
            )
        )
        assert any(c.chunk_index == 2 for c in chunks)

    # Second run: content shrinks to 1 chunk; chunk_index=2 should be removed.
    _ = repository.upsert_content(
        item_id=item_id, content_type="pdf_text", text="B" * 150
    )
    _ = index_items_as_documents(
        repository=repository,
        run_id="run-stale-content-2",
        period_start=period_start,
        period_end=period_end,
        limit=10,
        content_chunk_chars=200,
        max_content_chunks_per_item=8,
    )

    with Session(repository.engine) as session:
        stale = session.exec(
            select(DocumentChunk).where(
                DocumentChunk.doc_id == doc_id,
                DocumentChunk.kind == "content",
                DocumentChunk.chunk_index == 2,
            )
        ).first()
        assert stale is None


def test_index_items_as_documents_excludes_low_relevance_items(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Regression: trend item docs should respect min_relevance_score."""

    monkeypatch.setenv("PUBLISH_TARGETS", "markdown")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")

    _, repository = _build_runtime()
    period_start = datetime(2026, 1, 1, tzinfo=UTC)
    period_end = datetime(2026, 1, 2, tzinfo=UTC)

    for source_item_id, title, relevance in [
        ("trend-high", "High Signal Paper", 0.95),
        ("trend-low", "Low Signal Paper", 0.35),
    ]:
        draft = ItemDraft.from_values(
            source="rss",
            source_item_id=source_item_id,
            canonical_url=f"https://example.com/{source_item_id}",
            title=title,
            authors=["Alice"],
            published_at=period_start,
            raw_metadata={"source": "test"},
        )
        item, _ = repository.upsert_item(draft)
        assert item.id is not None
        _ = repository.save_analysis(
            item_id=int(item.id),
            result=AnalysisResult(
                model="test/fake-model",
                provider="test",
                summary=f"Summary for {title}",
                topics=["agents"],
                relevance_score=relevance,
                novelty_score=0.5,
                cost_usd=0.0,
                latency_ms=1,
            ),
        )

    _ = index_items_as_documents(
        repository=repository,
        run_id="run-trend-min-relevance",
        period_start=period_start,
        period_end=period_end,
        limit=10,
        min_relevance_score=0.8,
    )

    docs = repository.list_documents(
        doc_type="item",
        period_start=period_start,
        period_end=period_end,
        limit=10,
    )
    assert [str(getattr(doc, "title") or "") for doc in docs] == ["High Signal Paper"]


def test_index_items_as_documents_is_idempotent_for_item_meta_chunks(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("PUBLISH_TARGETS", "markdown")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "test/fake-model")
    monkeypatch.setenv("LLM_OUTPUT_LANGUAGE", "Chinese (Simplified)")
    monkeypatch.setenv("TOPICS", json.dumps(["agents"]))
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))

    settings, repository = _build_runtime()
    analyzer = FakeAnalyzer()

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="meta-idempotent-1",
        canonical_url="https://example.com/meta-idempotent-1",
        title="Meta Idempotence",
        authors=["Alice"],
        published_at=datetime(2026, 1, 1, tzinfo=UTC),
        raw_metadata={"source": "test"},
    )
    item, _ = repository.upsert_item(draft)
    assert item.id is not None
    item_id = int(item.id)
    analysis, _ = analyzer.analyze(
        title=str(item.title),
        canonical_url=str(item.canonical_url),
        user_topics=list(settings.topics),
        include_debug=False,
    )
    _ = repository.save_analysis(item_id=item_id, result=analysis)

    period_start = datetime(2026, 1, 1, tzinfo=UTC)
    period_end = datetime(2026, 1, 2, tzinfo=UTC)
    _ = index_items_as_documents(
        repository=repository,
        run_id="run-meta-idempotent-1",
        period_start=period_start,
        period_end=period_end,
        limit=10,
    )
    _ = index_items_as_documents(
        repository=repository,
        run_id="run-meta-idempotent-2",
        period_start=period_start,
        period_end=period_end,
        limit=10,
    )

    with Session(repository.engine) as session:
        doc = session.exec(
            select(Document).where(
                Document.doc_type == "item",
                Document.item_id == item_id,
            )
        ).first()
        assert doc is not None
        assert doc.id is not None
        meta_chunks = list(
            session.exec(
                select(DocumentChunk).where(
                    DocumentChunk.doc_id == int(doc.id),
                    DocumentChunk.kind == "meta",
                )
            )
        )

    assert len(meta_chunks) == 1


def test_index_items_as_documents_prunes_stale_low_relevance_docs(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Regression: trend item docs should be removed when an item's relevance drops below the threshold."""

    monkeypatch.setenv("PUBLISH_TARGETS", "markdown")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")

    _, repository = _build_runtime()
    period_start = datetime(2026, 1, 1, tzinfo=UTC)
    period_end = datetime(2026, 1, 2, tzinfo=UTC)
    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="trend-prune",
        canonical_url="https://example.com/trend-prune",
        title="Prunable Paper",
        authors=["Alice"],
        published_at=period_start,
        raw_metadata={"source": "test"},
    )
    item, _ = repository.upsert_item(draft)
    assert item.id is not None
    item_id = int(item.id)

    _ = repository.save_analysis(
        item_id=item_id,
        result=AnalysisResult(
            model="test/fake-model",
            provider="test",
            summary="High relevance summary",
            topics=["agents"],
            relevance_score=0.95,
            novelty_score=0.5,
            cost_usd=0.0,
            latency_ms=1,
        ),
    )
    _ = index_items_as_documents(
        repository=repository,
        run_id="run-trend-prune-1",
        period_start=period_start,
        period_end=period_end,
        limit=10,
        min_relevance_score=0.8,
    )
    assert repository.list_documents(
        doc_type="item",
        period_start=period_start,
        period_end=period_end,
        limit=10,
    )

    _ = repository.save_analysis(
        item_id=item_id,
        result=AnalysisResult(
            model="test/fake-model",
            provider="test",
            summary="Low relevance summary",
            topics=["agents"],
            relevance_score=0.2,
            novelty_score=0.5,
            cost_usd=0.0,
            latency_ms=1,
        ),
    )
    _ = index_items_as_documents(
        repository=repository,
        run_id="run-trend-prune-2",
        period_start=period_start,
        period_end=period_end,
        limit=10,
        min_relevance_score=0.8,
    )

    assert (
        repository.list_documents(
            doc_type="item",
            period_start=period_start,
            period_end=period_end,
            limit=10,
        )
        == []
    )


def test_index_items_as_documents_batches_writes_to_reduce_sql_commits(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Regression: indexing should not commit once per document chunk."""

    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")

    _, repository = _build_runtime()
    period_start = datetime(2026, 1, 1, tzinfo=UTC)
    period_end = datetime(2026, 1, 2, tzinfo=UTC)

    titles = [
        "Sparse retrieval graphs for robotic planners",
        "Photonic compilers for wafer-scale inference",
        "Mechanistic audits for browser agents",
        "Dataset distillation for multimodal search",
    ]

    for idx, title in enumerate(titles):
        draft = ItemDraft.from_values(
            source="rss",
            source_item_id=f"trend-batch-{idx}",
            canonical_url=f"https://example.com/trend-batch-{idx}",
            title=title,
            authors=["Alice"],
            published_at=period_start,
            raw_metadata={"source": "test"},
        )
        item, _ = repository.upsert_item(draft)
        assert item.id is not None
        item_id = int(item.id)
        _ = repository.save_analysis(
            item_id=item_id,
            result=AnalysisResult(
                model="test/fake-model",
                provider="test",
                summary=f"Summary for {title}",
                topics=["agents"],
                relevance_score=0.9,
                novelty_score=0.5,
                cost_usd=0.0,
                latency_ms=1,
            ),
        )
        _ = repository.upsert_content(
            item_id=item_id,
            content_type="pdf_text",
            text=(f"Item {idx} body. " * 60).strip(),
        )

    with repository.sql_diagnostics() as sql_diag:
        stats = index_items_as_documents(
            repository=repository,
            run_id="run-index-batch-commits",
            period_start=period_start,
            period_end=period_end,
            limit=10,
            content_chunk_chars=200,
            max_content_chunks_per_item=8,
        )

    assert stats["docs_upserted"] == 4
    assert stats["content_chunks_upserted"] > 0
    assert sql_diag.queries_total > 0
    assert sql_diag.commits_total > 0
    assert sql_diag.commits_total <= 4


def test_index_items_as_documents_passes_chunk_limit_to_segmenter(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Regression: indexing should bound chunk generation to max_content_chunks_per_item."""

    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")

    _, repository = _build_runtime()
    period_start = datetime(2026, 1, 1, tzinfo=UTC)
    period_end = datetime(2026, 1, 2, tzinfo=UTC)

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="trend-chunk-limit",
        canonical_url="https://example.com/trend-chunk-limit",
        title="Chunk Limit Paper",
        authors=["Alice"],
        published_at=period_start,
        raw_metadata={"source": "test"},
    )
    item, _ = repository.upsert_item(draft)
    assert item.id is not None

    item_id = int(item.id)
    _ = repository.save_analysis(
        item_id=item_id,
        result=AnalysisResult(
            model="test/fake-model",
            provider="test",
            summary="Summary for Chunk Limit Paper",
            topics=["agents"],
            relevance_score=0.9,
            novelty_score=0.5,
            cost_usd=0.0,
            latency_ms=1,
        ),
    )
    _ = repository.upsert_content(
        item_id=item_id,
        content_type="pdf_text",
        text="X" * 1_000,
    )

    import recoleta.trends as trends_mod

    original_chunk_text_segments = trends_mod._chunk_text_segments
    observed_limits: list[int | None] = []

    def _record_chunk_limit(  # type: ignore[no-untyped-def]
        text_value, *, chunk_chars, max_segments
    ):
        observed_limits.append(max_segments)
        return original_chunk_text_segments(
            text_value,
            chunk_chars=chunk_chars,
            max_segments=max_segments,
        )

    monkeypatch.setattr(trends_mod, "_chunk_text_segments", _record_chunk_limit)

    _ = index_items_as_documents(
        repository=repository,
        run_id="run-index-chunk-limit",
        period_start=period_start,
        period_end=period_end,
        limit=10,
        content_chunk_chars=200,
        max_content_chunks_per_item=2,
    )

    assert observed_limits == [2]


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


def test_search_chunks_text_accepts_hyphenated_query_terms(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Regression: FTS5 MATCH must not crash on hyphenated terms like 'vision-language'."""

    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))

    _, repository = _build_runtime()

    with Session(repository.engine) as session:
        doc = Document(
            doc_type="item",
            item_id=1,
            title="Hyphenated Query Spec",
            published_at=datetime(2026, 3, 4, tzinfo=UTC),
        )
        session.add(doc)
        session.commit()
        session.refresh(doc)
        assert doc.id is not None
        doc_id = int(doc.id)

    _chunk, _created = repository.upsert_document_chunk(
        doc_id=doc_id,
        chunk_index=0,
        kind="summary",
        text_value="Streaming vision-language models are improving.",
        start_char=0,
        end_char=None,
        source_content_type="analysis_summary",
    )

    period_start = datetime(2026, 3, 4, tzinfo=UTC)
    period_end = datetime(2026, 3, 5, tzinfo=UTC)
    hits = repository.search_chunks_text(
        query="streaming vision-language",
        doc_type="item",
        period_start=period_start,
        period_end=period_end,
        limit=10,
    )
    assert hits


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


def test_trends_semantic_search_reuses_warmed_summary_corpus_within_run(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Regression: repeated semantic searches in one run should not re-warm the same summary corpus."""

    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))
    _, repository = _build_runtime()

    period_start = datetime(2026, 1, 1, tzinfo=UTC)
    period_end = datetime(2026, 1, 2, tzinfo=UTC)

    docs: list[int] = []
    for idx, title, summary in [
        (1, "Agent Systems", "Agents are great."),
        (2, "Compiler Systems", "Systems are reliable."),
    ]:
        item, _ = repository.upsert_item(
            ItemDraft.from_values(
                source="rss",
                source_item_id=f"semantic-cache-{idx}",
                canonical_url=f"https://example.com/semantic-cache-{idx}",
                title=title,
                authors=["Alice"],
                published_at=period_start,
                raw_metadata={"source": "test"},
            )
        )
        assert item.id is not None
        doc = repository.upsert_document_for_item(item=item)
        assert doc.id is not None
        docs.append(int(doc.id))
        repository.upsert_document_chunk(
            doc_id=int(doc.id),
            chunk_index=0,
            kind="summary",
            text_value=summary,
            start_char=0,
            end_char=None,
            source_content_type="analysis_summary",
        )

    def fake_embedding(**kwargs):  # type: ignore[no-untyped-def]
        inputs = kwargs.get("input") or []
        data = []
        for text in inputs:
            token = str(text).lower()
            if "query:" in token:
                if "agents" in token:
                    data.append({"embedding": [1.0, 0.0]})
                else:
                    data.append({"embedding": [0.0, 1.0]})
            elif "agents" in token:
                data.append({"embedding": [1.0, 0.0]})
            else:
                data.append({"embedding": [0.0, 1.0]})
        return {"data": data, "usage": {"inputs": len(inputs)}}

    import recoleta.rag.embeddings as rag_embeddings
    import recoleta.rag.semantic_search as rag_semantic

    monkeypatch.setattr(rag_embeddings, "_embedding", fake_embedding)

    ensure_calls: list[str] = []
    original_ensure = rag_semantic.ensure_summary_vectors_for_period

    def counting_ensure(**kwargs):  # type: ignore[no-untyped-def]
        ensure_calls.append(str(kwargs.get("run_id") or ""))
        return original_ensure(**kwargs)

    monkeypatch.setattr(
        rag_semantic,
        "ensure_summary_vectors_for_period",
        counting_ensure,
    )

    hits_agents = semantic_search_summaries_in_period(
        repository=repository,
        lancedb_dir=Path(str(tmp_path / "lancedb")),
        run_id="run-semantic-cache",
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
    hits_systems = semantic_search_summaries_in_period(
        repository=repository,
        lancedb_dir=Path(str(tmp_path / "lancedb")),
        run_id="run-semantic-cache",
        doc_type="item",
        period_start=period_start,
        period_end=period_end,
        query="systems",
        embedding_model="test/embed",
        embedding_dimensions=None,
        max_batch_inputs=64,
        max_batch_chars=40000,
        limit=5,
        corpus_limit=10,
    )

    assert hits_agents
    assert hits_systems
    assert hits_agents[0].doc_id == docs[0]
    assert hits_systems[0].doc_id == docs[1]
    assert ensure_calls == ["run-semantic-cache"]


def test_trends_semantic_search_does_not_cache_partial_warmups_after_embed_errors(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Regression: transient embed failures must not freeze an incomplete corpus for the rest of the run."""

    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))
    _, repository = _build_runtime()

    period_start = datetime(2026, 1, 1, tzinfo=UTC)
    period_end = datetime(2026, 1, 2, tzinfo=UTC)

    for idx, title in enumerate(
        [
            "Robotic planners with agent memory",
            "Compiler diagnostics for retrieval systems",
        ]
    ):
        item, _ = repository.upsert_item(
            ItemDraft.from_values(
                source="rss",
                source_item_id=f"semantic-partial-{idx}",
                canonical_url=f"https://example.com/semantic-partial-{idx}",
                title=title,
                authors=["Alice"],
                published_at=period_start,
                raw_metadata={"source": "test"},
            )
        )
        assert item.id is not None
        doc = repository.upsert_document_for_item(item=item)
        assert doc.id is not None
        repository.upsert_document_chunk(
            doc_id=int(doc.id),
            chunk_index=0,
            kind="summary",
            text_value=f"Agents paper {idx}",
            start_char=0,
            end_char=None,
            source_content_type="analysis_summary",
        )

    import recoleta.rag.embeddings as rag_embeddings
    import recoleta.rag.semantic_search as rag_semantic

    content_embed_calls = 0

    def flaky_embedding(**kwargs):  # type: ignore[no-untyped-def]
        nonlocal content_embed_calls
        inputs = kwargs.get("input") or []
        token = str(inputs[0]).lower() if inputs else ""
        if "query:" in token:
            return {"data": [{"embedding": [1.0, 0.0]}], "usage": {"inputs": 1}}
        content_embed_calls += 1
        if content_embed_calls == 1:
            raise RuntimeError("transient embedding failure")
        return {"data": [{"embedding": [1.0, 0.0]}], "usage": {"inputs": len(inputs)}}

    monkeypatch.setattr(rag_embeddings, "_embedding", flaky_embedding)

    ensure_calls: list[str] = []
    original_ensure = rag_semantic.ensure_summary_vectors_for_period

    def counting_ensure(**kwargs):  # type: ignore[no-untyped-def]
        ensure_calls.append(str(kwargs.get("run_id") or ""))
        return original_ensure(**kwargs)

    monkeypatch.setattr(
        rag_semantic,
        "ensure_summary_vectors_for_period",
        counting_ensure,
    )

    first_hits = semantic_search_summaries_in_period(
        repository=repository,
        lancedb_dir=Path(str(tmp_path / "lancedb")),
        run_id="run-semantic-partial",
        doc_type="item",
        period_start=period_start,
        period_end=period_end,
        query="agents",
        embedding_model="test/embed",
        embedding_dimensions=None,
        max_batch_inputs=1,
        max_batch_chars=40000,
        embedding_failure_mode="continue",
        limit=5,
        corpus_limit=10,
    )
    second_hits = semantic_search_summaries_in_period(
        repository=repository,
        lancedb_dir=Path(str(tmp_path / "lancedb")),
        run_id="run-semantic-partial",
        doc_type="item",
        period_start=period_start,
        period_end=period_end,
        query="agents",
        embedding_model="test/embed",
        embedding_dimensions=None,
        max_batch_inputs=1,
        max_batch_chars=40000,
        embedding_failure_mode="continue",
        limit=5,
        corpus_limit=10,
    )

    assert len(first_hits) == 1
    assert len(second_hits) == 2
    assert ensure_calls == ["run-semantic-partial", "run-semantic-partial"]


def test_trends_vector_sync_threshold_aborts_after_max_errors_and_emits_log(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Spec: threshold failure mode aborts vector sync once max errors is reached."""

    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))
    _, repository = _build_runtime()

    with Session(repository.engine) as session:
        doc = Document(
            doc_type="item",
            item_id=101,
            title="Embedding failure policy",
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

    def _always_fail_embedding(**kwargs):  # type: ignore[no-untyped-def]
        _ = kwargs
        raise RuntimeError("simulated embedding failure")

    import recoleta.rag.embeddings as rag_embeddings

    monkeypatch.setattr(rag_embeddings, "_embedding", _always_fail_embedding)

    from loguru import logger as loguru_logger

    stream = io.StringIO()
    sink_id = loguru_logger.add(stream, level="WARNING")
    try:
        period_start = datetime(2026, 1, 1, tzinfo=UTC)
        period_end = datetime(2026, 1, 2, tzinfo=UTC)
        with pytest.raises(RuntimeError, match="simulated embedding failure"):
            _ = semantic_search_summaries_in_period(
                repository=repository,
                lancedb_dir=Path(str(tmp_path / "lancedb")),
                run_id="run-threshold-1",
                doc_type="item",
                period_start=period_start,
                period_end=period_end,
                query="agents",
                embedding_model="test/embed",
                embedding_dimensions=2,
                max_batch_inputs=64,
                max_batch_chars=40_000,
                embedding_failure_mode="threshold",
                embedding_max_errors=1,
                limit=5,
                corpus_limit=10,
            )
        output = stream.getvalue()
        assert "Vector sync aborting (threshold)" in output
    finally:
        loguru_logger.remove(sink_id)


def test_trends_vector_sync_threshold_aborts_when_all_batches_fail_and_emits_log(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Spec: threshold failure mode aborts even if max_errors is not reached, when all batches fail."""

    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))
    _, repository = _build_runtime()

    with Session(repository.engine) as session:
        doc = Document(
            doc_type="item",
            item_id=102,
            title="Embedding all-failure policy",
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

    def _always_fail_embedding(**kwargs):  # type: ignore[no-untyped-def]
        _ = kwargs
        raise RuntimeError("simulated embedding failure")

    import recoleta.rag.embeddings as rag_embeddings

    monkeypatch.setattr(rag_embeddings, "_embedding", _always_fail_embedding)

    from loguru import logger as loguru_logger

    stream = io.StringIO()
    sink_id = loguru_logger.add(stream, level="WARNING")
    try:
        period_start = datetime(2026, 1, 1, tzinfo=UTC)
        period_end = datetime(2026, 1, 2, tzinfo=UTC)
        with pytest.raises(RuntimeError, match="all embedding batches failed"):
            _ = semantic_search_summaries_in_period(
                repository=repository,
                lancedb_dir=Path(str(tmp_path / "lancedb")),
                run_id="run-threshold-all",
                doc_type="item",
                period_start=period_start,
                period_end=period_end,
                query="agents",
                embedding_model="test/embed",
                embedding_dimensions=2,
                max_batch_inputs=64,
                max_batch_chars=40_000,
                embedding_failure_mode="threshold",
                embedding_max_errors=10,
                limit=5,
                corpus_limit=10,
            )
        output = stream.getvalue()
        assert "Vector sync aborted (all batches failed)" in output
    finally:
        loguru_logger.remove(sink_id)


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


def test_trends_search_chunks_text_filters_by_trend_granularity(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    _, repository = _build_runtime()

    month_start = datetime(2026, 3, 1, tzinfo=UTC)
    month_end = datetime(2026, 4, 1, tzinfo=UTC)
    day_doc = repository.upsert_document_for_trend(
        granularity="day",
        period_start=datetime(2026, 3, 5, tzinfo=UTC),
        period_end=datetime(2026, 3, 6, tzinfo=UTC),
        title="Daily agents",
    )
    week_doc = repository.upsert_document_for_trend(
        granularity="week",
        period_start=datetime(2026, 3, 2, tzinfo=UTC),
        period_end=datetime(2026, 3, 9, tzinfo=UTC),
        title="Weekly agents",
    )
    month_doc = repository.upsert_document_for_trend(
        granularity="month",
        period_start=month_start,
        period_end=month_end,
        title="Monthly agents",
    )
    assert day_doc.id is not None
    assert week_doc.id is not None
    assert month_doc.id is not None

    repository.upsert_document_chunk(
        doc_id=int(day_doc.id),
        chunk_index=0,
        kind="summary",
        text_value="agents day summary",
        start_char=0,
        end_char=None,
        source_content_type="trend_overview",
    )
    repository.upsert_document_chunk(
        doc_id=int(week_doc.id),
        chunk_index=0,
        kind="summary",
        text_value="agents week summary",
        start_char=0,
        end_char=None,
        source_content_type="trend_overview",
    )
    repository.upsert_document_chunk(
        doc_id=int(month_doc.id),
        chunk_index=0,
        kind="summary",
        text_value="agents month summary",
        start_char=0,
        end_char=None,
        source_content_type="trend_overview",
    )

    hits = repository.search_chunks_text(
        query="agents",
        doc_type="trend",
        granularity="day",
        period_start=month_start,
        period_end=month_end,
        limit=10,
    )
    assert hits
    assert {int(hit["doc_id"]) for hit in hits} == {int(day_doc.id)}


def test_trends_semantic_search_filters_by_trend_granularity(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))
    _, repository = _build_runtime()

    month_start = datetime(2026, 3, 1, tzinfo=UTC)
    month_end = datetime(2026, 4, 1, tzinfo=UTC)
    with Session(repository.engine) as session:
        day_doc = Document(
            doc_type="trend",
            granularity="day",
            period_start=datetime(2026, 3, 5, tzinfo=UTC),
            period_end=datetime(2026, 3, 6, tzinfo=UTC),
            title="Daily agents",
        )
        week_doc = Document(
            doc_type="trend",
            granularity="week",
            period_start=datetime(2026, 3, 2, tzinfo=UTC),
            period_end=datetime(2026, 3, 9, tzinfo=UTC),
            title="Weekly gardening",
        )
        session.add(day_doc)
        session.add(week_doc)
        session.commit()
        session.refresh(day_doc)
        session.refresh(week_doc)
        assert day_doc.id is not None
        assert week_doc.id is not None
        day_doc_id = int(day_doc.id)
        week_doc_id = int(week_doc.id)

    repository.upsert_document_chunk(
        doc_id=day_doc_id,
        chunk_index=0,
        kind="summary",
        text_value="Agents are great.",
        start_char=0,
        end_char=None,
        source_content_type="trend_overview",
    )
    repository.upsert_document_chunk(
        doc_id=week_doc_id,
        chunk_index=0,
        kind="summary",
        text_value="Gardening tips.",
        start_char=0,
        end_char=None,
        source_content_type="trend_overview",
    )

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

    hits = semantic_search_summaries_in_period(
        repository=repository,
        lancedb_dir=Path(str(tmp_path / "lancedb")),
        run_id="run-semantic-granularity",
        doc_type="trend",
        granularity="day",
        period_start=month_start,
        period_end=month_end,
        query="agents",
        embedding_model="test/embed",
        embedding_dimensions=None,
        max_batch_inputs=64,
        max_batch_chars=40000,
        limit=5,
        corpus_limit=10,
    )
    assert hits
    assert {hit.doc_id for hit in hits} == {day_doc_id}


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


def test_week_trends_treat_empty_daily_trends_as_empty_corpus(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Regression: empty nested daily trend docs must not trigger weekly LLM synthesis."""

    monkeypatch.setenv("PUBLISH_TARGETS", "markdown")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "test/fake-model")
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    import recoleta.trends as trends_mod

    def _must_not_call_agent(**kwargs):  # type: ignore[no-untyped-def]
        raise AssertionError("Weekly trend LLM must not run for empty nested corpus")

    monkeypatch.setattr(trends_mod, "generate_trend_via_tools", _must_not_call_agent)

    anchor = date(2026, 3, 5)
    week_start, week_end = week_period_bounds(anchor)

    result: TrendResult = service.trends(
        run_id="run-trend-week-empty-nested",
        granularity="week",
        anchor_date=anchor,
        llm_model="test/fake-model",
    )

    assert result.doc_id > 0

    day_docs = repository.list_documents(
        doc_type="trend",
        granularity="day",
        period_start=week_start,
        period_end=week_end,
        order_by="event_asc",
        limit=20,
    )
    assert len(day_docs) == 7
    for day_doc in day_docs:
        assert day_doc.id is not None
        meta_chunk = repository.read_document_chunk(
            doc_id=int(day_doc.id),
            chunk_index=1,
        )
        assert meta_chunk is not None
        day_payload = TrendPayload.model_validate(
            json.loads(str(getattr(meta_chunk, "text", "") or "{}"))
        )
        assert is_empty_trend_payload(day_payload)

    week_pass_output = repository.get_latest_pass_output(
        pass_kind="trend_synthesis",
        status="succeeded",
        granularity="week",
        period_start=week_start,
        period_end=week_end,
    )
    assert week_pass_output is not None
    week_payload = TrendPayload.model_validate(
        json.loads(str(week_pass_output.payload_json or "{}"))
    )
    assert is_empty_trend_payload(week_payload)

    metric_values = {
        str(getattr(metric, "name", "")): float(getattr(metric, "value", 0.0))
        for metric in repository.list_metrics(run_id="run-trend-week-empty-nested")
    }
    assert metric_values["pipeline.trends.corpus.empty"] == 1.0


def test_week_trends_rerun_when_items_arrive_after_empty_daily_trends(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Regression: weekly reruns should not stay empty when self-similar item sources exist."""

    monkeypatch.setenv("PUBLISH_TARGETS", "markdown")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "test/fake-model")
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))
    monkeypatch.setenv("TRENDS_SELF_SIMILAR_ENABLED", "true")
    monkeypatch.setenv("TRENDS_PEER_HISTORY_ENABLED", "false")

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    anchor = date(2026, 3, 5)
    week_start, week_end = week_period_bounds(anchor)
    for offset in range(7):
        day_start, day_end = day_period_bounds((week_start + timedelta(days=offset)).date())
        payload = build_empty_trend_payload(
            granularity="day",
            period_start=day_start,
            period_end=day_end,
            output_language=None,
        )
        _ = persist_trend_payload(
            repository=repository,
            granularity="day",
            period_start=day_start,
            period_end=day_end,
            payload=payload,
        )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="late-week-item",
        canonical_url="https://example.com/late-week-item",
        title="Late Week Item",
        authors=["Alice"],
        published_at=datetime(2026, 3, 5, 1, 0, tzinfo=UTC),
        raw_metadata={"source": "test"},
    )
    item, _inserted = repository.upsert_item(draft)
    assert item.id is not None
    _ = repository.save_analysis(
        item_id=int(item.id),
        result=AnalysisResult(
            model="test/fake-model",
            provider="test",
            summary="## Summary\n\nLate item summary.",
            topics=["agents"],
            relevance_score=0.9,
            novelty_score=0.5,
            cost_usd=0.0,
            latency_ms=1,
        ),
    )

    import recoleta.trends as trends_mod

    calls = {"total": 0}

    def _fake_generate_trend_via_tools(**kwargs):  # type: ignore[no-untyped-def]
        calls["total"] += 1
        assert kwargs.get("rag_sources") == [
            {"doc_type": "item", "granularity": None},
            {"doc_type": "trend", "granularity": "day"},
        ]
        return (
            TrendPayload(
                title="Weekly Trend",
                granularity="week",
                period_start=week_start.isoformat(),
                period_end=week_end.isoformat(),
                overview_md="- weekly synthesis uses late item corpus",
                topics=["agents"],
                clusters=[],
            ),
            {"tool_calls_total": 0},
        )

    monkeypatch.setattr(
        trends_mod, "generate_trend_via_tools", _fake_generate_trend_via_tools
    )

    result: TrendResult = service.trends(
        run_id="run-trend-week-rerun-after-empty-days",
        granularity="week",
        anchor_date=anchor,
        llm_model="test/fake-model",
    )

    assert result.doc_id > 0
    assert calls["total"] == 1

    week_pass_output = repository.get_latest_pass_output(
        pass_kind="trend_synthesis",
        status="succeeded",
        granularity="week",
        period_start=week_start,
        period_end=week_end,
    )
    assert week_pass_output is not None
    week_payload = TrendPayload.model_validate(
        json.loads(str(week_pass_output.payload_json or "{}"))
    )
    assert not is_empty_trend_payload(week_payload)

    metric_values = {
        str(getattr(metric, "name", "")): float(getattr(metric, "value", 0.0))
        for metric in repository.list_metrics(
            run_id="run-trend-week-rerun-after-empty-days"
        )
    }
    assert metric_values["pipeline.trends.corpus.empty"] == 0.0
