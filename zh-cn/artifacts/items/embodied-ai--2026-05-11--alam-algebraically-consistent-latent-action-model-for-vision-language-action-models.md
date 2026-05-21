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
ALAM 从无动作标注的机器人视频中学习结构化的潜在动作转移，并把它们用作 VLA 策略训练的辅助目标。它的主要主张是：潜在空间中的代数一致性可以提升 MetaWorld、LIBERO 和真实世界操作任务上的流匹配机器人策略。

## 问题
- VLA 模型需要大量带动作标签的机器人数据，而这类数据采集成本高。
- 无动作标注视频数量很多，但只用重建目标训练出的潜在编码虽然能预测帧，却可能给动作生成策略提供较弱的目标。
- 这个问题很重要，因为更好地使用无标签视频，可以在不需要匹配动作标签的情况下改进机器人策略的扩展能力。

## 方法
- ALAM 从无动作标注视频中采样帧三元组，并把每一对帧编码成一个潜在转移。
- 解码器根据源帧和潜在转移重建目标帧，使编码对应到观测到的视觉变化。
- 两个损失塑造潜在空间：组合一致性使 z(a,c) 接近 z(a,b) + z(b,c)，反转一致性使 z(b,a) 接近 -z(a,b)。
- 在 VLA 训练期间，预训练编码器被冻结。它从第三人称和腕部相机片段中提取潜在转移序列。
- 流匹配策略在一个交错序列中共同生成潜在转移和机器人动作；推理时只执行动作流。

## 结果
- 表征探针显示，与非结构化潜在动作基线相比，加法性和可逆性误差降低 25-85 倍。
- 在 MetaWorld MT50 上，π0 + ALAM 达到 85.0% 的平均成功率，相比之下 π0 为 47.9%，SmolVLA 为 66.9%，Evo-1 为 80.6%。
- π0 + ALAM 的 MetaWorld MT50 分层得分为：Easy 89.3%，Medium 83.6%，Hard 85.0%，Very Hard 82.0%。
- 在 LIBERO 上，π0 + ALAM 达到 98.1% 的平均成功率，相比之下 π0 为 94.1%，π0.5 为 96.9%，JALA 为 96.9%，UniVLA 为 95.2%。
- π0 + ALAM 的 LIBERO 套件得分为：Spatial 99.2%，Object 99.6%，Goal 99.0%，Long 94.4%。
- 预训练使用 11 个无动作标注视频来源、128 块 H20 GPU、39 个 epoch，耗时约 4 天；下游微调使用 8 块 H20 GPU，并采用 π0 风格的流匹配骨干网络。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.10819v2](https://arxiv.org/abs/2605.10819v2)
