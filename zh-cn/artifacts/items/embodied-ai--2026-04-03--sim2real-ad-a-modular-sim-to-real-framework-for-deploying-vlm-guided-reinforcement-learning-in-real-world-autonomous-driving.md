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
Sim2Real-AD 是一个用于自动驾驶策略的 sim-to-real 部署流程，这些策略在 CARLA 中用 VLM 引导的强化学习训练。它面向零样本迁移到全尺寸真实车辆，通过连接仅有模拟器观测和模拟器特定控制输出来实现，而且不使用真实世界的 RL 训练数据。

## 问题
- 在 CARLA 中训练的 VLM 引导 RL 策略，通常接收特权的鸟瞰图语义输入，并输出与模拟器动力学绑定的控制信号，所以直接迁移到真实汽车时会失效。
- 这篇论文关注两个耦合的差距：一是干净的模拟器 BEV 与带噪的真实单目相机输入之间的观测差距，二是模拟器控制与真实车辆响应之间的动力学差距。
- 这很重要，因为即使驾驶 RL 在模拟中表现很好，如果策略不能在真实车辆上安全地闭环运行，部署仍然没有用。

## 方法
- 这个框架把迁移拆成四个模块：Geometric Observation Bridge（GOB）、Physics-Aware Action Mapping（PAM）、Two-Phase Progressive Training（TPT）和 Real-time Deployment Pipeline（RDP）。
- GOB 使用预训练语义分割和逆透视映射，把前视单目图像转换成与模拟器兼容的多通道 BEV，让策略看到更接近 CARLA 训练输入的表示。
- PAM 把策略输出空间从模拟器原生的低层控制改为曲率和目标速度等物理量，然后通过校准过的自行车模型和 PID 控制器映射到具体车辆。
- TPT 分两阶段适配策略：先在干净的模拟器 BEV 下适配新的动作语义，再适配带噪的 IPM 生成 BEV 观测。这样把两个变化分开处理，而不是逼策略一次学会两件事。
- 系统以 DriveVLM-RL 为基础实现，VLM 组件只在训练时用于奖励设计，在测试时移除，所以部署时使用的是轻量级神经驾驶策略。

## 结果
- 在全尺寸 Ford E-Transit 上进行零样本真实世界部署时，跟车、避障和停车标志交互的成功率分别为 **90%**、**80%** 和 **75%**。
- 论文称部署过程不使用任何真实世界 RL 训练数据，只需要大约 **30 分钟** 的轻量级平台标定。
- 论文还说，仿真实验保留了不同奖励范式下代表性 RL 算法的相对性能排序，并验证了各个模块的贡献。
- 摘要没有给出基准表、数据集规模、试验次数，或与先前 sim-to-real 基线的直接数值对比，所以提供文本里最强的量化证据是上面的三个真实车辆成功率。
- 作者称，这是最早几项在没有任何真实世界 RL 训练数据的情况下，将 CARLA 训练的 VLM 引导 RL 策略零样本、闭环部署到全尺寸真实车辆上的展示之一。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.03497v1](http://arxiv.org/abs/2604.03497v1)
