---
source: arxiv
url: https://arxiv.org/abs/2606.32026v1
published_at: '2026-06-30T17:53:48'
authors:
- Ying Wang
- Oumayma Bounou
- Yann LeCun
- Mengye Ren
topics:
- latent-world-model
- test-time-adaptation
- model-predictive-control
- jepa
- robot-planning
- distribution-shift
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# AdaJEPA: An Adaptive Latent World Model

## Summary
## 摘要
AdaJEPA 在 MPC 过程中使用每次执行动作后刚观测到的转移来适配 JEPA 潜在世界模型。论文报告称，在形状、视觉、动力学和迷宫布局发生偏移时，每次重新规划只做一步梯度更新即可提高到达目标的成功率。

## 问题
- 冻结的潜在世界模型在视觉或动力学偏移后可能给 MPC 提供错误的 rollout，导致规划器优化出的动作在真实环境中失败。
- 这对机器人规划很重要，因为小的一步预测误差会在 MPC 时域内累积，并降低到达目标的成功率。
- 论文目标是在没有奖励标签、专家示范或单独目标域数据收集阶段的情况下进行适配。

## 方法
- AdaJEPA 在 MPC 内运行规划、行动、适配、重新规划循环。
- 执行第一个动作或动作块后，它将观测到的转移 `(o_t, a_t, o_{t+1})` 存入一个小型在线缓冲区。
- 它应用训练中使用的同一 JEPA 潜在预测损失：从当前潜在状态和动作预测下一潜在状态，然后将其与编码后的下一观测进行比较，并对目标使用 stop-gradient。
- 测试时，它只更新一小部分参数，通常是最终的编码器层和预测器层，然后立即使用更新后的模型进行下一次 MPC 规划。
- 默认实验设置为每次 MPC 重新规划做一步梯度更新，缓冲区保留最近 5 个转移，最多 20 个 MPC 步，并在 3 个测试数据种子中的每个种子上运行 50 个 episode。

## 结果
- 在 PushObj 的分布内训练形状上，论文报告的最大提升是在适配当前形状时相对于冻结模型超过 20%。
- 在未见过的 PushObj 形状上，文本称 AdaJEPA 的规划成功率几乎是冻结模型的两倍；摘录中未提供确切百分比。
- 在低质量动力学的 PointMaze-Medium 上，`predlast + enclast` 将 GD 成功率从 77.3 ± 8.2 提高到 80.0 ± 3.3，将 CEM 成功率从 82.0 ± 2.8 提高到 86.7 ± 2.5。
- 在高阻尼的 PointMaze-Medium 上，`predfirst + enclast` 将 CEM 成功率从 76.0 ± 2.8 提高到 82.0 ± 3.3，同时 GD 从 77.3 ± 5.0 升至 78.7 ± 4.7。
- 在未见过的 PointMaze 布局上，`predfirst + enclast` 将 GD 成功率从 53.3 ± 8.2 提高到 78.7 ± 5.0，将 CEM 成功率从 49.3 ± 6.2 提高到 70.7 ± 3.8。
- 报告表中的延迟增幅很小：对于全局特征 Temporal Straightening 世界模型，GD 时间从 3.14 s 变为 3.17 s，CEM 时间从 0.24 s 变为 0.27 s；对于空间特征变体，GD 从 3.37 s 变为 3.38 s，CEM 从 5.37 s 变为 5.39 s。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.32026v1](https://arxiv.org/abs/2606.32026v1)
