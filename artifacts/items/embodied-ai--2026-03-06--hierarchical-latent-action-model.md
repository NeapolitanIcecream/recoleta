---
source: arxiv
url: http://arxiv.org/abs/2603.05815v1
published_at: '2026-03-06T01:59:07'
authors:
- Hanjung Kim
- Lerrel Pinto
- Seon Joo Kim
topics:
- latent-action-model
- hierarchical-policy
- skill-discovery
- actionless-video
- robot-learning
relevance_score: 0.91
run_id: materialize-outputs
---

# Hierarchical Latent Action Model

## Summary
HiLAM 旨在从**无动作标注视频**中学习更长时程的潜在技能，而不只是在相邻帧之间恢复低层动作。它把已有潜在动作模型提取出的短期动作序列，再分块压缩成可变长度的高层技能，用于分层机器人策略预训练。

## Problem
- 现有 Latent Action Model（LAM）大多只建模**短时帧转换**，能抓住低层运动，但常忽略视频里更重要的**长时程技能结构**。
- 这很重要，因为机器人与世界模型训练需要大量数据，而**带动作标签的数据昂贵且稀缺**；无标签视频很多，但若只能提取短期运动，就浪费了其中的高层行为信息。
- 以固定窗口、固定技能集合或仅靠语言来定义技能的方法，难以处理**真实技能时长可变、执行速度不同、行为多样**的问题。

## Approach
- 核心思路很简单：先用**预训练的逆动力学模型（IDM）**把无动作视频变成一串低层潜在动作，再让一个**分层序列模型**把这串动作自动切成若干段，每段对应一个高层潜在技能。
- HiLAM 采用 **H-Net 的 dynamic chunking**：若相邻 token 特征差异大，就在该位置开新段；这样可**自动发现技能边界**，无需人工标注，也不要求固定技能长度。
- 训练时做三件事：预测下一个潜在动作（latent next-token prediction）、用**预训练前向动力学模型（FDM）**根据预测动作重建未来帧以保持“动作性”、再加上 chunk ratio 正则避免退化分段。
- 学到技能后，作者训练一个**分层策略**：高层策略根据当前观测和语言预测潜在技能，低层策略再根据观测和该技能预测低层动作；最后只微调低层策略去输出真实机器人动作。
- 该设计复用已有 LAM 作为低层提取器，因此在计算上更适合处理**长时程轨迹**。

## Results
- 在 **LIBERO-Long** 上做数据效率实验时，仅用 **10%** 专家演示微调，**BAKU = 23%** 成功率，而 **HiLAM = 45%**，几乎翻倍。
- 在 **LIBERO-Long** 上，用 **50%** 演示时，**HiLAM = 84%**，达到与 **BAKU 用 100% 数据**相当的水平；用 **100%** 演示时，**HiLAM = 94%**，显著高于 BAKU。
- 论文声称在 **LIBERO-Spatial / Object / Goal / Long** 四个套件上都**一致优于**强基线 **BAKU**，但 excerpt 未给出这四个套件各自的完整数值表。
- **Table 1** 的 LIBERO-Long 消融显示：最佳设置是**人类视频预训练 + stage-2 latent skill + stage-0 latent action**，成功率 **0.94**；对应 **BAKU + human pretraining + z^0 latent action = 0.91**，以及 **HiLAM 无大规模预训练 = 0.67**。
- 机器人视频预训练下，HiLAM 也有效：**z^1 skill + z^0 action = 0.90**，**z^2 skill + z^0 action = 0.90**；说明方法并不依赖单一数据源。
- 非分层的 BAKU 用 latent conditioning 也能提升（如 **0.87 / 0.91**），但仍落后于最佳 HiLAM **0.94**，支持作者关于“**高层技能 + 分层策略**”更有效的主张。

## Link
- [http://arxiv.org/abs/2603.05815v1](http://arxiv.org/abs/2603.05815v1)
