from __future__ import annotations

import json
from typing import Any

import pytest

from recoleta.analyzer import LiteLLMAnalyzer


def _mock_response_content() -> str:
    return json.dumps(
        {
            "summary": (
                "## Summary\n"
                "Short summary.\n\n"
                "## Problem\n"
                "- Hard setup.\n\n"
                "## Approach\n"
                "- Use a structured agent.\n\n"
                "## Results\n"
                "- +12% on eval.\n"
            ),
            "topics": ["agents", "llm"],
            "relevance_score": 0.9,
            "novelty_score": 0.4,
        }
    )


def test_analyzer_system_message_includes_output_language(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured_messages: list[dict[str, str]] = []

    def fake_completion(**kwargs: Any) -> dict[str, Any]:
        nonlocal captured_messages
        captured_messages = kwargs["messages"]
        return {"choices": [{"message": {"content": _mock_response_content()}}]}

    monkeypatch.setattr("recoleta.analyzer.completion", fake_completion)
    analyzer = LiteLLMAnalyzer(
        model="openai/gpt-4o-mini", output_language="Chinese (Simplified)"
    )

    result, debug = analyzer.analyze(
        title="Sample title",
        canonical_url="https://example.com/paper",
        user_topics=["agents"],
        content="Sample content",
        include_debug=True,
    )

    assert result.summary.startswith("## Summary")
    assert debug is not None
    system_message = captured_messages[0]["content"]
    user_message = captured_messages[1]["content"]
    assert "Use Chinese (Simplified) for the summary value." in system_message
    assert (
        "Keep all JSON keys in English and keep topics as concise English tags."
        in system_message
    )
    assert "## Summary" in user_message
    assert "## Problem" in user_message
    assert "## Approach" in user_message
    assert "## Results" in user_message


def test_analyzer_system_message_defaults_when_output_language_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
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

    assert result.summary.startswith("## Summary")
    assert (
        captured_messages[0]["content"]
        == "You are a research signal analyst. Return strict JSON only."
    )


def test_analyzer_uses_model_default_temperature_gh_gpt52(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Regression: LiteLLM gpt-5.2 rejects explicit temperature params."""

    captured_kwargs: dict[str, Any] = {}

    def fake_completion(**kwargs: Any) -> dict[str, Any]:
        nonlocal captured_kwargs
        captured_kwargs = kwargs
        return {"choices": [{"message": {"content": _mock_response_content()}}]}

    monkeypatch.setattr("recoleta.analyzer.completion", fake_completion)
    analyzer = LiteLLMAnalyzer(model="openai/gpt-5.2")

    result, debug = analyzer.analyze(
        title="Sample title",
        canonical_url="https://example.com/paper",
        user_topics=["agents"],
        content="Sample content",
        include_debug=True,
    )

    assert result.summary.startswith("## Summary")
    assert "temperature" not in captured_kwargs
    assert debug is not None
    assert "temperature" not in debug.request
