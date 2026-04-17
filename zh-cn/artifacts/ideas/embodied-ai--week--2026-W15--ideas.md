---
kind: ideas
granularity: week
period_start: '2026-04-06T00:00:00'
period_end: '2026-04-13T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- embodied-ai
- robotics
- vla
- grounding
- world-models
- robustness
tags:
- recoleta/ideas
- topic/embodied-ai
- topic/robotics
- topic/vla
- topic/grounding
- topic/world-models
- topic/robustness
language_code: zh-CN
---

# 可检查的机器人控制闭环

## Summary
本周的 embodied AI 工作支持三项具体的流程改动：在精密放置中让目标定位在执行前可见，用能暴露脆弱泛化问题的留出式仿真任务为策略发布设闸，以及在把合成机器人轨迹用于训练前先做执行后的视觉检查和过滤。三者都把模型进展绑定到可检查的控制步骤或更严格的评估闭环上，而这正是当前采用压力增长最快的地方。

## 用于槽位级放置复核的视觉目标叠加
为放置任务建立一条带目标叠加的控制路径：机器人需要在多个槽位中选对一个，并且在严格的几何容差内完成落位。AnySlot 的结果说明，一个清晰的拆分方式有效：由一个模块把语言指令解析成可见的目标标记，再让动作策略在多个相机视角中跟随这个标记。这很适合装配、分拣套件和料箱插入这类工作，因为这类失败往往不是区域选错，而是最终位姿没有对准。一个有用的产品改动是，让界面保存并回放视觉目标本身，而不只是文本提示或单个 3D 点，这样操作员可以在执行前检查系统认为的目标是什么。一个低成本测试是做槽位放置评测，加入密集干扰项和不同措辞，用亚厘米级阈值评分，并对生成的标记加入人工复核。这里的基准细节足以支撑这套流程：槽位尺寸约 0.03 m，目标容差 0.02 m，在九类槽位推理任务上的零样本平均成功率接近 90%，而平面 Diffusion Policy 基线在大多数已展示类别上都失效。

### Evidence
- [AnySlot: Goal-Conditioned Vision-Language-Action Policies for Zero-Shot Slot-Level Placement](../Inbox/2026-04-12--anyslot-goal-conditioned-vision-language-action-policies-for-zero-shot-slot-level-placement.md): AnySlot 报告了明确的视觉目标标记、严格的放置容差，以及较高的零样本槽位放置性能。
- [AnySlot: Goal-Conditioned Vision-Language-Action Policies for Zero-Shot Slot-Level Placement](../Inbox/2026-04-12--anyslot-goal-conditioned-vision-language-action-policies-for-zero-shot-slot-level-placement.md): 论文摘要确认了这种面向槽位放置的中间视觉目标设计。

## 面向真实世界训练机器人策略的留出式仿真发布闸门
对于发布基于真实世界数据训练的 VLA 策略的团队，在现场部署前加入一个留出式仿真闸门。RoboLab 表明，当前策略在熟悉的基准上看起来可能还可以，但一旦场景、措辞和流程要求变化，就会在大多数域外任务上失败。这个流程改动很具体：每次策略更新都应跑过一组固定的、自动生成但经人工验证的任务，记录抓错物体、掉落、碰撞、路径质量和语言敏感性，并把发布标准绑定到这些失败模式，而不是单一成功率数字。这个做法最适合已经在收集真实示范并微调通用策略的机器人团队，因为他们需要一种更便宜的方法，在占用机器人实测时间之前先发现脆弱行为。这里的数字很直接：在 RoboLab-120 上，π0.5 的总体成功率是 23.3%，在复杂任务上降到 11.7%；在一个装箱设置中，目标物体数量从 1 增加到 3 时，成功率从 70% 降到 20%；在同一场景里，仅因指令措辞变化，结果就可能从 80% 变成 0%。

### Evidence
- [RoboLab: A High-Fidelity Simulation Benchmark for Analysis of Task Generalist Policies](../Inbox/2026-04-10--robolab-a-high-fidelity-simulation-benchmark-for-analysis-of-task-generalist-policies.md): RoboLab 提供了留出式仿真基准的设计，以及各类策略的主要失败结果。
- [RoboLab: A High-Fidelity Simulation Benchmark for Analysis of Task Generalist Policies](../Inbox/2026-04-10--robolab-a-high-fidelity-simulation-benchmark-for-analysis-of-task-generalist-policies.md): 论文正文说明了该基准的目标：在仿真中通过受控扰动分析真实世界策略。

## 用于长时程操作训练的已验证合成轨迹过滤
建立一条合成数据流水线，在轨迹进入 VLA 训练前剔除视觉上失败的样本。V-CAGE 给出了一个具体模式，适用于长时程操作数据：先生成面向任务的场景，用可复用的子任务模板执行，再在执行后做视觉检查；只要其中一步失败，就丢弃整条轨迹。对于想用仿真扩展少量真实数据的团队，这一支撑层很重要，因为合成 rollout 中的静默失败不会表现为运行时报错，却会污染训练。短期可做的构建是，把验证和过滤阶段接到现有仿真生成任务后面，再配合激进的视频压缩，让保留下来的数据更便于存储和重复训练。论文里的 Sim2Real 结果足以支持先做试点：在 ALOHA-AgileX 上，仅用 10 条真实示范，在 20 次试验中的成功率是 20%；再加入 250 条仿真轨迹后，成功率提高到 55%。同一系统还报告文件大小减少超过 90%，而压缩数据的下游训练效果基本相近。

### Evidence
- [V-CAGE: Vision-Closed-Loop Agentic Generation Engine for Robotic Manipulation](../Inbox/2026-04-10--v-cage-vision-closed-loop-agentic-generation-engine-for-robotic-manipulation.md): V-CAGE 描述了闭环合成数据流水线、轨迹剔除机制和训练结果。
- [V-CAGE: Vision-Closed-Loop Agentic Generation Engine for Robotic Manipulation](../Inbox/2026-04-10--v-cage-vision-closed-loop-agentic-generation-engine-for-robotic-manipulation.md): 正文说明了视觉自检步骤以及大幅视频压缩的结论。
