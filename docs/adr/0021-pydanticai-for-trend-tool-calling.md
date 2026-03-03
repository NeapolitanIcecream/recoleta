---
title: "ADR 0021: PydanticAI for trend tool-calling"
status: Accepted
---

## Context
Recoleta trend generation needs reliable tool calling over a local corpus and strict, typed outputs suitable for persistence and publishing.

## Decision
Use **PydanticAI** as the trend agent framework, with tools wrapping existing `Repository` methods and a Pydantic `TrendPayload` as the agent output type.

## Consequences
Tool schemas and the tool-call loop are no longer hand-rolled in `trends.py`. Agent outputs are validated at the boundary, reducing JSON glue code and improving correctness. Testing can override the agent model to avoid network calls.

