---
source: arxiv
url: https://arxiv.org/abs/2607.14695v1
published_at: '2026-07-16T07:56:43'
authors:
- Yuanchun Guo
- Bingyan Liu
topics:
- vision-language-action
- robot-foundation-model
- streaming-inference
- real-time-control
- robot-data-scaling
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Reflex: Real-Time VLA Control through Streaming Inference

## Summary
## 摘要
Reflex 通过将与时间步无关的感知过程同依赖时间步的动作去噪过程分离，为流匹配视觉-语言-动作策略实现实时流式推理。在 LIBERO 和 Kinetix 上，其报告的推理速度最高提升 2.58 倍，支持稳定的 50 Hz 流式处理，使反应延迟最高降低 54%，且未测得任务性能下降。

## 问题
- 流匹配 VLA 策略需要迭代去噪，因此同步推理可能阻塞机器人执行，并增加动态操作中的反应延迟。
- 当时间步条件在整个网络中改变表示时，标准 KV 缓存从数学上并不成立；而对于 50–100 Hz 控制而言，完整重计算又过慢。
- 长时间运行的混合精度流式处理可能出现数值不稳定，从而限制可靠部署。

## 方法
- Reflex 将注意力上下文划分为固定的指令前缀、滑动的视觉历史窗口和动态的流生成后缀。它缓存前两个区域，只重新计算依赖时间步的状态；对于固定上下文窗口，这将更新开销降至 O(1)，同时保持与完整批处理注意力一致。
- 异步流水线在独立的数据流上运行视觉编码和动作生成，使感知过程与执行过程重叠，而不是让机器人等待每个推理周期完成。
- AdaRMSNorm 在 FP32 中计算方差，并使用时间步和本体感受状态条件，减少连续流式处理期间的 BFloat16 激活塌缩。
- 面向未来条件的状态预测用于补偿推理延迟；算子融合和预分配环形缓冲区则减少内核启动与内存分配开销。

## 结果
- 在使用 Pi0.5 的 LIBERO 上，推理延迟从 135.2 ms 降至 52.4 ms，速度提升 2.58 倍；参数量更大的 3.1B Pi0 达到 2.73 倍加速。
- 在 LIBERO 和 Kinetix 上，对于固定输入和固定观测窗口，Reflex 相对于完整批处理注意力均保持 0.00 MSE；而 Naive Cache 基线由于忽略时间步条件，报告的 MSE 大于 1.0。
- LIBERO 和 Kinetix 上的峰值 VRAM 分别下降 27% 和 24%；系统实现了稳定的 50 Hz 流式处理，反应延迟最高降低 54%。
- 报告中的任务评估显示，LIBERO 上的性能保持一致，且流式处理未造成性能下降；所提供的摘录不包含完整的任务成功率表，也未包含 Kinetix 的全部数值结果。
- 精确性保证适用于固定输入条件下的 Partitioned Attention，不适用于异步调度、未来状态预测或混合精度行为；此外，该方法不适用于感知编码器接收去噪时间步条件的架构。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.14695v1](https://arxiv.org/abs/2607.14695v1)
