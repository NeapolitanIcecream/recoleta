---
source: arxiv
url: https://arxiv.org/abs/2606.29898v1
published_at: '2026-06-29T07:34:39'
authors:
- Haoxu Huang
- Tongsam Zheng
- Yifan Chen
- Jiacheng You
- Yang Gao
topics:
- offline-validation
- robot-manipulation
- vision-language-action
- policy-ranking
- robot-evaluation
- action-mse
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# Critical Interval MSE: Toward Reliable Offline Validation for Robot Manipulation Policies

## Summary
## 摘要
Critical Interval MSE 是一种用于机器人操作策略的离线验证指标，比原始动作 MSE 更能预测 rollout 性能。它只对任务关键轨迹片段打分，并在比较预测动作和专家动作前应用 rollout 时的动作对齐。

## 问题
- 机器人 rollout 提供最好的策略评估信号，但成本高、难以复现，而且数据通常太少，无法比较相近的模型变体。
- 基于专家演示的原始验证 MSE 常常不能很好地给策略排序，因为长时间的移动或空闲动作会主导误差，而短暂的接触、抓取、插入或对齐阶段决定任务是否成功。
- 离线验证很重要，因为更快的策略迭代需要一个低成本指标，并且该指标要能跟踪真实成功率或 rollout 排名。

## 方法
- CI-MSE 首先在演示视频中识别关键区间，例如抓取、接触、插入或精细对齐；论文使用少样本视觉语言模型提示来完成该标注。
- 它过滤验证集，只保留这些区间内的时间步，然后只在这些时间步上计算动作误差。
- 它在测量误差前，应用 rollout 时使用的相同动作执行流程，包括时间集成或实时动作分块。
- 它使用局部动态时间规整，避免因预测动作序列和专家动作序列之间的小时间偏移而产生惩罚。
- 对于数量有限的真实世界试验，论文还建议使用 Elo 式成对策略排名，而不是只依赖标量的部分进度分数。

## 结果
- 在 LBM-Eval 仿真中，覆盖 49 个任务、约 1 万条演示和 27 个策略检查点，CI-MSE 相对于 rollout 成功率达到 Pearson r = -0.74、Spearman ρ = -0.87；原始 MSE 达到 r = -0.56、ρ = -0.61。
- 在不同模型变体族中，CI-MSE 相比原始 MSE 在 Spearman 排名相关性上持平或更好。对于数据扩展变体，原始 MSE 给出错误方向，r = 0.67、ρ = 0.90；CI-MSE 给出 r = -0.97、ρ = -0.70。
- 在分布偏移下，CI-MSE 将物体布局 OOD 排名相关性从原始 MSE 的 ρ = -0.77 提高到 ρ = -0.88，将技能 OOD 从 ρ = -0.36 提高到 ρ = -0.69。视觉 OOD 仍然困难，CI-MSE 为 ρ = -0.66，原始 MSE 为 ρ = -0.68。
- 在真实世界 Franka 实验中，CI-MSE 对 pour water 给出接近完美的跨环境排名，r = -0.99、ρ = -1.00；对 arrange mouse 给出 r = -0.96、ρ = -1.00。
- 对于采集者不匹配的 fold-towel 跨物体验证，CI-MSE 优于原始 MSE：CI-MSE r = -0.87、ρ = -1.00，而原始 MSE r = -0.09、ρ = 0.00。
- 敏感性分析报告称，时间集成将排名相关性从 H = 1、ρ = -0.80 提高到 H = 8、ρ = -0.87；论文还称，在合理的超参数范围内，相关性下降小于 5%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.29898v1](https://arxiv.org/abs/2606.29898v1)
