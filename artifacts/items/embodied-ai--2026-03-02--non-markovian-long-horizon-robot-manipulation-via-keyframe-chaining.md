---
source: arxiv
url: http://arxiv.org/abs/2603.01465v1
published_at: '2026-03-02T05:26:29'
authors:
- Yipeng Chen
- Wentao Tan
- Lei Zhu
- Fengling Li
- Jingjing Li
- Guoli Yang
- Heng Tao Shen
topics:
- vision-language-action
- long-horizon-manipulation
- non-markovian-memory
- keyframe-retrieval
- generalist-robot-policy
relevance_score: 0.95
run_id: materialize-outputs
---

# Non-Markovian Long-Horizon Robot Manipulation via Keyframe Chaining

## Summary
该论文提出 Keyframe-Chaining VLA，用稀疏但语义关键的历史帧替代密集短窗口历史，让机器人在长时程、非马尔可夫操作任务中记住真正重要的过去。核心思想是在执行过程中自动挑出“关键时刻”并把这些帧串起来供 VLA 策略检索。

## Problem
- 现有 VLA 多依赖当前观测或短时密集历史，默认任务近似满足马尔可夫性；但很多长时程操作需要记住早先发生过的关键事件。
- 直接扩展上下文窗口会带来注意力计算开销，难以满足实时机器人控制。
- 现有检索、压缩或层级规划方法要么丢失精细时空信息，要么推理慢，仍难处理**仅由特定过去状态决定当前动作**的非马尔可夫依赖。

## Approach
- 提出 **Keyframe-Chaining VLA**：先用独立的 Keyframe Selection Module (KSM) 从连续视觉流中在线选出少量语义关键帧，再把这些关键帧与当前观测一起输入 VLA 策略。
- KSM 分两阶段训练：先用 triplet loss 学到区分不同任务/阶段/时间邻域的视觉嵌入空间；再用任务调制的查询网络，根据任务和当前执行阶段生成查询，匹配是否到达下一个语义里程碑。
- 查询机制用 FiLM 调制 phase embedding，使“同一个阶段概念”在不同任务下具有不同语义；再通过 cross-attention 从滑动窗口视觉特征中得到匹配分数，超过阈值就缓存为关键帧。
- 为减少抖动和误触发，作者加入 greedy temporal smoothing：在验证窗口内持续更新候选关键帧，只有分数回落并稳定后才最终提交。
- 动作策略采用 GR00T-N1.5/flow-matching backbone，不改主干架构，只把历史关键帧作为交错视觉 token 和结构化提示注入，从而以较低开销获得全局时序感知。

## Results
- 在作者新建的 **4 个 ManiSkill 非马尔可夫任务**上，方法平均成功率 **92.0%**，显著高于最强基线 **57.0%**，绝对提升 **35.0 个百分点**。
- 按任务看，Keyframe-Chaining VLA 分别达到：**Spatial 70.0%**, **Temporal 98.0%**, **Identity 100.0%**, **Counting 100.0%**。
- 与代表性基线相比：**π0** 平均仅 **15.5%**；**Diffusion Policy** 平均 **15.5%**；**GR00T-N1.5 (No History)** 平均 **16.0%**。
- 短时密集历史也不够：GR00T-N1.5 使用 short-term history 时，平均最好约 **27.0%**（N_h=3, I=1），远低于作者方法的 **92.0%**。
- 固定步长长时采样的最强配置平均 **57.0%**（GR00T-N1.5, N_h=3, I=40），仍明显落后于关键帧链式历史；说明“挑对历史帧”比“机械拉长历史”更有效。
- 文中还宣称在真实世界长时程部署上也显著优于基线，但给定摘录未提供对应的具体数值。

## Link
- [http://arxiv.org/abs/2603.01465v1](http://arxiv.org/abs/2603.01465v1)
