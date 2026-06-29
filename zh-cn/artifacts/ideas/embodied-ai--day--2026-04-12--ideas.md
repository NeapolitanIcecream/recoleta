---
kind: ideas
granularity: day
period_start: '2026-04-12T00:00:00'
period_end: '2026-04-13T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- vision-language-action
- goal-conditioning
- slot-placement
- benchmarks
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action
- topic/goal-conditioning
- topic/slot-placement
- topic/benchmarks
language_code: zh-CN
---

# 槽位放置精度

## Summary
这里最清楚的变化是操作层面的：槽位级放置已经有了具体做法，也有了更严格的测试方式。论文支持三个近期动作：在密集放置任务前加一个显式目标叠加阶段；用更窄的容差和会迫使模型真正选槽位的指令类别来评估；当槽位几何本身很重要时，不要把单点目标当成足够的表示。

## 适用于密集槽位放置的目标叠加前端
做料箱、托盘和工装夹具摆放的机器人团队，可以在现有 VLA 策略前面加一层小的目标叠加层。这里的证据很具体：AnySlot 会把语言指令转换成目标槽位上的可见场景标记，结合深度和标定把这个标记提升到 3D，再投影到各个相机视图，最后把叠加后的视图送入目标条件策略。这个分工对应一个常见失败模式：在密集布局里，模型会选错隔间，即使底层动作已经足以完成搬运。

一个实用的第一版不需要新的基础模型。可以先用一个视觉语言模块返回一个目标槽位，把彩色标记渲染到每个相机视图里，再把低层提示词固定成简单的放置指令。最便宜的检查方法，是在未见过的托盘布局上做对照测试，槽位间距要紧：比较同一个动作策略在有无显式叠加层时的表现，并把选错槽位的错误和运动失败分开统计。这对精密装配和工厂自动化最相关，因为放置目标是语义指定的，几何容差又很小。

### Evidence
- [AnySlot: Goal-Conditioned Vision-Language-Action Policies for Zero-Shot Slot-Level Placement](../Inbox/2026-04-12--anyslot-goal-conditioned-vision-language-action-policies-for-zero-shot-slot-level-placement.md): Summary describes the explicit visual goal marker, 3D lifting, multi-view reprojection, and relevance to precision assembly and factory automation.
- [AnySlot: Goal-Conditioned Vision-Language-Action Policies for Zero-Shot Slot-Level Placement](../Inbox/2026-04-12--anyslot-goal-conditioned-vision-language-action-policies-for-zero-shot-slot-level-placement.md): Paper text states that the explicit goal representation is consumed by a low-level policy and that the interface is tight and interpretable.

## 带明确容差和推理类别的槽位放置评测
语言条件下的机器人放置评测，需要一个能区分“选槽位”和“粗略抓放成功”的基准。SlotBench 在这里很有用，因为它把几何范围设得很窄：槽位大约 3 厘米，成功标准是落在真实槽位中心 2 厘米以内，还包含九类推理任务，覆盖序数词、否定、可供性和常识。可见结果里，一个平面的 Diffusion Policy 基线在序数推理上只有 16%，在其他展示类别上是 0%；而论文报告 AnySlot 在整个基准上的平均成功率接近 90%。

这会直接改变已经在更容易任务上报出较广泛操作成功的团队的工作方式。可以加一个槽位放置套件，设定明确的容差阈值和会迫使模型在邻近目标之间做区分的指令类别。一个小型内部版本可以用有重复隔间的托盘或面板夹具来做，再配上相对位置、排除条件和可供性约束这类提示词。它的主要价值是诊断：能看出失败来自语言定位、视觉定位，还是最终对齐。

### Evidence
- [AnySlot: Goal-Conditioned Vision-Language-Action Policies for Zero-Shot Slot-Level Placement](../Inbox/2026-04-12--anyslot-goal-conditioned-vision-language-action-policies-for-zero-shot-slot-level-placement.md): Summary gives the benchmark geometry, tolerance, task categories, and reported average success plus the visible flat baseline result.
- [AnySlot: Goal-Conditioned Vision-Language-Action Policies for Zero-Shot Slot-Level Placement](../Inbox/2026-04-12--anyslot-goal-conditioned-vision-language-action-policies-for-zero-shot-slot-level-placement.md): Paper text introduces SlotBench as a zero-shot benchmark covering nine structured reasoning tasks and notes that existing flat and modular pipelines struggle on most categories.

## 保留槽位几何信息的放置控制目标表示
用关键点或单一坐标来表示放置目标的团队，应该检查这些目标格式是不是布局变化下漏放的主要来源。论文给出了做这个检查的明确理由：槽位级放置对很小的定位误差就很敏感，而把目标压缩成关键点或连续坐标的旧方法，在分布偏移下会变得脆弱。在这种情况下，一个很小的像素误差就会变成有意义的 3D 偏移。

一个有用的实现，是在目标表示里保留槽位形状和边界信息的辅助层。最简单的版本，是把选中的槽位渲染成一个目标区域或标记，并用标定后的几何关系把它传播到各个视角。然后在未见过的槽位形状、相机位姿和杂乱程度上，把它和只用坐标的目标做对比。指标要把目标选择准确率和最终放置误差分开，因为这两类错误的原因不同。

### Evidence
- [AnySlot: Goal-Conditioned Vision-Language-Action Policies for Zero-Shot Slot-Level Placement](../Inbox/2026-04-12--anyslot-goal-conditioned-vision-language-action-policies-for-zero-shot-slot-level-placement.md): Summary says prior modular systems often reduce the target to a single coordinate and lose slot shape and boundary information needed for precise execution.
- [AnySlot: Goal-Conditioned Vision-Language-Action Policies for Zero-Shot Slot-Level Placement](../Inbox/2026-04-12--anyslot-goal-conditioned-vision-language-action-policies-for-zero-shot-slot-level-placement.md): Paper text states that keypoints or continuous coordinates can be brittle for high-precision localization, and that minor pixel deviations can lead to significant 3D misalignments.
