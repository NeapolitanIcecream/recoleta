---
kind: trend
trend_doc_id: 622
granularity: week
period_start: '2026-06-08T00:00:00'
period_end: '2026-06-15T00:00:00'
topics:
- robotics
- vision-language-action models
- manipulation
- real-robot evaluation
- temporal modeling
- contact control
- spatial grounding
run_id: materialize-outputs
aliases:
- recoleta-trend-622
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action-models
- topic/manipulation
- topic/real-robot-evaluation
- topic/temporal-modeling
- topic/contact-control
- topic/spatial-grounding
language_code: zh-CN
---

# 机器人 VLA 工作正在接受时间、接触和缺失证据的检验

## Overview
本周的机器人视觉-语言-动作（VLA）工作按执行细节来检验：记忆、恢复、遮挡、接触时序和任务特定标签。MemoryVLA++、UMI-Bench 1.0 和 DAM-VLA 提供了最强证据。

## Clusters

### 时间状态与恢复
几篇论文把机器人策略失败视为时序问题。MemoryVLA++ 加入长期记忆和隐空间未来预测，让策略记住早先交互并预判物体运动。论文报告，在通用、依赖记忆、依赖想象的任务组中，真实机器人增益分别为 9、26 和 28 个百分点。

B2FF 处理的情况更窄：冻结的 VLA 策略在受扰动后偏离名义轨迹。它先生成未来视觉里程碑，再在执行时选择恢复目标。在注入失败的 LIBERO 上，平均成功率从 56.3% 升至 74.0%。共同结论很实用：当前相机视图不完整时，策略需要访问过去状态和可信的近期未来状态。

#### Evidence
- [MemoryVLA++: Temporal Modeling via Memory and Imagination in Vision-Language-Action Models](../Inbox/2026-06-08--memoryvla-temporal-modeling-via-memory-and-imagination-in-vision-language-action-models.md): MemoryVLA++ 摘要提供了方法细节，以及报告的仿真和真实机器人增益。
- [Back to the Familiar Future: Failure Recovery for VLA Policies via Pre-Imagined Milestone Selection](../Inbox/2026-06-08--back-to-the-familiar-future-failure-recovery-for-vla-policies-via-pre-imagined-milestone-selection.md): B2FF 摘要提供了失败恢复设置和 LIBERO 成功率增益。

### 遮挡与物理基准
评测工作集中在标准操作基准可能掩盖真实难度的情况。LIBERO-Occ 向 LIBERO 加入场景导致的遮挡物，并显示当物体或目标区域被遮住时，现有 VLA 策略的表现会大幅下降。它的 Viewpoint Imagination 方法在没有真实互补视角的情况下达到 65.05% 平均成功率，高于列出的最强基线 57.10%。

UMI-Bench 1.0 处理另一个会导致弱结论的来源：真实机器人执行差异。它为 10 个桌面任务固定了腕部视角观测设置、重置流程、动作接口、日志记录和评分。报告结果显示，布局、位姿和动力学变化造成的损害大于外观和物体变化；在两个长时程任务上，三个被评测模型的完整成功率都为 0%。

#### Evidence
- [LIBERO-Occ: Evaluating and Improving Vision-Language-Action Models under Scene-Induced Occlusion via Viewpoint Imagination](../Inbox/2026-06-09--libero-occ-evaluating-and-improving-vision-language-action-models-under-scene-induced-occlusion-via-viewpoint-imagination.md): LIBERO-Occ 摘要给出了基准设计、遮挡类型和 VIM 结果。
- [UMI-Bench 1.0: An Open and Reproducible Real-World Benchmark for Tabletop Robotic Manipulation with UMI Data](../Inbox/2026-06-09--umi-bench-1-0-an-open-and-reproducible-real-world-benchmark-for-tabletop-robotic-manipulation-with-umi-data.md): UMI-Bench 摘要给出了真实机器人协议、任务覆盖范围和报告的模型结果。

### 接触与传感器时序
接触密集型操作论文对许多 VLA 策略采用的单一时钟设计提出压力。DAM-VLA 为语言、视觉、力和本体感知分别保留隐变量缓冲区，然后让动作头在每个控制步读取这些缓冲区。这个设计把较慢的语言和视觉更新与更快的力和状态信号配合起来。

本周报告的数字中，这组结果很具体。在七个真实 Franka 任务上，DAM-VLA 达到 95.2% 平均成功率；最强同步基线为 40.95%。朴素的 100 Hz 同步设置降至 21.9%，支持了论文的主张：在接触密集型任务中，更新时间与传感器选择同样关键。

#### Evidence
- [DAM-VLA: Decoupled Asynchronous Multimodal Vision Language Action model](../Inbox/2026-06-10--dam-vla-decoupled-asynchronous-multimodal-vision-language-action-model.md): DAM-VLA 摘要给出了异步模态设计和真实机器人成功率。

### 面向具体任务的数据 grounding
本周还增加了让机器人数据匹配任务的基础设施。SPARC 用物体框、轨迹和操作阶段自动标注机器人演示，再用交互证据评估标注可靠性。在 IA-Bench 上，它达到 80.2% 的被交互物体定位准确率；基于检测器置信度的基线为 58.1%。

LabVLA 和 GIVE 展示了两种专门化的 grounding。LabVLA 构建合成实验室场景和工作流，让 VLA 策略能跨机器人形态执行书面实验台协议。GIVE 为交接任务加入手势线索；在真实世界试验中，它报告 80.0% 交接成功率，而基线为 0.0%。这些论文对数据提出同一项要求：标签、指令和观测必须携带机器人在执行时真正需要的线索。

#### Evidence
- [SPARC: Reliable Spatial Annotations from Robot Demonstrations at Scale](../Inbox/2026-06-11--sparc-reliable-spatial-annotations-from-robot-demonstrations-at-scale.md): SPARC 摘要给出了标注方法、IA-Bench 规模和定位结果。
- [LabVLA: Grounding Vision-Language-Action Models in Scientific Laboratories](../Inbox/2026-06-11--labvla-grounding-vision-language-action-models-in-scientific-laboratories.md): LabVLA 摘要给出了面向实验室的数据引擎、支持的机器人和基准主张。
- [GIVE: Grounding Human Gestures in Vision-Language-Action Models](../Inbox/2026-06-11--give-grounding-human-gestures-in-vision-language-action-models.md): GIVE 摘要给出了手势 grounding 方法和真实世界交接结果。
