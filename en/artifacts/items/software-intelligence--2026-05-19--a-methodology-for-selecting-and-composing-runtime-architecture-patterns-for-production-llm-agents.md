---
source: arxiv
url: https://arxiv.org/abs/2605.20173v1
published_at: '2026-05-19T17:54:21'
authors:
- Vasundra Srinivasan
topics:
- llm-agents
- runtime-architecture
- multi-agent-systems
- software-engineering
- agent-reliability
- human-ai-interaction
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# A Methodology for Selecting and Composing Runtime Architecture Patterns for Production LLM Agents

## Summary
The paper argues that production LLM agents need an explicit contract between model output and system action. It names that contract the stochastic-deterministic boundary and gives a pattern-selection method for runtime architecture.

## Problem
- Production LLM agents often fail at the point where a model proposal becomes a database write, tool call, or external side effect.
- These failures matter because better models reduce per-call variance, but they do not decide state ownership, retries, gates, durable commits, or human approval.
- Teams already add checks and commits around agent actions, but the paper says they lack a shared contract for designing and reviewing that boundary.

## Approach
- The core mechanism is the stochastic-deterministic boundary: the LLM proposes an action, deterministic code verifies it, the system commits accepted actions durably, and a typed reject signal goes back to the LLM when verification fails.
- The paper groups runtime design into 3 concerns: Coordination, State, and Control.
- It defines 6 runtime patterns: Hierarchical Delegation, Scatter-Gather plus Saga, Event-Driven Sequencing, Shared State Machine, Supervisor plus Gate, and Human in the Loop.
- It gives a 5-step selection method: classify the runtime, choose the state spine, add coordination, add control, then record the decision.
- It adds a diagnostic procedure for production failures, including replay divergence, where replaying the same event log through a changed LLM or prompt produces different downstream events.

## Results
- An audit of 5 open-source agent projects found explicit verifier-and-commit logic at 19 of 21 LLM-to-action call sites.
- A classification of 21 published agent failure post-mortems found 15 of 21 cases, or 71.4%, localized to weaknesses at the boundary.
- The same classification found 17 of 21 fixes, or 81%, strengthened verification, commit semantics, or reject signaling.
- One cited Promptfoo case reported a 23-point drop in prompt-injection resistance after a model change, from 94% with GPT-4o to 71% with GPT-4.1; the fix added an output classifier and stricter tool gating.
- The paper applies the method to 5 workloads and builds 1 runnable reference implementation using the public IBM Telco Customer Churn dataset.
- It does not report a benchmark gain in accuracy, latency, cost, or incident reduction for deployed production systems.

## Link
- [https://arxiv.org/abs/2605.20173v1](https://arxiv.org/abs/2605.20173v1)
