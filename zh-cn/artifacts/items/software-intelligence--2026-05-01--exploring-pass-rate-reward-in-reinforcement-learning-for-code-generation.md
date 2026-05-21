---
source: arxiv
url: https://arxiv.org/abs/2605.02944v1
published_at: '2026-05-01T10:26:43'
authors:
- Xin-Ye Li
- Ren-Biao Liu
- Yun-Ji Zhang
- Hui Sun
- Zheng Xie
- Ming Li
topics:
- code-generation
- reinforcement-learning
- unit-test-feedback
- reward-design
- grpo
- rloo
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# Exploring Pass-Rate Reward in Reinforcement Learning for Code Generation

## Summary
## 摘要
本文测试测试用例通过率奖励是否能改进用于代码生成的无评论器强化学习。主要结果是否定的：通过率奖励提供更密集的反馈，但在最终 pass@k 上没有超过“通过全部测试”的二元奖励。

## 问题
- 代码生成的强化学习微调通常使用二元单元测试奖励：只有通过所有测试的解法才得到奖励 1。
- 在困难编程任务上，二元奖励可能很稀疏，因此许多训练运行会把测试用例通过率用作更密集的奖励。
- 论文研究更密集的部分得分奖励是否真的能提升完全正确性能。这个问题很重要，因为代码生成基准关注通过全部测试，而不是通过部分测试。

## 方法
- 作者比较了二元奖励、原始通过率奖励、按难度重新加权的通过率奖励，以及先用通过率再切换到二元奖励的两阶段日程。
- 他们使用无评论器强化学习方法 GRPO 和 RLOO 训练 DeepSeek-R1-Distill-Qwen-7B、Qwen3-4B 和 Qwen2.5-7B-Instruct。
- 训练使用 768 个更新步骤、每批 64 个问题、每个问题 16 次 rollout、学习率 1e-6、温度 1.0、不使用 KL 正则化，并采用严格的 on-policy 更新。
- 评估在 LiveCodeBench 和 LeetCodeDataset 测试划分上使用 pass@1、pass@4、pass@8 和 pass@16。
- 分析检查奖励密度，并探测通过率梯度是否会提高已知全通过解法的对数概率。

## 结果
- 在 DeepSeek-R1-Distill-Qwen-7B + GRPO 上，通过率奖励的平均 pass@1 只比二元奖励高 +0.3 个百分点，但在 pass@4、pass@8 和 pass@16 上更差，分别低 -0.6、-1.2 和 -2.0 个百分点。
- 在 DeepSeek-R1-Distill-Qwen-7B + RLOO 上，通过率奖励在平均 pass@1/pass@4/pass@8/pass@16 上落后二元奖励，差值分别为 -0.2、-0.4、-0.8 和 -1.7 个百分点。
- 在 Qwen3-4B + GRPO 上，二元奖励在所有平均指标上都超过通过率奖励：pass@1 为 46.4% 对 44.2%，pass@16 为 59.1% 对 56.8%。
- 在 Qwen2.5-7B-Instruct + GRPO 上，通过率奖励没有带来平均收益：pass@1 为 22.8%，二元奖励为 22.9%；pass@16 为 28.8%，二元奖励为 30.5%。
- DeepSeek-R1-Distill-Qwen-7B + GRPO 的训练集任务级结果在 97% 的任务上一致：2,650 个任务被两种奖励都解决，774 个任务两种奖励都失败，只有 97 个任务结果不同。
- 通过率反馈很密集：77.5% 的有效组包含 3 个或更多不同奖励值，47.2% 的样本具有中间通过率值；但在 392 个任务上的梯度探测显示，当没有全通过 rollout 时，梯度向全通过解法移动的幅度很弱。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.02944v1](https://arxiv.org/abs/2605.02944v1)
