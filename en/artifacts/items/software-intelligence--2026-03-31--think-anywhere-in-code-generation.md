---
source: arxiv
url: http://arxiv.org/abs/2603.29957v2
published_at: '2026-03-31T16:24:03'
authors:
- Xue Jiang
- Tianyu Zhang
- Ge Li
- Mengyang Liu
- Taozhi Chen
- Zhenhua Xu
- Binhua Li
- Wenpin Jiao
- Zhi Jin
- Yongbin Li
- Yihong Dong
topics:
- code-generation
- reasoning-llm
- reinforcement-learning
- test-time-reasoning
- code-benchmarks
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Think Anywhere in Code Generation

## Summary
Think-Anywhere changes code generation from one upfront reasoning block to reasoning that can be inserted during code writing. The paper claims this gives better pass@1 results on four code benchmarks and helps the model place extra reasoning near hard code positions.

## Problem
- Standard reasoning LLMs usually think once before generating code. In code tasks, many bugs appear during implementation, after the initial plan is already fixed.
- Code difficulty is uneven across tokens and lines. Boilerplate needs little reasoning, while algorithm choices and edge cases need more.
- Prompting alone does not reliably teach a model to pause and think inside code generation, so the behavior needs training.

## Approach
- The method lets the model emit normal code plus inline reasoning blocks marked with `<thinkanywhere>...</thinkanywhere>` at any token position, while the final executable code is obtained by stripping all reasoning blocks.
- Training has two stages: a cold-start supervised phase on about 5,000 auto-constructed samples that demonstrate inline reasoning, then RL with verifiable rewards so the model learns where to trigger reasoning.
- The RL setup uses GRPO and a reward that combines format checks for the required reasoning structure with binary execution correctness from test cases.
- The paper also tests a special-token variant, Think-Anywhere*, where the inline reasoning trigger is a dedicated vocabulary token initialized from existing token embeddings plus delimiter embeddings.
- Default experiments use Qwen2.5-Coder-7B-Instruct, 14K programming problems from the Skywork dataset, pass@1 evaluation, and four benchmarks: LeetCode, LiveCodeBench, HumanEval, and MBPP.

## Results
- Main result: Think-Anywhere (Ours) reaches **70.3 average pass@1**, above the **61.0** base model, **68.4** standard GRPO baseline, and **66.8** CodeRL+.
- By benchmark, Think-Anywhere (Ours) scores **69.4** on LeetCode, **37.2** on LiveCodeBench, **91.5** on HumanEval, and **82.9** on MBPP. The base model gets **50.6 / 34.3 / 88.4 / 70.7** on the same datasets.
- Against the strongest listed post-training baseline, CodeRL+, Think-Anywhere improves average pass@1 by **3.5 points** (**70.3 vs 66.8**).
- Against GRPO, Think-Anywhere improves average pass@1 by **1.9 points** (**70.3 vs 68.4**), with gains on LeetCode (**69.4 vs 67.3**), LiveCodeBench (**37.2 vs 36.0**), HumanEval (**91.5 vs 88.6**), and MBPP (**82.9 vs 81.7**).
- RL is important in their setup: Think-Anywhere (Prompting) gets **56.9** average and Think-Anywhere (SFT) gets **60.6**, both below the RL-trained version at **70.3**.
- The special-token version, Think-Anywhere* (Ours), reaches **70.0** average, close to the text-tag version's **70.3**. The paper also claims analysis shows the model tends to insert reasoning at higher-entropy positions, though the excerpt does not give a numeric entropy correlation.

## Link
- [http://arxiv.org/abs/2603.29957v2](http://arxiv.org/abs/2603.29957v2)
