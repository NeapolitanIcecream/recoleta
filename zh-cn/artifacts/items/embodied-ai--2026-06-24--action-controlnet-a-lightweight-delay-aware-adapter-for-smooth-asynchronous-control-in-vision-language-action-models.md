---
source: arxiv
url: https://arxiv.org/abs/2606.25985v1
published_at: '2026-06-24T15:53:43'
authors:
- Tiecheng Guo
- Meng Guo
topics:
- vision-language-action
- robot-control
- asynchronous-control
- action-adapter
- robot-manipulation
- delay-compensation
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Action ControlNet: A Lightweight Delay-Aware Adapter for Smooth Asynchronous Control in Vision-Language-Action Models

## Summary
## 摘要
ACNet 通过把推理延迟期间已经执行的运动输入动作头，使分块式 VLA 机器人策略适配异步执行。它的目标是在不重新训练完整骨干网络的情况下，减少动作块交接时的抖动。

## 问题
- 大型 VLA 骨干网络和生成式动作头会增加推理延迟，使同步机器人控制在动作块之间暂停。
- 异步执行去掉了空等时间，但机器人继续运动时，下一个动作块仍基于过时观测来预测。
- 直接拼接动作块可能导致动作跳变、抖动和接触任务失败；对大型预训练策略进行完整的延迟条件重训练成本很高。

## 方法
- 论文把推理延迟期间已执行的运动视为下一个动作块的关键边界信号。
- ACNet 取前一个动作块中已执行的后缀，称为延迟动作，并用可学习 token 将其填充到完整动作时域。
- 一个小型 transformer 对该延迟动作进行编码，随后投影层把它作为残差注入到基本冻结的动作头中。
- 感知-语言骨干网络保持冻结，该适配器面向 diffusion 和 flow matching 等生成式动作头设计。
- 训练会采样不同延迟并复用缓存的视觉-语言 latent，因此覆盖不同延迟不需要重复运行完整骨干网络。

## 结果
- 在 Kinetix 上，对于 d>0 的延迟设置，ACNet 的平均成功率达到 0.79；Naïve Async 为 0.61，RTC 为 0.72，Training-RTC 为 0.80。
- 在 Kinetix 上，ACNet 训练约 20% 的模型参数，而 Training-RTC 更新 100%。
- 在 Meta-World MT50 上，当 H=50 且延迟 d=0,5,10,15 时，ACNet 的平均成功率为 0.74，与 Training-RTC 的 0.74 持平，高于 Naïve Async 的 0.70 和 RTC 的 0.71。
- 在 Meta-World MT50 上，ACNet 报告的延迟为 91 ms，控制频率为 11.0 Hz；RTC 为 159 ms 和 6.28 Hz，Training-RTC 为 134 ms 和 7.46 Hz。论文称，这一延迟收益主要来自 ACNet 使用的 Evo-1 骨干网络，而不只来自适配器本身。
- 在真实 SO-ARM101 设置中，使用 50 次训练 rollout，并对每个任务进行 10 次试验，ACNet 在两个任务共 20 次试验中全部成功；Naïve Async 为 17/20。
- 在 Meta-World nut-assembly-v3 和 plate-slide-back-v3 上，H=50 且 d=10 的 jerk 图显示 ACNet 的动作块过渡更平滑，但摘录没有提供 jerk 数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.25985v1](https://arxiv.org/abs/2606.25985v1)
