# ADR 0002: LiteLLM as LLM Abstraction

## Status
Accepted

## Context
Recoleta needs to call multiple LLM providers with consistent request/response shapes, structured outputs, and retry/fallback without rewriting business logic per provider.

## Decision
Adopt LiteLLM as the unified LLM invocation layer using an OpenAI-compatible interface and structured output (`response_format`) validated by Pydantic.

## Consequences
- Provider switches become configuration changes instead of code changes.
- Easier to implement retries, budgets, and consistent telemetry.
- Must be careful to scrub secrets in any debug artifacts.

