from __future__ import annotations

import os
from typing import Any


def _non_empty_env(*keys: str) -> str | None:
    for key in keys:
        value = os.getenv(key, "").strip()
        if value:
            return value
    return None


def normalize_pydantic_ai_model_id(llm_model: str) -> str:
    """Normalize a LiteLLM-style model name to PydanticAI's `provider:model` format.

    Recoleta config uses LiteLLM naming: `<provider>/<model>`.
    PydanticAI prefers: `<provider>:<model>`.
    """

    normalized = str(llm_model or "").strip()
    if not normalized:
        raise ValueError("llm_model must not be empty")
    if ":" in normalized:
        return normalized
    if "/" in normalized:
        provider, rest = normalized.split("/", 1)
        provider = provider.strip()
        rest = rest.strip()
        if provider and rest:
            return f"{provider}:{rest}"
    return normalized


def _split_provider(llm_model: str) -> tuple[str, str | None]:
    normalized = str(llm_model or "").strip()
    if not normalized:
        return "", None
    if ":" in normalized:
        provider, rest = normalized.split(":", 1)
        return provider.strip(), rest.strip() or None
    if "/" in normalized:
        provider, rest = normalized.split("/", 1)
        return provider.strip(), rest.strip() or None
    return "", None


def build_pydantic_ai_model(llm_model: str) -> Any:
    """Build a PydanticAI model (or model-id string) from Recoleta's LLM config.

    Design goal: keep PydanticAI on native providers, but ensure OpenRouter base URL
    is configurable via environment variables to match the rest of the project.
    """

    normalized = str(llm_model or "").strip()
    if not normalized:
        raise ValueError("llm_model must not be empty")

    provider, rest = _split_provider(normalized)
    if provider.lower() == "openrouter":
        if not rest:
            raise ValueError(
                "OpenRouter model must be in the form 'openrouter/<provider>/<model>'"
            )

        from pydantic_ai.models.openrouter import OpenRouterModel
        from pydantic_ai.providers.openrouter import OpenRouterProvider

        class _EnvOpenRouterProvider(OpenRouterProvider):
            @property
            def base_url(self) -> str:  # type: ignore[override]
                # Keep compatibility with common OpenRouter env names used in OpenAI-compatible stacks.
                env_url = _non_empty_env("OPENROUTER_API_BASE", "OPENROUTER_BASE_URL")
                if env_url:
                    return env_url.rstrip("/")
                return super().base_url

        return OpenRouterModel(rest, provider=_EnvOpenRouterProvider())

    return normalize_pydantic_ai_model_id(normalized)
