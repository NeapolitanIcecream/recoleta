---
source: arxiv
url: http://arxiv.org/abs/2604.05963v1
published_at: '2026-04-07T14:56:38'
authors:
- Changxin Ke
- Rui Zhang
- Jiaming Guo
- Yuanbo Wen
- Li Ding
- Shuo Wang
- Xuyuan Zhu
- Xiong Peng
- Di Huang
- Zidong Du
- Xing Hu
- Qi Guo
- Yunji Chen
topics:
- program-repair
- code-intelligence
- reinforcement-learning
- llm-training
- speculative-decoding
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# QiMeng-PRepair: Precise Code Repair via Edit-Aware Reward Optimization

## Summary
This paper targets over-editing in LLM-based code repair: models often fix bugs by rewriting too much correct code. PRepair trains models to make smaller, targeted edits, and the reported gains are large on Python and Verilog repair benchmarks.

## Problem
- Standard code repair training optimizes correctness only, so models can pass tests while rewriting large parts of the program.
- Excess edits make bug localization worse and increase human review cost because correct code gets overwritten.
- The paper also points to a data problem: realistic buggy code with mostly-correct logic and a small local fault is scarce.

## Approach
- The paper defines **precise repair** as fixing the bug while reusing as much correct code as possible, and introduces **fix_p@k** to score both correctness and edit size.
- It measures edit size with normalized line-level Levenshtein distance between buggy input and generated repair.
- **Self-Breaking** creates training data by injecting bugs into correct programs, then keeps a diverse subset with min-max sampling over edit-distance-based similarity.
- **Self-Repairing** trains the model with **Edit-Aware GRPO (EA-GRPO)**, which adds an edit penalty only after a rollout group reaches a chosen accuracy threshold.
- The reward keeps correctness as the main target, then prefers correct candidates that change fewer lines than other correct candidates in the same group.

## Results
- The paper reports up to **31.4% improvement in fix_1@1** for repair precision.
- On **Python / HumanEvalFix**, **Qwen2.5-Coder-7B + EA-GRPO** reaches **91.19 pass@1** and **81.62 fix_1@1**, versus **89.82 pass@1** and **47.44 fix_1@1** for **+GRPO**. That is **+34.18 points** on **fix_1@1** with a small **+1.37 points** on **pass@1**.
- On **Verilog** benchmark, **Qwen2.5-Coder-7B + EA-GRPO** reaches **68.66 pass@1** and **68.11 fix_1@1**, versus **68.37 pass@1** and **8.49 fix_1@1** for **+GRPO**. That is **+59.62 points** on **fix_1@1** with near-identical **pass@1**.
- On **Python**, **Qwen2.5-Coder-3B + EA-GRPO** gets **67.96 fix_1@1** versus **34.27** for **+GRPO**; on **Verilog**, it gets **37.40** versus **18.55**.
- The paper states correctness-only GRPO can drive edit cost above **0.6** during training, which it uses as evidence of severe over-editing.
- It also claims higher decoding throughput when paired with speculative editing because smaller edits increase draft-token acceptance, but the excerpt does not provide exact throughput numbers.

## Link
- [http://arxiv.org/abs/2604.05963v1](http://arxiv.org/abs/2604.05963v1)
