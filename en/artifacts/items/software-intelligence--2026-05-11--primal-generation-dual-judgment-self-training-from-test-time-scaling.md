---
source: arxiv
url: https://arxiv.org/abs/2605.11299v2
published_at: '2026-05-11T22:34:45'
authors:
- Yizhu Jiao
- Ruixiang Zhang
- Richard Bai
- Jiawei Han
- Ronan Collobert
- Yizhe Zhang
topics:
- code-generation
- self-training
- test-time-scaling
- reinforcement-learning
- program-ranking
- livecodebench
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Primal Generation, Dual Judgment: Self-Training from Test-Time Scaling

## Summary
DuST trains a code model to judge its own generated solutions using execution labels, then uses the same trained model for code generation. The paper claims this ranking-only GRPO training improves both judging and pass@1 generation on LiveCodeBench.

## Problem
- Code models often get only a sparse pass/fail signal for one generated program, which gives little information about near-miss solutions.
- Generate-then-judge test-time scaling samples several programs and ranks them, but standard pipelines discard the ranking signal after inference.
- Better reuse of that signal matters because it can reduce repeated sampling cost and improve the generator itself.

## Approach
- For each programming problem, the base model samples many candidate programs; the authors use 64 candidates per problem in the main data construction.
- A sandbox executes each candidate and assigns a binary correctness label: passes all tests or fails.
- Candidates are grouped in sets of 4, and only mixed groups with at least one correct and one incorrect solution are kept.
- The model receives the problem and candidate set, outputs a ranking, and gets reward for placing correct programs above incorrect ones. This gives n+ × n- pairwise comparisons per group.
- GRPO updates the same model parameters used later for generation; the reward is only for ranking quality, and generated code receives no direct correctness reward.

## Results
- Training data: about 10K de-duplicated rSTARcoder problems; 64 sampled candidates per problem; about 6.9K valid queries and 37K training groups for the primary model.
- Qwen3-30B-Thinking on LiveCodeBench v6: pass@1 rises from 65.4% to 68.5% (+3.1), judgment NDCG from 70.1 to 76.3 (+6.2), and Best-of-4 accuracy from 68.7% to 72.6% (+3.9).
- Qwen3-30B-Thinking on LiveCodeBench v5: pass@1 rises from 69.2% to 71.0% (+1.8), NDCG from 76.0 to 78.2 (+2.2), and Best-of-4 accuracy from 72.3% to 75.2% (+2.9).
- GPT-OSS-20B on LiveCodeBench v6 improves Best-of-4 accuracy from 65.2% to 69.4% (+4.2), and on v5 from 67.5% to 72.8% (+5.3).
- Qwen3-4B-Thinking on LiveCodeBench v6 improves Best-of-4 accuracy from 55.0% to 59.4% (+4.4); Qwen3-30B-Instruct improves from 43.1% to 47.1% (+4.0).
- In the Qwen3-30B-Thinking ablation on LiveCodeBench v6, off-policy ranking reaches 72.6% TTS accuracy, 68.3% generation pass@1, and 76.3 NDCG, beating on-policy generation at 71.4%, 67.1%, and 74.6 respectively.

## Link
- [https://arxiv.org/abs/2605.11299v2](https://arxiv.org/abs/2605.11299v2)
