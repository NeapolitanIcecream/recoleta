from __future__ import annotations

import importlib


rag_agent = importlib.import_module("recoleta.rag.agent")


def test_trend_agent_tools_expose_descriptions_and_hybrid_search() -> None:
    agent = rag_agent.build_trend_agent(llm_model="openai/gpt-4o-mini")

    tool_defs = agent._function_toolset.tools

    assert "search_hybrid" in tool_defs
    for tool_name in (
        "list_docs",
        "get_doc",
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
