---
source: arxiv
url: http://arxiv.org/abs/2604.03497v1
published_at: '2026-04-03T22:41:45'
authors:
- Zilin Huang
- Zhengyang Wan
- Zihao Sheng
- Boyue Wang
- Junwei You
- Yue Leng
- Sikai Chen
topics:
- sim2real
- autonomous-driving
- vlm-guided-rl
- closed-loop-deployment
- birds-eye-view
relevance_score: 0.56
run_id: materialize-outputs
language_code: zh-CN
---

# Sim2Real-AD: A Modular Sim-to-Real Framework for Deploying VLM-Guided Reinforcement Learning in Real-World Autonomous Driving

## Summary
## 摘要
Sim2Real-AD 是一条面向自动驾驶策略的仿真到现实部署流程，适用于在 CARLA 中用 VLM 引导强化学习训练出的策略。它的目标是在不使用真实世界 RL 训练数据的情况下，通过弥合仅存在于模拟器中的观测和模拟器特有的控制输出，实现向全尺寸真实车辆的零样本迁移。

## 问题
- 在 CARLA 中训练的 VLM 引导 RL 策略通常依赖特权的鸟瞰语义输入，并输出与模拟器动力学绑定的控制信号，因此直接迁移到真实车辆时往往会失效。
- 论文聚焦于两个相互关联的鸿沟：一是干净的模拟器 BEV 与带噪声的真实单目相机输入之间的观测鸿沟，二是模拟器控制与真实车辆响应之间的动力学鸿沟。
- 这很重要，因为如果策略无法在真实车辆上安全地进行闭环运行，那么驾驶 RL 在仿真中的强结果就无法转化为实际部署能力。

## 方法
- 该框架将迁移拆分为四个模块：Geometric Observation Bridge (GOB)、Physics-Aware Action Mapping (PAM)、Two-Phase Progressive Training (TPT) 和 Real-time Deployment Pipeline (RDP)。
- GOB 使用预训练语义分割和逆透视映射，将前视单目图像转换为与模拟器兼容的多通道 BEV，让策略看到的表示更接近它在 CARLA 训练时的输入。
- PAM 将策略输出空间从模拟器原生的底层控制改为曲率、目标速度等物理量，再通过校准过的自行车模型和 PID 控制器映射到具体车辆。
- TPT 分两个阶段适配策略：先在干净的模拟器 BEV 下适应新的动作语义，再适应由 IPM 生成的、噪声更大的 BEV 观测。这样把两种变化分开处理，而不是让策略同时学习两者。
- 该系统以 DriveVLM-RL 为实例，其中 VLM 组件只在训练阶段用于奖励设计，并在测试时移除，因此部署时使用的是轻量级神经网络驾驶策略。

## 结果
- 在全尺寸 Ford E-Transit 上进行零样本真实世界部署时，论文报告的成功率分别为：跟车 **90%**、避障 **80%**、停车标志交互 **75%**。
- 论文称，部署过程**不使用真实世界 RL 训练数据**，只需要大约 **30 分钟**的轻量级平台标定。
- 文中表示，仿真实验保留了不同奖励范式下代表性 RL 算法的相对性能排序，并验证了各模块的贡献。
- 提供的摘录没有给出基准表、数据集规模、试验次数，也没有给出与以往 sim-to-real 基线的直接数值比较，因此在现有文本里，最有力的定量证据是上面的三个真实车辆成功率。
- 作者称，这是最早展示之一：在不使用任何真实世界 RL 训练数据的情况下，将在 CARLA 中训练的 VLM 引导 RL 策略以零样本方式部署到全尺寸真实车辆上，并实现闭环运行。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.03497v1](http://arxiv.org/abs/2604.03497v1)
