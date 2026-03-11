from __future__ import annotations

import json
from typing import Any

import pytest

from recoleta.analyzer import LiteLLMAnalyzer
from recoleta.item_summary import normalize_item_summary_markdown
from recoleta.llm_connection import LLMConnectionConfig


def _mock_response_content() -> str:
    return json.dumps(
        {
            "summary": "Short summary",
            "topics": ["agents", "llm"],
            "relevance_score": 0.9,
            "novelty_score": 0.4,
        }
    )


def test_analyzer_passes_recoleta_llm_connection_overrides(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Regression: dedicated Recoleta LLM envs must flow into LiteLLM calls."""

    captured_kwargs: dict[str, Any] = {}

    def fake_completion(**kwargs: Any) -> dict[str, Any]:
        nonlocal captured_kwargs
        captured_kwargs = kwargs
        return {"choices": [{"message": {"content": _mock_response_content()}}]}

    monkeypatch.setattr("recoleta.analyzer.completion", fake_completion)
    analyzer = LiteLLMAnalyzer(
        model="openai/gpt-4o-mini",
        llm_connection=LLMConnectionConfig(
            api_key="sk-recoleta-test",
            base_url="http://llm.local/v1",
        ),
    )

    result, debug = analyzer.analyze(
        title="Sample title",
        canonical_url="https://example.com/paper",
        user_topics=["agents"],
        content="Sample content",
        include_debug=True,
    )

    assert result.summary == normalize_item_summary_markdown("Short summary")
    assert captured_kwargs["api_key"] == "sk-recoleta-test"
    assert captured_kwargs["base_url"] == "http://llm.local/v1"
    assert debug is not None
    assert debug.request["connection_overrides"] == {
        "api_key_configured": True,
        "base_url": "http://llm.local/v1",
    }
