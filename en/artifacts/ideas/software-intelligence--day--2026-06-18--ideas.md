---
kind: ideas
granularity: day
period_start: '2026-06-18T00:00:00'
period_end: '2026-06-19T00:00:00'
run_id: 66bf5983-b3ff-46ff-9547-8902278fe71f
status: succeeded
topics:
- coding agents
- software engineering
- agent safety
- code evaluation
- compiler tuning
- benchmarking
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-engineering
- topic/agent-safety
- topic/code-evaluation
- topic/compiler-tuning
- topic/benchmarking
language_code: en
pass_output_id: 267
pass_kind: trend_ideas
upstream_pass_output_id: 266
upstream_pass_kind: trend_synthesis
---

# Coding Agent Release Controls

## Summary
Repository maintainers can now treat agent instructions, pull request creation, and model selection as testable software work. The practical moves are compact repository guidance revised after failed probes, issue-agent pull requests blocked by baseline-aware tests and permission gates, and evaluation suites that include the languages and project sizes used in production.

## Synthetic bug-fix probes for AGENTS.md files
Repository teams using coding agents should add a small tuning job for their AGENTS.md or equivalent repository guidance. The job can generate synthetic bug-fix tasks, run the agent against them, record where the instructions sent it to the wrong subsystem or missed the right test command, then edit the guidance file under a size cap.

Probe-and-Refine gives a concrete pattern: 10 synthetic bug-fix probes per iteration, 3 to 5 iterations per repository, and a final guidance file reused by the coding agent. On 500 SWE-bench Verified instances, the refined guidance reached a 33.0% mean resolve rate, compared with 28.3% for static guidance and 25.5% with no context. The gain came mainly from producing evaluable patches more often, which fits the common maintainer pain: the agent wastes its budget in the wrong files or follows stale local habits.

A cheap first version is a nightly job on the top repositories where agents already open drafts. Track whether the agent reaches an evaluable patch, which commands it ran, and which guidance lines were used or contradicted. Keep the output short enough for every run to read, and require a human review for guidance edits that change release, security, or data-migration steps.

### Evidence
- [Probe-and-Refine Tuning of Repository Guidance for Coding Agents](../Inbox/2026-06-18--probe-and-refine-tuning-of-repository-guidance-for-coding-agents.md): Shows the probe-and-refine method, the 33.0% versus 28.3% and 25.5% resolve-rate comparison, and the finding that refined guidance mainly increases evaluable patches.
- [Phoenix: Safe GitHub Issue Resolution via Multi-Agent LLMs](../Inbox/2026-06-18--phoenix-safe-github-issue-resolution-via-multi-agent-llms.md): Reports that manual inspection of real issue pull requests found many generic or invented-path changes, a failure mode that better repository guidance can target.

## Baseline-aware pull request gates for issue agents
Teams letting agents work GitHub issues should put the agent behind a pull request lane that compares a clean baseline test run with the patched run. The gate should allow drafts only when the patch adds no new failing tests, blocks sensitive file paths or workflow edits, and records the agent’s tool calls, approvals, and owner for review.

Phoenix is a useful reference design because it handles broken or flaky repositories by separating pre-existing failures from failures introduced by the patch. Its Tester runs the unmodified branch first, runs the patched branch next, and accepts a change only when no new failures appear. On a curated 24-task SWE-bench Lite slice, Phoenix reports 18 oracle-resolved tasks and no PASS_TO_PASS regressions on successful runs.

Permission choice needs its own check in the same lane. ToolPrivBench found that six of 11 evaluated models exceeded 30% over-privileged tool use when lower-privilege tools were sufficient. Eve shows the production plumbing that makes these gates easier to ship: durable sessions, sandboxes, human approvals, traces, and file-based evals. A production repository can start with three required records on every agent PR: baseline test hash, patched test hash, and any high-privilege tool or approval event.

### Evidence
- [Phoenix: Safe GitHub Issue Resolution via Multi-Agent LLMs](../Inbox/2026-06-18--phoenix-safe-github-issue-resolution-via-multi-agent-llms.md): Describes Phoenix’s baseline-versus-patched test gate, safety controls, pull request workflow, and reported no PASS_TO_PASS regressions on successful runs.
- [When Lower Privileges Suffice: Investigating Over-Privileged Tool Selection in LLM Agents](../Inbox/2026-06-18--when-lower-privileges-suffice-investigating-over-privileged-tool-selection-in-llm-agents.md): Shows that agents often choose higher-privilege tools even when lower-privilege tools are sufficient, with OPUR results across 11 models.
- [Eve](../Inbox/2026-06-18--eve.md): Lists production agent runtime features such as durable workflows, sandboxes, approvals, traces, and evals.
- [The Line Vibe Coding Can't Cross](../Inbox/2026-06-18--the-line-vibe-coding-can-t-cross.md): Connects production AI coding to required checks for auth, payments, secrets, and untrusted input, including tests, review, threat modeling, audit trail, and named owners.

## Cross-language and project-scale evaluation before coding-agent rollout
Engineering groups should stop accepting a single Python coding score as evidence for repository-wide agent use. A rollout eval should include the project’s main languages, compile or runtime checks in sandboxed containers, and at least one multi-file task with behavior checks for repositories where unit tests do not capture the main failure.

Multi-LCB gives the cross-language template. It extends LiveCodeBench to 12 languages while keeping release-date filtering and hidden tests. The reported scores show why this matters: Qwen3-235B-A22B-Thinking-2507 scores higher than GPT-OSS-120B Medium in Python and C++, then drops in Rust, Ruby, and Go, lowering its 12-language average.

JAMER adds the project-scale test. Its Godot benchmark filters more than 240,000 candidate repositories down to 8,133 behavior-valid projects and checks compilation, startup stability, structural completeness, and runtime behavior. Runtime pass rates on code completion fall from 80.4% on small projects to 5.7% on large projects. A practical adoption test can be small: pick 20 tasks from the team’s own languages and 5 large multi-file tasks, then block general rollout until the chosen agent passes the same CI and runtime checks a developer would face.

### Evidence
- [Multi-LCB: Extending LiveCodeBench to Multiple Programming Languages](../Inbox/2026-06-18--multi-lcb-extending-livecodebench-to-multiple-programming-languages.md): Shows Multi-LCB’s 12-language extension of LiveCodeBench and the reported language-specific score gaps.
- [JAMER: Project-Level Code Framework Dataset and Benchmark on Professional Game Engines](../Inbox/2026-06-18--jamer-project-level-code-framework-dataset-and-benchmark-on-professional-game-engines.md): Shows JAMER’s project-level Godot evaluation, behavior-valid repository filtering, and the runtime pass-rate drop from small to large projects.
