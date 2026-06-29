---
kind: trend
trend_doc_id: 106
granularity: week
period_start: '2026-04-06T00:00:00'
period_end: '2026-04-13T00:00:00'
topics:
- embodied-ai
- robotics
- vla
- grounding
- world-models
- robustness
run_id: materialize-outputs
aliases:
- recoleta-trend-106
tags:
- recoleta/trend
- topic/embodied-ai
- topic/robotics
- topic/vla
- topic/grounding
- topic/world-models
- topic/robustness
language_code: zh-CN
---

# Embodied AI 论文正在提高具备 grounding 且可检查控制系统的标准

## Overview
本周 embodied AI 工作最扎实的部分，是那些能在执行时被检查、复用并完成 grounding 的控制系统。VLA 论文继续改进动作闭环，但更清晰的模式已经落在操作层面：显式目标状态、经过验证的 grounding、可执行的合成数据，以及能在部署前暴露失败的鲁棒性测试。世界模型也仍然重要，尤其是在它们把机体布局、未来状态或物体结构编码成策略可直接使用的形式时。

## Clusters

### 控制栈正被构建为可复用的基础设施
可复用的控制基础设施仍是核心。整周反复出现的都是让 Vision-Language-Action (VLA) 系统更容易训练、调控和检查的组件。4 月 6 日的 Veo-Act、StarVLA 和 E-VLA 都体现了这一点：用视频模型生成高层计划、用标准化 VLA 代码库开发系统，以及用事件传感处理低照度或模糊场景下的操作。4 月 7 日又沿着这条线推进，重点放在更快的推理和更透明的动作生成上。

#### Evidence
- [StarVLA: A Lego-like Codebase for Vision-Language-Action Model Developing](../Inbox/2026-04-06--starvla-a-lego-like-codebase-for-vision-language-action-model-developing.md)
- [ProGAL-VLA: Grounded Alignment through Prospective Reasoning in Vision-Language-Action Models](../Inbox/2026-04-10--progal-vla-grounded-alignment-through-prospective-reasoning-in-vision-language-action-models.md)
- [Veo-Act: How Far Can Frontier Video Models Advance Generalizable Robot Manipulation?](../Inbox/2026-04-06--veo-act-how-far-can-frontier-video-models-advance-generalizable-robot-manipulation.md)
- [E-VLA: Event-Augmented Vision-Language-Action Model for Dark and Blurred Scenes](../Inbox/2026-04-06--e-vla-event-augmented-vision-language-action-model-for-dark-and-blurred-scenes.md)
- [V-CAGE: Vision-Closed-Loop Agentic Generation Engine for Robotic Manipulation](../Inbox/2026-04-10--v-cage-vision-closed-loop-agentic-generation-engine-for-robotic-manipulation.md)
- [Learning Vision-Language-Action World Models for Autonomous Driving](../Inbox/2026-04-10--learning-vision-language-action-world-models-for-autonomous-driving.md)

### Grounding 正在执行时接受检验
Grounding 已经变成一个具体的控制要求。多篇论文要求系统先确认自己正在对什么对象执行动作，让语言始终和执行过程对应起来，并在部署前暴露失败模式。4 月 10 日的 ProGAL-VLA 和 RoboLab 符合这一标准。到本周末，AnySlot 给出了最清晰的单一例子：它把语言指令转成一个可见的目标标记，再配合 SlotBench，并报告了接近 90% 的平均零样本 slot-level 放置成功率。

#### Evidence
- [ProGAL-VLA: Grounded Alignment through Prospective Reasoning in Vision-Language-Action Models](../Inbox/2026-04-10--progal-vla-grounded-alignment-through-prospective-reasoning-in-vision-language-action-models.md)
- [Grounding Hierarchical Vision-Language-Action Models Through Explicit Language-Action Alignment](../Inbox/2026-04-07--grounding-hierarchical-vision-language-action-models-through-explicit-language-action-alignment.md)
- [RoboPlayground: Democratizing Robotic Evaluation through Structured Physical Domains](../Inbox/2026-04-06--roboplayground-democratizing-robotic-evaluation-through-structured-physical-domains.md)
- [AnySlot: Goal-Conditioned Vision-Language-Action Policies for Zero-Shot Slot-Level Placement](../Inbox/2026-04-12--anyslot-goal-conditioned-vision-language-action-policies-for-zero-shot-slot-level-placement.md)
- [RoboLab: A High-Fidelity Simulation Benchmark for Analysis of Task Generalist Policies](../Inbox/2026-04-10--robolab-a-high-fidelity-simulation-benchmark-for-analysis-of-task-generalist-policies.md)
- [V-CAGE: Vision-Closed-Loop Agentic Generation Engine for Robotic Manipulation](../Inbox/2026-04-10--v-cage-vision-closed-loop-agentic-generation-engine-for-robotic-manipulation.md)

