---
source: arxiv
url: https://arxiv.org/abs/2604.24681v1
published_at: '2026-04-27T16:42:18'
authors:
- Yifan Xie
- YuAn Wang
- Guangyu Chen
- Jinkun Liu
- Yu Sun
- Wenbo Ding
topics:
- vision-language-action
- robot-manipulation
- human-demonstration-learning
- hand-motion-priors
- robot-data-scaling
- sim2real
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# Learning Human-Intention Priors from Large-Scale Human Demonstrations for Robotic Manipulation

## Summary
## 摘要
MoT-HRA 使用大规模人类操作视频来预训练机器人策略，先学习空间意图和手部运动意图，再把这些意图映射为机器人动作。论文称，该方法提升了手部运动生成和 SimplerEnv 机器人操作表现，在 WidowX 任务上的平均成功率为 66.1%。

## 问题
- 与人类视频数据集相比，机器人操作数据集采集成本高、依赖特定硬件，而且规模小。
- 人类视频包含有用的操作行为，但原始片段混合了场景上下文、手部运动、相机运动和人类特定的具身形态。
- 这个问题很重要，因为机器人策略需要可迁移的意图，例如在哪里交互以及接触如何展开，同时不能把人手运动直接当作机器人控制。

## 方法
- 作者构建了 HA-2.2M，这是一个包含 220 万个 episode 的动作-语言数据集，来源包括 HowTo100M、Ego4D、EPIC-KITCHENS 和 Something-Something-V2。
- 数据整理流程会筛选以手为中心的操作片段，用 HaMeR 重建 MANO 风格手部姿态，用 Depth Anything 3 对齐场景深度，用 V-JEPA 分割动作，并用 Gemini 进行标注和片段合并。
- MoT-HRA 将控制分解为三个专家：视觉-语言专家预测与具身形态无关的 3D 轨迹，意图专家生成 MANO 风格手部运动，精细专家预测机器人动作块。
- 只读键值传递让机器人动作专家使用轨迹和意图特征，同时阻止机器人动作损失覆盖上游人类运动先验。
- 训练结合 HA-2.2M 的人类运动监督和 AgiBot-World 的机器人动作监督，使用 15 的动作块时域长度。

## 结果
- HA-2.2M 包含 220 万个 episode：HowTo100M 贡献 140 万个，Ego4D 贡献 63 万个，EPIC-KITCHENS 贡献 12 万个，Something-Something-V2 贡献 5 万个。
- 在 Ego4D 手部运动生成上，MoT-HRA 报告 ADE 0.136 m、DTW 0.127 m、Rot 28.95°、Joint-Rot 34.16°，优于 VITRA 的 0.154 m、0.146 m、33.26° 和 41.81°。
- 在 OakInk 手部运动生成上，MoT-HRA 报告 ADE 0.184 m、DTW 0.176 m、Rot 38.47°、Joint-Rot 40.12°，优于 VITRA 的 0.211 m、0.201 m、42.59° 和 41.72°。
- 在 SimplerEnv-WidowX 上，MoT-HRA 达到 66.1% 的平均成功率；ThinkACT 为 43.8%，SpatialVLA 为 42.7%，OpenVLA-OFT 为 41.7%，RoboVLMs 为 37.5%，π0-FAST 为 32.1%，π0 为 27.1%。
- 在四个 SimplerEnv 任务上，MoT-HRA 在 Spoon 上为 78.1%，在 Carrot 上为 62.5%，在 Stack 上为 40.6%，在 Eggplant 上为 83.3%；只有 Eggplant 任务中 SpatialVLA 更高，为 100.0%。
- 摘录称真实世界操作有提升，但没有提供真实世界成功率数字。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.24681v1](https://arxiv.org/abs/2604.24681v1)
