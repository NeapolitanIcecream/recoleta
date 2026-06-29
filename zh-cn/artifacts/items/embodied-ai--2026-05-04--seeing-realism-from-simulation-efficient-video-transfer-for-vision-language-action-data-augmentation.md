---
source: arxiv
url: https://arxiv.org/abs/2605.02757v1
published_at: '2026-05-04T15:57:07'
authors:
- Chenyu Hui
- Xiaodi Huang
- Siyu Xu
- Yunke Wang
- Shan You
- Fei Wang
- Tao Huang
- Chang Xu
topics:
- vision-language-action
- sim2real
- robot-data-augmentation
- video-transfer
- coreset-sampling
- diffusion-acceleration
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Seeing Realism from Simulation: Efficient Video Transfer for Vision-Language-Action Data Augmentation

## Summary
## 摘要
本文认为，把仿真视频转成更逼真的视频，可以让仿真机器人数据在训练视觉-语言-动作策略时更有用。它把仿真轨迹转成视觉上更丰富的视频，同时保留相同动作，再用混合数据训练 VLA 模型。

## 问题
- VLA 策略需要大量真实机器人数据，但采集这些轨迹既慢又贵。
- 仿真轨迹虽然便宜，但干净的视觉效果、固定的布局和有限的场景变化，会让模型在杂乱环境、光照变化、纹理变化和指令变化上的迁移效果变差。
- 论文关注机器人策略的数据增强，尤其是在对大规模数据集做完整视频生成的成本过高时。

## 方法
- 该流程先用 VideoChat2 为每段仿真机器人视频生成描述，再用 Qwen3-8B 改写描述以改变场景外观，并提取深度图作为几何条件。
- Cosmos-Transfer 2.5 根据改写后的描述和深度信息生成逼真的视频，目标是保留原始任务语义和动作轨迹。
- 一个三阶段速度缓存方法会在稳定的去噪步骤中跳过重复的扩散速度预测，使用的参数包括 k=0.4、alpha=8 和 m=3 个最终调整步骤。
- 一个 coreset 采样器使用 RDT-1B 的动作预测损失衡量难度，并用 Cosmos-Embed1 视频嵌入衡量视觉多样性，从而选择用于增强的轨迹。

## 结果
- 在 RoboTwin 2.0 的单任务学习中，使用 RDT-1B 时，Hard 设置下平均成功率从 29.0% 提升到 39.0%（+10.0 个百分点），Easy 设置下从 49.0% 提升到 55.0%（+6.0 个百分点）；每个任务使用 50 个示范和 50 次测试。
- 在 RoboTwin 2.0 的多任务学习中，使用 RDT-1B 时，使用了 32 个任务和 9,600 条轨迹；将 10% 的 coreset 做增强后，Hard 设置下的平均成功率从 23.0% 提升到 31.0%（+8.0 个百分点）。
- 在包含 2,402 个评测设置的 LIBERO-Plus spatial suite 上，pi_0 从 42.7% 提升到 47.8%（+5.1 个百分点），其中物体布局提升了 16.6 个百分点，语言指令提升了 22.0 个百分点。
- 在同一 LIBERO-Plus suite 上，pi_0.5 从 89.8% 提升到 90.8%（+1.0 个百分点）；由于基线已经很高，增幅较小。
- 在标准 LIBERO 上，增强训练让性能略有下降：pi_0 平均下降 0.2 个百分点，pi_0.5 下降 0.5 个百分点，论文把这归因于 LIBERO 的训练和测试相似度较高。
- 扩散速度缓存方法在 RoboTwin 2.0 上把生成时间平均缩短了 61.2%，论文称质量损失很小。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.02757v1](https://arxiv.org/abs/2605.02757v1)
