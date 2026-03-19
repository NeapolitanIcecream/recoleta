---
source: hn
url: https://github.com/Photon48/tarvos/tree/main
published_at: '2026-03-12T23:55:30'
authors:
- Photon48
topics:
- ai-coding-agents
- multi-agent-orchestration
- context-management
- developer-tools
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Show HN: Tarvos – Relay Architecture for infinitely building with coding agents

## Summary
Tarvos proposes a “relay-style” orchestration architecture for AI coding agents, using multiple agents with clean contexts to continue long-running software development tasks in sequence, in order to mitigate the performance degradation caused by long contexts. It is currently provided as a reference implementation for Claude Code, with the core value proposition of replacing single-session execution with a phased, recoverable, and monitorable multi-agent pipeline.

## Problem
- Existing AI coding tools typically have a single agent execute a task from start to finish. As context continuously accumulates, model accuracy declines, and in later stages a large portion of the context is spent “remembering what has already been done” rather than continuing development.
- This limits long tasks, phased tasks, and workflows closer to “autonomous development,” especially when executing multi-phase PRDs.
- For users, the lack of reliable handoff, recovery, isolated execution, and context budget control makes it difficult for long-running coding agents to scale stably.

## Approach
- Replace long single-agent sessions with **Relay Architecture**: each new agent rereads the full Master Plan from disk, receives only a minimal handoff note (the Baton), and then continues the next segment of work.
- The handoff note is `progress.md`, limited to 40 lines, with the goal of forcing minimal information transfer and avoiding bringing bloated old context into the next agent, recreating “context corruption.”
- The system uses three explicit signals — `PHASE_COMPLETE`, `PHASE_IN_PROGRESS`, and `ALL_PHASES_COMPLETE` — to drive the orchestrator; the orchestrator does not need to understand code semantics and only needs to listen for status signals and schedule the next step.
- Introduce a **Context Budget**: token usage is tracked in real time, and when the budget threshold is reached, the current agent is automatically stopped and a new clean agent is created to take over; agents can also self-assess mid-run and proactively hand off.
- As a reference implementation, Tarvos also provides git worktree isolation, background execution, TUI monitoring, exception recovery (where a recovery agent can reconstruct the handoff from git history), and accept/reject/forget lifecycle management.

## Results
- In the demo case given in the text, a payment feature development plan of about **4 phases and roughly 2,400 lines of work** was completed by **5 agents** in **29 minutes**, ultimately reaching `ALL_PHASES_COMPLETE`.
- Example runtime and token usage by agent: Phase 1 **3 minutes / 42k tokens**; first run of Phase 2 **8 minutes / 87k tokens**, after which a clean handoff was triggered by the context budget; continued Phase 2 **6 minutes / 61k tokens**; Phase 3 **7 minutes / 79k tokens**; Phase 4 **5 minutes / 53k tokens**.
- The key claim is that each agent can operate at “full capacity,” rather than suffering degraded performance in the later stages of a long context; the system splits long tasks into multiple executions with fresh contexts, thereby covering a “distance that no single agent could sustain.”
- The text **does not provide formal benchmark experiments**, public dataset evaluations, statistical significance for comparison methods, or systematic quantitative comparisons with other AI coding agent frameworks.
- The strongest concrete evidence is product-level engineering features and a single end-to-end example run, rather than academic paper-style experimental results.

## Link
- [https://github.com/Photon48/tarvos/tree/main](https://github.com/Photon48/tarvos/tree/main)
