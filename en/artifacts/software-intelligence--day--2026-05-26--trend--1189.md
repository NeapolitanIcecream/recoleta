---
kind: trend
trend_doc_id: 1189
granularity: day
period_start: '2026-05-26T00:00:00'
period_end: '2026-05-27T00:00:00'
topics:
- coding agents
- software verification
- program repair
- agent testing
- security benchmarks
- RAN automation
- AI cost control
run_id: materialize-outputs
aliases:
- recoleta-trend-1189
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-verification
- topic/program-repair
- topic/agent-testing
- topic/security-benchmarks
- topic/ran-automation
- topic/ai-cost-control
language_code: en
pass_output_id: 208
pass_kind: trend_synthesis
---

# Coding agents are being asked to prove, audit, and pay for their work

## Overview
The day’s research treats coding agents as systems that need audit trails, executable checks, and budget controls. TrajAudit, EviACT, and Verus-SpecGym show the main emphasis: failures must be localized, evidence must pass gates, and specifications must be tested against user intent.

## Clusters

### Evidence-gated repair and failure diagnosis
Repository-level coding agents are being evaluated on their use of execution evidence. TrajAudit targets failed agent runs and predicts the earliest decisive error step. Its RootSE benchmark contains 93 failed instances, more than 4,500 execution steps, and about 27 million characters. The paper reports a localization gain above 24.4 percentage points while using at least 18% fewer tokens than baselines.

EviACT applies the same discipline during automated program repair (APR). It carries failing-test evidence into localization, rejects malformed or non-building patches before test validation, and reruns originally failing tests before full regression. With GPT-4o, it reports leading resolve rates across Defects4J 2.0 and SWE-bench variants, plus 70.1–88.6% lower per-bug API cost where baseline costs are available.

MocklessTester adds a lower-level version of the same idea for Java tests. It mines real dependency use, compiles and runs generated JUnit tests, and repairs failures under symbol and typestate constraints. On Defects4J, it reports 88.82% average line coverage and 83.74% branch coverage, with more real dependency code executed than the mock-based baseline.

#### Evidence
- [TrajAudit: Automated Failure Diagnosis for Agentic Coding Systems](../Inbox/2026-05-26--trajaudit-automated-failure-diagnosis-for-agentic-coding-systems.md): TrajAudit summary, RootSE scale, localization gain, and token reduction.
- [EviACT: An Evidence-to-Action Framework for Agentic Program Repair](../Inbox/2026-05-26--eviact-an-evidence-to-action-framework-for-agentic-program-repair.md): EviACT evidence gates, benchmark results, and API cost reductions.
- [LLM-based Mockless Unit Test Generation for Java](../Inbox/2026-05-26--llm-based-mockless-unit-test-generation-for-java.md): MocklessTester method and coverage results on Defects4J and Deps4J.

### Executable specifications and machine-checked software
Verification work focuses on the specification as a source of failure. Verus-SpecGym tests whether a language-model agent can translate an informal programming task into a faithful Verus specification. The benchmark has 581 Codeforces-derived tasks. The strongest reported model solves 77.8%, while an LLM-as-a-judge evaluator misses 26% of failures caught by executable checks.

ConVer uses large language models (LLMs) to write C function contracts and loop invariants, then lets ESBMC make the pass or fail decision. Its results vary by benchmark difficulty: 82–96% success on 45 Frama-C programs, 33–50% on a small X.509 parser benchmark, and 67% on LF-Hard programs converted to C.

The Lean-focused verification essay gives the broader rationale. It argues that AI-generated software needs an independent proof checker, because review and testing cannot scale with generated code volume. Its examples include a Claude-based zlib formalization and Lean’s Mathlib, cited as having more than 200,000 formalized theorems.

#### Evidence
- [Verus-SpecGym: An Agentic Environment for Evaluating Specification Autoformalization](../Inbox/2026-05-26--verus-specgym-an-agentic-environment-for-evaluating-specification-autoformalization.md): Verus-SpecGym benchmark design, model scores, and judge miss rate.
- [ConVer: Using Contracts and Loop Invariant Synthesis for Scalable Formal Software Verification](../Inbox/2026-05-26--conver-using-contracts-and-loop-invariant-synthesis-for-scalable-formal-software-verification.md): ConVer contract synthesis method and benchmark success rates.
- [When AI Writes the Software, Who Verifies It?](../Inbox/2026-05-26--when-ai-writes-the-software-who-verifies-it.md): Argument for machine-checked proofs and Lean-based examples.

### Security and workflow tests for long agent runs
SEC-bench Pro raises the bar for security-agent evaluation by using real JavaScript engine vulnerabilities with reproducible vulnerable, fixed, and latest images. The dataset has 183 validated vulnerabilities across V8 and SpiderMonkey. The strongest single-agent setup solves 32.0% of V8 tasks and 38.8% of SpiderMonkey tasks. A crash-only grader would overcount successes by 43.6%, so target attribution changes the score.

Testing agentic workflows adds a structural view. The proposed method turns an agent workflow into a graph of agents, tools, allowed calls, restricted calls, and delegation edges. Across 10 SDK-derived workflows, generated scenarios cover 54 of 75 allowed-tool obligations and 36 of 48 delegation obligations. Restricted-tool probing finds 23 violations among 248 restricted-tool obligations.

Keyblind is a practical guardrail around secrets. It gives agents fake `.env` values and injects real secrets only when commands run. The evidence is product-level rather than benchmark-level, but the threat is concrete: the project cites more than 100,000 LLM conversations with exposed secrets indexed by search engines in 2025.

#### Evidence
- [SEC-bench Pro: Can Language Models Solve Long-Horizon Software Security Tasks?](../Inbox/2026-05-26--sec-bench-pro-can-language-models-solve-long-horizon-software-security-tasks.md): SEC-bench Pro dataset, scoring method, agent results, and crash-only overcount.
- [Testing Agentic Workflows with Structural Coverage Criteria](../Inbox/2026-05-26--testing-agentic-workflows-with-structural-coverage-criteria.md): Structural coverage criteria and evaluation results for agent workflows.
- [Keyblind – encrypted secrets vault that hides API keys from AI agents](../Inbox/2026-05-26--keyblind-encrypted-secrets-vault-that-hides-api-keys-from-ai-agents.md): Keyblind secret-handling design and stated incident scale.

### Domain-specific agent systems and cost pressure
GENESIS shows how specialized agent systems are being built for technical domains where a small API or specification error can break deployment. For radio access network (RAN) work, it routes intents into synthesis, testing, hardening, optimization, discovery, or security pipelines. Validation runs through simulation, emulation, and over-the-air testbeds. The paper reports 100% success on two feature-implementation case studies, while Claude Code with Opus 4.7 produced no working implementation in those cases.

The enterprise cost signal is less technical but hard to ignore. Uber reportedly spent its full 2026 AI coding-tools budget in four months. Its COO said the company cannot yet draw a clear line between Claude Code usage and a measurable increase in useful consumer features. That makes token-metered agent use a management problem as well as an engineering problem.

#### Evidence
- [GENESIS: Harnessing AI Agents for Autonomous 6G RAN Synthesis, Research, and Testing](../Inbox/2026-05-26--genesis-harnessing-ai-agents-for-autonomous-6g-ran-synthesis-research-and-testing.md): GENESIS pipelines, validation tiers, and RAN case-study results.
- [Uber blows through its AI budget in 1 quarter](../Inbox/2026-05-26--uber-blows-through-its-ai-budget-in-1-quarter.md): Uber budget exhaustion, adoption claims, and uncertainty about product impact.
