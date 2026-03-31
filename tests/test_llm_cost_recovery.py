from __future__ import annotations

import json
from typing import Any

import pytest
from litellm.cost_calculator import completion_cost, cost_per_token

import recoleta.analyzer as analyzer_module
import recoleta.cli.maintenance as maintenance_cli
import recoleta.translation as translation_module
from recoleta.analyzer import LiteLLMAnalyzer


def _analysis_response_content() -> str:
    return json.dumps(
        {
            "summary": "Short summary",
            "topics": ["agents", "llm"],
            "relevance_score": 0.9,
            "novelty_score": 0.4,
        }
    )


def _translation_response_content() -> str:
    return json.dumps({"summary": "## Summary\n\nTranslated summary.\n"})


def _litellm_like_response(
    *,
    content: str,
    prompt_tokens: int = 15,
    completion_tokens: int = 12,
    resolved_model: str = "openai/gpt-5.4-20260305",
    measured_cost_usd: float | None = None,
) -> dict[str, Any]:
    usage: dict[str, Any] = {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": prompt_tokens + completion_tokens,
    }
    if measured_cost_usd is not None:
        usage["cost"] = measured_cost_usd
        usage["cost_details"] = {"upstream_inference_cost": measured_cost_usd}
    return {
        "model": resolved_model,
        "choices": [{"message": {"content": content}}],
        "usage": usage,
        "_hidden_params": {"response_cost": None},
    }


def _expected_cost_usd(*, model: str, prompt_tokens: int, completion_tokens: int) -> float:
    prompt_cost, completion_cost_usd = cost_per_token(
        model=model,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
    )
    return float(prompt_cost) + float(completion_cost_usd)


def _expected_response_cost_usd(*, response: dict[str, Any], model: str) -> float:
    return float(completion_cost(completion_response=response, model=model))


class _FakeSettings:
    def __init__(
        self,
        *,
        llm_model: str = "openai/openai/gpt-5.4",
        llm_api_key: str = "sk-recoleta-test",
        llm_base_url: str = "http://llm.local/v1",
    ) -> None:
        self.llm_model = llm_model
        self.llm_api_key = llm_api_key
        self.llm_base_url = llm_base_url


def test_analyzer_prefers_measured_usage_cost_when_hidden_cost_is_missing_gh_w12(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Regression: analyze billing dropped provider-reported usage.cost values."""

    measured_cost_usd = 0.1234

    def fake_completion(**_kwargs: Any) -> dict[str, Any]:
        return _litellm_like_response(
            content=_analysis_response_content(),
            measured_cost_usd=measured_cost_usd,
        )

    monkeypatch.setattr("recoleta.analyzer.completion", fake_completion)
    analyzer = LiteLLMAnalyzer(model="openai/openai/gpt-5.4")

    result, debug = analyzer.analyze(
        title="Sample title",
        canonical_url="https://example.com/paper",
        user_topics=["agents"],
        content="Sample content",
        include_debug=True,
    )

    assert result.cost_usd == measured_cost_usd
    assert debug is not None
    assert debug.response["usage"]["cost"] == measured_cost_usd


def test_analyzer_estimates_cost_from_configured_model_when_response_model_is_unmapped_gh_w12(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Regression: analyze billing must recover from dated resolved models."""

    prompt_tokens = 15
    completion_tokens = 12

    def fake_completion(**_kwargs: Any) -> dict[str, Any]:
        return _litellm_like_response(
            content=_analysis_response_content(),
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            measured_cost_usd=None,
        )

    monkeypatch.setattr("recoleta.analyzer.completion", fake_completion)
    analyzer = LiteLLMAnalyzer(model="openai/openai/gpt-5.4")

    result, _ = analyzer.analyze(
        title="Sample title",
        canonical_url="https://example.com/paper",
        user_topics=["agents"],
        content="Sample content",
        include_debug=False,
    )

    assert result.cost_usd == _expected_cost_usd(
        model="openai/gpt-5.4",
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
    )


def test_translation_recovers_measured_usage_cost_from_litellm_response_gh_w12(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Regression: translation billing must not discard usage.cost values."""

    measured_cost_usd = 0.0456

    def fake_completion(**_kwargs: Any) -> dict[str, Any]:
        return _litellm_like_response(
            content=_translation_response_content(),
            measured_cost_usd=measured_cost_usd,
        )

    monkeypatch.setattr(translation_module, "_get_completion", lambda: fake_completion)

    result = translation_module.translate_structured_payload(
        model="openai/openai/gpt-5.4",
        source_kind="analysis",
        payload={"summary": "## Summary\n\nSource summary.\n"},
        source_language_code="en",
        target_language_code="zh-CN",
        payload_model=None,
        return_debug=True,
    )
    assert isinstance(result, tuple)
    translated_payload, debug = result

    assert translated_payload["summary"] == "## Summary\n\nTranslated summary.\n"
    assert debug["estimated_cost_usd"] == measured_cost_usd
    assert debug["usage"]["cost"] == measured_cost_usd


def test_analyzer_preserves_cached_prompt_pricing_in_fallback_estimate_gh_w12(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Regression: fallback pricing must respect cached prompt token discounts."""

    prompt_tokens = 1000
    completion_tokens = 100
    response = _litellm_like_response(
        content=_analysis_response_content(),
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        measured_cost_usd=None,
    )
    response["usage"]["prompt_tokens_details"] = {"cached_tokens": 900}

    def fake_completion(**_kwargs: Any) -> dict[str, Any]:
        return response

    monkeypatch.setattr("recoleta.analyzer.completion", fake_completion)
    analyzer = LiteLLMAnalyzer(model="openai/openai/gpt-5.4")

    result, _ = analyzer.analyze(
        title="Sample title",
        canonical_url="https://example.com/paper",
        user_topics=["agents"],
        content="Sample content",
        include_debug=False,
    )

    assert result.cost_usd == _expected_response_cost_usd(
        response=response,
        model="openai/gpt-5.4",
    )


def test_doctor_ping_estimates_cost_when_provider_omits_measured_cost_gh_w12(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Regression: doctor ping billing must estimate cost from configured model."""

    prompt_tokens = 15
    completion_tokens = 12

    def fake_completion(**_kwargs: Any) -> dict[str, Any]:
        return _litellm_like_response(
            content="pong",
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            measured_cost_usd=None,
        )

    monkeypatch.setattr(analyzer_module, "completion", fake_completion)
    settings = _FakeSettings()

    payload = maintenance_cli._run_llm_ping(settings=settings, timeout_seconds=12)

    assert payload["status"] == "ok"
    assert payload["resolved_model"] == "openai/gpt-5.4-20260305"
    assert payload["cost_usd"] == _expected_cost_usd(
        model="openai/gpt-5.4",
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
    )
    assert payload["usage"]["prompt_tokens"] == prompt_tokens
    assert payload["usage"]["completion_tokens"] == completion_tokens
