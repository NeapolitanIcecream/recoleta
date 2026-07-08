---
source: arxiv
url: https://arxiv.org/abs/2607.04880v1
published_at: '2026-07-06T10:00:47'
authors:
- Dogyu Ko
- Haneul Kim
- Chanyoung Yeo
- Dowoon Lee
- Taeho Park
- Hyoseok Hwang
topics:
- robot-data-generation
- sim2real
- vision-language-action
- imitation-learning
- digital-cousins
- robot-manipulation
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# PRISM: Personalized Robotic Dataset Generation via Image-based Scene and Motion Synthesis

## Summary
## 摘要
PRISM 从一张目标场景图像和一条任务指令生成机器人训练数据集。它构建匹配但有变化的仿真场景，规划演示轨迹，并使用视觉随机化，让操作策略适应目标环境。

## 问题
- 预训练 VLA 策略在用户的真实场景中可能失败，因为其训练轨迹没有覆盖这个具体环境。
- 遥操作能提供匹配数据，但需要人工时间；通用仿真容易扩展，但可能无法贴近目标场景；数字孪生可能过拟合到单个场景实例。
- 论文目标是为个性化机器人操作生成低成本数据，这有助于在不收集大量真实演示的情况下适配机器人策略。

## 方法
- PRISM 从单张 RGB-D 图像中检测物体，使用 Grounded-SAM 生成掩码，并使用深度和相机内参；需要时用 Depth Anything v2 和 Perspective Fields 估计这些信息。
- 它用 CLIP 按类别检索 3D 资产，用 DINOv2 嵌入对渲染后的资产匹配结果排序，并让 VLM 选择视觉上相似的候选项。
- 它构建 digital cousin 场景，使物体类别、几何形状和空间关系接近目标场景，同时改变资产实例、物体姿态、光照、纹理和干扰物。
- VLM 将自然语言指令转换为 pick 和 place 等原子动作，然后 TAMP 生成包含抓取姿态和关节路径的无碰撞轨迹。
- 运动感知抓取选择会优先选择与标准末端执行器朝向一致的抓取方式；保持轨迹的视觉随机化会在不同视觉条件下重放同一条成功运动。

## 结果
- 在 sim-to-sim 测试中，每种方法为每个任务生成 400 条轨迹。在使用 pi_0.5 的 "Put milk in basket" 任务上，PRISM 在 LIBERO 上得分 98.0%，X-Sim 为 48.0%，RoboTwin 2.0 为 14.0%；在 LIBERO-Plus 上，PRISM 得分 67.6%，对比 35.8% 和 21.9%。
- 在使用 pi_0.5 的 "Put wine bottle on cabinet" 任务上，PRISM 在 LIBERO 上得分 98.0%，X-Sim 为 82.0%，RoboTwin 2.0 为 16.0%；在 LIBERO-Plus 上，PRISM 得分 52.0%，低于 X-Sim 的 54.5%，高于 RoboTwin 2.0 的 3.3%。
- 使用 Diffusion Policy 时，PRISM 在 "Put milk in basket" 任务上达到域内 95.0%、LIBERO 94.0%、LIBERO-Plus 35.6%；X-Sim 分别为 84.0%、80.0% 和 2.8%，RoboTwin 2.0 分别为 84.0%、2.0% 和 33.7%。
- 对于使用 Diffusion Policy 的 "Put wine bottle on cabinet" 任务，PRISM 得分为域内 100.0%、LIBERO 56.0%、LIBERO-Plus 28.8%；X-Sim 分别为 40.0%、44.0% 和 0.6%，RoboTwin 2.0 分别为 78.0%、34.0% 和 27.2%。
- 在 real-to-sim-to-real 实验中，PRISM 评估了三个真实操作任务，每个任务 10 次试验，并声称成功率最高达到 100%，且成功率高于基线生成数据集；摘录未提供 Figure 4 中各任务的具体数值。
- 消融实验报告称，PRISM-Cousin 在目标环境中为 80.0%，在变体环境中为 80.0%；PRISM-Twin 在目标环境中为 100.0%，在变体环境中为 30.0%。运动感知抓取选择将 pi_0.5 从 56.0% 提高到 98.0%，将 Diffusion Policy 从 52.0% 提高到 56.0%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.04880v1](https://arxiv.org/abs/2607.04880v1)
