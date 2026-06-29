---
kind: trend
trend_doc_id: 301
granularity: week
period_start: '2026-04-06T00:00:00'
period_end: '2026-04-13T00:00:00'
topics:
- coding-agents
- verification
- benchmarks
- security
- repo-scale-evaluation
run_id: materialize-outputs
aliases:
- recoleta-trend-301
tags:
- recoleta/trend
- topic/coding-agents
- topic/verification
- topic/benchmarks
- topic/security
- topic/repo-scale-evaluation
language_code: en
pass_output_id: 52
pass_kind: trend_synthesis
---

# Coding-agent research now treats verification surfaces as core system design

## Overview
This week’s coding-agent research is strongest when every important step leaves evidence. The center of gravity is executable control: written specs, exact edit spaces, runtime checks, and durable tool boundaries. Compared with the previous week, the brief gets more concrete about where that control lives: inside repository tasks, security repair flows, and agent write paths.

## Clusters

### Written specifications are becoming standard agent inputs
Across the week, strong papers kept pulling agent behavior into forms that can be checked outside the model. Requirements, contracts, architecture descriptors, and typed failure signals all act as hard surfaces for planning and review. The practical gain is clearer repo-scale work and fewer hidden assumptions in the loop. ReCodeAgent and REAgent tie generation to explicit task descriptions, while later work extends the same idea to formal specs and durable write paths.

#### Evidence
- [We need re-learn what AI agent development tools are in 2026](../Inbox/2026-04-07--we-need-re-learn-what-ai-agent-development-tools-are-in-2026.md)
- [REAgent: Requirement-Driven LLM Agents for Software Issue Resolution](../Inbox/2026-04-08--reagent-requirement-driven-llm-agents-for-software-issue-resolution.md)
- [Building an Internal Coding Agent at Zup: Lessons and Open Questions](../Inbox/2026-04-10--building-an-internal-coding-agent-at-zup-lessons-and-open-questions.md)
- [Can Coding Agents Be General Agents?](../Inbox/2026-04-10--can-coding-agents-be-general-agents.md)
- [From Helpful to Trustworthy: LLM Agents for Pair Programming](../Inbox/2026-04-11--from-helpful-to-trustworthy-llm-agents-for-pair-programming.md)
- [CODESTRUCT: Code Agents over Structured Action Spaces](../Inbox/2026-04-07--codestruct-code-agents-over-structured-action-spaces.md)

### Benchmarks are grading whole workflows, not just answers
Evaluation tightened around exact edits, end-to-end tasks, and runtime evidence. That changes what counts as success. Papers this week ask whether an agent can complete a repository task, follow design rules, expose what evidence it used, and stay within cost or action limits. Benchmarks such as CLI-Tool-Bench, SWD-Bench, and HiL-Bench point in the same direction: useful scores come from long tasks with visible constraints, not small isolated completions.

#### Evidence
- [Evaluating Repository-level Software Documentation via Question Answering and Feature-Driven Development](../Inbox/2026-04-08--evaluating-repository-level-software-documentation-via-question-answering-and-feature-driven-development.md)
- [Edit, But Verify: An Empirical Audit of Instructed Code-Editing Benchmarks](../Inbox/2026-04-06--edit-but-verify-an-empirical-audit-of-instructed-code-editing-benchmarks.md)
- [Evaluating LLM-Based 0-to-1 Software Generation in End-to-End CLI Tool Scenarios](../Inbox/2026-04-08--evaluating-llm-based-0-to-1-software-generation-in-end-to-end-cli-tool-scenarios.md)
- [HiL-Bench (Human-in-Loop Benchmark): Do Agents Know When to Ask for Help?](../Inbox/2026-04-10--hil-bench-human-in-loop-benchmark-do-agents-know-when-to-ask-for-help.md)
- [SysTradeBench: An Iterative Build-Test-Patch Benchmark for Strategy-to-Code Trading Systems with Drift-Aware Diagnostics](../Inbox/2026-04-06--systradebench-an-iterative-build-test-patch-benchmark-for-strategy-to-code-trading-systems-with-drift-aware-diagnostics.md)
- [Does Pass Rate Tell the Whole Story? Evaluating Design Constraint Compliance in LLM-based Issue Resolution](../Inbox/2026-04-07--does-pass-rate-tell-the-whole-story-evaluating-design-constraint-compliance-in-llm-based-issue-resolution.md)

### Verification and security checks are moving into the write path
Verification now sits inside the action loop for both coding and security work. Tests, runtime instrumentation, execution grounding, and guardrails are used as gates before an agent commit or repair is accepted. This week also kept a realistic view of limits: security work reports exploitable generated code and weak reliability in messy multi-step settings, even as systems like DeepGuard and Verify Before You Fix improve the checking path.

#### Evidence
- [TraceSafe: A Systematic Assessment of LLM Guardrails on Multi-Step Tool-Calling Trajectories](../Inbox/2026-04-08--tracesafe-a-systematic-assessment-of-llm-guardrails-on-multi-step-tool-calling-trajectories.md)
- [Nidus: Externalized Reasoning for AI-Assisted Engineering](../Inbox/2026-04-06--nidus-externalized-reasoning-for-ai-assisted-engineering.md)
- [DeepGuard: Secure Code Generation via Multi-Layer Semantic Aggregation](../Inbox/2026-04-10--deepguard-secure-code-generation-via-multi-layer-semantic-aggregation.md)
- [Broken by Default: A Formal Verification Study of Security Vulnerabilities in AI-Generated Code](../Inbox/2026-04-07--broken-by-default-a-formal-verification-study-of-security-vulnerabilities-in-ai-generated-code.md)
- [Resilient Write: A Six-Layer Durable Write Surface for LLM Coding Agents](../Inbox/2026-04-12--resilient-write-a-six-layer-durable-write-surface-for-llm-coding-agents.md)
- [Cryptographic delegation receipts to close the user-to-operator agent trust gap](../Inbox/2026-04-06--cryptographic-delegation-receipts-to-close-the-user-to-operator-agent-trust-gap.md)
