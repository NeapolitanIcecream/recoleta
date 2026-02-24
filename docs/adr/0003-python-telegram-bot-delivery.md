# ADR 0003: python-telegram-bot for Delivery

## Status
Accepted

## Context
Recoleta delivers a small number of curated insights to Telegram. Delivery must be async-friendly, handle flood limits, and provide robust error handling.

## Decision
Use `python-telegram-bot` as the Telegram Bot API client, leveraging its async API and rate limiting patterns.

## Consequences
- Reliable sending with configurable throttling and retries.
- Clear error handling hooks for observability.
- Delivery idempotency is enforced by recording message state in SQLite.

