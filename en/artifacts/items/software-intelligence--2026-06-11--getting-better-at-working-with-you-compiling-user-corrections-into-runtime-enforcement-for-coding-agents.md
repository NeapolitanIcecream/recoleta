---
source: arxiv
url: https://arxiv.org/abs/2606.13174v1
published_at: '2026-06-11T10:43:40'
authors:
- Yujun Zhou
- Kehan Guo
- Haomin Zhuang
- Xiangqi Wang
- Yue Huang
- Zhenwen Liang
- Pin-Yu Chen
- Tian Gao
- Nuno Moniz
- Nitesh V. Chawla
- Xiangliang Zhang
topics:
- coding-agents
- runtime-enforcement
- user-corrections
- agent-memory
- preference-compliance
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Getting Better at Working With You: Compiling User Corrections into Runtime Enforcement for Coding Agents

## Summary
Trace turns user corrections into runtime checks for coding agents, so the agent must satisfy the correction before it can finish a task. It targets the common failure where memory can recall a preference but the agent still violates it.

## Problem
- Coding agents often repeat the same user-specific mistakes across sessions, even after the correction is stored or retrieved.
- The paper measures this access-compliance gap and shows that memory alone does not make a correction binding.
- This matters because users have to restate the same constraint in future sessions, which breaks interactive work.

## Approach
- Trace scans user messages for correction signals, such as durable preferences or repeated friction.
- It rewrites each correction as an atomic rule with an applicability condition.
- It resolves each new rule against a per-user rule library using actions such as noop, update, supersede, split, or new.
- It compiles the rule into a runtime artifact with an applicability check, a behavior instruction, and a verifier.
- Hooks block task completion until the active verifier passes.

## Results
- On a diagnostic set built from 32 long-context coding-agent transcripts and 19 held-out tasks with 29 preference checks, Mem0 still left 57.5% of applicable preference checks violated.
- On ClawArena in-distribution tasks, Trace reduced violation rate from 100.0% to 37.6%; on out-of-distribution tasks, it reduced violation rate from 100.0% to 2.0%.
- On MemoryArena-derived in-distribution tasks, Trace reduced violation rate from 100.0% to 60.5% and matched or exceeded the strongest memory baseline on task pass.
- In ClawArena, Trace reduced average user turns from 2.00 with no memory to 1.37 in-distribution and 1.02 out-of-distribution.
- The paper reports simulation validation metrics of Precision 0.864, Recall 0.953, F1 0.906, and Specificity 0.940 for the user simulator.

## Link
- [https://arxiv.org/abs/2606.13174v1](https://arxiv.org/abs/2606.13174v1)
