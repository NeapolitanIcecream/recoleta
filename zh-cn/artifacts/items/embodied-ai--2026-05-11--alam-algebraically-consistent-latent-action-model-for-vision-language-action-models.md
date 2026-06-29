---
source: arxiv
url: https://arxiv.org/abs/2605.10819v2
published_at: '2026-05-11T16:37:07'
authors:
- Zuojin Tang
- Haoyun Liu
- Xinyuan Chang
- Changjie Wu
- Dongjie Huo
- Yandan Yang
- Bin Liu
- Zhejia Cai
- Feng Xiong
- Mu Xu
- jiachen Luo
- De Ma
- Zhiheng Ma
- Gang Pan
topics:
- vision-language-action
- latent-action-models
- robot-data-scaling
- flow-matching
- action-free-video
- robot-manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# ALAM: Algebraically Consistent Latent Action Model for Vision-Language-Action Models

## Summary
## 摘要
ALAM 从没有动作标注的机器人视频中学习结构化的潜在动作转移，并把它们作为 VLA 策略训练的辅助目标。它的核心主张是，潜在空间里的代数一致性能提升基于 flow matching 的机器人策略在 MetaWorld、LIBERO 和真实世界操作任务上的表现。

## 问题
- VLA 模型需要大量带动作标注的机器人数据，而这类数据收集成本高。
- 没有动作标注的视频很充足，但只按重建训练的潜在编码虽然能预测帧，却不能给策略生成动作提供足够有结构的目标。
- 这个问题重要，因为更好地利用未标注视频，可以在不需要匹配动作标签的情况下提升机器人策略的扩展能力。

## 方法
- ALAM 从没有动作标注的视频中采样帧三元组，并把每一对帧编码成一个潜在转移。
- 解码器根据源帧和潜在转移重建目标帧，把编码锚定在可观察的视觉变化上。
- 两个损失函数塑造潜在空间：composition consistency 让 z(a,c) 接近 z(a,b) + z(b,c)，reversal consistency 让 z(b,a) 接近 -z(a,b)。
- 在 VLA 训练阶段，预训练编码器保持冻结。它从第三人称和腕部相机视频片段中提取潜在转移序列。
- 一个 flow-matching 策略在一个交错序列里共同生成潜在转移和机器人动作；推理时只执行动作流。

## 结果
- 表征探针报告，和无结构的 latent-action 基线相比，加法和可逆性误差低 25-85 倍。
- 在 MetaWorld MT50 上，π0 + ALAM 的平均成功率达到 85.0%，而 π0 为 47.9%，SmolVLA 为 66.9%，Evo-1 为 80.6%。
- π0 + ALAM 在 MetaWorld MT50 各级别上的得分是：Easy 89.3%，Medium 83.6%，Hard 85.0%，Very Hard 82.0%。
- 在 LIBERO 上，π0 + ALAM 的平均成功率达到 98.1%，而 π0 为 94.1%，π0.5 为 96.9%，JALA 为 96.9%，UniVLA 为 95.2%。
- π0 + ALAM 在 LIBERO 套件中的得分是：Spatial 99.2%，Object 99.6%，Goal 99.0%，Long 94.4%。
- 预训练使用 11 个没有动作标注的视频来源、128 张 H20 GPU、39 个 epoch，耗时约 4 天；下游微调用 8 张 H20 GPU，并使用基于 π0 风格的 flow-matching 主干。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.10819v2](https://arxiv.org/abs/2605.10819v2)
