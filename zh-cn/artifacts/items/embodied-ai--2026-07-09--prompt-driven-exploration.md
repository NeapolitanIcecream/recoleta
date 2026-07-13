---
source: arxiv
url: https://arxiv.org/abs/2607.08837v1
published_at: '2026-07-09T18:00:24'
authors:
- Sunshine Jiang
- John Marangola
- David Zhang
- Raghuram Kowdeed
- Ruiyang Luo
- Nitish Dashora
- Richard Li
- Pulkit Agrawal
- Zhang-Wei Hong
topics:
- robot-foundation-model
- vision-language-action
- prompt-exploration
- sparse-reward-rl
- robot-data-scaling
- dexterous-manipulation
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# Prompt-Driven Exploration

## Summary
## 摘要
Prompt-Driven Exploration（PDE）通过改变语言提示词来探索机器人行为，而不是只添加动作噪声。视觉语言模型根据轨迹视频重写提示词，帮助强化学习在初始策略几乎没有奖励时找到成功行为。

## 问题
- 稀疏的二元奖励使弱视觉语言动作策略没有成功轨迹可供强化，尤其是在困难的操作任务中。
- 动作空间噪声只会局部改变单个动作，因此很少能让策略摆脱贯穿整个回合的错误行为模式。
- 这一问题会影响基于有限演示微调通用机器人策略的过程，因为初始成功率可能接近 0%。

## 方法
- PDE 为同一任务采样不同提示词，并在每次轨迹执行期间固定提示词，从而产生全局不同的行为模式。
- 视觉语言模型观看轨迹视频、诊断失败原因并提出修改后的提示词；提示词搜索期间不更新模型权重。
- 该方法将提示词采样器视为关于有用策略行为的隐式后验分布，并根据任务结果和轨迹历史更新这一分布。
- 近端策略优化（Proximal Policy Optimization）通过混合采样和混合反向传播，在探索提示词与标准提示词上训练，将有用行为迁移回标准任务提示词。

## 结果
- 在微波炉关门案例研究中，提示词搜索在累计 85 次轨迹执行内找到了 10–12 个成功的提示词变体；在策略训练前，表现最好的提示词成功率低于 40%。
- 到训练步骤 100 时，PDE 将原始标准提示词上的成功率从 0% 提高到约 98%，而标准动作噪声 PPO 的成功率仍接近零。
- 在 LIBERO-PRO 上，PDE 在困难、中等和简单三个等级中均优于所有测试基线；在包含 47 个任务的困难等级中，相对提升了 60%。
- 该基准涵盖 120 个 LIBERO-PRO 任务，每个任务在 250 个环境中评估成功率；使用 GR00T 和 Pi0 主干网络时，PDE 相比动作噪声也提高了学习效果。
- 论文还报告了 PDE 在 ManiSkill 操作任务和具有挑战性的 LLM 编程任务上的更广泛收益，表明该方法的适用范围不局限于单一机器人基准。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.08837v1](https://arxiv.org/abs/2607.08837v1)
