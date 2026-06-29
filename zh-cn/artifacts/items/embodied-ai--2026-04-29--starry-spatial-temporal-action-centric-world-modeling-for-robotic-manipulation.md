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
STARRY 是一个 VLA 机器人策略，把未来世界预测和动作生成结合起来，用于操作任务。它通过在联合扩散策略中加入 3D 几何引导注意力，在 RoboTwin 2.0 和真实双臂任务上取得了更高成功率。

## 问题
- 反应式 VLA 策略往往把当前 RGB-D 观测和语言直接映射到动作上，这会影响那些需要未来接触、时序和物体几何推理的任务。
- 以往的世界模型策略可以预测未来视频或潜在状态，但这些预测可能忽略对动作关键的区域，比如把手、开口、接触面，以及靠近末端执行器的空间。
- 论文针对的是空间约束下的操作失败。在这类任务中，细小的 3D 对齐误差就可能导致碰撞、不稳定抓取或放置失败。

## 方法
- STARRY 用同一个扩散策略，在相同时间范围内联合去噪未来空间-时间潜变量和未来动作序列。
- 它的空间-时间世界模型把多视角 RGB、深度、投影后的 3D 末端执行器轨迹和历史动作作为输入，再预测供动作分支使用的未来潜在状态。
- 几何专家在扩散过程中预测未来深度图和末端执行器位置。
- GASAM 将预测深度反投影到 3D，计算每个视觉 token 到预测末端执行器的距离，把这些距离转成 token 权重，并将动作到视频的注意力偏向附近、与几何相关的区域。
- 训练使用分阶段预训练、动作与几何学习，以及联合微调；视频扩散部分用 Wan 初始化，视觉语言理解部分用 Qwen-VL 初始化。

## 结果
- 在 RoboTwin 2.0 的 50 个双臂任务上，STARRY 报告 Clean 和 Randomized 设置下的平均成功率分别为 93.82% 和 93.30%。基线包括：LingBot-VA 92.93% / 91.55%，Motus 88.66% / 87.02%，X-VLA 72.80% / 72.84%，pi-0.5 62.86% / 60.30%。
- 在 Handover Mic 上，STARRY 达到 100% / 99%，而 Motus 为 78% / 63%，pi-0.5 为 63% / 57.5%。
- 在 Hanging Mug 上，STARRY 达到 69% / 72%，而 LingBot-VA 为 40% / 28%，Motus 为 38% / 38%，X-VLA 为 23% / 27%，pi-0.5 为 10.5% / 10%。
- 在 Press Stapler 上，STARRY 达到 100% / 100%，而 LingBot-VA 为 85% / 82%，Motus 为 93% / 98%，X-VLA 为 92% / 98%，pi-0.5 为 83.5% / 76.5%。
- 在 3 个 ARX R5 双臂真实任务的实验中，论文报告平均成功率从使用 pi-0.5 的 42.5% 提升到使用 STARRY 的 70.8%。每个任务使用 50 个示范，每种方法评估 20 次 rollout。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.26848v2](https://arxiv.org/abs/2604.26848v2)
