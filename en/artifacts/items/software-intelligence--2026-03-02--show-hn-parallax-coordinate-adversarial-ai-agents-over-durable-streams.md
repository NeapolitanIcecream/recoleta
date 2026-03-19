---
source: hn
url: https://github.com/s2-streamstore/parallax
published_at: '2026-03-02T23:04:19'
authors:
- infiniteregrets
topics:
- multi-agent-systems
- durable-streams
- agent-orchestration
- code-intelligence
- human-ai-collaboration
relevance_score: 0.89
run_id: materialize-outputs
language_code: en
---

# Show HN: Parallax – Coordinate adversarial AI agents over durable streams

## Summary
Parallax is a multi-agent research coordination prototype built on durable streams. Its core idea is to let multiple mutually isolated agent groups reason independently, then have a coordinator synthesize the results. It emphasizes “adversarial/parallel perspectives + resumable execution” for tasks such as research, analysis, and code auditing.

## Problem
- Many existing AI research tools essentially have **a single model play multiple perspectives within one shared context**, which can easily lead to perspective coupling, herd reasoning, and context contamination.
- If a multi-agent workflow lacks **durable, resumable, forkable execution infrastructure**, long-running tasks, human/multi-machine collaboration, and staged reasoning become fragile.
- This matters because in scenarios like research analysis, forecasting software decisions, and code auditing, **generating independent viewpoints first and summarizing later** often exposes disagreements and risks better than discussing directly in one shared context.

## Approach
- Parallax first uses a planner to generate a strategy JSON that defines the topology (such as groups, rounds, hierarchical), agent modes, and aggregation method.
- The executor creates multiple independent agent groups on **S2 durable streams** according to the strategy; each group reads only its own stream, and **groups are isolated during generation and cannot see each other’s content**.
- An autonomous moderator continuously reads outputs from each group, decides whether to redirect, create breakout streams, move to the next phase, or stop, and then performs the final synthesis.
- Agents are persistent sessions (Claude or Codex) that operate through bidirectional stream-json I/O; all state is stored in S2, so the system supports **crash-and-resume from the tail**.
- The system supports humans or other machines joining a specified swarm/group mid-process, and it can also assign different backend models and tool capabilities by group for workflows such as research, threat modeling, and code review.

## Results
- The text **does not provide formal benchmarks, controlled experiments, or quantitative evaluation results**, so there are no reportable accuracy, win-rate, cost, or throughput figures.
- The most specific capability claim given is that it can run an adversarial research workflow with **3 independent groups × 2 agents per group**, while maintaining inter-group isolation before synthesis.
- The examples also show a workflow with **5 independent panelists, 3 rounds of Delphi forecasting**, claiming that the moderator aggregates and feeds context back in so estimates “converge,” but no convergence metric or error data is provided.
- The system exposes several controllable boundary parameters, such as `--max-messages 15`, `--max-dynamic-streams 4`, `--max-phase-transitions 3`, and `--timeout 15`, indicating that its focus is on **orchestratable, resumable, constrained multi-agent execution** rather than a validated improvement in model performance.
- The author explicitly states that this is a **“vibecoded proof of concept”** and warns to “Expect rough edges,” indicating that the current contribution is more of a **system prototype and interaction mechanism** than a mature research result.

## Link
- [https://github.com/s2-streamstore/parallax](https://github.com/s2-streamstore/parallax)
