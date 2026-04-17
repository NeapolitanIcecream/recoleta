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
这篇论文针对基于 LLM 的代码修复中过度编辑的问题：模型常常通过重写过多原本正确的代码来修复缺陷。PRepair 训练模型进行更小、更有针对性的修改，论文报告称它在 Python 和 Verilog 修复基准上带来了显著提升。

## 问题
- 标准代码修复训练只优化正确性，因此模型可能在通过测试的同时重写程序的大部分内容。
- 过多编辑会让缺陷定位变差，并增加人工审查成本，因为正确代码会被覆盖。
- 论文还指出一个数据问题：带有少量局部错误、但大部分逻辑正确的真实缺陷代码较少。

## 方法
- 论文将 **precise repair** 定义为：在修复缺陷的同时尽可能复用正确代码，并引入 **fix_p@k** 同时衡量正确性和编辑规模。
- 它用有缺陷输入与生成修复结果之间、按行计算并归一化的 Levenshtein 距离来衡量编辑规模。
- **Self-Breaking** 通过向正确程序注入缺陷来构造训练数据，然后基于编辑距离相似度用 min-max sampling 保留一个多样化子集。
- **Self-Repairing** 使用 **Edit-Aware GRPO (EA-GRPO)** 训练模型；只有当一个 rollout group 达到设定的正确率阈值后，它才加入编辑惩罚。
- 该奖励机制将正确性作为首要目标，然后在同一组中优先选择那些相对其他正确候选修改行数更少的正确候选。

## 结果
- 论文报告 **fix_1@1** 在修复精度上最高提升 **31.4%**。
- 在 **Python / HumanEvalFix** 上，**Qwen2.5-Coder-7B + EA-GRPO** 达到 **91.19 pass@1** 和 **81.62 fix_1@1**，而 **+GRPO** 为 **89.82 pass@1** 和 **47.44 fix_1@1**。也就是 **fix_1@1** 提高 **34.18 点**，**pass@1** 小幅提高 **1.37 点**。
- 在 **Verilog** 基准上，**Qwen2.5-Coder-7B + EA-GRPO** 达到 **68.66 pass@1** 和 **68.11 fix_1@1**，而 **+GRPO** 为 **68.37 pass@1** 和 **8.49 fix_1@1**。也就是 **fix_1@1** 提高 **59.62 点**，**pass@1** 基本不变。
- 在 **Python** 上，**Qwen2.5-Coder-3B + EA-GRPO** 的 **fix_1@1** 为 **67.96**，而 **+GRPO** 为 **34.27**；在 **Verilog** 上分别为 **37.40** 和 **18.55**。
- 论文称，只优化正确性的 GRPO 在训练中会把编辑代价推高到 **0.6** 以上，并以此作为过度编辑严重的证据。
- 论文还称，与 speculative editing 结合时，它可以提高解码吞吐量，因为更小的修改会提升 draft token 的接受率，但摘录中没有给出具体吞吐量数字。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05963v1](http://arxiv.org/abs/2604.05963v1)
