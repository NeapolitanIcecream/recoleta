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
Wiggle and Go! 先通过一次短暂的探测动作估计绳索动力学参数，再用这些参数在仿真中规划动态绳索动作，并在真实环境中直接执行，不需要反复试错。论文面向零样本绳索任务，这类任务里失败代价可能很高，也可能带来安全风险。

## 问题
- 动态绳索操作很难，因为绳索行为取决于一些隐藏属性，例如刚度、阻尼、质量分布和链节数量。
- 以往方法通常需要大量真实世界数据，或者需要多次尝试任务后再调整；在一次失手就可能缠结、损坏或偏离目标且难以恢复的场景里，这种做法并不合适。
- 这篇论文的目标是先一次性推断出绳索特定的动力学，再把这个估计复用于不同任务，并直接执行面向目标的动作。

## 方法
- 该方法分两步：先执行一个预定义的低风险“wiggle”动作来观察绳索运动，然后预测绳索参数，并用这些参数优化任务动作。
- 一个时间卷积网络接收 wiggle 过程中跟踪得到的二维绳索关键点和角度特征，预测 9 个仿真参数，包括刚度、阻尼、绳长、单位长度质量、前端质量和链节数量。
- 模型在仿真中训练，参数标签已知，并加入 sim-to-real 随机化，覆盖相机标定噪声、跟踪噪声、延迟记录和时间窗口遮挡。
- 对于每个任务目标，系统在 Drake 中使用预测的绳索参数运行 CMA-ES 轨迹优化，然后把得到的机器人轨迹执行到 xArm 7 上。
- 这个系统识别模块不针对特定任务，在 3D 目标击打、抛掷和悬挂这三个下游任务中复用。

## 结果
- 在真实环境的 3D 目标击打任务中，使用预测的绳索系统参数时，方法报告的**平均精度为 3.55 cm**；当动作模型没有系统参数信息时，**平均精度为 15.34 cm**。
- 在引言中，论文还报告了**真实环境下的击打中位误差为 3.55 cm**、**仿真中的中位误差为 2.1 cm**；而没有参数信息的基线分别是**真实环境 15.29 cm**和**仿真 12.8 cm**。
- 在把识别出的动力学迁移到不同运动情境时，论文报告在一条未见过的轨迹上，预测绳索行为与真实绳索行为的傅里叶频率之间的**Pearson 相关系数为 0.95**。
- 在更复杂的下游任务上，论文声称**抛掷**和**悬挂**的**成功率超过 50%**。
- 在 wiggle 消融表中，主要 wiggle 在多个预测参数上的平均绝对误差都较低，包括链节数量 **0.098**、绳长 **0.006 m**、球阻尼 **0.010 N·s/m**、绳半径 **0.002 m**、单位长度质量 **0.007 kg/m**、前端质量 **0.005 kg** 和球刚度 **0.111 N/m**；随机 wiggle 在若干参数上的表现更差。
- 论文声称，一次 wiggle 观察就能支持多种操作策略，而不需要重新训练识别模块。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.22102v1](http://arxiv.org/abs/2604.22102v1)
