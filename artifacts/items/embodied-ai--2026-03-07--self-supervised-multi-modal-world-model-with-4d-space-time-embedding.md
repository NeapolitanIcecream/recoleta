---
source: arxiv
url: http://arxiv.org/abs/2603.07039v1
published_at: '2026-03-07T05:13:20'
authors:
- Lance Legel
- Qin Huang
- Brandon Voelker
- Daniel Neamati
- Patrick Alan Johnson
- Favyen Bastani
- Jeff Rose
- James Ryan Hennessy
- Robert Guralnick
- Douglas Soltis
- Pamela Soltis
- Shaowen Wang
topics:
- world-model
- self-supervised-learning
- multimodal-learning
- spatiotemporal-encoding
- earth-observation
relevance_score: 0.68
run_id: materialize-outputs
---

# Self-Supervised Multi-Modal World Model with 4D Space-Time Embedding

## Summary
DeepEarth提出了一个自监督多模态世界模型，并引入Earth4D这一行星尺度的4D时空位置编码器，用统一表示学习地球观测数据。其核心主张是：仅靠时空坐标与少量元数据，就能在生态预测任务上超过使用更多模态和更大预训练数据的基线模型。

## Problem
- 现有地球观测/世界模型很难同时在**全球范围、长时间跨度、高空间时间精度**下表示连续的4D时空信息。
- 多模态地球数据（图像、文本、传感器、遥感）分布复杂，若缺少强时空归纳偏置，统一建模与预测会受限。
- 这很重要，因为生态预测与灾害风险评估（如野火相关的植被含水量）依赖对“哪里、什么时候会发生什么”的准确建模。

## Approach
- 提出**Earth4D**：把传统3D多分辨率哈希编码扩展到4D，通过4个可并行的3D网格（xyz, xyt, yzt, xzt）来近似建模(latitude, longitude, elevation, time)的联合时空结构。
- 每个网格使用多分辨率哈希表，从而在固定内存预算下覆盖**行星尺度、跨世纪**的空间与时间，并声称可达到**亚米级、亚秒级**精度。
- DeepEarth将Earth4D时空嵌入与模态编码器（如视觉/语言编码器）的输出融合成token，在自编码器上下文窗口中进行**masked reconstruction**式自监督训练，学习联合分布并支持生成式重建/模拟。
- 为缓解哈希冲突，作者加入**learned hash probing**，让模型从候选索引中学习更优的哈希分配，提升表示效率与下游性能。

## Results
- 在**Globe-LFMC 2.0**生态预测基准上，Earth4D用于**Live Fuel Moisture Content**预测达到**MAE 11.7pp、RMSE 18.7pp、R² 0.783**。
- 对比基线**Galileo (pre-trained)**：其输入包含**遥感影像+天气+地形+(x,y,z,t)+species type**，结果为**MAE 12.6pp、RMSE 18.9pp、R² 0.72**；Earth4D仅用**(x,y,z,t)+species name**仍然更好。
- 测试集规模为**13,297**个样本；图中报告绝对误差**中位数 7.1pp**，并展示了**2017–2023**时间段内对季节变化的良好跟踪。
- 消融显示：不使用learned probing的标准哈希编码为**RMSE 26.0pp、MAE 16.6pp、R² 0.58**；加入learned probing后提升到**RMSE 18.7pp、MAE 11.7pp、R² 0.783**，即**MAE降低29.5%**、**R²提升35.0%**。
- 极限压缩版从**800M参数**降到**5M参数**（**99.3%**减少，哈希容量2^14），仍达到**MAE 15.0pp / R² 0.668**，相对800M无探测基线**R²高14.7%**，并带来**4×训练提速**与**93%内存降低**。
- 附录还声称，在RGB重建任务上，learned probing使验证损失再降**18%**；并将性能增益归因于**1M点模拟下哈希冲突降低33%**。

## Link
- [http://arxiv.org/abs/2603.07039v1](http://arxiv.org/abs/2603.07039v1)
