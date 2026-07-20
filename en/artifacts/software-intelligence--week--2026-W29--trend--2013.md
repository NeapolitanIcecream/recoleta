---
kind: trend
trend_doc_id: 2013
granularity: week
period_start: '2026-07-13T00:00:00'
period_end: '2026-07-20T00:00:00'
topics:
- coding agents
- agent evaluation
- software testing
- runtime verification
- repository context
- software security
run_id: materialize-outputs
aliases:
- recoleta-trend-2013
tags:
- recoleta/trend
- topic/coding-agents
- topic/agent-evaluation
- topic/software-testing
- topic/runtime-verification
- topic/repository-context
- topic/software-security
language_code: en
pass_output_id: 338
pass_kind: trend_synthesis
---

# Coding-agent controls gained precision through targeted context and executable evidence

## Overview
This week strengthens the three-week run of evidence that coding-agent performance depends on the system around the model. The new signal is precision: context is acquired for identified knowledge gaps, while checks bind claims to changed code, exact source state, or domain risks. Results span benchmarks and prototypes, but broad deployment evidence remains limited.

## Findings

### Minimum-sufficient repository context
Two studies favor selective context over exhaustive exploration. ACQUIRE asks repository-specific questions before repair and improved Pass@1 on SWE-bench Verified by up to 4.4 percentage points. E3 estimates task scope, begins with the smallest viable execution path, and expands only after failed verification; on its controlled benchmark, it preserved 100% success while cutting tokens by 91%. Together, they support context acquisition as a budgeted intervention rather than a default repository-wide scan. E3’s strongest numbers come from a simulator, so its efficiency gains need broader confirmation.

#### Sources
- [Know Before Fix: QA-Driven Repository Knowledge Acquisition for Software Issue Resolution](../Inbox/2026-07-13--know-before-fix-qa-driven-repository-knowledge-acquisition-for-software-issue-resolution.md): Reports ACQUIRE’s targeted question-answering method, up to 4.4-point Pass@1 gain, and repository-grounding results.
- [Do AI Agents Know When a Task Is Simple? Toward Complexity-Aware Reasoning and Execution](../Inbox/2026-07-14--do-ai-agents-know-when-a-task-is-simple-toward-complexity-aware-reasoning-and-execution.md): Reports E3’s expand-on-failure policy and controlled reductions of 85% in cost and 91% in tokens at 100% success.

### Harness-aware, source-bound gates
The harness is now part of both the measurement and the safety claim. AgentCompass found that changing the harness altered benchmark scores and trajectory failures. A supply-chain study likewise showed the same model catching or installing an attack depending on its harness, while a deterministic pre-install check closed most observed gaps. Proof-or-Stop adds a stricter lifecycle boundary: an agent’s claim advances only when fresh evidence is authenticated and tied to the current source state. Its tests blocked false completion and tampered receipts, although evaluation covered one model family and a self-hosted corpus.

#### Sources
- [AgentCompass: A Unified Evaluation Infrastructure for Agent Capabilities](../Inbox/2026-07-15--agentcompass-a-unified-evaluation-infrastructure-for-agent-capabilities.md): Shows score variation across harnesses and records harness-dependent failure patterns over multiple benchmarks.
- [Setup Complete, Now You Are Compromised: Weaponizing Setup Instructions Against AI Coding Agents](../Inbox/2026-07-16--setup-complete-now-you-are-compromised-weaponizing-setup-instructions-against-ai-coding-agents.md): Shows harness-model dependence in package-install attacks and the effect of checking dependency names, sources, and versions before execution.
- [Proof-or-Stop: Don't Trust the Agent, Trust the Evidence -- Loop Engineering for Verifiable Evidence-Gated Lifecycle Control](../Inbox/2026-07-16--proof-or-stop-don-t-trust-the-agent-trust-the-evidence-loop-engineering-for-verifiable-evidence-gated-lifecycle-control.md): Defines source-state-bound evidence gates and reports 10/10 lifecycle scenarios with zero false-done plus rejection of 18 tamper classes.

### Validation aimed at the relevant failure surface
Executable checks are becoming narrower and more domain-complete. DiffTestGen directs tests toward changed functions and exposed behavioral differences in 78.2% of 463 pull requests. GapForge targets uncovered compiler regions, adding tens of thousands of covered lines over a reported baseline and finding 12 real failures. Alipay-PIBench applies the same logic to payment integration, testing end-to-end behavior, signature and notification handling, idempotency, refunds, and business-state consistency. These results show that a generic pass signal is insufficient when the meaningful failure surface is a code diff, a coverage gap, or a domain invariant.

#### Sources
- [DiffTestGen: Change-Directed LLM-Based Testing for Exposing Behavioral Differences](../Inbox/2026-07-17--difftestgen-change-directed-llm-based-testing-for-exposing-behavioral-differences.md): Reports change-directed test generation, 78.2% behavioral-difference exposure, and 90.7% average union coverage across 463 pull requests.
- [GapForge: Directed Compiler Fuzzing via Coverage-Gap Analysis](../Inbox/2026-07-17--gapforge-directed-compiler-fuzzing-via-coverage-gap-analysis.md): Reports coverage-gap-directed compiler fuzzing, additional GCC and LLVM coverage, and 12 discovered failures.
- [Alipay-PIBench: A Realistic Payment Integration Benchmark for Coding Agents](../Inbox/2026-07-16--alipay-pibench-a-realistic-payment-integration-benchmark-for-coding-agents.md): Defines payment-specific static, unit, integration, and end-to-end checks across 18 repository-level tasks, including risk-hardening requirements.
