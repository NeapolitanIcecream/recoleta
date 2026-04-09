---
source: arxiv
url: http://arxiv.org/abs/2603.28565v1
published_at: '2026-03-30T15:23:27'
authors:
- Yiran Shi
- Dongqi Guo
- Tianchen Zhao
- Feng Gao
- Liangzhi Shi
- Chao Yu
- ZhiJian Mo
- Qihua Xiao
- XiaoShuai Peng
- Qingmin Liao
- Yu Wang
topics:
- vision-language-action
- robot-foundation-models
- streaming-inference
- action-flow-matching
- early-observation
- libero-benchmark
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# StreamingVLA: Streaming Vision-Language-Action Model with Action Flow Matching and Adaptive Early Observation

## Summary
## 摘要
StreamingVLA 通过并行运行观察、动作生成和执行来加速 vision-language-action 推理，不再让每个阶段依次等待完成。它面向边缘设备和真实机器人部署场景，因为 VLA 延迟会导致机器人动作缓慢、走走停停。

## 问题
- 标准 VLA 流水线，如 $\pi_{0.5}$，按顺序执行观察、动作生成和执行，因此机器人会在一段动作执行完后等待下一段动作。
- 这会带来较高的单步动作延迟，以及较大的停顿间隔 $T_{\text{halt}} = T_{o}+T_{g}$，使执行出现卡顿。
- 这个问题对运行在受限硬件上的具身系统很关键，因为如果控制速度太慢或动作不平滑，再强的策略也难以胜任真实任务。

## 方法
- 论文提出 **StreamingVLA**，一种分阶段的异步执行方案，在执行过程中重叠动作生成，同时在持续执行时重叠观察。
- 为了重叠生成与执行，它用 **action flow matching (AFM)** 替代按块预测动作的扩散式方法。AFM 将单个动作预测为轨迹上的一次状态更新。简单说，模型直接输出下一小步动作，机器人可以立刻执行，而不必等待整个动作块生成完。
- 为了让 AFM 能用于更大的 VLA 系统，作者加入了扩展的动作空间状态表示，并修改了归一化方式，使状态在通过累计动作更新时仍保持可加性。
- 为了重叠观察与执行，他们提出 **adaptive early observation (AEO)**。一个轻量级 transformer 预测剩余动作会在多大程度上改变下一次观察的 embedding，只有当这些被跳过动作的显著性较低时，系统才会提前观察。
- 运行时分析定义了两个重叠项，$O_{ge}$ 和 $O_{oe}$，说明阶段重叠可以同时减少单步动作耗时和停顿间隔，而不需要缩小基础模型。

## 结果
- 在 **LIBERO** 上，以 **$\pi_{0.5}$** 为基础模型时，基线在 $h=5$ 下达到 **96.9% 平均成功率**、**74.5 ms** 单步动作耗时和 **232.3 ms** 停顿间隔。
- **StreamingVLA (AFM)** 将平均成功率保持在 **97.1%**，同时把单步动作耗时降到 **33.7 ms（2.21x 加速）**，把停顿间隔降到 **76.1 ms（3.05x 降低）**。
- **StreamingVLA (AFM + AEO)** 给出了整体更均衡的流式结果：**94.9% 平均成功率**、**31.625 ms** 单步动作耗时（相对基线 **2.36x 加速**），以及 **36.0 ms** 停顿间隔（**6.45x 降低**）。
- 摘要给出的总体结果是，在不牺牲性能的情况下，实现 **2.4x 延迟加速**，并将执行停顿降低 **6.5x**。
- 与 LIBERO 上先前的快速执行基线相比，**VLASH** 在 **97.1%** 平均成功率下的单步动作耗时是 **40.6 ms**，而 **StreamingVLA (AFM)** 在相同 **97.1%** 平均成功率下更快，为 **33.7 ms**；加入 AEO 后，延迟进一步下降，但成功率有一定回落。
- 朴素的提前观察会损害性能：**AFM+NEO** 的单步动作耗时达到 **29.3 ms**，停顿间隔为 **23.0 ms**，但平均成功率降到 **86.2%**。带显著性感知的 AEO 将这一损失的大部分恢复到 **94.9%** 平均成功率。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.28565v1](http://arxiv.org/abs/2603.28565v1)
