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

# Robotics papers make execution supervision concrete

## 概览
这一天的机器人论文最强的是执行控制。主要工作把恢复信号、干预循环和物理约束直接加到动作系统里。LoHo-Manip、Hi-WM 和 BEHAVIOR1K 审计都说明了这个重点：长时程成功现在看的是策略能否恢复、能否被高效纠正，以及运行时是否保持安全。

## 研究发现

### Structured correction for long-horizon execution
长时程机器人工作围绕控制循环中的显式恢复逻辑展开。LoHo-Manip 把规划和执行分开，然后用当前图像、剩余计划记忆和 2D 轨迹提示重新规划。这个设计在 RoboVQA 上得到 63.1，在 EgoPlan2 上得到 56.7，超过了有名的 VLA 基线。ReCAPA 从另一个角度处理同样的失败模式。它预测动作、子目标和完整轨迹之间的不匹配，在 VisualAgentBench 上报 58.65，在 AI2-THOR 上报成功率 0.75。共同点很直接：论文把进度检查和纠正信号放进了执行过程，而不是放在策略外面。

#### 资料来源
- [Long-Horizon Manipulation via Trace-Conditioned VLA Planning](../Inbox/2026-04-23--long-horizon-manipulation-via-trace-conditioned-vla-planning.md): LoHo-Manip method and benchmark gains for progress-aware replanning with trace guidance.
- [ReCAPA: Hierarchical Predictive Correction to Mitigate Cascading Failures](../Inbox/2026-04-23--recapa-hierarchical-predictive-correction-to-mitigate-cascading-failures.md): ReCAPA hierarchy and results on cascading-failure mitigation.

### World models become intervention surfaces
世界模型开始被当作训练场，而不只是预测器。Hi-WM 在学习到的模拟器里推进策略，在接近失败时让人介入，再把这些纠正加入后训练。在三个真实机器人任务上，平均成功率比基础策略高 37.9 个百分点，比世界模型闭环基线高 19.0 个百分点。论文还报告了世界模型评估与真实性能之间的 Pearson r = 0.953。这让模拟器不仅能做离线评分，也能判断是否值得收集干预数据。

#### 资料来源
- [Hi-WM: Human-in-the-World-Model for Scalable Robot Post-Training](../Inbox/2026-04-23--hi-wm-human-in-the-world-model-for-scalable-robot-post-training.md): Hi-WM setup and real-world post-training gains.

### Action heads get explicit spatial and contact cues
几篇论文把物理结构在动作层面说得更清楚。CorridorVLA 预测几个未来的末端执行器锚点，并把生成动作限制在一个空间走廊内。这让 SmolVLA 在 LIBERO 上从 86.5% 提升到 90.95%，在 LIBERO-Plus 上从 45.37% 提升到 57.74%，GR00T 也有类似提升。FingerViP 给灵巧手加上五个指尖摄像头，让策略能看到腕部视角或第三人称视角看不到的接触区域。它在四个真实世界任务上的总体成功率是 80.8%，包括狭窄和遮挡场景。当天的机器人论文继续在接触附近增加结构：空间锚点、指尖视角，以及和实际运动几何绑定的信号。

#### 资料来源
- [CorridorVLA: Explicit Spatial Constraints for Generative Action Heads via Sparse Anchors](../Inbox/2026-04-23--corridorvla-explicit-spatial-constraints-for-generative-action-heads-via-sparse-anchors.md): CorridorVLA explicit spatial anchors and benchmark improvements.
- [FingerViP: Learning Real-World Dexterous Manipulation with Fingertip Visual Perception](../Inbox/2026-04-23--fingervip-learning-real-world-dexterous-manipulation-with-fingertip-visual-perception.md): FingerViP fingertip visual sensing and real-world dexterous results.

### Safety gets measured during execution
评估压力也变得更紧。BEHAVIOR1K 审计认为，最终状态指标会掩盖不安全执行和不稳定复现。在 500 次审查运行中，抓取失败是最常见错误，碰撞也很频繁。加入安全惩罚后，平均 RLC 分数从 Q = 0.256 降到 sQ = 0.239，Comet 从 0.192 降到 0.173。另一篇操作论文 Wiggle and Go! 从任务侧回应了同样的问题：它先用一次低风险试探动作估计绳子的动力学，再开始执行，在没有参数感知控制的情况下把真实目标精度做到 3.55 cm，而原来是 15.34 cm。信息很明确：更好的机器人结果现在依赖更安全的评估，以及在开始执行前更安全的信息收集。

#### 资料来源
- [How VLAs (Really) Work In Open-World Environments](../Inbox/2026-04-23--how-vlas-really-work-in-open-world-environments.md): Safety-aware audit of VLA execution and metric drops under safety penalties.
- [Wiggle and Go! System Identification for Zero-Shot Dynamic Rope Manipulation](../Inbox/2026-04-23--wiggle-and-go-system-identification-for-zero-shot-dynamic-rope-manipulation.md): Low-risk probing for zero-shot rope manipulation with large accuracy gain.
