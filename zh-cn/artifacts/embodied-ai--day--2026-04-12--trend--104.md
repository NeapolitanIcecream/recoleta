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

# 显式目标标记支撑零样本机器人放置

## 概览
这一时期最清楚的结果是：机器人放置被写成了一个带显式目标状态的精确对齐问题。AnySlot 先把自然语言指令变成可见的目标标记，再让带目标条件的 Vision-Language-Action 策略负责执行。论文把这个设计和 SlotBench 结合起来，这是一个严格的槽位放置基准，并在零样本设置下报告了接近 90% 的平均成功率。

## 研究发现

### 用于精确放置的显式视觉目标
AnySlot 将语言对齐当作控制前的一个单独视觉目标。系统会在目标槽位上用彩色标记编辑场景，把这个点抬到三维空间，再投影到各个相机视角。随后，动作策略沿着这个明确目标执行。这个设计适合这类任务：槽位放置既要做语义选择，也要做严格的几何对齐；论文认为，把两者塞进一个扁平策略里，会让稠密布局更难处理。

#### 资料来源
- [AnySlot: Goal-Conditioned Vision-Language-Action Policies for Zero-Shot Slot-Level Placement](../Inbox/2026-04-12--anyslot-goal-conditioned-vision-language-action-policies-for-zero-shot-slot-level-placement.md): Summary describes the two-stage pipeline and why flat policies struggle on slot-level placement.

### 更难的评估更适合槽位感知控制
基准测试的压力也很明确。SlotBench 要求在很小的容差下选择槽位，槽位大小约 3 厘米，正确性按与真实槽位中心 2 厘米以内来判定。它覆盖九类推理任务，包括序数、否定、可供性和世界知识。论文在这个设置上报告了接近 90% 的平均成功率，而可见的扁平 Diffusion Policy 基线在序数推理上只有 16%，在其他展示类别上为 0%。可用摘录没有给出完整对比表，所以最稳妥的结论是，这个任务在已展示结果中把显式目标控制和扁平基线明显区分开了。

#### 资料来源
- [AnySlot: Goal-Conditioned Vision-Language-Action Policies for Zero-Shot Slot-Level Placement](../Inbox/2026-04-12--anyslot-goal-conditioned-vision-language-action-policies-for-zero-shot-slot-level-placement.md): Summary gives SlotBench categories, geometry, tolerance, and reported average success.
