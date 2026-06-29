---
source: arxiv
url: https://arxiv.org/abs/2606.24742v1
published_at: '2026-06-23T16:07:48'
authors:
- Zhihao Wang
- Jianxiong Li
- Yu Cui
- Yuan Gao
- Xianyuan Zhan
- Junzhi Yu
- Xiao Ma
topics:
- world-models
- robot-value-models
- robot-manipulation
- suboptimal-data
- policy-learning
- video-diffusion
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# World Value Models for Robotic Manipulation

## Summary
## 摘要
WVM 使用预训练视频世界模型，根据视频和语言预测机器人任务进展。论文称，它在专家和次优操作数据上给出更好的价值估计，并用这些估计改进从带噪演示中进行的策略学习。

## 问题
- 机器人价值模型需要判断视频中的任务进展，包括停顿、失败尝试和重试，因为策略学习常使用质量混杂的机器人数据。
- 许多现有价值模型使用在静态或稀疏视觉输入上训练的 VLM 骨干，因此会漏掉判断进展、犹豫和倒退所需的时间线索。
- 现有 VOC 评测主要检查专家轨迹，因此不能测试模型是否能检测次优片段。

## 方法
- WVM 从 Wan2.2-TI2V-5B 出发，这是一个预训练视频世界模型，并加入一个更轻量的价值 DiT 流，用于预测一段逐帧价值。
- 价值流通过非对称 Mixture-of-Transformers 注意力关注视频潜变量：价值 token 读取视频特征，而视频 token 不读取价值 token。
- 它使用流匹配预测价值块上的分布，而不是对每帧回归一个标量价值。
- 训练包括视频协同训练、用于减少捷径使用的前缀随机化，以及通过视频倒放生成上升、平坦和下降的进展模式。
- 论文还引入 Suboptimal-Value-Bench，包含 800 条人工标注轨迹，覆盖 3 种具身形态和 15 个任务，重点关注犹豫和重试行为。

## 结果
- 在 Suboptimal-Value-Bench 的犹豫片段上，WVM 的平均 Hesitation-RMSE 为 0.05，优于 GVL 和 Robometer 的 0.14、RoboReward 的 0.21、TopReward 的 0.31、Robo-Dopamine 的 0.49，以及 VLAC 的 0.51。
- 在重试片段上，WVM 的平均 Retry-VOC 为 0.78，相比之下 GVL 为 0.62，TopReward 为 0.00，Robometer 为 -0.16，VLAC 为 -0.37。
- 在专家演示上，WVM 的平均 VOC 为 0.95，相比之下 RoboReward 为 0.88，Robo-Dopamine 为 0.82，Robometer 为 0.81，GVL 为 0.78，VLAC 为 0.59，TopReward 为 0.42。
- 数据集级别的专家 VOC 结果包括：WVM 在 OXE 上为 0.94，在 RoboCOIN 上为 0.95，在 EgoDex 上为 0.92，在自采集数据上为 0.99。
- 消融实验显示，完整 WVM 在次优数据上优于变体：去除视频协同训练后，Hesitation-RMSE 从 0.05 变为 0.08，Retry-VOC 从 0.78 变为 0.68；冻结视频流得到 0.12 RMSE 和 0.45 Retry-VOC。
- 对于下游策略学习，WVM 引导的 AWR 和过滤式 BC 在 3 个 RoboSuite 任务和 3 个真实 AgileX 任务上优于普通 BC；每个仿真任务只使用 10 条次优轨迹，每个真实任务使用 50 条；摘录未给出具体成功率数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.24742v1](https://arxiv.org/abs/2606.24742v1)
