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
潜变量世界模型可以准确预测短期结果，同时给出会误导规划的潜在空间。RC-aux 加入多步展开训练和有限预算可达性监督，让潜在距离更符合智能体在动作预算内能到达的状态。

## 问题
- 目标条件的像素控制常在潜在空间里展开动作，并选择终点潜在表示接近目标潜在表示的轨迹。
- 一步或短期预测损失会产生潜在捷径：即使没有可行的有限步动作序列，状态在欧氏潜在距离上也会显得很近。
- 这会让规划器选出在潜在空间里得分高、却在环境中失败的动作序列，障碍物场景和长时程任务里尤其明显。

## 方法
- RC-aux 保持 LeWorldModel 的骨干不变，只改训练信号，不新增世界模型架构。
- 它把局部的一步监督改成多时长无回放预测：把预测出的潜在表示再送回动力学模型，并在 K 步内与编码后的未来潜在表示对齐。
- 它训练一个可达性头 R_phi(z, z', h)，预测目标潜在表示 z' 是否能在预算 h 内从源潜在表示 z 到达。
- 可达性标签使用同轨迹正样本、时间硬负样本（目标出现时间晚于采样预算）、跨轨迹批内负样本，以及预测展开对。
- 测试时，可选的可达性感知规划器会在中间预测状态能在剩余时长内到达目标时，降低基础终点潜在成本；lambda_plan = 0 时恢复基础规划器。

## 结果
- 在五个基于像素的目标条件控制任务上，RC-aux 在 5 个 LeWM 家族对比中的 4 个上都有提升：TwoRoom +9.2，Reacher +4.4，Push-T -0.4，Wall +33.2，Cube +3.2 个成功率点。
- Wall 的提升最大：LeWM 为 50.4 ± 6.5 成功率，RC-aux 为 83.6 ± 3.6。
- TwoRoom 从 LeWM 家族控制下的 88.8 ± 3.0 提升到 RC-aux 的 98.0 ± 1.4。
- Reacher 从 82.8 ± 7.2 提升到 87.2 ± 6.4，Cube 从 72.8 ± 5.2 提升到 76.0 ± 7.5。
- 规划器消融显示，训练本身在 Wall 上就有帮助：控制组为 50.4 ± 6.5，lambda_plan = 0 的 RC-aux 达到 72.4 ± 3.6，完整 RC-aux 达到 83.6 ± 3.6。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.07278v1](https://arxiv.org/abs/2605.07278v1)
