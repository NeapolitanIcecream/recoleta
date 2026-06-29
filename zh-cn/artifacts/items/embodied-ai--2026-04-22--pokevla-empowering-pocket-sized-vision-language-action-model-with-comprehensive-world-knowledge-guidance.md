---
source: arxiv
url: http://arxiv.org/abs/2604.20834v2
published_at: '2026-04-22T17:58:19'
authors:
- Yupeng Zheng
- Xiang Li
- Songen Gu
- Yuhang Zheng
- Shuai Tian
- Weize Li
- Linbo Wang
- Senyu Fei
- Pengfei Li
- Yinfeng Gao
- Zebin Xing
- Yilun Chen
- Qichao Zhang
- Haoran Li
- Wenchao Ding
topics:
- vision-language-action
- robot-manipulation
- embodied-foundation-model
- spatial-reasoning
- multi-view-learning
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# PokeVLA: Empowering Pocket-Sized Vision-Language-Action Model with Comprehensive World Knowledge Guidance

## Summary
## 总结
PokeVLA 是一个用于机器人操作的小型视觉-语言-动作模型，它在动作训练前加入了具身世界知识。它的目标是在空间理解、目标感知和鲁棒性上优于轻量级 VLA 基线。

## 问题
- 现有 VLA 模型常把通用视觉-语言特征直接送入动作头，与机器人操作的对齐较弱，这会让学习变得低效且成本更高。
- 预训练的 VLM 知识与机器人任务的匹配还不够，尤其是在空间关系、多视角一致性和面向目标的引导上。
- 这些缺口很重要，因为机器人操作需要准确的物体定位、空间推理，以及在场景变化和扰动下保持稳定行为。

## 方法
- 这个方法分两阶段。第一阶段，它在大约 2.4M 到 2.5M 个多模态样本上预训练一个名为 PokeVLM 的紧凑视觉-语言模型，这些样本覆盖通用 VQA、空间定位、可供性学习和具身推理。
- PokeVLM 使用 Qwen2.5-0.5B 语言模型，以及 SigLIP 和 DINOv2 视觉编码器，所以基础模型保持较小，同时加入了具身视觉-语言知识。
- 在 VLA 后训练期间，模型学习一个特殊的 `<SEG>` token，它从主视角和腕部相机视角预测操作目标的分割掩码。这让策略在不同视角之间共享同一个目标表示。
- 训练时，它把视觉隐藏状态与 3D 几何模型 VGGT 的特征对齐，这样模型可以学习场景结构，而不需要在推理时使用几何模型。
- 带有可学习动作查询的动作头收集语言、视觉、分割、几何和机器人状态特征，并把它们送入动作专家来预测动作。

## 结果
- 在 LIBERO-Plus 上，当使用 LIBERO-Plus 数据集训练时，PokeVLA 的总成功率比 OpenVLA-OFT 高 **4.0%**，比 VLA-Adapter 高 **2.5%**。
- 在只用原始 LIBERO 训练、并在 LIBERO-Plus 变体和扰动上测试的迁移设置中，PokeVLA 的平均成功率比 OpenVLA-OFT 高 **9.7%**，比 VLA-Adapter 高 **20.2%**。
- 在带有空间和颜色引用的真实世界任务中，它报告的成功率比相近规模的基线高 **12.5%**。
- 在真实世界扰动下，报告的提升扩大到 **20.0%**，论文把这作为更强鲁棒性的证据。
- 预训练语料包含大约 **2.4M 到 2.5M** 个样本，其中包括 **665K** 个通用样本、**694K** 个定位样本、**553K** 个可供性样本和 **511K** 个推理样本。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.20834v2](http://arxiv.org/abs/2604.20834v2)
