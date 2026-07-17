---
source: arxiv
url: https://arxiv.org/abs/2607.15065v1
published_at: '2026-07-16T14:37:43'
authors:
- Susie Lu
- Haonan Chen
- Weirui Ye
- Yilun Du
topics:
- world-models
- robotics
- action-conditioned-video
- robot-planning
- policy-evaluation
- fast-generation
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# DriftWorld: Fast World Modeling through Drifting

## Summary
## 摘要
DriftWorld 是一种单步、动作条件世界模型，通过一次前向传递预测机器人未来观测，而不是使用迭代式扩散采样。在五个操作基准上，该模型报告了 17 倍的生成速度提升，同时保持或改善了 rollout 质量，并支持更快的规划和离线策略评估。

## 问题
- 基于扩散的机器人世界模型需要重复执行去噪步骤，导致大规模动作搜索速度缓慢；文中引用的一个基线模型在每个决策周期中有 90–95% 的时间用于生成 rollout，且每次决策至少需要 3 秒。
- 想象过程缓慢会限制机器人在执行动作前能够评估的候选动作序列数量，也会增加无需真实世界执行即可对策略进行排序的成本。

## 方法
- DriftWorld 在训练期间学习一个动作条件漂移场，使生成的未来视频样本向真实未来移动，并远离生成的负样本。
- 推理时，模型根据高斯噪声、观测历史和给定的动作序列，在一次 U-Net 前向传递中生成未来帧，从而避免迭代式扩散去噪。
- 模型采用逐帧 FiLM 动作条件、因子化时空卷积，以及用于复杂真实场景的 DINOv2/v3 特征空间漂移。
- 运动加权特征损失抑制模型忽略动作、仅复制当前观测的倾向。

## 结果
- 在五个基准——Bridge-V2、RT-1、Language Table、Push-T 和 Robomimic——上，论文报告了 30+ fps 的生成速度，以及相较于基于扩散的世界模型基线平均 17 倍的加速。
- 在 Push-T 的 64 帧 rollout 上，DriftWorld 达到 MSE 0.0007、SSIM 0.9925、PSNR 33.7753 和 LPIPS 0.0050，每生成一帧耗时 0.0037 秒；GPC 基线每帧耗时 0.0104 秒，SSIM 为 0.9717。
- 在 Bridge-V2 上，DriftWorld 达到 SSIM 0.821、PSNR 21.871、LPIPS 0.103 和 FVD 101.16，每帧耗时 0.0300 秒；相比之下，IRASim 的 SSIM 为 0.738，每帧耗时 1.1031 秒。
- 使用基于 rollout 的动作选择后，Push-T 的 IoU 从 0.635 提升至 0.781。
- 在离线策略排序中，rollout 得分与真实表现的 Pearson 相关系数为：Push-T 上 0.9515，Robomimic Lift 上 0.9916，Robomimic Can 上 0.9250。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.15065v1](https://arxiv.org/abs/2607.15065v1)
