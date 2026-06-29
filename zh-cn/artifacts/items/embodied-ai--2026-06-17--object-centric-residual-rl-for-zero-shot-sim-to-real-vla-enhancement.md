---
source: arxiv
url: https://arxiv.org/abs/2606.18953v1
published_at: '2026-06-17T11:36:54'
authors:
- Kinam Kim
- Namiko Saito
- Heecheol Kim
- Katsushi Ikeuchi
- Jaegul Choo
- Yasuyuki Matsushita
topics:
- vision-language-action
- residual-rl
- sim2real
- robot-manipulation
- object-pose
- vla-self-improvement
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Object-Centric Residual RL for Zero-Shot Sim-to-Real VLA Enhancement

## Summary
## 摘要
本文在冻结的 VLA 上加入基于位姿的残差 RL 策略，使只在仿真中训练的修正策略可以在真实 FR3 机器人上运行，无需真实环境 RL。在五个桌面任务上，该方法把真实机器人平均成功率从 42% 提高到 76%。

## 问题
- 通过模仿学习训练的 VLA 在精细操作中可能失败，因为小的动作误差会在一次执行过程中累积。
- 以往的残差 RL 方案有部署成本：特权仿真器状态需要蒸馏，图像观测会受到视觉仿真到现实差距的影响，真实环境 RL 成本高且有风险。
- 这个问题重要，因为更好的恢复能力可以改进已部署的机器人策略，而不需要收集更多遥操作数据或在硬件上运行 RL。

## 方法
- 该方法在 MuJoCo 和真实设置中回放相同的遥操作动作，训练配对的仿真 VLA 和真实 VLA，并对 GR00T-N1.5 按每个任务 30 条演示进行微调。
- 在残差 RL 训练期间，冻结的仿真 VLA 提供基础动作；部署时，冻结的真实 VLA 提供基础动作。
- 残差策略是一个 2 层 MLP，在仿真中用 TD3 训练。其输入包括 6-DoF 任务物体位姿、机器人本体感知信息，以及当前基础 VLA 动作。
- 残差输出与基础动作组合：位置和夹爪命令相加，旋转使用四元数乘法。
- 训练时注入位姿噪声，并有时将物体位姿向量置零，使策略能够处理 FoundationPose 加 SAM2 带来的位姿估计误差或跟踪丢失。

## 结果
- 在五个任务上，通过零样本仿真到现实迁移，真实 FR3 的平均成功率从 8.4/20 次试验提高到 15.2/20 次试验，即从 42% 提高到 76%。
- 所有任务的真实成功率都有提升：Cube Lift 从 7/20 到 17/20，Pick-and-Place 从 9/20 到 16/20，Stack Cube 从 7/20 到 15/20，Close Drawer 从 14/20 到 20/20，Stand Cup Up 从 5/20 到 8/20。
- 在 3 个种子上，仿真平均成功率从 7.6/20 ± 1.7 提高到 17.2/20 ± 0.9。
- 消融实验显示，完整的基于位姿的残差方法在真实机器人上优于基于图像和基于蒸馏的残差方法；例如，Pick-and-Place 达到 16/20，而基于图像的方法为 10/20，基于蒸馏的方法为 4/20。
- 去掉位姿 dropout 会降低各任务的真实成功率，其中 Stack Cube 从 15/20 降到 10/20，Close Drawer 从 20/20 降到 16/20。
- 残差 actor 增加的计算量很小：每次 GPU 前向传播约 0.06 ms，低于 VLA 约 140 ms 推理时间的 0.05%；FoundationPose 跟踪以异步方式运行，约为每帧 18 ms。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.18953v1](https://arxiv.org/abs/2606.18953v1)
