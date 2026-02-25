# ADR 0006: Configurable LLM Output Language

## Status
Accepted

## Context
Recoleta produces user-facing `summary`, `insight`, and `idea_directions` fields via LLM, but language is currently implicit and not configurable.

## Decision
Add optional `LLM_OUTPUT_LANGUAGE` (`llm_output_language`) to typed settings and inject it into the analyzer system message. Keep JSON keys in English and keep `topics` as concise English tags.

## Consequences
Users can choose output language without changing model or prompt templates manually. Existing schema validation and publish filtering behavior remain stable.
