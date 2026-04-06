from __future__ import annotations

import importlib
from typing import Any, cast

from pydantic_ai.messages import (
    ModelRequest,
    ModelResponse,
    ToolCallPart,
    ToolReturnPart,
)


rag_agent = importlib.import_module("recoleta.rag.agent")


def test_trend_agent_tools_expose_descriptions_and_hybrid_search() -> None:
    agent = rag_agent.build_trend_agent(llm_model="openai/gpt-4o-mini")

    tool_defs = agent._function_toolset.tools

    assert "search_hybrid" in tool_defs
    assert "get_doc_bundle" in tool_defs
    for tool_name in (
        "list_docs",
        "get_doc",
        "get_doc_bundle",
        "read_chunk",
        "search_text",
        "search_semantic",
        "search_hybrid",
    ):
        description = tool_defs[tool_name].description
        assert isinstance(description, str)
        assert description.strip()


def test_reciprocal_rank_fuse_search_hits_promotes_overlap() -> None:
    fused = rag_agent._reciprocal_rank_fuse_search_hits(
        text_hits=[
            {
                "doc_id": 1,
                "chunk_index": 0,
                "title": "Lexical-only paper",
                "canonical_url": "https://example.com/1",
                "snippet": "lexical signal",
            },
            {
                "doc_id": 2,
                "chunk_index": 0,
                "title": "Shared paper",
                "canonical_url": "https://example.com/2",
                "snippet": "shared lexical signal",
            },
        ],
        semantic_hits=[
            {
                "doc_id": 2,
                "chunk_index": 0,
                "title": "Shared paper",
                "canonical_url": "https://example.com/2",
                "text_preview": "shared semantic signal",
                "score": 0.91,
            },
            {
                "doc_id": 3,
                "chunk_index": 0,
                "title": "Semantic-only paper",
                "canonical_url": "https://example.com/3",
                "text_preview": "semantic signal",
                "score": 0.84,
            },
        ],
        limit=3,
    )

    assert [(row["doc_id"], row["chunk_index"]) for row in fused] == [
        (2, 0),
        (1, 0),
        (3, 0),
    ]
    assert fused[0]["match_sources"] == ["text", "semantic"]
    assert fused[0]["snippet"] == "shared lexical signal"
    assert fused[0]["text_preview"] == "shared semantic signal"
    assert fused[0]["rrf_score"] > fused[1]["rrf_score"]
    assert fused[1]["match_sources"] == ["text"]
    assert fused[2]["match_sources"] == ["semantic"]


def test_search_text_backoff_recovers_hits_for_long_conjunctive_query(
    monkeypatch,
    tmp_path,
) -> None:
    from datetime import UTC, datetime, timedelta
    from types import SimpleNamespace

    from recoleta.rag.agent import TrendAgentDeps, build_trend_agent
    from recoleta.rag.vector_store import LanceVectorStore
    from recoleta.types import AnalysisResult, ItemDraft
    from tests.spec_support import _build_runtime

    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")

    _, repository = _build_runtime()
    period_start = datetime(2026, 3, 2, tzinfo=UTC)
    period_end = period_start + timedelta(days=1)

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="tooling-backoff-paper",
        canonical_url="https://example.com/tooling-backoff-paper",
        title="Agent Memory Loops",
        authors=["Alice"],
        published_at=period_start + timedelta(hours=1),
        raw_metadata={"source": "test"},
    )
    item, _ = repository.upsert_item(draft)
    assert item.id is not None
    repository.upsert_contents_texts(
        item_id=int(item.id),
        texts_by_type={
            "html_maintext": (
                "retrieval memory loop tool use verifier loop for long-horizon agents"
            )
        },
    )
    repository.mark_item_enriched(item_id=int(item.id))
    repository.save_analysis(
        item_id=int(item.id),
        result=AnalysisResult(
            model="test/fake-model",
            provider="test",
            summary="Summary: retrieval memory loops for agents.",
            topics=["agents"],
            relevance_score=0.95,
            novelty_score=0.4,
            cost_usd=0.0,
            latency_ms=1,
        ),
    )

    from recoleta.trends import index_items_as_documents

    _ = index_items_as_documents(
        repository=repository,
        run_id="run-search-text-backoff",
        period_start=period_start,
        period_end=period_end,
    )

    agent = build_trend_agent(llm_model="openai/gpt-4o-mini")
    tool = agent._function_toolset.tools["search_text"].function
    ctx = cast(
        Any,
        SimpleNamespace(
            deps=TrendAgentDeps(
                repository=repository,
                vector_store=LanceVectorStore(db_dir=tmp_path / "lancedb"),
                run_id="run-search-text-backoff",
                period_start=period_start,
                period_end=period_end,
                rag_sources=[{"doc_type": "item", "granularity": None}],
                embedding_model="test/embed",
                embedding_dimensions=None,
                embedding_batch_max_inputs=64,
                embedding_batch_max_chars=40_000,
            )
        ),
    )

    result = tool(
        ctx,
        query="agent memory retrieval loops",
        doc_type="item",
        limit=3,
    )

    assert result["returned"] >= 1
    assert result["matched_queries"][0] == "memory retrieval loops"
    hit = result["hits"][0]
    assert hit["title"] == "Agent Memory Loops"
    assert hit["matched_query"] == "memory retrieval loops"
    assert hit["backoff_depth"] == 1


