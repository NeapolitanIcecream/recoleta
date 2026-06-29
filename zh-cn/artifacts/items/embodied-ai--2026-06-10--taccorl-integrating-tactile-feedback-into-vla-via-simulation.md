---
source: arxiv
url: https://arxiv.org/abs/2606.11743v1
published_at: '2026-06-10T07:20:36'
authors:
- Siyu Ma
- Yuqi Liang
- Chang Yu
- Yunuo Chen
- Hao Su
- Yixin Zhu
- Yin Yang
- Chenfanfu Jiang
topics:
- vision-language-action
- tactile-feedback
- sim2real
- robot-rl
- contact-rich-manipulation
- bimanual-manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# TacCoRL: Integrating Tactile Feedback into VLA via Simulation

## Summary
## 摘要
TacCoRL 在预训练的 VLA 机器人策略中加入触觉感知，并先在仿真中训练接触修正，再部署到真实环境。它面向双臂的接触密集任务，这类任务里摄像头看不到局部对齐和压力线索。

## 问题
- 插入、装配和拼图放置这类接触密集操作需要局部接触状态，但视觉通常看不到错位、阻塞、压力或接触位置。
- 真实机器人示教成本高，而且大多只展示成功的标准行为，因此对接近失败的接触状态监督很弱。
- 在硬件上收集大量偏离标准的接触轨迹可能损坏传感器，而且重置成本高，会拖慢训练。

## 方法
- 策略以预训练的 VLA 主干为起点，并加入最近一段触觉历史窗口中的触觉 token。
- 二值接触门控会在读数像背景噪声时移除触觉 token，因此触觉主要在接触过程中影响策略。
- sim-real 联合训练把真实示教与仿真的遥操作和 MimicGen 轨迹混合起来，先为触觉条件动作做热启动。
- PPO 强化学习在一个与真实环境对齐的模拟器中使用稀疏任务奖励运行，同时在真实轨迹上的监督损失让策略保持接近真实机器人上的观测和动作分布。
- 最终策略可以直接部署到真实机器人，不需要特权的模拟器状态，也不需要在线真实世界 RL。

## 结果
- 在 4 个真实世界的双臂接触密集任务上，最终的视触觉策略平均成功率达到 72.5%，而仅视觉的 RL 后训练策略为 50.0%。
- RL 后训练后的真实任务成功率在 Test Tube Insertion 上为 70%，在 Do Puzzle 上为 45%，在 Assembly #1 上为 95%，在 Assembly #2 上为 80%，对应的是视触觉策略。
- 在相同的真实任务上，仅视觉的 RL 后训练成功率分别为 35%、25%、80% 和 60%。
- 在仿真中，带联合训练的 RL 将视触觉策略的平均成功率提高到 78.5%，将仅视觉策略提高到 60.5%。
- 直接从基础 VLA 做稀疏奖励 RL 时，4 个仿真任务的成功率全是 0.0，说明在 RL 微调前需要联合训练。
- 对 Assembly #2 的消融结果显示，真实数据锚定权重 β=0.1 和 β=1.0 都把真实世界成功率提高到 80%，而在相同的 α=0.5 联合训练比例下，没有锚定时只有 45%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.11743v1](https://arxiv.org/abs/2606.11743v1)
