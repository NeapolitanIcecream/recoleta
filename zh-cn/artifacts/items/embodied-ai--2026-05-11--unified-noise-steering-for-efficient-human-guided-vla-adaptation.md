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
## 总结
UniSteer 通过把人类纠正动作转换为噪声目标，来改进扩散式或 flow-matching 的 VLA 机器人策略。方法冻结预训练 VLA，只训练一个小型 noise actor；在真实世界任务上，它以更少的人类数据获得了比噪声空间 RL 和动作空间 DAgger 更高的成功率。

## 问题
- 预训练 VLA 策略在物体位姿、场景布局、视角和接触动力学发生变化时，常常失效。
- 机器人上的 RL 速度慢、成本高，因为失败会消耗时间，而稀疏奖励提供的学习信号很弱。
- 人类纠正以动作形式给出，而噪声空间的 VLA 微调训练的是潜在噪声上的策略，因此这两类信号需要一个共享的训练目标。

## 方法
- UniSteer 冻结 flow-matching VLA 解码器，只训练一个轻量 actor 来选择初始噪声变量。
- 当人类接管时，方法会近似反演冻结的解码器，把纠正后的动作片段映射回初始噪声目标。
- 这个反演通过固定点迭代沿着 Euler flow 步骤向后运行。
- 纠正后的噪声目标用 L2 监督损失训练 actor，而自主交互和被纠正的转移也会训练一个用于 RL 的噪声空间 critic。
- 同一个 noise actor 同时接受基于奖励的更新和基于人类纠正的更新。

## 结果
- 在四个真实世界任务上，UniSteer 将初始策略的平均成功率从 20.0% 提升到 90.0%，适应时间为 66 分钟。
- UniSteer 的平均成功率为 90.0%，DSRL 为 55.0%，DAgger 为 60.0；相比这两个基线，UniSteer 分别高 35 和 30 个百分点。
- UniSteer 在各任务上的成功率分别为：Pick up Spoon 90.0%，Stack Blocks 95.0%，Insert Square 100.0%，Fold Towel 75.0%。
- 在 OOD 物体摆放下，UniSteer 在 Pick up Spoon、Stack Blocks 和 Insert Square 上都达到 100.0% 成功率；DSRL 分别为 0.0%、0.0% 和 25.0%，DAgger 分别为 75.0%、100.0% 和 25.0%。
- UniSteer 平均每轮使用 0.98 条纯人类轨迹，DAgger 平均每轮使用 8 条纯人类轨迹。
- 固定点反演的动作重建损失和耗时都低于基于优化的反演：在 Pick up Spoon 上分别为 0.00122 和 73.26 秒，而后者为 0.06516 和 208.04 秒；在 Insert Square 上分别为 0.00018 和 40.42 秒，而后者为 0.05624 和 80.96 秒。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.10821v1](https://arxiv.org/abs/2605.10821v1)
