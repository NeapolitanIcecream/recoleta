---
kind: ideas
granularity: day
period_start: '2026-04-06T00:00:00'
period_end: '2026-04-07T00:00:00'
run_id: ead7a913-d224-4dbe-aa9c-41958ae9d654
status: succeeded
topics:
- coding-agents
- reinforcement-learning
- software-testing
- program-repair
- verification
- workflow-automation
tags:
- recoleta/ideas
- topic/coding-agents
- topic/reinforcement-learning
- topic/software-testing
- topic/program-repair
- topic/verification
- topic/workflow-automation
language_code: en
pass_output_id: 39
pass_kind: trend_ideas
upstream_pass_output_id: 38
upstream_pass_kind: trend_synthesis
---

# Execution-checked agent workflows

## Summary
The most actionable work here pushes software agents into loops with hard execution checks. The clearest near-term builds are a repository repair worker that edits tests alongside code, a compiled workflow tool for audited high-volume operations, and an online dependency simulator for microservice integration tests. Each has a concrete user, a bounded pilot, and reported results that are specific enough to test in an existing engineering workflow.

## Repository repair with linked code and test patch generation
Repository repair agents can start treating tests as editable evidence, not fixed gatekeepers. Agent-CoEvo is the clearest case for a build that runs code patches and test patches together, scores both in one execution matrix, and keeps only candidates that explain the issue report and fail on the buggy repo before they pass on the repaired one. The operational pain is familiar: teams hit bug reports where the existing tests are incomplete, stale, or too weak to pin down the behavior change, so a code-only repair loop either overfits to bad tests or stalls.

A practical product shape is a CI-side repair worker for maintainers of large Python or Java repositories. It would open a draft PR with two linked diffs: the implementation patch and the test changes that justify it. The cheap check is narrow and clear: sample issues where maintainers had to edit tests during the fix, then compare a code-only agent against a coevolution loop on merged rate and reviewer rejection rate. The paper reports 41.33% resolved on SWE-bench Lite and 46.4% on SWT-bench Lite, with higher test quality than the listed baselines, which is enough to justify testing this workflow on repos with steady bug backlog and existing CI coverage.

### Evidence
- [Beyond Fixed Tests: Repository-Level Issue Resolution as Coevolution of Code and Behavioral Constraints](../Inbox/2026-04-06--beyond-fixed-tests-repository-level-issue-resolution-as-coevolution-of-code-and-behavioral-constraints.md): Reports joint search over code and test patches, plus benchmark gains on SWE-bench Lite and SWT-bench Lite.
- [Beyond Fixed Tests: Repository-Level Issue Resolution as Coevolution of Code and Behavioral Constraints](../Inbox/2026-04-06--beyond-fixed-tests-repository-level-issue-resolution-as-coevolution-of-code-and-behavioral-constraints.md): Explains the coevolution mechanism and why fixed tests under-constrain repository repair.

## Compiled workflow deployment for high-volume audited operations
High-volume document and transaction workflows can move model use to build time and run validated code in production. Compiled AI gives a concrete pattern: generate a small business-logic function once inside a fixed template, run security scanning, type and syntax checks, sandbox tests, and golden-set accuracy checks, then execute the approved artifact with no runtime model call for the main path. The user pressure is simple: operations teams in billing, prior authorization, claims intake, and document processing need repeatable outputs, short latency, and an audit trail that survives review.

This is buildable now as an internal tool for workflow engineers who already maintain prompt-based automations. Start with one narrow process that has a stable schema and enough traffic to matter, such as invoice field extraction or rules-based intake routing. The first validation is cost and variance: compile the current prompt workflow into code, replay a week of production inputs, and compare per-transaction latency, output drift, and manual exception rate. The reported break-even point is about 17 transactions on BFCL, with 4.5 ms median latency, 100% reproducibility, and large cost differences at scale. The DocILE result also suggests a bounded hybrid mode is workable when messy documents still require a constrained model call.

### Evidence
- [Compiled AI: Deterministic Code Generation for LLM-Based Workflow Automation](../Inbox/2026-04-06--compiled-ai-deterministic-code-generation-for-llm-based-workflow-automation.md): Summarizes the compiled workflow pattern, validation gates, and enterprise workflow fit.
- [Compiled AI: Deterministic Code Generation for LLM-Based Workflow Automation](../Inbox/2026-04-06--compiled-ai-deterministic-code-generation-for-llm-based-workflow-automation.md): Provides break-even, token, and latency results for function-calling workloads.

## Online dependency simulation for microservice integration testing
Teams testing microservices can replace brittle recorded mocks with an online dependency simulator that answers requests during the test run and keeps state across the scenario. Mirage shows why this matters: held-out scenarios break static substitutes because the artifact has to guess all relevant behavior ahead of time, while the runtime simulator can react to new parameters, error paths, and multi-step flows. This maps to a common blocker in service teams where downstream systems are expensive to provision, unavailable in CI, or too unstable for repeatable integration tests.

The concrete build is a test harness that stands up a FastAPI-compatible mock endpoint backed by an LLM, seeded with dependency source code when available and traces when it is not. Early users are platform and backend teams with service meshes, many internal APIs, and frequent contract drift. The first check is direct: pick one dependency that currently relies on record-replay fixtures, run the same integration suite against the real dependency, the current mock, and an online simulator, then compare pass-fail agreement and payload-shape fidelity. Mirage reports 99% status-code fidelity and 99% response-shape fidelity in white-box mode across 110 scenarios, while record-replay reached 62% and 16% on the same benchmarks. That gap is large enough to justify a focused pilot around the most failure-prone dependencies.

### Evidence
- [MIRAGE: Online LLM Simulation for Microservice Dependency Testing](../Inbox/2026-04-06--mirage-online-llm-simulation-for-microservice-dependency-testing.md): Summarizes the online simulation approach and fidelity gains over static substitutes.
- [MIRAGE: Online LLM Simulation for Microservice Dependency Testing](../Inbox/2026-04-06--mirage-online-llm-simulation-for-microservice-dependency-testing.md): Details why held-out scenarios break record-replay and other pre-generated mocks.
