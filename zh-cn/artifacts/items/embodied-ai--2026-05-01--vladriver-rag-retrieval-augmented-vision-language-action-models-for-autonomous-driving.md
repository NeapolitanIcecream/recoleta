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
VLADriver-RAG 在 VLA 驾驶策略中加入检索，使规划器在选择路径和速度时可以使用相似的历史场景。论文称，性能提升来自检索语义交通图，而不是原始图像，这减少了长尾驾驶案例中的视觉歧义。

## 问题
- 它针对自动驾驶 VLA 模型在稀有交通案例训练数据稀疏时泛化能力弱的问题。
- 原始视觉检索对闭环驾驶来说太慢，而且可能把像素相似但交通逻辑不同的场景匹配到一起，例如信号灯状态不同的场景。
- 这个问题很重要，因为错误检索到的示例可能把规划器推向稀有或分布外场景中的不安全轨迹。

## 方法
- 核心机制把摄像头观测转换为以自车为中心的时空语义图，包含车辆、车道、标志、信号灯和关系边。
- Scenario-Aligned Embedding Model 使用 R-GCN 和 Transformer 编码器对图序列进行编码。
- 训练使用图重建和 Graph-DTW 度量对齐，使相近向量对应相似的交通拓扑和交互历史。
- 运行时，当前图从向量数据库中检索历史驾驶先验。
- VLA 规划器融合视觉 token、导航和速度 token，以及检索到的上下文 token，然后使用独立的查询 token 预测路径路点和速度路点。

## 结果
- 在 Bench2Drive 上，VLADriver-RAG 报告的 Driving Score 为 89.12，Success Rate 为 70.42%。
- 它超过了文中引用的 VLA 基线 ORION；ORION 在同一基准上的结果为 77.74 DS 和 54.62% SR。
- 它在 Driving Score 上也超过了文中引用的 VLA 基线 Simlingo，摘录中报告为 85.0 DS。
- 它超过了摘录中列出的多个端到端基线，包括 DriverAdapter 的 64.22 DS 和 33.08% SR、ThinkTwice 的 62.44 DS 和 31.23% SR，以及 TCP-traj 的 59.90 DS 和 30.00% SR。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08133v2](https://arxiv.org/abs/2605.08133v2)
