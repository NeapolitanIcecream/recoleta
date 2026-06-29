---
source: arxiv
url: http://arxiv.org/abs/2604.03632v1
published_at: '2026-04-04T08:03:03'
authors:
- Ruwei Pan
- Jiangshuai Wang
- Qisheng Zhang
- Yueheng Zhu
- Linhao Wu
- Zixiong Yang
- Yakun Zhang
- Lu Zhang
- Hongyu Zhang
topics:
- repository-level-code-generation
- code-generation
- llm-agents
- cross-attempt-optimization
- software-engineering
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Persistent Cross-Attempt State Optimization for Repository-Level Code Generation

## Summary
LiveCoder improves repository-level code generation by carrying task-specific state across repeated attempts on the same task. It stores what worked, what failed, and the best repository found so far, then uses that state to guide later attempts and avoid regression.

## Problem
- Repository-level code generation often needs several full attempts because models must coordinate multiple files, modules, and dependencies.
- Existing methods usually optimize each attempt separately, so later attempts can repeat bad paths, forget useful partial solutions, and even score worse than an earlier repository.
- This matters because repeated full-attempt generation is costly, unstable, and common in complex software tasks.

## Approach
- The paper proposes **LiveCoder**, a cross-attempt optimization framework for repository-level code generation.
- After each full attempt, LiveCoder updates three persistent state items: **Success Knowledge** from strong repositories, **Failure Knowledge** from weak repositories and execution feedback, and a **historical-best repository** with its score.
- Success and failure knowledge are stored as structured text extracted by an LLM from the generated repository plus test and runtime feedback; later attempts retrieve relevant entries by embedding similarity and inject them into generation.
- The historical-best repository is kept as a full artifact, so the system can reuse it directly if it already reaches full score, and always return the best-so-far result at the end.
- Within this loop, each new attempt is guided by prior evidence instead of starting from scratch.

## Results
- On **RAL-Bench**, LiveCoder reports up to **+22.94 percentage points** in functional score, up to **81.58%** repository reuse, and up to **53.63%** cost reduction from the first to the fourth attempt.
- On **RAL-Bench Table 1**, against the **Direct** baseline, LiveCoder reaches **58.20 vs 38.50** functional score on **GPT-5** (**+19.70 points**), **34.37 vs 24.37** on **DeepSeek-V3** (**+10.00**), **67.00 vs 39.32** on **Claude-Sonnet-4.5** (**+27.68**), and **69.16 vs 43.86** on **Gemini-3-Pro** (**+25.30**).
- On the same table, non-functional quality is often competitive or higher on stronger backbones: **Claude-Sonnet-4.5** rises from **49.64 to 64.81** and **Gemini-3-Pro** from **50.57 to 67.03**; the abstract says non-functional quality stays broadly stable overall.
- The paper gives a concrete motivating example where a baseline scores **86%**, then drops to **63%**, then reaches **79%** across three attempts, while LiveCoder improves **86% to 92%** and keeps the stronger repository when a later attempt is worse.
- The excerpt names **RAL-Bench** and **NL2Repo-Bench** as evaluation benchmarks, but the provided quantitative table only shows detailed numbers for **RAL-Bench**.

## Link
- [http://arxiv.org/abs/2604.03632v1](http://arxiv.org/abs/2604.03632v1)
