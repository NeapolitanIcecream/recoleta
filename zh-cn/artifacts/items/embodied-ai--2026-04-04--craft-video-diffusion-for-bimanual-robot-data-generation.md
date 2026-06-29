---
source: arxiv
url: http://arxiv.org/abs/2604.03552v1
published_at: '2026-04-04T02:36:54'
authors:
- Jason Chen
- I-Chun Arthur Liu
- Gaurav Sukhatme
- Daniel Seita
topics:
- bimanual-manipulation
- video-diffusion
- robot-data-generation
- cross-embodiment-transfer
- sim2real
- imitation-learning
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# CRAFT: Video Diffusion for Bimanual Robot Data Generation

## Summary
## 摘要
CRAFT 通过在模拟器中运行轨迹，并用受 Canny 边缘引导的视频扩散模型把这些轨迹转换成视频，生成带动作标签的双臂机器人示范。它针对双臂模仿学习中的数据稀缺和视觉多样性不足，尤其适用于 sim2real 迁移、视角变化和跨本体训练。

## 问题
- 双臂模仿学习需要大量示范，但真实遥操作数据成本高，而且通常只覆盖有限的视角、物体布局、光照和机器人本体。
- 现有增强方法通常只改变一个因素，比如视角或本体，而且常常不能为新的视觉结果生成新的动作标签。
- 这很重要，因为双臂任务依赖精确的夹爪-物体接触和协调，训练数据范围太窄会削弱鲁棒性和迁移能力。

## 方法
- CRAFT 从少量真实数据出发，构建数字孪生，在模拟中回放并扩展轨迹，并把成功的新轨迹保留为额外监督。
- 它渲染模拟器视频，提取 Canny 边缘控制视频，再把这些边缘与真实参考图像和语言指令一起输入预训练的视频扩散模型。
- 核心思路是，Canny 边缘保留操控中重要的运动和物体结构，同时去掉模拟器的纹理细节，让扩散模型有空间生成真实外观。
- 生成视频继承模拟轨迹的动作标签，因此方法输出的是动作一致的示范，而不是只改图像。
- 同一条流程支持七种增强类型：物体姿态、光照、物体颜色、背景、跨本体迁移、相机视角，以及关节腕部和第三人称多视角生成。

## 结果
- 在模拟中的跨本体迁移实验里，从双臂 UR5 到双臂 Franka，CRAFT（Ours）在 Lift Pot 上达到 **82.6%**，在 Place Cans 上达到 **89.3%**，在 Stack Bowls 上达到 **86.0%**，使用 **1000 个生成示范**，且**没有目标机器人示范**。
- 在相同的模拟任务上，CRAFT（Target）在没有额外生成数据时得到 **11.3%**、**6.0%** 和 **21.6%**，Shadow 得到 **2.0%**、**2.3%** 和 **6.0%**。
- 论文还报告，CRAFT（Ours）超过了目标机器人收集数据基线；该基线在这三个模拟任务上的分数分别是 **55.0%**、**69.0%** 和 **59.0%**，而且需要 **100 个收集到的目标示范**。
- 在真实世界的跨本体迁移实验里，从双臂 xArm7 到双臂 Franka，CRAFT（Ours）在 LR、PC 和 SB 上分别达到 **17/20**、**15/20** 和 **16/20** 次成功；CRAFT（Target）分别是 **4/20**、**1/20** 和 **2/20**，Shadow 分别是 **2/20**、**1/20** 和 **1/20**，收集到的目标数据分别是 **5/20**、**2/20** 和 **3/20**。
- 在 Stack Bowls 的消融实验中，加入 Canny 引导后，成功率从没有 Canny 的 **10.3%** 提升到 **21.6%**；收集示范的上限是 **59.0%**。
- 摘要片段没有给出全部七种增强类型的完整量化结果，但它声称在模拟和真实的双臂任务上，相比现有增强基线和直接扩大数据规模，CRAFT 都有稳定提升。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.03552v1](http://arxiv.org/abs/2604.03552v1)
