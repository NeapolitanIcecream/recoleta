---
kind: trend
trend_doc_id: 839
granularity: day
period_start: '2026-07-09T00:00:00'
period_end: '2026-07-10T00:00:00'
topics:
- "\u673A\u5668\u4EBA\u64CD\u4F5C"
- "\u89C6\u89C9-\u8BED\u8A00-\u52A8\u4F5C\u6A21\u578B"
- "\u7B56\u7565\u9002\u5E94"
- "\u65F6\u95F4\u8BB0\u5FC6"
- "\u7075\u5DE7\u64CD\u4F5C\u57FA\u51C6"
run_id: materialize-outputs
aliases:
- recoleta-trend-839
tags:
- recoleta/trend
- "topic/\u673A\u5668\u4EBA\u64CD\u4F5C"
- "topic/\u89C6\u89C9-\u8BED\u8A00-\u52A8\u4F5C\u6A21\u578B"
- "topic/\u7B56\u7565\u9002\u5E94"
- "topic/\u65F6\u95F4\u8BB0\u5FC6"
- "topic/\u7075\u5DE7\u64CD\u4F5C\u57FA\u51C6"
language_code: zh-CN
---

# 机器人策略的提升取决于记忆、定向适应和更高难度的灵巧操作测试

## Overview
这一时期的机器人学习工作集中于提高现有策略在扰动和稀疏反馈下的可靠性。Harness VLA 在冻结控制器外加入规划和重试。Prompt-Driven Exploration 搜索由语言条件控制的行为。DexVerse 说明这些控制为何重要：领先方法在其测试的灵巧操作任务上平均成功率只有 34%。

## Clusters

### 记忆与任务状态控制
多篇论文为视觉-语言-动作（VLA）策略加入对任务进度的显式控制。Harness VLA 将冻结的 VLA 视为短时、可重试的接触技能，由规划器负责目标定位、搬运、暂存和失败恢复。在 LIBERO-Pro 上，它的成功率达到 82.4%，而直接使用冻结策略的基线为 50.0%。TFP 保存每个回合内的信念状态，并根据经过的时间和交互事件更新该状态；真实机器人上的物体交换成功率从 3/20 提升到 15/20。LEEVLA 在训练期间加入与任务相关的区域加权和潜在未来特征预测，在 LIBERO 上达到 98.2%，推理成本没有增加。

#### Evidence
- [Harness VLA: Steering Frozen VLAs into Reliable Manipulation Primitives via Memory-Guided Agents](../Inbox/2026-07-09--harness-vla-steering-frozen-vlas-into-reliable-manipulation-primitives-via-memory-guided-agents.md): 规划器控制的暂存、重试机制、冻结 VLA 设计和 LIBERO-Pro 结果。
- [TFP: Temporally Conditioned Memory-Fusion Policies for Visuomotor Learning](../Inbox/2026-07-09--tfp-temporally-conditioned-memory-fusion-policies-for-visuomotor-learning.md): 连续时间任务记忆和真实机器人物体交换结果。
- [LEEVLA: Seeing What Matters in Latent Environment Evolution for Vision-Language-Action](../Inbox/2026-07-09--leevla-seeing-what-matters-in-latent-environment-evolution-for-vision-language-action.md): 任务感知的视觉加权、潜在特征预测和 LIBERO 性能。

### 定向适应与探索
适应方法正在改造预训练策略周围的小型接口。FlowDAgger 将稀疏的人类纠正转换为冻结生成式控制器的潜在噪声目标。在 12 个 MetaWorld 任务上，运行 50 个回合后平均成功率达到 0.78，基础策略为 0.53。Prompt-Driven Exploration 检查运行视频后重写任务提示；在其微波炉案例中，规范提示的成功率达到约 98%，而动作噪声 PPO 仍接近于零。CLAP 在数值控制之前加入自然语言动作描述。其 2B 模型经过一个训练周期后在 LIBERO 上达到 90.8%，比匹配的基线高 14.9 个百分点。

#### Evidence
- [FlowDAgger: Human-in-the-Loop Adaptation of Generative Robot Policies in Latent Space](../Inbox/2026-07-09--flowdagger-human-in-the-loop-adaptation-of-generative-robot-policies-in-latent-space.md): 潜在动作反演、稀疏干预设置和 MetaWorld 结果。
- [Prompt-Driven Exploration](../Inbox/2026-07-09--prompt-driven-exploration.md): 基于提示的探索机制和从零奖励开始的结果。
- [CLAP: Direct VLM-to-VLA Adaptation via Language-Action Grounding](../Inbox/2026-07-09--clap-direct-vlm-to-vla-adaptation-via-language-action-grounding.md): 语言-动作令牌序列和一个训练周期后的 LIBERO 增益。

### 小型模型遇到灵巧操作上限
FabriVLA 表明，一个拥有 0.89B 参数的模型可以利用中间视觉-语言特征以及动作令牌之间的门控注意力，在 Meta-World MT50 上达到 92.0% 的回合成功率。DexVerse 展示了更高的难度上限。在 19 个灵巧操作任务中，最高平均成功率为 0.34，由 3D Diffusion Policy 和 pi0.5 共同达到。所有受测方法在 PushT 上的得分都是零，插入、刀具滑动和打开笔记本电脑的成功率也接近于零。因此，标准测试套件上的高分不足以证明策略具备力控制、精细对齐和多阶段手部操作能力。

#### Evidence
- [FabriVLA: A Lightweight Vision-Language-Action Model for Precise Multi-Task Manipulation](../Inbox/2026-07-09--fabrivla-a-lightweight-vision-language-action-model-for-precise-multi-task-manipulation.md): 模型规模、架构组件和 MT50 性能。
- [DexVerse: A Modular Benchmark for Multi-Task, Multi-Embodiment Dexterous Manipulation](../Inbox/2026-07-09--dexverse-a-modular-benchmark-for-multi-task-multi-embodiment-dexterous-manipulation.md): DexVerse 的范围、对比成功率和精密任务上的近零结果。
