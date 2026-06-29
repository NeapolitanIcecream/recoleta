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
language_code: zh-CN
---

# QiMeng-PRepair: Precise Code Repair via Edit-Aware Reward Optimization

## Summary
## 摘要
这篇论文针对基于 LLM 的代码修复中的过度编辑问题：模型常常通过重写过多正确代码来修复 bug。PRepair 训练模型做更小、更有针对性的修改，文中报告的 Python 和 Verilog 修复基准提升幅度很大。

## 问题
- 标准的代码修复训练只优化正确性，所以模型可以在通过测试的同时重写程序的大部分内容。
- 过多的修改会让 bug 定位更差，也会增加人工审查成本，因为正确代码被覆盖了。
- 论文还指出一个数据问题：现实中的 buggy code 很少，尤其是那种大部分逻辑正确、只有一个局部故障的样本。

## 方法
- 论文把 **precise repair** 定义为在修复 bug 的同时尽量复用正确代码，并引入 **fix_p@k** 来同时评估正确性和编辑规模。
- 它用 buggy 输入和生成修复之间的归一化行级 Levenshtein 距离来衡量编辑规模。
- **Self-Breaking** 通过向正确程序注入 bug 来生成训练数据，然后用基于编辑距离相似度的 min-max sampling 保留一个多样化子集。
- **Self-Repairing** 使用 **Edit-Aware GRPO (EA-GRPO)** 训练模型。它只在一个 rollout group 达到选定的准确率阈值后才加入编辑惩罚。
- 奖励函数把正确性作为主要目标，然后在同一组中优先选择那些比其他正确候选改动更少行的正确候选。

## 结果
- 论文报告 **fix_1@1** 的修复精度最高提升 **31.4%**。
- 在 **Python / HumanEvalFix** 上，**Qwen2.5-Coder-7B + EA-GRPO** 达到 **91.19 pass@1** 和 **81.62 fix_1@1**；**+GRPO** 分别是 **89.82 pass@1** 和 **47.44 fix_1@1**。也就是 **fix_1@1** 提升 **34.18** 个点，**pass@1** 只提升 **1.37** 个点。
- 在 **Verilog** 基准上，**Qwen2.5-Coder-7B + EA-GRPO** 达到 **68.66 pass@1** 和 **68.11 fix_1@1**；**+GRPO** 分别是 **68.37 pass@1** 和 **8.49 fix_1@1**。也就是 **fix_1@1** 提升 **59.62** 个点，而 **pass@1** 几乎不变。
- 在 **Python** 上，**Qwen2.5-Coder-3B + EA-GRPO** 的 **fix_1@1** 是 **67.96**，而 **+GRPO** 是 **34.27**；在 **Verilog** 上分别是 **37.40** 和 **18.55**。
- 论文指出，只优化正确性的 GRPO 在训练中会把 edit cost 推到 **0.6** 以上，它把这当作严重过度编辑的证据。
- 论文还说，和 speculative editing 一起使用时，较小的编辑会提高 draft-token acceptance，因此解码吞吐量更高，但摘录里没有给出具体吞吐量数字。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05963v1](http://arxiv.org/abs/2604.05963v1)
