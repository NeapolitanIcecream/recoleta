from __future__ import annotations

from dataclasses import dataclass
from typing import Any


def _normalize_optional_value(value: Any) -> str | None:
    if value is None:
        return None
    normalized = str(value).strip()
    return normalized or None


def _extract_secret_value(value: Any) -> str | None:
    if value is None:
        return None
    getter = getattr(value, "get_secret_value", None)
    if callable(getter):
        try:
            return _normalize_optional_value(getter())
        except Exception:
            return None
    return _normalize_optional_value(value)


@dataclass(frozen=True, slots=True)
class LLMConnectionConfig:
    api_key: str | None = None
    base_url: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "api_key", _normalize_optional_value(self.api_key))
        object.__setattr__(self, "base_url", _normalize_optional_value(self.base_url))

    def litellm_completion_kwargs(self) -> dict[str, Any]:
        kwargs: dict[str, Any] = {}
        if self.api_key is not None:
            kwargs["api_key"] = self.api_key
        if self.base_url is not None:
            kwargs["base_url"] = self.base_url
        return kwargs

    def litellm_embedding_kwargs(self) -> dict[str, Any]:
        kwargs: dict[str, Any] = {}
        if self.api_key is not None:
            kwargs["api_key"] = self.api_key
        if self.base_url is not None:
            kwargs["api_base"] = self.base_url
        return kwargs

    def pydantic_ai_provider_kwargs(self) -> dict[str, str]:
        kwargs: dict[str, str] = {}
        if self.api_key is not None:
            kwargs["api_key"] = self.api_key
        if self.base_url is not None:
            kwargs["base_url"] = self.base_url
        return kwargs

    def debug_payload(self) -> dict[str, Any]:
        if self.api_key is None and self.base_url is None:
            return {}
        payload: dict[str, Any] = {
            "api_key_configured": self.api_key is not None,
        }
        if self.base_url is not None:
            payload["base_url"] = self.base_url
        return payload


def llm_connection_from_settings(settings: Any) -> LLMConnectionConfig:
    return LLMConnectionConfig(
        api_key=_extract_secret_value(getattr(settings, "llm_api_key", None)),
        base_url=_normalize_optional_value(getattr(settings, "llm_base_url", None)),
    )
