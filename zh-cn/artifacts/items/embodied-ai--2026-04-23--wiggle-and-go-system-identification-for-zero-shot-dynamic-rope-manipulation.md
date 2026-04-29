---
source: arxiv
url: http://arxiv.org/abs/2604.22102v1
published_at: '2026-04-23T22:17:45'
authors:
- Arthur Jakobsson
- Abhinav Mahajan
- Karthik Pullalarevu
- Krishna Suresh
- Yunchao Yao
- Yuemin Mao
- Bardienus Duisterhof
- Shahram Najam Syed
- Jeffrey Ichnowski
topics:
- dynamic-rope-manipulation
- system-identification
- sim-to-real
- zero-shot-control
- trajectory-optimization
relevance_score: 0.72
run_id: materialize-outputs
language_code: zh-CN
---

# Wiggle and Go! System Identification for Zero-Shot Dynamic Rope Manipulation

## Summary
## 摘要
Wiggle and Go! 先通过一次短暂的探测动作估计绳索动力学，再用这些估计参数在仿真中规划动态绳索动作，并在真实世界中直接执行，无需反复试错。论文面向零样本绳索任务，这类任务一旦失败，代价可能很高或存在安全风险。

## 问题
- 动态绳索操作很难，因为绳索行为取决于一些隐藏属性，例如刚度、阻尼、质量分布和链节数量。
- 以往方法通常需要大量真实世界数据集，或在任务中尝试多次才能适应；当一次糟糕的抛掷可能导致缠绕、损坏或偏离目标，而且很难补救时，这种做法并不合适。
- 论文的目标是先对特定绳索的动力学进行一次推断，再把这一估计复用于多个任务，并以零样本方式执行目标条件动作。

## 方法
- 该方法分为两个阶段：先执行一个预定义、低风险的“wiggle”动作来观察绳索运动，再预测绳索参数，并用这些参数优化任务动作。
- 一个时序卷积网络接收 wiggle 过程中跟踪得到的 2D 绳索关键点和角度特征，预测 9 个仿真器参数，包括刚度、阻尼、绳长、单位长度质量、前端配重质量和链节数量。
- 模型在仿真中训练，因为仿真中参数标签已知；训练时还加入了 sim-to-real 随机化，覆盖相机标定噪声、跟踪噪声、录制延迟和时间窗口遮蔽。
- 对每个任务目标，系统都会在 Drake 中使用预测的绳索参数运行 CMA-ES 轨迹优化，然后在 xArm 7 上执行得到的机器人轨迹。
- 同一个系统辨识模块不依赖具体任务，并被复用于三个下游任务：3D 目标击打、挑抛和搭挂。

## 结果
- 在真实 3D 目标击打任务上，方法在使用预测绳索系统参数时报告的**平均精度为 3.55 cm**，而动作模型未使用系统参数信息时为 **15.34 cm**。
- 在引言中，论文还报告真实环境下的**击打精度中位数为 3.55 cm**、仿真中为 **2.1 cm**；相比之下，未使用参数信息的基线在真实环境中为 **15.29 cm**，在仿真中为 **12.8 cm**。
- 对于把已识别动力学迁移到另一种运动情境，论文报告在一条未见过的轨迹上，预测绳索与真实绳索行为的傅里叶频率之间的**Pearson 相关系数为 0.95**。
- 在更复杂的下游任务中，论文称**挑抛**和**搭挂**的**成功率超过 50%**。
- 在 wiggle 消融表中，主要 wiggle 动作在多个预测参数上取得了较低的平均绝对误差，包括链节数量 **0.098**、绳长 **0.006 m**、球阻尼 **0.010 N·s/m**、绳索半径 **0.002 m**、单位长度质量 **0.007 kg/m**、前端配重质量 **0.005 kg**，以及球刚度 **0.111 N/m**；随机 wiggle 在若干参数上的表现更差。
- 论文称，一次 wiggle 观测就可以支持多个操作策略，而无需重新训练辨识模块。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.22102v1](http://arxiv.org/abs/2604.22102v1)
