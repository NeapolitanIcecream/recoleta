---
source: arxiv
url: https://arxiv.org/abs/2605.21850v1
published_at: '2026-05-21T00:47:03'
authors:
- Qisheng Su
- Zhen Fang
- Shiting Huang
- Yu Zeng
- Yiming Zhao
- Kou Shi
- Ziao Zhang
- Lin Chen
- Zehui Chen
- Lijun Wu
- Feng Zhao
topics:
- long-context-training
- agent-trajectories
- software-engineering-agents
- code-intelligence
- supervised-fine-tuning
- tool-use-data
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# ACC: Compiling Agent Trajectories for Long-Context Training

## Summary
ACC turns completed agent runs into long-context QA training examples, so a model learns to answer from evidence spread across tool outputs. On Qwen3-30B-A3B-Thinking, it improves MRCR and GraphWalks while leaving general benchmarks mostly unchanged.

## Problem
- Long-context LLM training often needs curated long documents or synthetic contexts, which cost time and can miss the dependencies created during real problem solving.
- Agent trajectories contain useful evidence across tool calls, but standard agent SFT masks tool responses and mainly trains next-action prediction.
- This matters for search, software engineering, and SQL agents because final answers often depend on evidence scattered across many turns.

## Approach
- Collect answer-verified trajectories from Search, SWE, and SQL agents: 10,802 total, with 3,369 Search, 4,368 SWE, and 3,065 SQL trajectories.
- Extract evidence pieces from each trajectory: visited pages plus distractors for Search, patch-related files plus inspected files for SWE, and queried tables for SQL.
- Shuffle and concatenate the evidence into one context, capped at 131,072 tokens, then pair the original question and compiled context with the final answer.
- Generate reasoning traces with DeepSeek-V3.2-Thinking and keep only traces that lead to the correct answer; reported pass rates are near 100% for Search, near 50% for SQL, and near 10% for SWE.
- Fine-tune Qwen3-30B-A3B-Thinking for 4 epochs with cross-entropy loss, global batch size 16, and learning rate 1e-5.

## Results
- MRCR overall rises to 68.28 from 50.19 on the Qwen3-30B-A3B-Thinking baseline, a +18.09 gain; 2-needle improves to 76.90 from 61.84, and 4-needle improves to 59.57 from 38.41.
- GraphWalks overall precision rises to 77.51 from 69.92, a +7.59 gain; Parents improves to 81.50 from 71.19, and BFS improves to 72.95 from 68.47.
- The ACC-trained Qwen3-30B-A3B model slightly exceeds Qwen3-235B-A22B-Thinking on these two long-range tests: MRCR 68.28 vs 67.51 and GraphWalks 77.51 vs 76.63.
- General benchmark scores stay close to or above the base model: GPQA-Diamond 70.20 vs 67.71, MMLU-Pro 76.00 vs 74.50, AIME’24 90.00 vs 90.00, AIME’25 90.00 vs 86.67, and IFEval 86.14 vs 86.69.
- The compiled training examples span 2K to 128K tokens, using a 131,072-token sequence length during fine-tuning.

## Link
- [https://arxiv.org/abs/2605.21850v1](https://arxiv.org/abs/2605.21850v1)
