---
source: arxiv
url: http://arxiv.org/abs/2604.10352v1
published_at: '2026-04-11T21:38:15'
authors:
- Mofasshara Rafique
- Laurent Bindschaedler
topics:
- llm-agents
- agent-memory
- virtual-memory
- tool-using-agents
- code-intelligence
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# ClawVM: Harness-Managed Virtual Memory for Stateful Tool-Using LLM Agents

## Summary
ClawVM adds an OS-style virtual memory layer to the agent harness for stateful tool-using LLM agents. It aims to stop memory failures caused by compaction, reset, and unsafe persistence while adding little runtime overhead.

## Problem
- Stateful agents use the context window as working memory, but current harnesses treat memory residency and persistence as best-effort. This causes lost instructions, lost plans, repeated tool calls, and overwritten state after compaction or reset.
- The paper targets policy-controllable failures: missing required state in prompt assembly, missed flushes before destructive lifecycle events, destructive writeback, and silent memory lookup failures without reason codes.
- This matters because long-running agents for coding, email, calendars, and other tools can run for hours or days across many context windows. When memory handling fails, the agent repeats work, violates user constraints, or loses progress.

## Approach
- ClawVM moves memory control into the agent harness, which already assembles prompts, mediates tools, and sees lifecycle events. The harness tracks agent state as typed pages such as bootstrap instructions, constraints, plans, preferences, evidence, and conversation segments.
- Each page has a minimum-fidelity invariant and several precomputed representations: full, compressed, structured, or pointer. Under token pressure, the system degrades pages only as far as their invariant allows.
- Prompt assembly uses a deterministic two-phase policy: first place all required minimum representations, then spend remaining tokens on the highest-utility upgrades per token.
- ClawVM adds an explicit fault model for refetch faults, duplicate-tool faults, pinned invariant misses, post-compaction bootstrap faults, silent-recall faults, and flush-miss faults. It also measures paging instability with a thrash index.
- Persistence uses staged validated writeback at every lifecycle boundary. Updates are typed, schema-checked, scoped, non-destructive, and logged in a journal so failures are auditable and replayable.

## Results
- Across 4 OpenClaw-derived workload families and 6 token budgets, ClawVM reduces mean policy-controllable faults from 67.8 for the retrieval baseline and 1.5 for the practitioner-configured compaction+retrieval baseline to 0, when the minimum-fidelity set fits in budget.
- It reduces paging instability by 77.4% versus retrieval and 11.4% versus the practitioner-configured baseline.
- An offline oracle with future knowledge finds no remaining fault headroom: the paper claims the online ClawVM policy already matches the optimum fault count.
- On 12 real-session traces and 30 task-level replays, the paper reports the same zero policy-controllable faults and 100% success at the tightest budget, compared with 76.7% for the practitioner-configured baseline.
- Median policy-engine overhead is reported as under 50 microseconds per turn.
- The abstract states the zero-fault claim holds for synthetic workloads, real traces, and adversarial stress tests whenever the minimum-fidelity set fits within the token budget.

## Link
- [http://arxiv.org/abs/2604.10352v1](http://arxiv.org/abs/2604.10352v1)
