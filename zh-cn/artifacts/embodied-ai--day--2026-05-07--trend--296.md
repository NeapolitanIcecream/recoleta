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

# 机器人策略按对象身份、接触和仿真器保真度来评判

## Overview
这一时期的机器人研究集中在能承受场景变化的控制上。视觉-语言-动作（VLA）论文让对象身份、手部接触、动作条件世界模型和仿真器保真度变得可测量。OA-WAM、HumanNet 和 VISER 的证据最清楚，因为它们把机制与基准或验证结果配在一起。

## Clusters

### 基于对象的 VLA 控制
VLA 策略正在动作路径中加入显式的对象和关系结构。OA-WAM 将固定的对象地址与会变化的对象内容分开，使目标绑定可以通过槽位干预来测试。它在 LIBERO 上报告 97.8% 的平均成功率，交换绑定余弦为 0.87；整体式基线为 0.09 或更低。

TriRelVLA 通过对象、手和任务节点采用相近路线。它的图使用四种关系类型：任务-对象、任务-手、对象-手和对象-对象。现有摘录给出了机制细节，并声称在跨场景、跨对象和跨任务操作上有提升，但没有量化基准表。

#### Evidence
- [OA-WAM: Object-Addressable World Action Model for Robust Robot Manipulation](../Inbox/2026-05-07--oa-wam-object-addressable-world-action-model-for-robust-robot-manipulation.md): OA-WAM 的对象槽位设计，以及 LIBERO、SimplerEnv、LIBERO-Plus 和槽位干预结果。
- [TriRelVLA: Triadic Relational Structure for Generalizable Embodied Manipulation](../Inbox/2026-05-07--trirelvla-triadic-relational-structure-for-generalizable-embodied-manipulation.md): TriRelVLA 的关系图、任务 token、关系类型和文中给出的泛化设置。

### 面向控制信号构建的世界模型
世界模型研究正在按其潜在状态是否保留与动作相关的信息来评估。一项研究在 BridgeV2 上训练动作条件扩散世界模型，只改变潜在编码器。V-JEPA 2.1 和 SigLIP 2 等语义编码器在策略 rollout、动作恢复和成功分类上优于侧重重建的 VAE。V-JEPA 2.1_96 在 DiT-S rollout 中达到 0.362 的共识成功率，而 VAE 为 0.169。

EA-WM 处理动作条件侧的问题。它将机器人运动学转换为与相机对齐的视觉场，包括机械臂骨架、夹爪几何、末端执行器热力图和位姿轴。在 WorldArena 上，它报告 76.60 的 P3CScore，高于 CogVideoX 的 71.08；消融结果显示，移除运动学到视觉场或事件感知融合后分数下降。

#### Evidence
- [Reconstruction or Semantics? What Makes a Latent Space Useful for Robotic World Models](../Inbox/2026-05-07--reconstruction-or-semantics-what-makes-a-latent-space-useful-for-robotic-world-models.md): 机器人扩散世界模型中语义潜变量与重建潜变量的比较，包括 rollout 和动作恢复指标。
- [EA-WM: Event-Aware Generative World Model with Structured Kinematic-to-Visual Action Fields](../Inbox/2026-05-07--ea-wm-event-aware-generative-world-model-with-structured-kinematic-to-visual-action-fields.md): EA-WM 的动作场设计、WorldArena 分数和消融结果。

### 用于机器人执行的人类交互数据
人类数据以两种形式出现：大规模视频预训练，以及被细化为可执行灵巧动作的小型运动集。HumanNet 报告了 1,000,000 小时以人为中心的视频，包含第一人称和第三人称视角、字幕、运动描述以及手部/身体信号。在一项受控 VLA 验证中，在相同 LingBot-VLA 设置下，1,000 小时的第一人称 HumanNet 预训练据称达到或略高于 100 小时真实机器人 CoBot 预训练。

DexSynRefine 展示了小数据路径。它从每个任务七个人-物交互演示开始，将其扩展到每个任务约 300 条轨迹，并加入残差强化学习以及接触和动力学适配。在五个灵巧任务中，任务空间残差动作达到 68.1% 的平均模拟成功率，而原始运动学重定向接近失败。

#### Evidence
- [HumanNet: Scaling Human-centric Video Learning to One Million Hours](../Inbox/2026-05-07--humannet-scaling-human-centric-video-learning-to-one-million-hours.md): HumanNet 的规模、标注，以及与机器人数据预训练对比的受控 VLA 验证。
- [DexSynRefine: Synthesizing and Refining Human-Object Interaction Motion for Physically Feasible Dexterous Robot Actions](../Inbox/2026-05-07--dexsynrefine-synthesizing-and-refining-human-object-interaction-motion-for-physically-feasible-dexterous-robot-actions.md): DexSynRefine 的数据扩展、残差策略设计、接触/动力学适配和任务成功结果。

### 视觉扰动下的适配和评估
两篇论文关注机器人策略结论在分布变化下是否成立。VLA-GSE 使用参数高效微调：它训练 4,551.85M 参数中的 114.04M，即 2.51%，并使用共享和路由的低秩专家。它在 LIBERO-Plus 上报告 81.2% 的平均零样本成功率，在同骨干比较中高于全量微调和多个 PEFT 基线。

VISER 测试评估侧。它构建了覆盖 319 个类别的 1,049 个基于物理的渲染资产，并加入镜面材料、柔和阴影和重建的真实世界任务。该基准报告仿真与真实世界策略性能之间的平均 Pearson 相关系数为 0.92；视觉线索会大幅改变任务结果：没有镜面高光时，茄子放入锅中的成功率为 10%，加入后升至 90%。

#### Evidence
- [VLA-GSE: Boosting Parameter-Efficient Fine-Tuning in VLA with Generalized and Specialized Experts](../Inbox/2026-05-07--vla-gse-boosting-parameter-efficient-fine-tuning-in-vla-with-generalized-and-specialized-experts.md): VLA-GSE 的可训练参数数量、LIBERO-Plus 零样本结果和分布偏移分数。
- [Toward Visually Realistic Simulation: A Benchmark for Evaluating Robot Manipulation in Simulation](../Inbox/2026-05-07--toward-visually-realistic-simulation-a-benchmark-for-evaluating-robot-manipulation-in-simulation.md): VISER 的资产规模、视觉真实感设计、仿真到现实相关性，以及光照/材料消融。
