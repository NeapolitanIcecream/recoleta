---
source: arxiv
url: https://arxiv.org/abs/2607.08575v2
published_at: '2026-07-09T15:06:43'
authors:
- Shiyuan Yang
- Borong Zhang
- Jizheng Zhang
- Zhijia Tao
- Junfei Guo
- Donglai Ran
- Xu Bian
- Qingbiao Li
topics:
- vision-language-action
- robot-foundation-model
- generalist-robot-policy
- dexterous-manipulation
- flow-matching
- robot-data-scaling
relevance_score: 0.98
run_id: materialize-outputs
language_code: zh-CN
---

# FabriVLA: A Lightweight Vision-Language-Action Model for Precise Multi-Task Manipulation

## Summary
## 总结
FabriVLA 是一个参数量为 0.89B、用于多任务机器人操作的视觉-语言-动作模型。它结合流匹配动作生成、门控自注意力和中间视觉-语言特征，在没有机器人数据预训练的情况下，在 Meta-World MT50 上达到 90.0% 的分层平均成功率和 92.0% 的 episode 级成功率。

## 问题
- 大型 VLA 模型能够执行通用机器人操作，但需要较高算力，推理成本也可能较高，限制了实际机器人控制。
- 插入、装配、接触驱动和物体定位等精确任务，同时需要语言对齐能力和细致的空间信息。
- 论文旨在构建一个紧凑模型，在不使用数十亿参数规模的 VLA 主干网络和机器人数据预训练的情况下，保持较强的多任务性能。

## 方法
- FabriVLA 使用 1B 规模的 InternVL3.5-1B 主干网络，并保留其中 14 层。模型通过一个包含 2.1M 个参数的投影层，将最后一层与第 6 层融合，使动作头同时获得语义特征和空间特征。
- 流匹配动作头预测长度为 50 步的动作序列，每步包含 24 个动作维度。它从均匀噪声开始，学习将噪声传输到专家动作的速度场。
- 八个 Transformer 模块先对动作 token 使用门控自注意力，再对视觉-语言上下文执行交叉注意力。门控参数从零开始，并在训练过程中逐步打开，使模型通过渐进式优化路径加入动作之间的时间依赖。
- 模型在 2,500 条 Meta-World 演示数据上进行单阶段联合微调，其中 50 个任务各包含 50 条轨迹。预训练主干网络和随机初始化的动作头同时参与微调。

## 结果
- 在 Meta-World MT50 上，FabriVLA 在 500 个评估 episode 中达到 90.0% 的分层平均成功率和 92.0% 的总体 episode 级成功率。各难度层级的得分分别为：简单 95.0%、中等 88.2%、困难 86.7%、非常困难 90.0%。
- FabriVLA 的分层平均成功率为 90.0%，高于 LA4VLA 的 87.5% 和 Evo-Depth 的 84.4%；其参数量为 0.89B，且未使用机器人数据预训练。表中结果来自相应基线论文。
- 加入第 6 层融合后，分层平均成功率从 82.9% 提升至 90.0%，episode 级成功率从 86.8% 提升至 92.0%，分别增加 7.1 和 5.2 个百分点。
- 在受控的 50k 步动作头消融实验中，门控自注意力将分层平均成功率从 48.5% 提升至 57.7%，将 episode 级成功率从 55.4% 提升至 66.9%。与单独使用门控自注意力相比，加入 token 残差头或时间卷积都会降低性能。
- 表现最强的任务组是平面精度与滑动任务，以及关节运动或接触驱动任务，得分均为 95.7%。工具介导的操作表现较弱，得分为 83.3%，说明工具使用和大范围搬运仍然较难。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.08575v2](https://arxiv.org/abs/2607.08575v2)
