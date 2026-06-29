---
source: arxiv
url: https://arxiv.org/abs/2605.08133v2
published_at: '2026-05-01T05:50:00'
authors:
- Rui Zhao
- Haofeng Hu
- Zhenhai Gao
- Jiaqiao Liu
- Gao Fei
topics:
- autonomous-driving
- vision-language-action
- retrieval-augmented-generation
- trajectory-planning
- graph-retrieval
- bench2drive
relevance_score: 0.72
run_id: materialize-outputs
language_code: zh-CN
---

# VLADriver-RAG: Retrieval-Augmented Vision-Language-Action Models for Autonomous Driving

## Summary
## 摘要
VLADriver-RAG 给 VLA 驾驶策略加入检索，让规划器在选择路径和速度时可以利用相似的历史场景。论文声称，提升来自检索语义交通图，而不是原始图像，这样在长尾驾驶场景中能减少视觉歧义。

## 问题
- 它解决的是自动驾驶 VLA 模型在稀有交通情况上泛化能力弱的问题，因为这类情况在训练数据里很少。
- 原始视觉检索在闭环驾驶中太慢，而且会把像素相似但交通逻辑不同的场景匹配到一起，比如信号灯状态不同。
- 这个问题很重要，因为一旦检索到错误示例，规划器在罕见或分布外场景里可能会走向不安全轨迹。

## 方法
- 核心机制把摄像头观测转换成以自车为中心的时空语义图，图里包含车辆、车道、标志、信号灯和关系边。
- Scenario-Aligned Embedding Model 用 R-GCN 和 Transformer 编码器对图序列编码。
- 训练时结合图重建和 Graph-DTW 度量对齐，让相近向量对应相似的交通拓扑和交互历史。
- 运行时，当前图会从向量数据库里检索历史驾驶先验。
- VLA 规划器融合视觉 token、导航和速度 token，以及检索到的上下文 token，然后用单独的 query token 预测路径航点和速度航点。

## 结果
- 在 Bench2Drive 上，VLADriver-RAG 的 Driving Score 为 89.12，Success Rate 为 70.42%。
- 它超过了文中引用的 VLA 基线 ORION，后者在同一基准上的 DS 为 77.74、SR 为 54.62%。
- 它在 Driving Score 上也超过了文中引用的 VLA 基线 Simlingo，摘录中给出的 DS 为 85.0。
- 它超过了摘录中列出的几个端到端基线，包括 DriverAdapter 的 64.22 DS 和 33.08% SR、ThinkTwice 的 62.44 DS 和 31.23% SR，以及 TCP-traj 的 59.90 DS 和 30.00% SR。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08133v2](https://arxiv.org/abs/2605.08133v2)
