from __future__ import annotations

import json
from typing import Any

import pytest

from recoleta.analyzer import LiteLLMAnalyzer


def _mock_response_content() -> str:
    return json.dumps(
        {
            "summary": "Short summary",
            "insight": "Useful insight",
            "idea_directions": ["Direction one", "Direction two"],
            "topics": ["agents", "llm"],
            "relevance_score": 0.9,
            "novelty_score": 0.4,
        }
    )


def test_analyzer_system_message_includes_output_language(monkeypatch: pytest.MonkeyPatch) -> None:
    captured_messages: list[dict[str, str]] = []

    def fake_completion(**kwargs: Any) -> dict[str, Any]:
        nonlocal captured_messages
        captured_messages = kwargs["messages"]
        return {"choices": [{"message": {"content": _mock_response_content()}}]}

    monkeypatch.setattr("recoleta.analyzer.completion", fake_completion)
    analyzer = LiteLLMAnalyzer(model="openai/gpt-4o-mini", output_language="Chinese (Simplified)")

    result, debug = analyzer.analyze(
        title="Sample title",
        canonical_url="https://example.com/paper",
        user_topics=["agents"],
        content="Sample content",
        include_debug=True,
    )

    assert result.summary == "Short summary"
    assert debug is not None
    system_message = captured_messages[0]["content"]
    assert "Use Chinese (Simplified) for summary, insight, and idea_directions values." in system_message
    assert "Keep all JSON keys in English and keep topics as concise English tags." in system_message


def test_analyzer_system_message_defaults_when_output_language_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    captured_messages: list[dict[str, str]] = []

    def fake_completion(**kwargs: Any) -> dict[str, Any]:
        nonlocal captured_messages
        captured_messages = kwargs["messages"]
        return {"choices": [{"message": {"content": _mock_response_content()}}]}

    monkeypatch.setattr("recoleta.analyzer.completion", fake_completion)
    analyzer = LiteLLMAnalyzer(model="openai/gpt-4o-mini")

    result, _ = analyzer.analyze(
        title="Sample title",
        canonical_url="https://example.com/paper",
        user_topics=["agents"],
        content="Sample content",
    )

    assert result.summary == "Short summary"
    assert captured_messages[0]["content"] == "You are a research signal analyst. Return strict JSON only."
