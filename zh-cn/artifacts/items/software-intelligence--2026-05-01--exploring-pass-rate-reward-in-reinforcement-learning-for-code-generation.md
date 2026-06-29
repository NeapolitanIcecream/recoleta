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
这篇论文检验了测试用例通过率奖励是否能改进用于代码生成的无评论家强化学习。主要结论是否定的：通过率奖励提供了更密集的反馈，但在最终 pass@k 上并没有超过二元的“全测试通过”奖励。

## 问题
- 用于代码生成的 RL 微调常用二元单元测试奖励：只有当一个解通过所有测试时，奖励才是 1。
- 在困难编程任务上，二元奖励可能很稀疏，所以很多训练会改用测试用例通过率作为更密集的奖励。
- 论文要回答的是，这种更密集的部分奖励，是否真的能提升完整正确性的表现。这个问题很重要，因为代码生成基准关心的是通过所有测试，而不是通过一部分测试。

## 方法
- 作者比较了二元奖励、原始通过率奖励、按难度重加权的通过率奖励，以及一个先通过率后切换为二元奖励的两阶段方案。
- 他们用无评论家 RL 方法 GRPO 和 RLOO，训练了 DeepSeek-R1-Distill-Qwen-7B、Qwen3-4B 和 Qwen2.5-7B-Instruct。
- 训练设置为 768 次更新、每个批次 64 个问题、每个问题 16 次采样、学习率 1e-6、温度 1.0、无 KL 正则，并严格按 on-policy 更新。
- 评估使用 LiveCodeBench 和 LeetCodeDataset 测试集上的 pass@1、pass@4、pass@8 和 pass@16。
- 分析部分检查奖励密度，并检验通过率梯度是否会提高一个已知全通过解的对数概率。

## 结果
- 在 DeepSeek-R1-Distill-Qwen-7B + GRPO 上，通过率奖励的平均 pass@1 只比二元奖励高 0.3 个点，但在 pass@4、pass@8 和 pass@16 上更差：分别低 0.6、1.2 和 2.0 个点。
- 在 DeepSeek-R1-Distill-Qwen-7B + RLOO 上，通过率奖励在平均 pass@1/pass@4/pass@8/pass@16 上分别比二元奖励低 0.2、0.4、0.8 和 1.7 个点。
- 在 Qwen3-4B + GRPO 上，二元奖励在所有平均指标上都优于通过率奖励：pass@1 为 46.4% 对 44.2%，pass@16 为 59.1% 对 56.8%。
- 在 Qwen2.5-7B-Instruct + GRPO 上，通过率奖励没有带来平均提升：pass@1 为 22.8%，二元奖励为 22.9%；pass@16 为 28.8%，二元奖励为 30.5%。
- 对 DeepSeek-R1-Distill-Qwen-7B + GRPO 的任务级训练集结果，97% 的任务结论一致：2,650 个任务两种奖励都解决了，774 个任务两种奖励都失败了，只有 97 个任务不同。
- 通过率反馈确实更密集：77.5% 的有效分组包含 3 个或更多不同的奖励值，47.2% 的样本有中间通过率值；但在 392 个任务上的梯度探测显示，当没有全通过采样时，梯度朝向全通过解的移动很弱。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.02944v1](https://arxiv.org/abs/2605.02944v1)
