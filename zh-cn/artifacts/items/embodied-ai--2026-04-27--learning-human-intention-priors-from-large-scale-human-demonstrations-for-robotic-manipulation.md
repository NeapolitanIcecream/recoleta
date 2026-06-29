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
MoT-HRA 使用大规模人类操作视频，在把意图映射到机器人动作之前，先用空间信息和手部运动意图预训练机器人策略。论文声称，它在手部运动生成和 SimplerEnv 机器人操作上都有提升，在 WidowX 任务上的平均成功率为 66.1%。

## 问题
- 机器人操作数据集采集成本高，依赖特定硬件，而且规模远小于人类视频数据集。
- 人类视频包含有用的操作行为，但原始片段会混在一起场景上下文、手部运动、相机运动和人类特有的身体结构。
- 这个问题很关键，因为机器人策略需要可迁移的意图，例如该在哪里接触、接触过程如何展开，而不是把人类手部运动当成机器人控制信号。

## 方法
- 作者构建了 HA-2.2M，这是一个 220 万 episode 的动作-语言数据集，来源于 HowTo100M、Ego4D、EPIC-KITCHENS 和 Something-Something-V2。
- 该整理流程先筛出以手为中心的操作片段，再用 HaMeR 重建 MANO 风格的手部姿态，用 Depth Anything 3 对齐场景深度，用 V-JEPA 划分动作段，并用 Gemini 做标注和片段合并。
- MoT-HRA 把控制拆成三个专家：视觉-语言专家预测与身体结构无关的 3D 轨迹，意图专家生成 MANO 风格的手部运动，精细专家预测机器人动作块。
- 只读键值传递让机器人动作专家可以使用轨迹和意图特征，同时阻止机器人动作损失覆盖上游的人类运动先验。
- 训练把 HA-2.2M 用于人类运动监督，把 AgiBot-World 用于机器人动作监督，chunk horizon 设为 15。

## 结果
- HA-2.2M 包含 220 万个 episode：其中 140 万来自 HowTo100M，63 万来自 Ego4D，12 万来自 EPIC-KITCHENS，5 万来自 Something-Something-V2。
- 在 Ego4D 手部运动生成任务上，MoT-HRA 的 ADE 为 0.136 m，DTW 为 0.127 m，Rot 为 28.95°，Joint-Rot 为 34.16°，优于 VITRA 的 0.154 m、0.146 m、33.26° 和 41.81°。
- 在 OakInk 手部运动生成任务上，MoT-HRA 的 ADE 为 0.184 m，DTW 为 0.176 m，Rot 为 38.47°，Joint-Rot 为 40.12°，优于 VITRA 的 0.211 m、0.201 m、42.59° 和 41.72°。
- 在 SimplerEnv-WidowX 上，MoT-HRA 的平均成功率为 66.1%，高于 ThinkACT 的 43.8%、SpatialVLA 的 42.7%、OpenVLA-OFT 的 41.7%、RoboVLMs 的 37.5%、π0-FAST 的 32.1% 和 π0 的 27.1%。
- 在这四个 SimplerEnv 任务上，MoT-HRA 在 Spoon 上为 78.1%，在 Carrot 上为 62.5%，在 Stack 上为 40.6%，在 Eggplant 上为 83.3%；SpatialVLA 只在 Eggplant 上更高，为 100.0%。
- 摘要声称它在真实世界操作上也有提升，但没有给出真实世界的成功率数字。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.24681v1](https://arxiv.org/abs/2604.24681v1)
