---
source: arxiv
url: http://arxiv.org/abs/2603.12193v1
published_at: '2026-03-12T17:23:46'
authors:
- Mengzhen Liu
- Enshen Zhou
- Cheng Chi
- Yi Han
- Shanyu Rong
- Liming Chen
- Pengwei Wang
- Zhongyuan Wang
- Shanghang Zhang
topics:
- robotics
- vision-language-action
- active-perception
- manipulation
- benchmark
- 3d-geometry
relevance_score: 0.26
run_id: materialize-outputs
---

# SaPaVe: Towards Active Perception and Manipulation in Vision-Language-Action Models for Robotics

## Summary
SaPaVe 是一个面向机器人主动感知与操作的端到端视觉-语言-动作框架，核心思想是把相机运动和操作动作解耦，并分两阶段学习。论文同时提出了一个 20 万规模的语义相机控制数据集和首个主动操作基准，用于提升在遮挡、视角不佳和目标出视野时的成功率。

## Problem
- 现有 VLA/机器人操作方法大多假设**固定且接近最优的相机视角**，在遮挡、目标出视野、视角变化时容易失败。
- 把相机控制和机械操作直接放进**统一动作空间**，会破坏已有操作先验，还需要昂贵的同步相机+操作标注数据。
- 缺少专门评测“主动操作”的**大规模数据集与标准 benchmark**，导致方法难以系统训练和可复现比较。

## Approach
- 提出 **SaPaVe**：将头部相机动作与其他操作动作**解耦**，分别由不同动作头预测，减少相互干扰。
- 采用**两阶段自底向上训练**：先用 **ActiveViewPose-200K** 学“语义驱动的相机移动”，再用混合数据联合微调主动操作。
- 引入 **Camera Adapter**（基于 LoRA）保存语义相机控制能力，在第二阶段冻结该模块，避免破坏已学到的主动感知先验。
- 设计 **Universal Spatial Knowledge Injection**，把深度、相机内外参等 3D 几何信息编码后注入动作解码过程，提高动态视角下的空间鲁棒性。
- 提出 **ActiveManip-Bench**：首个专门评测主动操作的仿真基准，覆盖 12 个任务、100 个物体、20 个场景。

## Results
- 在 **ActiveViewPose-200K** 的语义主动感知评测上，SaPaVe（Stage 1）成功率为 **84.3% avg**，高于 **Gemini-2.5-Pro 72.7%**、**Multi-SpatialMLLM 70.2%**、**Qwen2.5-VL-72B 62.3%**；相对 Gemini 平均提升 **11.6 个百分点**。分项上：Val **85.5**，Test1 **89.1**，Test2 **78.3**。
- 在 **ActiveManip-Bench** 仿真中，SaPaVe（Active Camera）平均成功率 **74.83%**，优于 **Fixed Camera 36.17%**、**Fixed Camera + Wrist Camera 52.33%**、**Active Camera + Wrist Camera 73.16%**。
- 仿真分任务中，SaPaVe 在 **Out-of-View Pick-and-Place** 达到 **72%**，而 **Fixed Camera** 仅 **11%**；在 **Out-of-View Articulated Manipulation** 达到 **68%**，而 **Fixed Camera** 仅 **7%**，说明主动视角对“看不见目标”的场景尤其关键。
- 图 1 与正文声称其在 ActiveManip-Bench 上平均成功率约 **75.2%**，并且相较近期 VLA 基线可获得**最高 58 个百分点绝对提升**（文中举例对比固定视角 GR00T-N1）。
- 在**真实机器人**主动操作中，SaPaVe 平均成功率 **85.0%**，高于 **GR00T-N1 53.75%** 和 **π0 45.0%**；相对 GR00T-N1 提升 **31.25 个百分点**，相对 π0 提升 **40 个百分点**。
- 真实世界分项结果：Occluded Pick-and-Place **90%**、Out-of-View Pick-and-Place **85%**、Occluded Articulated Manipulation **85%**、Out-of-View Articulated Manipulation **80%**；对应 GR00T-N1 分别为 **60/55/50/50**，π0 为 **55/45/45/35**。

## Link
- [http://arxiv.org/abs/2603.12193v1](http://arxiv.org/abs/2603.12193v1)
