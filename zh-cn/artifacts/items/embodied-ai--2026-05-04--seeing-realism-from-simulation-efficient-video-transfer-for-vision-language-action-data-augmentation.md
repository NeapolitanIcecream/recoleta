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
论文称，逼真的视频迁移可以让仿真机器人数据更适合训练视觉-语言-动作策略。该方法把仿真轨迹转换成视觉上更多样的视频，同时保留相同动作，然后用混合数据训练 VLA 模型。

## 问题
- VLA 策略需要大量真实机器人数据集，但采集这些轨迹速度慢、成本高。
- 仿真轨迹成本低，但画面干净、布局固定、场景变化范围窄，导致模型很难迁移到杂乱环境、光照变化、纹理变化和指令变化中。
- 论文研究机器人策略的数据增强，重点关注在大规模数据集上做完整视频生成成本过高的情况。

## 方法
- 流水线用 VideoChat2 为每个仿真机器人视频生成字幕，用 Qwen3-8B 改写字幕以改变场景外观，并提取深度图作为几何条件。
- Cosmos-Transfer 2.5 在改写后的字幕和深度条件下生成逼真视频，目标是保留原始任务语义和动作轨迹。
- 三阶段 velocity caching 方法在稳定去噪步骤中跳过重复的扩散 velocity 预测，使用 k=0.4、alpha=8、m=3 个最终调整步骤等参数。
- coreset 采样器用 RDT-1B 动作预测损失衡量难度，并用 Cosmos-Embed1 视频嵌入衡量视觉多样性，从而选择要增强的轨迹。

## 结果
- 在使用 RDT-1B 的 RoboTwin 2.0 单任务学习中，每个任务使用 50 个演示和 50 次测试；Hard 设置下平均成功率从 29.0% 升至 39.0%（+10.0 个百分点），Easy 设置下从 49.0% 升至 55.0%（+6.0 个百分点）。
- 在使用 RDT-1B 的 RoboTwin 2.0 多任务学习中，实验使用 32 个任务和 9,600 条轨迹；增强 10% 的 coreset 后，Hard 设置下平均成功率从 23.0% 升至 31.0%（+8.0 个百分点）。
- 在包含 2,402 个评估设置的 LIBERO-Plus spatial suite 上，pi_0 从 42.7% 提升到 47.8%（+5.1 个百分点），其中 object layout（+16.6 个百分点）和 language instructions（+22.0 个百分点）增幅较大。
- 在同一 LIBERO-Plus suite 上，pi_0.5 从 89.8% 提升到 90.8%（+1.0 个百分点）；由于基线已经很高，增幅较小。
- 在标准 LIBERO 上，增强训练使性能略有下降：pi_0 平均下降 0.2 个百分点，pi_0.5 下降 0.5 个百分点；论文将其归因于 LIBERO 的训练-测试相似性。
- diffusion velocity caching 方法在 RoboTwin 2.0 上将生成时间平均减少 61.2%，论文称质量损失很小。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.02757v1](https://arxiv.org/abs/2605.02757v1)
