---
source: arxiv
url: https://arxiv.org/abs/2605.06445v1
published_at: '2026-05-07T15:44:40'
authors:
- Francesco Dente
- Dario Satriani
- Paolo Papotti
topics:
- software-foundation-models
- code-intelligence
- backend-code-generation
- llm-agents
- software-benchmarks
- multi-agent-software-engineering
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Constraint Decay: The Fragility of LLM Agents in Backend Code Generation

## Summary
The paper shows that LLM coding agents fail much more often when backend code must obey database, ORM, and architecture requirements. The main result is a measured “constraint decay” effect: capable agents lose about 30 percentage points in assertion pass rate from loose tasks to fully specified tasks.

## Problem
- Production backends must match an API contract and also follow structural rules, including layered code, a chosen database, and a required ORM.
- Many code-generation benchmarks reward working behavior while ignoring whether the code fits these structural rules.
- This matters for software engineering agents because a generated service can pass simple functional checks yet still be hard to maintain, integrate, or deploy.

## Approach
- The authors fix one OpenAPI 3.0 contract based on the RealWorld Conduit API: 19 endpoints across articles, comments, users, profiles, and tags.
- They create 80 greenfield backend-generation tasks across 8 web frameworks: Flask, FastAPI, Django, aiohttp, Express, Fastify, Hono, and Koa.
- They vary structural constraints across levels L0 to L3: web framework only, then Clean Architecture, SQLite or PostgreSQL, and ORM use with SQLAlchemy or Sequelize.
- They evaluate generated services with a shared HTTP behavioral suite of 32 requests and 291 assertions, then check structural compliance with static verifiers for architecture, database, and ORM use.
- They test Mini-SWE-Agent and OpenHands with models including GPT-5-mini, GPT-5.2, Qwen3-Coder-Next, Qwen3-235B-A22B, MiniMax-M2.5, and Kimi-K2.5.

## Results
- Across capable configurations with L0 A% above 50, assertion pass rate drops by about 30 percentage points from L0 to L3, a 40% relative loss from baseline performance.
- OpenHands + Qwen3-Coder-Next has the largest reported drop: 73.0 A% at L0 to 27.6 A% at L3, down 45.5 points. OpenHands + MiniMax-M2.5 is the strongest reported L3 configuration: 78.6 A% at L3, but only 8.3% pass@1.
- Database requirements cause the largest marginal losses: PostgreSQL costs 19.3 ± 2.5 A% points and SQLite costs 14.3 ± 2.5 points. Clean Architecture costs 9.1 ± 1.6 points.
- ORM requirements add little marginal loss in the matched-pair analysis: SQLAlchemy costs 1.5 ± 2.1 A% points and Sequelize costs 0.6 ± 2.2 points.
- The paper reports that verifier enforcement changes any single A% score by at most 2.7 points, so the decay mainly comes from behavioral failures rather than static-check penalties.
- In 20 feature-implementation tasks on existing RealWorld repositories, pass@1 remains low: GPT-5.2 reaches 50.0% with Mini-SWE-Agent and 55.0% with OpenHands, while GPT-5-mini reaches 15.0% and 48.3% respectively.

## Link
- [https://arxiv.org/abs/2605.06445v1](https://arxiv.org/abs/2605.06445v1)
