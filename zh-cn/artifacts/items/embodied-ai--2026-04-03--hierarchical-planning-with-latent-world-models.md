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
这篇论文提出 HWM，这是一种用于学习式潜在世界模型的分层规划方法，可提升长时程的零样本控制能力。它在共享潜在空间中按两个时间尺度进行规划，在减少规划计算量的同时，提高了真实机器人操作任务和仿真任务的成功率。

## 问题
- 学习式世界模型可以支持零样本控制，但扁平的模型预测控制在长时程任务上效果较差，因为滚动预测误差会随时间累积。
- 在长动作序列上进行规划成本很高，因为搜索空间会随着时域迅速增长。
- 这对具身控制很重要，因为许多机器人和导航任务需要基于高维观测完成多阶段、非贪心行为，而且测试时通常只有一张目标图像。

## 方法
- HWM 在同一个潜在空间中训练两个潜在世界模型：一个低层模型用于短时程的原始动作，另一个高层模型用于更长时程的状态转移。
- 高层模型使用学到的宏动作来预测路标潜变量。这些宏动作来自一个动作编码器，它将路标之间的一段低层动作压缩编码。
- 在推理时，高层规划器在潜在宏动作上搜索，使当前潜在状态朝目标潜在状态移动。它预测出的第一个潜在路标会作为子目标。
- 随后，低层规划器搜索原始动作以到达该潜在子目标，系统在执行过程中按 MPC 方式持续重规划。
- 由于两个层级共享同一个潜在空间，HWM 不需要任务特定奖励、技能学习、逆模型或分层策略。

## 结果
- 在真实 Franka 抓取放置任务中，使用 VJEPA2-AC 且只提供最终目标图像时，扁平规划的成功率为 **0%**，HWM 为 **70%**，提升 **70 个百分点**。
- 在 Franka 抽屉开关任务上，VJEPA2-AC 的成功率从 **30%** 提升到 **70%**，增加 **40 个百分点**。
- 在使用 DINO-WM 的 Push-T 任务上，成功率从 **17%** 提升到 **61%**，增加 **44 个百分点**。
- 在使用 PLDM 的 Diverse Maze 任务上，成功率从 **44%** 提升到 **83%**，增加 **39 个百分点**。
- 在带有 oracle 子目标的抓取放置任务上，扁平规划器和 HWM 都达到 **80%**，说明主要收益来自自动生成子目标，而不是更容易的低层控制。
- 论文在图注中称，在成功率相近或更高的情况下，规划时间约减少 **3×**；在贡献总结中称，推理时的规划成本最高可降低 **4×**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.03208v1](http://arxiv.org/abs/2604.03208v1)
