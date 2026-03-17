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
- vision-language-action
- active-perception
- robot-manipulation
- sim2real
- benchmark
relevance_score: 0.94
run_id: materialize-outputs
---

# SaPaVe: Towards Active Perception and Manipulation in Vision-Language-Action Models for Robotics

## Summary
SaPaVe 是一个面向机器人主动感知与操作的端到端视觉-语言-动作框架，核心是将相机控制与操作控制解耦，并用两阶段训练把“先看清楚”与“再动手”结合起来。论文还同时提出了一个 20 万规模的语义相机控制数据集和首个主动操作评测基准。

## Problem
- 现有 VLA/机器人操作方法大多假设固定且接近最优的视角，遇到遮挡、目标不在视野内、视角变化时容易失败。
- 直接把相机运动和机械臂动作塞进同一个动作空间，需要大量带双重标注的数据，还会干扰已有操作先验，训练低效。
- 缺少专门评测“主动感知+主动操作”的标准化基准，导致这类能力难以系统比较与复现。

## Approach
- 将动作空间解耦为两部分：头部相机动作和其他操作动作，分别用独立 action heads 预测，减少相互干扰。
- 采用两阶段自底向上训练：先在 **ActiveViewPose-200K** 上只学语义驱动的相机运动，再用混合数据联合优化相机与操作。
- 用一个基于 LoRA 的 **Camera Adapter** 保留“如何为了任务去看”的语义相机控制先验，而不破坏原始 VLM/VLA 权重。
- 引入 **Universal Spatial Knowledge Injection**，把深度、相机内外参等 3D 几何信息编码后注入动作解码过程，提升动态视角下的空间鲁棒性。
- 提出 **ActiveManip-Bench**，用于在仿真中系统评估主动操作，覆盖 12 个任务、100 个物体、20 个场景。

## Results
- 在语义主动感知评测上，SaPaVe Stage 1 在 **ActiveViewPose-200K** 上取得 **84.3%** 平均成功率，超过 **Gemini-2.5-Pro 的 72.7%**、**Multi-SpatialMLLM 的 70.2%**、**Qwen2.5-VL-72B 的 62.3%**；相对 Gemini 提升 **11.6 个百分点**（文中前文也宣称最高约 **16%**）。
- 分拆看该任务：SaPaVe 在 **Val/Test1/Test2** 上分别为 **85.5/89.1/78.3**，而 Gemini-2.5-Pro 为 **73.3/76.5/68.2**，说明在需要更强语义推断的 Test2 上也保持领先。
- 在仿真 **ActiveManip-Bench** 上，SaPaVe（Active Camera）平均成功率 **74.83%**，高于 **Fixed Camera 的 36.17%**、**Fixed Camera + Wrist Camera 的 52.33%**、**Active Camera + Wrist Camera 的 73.16%**。
- 同一仿真基准中，固定视角在 Out-of-View 任务上明显失效，例如 **Out-of-View Pick-and-Place 仅 11%**、**Out-of-View Articulated Manipulation 仅 7%**；SaPaVe 分别达到 **72%** 和 **68%**。
- 图注声称在 **ActiveManip-Bench** 上整体平均成功率达到 **75.2%**，并且相对固定视角 VLA（如 **GR00T-N1**）绝对提升可达 **58 个百分点**。
- 在真实机器人主动操作上，SaPaVe 平均成功率 **85.0%**，显著高于 **π0 的 45.0%** 和 **GR00T-N1 的 53.75%**；相对 π0 提升 **40 个百分点**，相对 GR00T-N1 提升 **31.25 个百分点**。

## Link
- [http://arxiv.org/abs/2603.12193v1](http://arxiv.org/abs/2603.12193v1)
