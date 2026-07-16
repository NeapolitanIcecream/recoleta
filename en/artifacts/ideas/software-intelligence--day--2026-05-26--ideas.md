---
kind: ideas
granularity: day
period_start: '2026-05-26T00:00:00'
period_end: '2026-05-27T00:00:00'
run_id: de086bd3-22dd-425a-8e8b-efdc6623baee
status: succeeded
topics:
- coding agents
- software verification
- program repair
- agent testing
- security benchmarks
- RAN automation
- AI cost control
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-verification
- topic/program-repair
- topic/agent-testing
- topic/security-benchmarks
- topic/ran-automation
- topic/ai-cost-control
language_code: en
pass_output_id: 209
pass_kind: trend_ideas
upstream_pass_output_id: 208
upstream_pass_kind: trend_synthesis
---

# Agent Workflow Checkpoints

## Summary
Coding-agent adoption now needs smaller control points inside the development workflow: repair gates before expensive validation, executable checks for generated specifications, and structural tests for tool access and handoffs. The common pressure is practical: teams need to know which agent step failed, whether a claimed fix or spec passes an independent check, and whether token spend is tied to accepted work.

## Evidence gates before full regression in agentic program repair
Teams running coding agents on bug fixes can add a repair gate that preserves failing-test evidence across localization, patching, and validation. The gate should reject unappliable diffs, syntax errors, and build failures before test validation, then rerun the originally failing tests before a full regression suite. Failed attempts should return structured diagnostics to the agent and store the earliest decisive error step for review.

EviACT gives a concrete version of this workflow: it maps RED failing-test evidence to suspect code spans, filters invalid patches with a compile gate, and runs target tests before regression. With GPT-4o, it reports 25.0% resolve rate on Defects4J 2.0, 40.4% on SWE-bench Verified, and 70.1–88.6% lower per-bug API cost where baseline costs are available. TrajAudit adds the audit trail: it diagnoses failed repository-level agent runs by predicting the first step that sent the run off course, with more than 24.4 percentage points better localization accuracy on RootSE while using at least 18% fewer tokens than baselines.

A low-cost rollout is a wrapper around the existing agent runner and CI system. Run it on recent failed agent patches, compare accepted fixes, build-fail rate, full-regression invocations, and tokens per accepted patch, then decide whether to make the gates mandatory for agent-authored pull requests.

### Sources
- [EviACT: An Evidence-to-Action Framework for Agentic Program Repair](../Inbox/2026-05-26--eviact-an-evidence-to-action-framework-for-agentic-program-repair.md): EviACT defines evidence-driven repair stages, compile and test-driven gates, resolve rates, and reported per-bug API cost reductions.
- [EviACT: An Evidence-to-Action Framework for Agentic Program Repair](../Inbox/2026-05-26--eviact-an-evidence-to-action-framework-for-agentic-program-repair.md): The paper describes the validation-cost problem and the Setup–Localize–Patch–Verify pipeline with retrieval, compile, and target-test gates.
- [TrajAudit: Automated Failure Diagnosis for Agentic Coding Systems](../Inbox/2026-05-26--trajaudit-automated-failure-diagnosis-for-agentic-coding-systems.md): TrajAudit supplies failure diagnosis for repository-level coding-agent trajectories and reports RootSE scale, localization gains, and token reduction.

## Executable acceptance tests for generated formal specifications
Teams asking agents to write formal specifications should test the specification as a program artifact before trusting a verifier result. The practical build is a harness that turns requirements into executable checks over valid inputs, invalid inputs, correct outputs, and incorrect outputs, then runs hidden and adversarial cases against the generated spec.

Verus-SpecGym shows why this check matters. A verifier can prove code against the wrong specification, so the spec has to match user intent. The benchmark gives agents Codeforces-derived tasks, Verus skeletons, examples, documentation, and tool access, then evaluates generated specs with executable Rust checks. The best reported model solves 77.8% of 581 tasks, while LLM-as-a-judge evaluation misses 26% of failures caught by the executable evaluator.

The adoption path is narrow and useful: start with small pure functions or service-level invariants where product owners can write examples and edge cases. Treat a generated spec as ready for proof work only after it accepts valid behavior and rejects invalid behavior under concrete tests.

### Sources
- [Verus-SpecGym: An Agentic Environment for Evaluating Specification Autoformalization](../Inbox/2026-05-26--verus-specgym-an-agentic-environment-for-evaluating-specification-autoformalization.md): Verus-SpecGym defines executable evaluation for generated Verus specifications and reports task count, model scores, and LLM-judge misses.
- [Verus-SpecGym: An Agentic Environment for Evaluating Specification Autoformalization](../Inbox/2026-05-26--verus-specgym-an-agentic-environment-for-evaluating-specification-autoformalization.md): The paper reports executable Rust evaluation against official Codeforces tests and adversarial hacks, plus failure modes in generated specifications.
- [Verus-SpecGym: An Agentic Environment for Evaluating Specification Autoformalization](../Inbox/2026-05-26--verus-specgym-an-agentic-environment-for-evaluating-specification-autoformalization.md): The source explains how weak or overly strong specifications can certify wrong behavior or reject correct programs.

## Structural coverage tests for agent tool permissions and handoffs
Teams with multi-agent workflows can add a test suite that covers the declared coordination structure, including reachable agents, allowed tool calls, restricted tool attempts, and delegation edges. The build is straightforward: extract a manifest from agent entry points, turn it into a graph, generate witness scenarios for each obligation, and judge runtime traces for the expected event or violation.

The workflow-testing paper demonstrates this on OpenAI Agents SDK-style systems. Across 10 SDK-derived workflows with 49 reachable agents, 47 tools, and 403 structural obligations, generated scenarios witnessed 54 of 75 allowed-tool obligations and 36 of 48 delegation obligations within the stated refinement budget. Restricted-tool probing found 23 violations among 248 restricted-tool obligations.

This fits teams that already review tool permissions manually or rely on end-to-end task success. A first check can run in CI after workflow edits and fail only on restricted-tool violations; coverage thresholds for allowed calls and delegation paths can start as reported metrics until the scenarios stabilize.

### Sources
- [Testing Agentic Workflows with Structural Coverage Criteria](../Inbox/2026-05-26--testing-agentic-workflows-with-structural-coverage-criteria.md): The paper defines structural coverage criteria for multi-agent workflows and reports coverage and restricted-tool violation results.
- [Testing Agentic Workflows with Structural Coverage Criteria](../Inbox/2026-05-26--testing-agentic-workflows-with-structural-coverage-criteria.md): The abstract describes deriving coverage obligations over reachable agents, allowed tool edges, restricted tool edges, and delegation edges.
- [Testing Agentic Workflows with Structural Coverage Criteria](../Inbox/2026-05-26--testing-agentic-workflows-with-structural-coverage-criteria.md): The source explains why safety-, policy-, and compliance-sensitive workflows need traceable tests for tool-access rules and coordination paths.
