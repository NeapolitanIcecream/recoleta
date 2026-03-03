# LLM Output Language

This document defines how Recoleta controls the natural language used in LLM-generated content.

## Goals

- Let users configure the output language for `summary` and trend notes.
- Keep structured output schema stable so existing validation and storage continue to work.
- Avoid regressions in publish filtering based on `topics` tags.

## Non-goals

- Per-source or per-item language routing.
- Automatic language detection from item content.
- Translating historical analysis rows already stored in SQLite.

## Configuration

Recoleta supports one optional setting:

- `LLM_OUTPUT_LANGUAGE` / `llm_output_language` (default: unset)

Accepted sources:

- Environment variable: `LLM_OUTPUT_LANGUAGE`
- Config file (`RECOLETA_CONFIG_PATH`): either `LLM_OUTPUT_LANGUAGE` or `llm_output_language`

Validation rules:

- Trim surrounding whitespace.
- Empty value is treated as unset (`None`).
- Must be single-line.
- Max length: 64 characters.

## Prompt behavior

When `llm_output_language` is set, Recoleta appends language instructions in:

- the analyzer system message (for `summary`)
- the trend agent instructions (for trend note content)

- `summary` and trend note natural language fields should use the configured language.
- JSON keys must remain in English.
- `topics` should remain concise English tags.

When `llm_output_language` is unset, Recoleta keeps the existing system message behavior.

## Observability and safety

- LLM request debug artifacts already store the final `messages`, so effective language instruction is auditable.
- `Settings.safe_fingerprint()` automatically includes `llm_output_language`, so run fingerprints change when this setting changes.
- The single-line + length validation fails fast for malformed language strings and avoids prompt injection through multi-line config values.
