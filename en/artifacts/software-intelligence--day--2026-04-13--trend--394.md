---
kind: trend
trend_doc_id: 394
granularity: day
period_start: '2026-04-13T00:00:00'
period_end: '2026-04-14T00:00:00'
topics:
- coding-agents
- execution-verification
- software-analysis
- bug-validation
- traceability
run_id: materialize-outputs
aliases:
- recoleta-trend-394
tags:
- recoleta/trend
- topic/coding-agents
- topic/execution-verification
- topic/software-analysis
- topic/bug-validation
- topic/traceability
language_code: en
pass_output_id: 68
pass_kind: trend_synthesis
---

# Executable proof is becoming the standard output for coding agents

## Overview
The clearest signal for this day is that coding-agent work is tightening around executable proof. AgentForge, AnyPoC, and AnalysisBench all treat model output as a draft that must survive a concrete check: sandbox execution, reproducible analysis output, or a re-run proof-of-concept. That emphasis fits the recent run of papers on control surfaces and verification, but this set is more concrete about the artifact that must exist at the end: a passing patch, a valid analysis result, or a bug-triggering test.

## Clusters

### Verification in the loop
Execution is now the gate for agent claims. AgentForge requires every patch to run in a network-isolated Docker sandbox before it can move forward, and reports 40.0% resolution on SWE-bench Lite, with a 26 to 28 point gain over its single-agent baselines. AnalysisBench reaches the same conclusion in a different setting: agents need explicit stages and evidence-based stopping rules, because self-validation still overstated success by 15%. AnyPoC applies the pattern to security reports by generating and re-running executable proof-of-concept tests, then rejecting bug reports that fail that check.

#### Evidence
- [AgentForge: Execution-Grounded Multi-Agent LLM Framework for Autonomous Software Engineering](../Inbox/2026-04-13--agentforge-execution-grounded-multi-agent-llm-framework-for-autonomous-software-engineering.md): AgentForge makes sandbox execution mandatory and reports benchmark gains.
- [Evaluating LLM Agents on Automated Software Analysis Tasks](../Inbox/2026-04-13--evaluating-llm-agents-on-automated-software-analysis-tasks.md): AnalysisBench shows evidence-based completion checks and measured self-validation error.
- [AnyPoC: Universal Proof-of-Concept Test Generation for Scalable LLM-Based Bug Detection](../Inbox/2026-04-13--anypoc-universal-proof-of-concept-test-generation-for-scalable-llm-based-bug-detection.md): AnyPoC uses executable PoCs and independent re-execution to validate bug reports.

### Structured control and traceability
The strongest systems are writing down workflow boundaries, not just adding more model capacity. AnalysisAgent uses one action per cycle, deterministic log condensation, and manual verification of tool-specific outputs across 35 tool-project tasks. CodeTracer studies what happens when those boundaries are missing or weak. It reconstructs runs into state-transition trees, then locates the earliest failure-causing stage and step. On GPT-5 traces, step-level F1 rises to 48.02 from about 19 for lighter baselines, while token use drops to 31.1k from 44.8k to 58.5k. The practical message is clear: explicit stages help both execution and diagnosis.

#### Evidence
- [Evaluating LLM Agents on Automated Software Analysis Tasks](../Inbox/2026-04-13--evaluating-llm-agents-on-automated-software-analysis-tasks.md): AnalysisAgent shows staged orchestration and verified outcomes on end-to-end analysis tasks.
- [CodeTracer: Towards Traceable Agent States](../Inbox/2026-04-13--codetracer-towards-traceable-agent-states.md): CodeTracer quantifies failure localization gains and lower token use from structured traces.

### Operational proof across tougher tasks
This period also extends executable checking beyond coding benchmarks into harder real settings. AnyPoC works across 12 large software systems, including Chromium, Firefox, LLVM, OpenSSL, SQLite, FFmpeg, and Redis. It reports 1.3x more valid PoCs for true bug reports, 9.8x more rejected false positives, and 45 generated PoCs adopted as official regression tests. ORBIT, in a separate translation setting, couples project-level orchestration with compile and test repair, reporting 100% compilation success and 91.7% test success on 24 CRUST-Bench programs. The common thread is operational proof: compilation, tests, traces, and reproducing artifacts are becoming the accepted output, not just plausible text.

#### Evidence
- [AnyPoC: Universal Proof-of-Concept Test Generation for Scalable LLM-Based Bug Detection](../Inbox/2026-04-13--anypoc-universal-proof-of-concept-test-generation-for-scalable-llm-based-bug-detection.md): AnyPoC provides concrete multi-system results and adoption of generated PoCs as regression tests.
- [OOM-RL: Out-of-Money Reinforcement Learning Market-Driven Alignment for LLM-Based Multi-Agent Systems](../Inbox/2026-04-13--oom-rl-out-of-money-reinforcement-learning-market-driven-alignment-for-llm-based-multi-agent-systems.md): Additional evidence in the period shows hard external constraints and executable checks matter in deployed agent systems.
