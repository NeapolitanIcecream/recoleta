---
source: hn
url: https://github.com/mirkofr/FERNme
published_at: '2026-06-20T23:34:03'
authors:
- mirkofr
topics:
- agent-memory
- user-owned-data
- hebbian-learning
- human-ai-interaction
- action-based-personalization
- ai-agents
relevance_score: 0.68
run_id: materialize-outputs
language_code: en
---

# Show HN: FERNme – agent memory that updates with ~zero LLM calls

## Summary
FERNme is a user-owned memory layer for AI agents that updates user preference graphs with little or no LLM use. The strongest evidence is synthetic or LLM-authored, so the claim is about a tested mechanism rather than proven behavior with real users.

## Problem
- Many agent memory systems use an LLM on each turn to write memory, which raises cost and can add extraction errors.
- The project targets action-driven agents, such as shopping, support, booking, tutoring, healthcare, and government sites, where memory should improve outcomes rather than answer memory questions.
- It also addresses user control: users can inspect, edit, export, and delete what the system remembers.

## Approach
- Each user has a sparse per-site graph with weighted 0-9 edges connecting users, preferences, topics, goals, and contexts.
- New events update the graph with a Hebbian co-occurrence rule: connected attributes strengthen after useful behavior, weaken after poor outcomes, and decay over time.
- Retrieval uses spreading activation over the graph, then produces a bounded memory card of about 25 tokens for the agent prompt.
- A population prior helps cold start, and the stored card keeps deviations from that prior instead of repeating common preferences.
- LLM use is optional: the hot write path uses deterministic mapping, while gated LLM tagging only runs when deterministic mapping cannot handle novel free text.

## Results
- The repository reports 88 tests covering the engine, SQLite and Postgres stores, supernode and sign-in, triggers, safety, REST and MCP interfaces, UI views, and evaluation scripts.
- In a cold-start ablation, the population prior adds +0.06 precision@5 during turns 1-3 and fades by turn 10.
- In a synthetic simulated storefront pilot, FERNme reports a +16% relative conversion lift over a popularity baseline; it ties at visit 1 and improves as user behavior accumulates.
- In the cost and quality Pareto analysis, FERNme plus gated or offline LLM modes is reported at about 80-90% of the modeled LLM-ceiling quality with 1-2 orders of magnitude lower cost per 1,000 interactions.
- Recall quality experiments use 5 seeds × 40 users and compare precision@5 against ground-truth preferences; the excerpt gives the setup but not exact precision values.
- The Mem0 LLM head-to-head has not been run, and the author states that the main numbers come from synthetic or LLM-authored data rather than real users.

## Link
- [https://github.com/mirkofr/FERNme](https://github.com/mirkofr/FERNme)
