---
kind: ideas
granularity: day
period_start: '2026-05-28T00:00:00'
period_end: '2026-05-29T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- vision-language-action
- robot manipulation
- real-robot evaluation
- dexterous control
- spatial reasoning
- inference efficiency
tags:
- recoleta/ideas
- topic/vision-language-action
- topic/robot-manipulation
- topic/real-robot-evaluation
- topic/dexterous-control
- topic/spatial-reasoning
- topic/inference-efficiency
language_code: zh-CN
---

# Real-Robot VLA Deployment Controls

## 摘要
真实机器人 VLA 团队应先加入按吞吐量统计的 rollout 日志、延迟检查和小型适配层，再扩大任务宣称。最直接的操作变化集中在评估协议、逐步推理控制和灵巧手后训练上。

## Time-to-success logging for real-robot VLA comparisons
比较 VLA 策略的机器人实验室应把每次 rollout 都记成完成时间、硬失败或安全停止，然后报告带置信区间的 time-to-success 分布。PhAIL 提供了一个具体模板：用 Kaplan-Meier CDF、相同工装下的人类遥操作作为 Human-Relative Throughput 基线，以及按对象做 KS 检验来比较模型。

这套流程解决了一个常见的落地障碍：两种机器人策略在固定时间成功率上看起来接近，但其中一个更慢，或者失败尾部更差。在 PhAIL 的 Franka FR3 基准中，表现最好的 VLA 按 RMST 比值算大约比人类参考慢 7 倍，而且任何对象上都没有推理模型超过 19% 的 Human-Relative Throughput。一个低成本的起点是复用已有的 rollout 视频和日志，给任务完成和不可恢复失败补上时间戳，然后看当成功率换成完整完成时间分布后，排序是否变化。

### 资料来源
- [PhAIL: A Real-Robot VLA Benchmark and Distributional Methodology](../Inbox/2026-05-28--phail-a-real-robot-vla-benchmark-and-distributional-methodology.md): PhAIL defines time-to-success CDF evaluation, Human-Relative Throughput, bootstrap confidence intervals, and reports the gap between evaluated VLAs and same-fixture human teleoperation.
- [PhAIL: A Real-Robot VLA Benchmark and Distributional Methodology](../Inbox/2026-05-28--phail-a-real-robot-vla-benchmark-and-distributional-methodology.md): The paper abstract describes the open Franka FR3 benchmark, per-rollout artifacts, and the distributional evaluation method.

## Per-step compute scheduling around frozen VLA policies
部署 GR00T 类或 CogACT 类策略的团队，应该测试一个小型调度器，用来决定何时重新计算视觉编码器、LLM 和动作头，以及何时可以安全复用缓存表示。ElegantVLA 保持基础策略冻结，使用表示相似度、机器人运动和 episode 进度来选择每个控制步的计算模式。

实际问题在控制频率。每一步都运行所有组件，会让机器人在移动物体跟踪、接触、对齐、插入或放置时反应变慢。ElegantVLA 报告了基于 GR00T 的真实世界六任务测试：计算量减少 2.18×，控制频率从 13.8 Hz 提高到 26.3 Hz，平均成功率从 61.67% 提高到 65.00%。VisualThink-VLA 给出了一条相关的低延迟经验：稀疏视觉证据通道可以把推理维持在亚秒级，BridgeData V2 上每步 0.367 秒，而 ECoT 是 8.377 秒。一个有用的落地测试，是同时要求真实控制器上的任务成功率和实测 Hz，并分别检查稳定运动阶段和高接触阶段。

### 资料来源
- [ElegantVLA: Learning When to Think for Efficient Vision-Language-Action Models](../Inbox/2026-05-28--elegantvla-learning-when-to-think-for-efficient-vision-language-action-models.md): ElegantVLA describes a frozen-policy scheduler for vision, language, and action computation, with real-world gains in compute, control frequency, and success.
- [ElegantVLA: Learning When to Think for Efficient Vision-Language-Action Models](../Inbox/2026-05-28--elegantvla-learning-when-to-think-for-efficient-vision-language-action-models.md): The abstract states the per-step compute allocation mechanism and the GR00T real-world result of 13.8 Hz to 26.3 Hz.
- [VisualThink-VLA: Visual Intermediate Reasoning for Effective and Low-Latency Vision-Language-Action Policies](../Inbox/2026-05-28--visualthink-vla-visual-intermediate-reasoning-for-effective-and-low-latency-vision-language-action-policies.md): VisualThink-VLA reports sparse visual evidence routing with 0.367 s per step on BridgeData V2 versus 8.377 s for ECoT.

## Human-guided residual adaptation for dexterous VLA hands
灵巧手部署应把预训练 VLA 和真实机器人的纠正层分开。BORA 在在线使用时冻结基础策略，训练一个小的 residual actor，在风险状态下借助离线的 action-conditioned critic 和人工干预，添加按 chunk 计算的修正。

这对多自由度手很有用，因为接触误差会很快累积，而直接做全模型在线 RL 可能带来不安全的探索。在 5 个 Franka 机械臂加 12-DoF 手任务上，BORA-Full 的平均成功率达到 86.0%，而 consistency-policy 基线是 53.0%。在未见物体上，它达到 70.0%，同一基线是 27.0%。报告中的在线阶段在 2 轮 RL 内收敛，每个任务需要 1 到 2 次人工干预，在线轨迹时间里大约 20% 由人工控制。一个小规模验证可以从一个接触密集任务开始，冻结基础策略，测量 residual 修正是否能减少重复抓取、滑移或对齐失败，而不重新训练 VLA 主干。

### 资料来源
- [BORA: Bridging Offline Reinforcement Learning and Online Residual Adaptation for Real-World Dexterous VLA Models](../Inbox/2026-05-28--bora-bridging-offline-reinforcement-learning-and-online-residual-adaptation-for-real-world-dexterous-vla-models.md): BORA defines the offline critic, frozen base VLA, human-guided residual actor, and reports success gains on real dexterous tasks and unseen objects.
- [BORA: Bridging Offline Reinforcement Learning and Online Residual Adaptation for Real-World Dexterous VLA Models](../Inbox/2026-05-28--bora-bridging-offline-reinforcement-learning-and-online-residual-adaptation-for-real-world-dexterous-vla-models.md): The abstract states the lightweight human-in-the-loop residual adaptation mechanism and the reported 33-point and 43-point success improvements.
