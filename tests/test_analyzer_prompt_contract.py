from __future__ import annotations

from typing import Any

import pytest

from recoleta.analyzer import LiteLLMAnalyzer


def test_analyzer_prompt_requires_reframe_insight_and_broad_directions() -> None:
    prompt = LiteLLMAnalyzer._build_prompt(
        title="Sample title",
        canonical_url="https://example.com/paper",
        user_topics=["agents", "ml-systems"],
        content="Sample content",
        content_max_chars=5000,
    )

    assert "It reframes <X> from <A> to <B>" in prompt
    assert "NEW VIEWPOINT" in prompt
    assert "BROAD, GENERALIZABLE" in prompt
    assert "broader LLM scope" in prompt
    assert "Opportunity:" in prompt
    assert "Why now:" in prompt
    assert "Example bet:" in prompt
    assert "lower-kebab-case" in prompt


def test_analyzer_prompt_truncates_content_excerpt_when_over_limit() -> None:
    long_content = "x" * 100
    prompt = LiteLLMAnalyzer._build_prompt(
        title="Sample title",
        canonical_url="https://example.com/paper",
        user_topics=["agents"],
        content=long_content,
        content_max_chars=10,
    )

    assert "Content excerpt:" in prompt
    assert "...[truncated]..." in prompt


def test_analyzer_passes_prompt_to_llm_as_user_message(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured_messages: list[dict[str, str]] = []

    def fake_completion(**kwargs: Any) -> dict[str, Any]:
        nonlocal captured_messages
        captured_messages = kwargs["messages"]
        return {
            "choices": [
                {
                    "message": {
                        "content": (
                            '{"summary":"s","insight":"i","idea_directions":["d"],'
                            '"topics":["tool-use-agents"],"relevance_score":0.5,"novelty_score":0.5}'
                        )
                    }
                }
            ]
        }

    monkeypatch.setattr("recoleta.analyzer.completion", fake_completion)
    analyzer = LiteLLMAnalyzer(model="openai/gpt-4o-mini")

    analyzer.analyze(
        title="Sample title",
        canonical_url="https://example.com/paper",
        user_topics=["agents"],
        content="Sample content",
    )

    assert len(captured_messages) == 2
    assert captured_messages[1]["role"] == "user"
    assert "It reframes <X> from <A> to <B>" in captured_messages[1]["content"]
