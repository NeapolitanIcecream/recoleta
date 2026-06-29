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
StreamingVLA 通过让观测、动作生成和执行并行运行，而不是等待每个阶段完成，来加快视觉-语言-动作推理。它面向边缘设备和真实机器人部署，这类场景里 VLA 延迟会让动作变慢、停顿增多。

## 问题
- 标准 VLA 流水线，例如 $\pi_{0.5}$，会按顺序执行观测、动作生成和执行，所以机器人在每次动作块之间都要等待。
- 这会带来较高的单次动作延迟和较大的停顿间隙 $T_{\text{halt}} = T_{o}+T_{g}$，让执行过程出现卡顿。
- 对资源受限硬件上的具身系统来说，这个问题很重要，因为如果控制太慢或太不平滑，再强的策略也很难在真实任务里发挥作用。

## 方法
- 论文提出 **StreamingVLA**，一种分阶段的异步执行方案，把动作生成与执行重叠起来，也把观测与持续执行重叠起来。
- 为了重叠生成和执行，作者用 **action flow matching (AFM)** 取代按块扩散式动作预测。AFM 预测的是沿轨迹变化的动作流，而不是对动作块逐个去噪。通俗地说，模型直接输出下一小步动作，机器人就能立刻执行，而不用等整块动作都生成完。
- 为了让 AFM 能用于更大的 VLA 系统，作者加入了扩展的动作空间状态表示，并修改归一化方式，使状态在累积动作更新时仍保持可加性。
- 为了重叠观测和执行，作者加入 **adaptive early observation (AEO)**。一个轻量级 transformer 先预测剩余动作会把下一次观测嵌入改变量带到什么程度；只有当这些被跳过的动作显著性较低时，系统才提前观测。
- 运行时分析把重叠写成两个项，$O_{ge}$ 和 $O_{oe}$，说明阶段重叠可以同时降低单次动作时间和停顿间隙，而且不需要缩小基础模型。

## 结果
- 在 **LIBERO** 上，以 **$\pi_{0.5}$** 作为基础模型时，基线在 $h=5$ 下的 **平均成功率为 96.9%**，**单次动作时间为 74.5 ms**，**停顿间隙为 232.3 ms**。
- **StreamingVLA (AFM)** 保持 **97.1% 平均成功率**，同时把单次动作时间降到 **33.7 ms（2.21x 加速）**，把停顿间隙降到 **76.1 ms（缩短 3.05x）**。
- **StreamingVLA (AFM + AEO)** 给出了最均衡的流式结果：**94.9% 平均成功率**、**31.625 ms** 的单次动作时间（相比基线 **2.36x 加速**），以及 **36.0 ms** 的停顿间隙（**缩短 6.45x**）。
- 摘要报告，在不牺牲性能的情况下，整体实现了 **2.4x 延迟加速** 和 **6.5x 更低的执行停顿**。
- 与 LIBERO 上之前的快速执行基线相比，**VLASH** 的单次动作时间为 **40.6 ms**，平均成功率 **97.1%**；**StreamingVLA (AFM)** 更快，单次动作时间 **33.7 ms**，平均成功率同样是 **97.1%**；加入 AEO 后延迟进一步下降，但成功率会有一定回落。
- 朴素的提前观测会损害性能：**AFM+NEO** 的单次动作时间为 **29.3 ms**，停顿间隙为 **23.0 ms**，但平均成功率降到 **86.2%**。带显著性感知的 AEO 变体把这部分损失补回了大半，把平均成功率提高到 **94.9%**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.28565v1](http://arxiv.org/abs/2603.28565v1)
