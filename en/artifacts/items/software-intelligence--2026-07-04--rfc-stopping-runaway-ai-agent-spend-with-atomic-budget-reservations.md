---
source: hn
url: https://github.com/iamapsrajput/agent-budget-protocol/blob/main/RFC.md
published_at: '2026-07-04T22:42:00'
authors:
- iamapsrajput
topics:
- agent-budgeting
- llm-gateway
- cost-control
- agent-runtime
- software-agents
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# RFC: Stopping runaway AI agent spend with atomic budget reservations

## Summary
This RFC proposes a run-scoped budget authority for AI agents that reserves estimated LLM spend before each provider call. It targets runaway costs caused by agent loops that resend growing context and make many calls in one session.

## Problem
- Agent runs can grow cost fast because each loop may resend accumulated context; the excerpt says a call can exceed 50K input tokens by step 20.
- Existing gateway budgets usually attach to API keys, users, or teams over days or months, while one agent run can burn the quota in hours.
- Current budget failures often give agents opaque errors, so agents cannot switch to cheaper models, shorten context, or stop cleanly.

## Approach
- Add a budget-decision plane as a gateway hook, sidecar, or SDK middleware.
- Before a provider call, compute an estimated worst-case cost from actual input tokens, effective max output tokens, and a versioned price table.
- Atomically reserve that estimate across all applicable scopes, such as run, user, team, key, and feature, using one Redis Lua script or one SQL transaction.
- After the call, commit actual usage and release unused reserve; on provider failure, release the reserve; on missing results, expire and reconcile it later.
- Return budget state through headers and RFC 9457 problem-detail errors, including allowed alternatives that meet tool, JSON, context, modality, and tenant policy needs.

## Results
- The RFC reports motivating cost incidents rather than new experiments: one developer was reported to hit $4,200 in API fees over one weekend, and a 35-engineer team was reported to receive an $87K monthly bill.
- It cites one audit of 30 teams with a 20x spread between p10 and p90 per-developer cost for the same tooling; the excerpt says these came from industry writeups rather than primary incident reports.
- In hard-gate mode, it claims no request is forwarded unless estimated spend has been reserved against every applicable ceiling, closing the race where 10 parallel calls each see remaining budget and all pass.
- v1 scope includes enforceable ceilings for run, user, and key; feature and team are attribution tags in v1, with enforceable feature/team ceilings after v1.
- It gives no benchmark results for latency, throughput, false blocks, cost savings, or production adoption.

## Link
- [https://github.com/iamapsrajput/agent-budget-protocol/blob/main/RFC.md](https://github.com/iamapsrajput/agent-budget-protocol/blob/main/RFC.md)
