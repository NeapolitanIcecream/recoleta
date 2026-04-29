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
## 摘要
PokeVLA 是一个用于机器人操作的小型视觉-语言-动作模型，它在动作训练前加入了具身世界知识。与轻量级 VLA 基线相比，它的目标是提升空间理解、目标感知和鲁棒性。

## 问题
- 现有 VLA 模型常常把通用的视觉-语言特征直接传给动作头，而这些特征与机器人操作的对齐较弱，这会让学习过程效率低、成本高。
- 预训练 VLM 的知识与机器人任务的匹配度不够，尤其是在空间关系、多视角一致性和目标导向引导方面。
- 这些缺口很重要，因为机器人操作需要准确的目标定位、空间推理，以及在场景变化和扰动下保持稳定行为。

## 方法
- 该方法分为两个阶段。第一阶段，在约 2.4M 到 2.5M 个多模态样本上预训练一个紧凑的视觉-语言模型 PokeVLM，这些样本覆盖通用 VQA、空间定位、可供性学习和具身推理。
- PokeVLM 使用 Qwen2.5-0.5B 语言模型，以及 SigLIP 和 DINOv2 视觉编码器，因此基础模型规模较小，同时加入了具身视觉-语言知识。
- 在 VLA 后训练阶段，模型学习一个特殊的 `<SEG>` token，用来根据基座相机和腕部相机视角预测操作目标的分割掩码。这让策略能够在不同视角之间获得目标的共享表示。
- 训练时，它将视觉隐藏状态与 3D 几何模型 VGGT 的特征对齐，因此模型可以学习场景结构，同时在推理时不需要几何模型。
- 带有可学习动作查询的动作头会汇集语言、视觉、分割、几何和机器人状态特征，并将它们输入动作专家以预测动作。

## 结果
- 在 LIBERO-Plus 上，当使用 LIBERO-Plus 数据集训练时，PokeVLA 的总成功率比 OpenVLA-OFT 高 **4.0%**，比 VLA-Adapter 高 **2.5%**。
- 在迁移设置中，只用原始 LIBERO 训练、在 LIBERO-Plus 变体和扰动上测试时，PokeVLA 的平均成功率比 OpenVLA-OFT 高 **9.7%**，比 VLA-Adapter 高 **20.2%**。
- 在包含空间和颜色指代的真实世界任务中，论文报告其成功率比同规模基线高 **12.5%**。
- 在真实世界扰动下，报告增幅扩大到 **20.0%**，论文将其作为鲁棒性更强的证据。
- 预训练语料大约包含 **2.4M 到 2.5M** 个样本，其中包括 **665K** 个通用样本、**694K** 个定位样本、**553K** 个可供性样本和 **511K** 个推理样本。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.20834v2](http://arxiv.org/abs/2604.20834v2)
