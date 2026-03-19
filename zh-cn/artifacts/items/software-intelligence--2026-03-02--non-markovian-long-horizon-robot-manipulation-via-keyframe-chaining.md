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
- robot-manipulation
- vision-language-action
- long-horizon-planning
- non-markovian-memory
- keyframe-retrieval
relevance_score: 0.2
run_id: materialize-outputs
language_code: zh-CN
---

# Non-Markovian Long-Horizon Robot Manipulation via Keyframe Chaining

## Summary
本文提出 Keyframe-Chaining VLA，通过自动挑选并串联少量关键历史帧，让机器人在长时程、非马尔可夫操作任务中记住真正重要的过去。其核心价值是用稀疏语义记忆替代密集历史窗口，在更低时序冗余下显著提升长期依赖推理能力。

## Problem
- 现有 VLA 往往主要依赖当前观测或很短的历史窗口，难以处理**非马尔可夫**任务：正确动作取决于某些过去状态，而不是当前画面。
- 直接拉长上下文窗口会带来注意力计算开销暴涨，难以满足机器人实时控制需求。
- 现有检索、压缩或层级规划方法，要么丢失细粒度空间信息，要么推理慢，且难以稳定解决状态混淆（state aliasing）。

## Approach
- 提出 **Keyframe-Chaining VLA**：不是保存整段密集视频，而是在线提取少量“语义关键帧”，把它们与当前观测一起送入 VLA 策略。
- 设计两阶段 **Keyframe Selection Module (KSM)**：先用度量学习训练视觉编码器，学习能区分任务阶段的嵌入空间；再用任务调制查询网络，根据当前任务/阶段去匹配是否到达关键里程碑。
- 查询机制使用 **FiLM** 把任务身份注入共享阶段表示，再通过 cross-attention 从最近视觉窗口中判断当前是否触发关键帧，从而实现“进度感知”的历史检索。
- 为了减少在线抖动误检，加入 greedy temporal smoothing：候选关键帧只有在一段验证窗口后才正式写入历史缓冲区。
- 在策略端，使用 **GR00T-N1.5** 作为骨干，把历史关键帧与当前观测组成稀疏语义历史，并以交错视觉 token/结构化提示词条件化 flow-matching 动作头。

## Results
- 在作者构建的 **4 个 ManiSkill 非马尔可夫任务**上，方法平均成功率 **92.0%**，显著高于最强基线 **57.0%**，绝对提升 **35.0 个百分点**。
- 相比无历史的 **GR00T-N1.5**，其平均成功率从 **16.0%** 提升到 **92.0%**；相比短期历史 GR00T（最佳表中平均 **27.0%**），提升更大。
- 对四项任务分别达到：**Spatial 70.0%**、**Temporal 98.0%**、**Identity 100.0%**、**Counting 100.0%**。
- 最强固定步长长程采样基线为 **GR00T-N1.5, N_h=3, I=40**，平均 **57.0%**；作者方法在保持稀疏记忆表示的同时进一步超过该基线 **35.0 个百分点**。
- 其他代表性基线表现明显较弱：**π0** 平均 **15.5%**，**Diffusion Policy** 平均 **15.5%**，说明仅依赖当前或短局部上下文难以解决记忆依赖任务。
- 论文还声称方法在真实世界长时程部署中同样优于基线，但给定摘录中未提供对应真实机器人量化数值。

## Link
- [http://arxiv.org/abs/2603.01465v1](http://arxiv.org/abs/2603.01465v1)
