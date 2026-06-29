---
source: arxiv
url: https://arxiv.org/abs/2605.26478v1
published_at: '2026-05-26T02:35:08'
authors:
- Haoxiang You
- Yilang Liu
- Davis Zong
- Qian Wang
- Teeratham Vitchutripop
- Qi Wang
- Daniel Rakita
- Ian Abraham
topics:
- visual-rl
- robot-learning
- sim2real
- dexterous-manipulation
- policy-gradient
- visuomotor-control
relevance_score: 0.66
run_id: materialize-outputs
language_code: zh-CN
---

# Efficient On-policy Visual-RL via Stochastic Decoupled Policy Gradient

## Summary
## 摘要
SDPG 用远少于标准按策略视觉强化学习的渲染仿真，端到端训练视觉机器人控制策略。论文的主要观点是，随机动作序列扰动可以替代完整轨迹求导，同时让训练在一块 RTX 4080 GPU 上保持较快速度。

## 问题
- 视觉 RL 速度慢、占内存，因为图像渲染和视觉编码器让大规模按策略批处理代价很高。
- 可微的一阶 RL 可以减少样本，但长时程反向传播在接触密集任务里不稳定，而且需要可微模拟器和奖励。
- 教师-学生蒸馏可以更快训练，但如果教师数据没有覆盖部署时会遇到的状态，视觉学生可能失效。

## 方法
- SDPG 先在少量名义视觉环境中 rollout，再在每个名义动作序列上加入随机扰动，进行多个仅物理辅助 rollout。
- 它根据回报差异估计动作序列梯度：更好的扰动会把策略推向相似动作，更差的扰动会把策略推开。
- 策略更新写成监督损失，把视觉策略输出拉向 `action + estimated gradient`，目标端使用 stop-gradient。
- 方法会调整探索尺度 `delta`，按回报标准差归一化，并用短时程 rollout 降低方差、提高吞吐。
- actor 使用视觉观测，critic 可以使用特权低维状态，加快价值学习。

## 结果
- 在 Visual MuJoCo 的 Hopper、Walker、Ant 和 Humanoid 上，SDPG 在图中展示的训练曲线里取得最高回报，并达到与基于状态的方法相当的水平，但摘要片段没有给出精确回报值。
- SDPG 使用 64 个按批渲染环境，而 PPO 的内存估计使用 4096 个环境。
- SDPG 的内存占用在 Hopper 上为 10.2 GB，在 Walker 上为 10.3 GB，在 Ant 上为 10.3 GB，在 Humanoid 上为 10.5 GB。
- PPO 的内存估计在 Hopper 上为 48 GB，在 Walker 上为 48 GB，在 Ant 上为 49 GB，在 Humanoid 上为 50 GB，表中大约是 SDPG 的 4.7 倍到 4.8 倍。
- 表中 SDPG 的内存与 DrQv2、DreamerV3 和蒸馏方法接近：DrQv2 为 8.2 GB 到 11.6 GB，DreamerV3 为 10.8 GB 到 10.9 GB，蒸馏方法为 10.3 GB 到 10.7 GB。
- 论文声称，单块 NVIDIA RTX 4080 GPU 上可以在几小时内完成行走和操作任务的端到端训练，并报告了在 Unitree Go2 机器人上的仿真到现实部署。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.26478v1](https://arxiv.org/abs/2605.26478v1)
