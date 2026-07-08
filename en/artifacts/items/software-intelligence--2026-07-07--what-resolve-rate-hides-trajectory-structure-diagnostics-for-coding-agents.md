---
source: arxiv
url: https://arxiv.org/abs/2607.06184v1
published_at: '2026-07-07T12:09:46'
authors:
- Rui Shu
- Chun Yong Chong
- Xin Zhou
- Yun Peng
- Zihan Wu
- Xu Han
- Zeyang Zhuang
- Guowen Yuan
- Yuan Wang
topics:
- coding-agents
- trajectory-analysis
- swe-bench
- agent-evaluation
- code-intelligence
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# What Resolve Rate Hides: Trajectory Structure Diagnostics for Coding Agents

## Summary
TraceProbe diagnoses coding-agent runs by turning raw traces into comparable action sequences and rule-based process signals. It adds process evidence to SWE-Bench-style resolve rate, so developers can see where agents searched, edited, validated, failed, or wasted work.

## Problem
- Resolve rate only says whether the final patch passed target tests. It misses why a run failed or why a passing run used extra steps, tokens, and tool calls.
- Raw agent traces mix reads, searches, edits, commands, plans, reasoning, and logs in scaffold-specific formats, which makes cross-agent comparison hard.
- The problem matters for code-agent development because two agents can solve the same task with very different costs and failure recovery patterns.

## Approach
- TraceProbe normalizes each run into 9 canonical action types: file read, file write, search, command, sub-agent spawn, plan, navigate, fetch, and reason.
- It assigns deterministic effect labels such as survived, failed, reverted, justified, recorded, off-anchor, and reasoning based on observed trace state.
- The Insight module scans one trajectory for named anti-patterns with fixed rules, including search loops, re-read churn, redundant search, verification skips, and unsupported completion claims.
- The Converge module aligns two runs with sequence matching, then labels unmatched or reordered spans as divergences such as off-anchor exploration, scope drift, and rapid rewrite.
- Gold SWE-Bench patches supply anchor files when available, so TraceProbe can measure first relevant read, first relevant write, all anchors written, first passing validation, and first justified action.

## Results
- The study applies TraceProbe to 2,500 trajectories on SWE-Bench Verified across 5 production settings, 3 scaffolds, and 3 model backbones.
- In the paper’s motivating SWE-Bench pytest-7982 example, Claude Code with Opus 4.6 resolves the task in 10 steps with no failed actions, while OpenCode with GLM-5 also resolves it in 49 steps with repeated failed and recovery spans.
- The paper claims file-level choice is too coarse for separating success from failure; function selection and completion behavior give more local failure evidence.
- Search loops are reported as the most stable Insight anti-pattern across checks, while other anti-patterns are more split-sensitive. The excerpt does not provide rates, confidence intervals, or effect sizes for these detector gaps.
- Converge finds that even resolved runs differ in time to reach relevant code, amount of failed work, and scaffold/model-specific process changes. The excerpt does not provide aggregate milestone medians or resolve-rate deltas.

## Link
- [https://arxiv.org/abs/2607.06184v1](https://arxiv.org/abs/2607.06184v1)
