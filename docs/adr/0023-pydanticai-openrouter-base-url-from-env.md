# ADR 0023: PydanticAI OpenRouter base URL from env

## Status
Accepted

## Context
Recoleta configures OpenAI-compatible endpoints via environment variables (including OpenRouter).
PydanticAI's built-in OpenRouter provider uses a fixed base URL and does not follow env overrides.

## Decision
Keep PydanticAI on native models/providers, but wrap the OpenRouter provider so `OPENROUTER_API_BASE` / `OPENROUTER_BASE_URL` override the base URL.

## Consequences
Trend tool-calling inherits the same OpenRouter endpoint configuration without adding a custom LLM compatibility layer.

