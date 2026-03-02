---
title: Insight and idea_directions contract
status: accepted
date: 2026-03-02
---

## Context
Users want Insight to be a readable viewpoint shift, and Ideas to be broad, generalizable directions (not paper-specific follow-ups).

## Decision
Enforce a prompt-level contract:
- `insight` must use an explicit "reframes X from A to B" thesis and include a broader implication.
- `idea_directions` must be structured as "Opportunity | Why now | Example bet" and focus on broader LLM scope directions.

## Consequences
Outputs become less nerdy and more actionable for downstream triage; publish rendering can format structured ideas without changing the stored schema.

