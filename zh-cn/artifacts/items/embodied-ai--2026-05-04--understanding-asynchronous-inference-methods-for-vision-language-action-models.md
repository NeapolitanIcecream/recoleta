---
source: arxiv
url: https://arxiv.org/abs/2605.08168v1
published_at: '2026-05-04T18:01:15'
authors:
- Ayoub Agouzoul
topics:
- vision-language-action
- generalist-robot-policy
- asynchronous-inference
- robot-control-latency
- action-chunking
- libero-benchmark
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Understanding Asynchronous Inference Methods for Vision-Language-Action Models

## Summary
## 摘要
这篇论文发现，在异步 VLA 控制的高延迟场景中，A2C2 是表现最强的方法；TT-RTC 在有效时运行成本最低。研究主要是在受控条件下对现有方法做基准测试，使用两个统一代码库和匹配的评估设置。

## 问题
- VLA 策略通常会预测动作块，但推理耗时较长，动作块准备好时，机器人已经在基于旧观测执行动作。
- 同步执行会通过暂停机器人来避免观测过期，这会降低控制频率，并可能影响快速操作或动态控制。
- 之前处理这一延迟问题的方法分别在不同代码库、基础策略、数据集和协议下测试，因此难以比较它们的取舍。

## 方法
- 论文在共享实现下比较四种方法：IT-RTC、TT-RTC、VLASH 和 A2C2。
- IT-RTC 固定已经提交的动作前缀，并在流匹配推理期间对动作块的其余部分做修复填充。
- TT-RTC 用模拟延迟训练策略，使其学会以动作前缀为条件预测剩余动作，且不增加推理成本。
- VLASH 通过将状态向前滚动来估计执行时的机器人状态，然后让策略以该未来状态为条件。
- A2C2 在每个控制步运行一个小型修正模型，并向过期的基础策略动作添加残差动作。

## 结果
- 在 Kinetix 上，使用 10 个环境、动作块大小 H=16 时，A2C2 在延迟 d=8 以内的求解率保持在 90% 以上，而朴素异步基线降到 40% 以下。
- 在 Kinetix 上，使用 H=30 且延迟最高到 d=15 时，A2C2 总体领先；TT-RTC 在 d_max 为 4、8 和 15 时都有良好泛化；IT-RTC 在高延迟下相比朴素方法提升很小。
- 在 LIBERO 上，使用 SmolVLA、40 个任务、H=50，以及延迟 d∈{0,1,2,4,8,15,20} 时，A2C2 从 d≥4 开始领先，并在 d=20 时达到约 58% 的成功率。
- 在 LIBERO d=20 时，朴素基线约为 10-12%，IT-RTC 约为 20%，TT-RTC 在 d_max=8 时约为 25%、在 d_max=4 时约为 33%，而 d_max=8 或 16 的 VLASH 保持在约 55-56%。
- LIBERO 上的 VLASH 使用真实未来状态，因为该基准的状态维度和动作维度不匹配，所以它的高延迟结果是可部署版本的上界。
- 在 RTX 3090 上运行 LIBERO 时，朴素 SmolVLA 推理每个动作块耗时 405.2 ms，TT-RTC 为 402.7 ms，IT-RTC 为 469.7 ms，A2C2 串行推理为 412.4 ms；A2C2 残差头单独耗时 7.27 ms。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08168v1](https://arxiv.org/abs/2605.08168v1)
