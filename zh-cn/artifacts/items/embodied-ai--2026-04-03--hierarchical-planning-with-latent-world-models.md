---
source: arxiv
url: http://arxiv.org/abs/2604.03208v1
published_at: '2026-04-03T17:32:36'
authors:
- Wancong Zhang
- Basile Terver
- Artem Zholus
- Soham Chitnis
- Harsh Sutaria
- Mido Assran
- Randall Balestriero
- Amir Bar
- Adrien Bardes
- Yann LeCun
- Nicolas Ballas
topics:
- hierarchical-planning
- latent-world-models
- model-predictive-control
- zero-shot-robot-control
- long-horizon-planning
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Hierarchical Planning with Latent World Models

## Summary
## 摘要
这篇论文提出了 HWM，一种用于学习型潜在世界模型的分层规划方法，用来改善长时程零样本控制。它在共享潜在空间中做两个时间尺度的规划，从而提高真实机器人操作和仿真任务的成功率，同时降低规划计算量。

## 问题
- 学习型世界模型可以支持零样本控制，但平面式模型预测控制在长时程任务上效果较弱，因为滚动误差会随时间累积。
- 在长序列的原始动作上做规划很耗计算，因为搜索空间会随着时长迅速扩大。
- 这对具身控制很重要，因为许多机器人和导航任务需要多阶段、非贪心的行为，输入还是高维观测，测试时往往只给一个目标图像。

## 方法
- HWM 在同一个潜在空间中训练两个潜在世界模型：一个低层模型负责短时程原始动作，一个高层模型负责更长时程的状态转移。
- 高层模型用学到的宏动作预测路径点潜变量。这些宏动作来自一个动作编码器，它把两个路径点之间的一段低层动作压缩起来。
- 在推理时，高层规划器在潜在宏动作上搜索，把当前潜在状态推向目标潜变量。它预测出的第一个潜在路径点会被当作子目标。
- 低层规划器随后在原始动作上搜索，以到达这个潜在子目标，系统在执行过程中按 MPC 方式重新规划。
- 因为两层共享同一个潜在空间，HWM 不需要任务特定奖励、技能学习、逆模型或分层策略。

## 结果
- 在一个真实的 Franka 取放任务上，使用 VJEPA2-AC 且只给最终目标图像时，平面式规划的成功率是 **0%**，HWM 的成功率是 **70%**，提升 **70** 个百分点。
- 在 Franka 抽屉开关任务上，VJEPA2-AC 从 **30%** 提升到 **70%**，提升 **40** 个百分点。
- 在 Push-T 上使用 DINO-WM，成功率从 **17%** 升到 **61%**，提升 **44** 个百分点。
- 在 Diverse Maze 上使用 PLDM，成功率从 **44%** 升到 **83%**，提升 **39** 个百分点。
- 在使用 oracle 子目标的取放任务上，平面规划器和 HWM 都得到 **80%**，说明主要收益来自自动生成子目标，而不是更容易的低层控制。
- 论文在图注中声称，规划时间大约减少 **3 倍**，在贡献总结中声称推理时规划成本最高降低 **4 倍**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.03208v1](http://arxiv.org/abs/2604.03208v1)
