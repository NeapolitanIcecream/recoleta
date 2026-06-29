---
kind: trend
trend_doc_id: 296
granularity: day
period_start: '2026-05-07T00:00:00'
period_end: '2026-05-08T00:00:00'
topics:
- robot manipulation
- vision-language-action
- world models
- human video data
- simulation evaluation
- dexterous manipulation
run_id: materialize-outputs
aliases:
- recoleta-trend-296
tags:
- recoleta/trend
- topic/robot-manipulation
- topic/vision-language-action
- topic/world-models
- topic/human-video-data
- topic/simulation-evaluation
- topic/dexterous-manipulation
language_code: zh-CN
---

# 机器人策略按物体身份、接触和模拟器保真度来评判

## Overview
这一时期的机器人研究集中在能否在场景变化下继续工作的控制。视觉-语言-动作（VLA）论文把物体身份、手部接触、动作条件世界模型和模拟器保真度都变成了可测量对象。OA-WAM、HumanNet 和 VISER 提供了最清楚的证据，因为它们把机制和基准或验证结果放在一起。

## Clusters

### Object-grounded VLA control
VLA 策略正在在动作路径中加入明确的物体和关系结构。OA-WAM 将固定的物体地址与变化的物体内容分开，这让目标绑定可以通过槽位干预来检验。它在 LIBERO 上报告 97.8% 的平均成功率，swap-binding 余弦为 0.87，而整体式基线保持在 0.09 或更低。

TriRelVLA 走了类似的路线，通过物体、手和任务节点来建模。它的图使用四种关系类型：task-object、task-hand、object-hand 和 object-object。可见摘录给出了机制细节，以及在跨场景、跨物体和跨任务操作上的宣称提升，但没有量化基准表。

#### Evidence
- [OA-WAM: Object-Addressable World Action Model for Robust Robot Manipulation](../Inbox/2026-05-07--oa-wam-object-addressable-world-action-model-for-robust-robot-manipulation.md): OA-WAM object-slot design and LIBERO, SimplerEnv, LIBERO-Plus, and slot-intervention results.
- [TriRelVLA: Triadic Relational Structure for Generalizable Embodied Manipulation](../Inbox/2026-05-07--trirelvla-triadic-relational-structure-for-generalizable-embodied-manipulation.md): TriRelVLA relation graph, task tokens, relation types, and stated generalization settings.

### World models built for control signals
世界模型工作的评价重点，放在潜在状态是否保留了与动作相关的信息。一个研究在 BridgeV2 上训练条件于动作的扩散世界模型，只改变潜在编码器。V-JEPA 2.1 和 SigLIP 2 这类语义编码器在策略 rollout、动作恢复和成功分类上都优于以重建为主的 VAE。V-JEPA 2.1_96 在 DiT-S rollout 中达到 0.362 的一致成功率，VAE 为 0.169。

EA-WM 处理的是动作条件这一侧。它把机器人运动学转换成对齐相机视角的视觉场，包括机械臂骨架、夹爪几何、末端执行器热图和姿态轴。在 WorldArena 上，它报告 76.60 的 P3CScore，高于 CogVideoX 的 71.08；消融显示，去掉运动学到视觉场或事件感知融合都会带来损失。

#### Evidence
- [Reconstruction or Semantics? What Makes a Latent Space Useful for Robotic World Models](../Inbox/2026-05-07--reconstruction-or-semantics-what-makes-a-latent-space-useful-for-robotic-world-models.md): Comparison of semantic and reconstruction latents for robot diffusion world models, with rollout and action-recovery metrics.
- [EA-WM: Event-Aware Generative World Model with Structured Kinematic-to-Visual Action Fields](../Inbox/2026-05-07--ea-wm-event-aware-generative-world-model-with-structured-kinematic-to-visual-action-fields.md): EA-WM action-field design, WorldArena scores, and ablation results.

### Human interaction data for robot execution
人类数据主要有两种形式：大规模视频预训练，以及小规模动作集再加工成可执行的灵巧操作。HumanNet 报告了 1,000,000 小时的人类中心视频，包含第一视角和第三视角、字幕、动作描述，以及手和身体信号。在一个受控的 VLA 验证中，同样的 LingBot-VLA 设置下，1,000 小时的第一视角 HumanNet 预训练据称与 100 小时真实机器人 CoBot 预训练相当，或者略好。

DexSynRefine 走的是小数据路线。它从每个任务 7 个的人类-物体交互演示开始，把它们扩展到每个任务约 300 条轨迹，再加入残差强化学习以及接触和动力学适配。跨五个灵巧任务，任务空间残差动作的平均仿真成功率达到 68.1%，而原始运动学重定位几乎一直失败。

#### Evidence
- [HumanNet: Scaling Human-centric Video Learning to One Million Hours](../Inbox/2026-05-07--humannet-scaling-human-centric-video-learning-to-one-million-hours.md): HumanNet scale, annotations, and controlled VLA validation against robot-data pretraining.
- [DexSynRefine: Synthesizing and Refining Human-Object Interaction Motion for Physically Feasible Dexterous Robot Actions](../Inbox/2026-05-07--dexsynrefine-synthesizing-and-refining-human-object-interaction-motion-for-physically-feasible-dexterous-robot-actions.md): DexSynRefine data expansion, residual policy design, contact/dynamics adaptation, and task success results.

### Adaptation and evaluation under visual perturbations
两篇论文都在看机器人策略的说法能否在分布变化下成立。VLA-GSE 使用参数高效微调：它训练了 4,551.85M 个参数中的 114.04M，也就是 2.51%，并使用共享和路由的低秩专家。它在 LIBERO-Plus 上报告 81.2% 的平均零样本成功率，在同一骨干的比较中，超过了全量微调和几种 PEFT 基线。

VISER 在评估端做测试。它构建了 1,049 个基于物理渲染的资产，覆盖 319 个类别，并加入镜面材质、软阴影和重建的真实世界任务。该基准报告仿真与真实世界策略表现之间的平均 Pearson 相关系数为 0.92；视觉线索会明显改变任务结果：茄子入锅的成功率从没有镜面高光时的 10% 上升到有高光时的 90%。

#### Evidence
- [VLA-GSE: Boosting Parameter-Efficient Fine-Tuning in VLA with Generalized and Specialized Experts](../Inbox/2026-05-07--vla-gse-boosting-parameter-efficient-fine-tuning-in-vla-with-generalized-and-specialized-experts.md): VLA-GSE trainable-parameter count, LIBERO-Plus zero-shot results, and distribution-shift scores.
- [Toward Visually Realistic Simulation: A Benchmark for Evaluating Robot Manipulation in Simulation](../Inbox/2026-05-07--toward-visually-realistic-simulation-a-benchmark-for-evaluating-robot-manipulation-in-simulation.md): VISER asset scale, visual realism design, sim-to-real correlation, and lighting/material ablations.
