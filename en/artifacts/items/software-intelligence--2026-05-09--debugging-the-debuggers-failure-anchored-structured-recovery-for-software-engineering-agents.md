---
source: arxiv
url: https://arxiv.org/abs/2605.08717v1
published_at: '2026-05-09T06:02:08'
authors:
- Chenyu Zhao
- Shenglin Zhang
- Yihang Lin
- Wenwei Gu
- Zhimin Chen
- Yongqian Sun
- Dan Pei
- Chetan Bansal
- Saravan Rajmohan
- Minghua Ma
topics:
- software-engineering-agents
- agent-recovery
- code-intelligence
- telemetry
- failure-diagnosis
- aiops
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Debugging the Debuggers: Failure-Anchored Structured Recovery for Software Engineering Agents

## Summary
PROBE improves post-failure recovery for software engineering agents by turning failed-run telemetry into evidence-grounded retry guidance. It targets failed agent runs in code repair, enterprise workflows, and AIOps service mitigation.

## Problem
- Software engineering agents fail after tool errors, unchecked outcomes, wrong workflow state, or premature submission; manual recovery is slow and inconsistent.
- A final benchmark failure label does not show which step broke, which evidence matters, or what the next attempt should change.
- In 257 unresolved first attempts, 172 cases (66.93%) came from insufficient validation, tool/subprocess failure handling, or state/workflow error.

## Approach
- PROBE records span-level telemetry from failed runs, including metrics, logs, traces, agent intent, tool-environment state, and optional evaluator outcomes.
- It localizes failure evidence with metric anomaly checks using MAD-based z-scores, empirical quantiles, Isolation Forest, log signatures, repeated tool failures, trace patterns, and evaluator signals.
- It fuses related findings into structured evidence records with anchors, time scope, severity, support, conflicts, and provenance.
- An anchor-first diagnosis step emits structured fields such as failure anchor, primary cause, behavioral mistake, contributing factors, evidence, and confidence.
- A Guidance Gate produces retry guidance with a target, operation, verification signal, and boundary condition only when the diagnosis is evidence-grounded, actionable, and within agent-side control.

## Results
- The evaluation covers 257 initially unresolved cases across SWE-bench, EnterpriseOps-Gym, and AIOpsLab: 102, 106, and 49 cases respectively.
- PROBE reports 65.37% Top-1 diagnosis accuracy, 43.58 percentage points above the strongest non-PROBE baseline.
- PROBE reports a 21.79% recovery rate, 12.45 percentage points above the strongest non-PROBE baseline.
- The paper reports a diagnosis-recovery gap: 65.37% diagnosis accuracy versus 21.79% recovery, so correct diagnosis often does not translate into a successful next run.
- A Microsoft IcM prototype attaches PROBE as a side channel with 0 required changes to the agent policy, toolset, or execution budget; the excerpt gives no quantitative IcM success metric.

## Link
- [https://arxiv.org/abs/2605.08717v1](https://arxiv.org/abs/2605.08717v1)
