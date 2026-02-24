# ADR 0005: Optional Config File Settings Source

## Status
Accepted

## Context
Recoleta needs typed settings from environment variables, but some non-secret configuration is easier to manage in a file. Secrets must remain env-only.

## Decision
Support an optional YAML/JSON config file via `RECOLETA_CONFIG_PATH`. Load precedence is: init args > env vars > config file > defaults. Reject `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in the config file.

## Consequences
Users can store non-secret settings in a local config file while keeping secrets in env. Invalid or missing config files fail fast to avoid silent misconfiguration.

