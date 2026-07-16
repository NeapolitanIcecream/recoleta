---
source: arxiv
url: https://arxiv.org/abs/2607.13154v1
published_at: '2026-07-14T18:04:58'
authors:
- Lingxiao Guo
- Huanyu Li
- Guanya Shi
topics:
- robot-foundation-model
- generalist-robot-policy
- robot-data-scaling
- sim2real
- mobile-manipulation
- vision-language-action
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# Worlds in One Demo: A Synthetic Data Engine for Learning Open-World Mobile Manipulation

## Summary
## 摘要
WANDA 将一次真实的 RGBD 移动操作演示转换为跨越重建场景和生成式 3D 场景的合成轨迹。论文报告称，该方法提升了数据效率、空间泛化能力和长时域鲁棒性，并在五项任务上实现了真实世界部署，还能零样本迁移到具有不同形态的另一种机器人上。

## 问题
- 开放世界移动操作需要大量演示，因为机器人必须在不同物体位置、场景和较长任务时域中协调导航与操作。
- 远程操作和 UMI 数据采集需要大量人力、硬件和精确定位，因此大规模数据采集成本高昂。
- 这一问题之所以重要，是因为仅用少量演示训练的策略往往会出现空间泛化失败，并在长时域执行过程中产生不断累积的状态误差。

## 方法
- WANDA 使用 Gaussian splatting 从移动 RGBD 视角重建背景，并通过 BundleSDF 重建物体几何和 6D 运动，从一次演示构建可渲染的规划工作空间。
- 它将接触密集型交互片段重新定位到新的物体和机器人配置中，然后使用全身逆运动学和 RRT-Connect 规划，将导航与操作串联成完整轨迹。
- Corrective State Expansion 对物体和机器人状态施加扰动，使策略能够接触到导航和操作漂移，而不只是名义演示。
- 它使用 Marble 根据单张日常照片生成额外的 3D 场景，并将 Gaussian splatting 背景与渲染的机器人和物体网格结合，生成视觉训练数据。

## 结果
- 在 Bigym 仿真中，WANDA 根据一次源演示生成数据，在三个任务上取得了 75.6% 的平均成功率；相比之下，使用约 40–60 次源演示训练的 ACT 达到 78.0%。在单场景设置中，论文报告其相对于远程操作基线的数据效率提升约为 50 倍。
- 在 BEHAVIOR Challenge 任务中，WANDA 使用一次演示和 1,360 次生成演示取得了 16.67 的 Q-score；相比之下，使用 20、50 和 200 次官方演示训练的策略分别取得 3.33、11.11 和 62.22。
- 在 Agibot G1 上，一次演示在五项长时域任务中取得了 54.8% 的真实世界平均进度分数，每项任务进行 10 次试验：Lunch Box 为 55.0%，Utensil 为 52.5%，Drop Trash 为 75.0%，Fridge 为 46.7%，Pour 为 45.0%；这些结果来自所给摘录。
- 移除 Corrective State Expansion 后，报告的真实世界平均进度降至 15.7%，而完整 WANDA 为 54.8%。
- 论文报告称，该方法已在 16 个环境中部署，并使用根据单次 Agibot G1 演示生成的合成数据，零样本迁移到形态不同的 Linearbot 移动操作机器人；摘录未提供单独的迁移成功率指标。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.13154v1](https://arxiv.org/abs/2607.13154v1)
