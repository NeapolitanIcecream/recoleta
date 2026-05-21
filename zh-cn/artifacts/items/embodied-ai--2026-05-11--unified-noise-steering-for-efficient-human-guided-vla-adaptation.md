---
source: arxiv
url: https://arxiv.org/abs/2605.10821v1
published_at: '2026-05-11T16:37:34'
authors:
- Junjie Lu
- Xinyao Qin
- Yuhua Jiang
- Kaixin Wang
- Chuheng Zhang
- Bin Liang
- Jun Yang
- Min Xu
- Li Zhao
topics:
- vision-language-action
- robot-policy-adaptation
- human-guided-learning
- noise-space-rl
- flow-matching
- real-world-manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Unified Noise Steering for Efficient Human-Guided VLA Adaptation

## Summary
## 摘要
UniSteer 通过把人类纠正动作转换为小型噪声 actor 的噪声目标，来适配基于扩散或流匹配的 VLA 机器人策略。该方法冻结预训练 VLA，并报告其在真实世界中用少于噪声空间 RL 和动作空间 DAgger 的人类数据取得了更高成功率。

## 问题
- 预训练 VLA 策略在物体姿态、场景布局、视角和接触动力学发生真实世界偏移时经常失败。
- 机器人本体上的 RL 速度慢、成本高，因为失败会消耗时间，稀疏奖励也提供较弱的学习信号。
- 人类纠正以动作形式给出，而噪声空间 VLA 微调训练的是潜在噪声上的策略，因此这两种信号需要一个共享的训练目标。

## 方法
- UniSteer 冻结流匹配 VLA 解码器，并训练一个轻量级 actor 来选择初始噪声变量。
- 当人类接管时，该方法近似反演冻结的解码器，把纠正后的动作块映射回初始噪声目标。
- 反演通过固定点迭代沿 Euler 流步骤反向运行。
- 纠正后的噪声目标用 L2 监督损失训练 actor，同时自主转移和纠正转移也会训练用于 RL 的噪声空间 critic。
- 同一个噪声 actor 同时接收基于奖励的更新和人类纠正更新。

## 结果
- 在四个真实世界任务上，UniSteer 将平均成功率从初始策略的 20.0% 提高到 66 分钟适配后的 90.0%。
- UniSteer 的平均成功率为 90.0%，DSRL 为 55.0%，DAgger 为 60.0%；UniSteer 相比这些基线分别提高了 35 和 30 个百分点。
- UniSteer 在各任务上的成功率为：Pick up Spoon 90.0%，Stack Blocks 95.0%，Insert Square 100.0%，Fold Towel 75.0%。
- 在 OOD 物体摆放上，UniSteer 在 Pick up Spoon、Stack Blocks 和 Insert Square 上均达到 100.0% 成功率；DSRL 分别达到 0.0%、0.0% 和 25.0%，DAgger 分别达到 75.0%、100.0% 和 25.0%。
- UniSteer 平均每轮使用 0.98 条纯人类轨迹，而 DAgger 每轮使用 8 条纯人类轨迹。
- 固定点反演的动作重建损失和耗时都低于基于优化的反演：在 Pick up Spoon 上，损失为 0.00122、总耗时 73.26 秒，对比 0.06516 损失和 208.04 秒；在 Insert Square 上，损失为 0.00018、耗时 40.42 秒，对比 0.05624 损失和 80.96 秒。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.10821v1](https://arxiv.org/abs/2605.10821v1)
