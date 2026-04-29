---
kind: trend
trend_doc_id: 180
granularity: day
period_start: '2026-04-23T00:00:00'
period_end: '2026-04-24T00:00:00'
topics:
- robotics
- vision-language-action
- long-horizon manipulation
- world models
- safety evaluation
- dexterous manipulation
run_id: materialize-outputs
aliases:
- recoleta-trend-180
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/long-horizon-manipulation
- topic/world-models
- topic/safety-evaluation
- topic/dexterous-manipulation
language_code: zh-CN
---

# 机器人论文把执行监督做得更具体

## Overview
这一天的机器人论文最突出的方向是执行控制。主要工作把恢复信号、干预闭环和物理约束直接加到动作系统里。LoHo-Manip、Hi-WM 和 BEHAVIOR1K 审计体现了这个重点：长时程成功越来越取决于策略在运行中能否恢复、能否被高效纠正，以及能否保持安全。

## Clusters

### 长时程执行中的结构化纠错
长时程机器人研究的重点转向把明确的恢复逻辑放进控制闭环。LoHo-Manip 将规划与执行拆开，然后基于当前图像、剩余计划记忆和 2D 轨迹提示重新规划。这个设计在 RoboVQA 上达到 63.1，在 EgoPlan2 上达到 56.7，超过文中点名的 VLA 基线。ReCAPA 从另一个角度处理同类失效问题。它预测动作、子目标和完整轨迹之间的不匹配，在 VisualAgentBench 上得到 58.65，在 AI2-THOR 上的成功率为 0.75。共同点很明确：这些论文把进度检查和纠错信号放进执行过程中，而不是留在策略之外。

#### Evidence
- [Long-Horizon Manipulation via Trace-Conditioned VLA Planning](../Inbox/2026-04-23--long-horizon-manipulation-via-trace-conditioned-vla-planning.md): LoHo-Manip 方法，以及基于轨迹引导的进度感知重规划所带来的基准提升。
- [ReCAPA: Hierarchical Predictive Correction to Mitigate Cascading Failures](../Inbox/2026-04-23--recapa-hierarchical-predictive-correction-to-mitigate-cascading-failures.md): ReCAPA 的层级结构，以及它在缓解级联失败上的结果。

### 世界模型变成干预界面
世界模型开始被当作训练工作区使用，而不只是预测器。Hi-WM 在学习到的模拟器中展开策略，在接近失败时让人类介入，再把这些修正加入后训练。在三个真实机器人任务上，平均成功率比基础策略提高 37.9 个点，比世界模型闭环基线提高 19.0 个点。论文还报告世界模型评估与真实性能之间的 Pearson r = 0.953。这说明模拟器不只适合离线打分，也适合判断何时值得收集干预数据。

#### Evidence
- [Hi-WM: Human-in-the-World-Model for Scalable Robot Post-Training](../Inbox/2026-04-23--hi-wm-human-in-the-world-model-for-scalable-robot-post-training.md): Hi-WM 的设置，以及它在真实世界后训练中的收益。

### 动作头加入明确的空间与接触线索
有几篇论文在动作层把物理结构写得更明确。CorridorVLA 预测少量未来末端执行器锚点，并约束生成动作保持在一个空间走廊内。这让 SmolVLA 在 LIBERO 上从 86.5% 提高到 90.95%，在 LIBERO-Plus 上从 45.37% 提高到 57.74%，GR00T 也有相近提升。FingerViP 给灵巧手加了五个指尖相机，让策略能看到腕部视角或第三人称视角看不到的接触区域。它在四个真实世界任务上的总体成功率为 80.8%，其中包括受限和遮挡场景。这一天的机器人论文持续在接触附近增加结构：空间锚点、指尖视角，以及与实际运动几何直接相关的信号。

#### Evidence
- [CorridorVLA: Explicit Spatial Constraints for Generative Action Heads via Sparse Anchors](../Inbox/2026-04-23--corridorvla-explicit-spatial-constraints-for-generative-action-heads-via-sparse-anchors.md): CorridorVLA 的显式空间锚点，以及基准结果的提升。
- [FingerViP: Learning Real-World Dexterous Manipulation with Fingertip Visual Perception](../Inbox/2026-04-23--fingervip-learning-real-world-dexterous-manipulation-with-fingertip-visual-perception.md): FingerViP 的指尖视觉感知，以及真实世界灵巧操作结果。

### 安全性开始在执行过程中被衡量
评估压力也变得更严。BEHAVIOR1K 审计指出，终态指标会掩盖不安全的执行过程和不稳定的复现结果。在审查的 500 次运行中，抓取失败是最常见的错误，碰撞也很常见。加入安全惩罚后，平均 RLC 分数从 Q = 0.256 降到 sQ = 0.239，Comet 从 0.192 降到 0.173。另一篇操作论文 Wiggle and Go! 也对应了同样的问题，不过是从任务侧入手：它在正式动作前先用一次低风险探测运动估计绳索动力学，然后把真实目标误差做到 3.55 cm；没有参数感知控制时，这个数值是 15.34 cm。结论很实际。更好的机器人结果现在依赖更安全的评估，以及在正式执行前更安全的信息获取。

#### Evidence
- [How VLAs (Really) Work In Open-World Environments](../Inbox/2026-04-23--how-vlas-really-work-in-open-world-environments.md): 面向安全的 VLA 执行审计，以及加入安全惩罚后的指标下降。
- [Wiggle and Go! System Identification for Zero-Shot Dynamic Rope Manipulation](../Inbox/2026-04-23--wiggle-and-go-system-identification-for-zero-shot-dynamic-rope-manipulation.md): 用于零样本绳索操作的低风险探测，以及显著的精度提升。
