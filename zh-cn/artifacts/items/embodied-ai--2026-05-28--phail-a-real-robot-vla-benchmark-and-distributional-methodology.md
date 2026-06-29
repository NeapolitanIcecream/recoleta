---
source: arxiv
url: https://arxiv.org/abs/2605.29710v1
published_at: '2026-05-28T10:10:19'
authors:
- Sergey Arkhangelskiy
topics:
- vision-language-action
- robot-benchmark
- real-robot-evaluation
- time-to-success
- robot-policy-ranking
- human-relative-throughput
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# PhAIL: A Real-Robot VLA Benchmark and Distributional Methodology

## Summary
## 摘要
PhAIL 是一个面向视觉-语言-动作策略的真实机器人基准和评估方法。它测量完整的成功耗时分布，而不只看固定超时下的成功率，因此可以用更少的 rollout 对接近的策略进行检验。

## 问题
- 真实机器人 VLA 论文常在一个超时点报告二元成功率，每个条件通常只有 N≤25 次 rollout，而且往往没有置信区间或配对检验。
- 二元成功率会漏掉速度、硬失败和尾部行为，所以两种策略可能看起来打平，也可能因为选了不同标量指标而互换顺序。
- 这个问题很重要，因为真实机器人 rollout 代价高，而薄弱的评估会用噪声给通用机器人策略排序。

## 方法
- PhAIL 把成功耗时的 CDF 作为主要评估对象：每次操作都贡献一个完成时间，不可恢复的失败记为 T=∞ 事件。
- 它用 Kaplan-Meier 生存分析估计 CDF，并报告 95% 的 episode-clustered bootstrap 置信区间。
- 它把评分和显著性检验分开。评分使用 Human-Relative Throughput，即同一夹具上人类参考 RMST 与模型 RMST 的比值。
- 显著性检验先对每个对象的 CDF 计算 Kolmogorov-Smirnov 统计量，再在对象之间做宏平均。
- 该基准运行在带 Robotiq 2F-85 夹爪、外部和腕部 RGB 相机、四类对象、公开 rollout 产物和参考实现的 Franka FR3 上。

## 结果
- 该基准包含约 995 个分析后的 episode，其中有 396 个同一夹具上的人类遥操作 rollout，覆盖四类对象：木勺、毛巾、剪刀和电池。
- 四个 VLA 在同一组 449 个 episode、约 13 小时的演示集上微调后进行评估：OpenPI π0.5、NVIDIA GR00T N1.6、ACT 和 SmolVLA。
- 人类遥操作的 RMST 为 10.5 s [10.3, 10.8]。OpenPI 的 RMST 为 77.7 s [69.2, 87.0]，HRT 为 13.8% [12.2, 15.7]；GR00T 的 RMST 为 77.2 s [69.0, 86.4]，HRT 为 13.3% [12.0, 15.2]。
- ACT 的 RMST 为 100.9 s [85.8, 117.6]，HRT 为 10.5% [9.2, 13.2]。SmolVLA 的 RMST 为 165.8 s [147.0, 185.6]，HRT 为 6.4% [5.7, 7.5]。
- 按 RMST 比值算，评估中最好的 VLA 比人类参考慢约 7 倍，而且没有任何推理模型在单个对象上超过 19% 的 HRT。
- 宏平均 KS 在每个模型-对象单元 N=25 时分开了 GR00T vs. ACT，在 N=30 时分开了 OpenPI vs. ACT；OpenPI vs. GR00T 仍未分开。论文把这一点和二元 McNemar 基线做了比较，后者要在每个单元里需要 600–1500 次配对 rollout 才能检测 5 个百分点的配对差异。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.29710v1](https://arxiv.org/abs/2605.29710v1)
