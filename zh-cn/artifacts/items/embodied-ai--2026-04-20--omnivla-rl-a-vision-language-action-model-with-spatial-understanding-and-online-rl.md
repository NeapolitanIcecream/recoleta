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
## 摘要
OmniVLA-RL 是一个视觉-语言-动作模型，它为机器人操作加入了显式的 3D 空间建模和在线强化学习。论文声称，这种组合提高了动作精度、训练稳定性，以及在 LIBERO 和 LIBERO-Plus 上的基准成功率。

## 问题
- 现有 VLA 模型通常能较好理解语言和图像语义，但缺少抓取、放置和避障操作所需的细粒度 3D 空间信息。
- 常见的空间融合设计只在核心模型前后加入 3D 特征，限制了语言、视觉、空间线索和动作之间的联合推理。
- VLA 模型的 RL 微调很难稳定：PPO 因为需要价值模型而开销较大，论文认为把 GRPO 用在 token 级别时也可能出现不稳定。

## 方法
- 该模型使用 **Mixture-of-Transformers (MoT)** 主干，在共享的 Transformer 层中包含三个专家：Reasoning Expert 负责视觉-语言理解，Spatial Expert 负责 3D 场景特征，Action Expert 负责控制生成。
- Reasoning Expert 使用 **SigLIP** 编码多视角 RGB 观测和语言 token。Spatial Expert 使用 **VGGT** 提取细粒度空间特征，并在训练期间加入一个辅助空间解码器。
- **Block-wise Causal Attention** 掩码把推理和空间 token 视为完全可见的前缀，而动作 token 组成因果后缀。这样，动作生成可以读取场景上下文，同时避免动作噪声污染场景理解。
- 动作通过带有空间、语义和语言特征条件约束的 **Conditional Flow Matching** 在动作块上生成。
- 对于在线 RL，论文提出 **Flow-GSPO**：先把流匹配动作采样器从确定性的 ODE 转为随机 SDE，再在动作块级别应用 **GSPO**，让探索保持随机性，同时让优化更贴近序列动作。

## 结果
- 在 **LIBERO** 上，论文声称平均成功率为 **97.6%**。
- 摘要和引言说，该方法在 **LIBERO** 和 **LIBERO-Plus** 上 **超过了现有主流方法**。
- 论文声称，与 **PPO** 和 **GRPO** 基线相比，它在 **LIBERO-Plus** 上有更好的 **收敛速度** 和 **最终性能**。
- 提供的摘录 **没有** 包含完整结果表、逐任务分数，也没有超过 **LIBERO 上 97.6% 平均成功率** 之外的 **PPO/GRPO** 精确对比数字。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.17706v2](http://arxiv.org/abs/2604.17706v2)
