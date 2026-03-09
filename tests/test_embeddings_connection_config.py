from __future__ import annotations

from typing import Any

from recoleta.llm_connection import LLMConnectionConfig
from recoleta.rag.embeddings import LiteLLMEmbedder


def test_embedder_passes_recoleta_llm_connection_overrides(
    monkeypatch,
) -> None:
    """Regression: dedicated Recoleta LLM envs must flow into embedding calls."""

    captured_kwargs: dict[str, Any] = {}

    def fake_embedding(**kwargs: Any) -> dict[str, Any]:
        nonlocal captured_kwargs
        captured_kwargs = kwargs
        return {
            "data": [{"embedding": [0.1, 0.2, 0.3]}],
            "usage": {"prompt_tokens": 3, "total_tokens": 3},
        }

    monkeypatch.setattr("recoleta.rag.embeddings._embedding", fake_embedding)
    embedder = LiteLLMEmbedder(
        llm_connection=LLMConnectionConfig(
            api_key="sk-recoleta-test",
            base_url="http://llm.local/v1",
        )
    )

    vectors, debug = embedder.embed(
        model="text-embedding-3-small",
        inputs=["agents"],
    )

    assert vectors == [[0.1, 0.2, 0.3]]
    assert captured_kwargs["api_key"] == "sk-recoleta-test"
    assert captured_kwargs["api_base"] == "http://llm.local/v1"
    assert debug["connection_overrides"] == {
        "api_key_configured": True,
        "base_url": "http://llm.local/v1",
    }