### 世界模型和策略正在加入显式任务结构
机器人论文开始把结构直接写进策略或世界模型里。4 月 8 日的重点是基于检索的决策循环和 grounded imagination，用来保持长时程控制的稳定性。4 月 9 日则把形态信息、未来状态和物体运动学直接纳入学习，覆盖四足机器人、人形机器人、导航、灵巧抓取和关节物体等任务。实际效果是更容易诊断失败原因，也能更好利用任务特定约束。

#### Evidence
- [Toward Hardware-Agnostic Quadrupedal World Models via Morphology Conditioning](../Inbox/2026-04-09--toward-hardware-agnostic-quadrupedal-world-models-via-morphology-conditioning.md)
- [Event-Centric World Modeling with Memory-Augmented Retrieval for Embodied Decision-Making](../Inbox/2026-04-08--event-centric-world-modeling-with-memory-augmented-retrieval-for-embodied-decision-making.md)
- [RoboPlayground: Democratizing Robotic Evaluation through Structured Physical Domains](../Inbox/2026-04-06--roboplayground-democratizing-robotic-evaluation-through-structured-physical-domains.md)
- [Action Images: End-to-End Policy Learning via Multiview Video Generation](../Inbox/2026-04-07--action-images-end-to-end-policy-learning-via-multiview-video-generation.md)
- [RoboLab: A High-Fidelity Simulation Benchmark for Analysis of Task Generalist Policies](../Inbox/2026-04-10--robolab-a-high-fidelity-simulation-benchmark-for-analysis-of-task-generalist-policies.md)
- [HEX: Humanoid-Aligned Experts for Cross-Embodiment Whole-Body Manipulation](../Inbox/2026-04-09--hex-humanoid-aligned-experts-for-cross-embodiment-whole-body-manipulation.md)

### 鲁棒性研究正进入核心评估
鲁棒性仍在主要评估环节里。本周包含了对语言条件动作系统更严苛的压力测试，也直接检验了受损输入下的性能。4 月 7 日强调了语言多么容易让机器人策略失效。4 月 11 日的 STRONG-VLA 延续了这一重点，把多模态扰动下的抗干扰能力当作可测量目标，而不是附带检查。和前一周相比，这批论文仍然围绕动作闭环质量展开，但这一周把这个目标和 grounding 检查、可执行数据结合得更紧。

#### Evidence
- [STRONG-VLA: Decoupled Robustness Learning for Vision-Language-Action Models under Multimodal Perturbations](../Inbox/2026-04-11--strong-vla-decoupled-robustness-learning-for-vision-language-action-models-under-multimodal-perturbations.md)
- [RoboPlayground: Democratizing Robotic Evaluation through Structured Physical Domains](../Inbox/2026-04-06--roboplayground-democratizing-robotic-evaluation-through-structured-physical-domains.md)
- [RoboLab: A High-Fidelity Simulation Benchmark for Analysis of Task Generalist Policies](../Inbox/2026-04-10--robolab-a-high-fidelity-simulation-benchmark-for-analysis-of-task-generalist-policies.md)
- [Uncovering Linguistic Fragility in Vision-Language-Action Models via Diversity-Aware Red Teaming](../Inbox/2026-04-07--uncovering-linguistic-fragility-in-vision-language-action-models-via-diversity-aware-red-teaming.md)
- [StarVLA: A Lego-like Codebase for Vision-Language-Action Model Developing](../Inbox/2026-04-06--starvla-a-lego-like-codebase-for-vision-language-action-model-developing.md)
- [You're Pushing My Buttons: Instrumented Learning of Gentle Button Presses](../Inbox/2026-04-07--you-re-pushing-my-buttons-instrumented-learning-of-gentle-button-presses.md)
