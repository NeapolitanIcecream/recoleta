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
CRAFT 先在模拟器中运行轨迹，再用 Canny 引导的视频扩散模型将其转换为视频，从而生成带动作标签、具备照片级真实感的双臂机器人示范数据。它要解决的是双臂模仿学习中的数据稀缺和视觉多样性不足，尤其针对 sim2real 迁移、视角变化和跨 embodiment 训练。

## 问题
- 双臂模仿学习需要大量示范，但真实遥操作数据成本高，而且通常只覆盖有限的视角、物体布局、光照和机器人 embodiment。
- 现有增强方法通常只改变一个因素，比如视角或 embodiment，而且往往不能为新视觉样本同时生成对应的新动作标签。
- 这很关键，因为双臂任务依赖精确的夹爪-物体接触和双臂协调，训练数据过窄会削弱鲁棒性和迁移效果。

## 方法
- CRAFT 从一个小规模真实数据集出发，构建数字孪生，在模拟中重放并扩展轨迹，把成功的新轨迹保留下来作为额外监督。
- 它先渲染模拟器视频，提取 Canny 边缘控制视频，再将这些边缘与一张真实参考图像和一条语言指令一起输入预训练视频扩散模型。
- 核心思路是，Canny 边缘保留了操作任务中关键的运动和物体结构，同时去掉了模拟器纹理细节，这让扩散模型可以生成更真实的外观。
- 生成视频直接继承模拟轨迹中的动作标签，因此该方法输出的是动作一致的示范，而不是只改图像的编辑结果。
- 同一条流程支持七种增强类型：物体位姿、光照、物体颜色、背景、跨 embodiment 迁移、相机视角，以及手腕视角加第三人称视角的多视图生成。

## 结果
- 在模拟环境中的跨 embodiment 迁移任务里，从双臂 UR5 转到双臂 Franka 时，CRAFT (Ours) 在 Lift Pot、Place Cans 和 Stack Bowls 上分别达到 **82.6%**、**89.3%** 和 **86.0%**，使用 **1000 generated demos**，且 **no target-robot demos**。
- 在同一组模拟任务上，不使用额外生成数据的 CRAFT (Target) 分别为 **11.3%**、**6.0%** 和 **21.6%**，Shadow 分别为 **2.0%**、**2.3%** 和 **6.0%**。
- 论文报告称，CRAFT (Ours) 优于为目标机器人采集数据的基线；后者在这三个模拟任务上的得分分别为 **55.0%**、**69.0%** 和 **59.0%**，同时需要 **100 collected target demos**。
- 在真实环境中的跨 embodiment 迁移任务里，从双臂 xArm7 转到双臂 Franka 时，CRAFT (Ours) 在 LR、PC 和 SB 上分别取得 **17/20**、**15/20** 和 **16/20** 次成功；相比之下，CRAFT (Target) 为 **4/20**、**1/20** 和 **2/20**，Shadow 为 **2/20**、**1/20** 和 **1/20**，采集目标机器人数据为 **5/20**、**2/20** 和 **3/20**。
- 在 Stack Bowls 的消融实验中，Canny 引导将成功率从不使用 Canny 时的 **10.3%** 提高到使用 Canny 时的 **21.6%**；采集示范数据的上界为 **59.0%**。
- 摘要片段没有给出全部七种增强类型的完整定量结果，但文中称，在模拟和真实双臂任务上，它相对现有增强基线和直接扩大数据规模的方法都有稳定提升。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.03552v1](http://arxiv.org/abs/2604.03552v1)
