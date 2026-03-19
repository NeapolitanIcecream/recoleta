---
source: arxiv
url: http://arxiv.org/abs/2603.05117v2
published_at: '2026-03-05T12:42:53'
authors:
- Youqiang Gui
- Yuxuan Zhou
- Shen Cheng
- Xinyang Yuan
- Haoqiang Fan
- Peng Cheng
- Shuaicheng Liu
topics:
- robot-manipulation
- diffusion-policy
- imitation-learning
- temporal-attention
- long-horizon-control
relevance_score: 0.31
run_id: materialize-outputs
language_code: zh-CN
---

# SeedPolicy: Horizon Scaling via Self-Evolving Diffusion Policy for Robot Manipulation

## Summary
SeedPolicy针对扩散式模仿学习在长时域机器人操作中“看得更久反而更差”的问题，提出了可递归更新历史状态的时序模块SEGA。它把长历史压缩成固定大小的潜状态，并用注意力生成的门控过滤无关帧，从而让扩散策略随观察时域增长而持续受益。

## Problem
- 现有Diffusion Policy虽然能建模多模态专家行为，但观察历史一变长，性能反而下降，限制了长时程操作。
- 直接堆叠图像帧不能有效建模复杂时间依赖；而标准时序注意力又会随时域长度带来二次方计算开销。
- 机器人视觉流里存在大量时间稀疏且无关的信息（背景变化、遮挡、噪声），若全部写入历史会污染决策。

## Approach
- 提出**SEGA (Self-Evolving Gated Attention)**：维护一个固定大小、随时间演化的潜在状态，用它来压缩长期历史，而不是无限堆叠原始帧。
- 在**状态更新流**中，上一时刻状态作为Query，从当前观测中提取相关信息，得到中间新状态。
- 用交叉注意力分数直接生成**Self-Evolving Gate (SEG)**，决定“该写入多少新信息、保留多少旧状态”，从而抑制无关时间噪声。
- 在**状态检索流**中，当前观测反向查询历史状态，得到增强观测特征，再交给扩散动作专家预测未来14-DoF动作序列。
- 将SEGA集成到Diffusion Policy中形成**SeedPolicy**，以较温和的额外开销实现可扩展的长时域建模。

## Results
- 在RoboTwin 2.0的**50个操作任务**上，SeedPolicy优于DP和其他IL基线；训练设置为每任务**50条示范、600 epochs、100次rollout测试、3次独立试验取均值**。
- 表1中，**Easy**设置下：DP-Transformer **33.10%** → SeedPolicy-Transformer **40.08%**（**+6.98**个点，约**+21.1%**相对提升）；DP-CNN **28.04%** → SeedPolicy-CNN **42.76%**（**+14.72**个点，约**+52.5%**相对提升）。
- **Hard**设置下：DP-Transformer **1.44%** → SeedPolicy-Transformer **4.28%**（**+2.84**个点，约**+197.2%**相对提升）；DP-CNN **0.64%** → SeedPolicy-CNN **1.54%**（**+0.90**个点，约**+140.6%**相对提升）。论文摘要还给出跨CNN与Transformer平均的结论：相对DP在clean下**+36.8%**、在randomized hard下**+169%**。
- 与大模型RDT比较：RDT为**1.2B**参数，SeedPolicy-Transformer仅**33.36M**、SeedPolicy-CNN为**147.26M**；在Easy下SeedPolicy-CNN **42.76%** 高于RDT **34.50%**，但Hard下RDT **13.72%** 仍高于SeedPolicy。
- 任务覆盖面上，SeedPolicy在**45/50**个任务（Transformer）和**44/50**个任务（CNN）上优于或持平基线。
- 长任务收益最明显：按任务长度分组时，短/中/长任务上相对基线的绝对增益分别为Transformer **+2.9/+6.4/+16.0** 个点，CNN **+13.6/+12.9/+21.9** 个点，支持其“时域越长越占优”的核心主张。

## Link
- [http://arxiv.org/abs/2603.05117v2](http://arxiv.org/abs/2603.05117v2)
