from __future__ import annotations

import json
from typing import Any

import pytest
from litellm.exceptions import RateLimitError

from recoleta.analyzer import LiteLLMAnalyzer
from recoleta.item_summary import normalize_item_summary_markdown


def _valid_response_content() -> str:
    return json.dumps(
        {
            "summary": "Short summary",
            "topics": ["agents", "llm"],
            "relevance_score": 0.9,
            "novelty_score": 0.4,
        }
    )


def test_analyzer_retries_on_rate_limit_and_succeeds(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = 0

    def fake_completion(**_kwargs: Any) -> dict[str, Any]:
        nonlocal calls
        calls += 1
        if calls == 1:
            raise RateLimitError(
                "rate limited",
                llm_provider="openai",
                model="openai/gpt-4o-mini",
            )
        return {"choices": [{"message": {"content": _valid_response_content()}}]}

    monkeypatch.setattr("recoleta.analyzer.completion", fake_completion)
    monkeypatch.setattr("recoleta.analyzer._retry_sleep", lambda _s: None)

    analyzer = LiteLLMAnalyzer(model="openai/gpt-4o-mini")
    result, debug = analyzer.analyze(
        title="Sample title",
        canonical_url="https://example.com/paper",
        user_topics=["agents"],
        content="Sample content",
        include_debug=True,
    )

    assert calls == 2
    assert result.summary == normalize_item_summary_markdown("Short summary")
    assert debug is not None
    retry = debug.response.get("retry") or {}
    assert retry.get("attempts_total") == 2
    attempts = retry.get("attempts") or []
    assert len(attempts) == 1
    assert attempts[0]["error_type"] == "RateLimitError"


def test_analyzer_retries_on_invalid_json_and_succeeds(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = 0

    def fake_completion(**_kwargs: Any) -> dict[str, Any]:
        nonlocal calls
        calls += 1
        if calls == 1:
            return {"choices": [{"message": {"content": "not-json"}}]}
        return {"choices": [{"message": {"content": _valid_response_content()}}]}

    monkeypatch.setattr("recoleta.analyzer.completion", fake_completion)
    monkeypatch.setattr("recoleta.analyzer._retry_sleep", lambda _s: None)

    analyzer = LiteLLMAnalyzer(model="openai/gpt-4o-mini")
    result, debug = analyzer.analyze(
        title="Sample title",
        canonical_url="https://example.com/paper",
        user_topics=["agents"],
        content="Sample content",
        include_debug=True,
    )

    assert calls == 2
    assert result.summary == normalize_item_summary_markdown("Short summary")
    assert debug is not None
    retry = debug.response.get("retry") or {}
    assert retry.get("attempts_total") == 2
    attempts = retry.get("attempts") or []
    assert len(attempts) == 1
    assert attempts[0]["error_type"] == "_AnalyzeRetryableError"
