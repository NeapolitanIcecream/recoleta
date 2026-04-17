---
kind: trend
trend_doc_id: 104
granularity: day
period_start: '2026-04-12T00:00:00'
period_end: '2026-04-13T00:00:00'
topics:
- robotics
- vision-language-action
- goal-conditioning
- slot-placement
- benchmarks
run_id: materialize-outputs
aliases:
- recoleta-trend-104
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/goal-conditioning
- topic/slot-placement
- topic/benchmarks
language_code: zh-CN
---

# 显式目标标记为 zero-shot 机器人放置提供锚点

## Overview
这一时期最明确的结果是：机器人放置任务正被表述为一个带有显式目标状态的精确 grounding 问题。AnySlot 把自然语言指令转成可见的目标标记，再由目标条件化的 Vision-Language-Action 策略执行操作。论文还配套提出了严格的槽位放置基准 SlotBench，并报告在 zero-shot 设置下平均成功率接近 90%。

## Clusters

### 用于精确放置的显式视觉目标
AnySlot 在控制之前，先把语言 grounding 处理成一个独立的视觉目标。系统会在目标槽位上加入一个彩色标记，把该点提升到 3D，再投影到各个相机视角中。随后，动作策略跟随这个显式目标执行。这个设计符合任务需求：槽位放置既需要语义选择，也需要严格的几何对齐。论文认为，把两者都塞进单一的扁平策略，会让密集布局更难处理。

#### Evidence
- [AnySlot: Goal-Conditioned Vision-Language-Action Policies for Zero-Shot Slot-Level Placement](../Inbox/2026-04-12--anyslot-goal-conditioned-vision-language-action-policies-for-zero-shot-slot-level-placement.md): 摘要描述了两阶段流水线，以及为什么扁平策略在槽位级放置上表现吃力。

### 更难的评测更有利于槽位感知控制
基准测试的压力也很清楚。SlotBench 要求在严格容差下选择槽位，槽位尺寸约为 3 cm，只有落在真实槽位中心 2 cm 范围内才算正确。它覆盖九类推理任务，包括序数、否定、可供性和世界知识。在这套设置下，论文报告平均成功率接近 90%；而一个可见的扁平 Diffusion Policy 基线在序数推理上达到 16%，在其余展示的类别上为 0%。现有摘录没有给出完整的对比表，因此目前最稳妥的结论是：在已展示的结果中，这个任务能明显区分显式目标控制与扁平基线。

#### Evidence
- [AnySlot: Goal-Conditioned Vision-Language-Action Policies for Zero-Shot Slot-Level Placement](../Inbox/2026-04-12--anyslot-goal-conditioned-vision-language-action-policies-for-zero-shot-slot-level-placement.md): 摘要给出了 SlotBench 的类别、几何设置、容差和报告的平均成功率。
