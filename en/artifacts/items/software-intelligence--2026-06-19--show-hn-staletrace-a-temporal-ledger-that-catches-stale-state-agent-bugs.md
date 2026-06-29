---
source: hn
url: https://stale-trace.vercel.app/
published_at: '2026-06-19T23:03:36'
authors:
- zahraarman
topics:
- agent-debugging
- temporal-ledger
- code-intelligence
- production-agents
- human-ai-interaction
relevance_score: 0.67
run_id: materialize-outputs
language_code: en
---

# Show HN: StaleTrace – A temporal ledger that catches stale-state agent bugs

## Summary
StaleTrace is a deterministic incident-debugging tool for agents that finds when an agent used stale, conflicting, or invalid state. It builds a temporal ledger from existing tool calls and fact events, then writes a plain-language incident report.

## Problem
- Agent failures in production can come from facts changing after the agent observed them, such as an account closing or a customer record changing.
- Teams need to know what was true when the agent acted, because current database state can hide the cause of a past failure.
- The target pain is auditability for production agents without asking another LLM to judge the failure.

## Approach
- The system ingests agent tool calls and fact events already recorded by the user's systems.
- It replays fact events into ValidMemory, a temporal fact ledger where each value has a validity window.
- It compares the facts the agent used with the facts valid at that time.
- It flags stale facts, conflicting facts, and closed-account state, then generates a root cause, blast radius, and copyable incident report.

## Results
- The excerpt gives no benchmark, dataset, accuracy, latency, or production-volume numbers.
- It claims 0 LLM calls for auditing, 0 embeddings, and no graph database.
- It claims deterministic outputs: the same inputs produce the same verdict.
- It claims report generation for 1 reconstructed example, customer_123, but does not show a measured comparison against traces, logs, or LLM-based evaluators.
- The only time number in the excerpt is a 20-minute walkthrough offer, which is sales process detail, not a technical result.

## Link
- [https://stale-trace.vercel.app/](https://stale-trace.vercel.app/)
