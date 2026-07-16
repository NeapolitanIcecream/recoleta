---
kind: trend
trend_doc_id: 536
granularity: day
period_start: '2026-06-04T00:00:00'
period_end: '2026-06-05T00:00:00'
topics:
- robotics
- vision-language-action
- world models
- test-time compute
- affordance grounding
- policy evaluation
run_id: materialize-outputs
aliases:
- recoleta-trend-536
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/world-models
- topic/test-time-compute
- topic/affordance-grounding
- topic/policy-evaluation
language_code: zh-CN
---

# 机器人策略正在按预测未来和执行延迟打分

## 概览
这一天的内容主要是机器人论文，它们把 Vision-Language-Action（VLA）策略质量当作一个闭环控制问题。WLA、MPCoT 和 PiL-World 给出了最清楚的证据：未来状态预测、潜变量动作选择和想象 rollout 都直接和成功率与延迟相关。

## 研究发现

### 机器人策略中的世界模型
一些论文把未来状态预测用作训练信号，或把它纳入动作选择。WLA 在一个策略里同时预测文本子任务、紧凑的物理过渡和一个动作块。它的世界建模损失有可测影响：去掉后，RoboTwin Clean 成功率从 92.94% 降到 90.98%，LIBERO 平均成功率从 98.6% 降到 97.9%。

同样的思路也出现在桌面操作之外。WorldFly 把未来视频潜变量和导航动作结合起来，用于低空无人机控制。在 Urban Canyon Traversal 基准上，它在见过的路口达到 87% 成功率，在更难的未见路口达到 31%，在报告指标上超过 OpenFly 和 Pi-0-UAV。DexFuture 用预测的未来手-工具-物体目标做双手工具使用，运行速度为 60 Hz，避免了对高维手部动作进行缓慢的在线规划。

#### 资料来源
- [World-Language-Action Model for Unified World Modeling, Language Reasoning, and Action Synthesis](../Inbox/2026-06-04--world-language-action-model-for-unified-world-modeling-language-reasoning-and-action-synthesis.md): WLA architecture, world-model ablation, LIBERO and RoboTwin results.
- [WorldFly: A World-Model-Based Vision-Language-Action Model for UAV Navigation](../Inbox/2026-06-04--worldfly-a-world-model-based-vision-language-action-model-for-uav-navigation.md): WorldFly future-view/action coupling and Urban Canyon Traversal results.
- [DexFuture: Hierarchical Future-State Visuomotor Targeting for Bimanual Dexterous Tool Use](../Inbox/2026-06-04--dexfuture-hierarchical-future-state-visuomotor-targeting-for-bimanual-dexterous-tool-use.md): DexFuture future-state targeting, success rates, and 60 Hz execution.

### 推理时控制预算
最强的控制论文把计算开销也写进结果里。MPCoT 保留了 OpenVLA-OFT 的 8 步动作接口，并加入潜变量多路径细化。它的最佳设置把 LIBERO Long 成功率从 95.3% 提高到 98.9%，同时测得延迟从 24 ms 增加到 38 ms，而且没有生成推理 token。

另一条线在降低解码成本。one-step VLA 论文表明，带高噪声偏置的 flow-matching 训练日程可以让单步动作生成接近 10 步解码的表现。在 LIBERO-Plus 上，18 种可比配置里，单步解码都不低于 10 步解码，平均高出 5.4 个成功点。TempoVLA 通过把一个 VLA 策略条件在指令速度上，直接在策略层面处理执行速度，在三种速度条件化方法之间，LIBERO 成功率相近。

#### 资料来源
- [MPCoT: Reward-Guided Multi-Path Latent Reasoning for Test-Time Scalable Vision-Language-Action](../Inbox/2026-06-04--mpcot-reward-guided-multi-path-latent-reasoning-for-test-time-scalable-vision-language-action.md): MPCoT latent refinement, LIBERO/CALVIN gains, and latency numbers.
- [Let It Be Simple: One-Step Action Generation for Vision-Language-Action Models](../Inbox/2026-06-04--let-it-be-simple-one-step-action-generation-for-vision-language-action-models.md): One-step action generation method and LIBERO-family results.
- [TempoVLA: Learning Speed-Controllable Vision-Language-Action Policies](../Inbox/2026-06-04--tempovla-learning-speed-controllable-vision-language-action-policies.md): TempoVLA speed conditioning and reported LIBERO speed-control results.

### 把空间可供性作为动作输入
AffordanceVLA 把接触线索显式化。它在生成动作前预测目标物体、二维交互区域和三维形状/布局线索。可用摘录没有给出 LIBERO 或 CALVIN 的数值表，但它描述了一个自动化流程，生成了超过 100,000 条 affordance 标注。

DexFuture 给出了同一问题在灵巧工具使用中的更保守版本。它预测手部连杆、工具和物体的稀疏未来目标，然后让低层策略跟踪这些目标。在 OakInk2 双手任务上，它报告平均成功率为 59.69%，接近特权目标基线的 66.52%；摘要中报告无目标策略的平均成功率接近 7%。

#### 资料来源
- [AffordanceVLA: A Vision-Language-Action Model Empowering Action Generation through Affordance-Aware Understanding](../Inbox/2026-06-04--affordancevla-a-vision-language-action-model-empowering-action-generation-through-affordance-aware-understanding.md): AffordanceVLA object, contact-region, 3D shape cues, and annotation pipeline.
- [DexFuture: Hierarchical Future-State Visuomotor Targeting for Bimanual Dexterous Tool Use](../Inbox/2026-06-04--dexfuture-hierarchical-future-state-visuomotor-targeting-for-bimanual-dexterous-tool-use.md): DexFuture target representation and OakInk2 success comparisons.

### 闭环评测和恢复数据
评测工作正在用世界模型减少对完整机器人 rollout 的依赖。PiL-World 在冻结的 VLA 策略和世界模型之间交替，把生成的终点观测反馈回策略。在三个真实双臂任务上，它把真实与想象成功率的平均差距从 Ctrl-World 的 63.2% 降到 12.0%，并在不同任务和 checkpoint 组合上报告了 0.94 的 Pearson 相关系数。

物流数据飞轮论文把动作条件世界模型用于恢复数据。WM-DAgger 生成并筛选合成恢复轨迹，然后用真实示范训练模仿策略。在 Soft Bag Pushing 中，5 条真实示范加 1,500 条生成轨迹达到 93.3% 成功率，而行为克隆只有 26.7%。

#### 资料来源
- [PiL-World: A Chunk-Wise World Model for VLA Policy-in-the-Loop Evaluation](../Inbox/2026-06-04--pil-world-a-chunk-wise-world-model-for-vla-policy-in-the-loop-evaluation.md): PiL-World closed-loop imagined evaluation and real-imagined gap results.
- [Towards a Data Flywheel for Embodied Intelligence in Logistics](../Inbox/2026-06-04--towards-a-data-flywheel-for-embodied-intelligence-in-logistics.md): WM-DAgger synthetic recovery data and logistics manipulation success rates.
