---
kind: ideas
granularity: week
period_start: '2026-06-29T00:00:00'
period_end: '2026-07-06T00:00:00'
run_id: 173050ed-1e00-4237-8f36-e8125c1a43f2
status: succeeded
topics:
- coding agents
- agent evaluation
- software engineering agents
- LLM operations
- agent security
- identity and access control
- cost control
tags:
- recoleta/ideas
- topic/coding-agents
- topic/agent-evaluation
- topic/software-engineering-agents
- topic/llm-operations
- topic/agent-security
- topic/identity-and-access-control
- topic/cost-control
language_code: en
pass_output_id: 307
pass_kind: trend_ideas
upstream_pass_output_id: 306
upstream_pass_kind: trend_synthesis
---

# Controlled Coding-Agent Operations

## Summary
Coding-agent adoption now needs narrower gates: replayed review sessions before rollout, run-level spend reservations tied to token telemetry, and command execution that keeps credentials and shell effects away from the durable agent process.

## Replayed multi-turn review tests for coding-agent rollout
Teams choosing a coding agent should test it on replayed review sessions from their own repositories before expanding use. The test should preserve the initial incomplete request, the repository state, the later user corrections, and the final verifier. Score final correctness together with a correction count, because two agents can land similar patches while demanding different amounts of developer review.

SWE-Together shows a workable pattern: it filtered 11,260 recorded sessions into 109 repository-level tasks, replayed feedback through a state-conditioned user simulator, and reported User Correction alongside pass rates. SWE-INTERACT adds pressure from delayed requirements: Opus 4.8 and GPT 5.5 fell from about 50% single-turn resolve rates to 26.7% and 24.7% in multi-turn sessions, while GPT 5.5 cost rose from $2.78 to $9.84 per trial. A practical internal version can start with 20 to 50 recent agent-assisted tickets where the team can restore the commit, replay the first request, and compare final tests with the number of reviewer interventions.

### Sources
- [SWE-Together: Evaluating Coding Agents in Interactive User Sessions](../Inbox/2026-06-29--swe-together-evaluating-coding-agents-in-interactive-user-sessions.md): SWE-Together defines replayed multi-turn coding sessions and reports User Correction alongside final correctness.
- [SWE-INTERACT: Reimagining SWE Benchmarks as User-Driven Long-Horizon Coding Sessions](../Inbox/2026-06-29--swe-interact-reimagining-swe-benchmarks-as-user-driven-long-horizon-coding-sessions.md): SWE-INTERACT shows large drops in resolve rate and higher cost when agents handle delayed requirements over multiple turns.

## Run-scoped spend reservations for long coding-agent sessions
LLM platform teams should add a per-run budget check before every coding-agent provider call. The check can estimate worst-case cost from current input tokens, max output tokens, and a versioned price table; reserve that amount atomically across run, user, and key limits; then commit actual usage after the call. The agent should receive machine-readable budget state so it can shorten context, choose a cheaper model, or stop cleanly.

TraceLab gives the operational reason to measure at this level. In 4,265 real Claude Code and Codex sessions, prefix tokens were 52.56B of 54.90B input tokens and 59.5% of estimated API cost. Cache misses still caused 3.8 times more prefilling than truly new input tokens. The budget RFC supplies an implementation shape: a gateway hook, sidecar, or SDK middleware that reserves estimated spend before forwarding a request and releases unused reserve afterward. The first deployment check is simple: log prefix, append, and output tokens by run for two weeks, then set a soft run ceiling and inspect how often agents would have received a downshift signal.

### Sources
- [TraceLab: Characterizing Coding Agent Workloads for LLM Serving](../Inbox/2026-06-29--tracelab-characterizing-coding-agent-workloads-for-llm-serving.md): TraceLab quantifies real coding-agent sessions and shows prefix reads dominate estimated cost.
- [RFC: Stopping runaway AI agent spend with atomic budget reservations](../Inbox/2026-07-04--rfc-stopping-runaway-ai-agent-spend-with-atomic-budget-reservations.md): The budget RFC describes run-scoped atomic spend reservations and machine-readable budget state for agents.

## Disposable command sandboxes with brokered OAuth access for DevOps agents
Security and platform teams giving agents DevOps tools should split the durable agent loop from command execution. Keep memory, task history, and orchestration in a stable process. Run shell commands in a per-session disposable sandbox, with checkpoints before risky steps. For SaaS and internal APIs, route calls through a broker and proxy so the agent environment receives a broker-minted token bound to the live mTLS client certificate, while the proxy handles the real OAuth token.

UnderSpecBench shows why DevOps agents need this boundary. Across 2,208 prompt variants, acted runs violated action boundaries 55.8% to 67.8% of the time, with wrong-target and overscope outcomes on cleanup, rollback, pruning, and access-change tasks. Fly.io’s Sprite pattern gives a concrete execution model: one shared agent runtime can dispatch commands to isolated per-session Sprites, inject a user token for a single `flyctl` command, and restore a damaged filesystem and toolchain from a checkpoint. Securing Agentic Identity gives the API access pattern, keeping reusable OAuth tokens out of the agent runtime while preserving stateless broker and proxy scaling.

### Sources
- [Coding Agents Are Guessing: Measuring Action-Boundary Violations in Underspecified DevOps Instructions](../Inbox/2026-07-02--coding-agents-are-guessing-measuring-action-boundary-violations-in-underspecified-devops-instructions.md): UnderSpecBench measures wrong-target and overscope behavior in underspecified DevOps tasks.
- [Building Agents That Don't Break Themselves](../Inbox/2026-07-05--building-agents-that-don-t-break-themselves.md): The Fly.io Sprite pattern separates the long-lived agent loop from disposable command sandboxes and single-command token injection.
- [Securing Agentic Identity](../Inbox/2026-07-03--securing-agentic-identity.md): Securing Agentic Identity proposes a broker, proxy, and mTLS binding so real OAuth tokens stay out of the agent environment.
