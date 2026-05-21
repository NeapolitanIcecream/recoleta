---
source: arxiv
url: https://arxiv.org/abs/2605.05949v2
published_at: '2026-05-07T09:57:53'
authors:
- Yuliang Xu
- Xiang Xu
- Yao Wan
- Hu Wei
- Tong Jia
topics:
- multi-agent-systems
- code-generation
- algorithmic-reasoning
- competitive-programming
- software-agents
- retrieval-augmented-generation
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# MAS-Algorithm: A Workflow for Solving Algorithmic Programming Problems with a Multi-Agent System

## Summary
MAS-Algorithm is a five-agent workflow for competitive-programming problems. It improves acceptance rates for Qwen coding models by adding algorithm selection, retrieval, planning, coding, judging, and error feedback around the same base model.

## Problem
- Algorithmic programming tasks test whether coding models can choose algorithms, reason about constraints, and produce correct efficient code.
- Direct prompting gives weak control over intermediate reasoning, so errors in algorithm choice, complexity, edge cases, or implementation are hard to isolate.
- Fine-tuning can be expensive and gave small gains in this study, which makes inference-time coordination useful for code intelligence systems.

## Approach
- Agent1 selects likely algorithms and data structures from candidate labels, with support for multiple solution branches.
- Agent2 retrieves algorithm knowledge from a local OI-WIKI store using bge-zh embeddings and summarizes it for the solver.
- Agent3 writes a structured solution plan, Agent4 turns the plan into C++ code, and Agent5 diagnoses failures.
- A judging tool compiles and runs code in a Docker gcc environment, compares outputs, and sends failed cases back to Agent5.
- Agent5 returns PASS, FIX, or RETHINK, routing the workflow back to code revision or solution replanning until success or an iteration limit.

## Results
- On the self-built dataset, MAS-Algorithm improved average AC rate across five Qwen models by 6.48 percentage points over direct prompting, with gains from +4.39 to +9.00 points.
- Qwen3-14B rose from 28.98% AC to 37.98% AC, a +9.00 point gain; its case pass rate rose from 29.34% to 40.14%, a +10.80 point gain.
- Qwen3-Coder-30B-A3B-Instruct rose from 32.25% AC to 38.87% AC, a +6.62 point gain. LoRA fine-tuning on accepted solutions improved direct prompting only to 33.14% AC, a +0.89 point gain.
- Qwen3-235B-A22B-Instruct-2507 rose from 62.87% AC to 67.26% AC, a +4.39 point gain.
- On LiveCodeBench-Pro, Qwen3-Coder-30B-A3B-Instruct improved from 5.28% AC to 10.00% AC, a +4.72 point gain; case pass rate rose from 9.07% to 14.05%.
- Replacement studies reported large upper-bound gains: improving Agent3 reached 66.57% AC, +27.70 points over the base MAS-Algorithm setting in that experiment; improving Agent2 reached 61.82% AC, +22.95 points.

## Link
- [https://arxiv.org/abs/2605.05949v2](https://arxiv.org/abs/2605.05949v2)
