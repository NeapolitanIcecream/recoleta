# ADR 0007: Local Markdown as Default Output

## Decision

Recoleta publishes user-facing results to a local Markdown directory by default (`PUBLISH_TARGETS=["markdown"]`).

## Rationale

- Keep the project usable without external integrations.
- Make outputs directly readable with any editor (`latest.md` + `Inbox/`).
- Preserve a simple mental model: publish targets are explicit and independently configurable.

## Consequences

- Obsidian and Telegram become optional and are only required when enabled in `PUBLISH_TARGETS`.
- `recoleta publish` fails fast if an enabled target is missing required configuration.
