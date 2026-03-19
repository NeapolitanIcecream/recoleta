---
source: hn
url: https://github.com/Photon48/tarvos/tree/main
published_at: '2026-03-12T23:55:30'
authors:
- Photon48
topics:
- coding-agents
- multi-agent-orchestration
- context-management
- software-automation
- developer-tools
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Show HN: Tarvos – Relay Architecture for infinitely building with coding agents

## Summary
Tarvos proposes a “relay-style” execution architecture for AI coding agents that avoids the performance degradation caused by long contexts by continuously switching to fresh agents. It breaks software development into phases and maintains continuity through minimal handoff information and an external orchestrator, thereby supporting longer-horizon automated coding workflows.

## Problem
- Existing AI coding tools typically rely on a single agent to execute a task from start to finish, but as the context window fills with historical content, model accuracy drops significantly.
- In multi-phase software development, a large share of tokens in later stages is spent “remembering what was done before” rather than continuing to implement new tasks at high quality, which limits true autonomous development.
- This matters because complex software tasks often span multiple phases and extended durations, making it difficult for single-session agents to reliably complete end-to-end delivery.

## Approach
- The core method is “Relay Architecture”: instead of having one agent do the entire task, multiple fresh agents take turns by phase, each reading the full master plan from disk and then continuing based on an extremely minimal handoff.
- It splits shared state into 4 components: **Master Plan** (a persistent phased plan), **Baton** (a `progress.md` handoff of at most 40 lines), **Signals** (`PHASE_COMPLETE`/`PHASE_IN_PROGRESS`/`ALL_PHASES_COMPLETE`), and **Context Budget** (a real-time token budget with threshold-based switching).
- The orchestrator does not understand code semantics; it only listens for signals, monitors token consumption, and stops the current agent and launches a new one when the budget is exceeded.
- As a reference implementation of this architecture, Tarvos provides git worktree isolation, background execution, TUI monitoring, automatic recovery, and accept/reject/forget lifecycle management.

## Results
- In the example, the task “payments” was split into **4 phases**, with an estimated **~2400 lines of work**, and was ultimately completed by **5 agents** working in relay, with a total runtime of **29 minutes**.
- The example token usage per agent is: Phase 1 **42k tokens / 3m**, Phase 2 **87k / 8m** before a budget-triggered handoff, continued Phase 2 **61k / 6m**, Phase 3 **79k / 7m**, and Phase 4 **53k / 5m**.
- The article’s central qualitative claim is that each agent can operate at “full capacity” with a “clean context,” avoiding the degradation a single agent experiences in long contexts.
- The article cites an external empirical motivation (Chroma Research indicates that longer inputs reduce model accuracy), but **does not provide formal benchmark experiments, control groups, success-rate statistics, or quantitative comparisons with other coding agent systems**.
- Therefore, the current result is better understood as a persuasive systems demo and engineering implementation, rather than a rigorously evaluated performance breakthrough validated by paper-style benchmarking.

## Link
- [https://github.com/Photon48/tarvos/tree/main](https://github.com/Photon48/tarvos/tree/main)
