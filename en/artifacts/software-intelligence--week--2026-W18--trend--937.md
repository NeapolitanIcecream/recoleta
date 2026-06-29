---
kind: trend
trend_doc_id: 937
granularity: week
period_start: '2026-04-27T00:00:00'
period_end: '2026-05-04T00:00:00'
topics:
- coding agents
- software engineering
- benchmarks
- verification
- security repair
- agent infrastructure
run_id: materialize-outputs
aliases:
- recoleta-trend-937
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-engineering
- topic/benchmarks
- topic/verification
- topic/security-repair
- topic/agent-infrastructure
language_code: en
pass_output_id: 142
pass_kind: trend_synthesis
---

# Coding agents earn trust through context, traces, and executable checks

## Overview
This week’s coding-agent research set a clear bar: generated work needs context, traces, and executable checks before it earns trust. SWE-Edit, AutoMat, and LiveFMBench show the pattern across editing, scientific reproduction, and formal specifications.

## Clusters

### Project context and editing interfaces
Several results treat the agent interface as part of the capability being measured. Context-Augmented Code Generation reports that adding Brief, a product-context retrieval system, raises decision compliance for Claude Code on an 8-task benchmark from 46% to 95%. The result is useful, but the paper also notes a workflow confound: Brief changes available context and adds specs, acceptance criteria, and mid-build guidance.

SWE-Edit makes a narrower systems claim. It splits file viewing and patch writing into separate subagents, so the main agent keeps a cleaner reasoning context. On SWE-bench Verified, it raises resolved rate from 69.9% to 72.0%, cuts total inference cost by 17.9%, and improves edit success from 93.4% to 96.9%. The common lesson is practical: agent quality depends on what the model can see, what it is asked to write, and how edits are applied.

#### Evidence
- [Context-Augmented Code Generation: How Product Context Improves AI Coding Agent Decision Compliance by 49%](../Inbox/2026-04-27--context-augmented-code-generation-how-product-context-improves-ai-coding-agent-decision-compliance-by-49.md): Product-context benchmark, compliance gain, and stated workflow confound.
- [SWE-Edit: Rethinking Code Editing for Efficient SWE-Agent](../Inbox/2026-04-28--swe-edit-rethinking-code-editing-for-efficient-swe-agent.md): SWE-Edit design, SWE-bench Verified results, cost, and edit-success metrics.

### Evidence gates for specifications and scientific work
The strongest evaluations this week ask agents to leave checkable artifacts. AutoMat tests reproduction of 85 computational materials-science claims. The best tested agent reaches a 54.1% success rate, while paper-only reproduction has near-zero success across systems. The weak point is reconstructing underspecified procedures and judging whether outputs support the scientific claim.

LiveFMBench applies the same discipline to formal specifications for C programs. It uses 630 ACSL-annotated programs and filters outputs that change the program or assertion. After that faithfulness check, measured accuracy drops by about 20%. Claw-Eval-Live extends trace-based grading to workflow agents by recording tool traces, service audit logs, command traces, files, tests, and service state. Its leading model passes 66.7% of 105 tasks, so the benchmark still exposes many failed real workflows.

#### Evidence
- [Can Coding Agents Reproduce Findings in Computational Materials Science?](../Inbox/2026-05-01--can-coding-agents-reproduce-findings-in-computational-materials-science.md): AutoMat task design, success rates, and paper-only reproduction failure pattern.
- [LiveFMBench: Unveiling the Power and Limits of Agentic Workflows in Specification Generation](../Inbox/2026-05-02--livefmbench-unveiling-the-power-and-limits-of-agentic-workflows-in-specification-generation.md): LiveFMBench dataset, faithfulness filtering, prover checks, and measured accuracy drop.
- [Claw-Eval-Live: A Live Agent Benchmark for Evolving Real-World Workflows](../Inbox/2026-04-30--claw-eval-live-a-live-agent-benchmark-for-evolving-real-world-workflows.md): Claw-Eval-Live trace-based grading and public model pass rates.

### Testing and security use bounded model review
Security and testing papers give the model a constrained job, then verify the output against a concrete signal. FeedbackLLM feeds uncovered line and branch data back into later prompts for C and Python test generation. Its reported gains are large on several PALS/RERS programs, although the excerpt also shows weaker cases and no aggregate mean coverage.

QASecClaw keeps Semgrep as the high-recall scanner, then asks a coding-focused large language model to judge each finding with source context. On OWASP Benchmark v1.2, false positives fall from 560 to 64, with recall down by 3.1%. VulKey takes a similar bounded approach for repair: it predicts repair patterns using CWE type, syntactic action, and security-specific key elements, then generates a patch. On PrimeVul, it reports 31.5% repair accuracy, 7.6 percentage points above the best baseline in the excerpt.

#### Evidence
- [FeedbackLLM: Metadata driven Multi-Agentic Language Agnostic Test Case Generator with Evolving prompt and Coverage Feedback](../Inbox/2026-05-02--feedbackllm-metadata-driven-multi-agentic-language-agnostic-test-case-generator-with-evolving-prompt-and-coverage-feedback.md): FeedbackLLM coverage-feedback loop, benchmark setup, and reported coverage results.
- [QASecClaw: A Multi-Agent LLM Approach for False Positive Reduction in Static Application Security Testing](../Inbox/2026-05-03--qasecclaw-a-multi-agent-llm-approach-for-false-positive-reduction-in-static-application-security-testing.md): QASecClaw Semgrep-plus-LLM design and OWASP false-positive results.
- [VulKey: Automated Vulnerability Repair Guided by Domain-Specific Repair Patterns](../Inbox/2026-05-03--vulkey-automated-vulnerability-repair-guided-by-domain-specific-repair-patterns.md): VulKey pattern-guided repair method and PrimeVul repair accuracy.

### Agent infrastructure is measured by full-task behavior
The week also treats orchestration and serving as measurable parts of agent performance. SAGA schedules an entire agent workflow on GPU clusters, rather than treating each model call as independent. The reason is concrete: agent tasks can make 10 to 100 chained calls with tool gaps, and request-level schedulers regenerate cache and inflate end-to-end latency.

On 64 A100 GPUs, SAGA reduces task completion time by 1.73x on SWE-bench and 1.55x on WebArena versus vLLM with automatic prefix caching. The tradeoff is explicit: peak throughput is about 30% lower than throughput-optimized batching. That kind of accounting matches the week’s broader standard. Agent work is judged by complete task time, stored traces, reproducible artifacts, and failure modes that users can inspect.

#### Evidence
- [SAGA: Workflow-Atomic Scheduling for AI Agent Inference on GPU Clusters](../Inbox/2026-05-01--saga-workflow-atomic-scheduling-for-ai-agent-inference-on-gpu-clusters.md): SAGA workflow-level scheduling problem, mechanisms, latency gains, and throughput tradeoff.
