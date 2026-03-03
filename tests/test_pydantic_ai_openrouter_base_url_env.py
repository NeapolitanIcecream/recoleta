from __future__ import annotations

import pytest
from pydantic_ai.models.openrouter import OpenRouterModel

from recoleta.rag.pydantic_ai_model import build_pydantic_ai_model


def test_build_pydantic_ai_model_openrouter_respects_env_base_url(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-openrouter-key")
    monkeypatch.delenv("OPENROUTER_BASE_URL", raising=False)
    monkeypatch.setenv("OPENROUTER_API_BASE", "http://openrouter.local/api/v1/")

    model = build_pydantic_ai_model("openrouter/anthropic/claude-3-5-sonnet")
    assert isinstance(model, OpenRouterModel)
    assert str(model.base_url).rstrip("/") == "http://openrouter.local/api/v1"


def test_build_pydantic_ai_model_openrouter_accepts_colon_format(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-openrouter-key")
    monkeypatch.delenv("OPENROUTER_API_BASE", raising=False)
    monkeypatch.setenv("OPENROUTER_BASE_URL", "http://openrouter.alt/api/v1")

    model = build_pydantic_ai_model("openrouter:anthropic/claude-3-5-sonnet")
    assert isinstance(model, OpenRouterModel)
    assert str(model.base_url).rstrip("/") == "http://openrouter.alt/api/v1"


def test_build_pydantic_ai_model_normalizes_non_openrouter_models() -> None:
    model = build_pydantic_ai_model("openai/gpt-4o-mini")
    assert model == "openai:gpt-4o-mini"
