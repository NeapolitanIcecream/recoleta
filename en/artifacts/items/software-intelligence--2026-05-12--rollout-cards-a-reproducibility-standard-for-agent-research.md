---
source: arxiv
url: https://arxiv.org/abs/2605.12131v1
published_at: '2026-05-12T13:54:31'
authors:
- Charlie Masters
- Ziyuan Liu
- Stefano V. Albrecht
topics:
- agent-reproducibility
- rollout-traces
- evaluation-standards
- software-agents
- multi-agent-systems
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# Rollout Cards: A Reproducibility Standard for Agent Research

## Summary
The paper argues that agent research should publish rollout records, views, reporting rules, and omitted fields, not only headline scores. It proposes rollout cards and reports audits and re-scoring tests showing that reporting choices can change agent benchmark conclusions.

## Problem
- Agent evaluations often publish scores without the rollout records behind them, so later researchers cannot inspect model actions, tool calls, failures, timing, or environment state.
- Different scoring and reporting rules can assign different scores to the same agent behavior, which makes comparisons between systems unreliable.
- The issue matters for software agents, tool-use agents, multi-agent systems, and safety work because rerunning frontier rollouts can be expensive and the original model, tool, and environment setup may no longer exist.

## Approach
- A rollout card stores the evidence from each episode: task, environment state, observations, model outputs, tool calls, tool results, artifacts, timing, terminal status, and failures.
- Each card declares the view used for a reported score, the reporting rule that computed it, and a drops manifest listing which fields, rows, or structures the score used or omitted.
- The authors implement the specification in Ergon, an open-source reinforcement learning gym, while saying other systems can emit the same bundle format.
- They test the idea by converting public agent artifacts into rollout-card exports and by re-grading fixed benchmark outputs under different public reporting rules.

## Results
- In an audit of 50 popular training and evaluation repositories, none reported failed, errored, or skipped rollouts beside headline accuracy or score.
- The audit found 37 reporting-rule discrepancies across task success, cost/token accounting, and timing. Examples include MMLU gaps up to 24.6 percentage points from prompt templates, a 2.0x cached-token accounting difference, a $14.41 cost difference for the same model family in Aider cases, and a 3.1x runtime gap on matched hardware.
- The paper releases 21 rollout-card exports: 17 trace-publication exports and 4 analytic or recovered-view non-trace exports, covering tool use, software engineering, web interaction, multi-agent coordination, safety, and search.
- Re-grading fixed benchmark artifacts changed reported scores by up to 20.9 absolute percentage points and could swap GPT-4o and Claude 3.5 Sonnet rankings on tau-bench.
- On MLE-Bench, changing the medal/pass reporting definition changed pass rates from 34.2% to 13.3%.
- Reanalysis of public rollouts found concrete hidden signals: in GAP, 1,002 of 4,855 text-safe samples, or 20.64%, still made unsafe tool calls; in MAESTRO, failed runs had median 48 spans and 78,523 tokens versus 10 spans and 11,586 tokens for successful runs; in COPRA miniF2F logs, all 44 one-step attempts succeeded while only 74 of 864 longer attempts succeeded.

## Link
- [https://arxiv.org/abs/2605.12131v1](https://arxiv.org/abs/2605.12131v1)
