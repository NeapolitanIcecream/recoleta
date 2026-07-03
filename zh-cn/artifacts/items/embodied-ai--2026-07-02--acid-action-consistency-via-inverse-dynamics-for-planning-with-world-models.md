---
source: arxiv
url: https://arxiv.org/abs/2607.02403v1
published_at: '2026-07-02T16:38:10'
authors:
- Gawon Seo
- Dongwon Kim
- Suha Kwak
topics:
- world-model
- decision-time-planning
- inverse-dynamics
- embodied-control
- robot-manipulation
- visual-navigation
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# ACID: Action Consistency via Inverse Dynamics for Planning with World Models

## Summary
## 摘要
ACID 为使用动作条件世界模型的决策时规划加入了逆动力学一致性检查。它在四种世界模型和六个任务上提升了目标条件控制效果，并且不需要重新训练世界模型。

## 问题
- 使用世界模型的标准 MPC/CEM 规划主要根据预测最终状态到目标的距离来给候选动作序列打分。
- 这种打分方式没有检查每个预测转移是否能由其条件动作产生，因此规划器可能选择一组动作，使想象中的 rollout 到达目标，但真实 rollout 发生偏移。
- 这个问题影响机器人操作、可变形物体控制和视觉导航，因为执行效果取决于可实现的中间转移，不能只看像目标的最终预测。

## 方法
- ACID 使用逆动力学模型 `G_phi` 作为决策时验证器：给定两个连续的预测 latent，它预测能够解释该转移的动作。
- 对每个预测步，它用平方误差比较原始采样动作 `a_t` 和推断动作 `G_phi(z_t, z_{t+1})`。
- 它将这个逐步误差在规划时域上求平均，作为动作一致性代价，并把它加入常规目标代价。
- 权重是自适应的：`w_a = lambda * sigma_g / sigma_a`，其中两个 sigma 分别是当前 CEM 迭代中各候选序列的目标代价和一致性代价的标准差。
- 该方法只改变规划代价，因此可用于 latent JEPA 风格预测器和像素/视频世界模型。

## 结果
- 在 Le-WM 上，成功率在 Cube 上从 70.0% 提升到 74.0%，在 Reacher 上从 76.0% 提升到 88.0%，在 PushT 上从 96.0% 提升到 100.0%。
- 在 PLDM 上，成功率在 Cube 上从 58.0% 提升到 68.0%，在 Reacher 上从 76.0% 提升到 90.0%，在 PushT 上从 72.0% 提升到 76.0%。
- 在用于可变形操作的 DINO-WM 上，Chamfer distance 在 Rope 上从 1.38 降到 0.56，在 Granular 上从 0.49 降到 0.30。
- 在用于视觉导航、配合 CompACT 的 NWM 上，ATE 从 1.3141 降到 1.2835，降幅为 2.3%；平移 RPE 从 0.3831 降到 0.3773，降幅为 1.5%。
- 在 Reacher 的 CEM 预算扫描中，样本数为 30、50、150 和 300 时，ACID 在每个测试预算下都优于 Le-WM 和 PLDM 的原始规划器；对于 50 个样本的 PLDM，ACID 达到 84%，而原始规划器在 300 个样本时为 76%。
- 在 Le-WM 的自适应权重消融中，ACID 在 Cube、PushT 和 Reacher 上的总成功率增益为 +20.0 个百分点；测试过的最佳常数权重达到 +14.0 个百分点，一些常数权重还降低了总体性能。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.02403v1](https://arxiv.org/abs/2607.02403v1)
