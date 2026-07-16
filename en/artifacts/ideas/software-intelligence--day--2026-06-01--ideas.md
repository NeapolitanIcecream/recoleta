---
kind: ideas
granularity: day
period_start: '2026-06-01T00:00:00'
period_end: '2026-06-02T00:00:00'
run_id: debd82ff-59fc-4b6d-b45d-fbe007d59cb3
status: succeeded
topics:
- agent systems
- coding agents
- software engineering
- monitoring
- code review
- requirements engineering
tags:
- recoleta/ideas
- topic/agent-systems
- topic/coding-agents
- topic/software-engineering
- topic/monitoring
- topic/code-review
- topic/requirements-engineering
language_code: en
pass_output_id: 223
pass_kind: trend_ideas
upstream_pass_output_id: 222
upstream_pass_kind: trend_synthesis
---

# Agent Reliability Engineering Interfaces

## Summary
Agent reliability work is moving into ordinary engineering surfaces: compiler output, monitoring queues, IDE review flows, and pre-action gates. The most practical changes are small enough to pilot inside one language toolchain, one regulated agent workflow, or one code-review path.

## Agent-facing compiler diagnostics for typed repair loops
Compiler and type-checker teams should add an agent-facing diagnostic mode that emits the full repair context to coding agents while keeping the existing concise messages for developers. The Type-Error Ablation study tested this directly in Shplait: 2,400 qwen2.5-coder:14b repair trials compared full unification-stack output, proximate error location, minimal type errors, and untyped test-suite feedback. Richer typed diagnostics improved repair behavior, and 97.9% of repairs that removed the type error also passed the semantic tests.

A cheap pilot is a feature flag in a typed language server or CI repair harness. When an agent is the consumer, the tool can include full constraint traces, inferred types, candidate origin sites, and failing test summaries in a structured artifact. The team can replay recent type failures through the current diagnostic mode and the agent-facing mode, then compare fix rate, semantic-test pass rate, and number of edit attempts. This is a concrete toolchain change for teams already letting agents read compiler output and patch code.

### Sources
- [Type-Error Ablation and AI Coding Agents](../Inbox/2026-06-01--type-error-ablation-and-ai-coding-agents.md): Summarizes the Shplait experiment, diagnostic modes, 2,400 qwen2.5-coder trials, and the 97.9% semantic-test result.
- [Type-Error Ablation and AI Coding Agents](../Inbox/2026-06-01--type-error-ablation-and-ai-coding-agents.md): States the controlled comparison between unification-stack context, proximate location, minimal type error, and dynamic test feedback.
- [Type-Error Ablation and AI Coding Agents](../Inbox/2026-06-01--type-error-ablation-and-ai-coding-agents.md): States the primary experiment scale and the authors’ recommendation to consider separate human and AI reporting modes.

## Structural monitors with severity routing for document-heavy agents
Teams running multi-stage agents in audit, finance, healthcare, legal, or other document-heavy workflows should test structural monitors before tuning task-level accuracy alerts. The monitoring study found that integration defects can hide task-level signals: within-run monitors found deterministic stage defects with CV = 0.02, cross-run monitors found variable failures with CV = 1.25, and a structural monitor found an integration gap with CV = 0.00. Its triage method sent 97% of findings to automated tracking and about 2% to human investigation.

The build is an evaluation layer with three scopes: checks inside a single run, repeated-run variance checks, and explicit checks for missing or broken stage connections. Findings should carry severity labels that determine whether they go to an analyst queue or automated tracking. A pilot can replay a small batch of real or synthetic cases through the current agent and measure how many alerts are deterministic low-severity defects, how many vary across runs, and how much human review volume the severity routing removes.

### Sources
- [Monitoring Agentic Systems Before They're Reliable](../Inbox/2026-06-01--monitoring-agentic-systems-before-they-re-reliable.md): Describes the three monitoring scopes, variance signal, FMEA-style severity routing, synthetic audit-agent testbed, and 43x review-volume reduction.
- [Monitoring Agentic Systems Before They're Reliable](../Inbox/2026-06-01--monitoring-agentic-systems-before-they-re-reliable.md): Gives the paper’s claim that structural defects dominate early production agent failures and describes the monitoring and triage method.
- [Monitoring Agentic Systems Before They're Reliable](../Inbox/2026-06-01--monitoring-agentic-systems-before-they-re-reliable.md): Reports that task-level errors were indistinguishable from clean baselines and that deterministic triage routed 97% of findings to automated tracking.

## Risk-ranked IDE review flow for LLM-generated multi-file changes
IDE teams and developer-tooling groups should add a review path for LLM-generated multi-file changes that starts with a change overview, ranks files by risk, and then guides reviewers to risky snippets. The JetBrains participatory design study found that practitioners treated trust calibration as the central review problem. Its proposed workflow has three levels: overview, file analysis, and code-snippet review, with constructs such as risk-per-file, risk-per-line, judge, walk-through, zooming in/out, and security cage.

The first version can be a pull-request or IDE extension that combines agent action logs, test results, changed-file metadata, ownership data, and static-analysis warnings into a file risk score. Reviewers should still inspect the code, but the tool can make large generated changes less opaque by showing where the agent touched sensitive code, crossed module boundaries, or changed security-relevant paths. The next check is a controlled review task measuring defect detection, review time, and reviewer confidence against a normal diff view.

### Sources
- [Trust-Calibrated Code Review: A Participatory Design Study of Review Workflows for LLM-Generated Multi-File Changes](../Inbox/2026-06-01--trust-calibrated-code-review-a-participatory-design-study-of-review-workflows-for-llm-generated-multi-file-changes.md): Summarizes the trust-calibrated review problem, the three-level workflow, design constructs, validation survey, and evidence limits.
- [Trust-Calibrated Code Review: A Participatory Design Study of Review Workflows for LLM-Generated Multi-File Changes](../Inbox/2026-06-01--trust-calibrated-code-review-a-participatory-design-study-of-review-workflows-for-llm-generated-multi-file-changes.md): States the JetBrains study method, the N=43 prototype evaluation, and the workflow constructs including risk-per-line and risk-per-file.
