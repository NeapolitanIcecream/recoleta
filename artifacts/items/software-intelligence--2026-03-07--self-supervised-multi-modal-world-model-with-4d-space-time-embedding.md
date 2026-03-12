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
- spatiotemporal-embedding
- earth-observation
relevance_score: 0.18
run_id: materialize-outputs
---

# Self-Supervised Multi-Modal World Model with 4D Space-Time Embedding

## Summary
DeepEarth 提出了一种自监督多模态世界模型，并用 Earth4D 把地球上的位置与时间统一编码成可学习表示。其核心主张是：仅靠时空坐标加少量语义信息，也能学到强表达，并在生态预测任务上超过更重的预训练多模态基线。

## Problem
- 需要一种能在**全球尺度**上统一表示空间与时间的方法，用于学习地球观测中的多模态规律。
- 现有方法很难同时覆盖**超大空间范围、长时间跨度**与**高精度**，还要兼顾内存/计算可扩展性。
- 这很重要，因为生态预测、环境监测和世界模型构建都依赖稳定的时空表示；若表示不足，就难以泛化到不同地点、季节和事件。

## Approach
- 提出 **Earth4D**：把连续的 `(latitude, longitude, elevation, time)` 映射为 4D 时空位置嵌入，基于多分辨率哈希编码扩展而来。
- Earth4D 不直接做完整 4D 网格，而是组合四个可并行的 3D 网格：`xyz`、`xyt`、`yzt`、`xzt`，以更高效地表示时空结构。
- 在 **DeepEarth** 中，Earth4D 嵌入与视觉、语言、传感器等模态编码器输出融合，作为 token 输入自编码器，通过**masked reconstruction**进行自监督训练。
- 为减轻哈希冲突，作者加入 **learned hash probing**，让模型学习更优的哈希索引分配，从而提升表示质量。
- 在 LFMC 实验里，模型甚至只用 `(x,y,z,t) + species` 就进行预测，验证时空编码本身的表达能力。

## Results
- 在 **Globe-LFMC 2.0**（官方划分：训练 **76,467**，测试 **13,297**）上，**Earth4D (Learned Hashing)** 达到 **MAE 11.7pp、RMSE 18.7pp、R² 0.783**。
- 对比预训练多模态基线 **Galileo**（输入含遥感、天气、地形、坐标和物种），其结果为 **MAE 12.6pp、RMSE 18.9pp、R² 0.72**；Earth4D 在更少输入下仍更好，MAE 绝对降低 **0.9pp**，R² 提升 **0.063**。
- 误差分布图显示，在测试集上的**中位绝对误差为 7.1pp**，并声称时序预测能较好跟踪 **2017–2023** 年季节变化。
- 相比**不带 learned probing** 的标准哈希编码（**RMSE 26.0pp、MAE 16.6pp、R² 0.58**），加入 learned probing 后提升到 **18.7pp / 11.7pp / 0.783**，即 **MAE 降低 29.5%**、**R² 提升 35.0%**。
- 在极限压缩设置下，模型从 **800M 参数**压到 **5M 参数**（**99.3%** reduction，**93%** memory reduction），仍达到 **MAE 15.0pp、R² 0.668**，并声称较 800M 无 probing 基线 **训练快 4×**、**R² 高 14.7%**。
- 附录还声称 learned probing 在 RGB reconstruction 上使验证损失降低 **18%**，并把 **1M points** 情况下的哈希冲突减少 **33%**。

## Link
- [http://arxiv.org/abs/2603.07039v1](http://arxiv.org/abs/2603.07039v1)
