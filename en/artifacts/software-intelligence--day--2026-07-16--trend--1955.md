---
kind: trend
trend_doc_id: 1955
granularity: day
period_start: '2026-07-16T00:00:00'
period_end: '2026-07-17T00:00:00'
topics:
- agent reliability
- evidence gating
- coding agents
- dynamic tools
- domain evaluation
run_id: materialize-outputs
aliases:
- recoleta-trend-1955
tags:
- recoleta/trend
- topic/agent-reliability
- topic/evidence-gating
- topic/coding-agents
- topic/dynamic-tools
- topic/domain-evaluation
language_code: en
pass_output_id: 330
pass_kind: trend_synthesis
---

# Executable gates expose failures that static agent scores miss

## Overview
Recent momentum around engineered checks is becoming more operational. Today’s evidence favors controls tied to actual source state, tool versions, and domain rules. Static or text-only success can hide supply-chain, workflow, and adaptation failures. The studies are mostly narrow or early-stage, so they establish concrete failure modes rather than broad production reliability.

## Findings

### Evidence-gated execution
Reliable automation increasingly depends on deterministic controls outside the model. A setup-security study found that agents usually missed malicious package sources across ecosystems; prompts only helped for the attack dimension they named, while a pre-install check covering names, sources, and versions closed most of the observed gap. Proof-or-Stop applies the same principle to lifecycle decisions: claims such as “tested” or “done” advance only with fresh evidence bound to the tracked source state. Its gated loop recorded zero false-done outcomes in 10 scenarios and rejected all 18 tested receipt-tampering classes, though evaluation was limited to one model family and a self-hosted corpus.

#### Sources
- [Setup Complete, Now You Are Compromised: Weaponizing Setup Instructions Against AI Coding Agents](../Inbox/2026-07-16--setup-complete-now-you-are-compromised-weaponizing-setup-instructions-against-ai-coding-agents.md): Reports cross-ecosystem source blind spots and the effect of deterministic pre-install verification.
- [Proof-or-Stop: Don't Trust the Agent, Trust the Evidence -- Loop Engineering for Verifiable Evidence-Gated Lifecycle Control](../Inbox/2026-07-16--proof-or-stop-don-t-trust-the-agent-trust-the-evidence-loop-engineering-for-verifiable-evidence-gated-lifecycle-control.md): Reports 10/10 scenarios with zero false-done and rejection of 18 tamper classes, alongside evaluation limits.

### Domain-complete evaluation
Benchmarks are treating the full executable workflow—not plausible code or a final answer—as the unit of success. Alipay-PIBench tests payment integration with end-to-end behavior, signature and notification handling, refund safeguards, and business-state consistency; supplying an official domain skill raised mean rubric pass rate by 10.31 percentage points. StructureClaw requires a linked chain of models, validation records, solver outputs, and reports, raising average success from 56.8% to 88.6% with its governed workflow. Kaleidoscope extends the pattern to deployed applications by calibrating application-specific judges against human labels, but its evidence remains an uncontrolled four-use-case pilot.

#### Sources
- [Alipay-PIBench: A Realistic Payment Integration Benchmark for Coding Agents](../Inbox/2026-07-16--alipay-pibench-a-realistic-payment-integration-benchmark-for-coding-agents.md): Defines progressive payment-risk scenarios and reports a 10.31-point average gain from domain skills.
- [StructureClaw: Traceable LLM Agents and an Executable Benchmark for Structural Engineering Workflows](../Inbox/2026-07-16--structureclaw-traceable-llm-agents-and-an-executable-benchmark-for-structural-engineering-workflows.md): Reports the workflow-level success increase from 56.8% to 88.6%.
- [Project Kaleidoscope: Contextual, Human-Aligned Evaluation for Real-World AI Applications](../Inbox/2026-07-16--project-kaleidoscope-contextual-human-aligned-evaluation-for-real-world-ai-applications.md): Describes contextual rubrics, human calibration, and the limited three-week pilot.

### Changing and multimodal conditions
Controlled evaluations show that capability measured in a fixed, text-dominant environment does not transfer cleanly. On evolved Model Context Protocol (MCP) servers, GPT-5.4 and Claude-Sonnet-4-6 lost 13.7% and 14.4% task performance. In repository localization with screenshots and other visual evidence, the strongest agent reached only 38.96 file Acc@5 and 22.45 function Acc@10. Maintenance evidence points to a related scope problem: 28 of 64 sampled AI/ML issues required changes beyond production code, including prompts, datasets, dependencies, and runtime configuration. Evaluation therefore needs to preserve environmental change and heterogeneous artifacts rather than reducing work to a static code snapshot.

#### Sources
- [MCPEvol-Bench: Benchmarking LLM Agent Performance Across Dynamic Evolutions of MCP Servers](../Inbox/2026-07-16--mcpevol-bench-benchmarking-llm-agent-performance-across-dynamic-evolutions-of-mcp-servers.md): Reports frontier-model degradation under realistic MCP server evolution.
- [MM-IssueLoc: A Controlled Benchmark for Evaluating Visual Evidence in Multimodal Repository-Level Issue Localization](../Inbox/2026-07-16--mm-issueloc-a-controlled-benchmark-for-evaluating-visual-evidence-in-multimodal-repository-level-issue-localization.md): Reports low file- and function-localization accuracy under multimodal repository evidence.
- [Rethinking Issue Resolution for AI/ML Systems](../Inbox/2026-07-16--rethinking-issue-resolution-for-ai-ml-systems.md): Finds iterative workflows spanning datasets, prompts, model configurations, and other non-code artifacts.
