---
source: arxiv
url: https://arxiv.org/abs/2606.18955v1
published_at: '2026-06-17T11:37:59'
authors:
- Runze Xu
- Yiluo Zhang
- Jian Wang
- Yu Wang
- Jincheng Yu
topics:
- vision-language-action
- latent-action
- human-egovideo
- cross-embodiment
- robot-data-scaling
- dual-arm-manipulation
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# Motion-Focused Latent Action Enables Cross-Embodiment VLA Training from Human EgoVideos

## Summary
## 摘要
本文提出一种 VLA 训练方法：从无标注的人类第一视角视频中学习运动意图，并用每个任务约 50 条轨迹适配到机器人。其主要主张是，带掩码的潜在动作 token 可以在人类、单臂机器人和双臂机器人具身形态之间迁移。

## 问题
- 通用 VLA 模型需要带动作标签的大规模机器人数据集；这类数据采集成本高，并且难以在不同机器人本体之间对齐。
- 人类第一视角操作视频数量充足，但大多数缺少手部姿态或机器人动作标签，因此标准 VLA 训练无法直接使用它们。
- 现有的潜在动作视频方法可能把背景变化、相机运动和其他视觉噪声编码为动作 token，从而削弱从人类到机器人的迁移。

## 方法
- 该方法在相隔 1 秒的相邻视频帧上训练混合解耦 VQ-VAE，使用冻结的 DINOv2 特征以及独立的动作潜在分支和背景潜在分支。
- 它使用来自 SAM2 的人手物理掩码，或来自 RoboEngine 的机器人手臂物理掩码，使动作分支重建前景运动，同时让背景分支重建场景区域。
- 动作码本和背景码本的大小均为 16；每对帧被编码为 4 个离散潜在动作 token。
- 一个 Prismatic-7B VLM 经过预训练，可从图像和语言指令预测这些潜在动作 token，因此 VLM 在没有动作标签的情况下学习运动意图。
- 在机器人适配期间，LoRA 更新 VLM，流匹配动作专家预测机器人控制量，DINOv2 视觉特征加本体感知提供状态反馈，以减少动作幻觉。

## 结果
- 在 LIBERO 仿真中，完整方法在 Spatial、Object、Goal 和 Long 套件上的平均成功率达到 91.8%，高于 villa-x 的 90.1%、UniVLA-Bridge 的 88.1%、pi0-fast 的 85.5%、OpenVLA 的 76.5% 和 Diffusion Policy 的 72.4%。
- 在 LIBERO 上，它在 Spatial、Object、Goal 和 Long 上的得分分别为 95.5%、94.0%、93.5% 和 84.0%。它在 Goal 上比 villa-x 高 2.0 个百分点，在 Long 上高 9.5 个百分点；villa-x 在 Spatial 和 Object 上更高。
- LIBERO 消融实验中，去掉 DINO 状态特征后，平均成功率从 91.8% 降至 85.4%，支持意图与感知分离的设计。
- 在 RoboTwin 2.0 双臂仿真中，该方法在 10 个任务上的平均成功率达到 67.7%，相比之下 pi0 为 65.2%，UniVLA 为 63.6%，RDT 为 52.5%，ACT 为 51.2%，Diffusion Policy 为 49.7%。
- 在 RoboTwin 2.0 上，去掉 DINO 状态特征后的平均成功率为 62.8%，在后训练期间冻结 VLM 后为 52.4%，完整方法为 67.7%。
- 下游适配设置在 LIBERO 和 RoboTwin 2.0 上每个任务使用 50 条轨迹；预训练只使用无标注视频数据，不使用动作标签。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.18955v1](https://arxiv.org/abs/2606.18955v1)
