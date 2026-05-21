---
source: arxiv
url: https://arxiv.org/abs/2604.26848v2
published_at: '2026-04-29T16:13:39'
authors:
- Yuxuan Tian
- Yurun Jin
- Bin Yu
- Yukun Shi
- Hao Wu
- Chi Harold Liu
- Kai Chen
- Cong Huang
topics:
- vision-language-action
- robot-world-model
- diffusion-policy
- geometric-attention
- bimanual-manipulation
- sim2real
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# STARRY: Spatial-Temporal Action-Centric World Modeling for Robotic Manipulation

## Summary
## 摘要
STARRY 是一种 VLA 机器人策略，用于在操作任务中把未来世界预测与动作生成结合起来。它在联合扩散策略中加入 3D 几何引导的注意力，并在 RoboTwin 2.0 和真实双臂任务上报告了更高的成功率。

## 问题
- 反应式 VLA 策略通常把当前 RGB-D 观测和语言直接映射到动作，这会影响需要推理未来接触、时序和物体几何的任务。
- 既有世界模型策略可以预测未来视频或潜在状态，但这些预测可能忽略对动作关键的区域，例如把手、开口、接触面以及末端执行器附近的空间。
- 论文针对空间受限操作中的失败问题；在这类任务中，微小的 3D 对齐误差可能导致碰撞、抓取不稳或放置失败。

## 方法
- STARRY 使用扩散策略，在同一时间范围内联合去噪未来时空潜变量和未来动作序列。
- 它的 Spatial-Temporal World Model 由多视角 RGB、深度、投影后的 3D 末端执行器轨迹和历史动作构建输入，然后预测供动作分支使用的未来潜在状态。
- Geometry Expert 在扩散过程中预测未来深度图和末端执行器位置。
- GASAM 将预测深度反投影到 3D，计算每个视觉 token 到预测末端执行器的距离，把这些距离转换为 token 权重，并使动作到视频的注意力偏向附近的几何相关区域。
- 训练采用分阶段预训练、动作与几何学习以及联合微调，并使用 Wan 初始化视频扩散部分，使用 Qwen-VL 初始化视觉语言理解部分。

## 结果
- 在 RoboTwin 2.0 的 50 个双臂任务上，STARRY 报告的平均成功率为 Clean 93.82%、Randomized 93.30%。基线：LingBot-VA 为 92.93% / 91.55%，Motus 为 88.66% / 87.02%，X-VLA 为 72.80% / 72.84%，pi-0.5 为 62.86% / 60.30%。
- 在 Handover Mic 上，STARRY 达到 100% / 99%，相比之下 Motus 为 78% / 63%，pi-0.5 为 63% / 57.5%。
- 在 Hanging Mug 上，STARRY 达到 69% / 72%，相比之下 LingBot-VA 为 40% / 28%，Motus 为 38% / 38%，X-VLA 为 23% / 27%，pi-0.5 为 10.5% / 10%。
- 在 Press Stapler 上，STARRY 达到 100% / 100%，相比之下 LingBot-VA 为 85% / 82%，Motus 为 93% / 98%，X-VLA 为 92% / 98%，pi-0.5 为 83.5% / 76.5%。
- 在三项 ARX R5 真实双臂任务实验中，论文报告称，平均成功率从 pi-0.5 的 42.5% 提高到 STARRY 的 70.8%；每个任务使用 50 次演示，每种方法进行 20 次评估 rollout。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.26848v2](https://arxiv.org/abs/2604.26848v2)
