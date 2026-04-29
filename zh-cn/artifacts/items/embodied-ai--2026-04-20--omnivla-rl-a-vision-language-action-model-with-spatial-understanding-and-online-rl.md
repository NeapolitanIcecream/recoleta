---
source: arxiv
url: http://arxiv.org/abs/2604.17706v2
published_at: '2026-04-20T01:36:58'
authors:
- Haoxiang Jie
- Yaoyuan Yan
- Xiangyu Wei
- Kailin Wang
- Hongjie Yan
- Zhiyou Heng
- Daocheng Chen
topics:
- vision-language-action
- robot-foundation-model
- spatial-understanding
- online-reinforcement-learning
- flow-matching
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# OmniVLA-RL: A Vision-Language-Action Model with Spatial Understanding and Online RL

## Summary
## 概要
OmniVLA-RL 是一个用于机器人操作的视觉-语言-动作模型，加入了显式的 3D 空间建模和在线强化学习。论文称，这种组合提升了动作精度、训练稳定性，以及在 LIBERO 和 LIBERO-Plus 上的基准成功率。

## 问题
- 现有 VLA 模型通常能较好理解语言和图像语义，但会遗漏抓取、放置和避障操作所需的细粒度 3D 空间细节。
- 常见的空间融合设计只在核心模型之前或之后加入 3D 特征，这限制了语言、视觉、空间线索和动作之间的联合推理。
- VLA 模型的强化学习微调很难稳定：PPO 开销较大，因为它需要价值模型；论文则认为，GRPO 在 token 级别应用时可能变得不稳定。

## 方法
- 该模型使用 **Mixture-of-Transformers (MoT)** 主干，在共享的 Transformer 层中包含三个专家：用于视觉-语言理解的 Reasoning Expert、用于 3D 场景特征的 Spatial Expert，以及用于控制生成的 Action Expert。
- Reasoning Expert 使用 **SigLIP** 对多视角 RGB 观测和语言 token 进行编码。Spatial Expert 使用 **VGGT** 提取细粒度空间特征，并在训练时加入一个辅助空间解码器。
- **Block-wise Causal Attention** 掩码将 reasoning 和 spatial token 作为完全可见的前缀，而 action token 构成因果后缀。这样动作生成可以读取场景上下文，同时避免动作噪声干扰场景理解。
- 动作通过对动作块进行 **Conditional Flow Matching** 生成，并以空间、语义和语言特征为条件。
- 对于在线强化学习，论文提出了 **Flow-GSPO**：它将 flow-matching 的动作采样器从确定性的 ODE 转换为随机性的 SDE，然后在动作块级别应用 **GSPO**，以保持探索的随机性，并让优化过程更贴合序列动作。

## 结果
- 在 **LIBERO** 上，论文称平均成功率为 **97.6%**。
- 摘要和引言称，该方法在 **LIBERO** 和 **LIBERO-Plus** 上 **超过了主流现有方法**。
- 论文称，在 **LIBERO-Plus** 上，相比 **PPO** 和 **GRPO** 基线，该方法有更快的 **收敛速度** 和更好的 **最终性能**。
- 给出的摘录 **没有** 包含完整结果表、各任务分数，或除 **LIBERO 上 97.6% 的平均成功率** 之外的精确 PPO/GRPO 对比数字。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.17706v2](http://arxiv.org/abs/2604.17706v2)
