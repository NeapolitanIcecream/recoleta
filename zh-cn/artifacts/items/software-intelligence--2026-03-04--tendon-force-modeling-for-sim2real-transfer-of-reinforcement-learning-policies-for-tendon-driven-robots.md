---
source: arxiv
url: http://arxiv.org/abs/2603.04351v1
published_at: '2026-03-04T18:16:58'
authors:
- Valentin Yuryev
- Josie Hughes
topics:
- sim2real-transfer
- reinforcement-learning
- tendon-driven-robots
- force-modeling
- transformer
- robot-control
relevance_score: 0.13
run_id: materialize-outputs
language_code: zh-CN
---

# Tendon Force Modeling for Sim2Real Transfer of Reinforcement Learning Policies for Tendon-Driven Robots

## Summary
本文针对腱驱动机器人中强化学习策略难以从仿真迁移到真实系统的问题，提出了一个基于时序上下文的腱力学习模型。核心贡献是把仅依赖电机编码器信号的力估计器嵌入仿真，从而更真实地训练RL控制器并提升真实手指上的表现。

## Problem
- 腱驱动机器人常用位置控制舵机，但RL训练依赖较准确的力/扭矩驱动仿真；真实系统中电机摩擦、腱松弛、控制延迟和柔顺性会造成明显sim-to-real gap。
- 仅用理想力源或简单摩擦模型，无法覆盖接触丰富操作中的复杂非线性动力学，导致仿真中学到的策略落地效果差。
- 这很重要，因为腱驱动结构广泛用于灵巧手、软体机器人和顺应性交互系统，而高效可迁移控制一直是瓶颈。

## Approach
- 搭建了一个带负载传感器的通用数据采集平台，在弹簧系统和真实腱驱动手指上采集电机期望位置、实测位置、速度与真实腱力数据，并包含接触场景。
- 将腱力估计表述为时序监督学习：输入过去1.5秒历史窗口（30步、20Hz）的 \(\theta^d, \theta, \dot{\theta}\)，输出当前腱力估计 \(\hat F\)。
- 对比了MLP、RNN和Transformer编码器三类模型；作者认为Transformer通过自注意力更好利用长时上下文，因此更能刻画慢速舵机中的滞后、摩擦和方向相关效应。
- 把学到的腱力模型嵌入GPU加速的腱力驱动刚体仿真中，再结合PPO和30%范围的domain randomization训练手指末端位姿跟踪策略。
- 推理阶段无需力传感器，只依赖电机编码器信号，因此方法具有机器人无关性并更易部署。

## Results
- 在弱弹簧、强弹簧和手指三种系统上的总体比较中，Transformer平均RMSE为 **0.61 N**，约等于电机最大力 **21 N** 的 **2.9%**；文中称其优于RNN，并且比MLP具有更好的跨系统泛化。
- 摘要中声称该Transformer力模型可将腱力预测误差控制在 **最大电机力的3%以内**，且对不同机器人系统具有通用性。
- 将学习到的力模型接入仿真后，作者报告测试轨迹上的 **sim-to-real gap降低41%**；摘录未给出更细的轨迹指标定义或完整表格。
- 基于该模型训练的RL控制器在真实腱驱动机器人手指的指尖位姿跟踪任务上，相比基线获得 **50% improvement**；基线为使用理想力源估计训练的控制器。
- 文中还定性指出：RNN在测试中出现明显漂移和阶跃时的力尖峰；MLP在输入微扰下更容易产生高频振荡；Transformer在不同系统和接触情形下最稳健。
- 由于提供内容被截断，接触丰富场景的更细粒度定量结果未完整展示。

## Link
- [http://arxiv.org/abs/2603.04351v1](http://arxiv.org/abs/2603.04351v1)
