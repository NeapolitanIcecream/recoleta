---
source: arxiv
url: http://arxiv.org/abs/2603.04351v1
published_at: '2026-03-04T18:16:58'
authors:
- Valentin Yuryev
- Josie Hughes
topics:
- sim2real
- tendon-driven-robot
- reinforcement-learning
- force-modeling
- transformer
- dexterous-manipulation
relevance_score: 0.89
run_id: materialize-outputs
language_code: zh-CN
---

# Tendon Force Modeling for Sim2Real Transfer of Reinforcement Learning Policies for Tendon-Driven Robots

## Summary
本文提出一种面向腱驱动机器人的数据驱动腱力建模方法，把仅有位置/编码器信号的伺服电机行为转成更真实的受力仿真，从而提升强化学习策略的 sim2real 迁移。核心贡献是用带时间上下文的 Transformer 力估计器配合接触感知数据采集台，在真实腱驱动手指上显著缩小仿真差距并提升跟踪控制效果。

## Problem
- 腱驱动机器人常用位置控制伺服而非可直接测力/测矩的执行器，导致 RL 所需的力驱动仿真与真实系统之间存在明显 sim2real gap。
- 这种差距不仅来自摩擦，还来自腱松弛、控制延迟、齿轮/执行器非线性和柔顺结构；若仿真假设“理想力源”，训练出的策略落地会明显失效。
- 这很重要，因为腱驱动结构广泛用于灵巧手、软体机器人和顺应性交互系统，若不能可靠迁移，RL 很难真正用于真实复杂操作。

## Approach
- 搭建一个带负载传感器的通用数据采集测试台，把伺服电机与弹簧/手指等腱驱动系统串联，在自由运动和接触场景下采集真实腱张力数据。
- 学习一个从历史编码器信号到腱力的映射：输入为过去 1.5 s 的期望位置、实测位置、实测速度，输出当前腱力估计；比较了 MLP、RNN 和 Transformer 三种时序模型。
- 其中 Transformer 编码器用因果自注意力处理整段历史，目标是在不依赖推理时力传感器的情况下捕捉慢速伺服的滞后、摩擦和上下文相关动态。
- 将学到的腱力模型嵌入 GPU 加速的腱力驱动刚体仿真中，再用 PPO 和 30% 范围的域随机化训练手指末端位姿跟踪策略。
- 与直接使用理想化力模型相比，该流程让仿真 rollout 的执行器行为更接近真实硬件，从而提高 RL 策略可迁移性。

## Results
- 在跨系统泛化测试中，Transformer 的平均力预测 RMSE 为 **0.61 N**，相当于电机最大力 **21 N** 的 **2.9%**；摘要中进一步概括为预测误差在最大电机力的 **3%** 以内。
- 作者报告 Transformer 相比 MLP 和 RNN 泛化更好：RNN 会明显漂移并在阶跃处产生尖峰，MLP 则更易出现高频振荡；Transformer 在弱弹簧、强弹簧和手指三种配置上整体最稳健。
- 将学习到的腱力模型集成到仿真后，论文声称对测试轨迹的 **sim-to-real gap 降低了 41%**。
- 基于该模型训练的 RL 控制器在真实腱驱动手指的指尖位姿跟踪任务上，相比基线实现 **50% 提升**（文中将基线描述为使用理想力源/理想力假设训练的控制器）。
- 数据与系统规模方面：共采集约 **36 分钟**、**80 Hz** 的真实数据；模型大小约 **0.1–0.2 MB**，可在树莓派 5 上推理。
- 论文节选未给出所有实验表格中的完整逐项数值（例如各接触场景和各模型的全面定量对比），但最强的定量结论是 **2.9% 力预测误差、41% sim2real gap 降低、50% 真实跟踪提升**。

## Link
- [http://arxiv.org/abs/2603.04351v1](http://arxiv.org/abs/2603.04351v1)
