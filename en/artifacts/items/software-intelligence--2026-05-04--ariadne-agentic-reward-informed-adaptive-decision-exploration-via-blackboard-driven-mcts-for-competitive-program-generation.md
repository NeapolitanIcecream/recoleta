---
source: arxiv
url: https://arxiv.org/abs/2605.02431v1
published_at: '2026-05-04T10:30:33'
authors:
- Minnan Wei
- Xiang Chen
- Xiaoshuai Niu
- Siyu Chen
topics:
- code-generation
- competitive-programming
- mcts
- llm-agents
- code-repair
- software-engineering
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# ARIADNE: Agentic Reward-Informed Adaptive Decision Exploration via Blackboard-Driven MCTS for Competitive Program Generation

## Summary
ARIADNE is an LLM-based competitive programming system that uses MCTS and a shared blackboard to plan, test, and repair code under a fixed search budget. It reports higher Pass@1 than agentic coding baselines on APPS, CodeContests, CodeContests+, LiveCodeBench, and two recent contest sets.

## Problem
- It addresses unreliable one-shot program generation for contest problems, where a model must choose the right algorithm, satisfy time and memory limits, and handle hidden edge cases.
- The problem matters because small strategy errors or missed edge cases can make generated code fail all hidden tests, even when the code looks plausible.
- Prior agent pipelines, MCTS code search, and blackboard coordination each miss part of the needed loop: adaptive planning, persistent failure evidence, and budget allocation.

## Approach
- ARIADNE treats program generation as a sequential decision process over states `(current code, blackboard evidence)`.
- MCTS chooses among five action families: strategy selection, code generation, test generation, quality evaluation, and code repair.
- The blackboard stores parsed constraints, candidate strategies, generated tests, counterexamples, diagnostics, and repair notes so later branches can reuse earlier evidence.
- Evaluation returns both a scalar reward and structured feedback. The reward uses weights of 0.6 for correctness, 0.2 for performance, and 0.2 for code structure.
- UCB-guided selection and reward backpropagation move the search budget toward branches with better test results and useful repairs.

## Results
- With GPT-4o, ARIADNE reports Pass@1 of 41.30 on APPS, 46.67 on CodeContests, 27.27 on CodeContests+, and 20.91 on LiveCodeBench.
- The paper says ARIADNE beats the strongest listed baseline, CodeSim, by up to 26.06 Pass@1 points.
- On the 2025 ICPC Asia Shenyang Regional Contest set, ARIADNE reports pass@1/3/5 of 3/13, 6/13, and 7/13, compared with 1/13, 4/13, and 5/13 for the best benchmark baseline.
- On the 2025 CCPC Fujian Invitational set, ARIADNE reports pass@1/3/5 of 4/13, 5/13, and 7/13, compared with 2/13, 2/13, and 5/13.
- The excerpt also claims further gains with DeepSeek-V3.2, but it does not provide exact DeepSeek-V3.2 scores.

## Link
- [https://arxiv.org/abs/2605.02431v1](https://arxiv.org/abs/2605.02431v1)
