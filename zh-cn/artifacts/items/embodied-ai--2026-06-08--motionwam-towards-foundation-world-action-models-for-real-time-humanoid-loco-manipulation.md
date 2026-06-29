---
source: arxiv
url: https://arxiv.org/abs/2606.09215v1
published_at: '2026-06-08T08:50:14'
authors:
- Jia Zheng
- Teli Ma
- Yudong Fan
- Zifan Wang
- Shuo Yang
- Junwei Liang
topics:
- world-action-models
- humanoid-loco-manipulation
- vision-language-action
- whole-body-control
- egocentric-video
- robot-data-scaling
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# MotionWAM: Towards Foundation World Action Models for Real-Time Humanoid Loco-Manipulation

## Summary
## 摘要
MotionWAM 是一个用于 Unitree G1 人形机器人 loco-manipulation 的实时 World Action Model，只用一台第一人称相机输入。它把视频世界模型特征和全身运动 token 结合起来，在同一个动作空间里控制腿、躯干、身高、脚和手。

## 问题
- 现有 WAM 策略在闭环人形控制中太慢，因为它们要在视频-动作潜变量上做迭代去噪。
- 许多人形系统把控制拆成上半身操作和下半身底盘指令，这会阻碍任务驱动的脚部动作，比如踩踏板或踢球。
- 这个问题很重要，因为真实的人形任务需要在同一个策略循环里协调平衡、行走、躯干运动、伸手和物体接触。

## 方法
- MotionWAM 将一个从 Cosmos-Predict2.5-2B 初始化的 Video DiT 与一个预测全身运动潜变量的 Motion DiT 配对。
- Video DiT 在较高噪声的 flow 步长上运行一次前向传播，并暴露中间去噪激活；策略直接使用这些特征，而不是等待完整生成的未来视频。
- 动作输出是一个统一的运动潜变量，由 SONIC 解码成关节指令，其中离散运动 token 负责全身运动，连续通道负责夹爪或灵巧手。
- 训练分 3 个阶段：先在约 2,136 小时的人类与人形第一人称视频上预训练视频分支，再在异构的 Unitree G1 数据上对视频和动作联合后训练，最后在 9 个目标任务上对每个任务用 200 个遥操作 episode 微调。

## 结果
- 在 9 个真实 Unitree G1 任务上，每个任务 20 次试验，MotionWAM 的平均成功率为 76.1%，强于最强基线 GR00T-N1.7 的 43.9%，提升 32.2 个百分点。
- 与最强列出的基线结果相比，MotionWAM 在 Kick Soccer（+40）、Load Cart（+40）、Retrieve Item（+40）、Wipe Board（+45）和 Do Laundry（+30）上的任务提升最大。
- 在一个 5 任务消融实验中，完整的 3 阶段模型平均成功率为 70.0%；去掉 Stage 1 后降到 59.0%，去掉 Stage 2 后降到 42.0%。
- MotionWAM 在一块 NVIDIA A100 上以 4.9 Hz 运行，可训练参数为 2.5B；Cosmos Policy 为 0.7 Hz，GR00T-N1.7 为 6.5 Hz，Qwen3DiT 为 9.0 Hz。
- 论文报告了真实硬件上的任务驱动脚部交互，包括踢球和踩踏板，而评测的上-下肢解耦控制设计无法通过其动作接口表达这些动作。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.09215v1](https://arxiv.org/abs/2606.09215v1)
