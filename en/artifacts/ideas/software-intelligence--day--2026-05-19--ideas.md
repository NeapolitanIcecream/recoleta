---
kind: ideas
granularity: day
period_start: '2026-05-19T00:00:00'
period_end: '2026-05-20T00:00:00'
run_id: f4d60be8-002e-44a7-a834-d55624705ca0
status: succeeded
topics:
- agent reliability
- code generation
- runtime verification
- multi-agent systems
- code model calibration
tags:
- recoleta/ideas
- topic/agent-reliability
- topic/code-generation
- topic/runtime-verification
- topic/multi-agent-systems
- topic/code-model-calibration
language_code: en
pass_output_id: 179
pass_kind: trend_ideas
upstream_pass_output_id: 178
upstream_pass_kind: trend_synthesis
---

# Agent State Verification

## Summary
Agent deployments are getting concrete control points: write-time state checks for parallel coding agents, executable state verifiers for desktop tasks, and runtime evidence for choosing or deferring generated code. The common pattern is simple: record what the agent saw, check the action against current state, and keep a machine-readable reason when the system rejects or routes the output.

## Versioned write gates for parallel coding agents
Teams running several coding agents on the same repository can add a shared write gate before scaling the number of agents. The gate keeps a version counter for each file, records the files each agent read, and rejects a write when any file in that read set has changed. The rejection should return the current target file, the direct diff, and any stale dependency files so the agent can retry with current context.

STORM gives a concrete design for this workflow. It keeps one shared workspace, checks an agent’s read snapshot before each write, and uses structured intent comments so nearby agents can see why code changed. On Commit0-Lite with Claude Sonnet 4.6, STORM reported 46.2 weighted pass rate and 82.5 macro pass rate, compared with 24.6 / 63.8 for a GitWorktree baseline. The cheap test is to run the same backlog with isolated worktrees and with a versioned write gate, then compare integration failures, rejected stale writes, retry rate, and wall-clock time.

### Sources
- [Multi-agent Collaboration with State Management](../Inbox/2026-05-19--multi-agent-collaboration-with-state-management.md): STORM describes version counters, read snapshots, stale-write rejection, retry context, and benchmark gains over GitWorktree and single-agent baselines.
- [Multi-agent Collaboration with State Management](../Inbox/2026-05-19--multi-agent-collaboration-with-state-management.md): The paper explains why workspace isolation delays semantic conflicts until merge time and motivates write-time state management.

## Application-state verifiers for desktop-agent QA runs
Computer-use agents need QA checks that inspect saved application state, files, databases, and settings after a run. A practical build is a small verifier package per target application: Python CLI endpoints return JSON checks for browser profiles, SQLite databases, LibreOffice documents, D-Bus state, saved files, and accessibility state. Each task can ship with its initial sandbox state, user instruction, and executable success criteria.

OpenComputer shows this at benchmark scale with 33 desktop applications and 1,000 tasks, averaging 17.7 verifier endpoints per app and 6.9 checks per task. Its warning applies to internal QA as well: screenshots and LLM judges can miss errors in metadata or persistent side effects. AgentAtlas adds the trace layer that operators need during review: label decisions such as Act, Ask, Refuse, Stop, Confirm, and Recover, and record failure categories when the agent loops, skips confirmation, uses the wrong tool, or recovers poorly. A first adoption step is to convert ten common desktop tasks into sandbox initializers plus executable checks, then compare screenshot-only review with verifier results.

### Sources
- [OpenComputer: Verifiable Software Worlds for Computer-Use Agents](../Inbox/2026-05-19--opencomputer-verifiable-software-worlds-for-computer-use-agents.md): OpenComputer details app-specific verifier modules, real application state inspection, sandboxed task generation, and benchmark scale.
- [OpenComputer: Verifiable Software Worlds for Computer-Use Agents](../Inbox/2026-05-19--opencomputer-verifiable-software-worlds-for-computer-use-agents.md): The source text explains why screenshots can miss file contents, metadata, and persistent side effects.
- [AgentAtlas: Beyond Outcome Leaderboards for LLM Agents](../Inbox/2026-05-19--agentatlas-beyond-outcome-leaderboards-for-llm-agents.md): AgentAtlas provides control-decision labels and trajectory failure categories for reviewing agent runs beyond final task success.

## Fuzzing-based candidate selection before returning generated code
Coding assistants can sample several candidate programs and run a local selector before showing one answer to a developer. DIFFCODEGEN gives a buildable version: generate diverse candidates, fuzz one reference candidate to create inputs, execute every candidate on those inputs, compare outputs, errors, return values, exceptions, and exit codes, then return the medoid of the largest behavior cluster.

This is useful when public tests are unavailable and another LLM judging pass would add cost or latency. The paper reports that selection needs no extra model calls after initial generation, uses about 20% of the execution time of prior test-time scaling methods for locally served LLMs on LiveCodeBench, about 5% for API-based LLMs, and about 4% of the input tokens used by previous work. For higher-risk tasks, the selector can feed a defer step: calibrated low-confidence or low-agreement cases go to compiler checks, static analysis, validators, prompt augmentation, task decomposition, or human review.

### Sources
- [Code Generation by Differential Test Time Scaling](../Inbox/2026-05-19--code-generation-by-differential-test-time-scaling.md): DIFFCODEGEN describes candidate generation, coverage-guided fuzzing, behavioral comparison, clustering, medoid selection, and reported time/token savings.
- [Code Generation by Differential Test Time Scaling](../Inbox/2026-05-19--code-generation-by-differential-test-time-scaling.md): The source text states why PASS@K does not match real coding assistants that must return one solution.
- [When to Answer and When to Defer: A Decision Framework for Reliable Code Predictions](../Inbox/2026-05-19--when-to-answer-and-when-to-defer-a-decision-framework-for-reliable-code-predictions.md): The defer-and-recover paper describes calibrated thresholds and routes uncertain code outputs to analysis tools or recovery steps.
