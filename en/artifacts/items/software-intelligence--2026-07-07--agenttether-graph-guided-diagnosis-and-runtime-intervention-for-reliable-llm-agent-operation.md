---
source: arxiv
url: https://arxiv.org/abs/2607.06273v1
published_at: '2026-07-07T13:40:31'
authors:
- Chenyu Zhao
- Shenglin Zhang
- Wenwei Gu
- Yongqian Sun
- Dan Pei
- Chetan Bansal
- Saravan Rajmohan
- Minghua Ma
topics:
- llm-agents
- agent-repair
- runtime-intervention
- graph-diagnosis
- tool-use
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# AgentTether: Graph-Guided Diagnosis and Runtime Intervention for Reliable LLM Agent Operation

## Summary
AgentTether is a runtime repair layer for LLM agents that diagnoses failed tool-use runs with a dependency graph, then guides and supervises the next run. It targets failures where an early wrong action causes later errors and one-shot feedback fades during long executions.

## Problem
- LLM agents in stateful tool workflows can fail because an early wrong tool call, missing action, or bad argument changes later state and causes downstream errors.
- Blind retry and outcome feedback do not identify the failing step, and self-reflection can repeat the same mistake without trace-grounded evidence.
- This matters for production agents because failed or risky actions can waste turns and tokens, violate workflow policy, or change external state incorrectly.

## Approach
- AgentTether records a run without changing the agent, then compresses the trace into Transition Units: observation, belief, action, and feedback for each decision cycle.
- It builds a Critical Transition Graph where nodes are Transition Units and edges capture time order plus shared-state dependencies between steps.
- It localizes suspicious subtrajectories with two detectors: a heterogeneous graph transformer trained on 21,143 success-only trajectories, and a run-local Isolation Forest over 25 graph-context features.
- An analyst LLM turns the localized evidence into a root cause, turning point, and recovery hints; a feedback builder converts this into short behavior-scoped guidance.
- Repair Memory carries fixed and unresolved directives across attempts, while a runtime harness checks for loops, intent drift, expectation deviation, and missing corrective actions before injecting guarded corrections.

## Results
- On 261 τ-bench tasks across Retail, Airline, and Banking with Qwen3.7-max, AgentTether repaired 69.11% of initially failed tasks.
- Against blind retry, it improved repair rate by 26.02 percentage points overall and by 32.53 percentage points on Banking.
- On Qwen3.7-max Banking, it repaired 59.04% of initially failed tasks, 49 out of 83.
- On GPT-5.4 Banking, it repaired 65.12% of initially failed tasks, 56 out of 86, showing transfer across agent backbones in the tested domain.
- Guarded runtime intervention added 12.05 percentage points on Qwen3.7-max Banking, where feedback adherence was weak.
- The paper also reports fewer agent turns and lower end-to-end approach tokens, but the excerpt does not give exact turn or token counts.

## Link
- [https://arxiv.org/abs/2607.06273v1](https://arxiv.org/abs/2607.06273v1)
