---
source: arxiv
url: https://arxiv.org/abs/2605.07278v1
published_at: '2026-05-08T05:43:33'
authors:
- Wenyuan Li
- Guang Li
- Keisuke Maeda
- Takahiro Ogawa
- Miki Haseyama
topics:
- latent-world-models
- goal-conditioned-control
- reachability-learning
- latent-planning
- pixel-control
- robot-manipulation
relevance_score: 0.66
run_id: materialize-outputs
language_code: zh-CN
---

# Predictive but Not Plannable: RC-aux for Latent World Models

## Summary
## 摘要
潜在世界模型可以准确预测短期结果，但仍可能生成会误导规划的潜在空间。RC-aux 加入多步 rollout 训练和有限预算可达性监督，使潜在距离更符合智能体在动作预算内实际能到达的位置。

## 问题
- 目标条件像素控制通常会在潜在空间中 rollout 动作，并选择终端潜变量接近目标潜变量的轨迹。
- 一步或短期预测损失可能产生潜在捷径：即使不存在可行的有限时域动作序列能到达某些状态，这些状态在欧氏潜在距离上也看起来很近。
- 这会影响规划结果，因为规划器可能选择在潜在空间中得分高、但在环境中失败的动作序列，尤其是在有障碍或长时域任务中。

## 方法
- RC-aux 保留 LeWorldModel 主干，改变训练信号，而不是加入新的世界模型架构。
- 它用多时域开环预测替代局部一步监督：将预测出的潜变量反馈给动力学模型，并在 K 步内与编码后的未来潜变量匹配。
- 它训练一个可达性头 R_phi(z, z', h)，预测目标潜变量 z' 是否能在预算 h 内从源潜变量 z 到达。
- 可达性标签使用同轨迹正样本、目标出现时间晚于采样预算的时间硬负样本、跨轨迹批内负样本，以及预测 rollout 对。
- 测试时，可选的可达性感知规划器会在某个中间预测状态能在剩余时域内到达目标时，折扣基础终端潜变量代价；lambda_plan = 0 时恢复基础规划器。

## 结果
- 在五个基于像素的目标条件控制任务上，RC-aux 在 5 个匹配的 LeWM 系列比较中提升了 4 个：TwoRoom +9.2、Reacher +4.4、Push-T -0.4、Wall +33.2、Cube +3.2 个成功率百分点。
- Wall 的提升最大：LeWM 的成功率为 50.4 ± 6.5，RC-aux 为 83.6 ± 3.6。
- TwoRoom 从 LeWM 系列对照的 88.8 ± 3.0 提升到使用 RC-aux 后的 98.0 ± 1.4。
- Reacher 从 82.8 ± 7.2 提升到 87.2 ± 6.4，Cube 从 72.8 ± 5.2 提升到 76.0 ± 7.5。
- 规划器消融显示，仅训练改动就能帮助 Wall：对照为 50.4 ± 6.5，lambda_plan = 0 的 RC-aux 达到 72.4 ± 3.6，完整 RC-aux 达到 83.6 ± 3.6。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.07278v1](https://arxiv.org/abs/2605.07278v1)