def test_search_text_backoff_caps_candidate_budget_for_long_queries() -> None:
    from datetime import UTC, datetime

    from recoleta.rag.corpus_tools import _collect_text_hits_with_backoff

    seen_queries: list[str] = []

    class _FakeRepository:
        def search_chunks_text(self, **kwargs):  # type: ignore[no-untyped-def]
            seen_queries.append(str(kwargs.get("query") or ""))
            return []

    hits, matched_queries = _collect_text_hits_with_backoff(
        repository=cast(Any, _FakeRepository()),
        query=" ".join(f"term{i}" for i in range(40)),
        doc_type="item",
        granularity=None,
        period_start=datetime(2026, 3, 2, tzinfo=UTC),
        period_end=datetime(2026, 3, 3, tzinfo=UTC),
        limit=5,
    )

    assert hits == []
    assert matched_queries == []
    assert len(seen_queries) == rag_agent._SEARCH_TEXT_BACKOFF_MAX_CANDIDATES
    token_counts = [len(query.split()) for query in seen_queries]
    assert max(token_counts) == 40
    assert min(token_counts) <= 3


def test_get_doc_bundle_returns_summary_sections_and_content_chunks(
    monkeypatch,
    tmp_path,
) -> None:
    from datetime import UTC, datetime, timedelta
    from types import SimpleNamespace

    from recoleta.rag.agent import TrendAgentDeps, build_trend_agent
    from recoleta.rag.vector_store import LanceVectorStore
    from recoleta.types import AnalysisResult, ItemDraft
    from tests.spec_support import _build_runtime

    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")

    _, repository = _build_runtime()
    period_start = datetime(2026, 3, 2, tzinfo=UTC)
    period_end = period_start + timedelta(days=1)

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="doc-bundle-paper",
        canonical_url="https://example.com/doc-bundle-paper",
        title="Agent Memory Loops",
        authors=["Alice"],
        published_at=period_start + timedelta(hours=1),
        raw_metadata={"source": "test"},
    )
    item, _ = repository.upsert_item(draft)
    assert item.id is not None
    repository.upsert_contents_texts(
        item_id=int(item.id),
        texts_by_type={
            "html_maintext": (
                "This paper studies retrieval memory loops for long-horizon agents. "
                "A verifier loop checks tool results before replanning."
            )
        },
    )
    repository.mark_item_enriched(item_id=int(item.id))
    repository.save_analysis(
        item_id=int(item.id),
        result=AnalysisResult(
            model="test/fake-model",
            provider="test",
            summary=(
                "Summary: retrieval memory loops for agents.\n"
                "Problem: planners forget earlier observations.\n"
                "Approach: retrieval-augmented memory with verifier loops.\n"
                "Results: fewer cascading tool errors."
            ),
            topics=["agents"],
            relevance_score=0.95,
            novelty_score=0.4,
            cost_usd=0.0,
            latency_ms=1,
        ),
    )

    from recoleta.trends import index_items_as_documents

    _ = index_items_as_documents(
        repository=repository,
        run_id="run-doc-bundle",
        period_start=period_start,
        period_end=period_end,
    )

    doc = repository.list_documents(
        doc_type="item",
        period_start=period_start,
        period_end=period_end,
        limit=1,
    )[0]
    assert doc.id is not None

    agent = build_trend_agent(llm_model="openai/gpt-4o-mini")
    tool = agent._function_toolset.tools["get_doc_bundle"].function
    ctx = cast(
        Any,
        SimpleNamespace(
            deps=TrendAgentDeps(
                repository=repository,
                vector_store=LanceVectorStore(db_dir=tmp_path / "lancedb"),
                run_id="run-doc-bundle",
                period_start=period_start,
                period_end=period_end,
                rag_sources=[{"doc_type": "item", "granularity": None}],
                embedding_model="test/embed",
                embedding_dimensions=None,
                embedding_batch_max_inputs=64,
                embedding_batch_max_chars=40_000,
            )
        ),
    )

    result = tool(ctx, doc_id=int(doc.id), content_limit=2, content_chars=120)

    bundle = result["bundle"]
    assert bundle["doc"]["title"] == "Agent Memory Loops"
    assert bundle["summary"]["text"].startswith("Summary: retrieval memory loops")
    assert (
        bundle["summary_sections"]["problem"] == "planners forget earlier observations."
    )
    assert bundle["content_chunks"]
    assert bundle["content_chunks"][0]["source_content_type"] == "html_maintext"
    assert "verifier loop checks tool results" in bundle["content_chunks"][0]["text"]


