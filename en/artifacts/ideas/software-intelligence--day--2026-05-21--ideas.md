---
kind: ideas
granularity: day
period_start: '2026-05-21T00:00:00'
period_end: '2026-05-22T00:00:00'
run_id: f4d60be8-002e-44a7-a834-d55624705ca0
status: succeeded
topics:
- coding agents
- software engineering
- agent evaluation
- test generation
- trajectory training
- self-evolving agents
- pull requests
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-engineering
- topic/agent-evaluation
- topic/test-generation
- topic/trajectory-training
- topic/self-evolving-agents
- topic/pull-requests
language_code: en
pass_output_id: 183
pass_kind: trend_ideas
upstream_pass_output_id: 182
upstream_pass_kind: trend_synthesis
---

# Coding Agent Verification Trails

## Summary
Coding-agent adoption now needs checks that preserve the evidence behind a result: mutant survival for generated tests, review context and refactoring risk for pull requests, and replayed user failures for source-level updates in deployed agents.

## Mutation checks for generated issue tests
Teams that use coding agents to write tests can add a small mutation gate before those tests affect patch approval, benchmark scores, or repair-agent training. A generated test suite should fail on the original bug, pass on the fix, and catch a few semantically plausible faulty variants derived from the fix.

SWE-Mutation shows why this gate is useful. DeepSeek-V3.1 with Mini-Swe-Agent reached 88.20% Pass@1 on Python test generation, yet only 10.20% verification and 36.15% mutant detection. The test files ran, but many did not prove the reported issue or catch nearby wrong repairs. A cheap pilot is to take recent fixed issues, generate 3 to 5 mutants per fix, and track VRR and RDR beside Pass@1 in CI or evaluation runs.

### Sources
- [SWE-Mutation: Can LLMs Generate Reliable Test Suites in Software Engineering?](../Inbox/2026-05-21--swe-mutation-can-llms-generate-reliable-test-suites-in-software-engineering.md): SWE-Mutation defines the issue-test evaluation with Pass@1, VRR, and RDR, and reports the large gap between executable tests and useful tests.
- [SWE-Mutation: Can LLMs Generate Reliable Test Suites in Software Engineering?](../Inbox/2026-05-21--swe-mutation-can-llms-generate-reliable-test-suites-in-software-engineering.md): The paper states the dataset size, DeepSeek-V3.1 verification and detection rates, and the drop in detection under agentic mutants.

## Agent pull request review records with refactoring checks
Repositories accepting agent-authored pull requests should record review evidence in the same place they record merge status. A GitHub bot can attach fields for CI result, reviewer comments, reviewer-applied commits, closure reason, duplicate or superseded work, and explicit human feedback. For Java patches, the same check can run RefactoringMiner and flag tangled refactorings that were not requested by the issue.

The pull-request study found that only 35.7% of sampled rejected agentic PRs were clear agent failures, while 31.2% came from workflow constraints and 33.1% had no visible rationale. Merged PRs also need context: 15.4% involved explicit reviewer feedback or reviewer-applied commits. Refactoring Runaway adds a patch-level reason to keep this record: tangled refactorings appeared in 21.43% of valid Java agent patches and were associated with lower compilability. RefUntangle raised average compilation success from 19.34% to 38.33%, which points to a practical pre-review repair step for risky structural edits.

### Sources
- [Why Are Agentic Pull Requests Merged or Rejected? An Empirical Study](../Inbox/2026-05-21--why-are-agentic-pull-requests-merged-or-rejected-an-empirical-study.md): The study quantifies rejected and merged agentic PRs and shows why merge status alone misreads agent performance.
- ["Refactoring Runaway": Understanding and Mitigating Tangled Refactorings in Coding Agents for Issue Resolution](../Inbox/2026-05-21--refactoring-runaway-understanding-and-mitigating-tangled-refactorings-in-coding-agents-for-issue-resolution.md): The paper measures tangled refactorings in Java agent patches and reports RefUntangle’s compilation gains.

## Failure-batch replay before source-level agent updates
Teams running deployed agents can turn repeated user-facing failures into a guarded update workflow. The system logs weak or missing dialogue chunks, seals a small batch, asks a coding agent to locate and edit the source-level fault, and replays the batch against a candidate image in an isolated worker before any production change. Promotion requires a human apply step, health probes, and rollback.

MOSS gives a concrete pattern for this workflow. It targets failures in routing, hook ordering, session state, dispatch, and concurrency, which prompt or skill edits may not fix. On OpenClaw, one evolution cycle raised the four-task mean grader score from 0.25 to 0.61 without human code edits. The safety detail matters for adoption: MOSS tests candidate images in ephemeral trial-worker containers and requires `moss evo apply`, health checks, and rollback before promotion.

### Sources
- [MOSS: Self-Evolution through Source-Level Rewriting in Autonomous Agent Systems](../Inbox/2026-05-21--moss-self-evolution-through-source-level-rewriting-in-autonomous-agent-systems.md): MOSS describes failure batching, ordered repair stages, candidate-image replay, consent-gated promotion, and the OpenClaw score gain.
- [MOSS: Self-Evolution through Source-Level Rewriting in Autonomous Agent Systems](../Inbox/2026-05-21--moss-self-evolution-through-source-level-rewriting-in-autonomous-agent-systems.md): The paper states that code changes are delegated to external coding-agent CLIs and verified through replay in trial workers before promotion.
- [MOSS: Self-Evolution through Source-Level Rewriting in Autonomous Agent Systems](../Inbox/2026-05-21--moss-self-evolution-through-source-level-rewriting-in-autonomous-agent-systems.md): The paper lists harness-level failures such as routing, hooks, state management, dispatch, and session lifecycle as source-level repair targets.