def test_get_doc_bundle_parses_inline_legacy_summary_sections(
    monkeypatch,
    tmp_path,
) -> None:
    from datetime import UTC, datetime, timedelta
    from types import SimpleNamespace

    from recoleta.rag.agent import TrendAgentDeps, build_trend_agent
    from recoleta.rag.vector_store import LanceVectorStore
    from recoleta.types import AnalysisResult, ItemDraft
    from tests.spec_support import _build_runtime

    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")

    _, repository = _build_runtime()
    period_start = datetime(2026, 3, 2, tzinfo=UTC)
    period_end = period_start + timedelta(days=1)

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="doc-bundle-inline-paper",
        canonical_url="https://example.com/doc-bundle-inline-paper",
        title="Inline Summary Paper",
        authors=["Alice"],
        published_at=period_start + timedelta(hours=1),
        raw_metadata={"source": "test"},
    )
    item, _ = repository.upsert_item(draft)
    assert item.id is not None
    repository.upsert_contents_texts(
        item_id=int(item.id),
        texts_by_type={"html_maintext": "inline content chunk"},
    )
    repository.mark_item_enriched(item_id=int(item.id))
    repository.save_analysis(
        item_id=int(item.id),
        result=AnalysisResult(
            model="test/fake-model",
            provider="test",
            summary=(
                "Summary: memory loops for agents. "
                "Problem: planners forget observations. "
                "Approach: retrieval-augmented verifier loops. "
                "Results: fewer cascading tool errors."
            ),
            topics=["agents"],
            relevance_score=0.95,
            novelty_score=0.4,
            cost_usd=0.0,
            latency_ms=1,
        ),
    )

    from recoleta.trends import index_items_as_documents

    _ = index_items_as_documents(
        repository=repository,
        run_id="run-doc-bundle-inline",
        period_start=period_start,
        period_end=period_end,
    )

    doc = repository.list_documents(
        doc_type="item",
        period_start=period_start,
        period_end=period_end,
        limit=1,
    )[0]
    assert doc.id is not None

    agent = build_trend_agent(llm_model="openai/gpt-4o-mini")
    tool = agent._function_toolset.tools["get_doc_bundle"].function
    ctx = cast(
        Any,
        SimpleNamespace(
            deps=TrendAgentDeps(
                repository=repository,
                vector_store=LanceVectorStore(db_dir=tmp_path / "lancedb"),
                run_id="run-doc-bundle-inline",
                period_start=period_start,
                period_end=period_end,
                rag_sources=[{"doc_type": "item", "granularity": None}],
                embedding_model="test/embed",
                embedding_dimensions=None,
                embedding_batch_max_inputs=64,
                embedding_batch_max_chars=40_000,
            )
        ),
    )

    result = tool(ctx, doc_id=int(doc.id), content_limit=1, content_chars=120)

    sections = result["bundle"]["summary_sections"]
    assert sections["summary"] == "memory loops for agents."
    assert sections["problem"] == "planners forget observations."
    assert sections["approach"] == "retrieval-augmented verifier loops."
    assert sections["results"] == "fewer cascading tool errors."


def test_extract_raw_tool_trace_captures_calls_and_returns() -> None:
    messages = [
        ModelResponse(
            parts=[
                ToolCallPart(
                    tool_name="search_hybrid",
                    args={"query": "agent memory loops", "doc_type": "item"},
                    tool_call_id="call-1",
                )
            ]
        ),
        ModelRequest(
            parts=[
                ToolReturnPart(
                    tool_name="search_hybrid",
                    tool_call_id="call-1",
                    content={
                        "hits": [
                            {"doc_id": 42, "chunk_index": 0, "title": "Agent Memory"}
                        ],
                        "returned": 1,
                    },
                )
            ]
        ),
        ModelResponse(
            parts=[
                ToolCallPart(
                    tool_name="get_doc_bundle",
                    args={"doc_id": 42, "content_limit": 2},
                    tool_call_id="call-2",
                )
            ]
        ),
        ModelRequest(
            parts=[
                ToolReturnPart(
                    tool_name="get_doc_bundle",
                    tool_call_id="call-2",
                    content={
                        "bundle": {
                            "doc": {"doc_id": 42, "title": "Agent Memory"},
                            "summary": {"text": "retrieval memory loops"},
                        }
                    },
                )
            ]
        ),
    ]

    trace = rag_agent._extract_raw_tool_trace(messages)

    assert trace["status"] == "captured"
    assert trace["tool_calls_total"] == 2
    assert trace["events_total"] == 4
    assert trace["events_truncated"] is False
    assert [event["kind"] for event in trace["events"]] == [
        "tool-call",
        "tool-return",
        "tool-call",
        "tool-return",
    ]
    assert trace["events"][0]["tool_name"] == "search_hybrid"
    assert trace["events"][0]["args"] == {
        "query": "agent memory loops",
        "doc_type": "item",
    }
    assert trace["events"][1]["content"]["returned"] == 1
    assert trace["events"][3]["content"]["bundle"]["doc"]["doc_id"] == 42


def test_extract_raw_tool_trace_marks_unavailable_without_messages() -> None:
    trace = rag_agent._extract_raw_tool_trace([])

    assert trace["status"] == "unavailable"
    assert trace["events"] == []
    assert trace["tool_calls_total"] == 0
