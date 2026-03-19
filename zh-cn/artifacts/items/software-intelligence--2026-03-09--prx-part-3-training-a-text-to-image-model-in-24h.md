---
source: hn
url: https://huggingface.co/blog/Photoroom/prx-part3
published_at: '2026-03-09T23:17:50'
authors:
- gsky
topics:
- text-to-image
- diffusion-models
- pixel-space-training
- efficient-training
- perceptual-loss
- token-routing
relevance_score: 0.18
run_id: materialize-outputs
language_code: zh-CN
---

# PRX Part 3 – Training a Text-to-Image Model in 24h

## Summary
这篇文章展示了一个务实的扩散模型训练配方：把多种已验证有效的工程技巧组合起来，在 **24 小时、32 张 H200、约 1500 美元** 的预算下训练出一个可用的文生图模型。核心贡献不在提出全新单一算法，而在于证明低成本、短周期下，像素空间训练与多种加速/提质方法可以稳定协同。

## Problem
- 要解决的问题是：**如何在严格算力与预算约束下，快速训练出质量尚可、可实际使用的文本到图像扩散模型**。
- 这很重要，因为早期高质量扩散模型训练通常需要极高成本；若能把成本压到一天和约 1500 美元量级，会显著降低研究与产品化门槛。
- 实际难点在于：既要降低训练开销，又不能让图像质量、提示词跟随能力和高分辨率细节明显崩坏。

## Approach
- **直接在像素空间训练**：采用 x-prediction，不再使用 VAE；通过 patch size 32 和 256 维 bottleneck 控制 token 数，从而可在 512px 起步并再微调到 1024px。
- **加入感知损失**：在主 diffusion/flow matching 目标之外，增加 **LPIPS（权重 0.1）** 和 **DINOv2 感知损失（权重 0.01）**，直接约束预测图像与目标图像在感知特征空间中的接近程度，以提升收敛速度和视觉质量。
- **用 TREAD 做 token routing**：让 **50% tokens** 从第 2 个 block 跳到倒数第 2 个 block，减少计算；同时用 dense vs. routed conditional prediction 的 self-guidance 缓解 routed 模型在 vanilla CFG 下观感变差的问题。
- **用 REPA 做表征对齐**：以 **DINOv3** 作为 teacher，在第 **8 个 transformer block** 施加对齐损失，权重 **0.5**；只在非 routed tokens 上计算，以保持信号一致。
- **优化器与训练配方**：2D 参数使用 **Muon**，其余参数用 Adam；数据集为 **1.7M + 6M + 1M** 三个公开合成数据集；训练日程是 **512px 100k steps（batch 1024）**，再 **1024px 20k steps（batch 512，无 REPA）**，并使用 **EMA=0.999**。

## Results
- 最核心结果是：作者声称在 **32×H200、24 小时、约 1500 美元** 的预算下，训练出了一个“**clearly usable**”的文生图模型，说明低成本快速训练已经可行。
- 定量训练配置方面，模型使用约 **8.7M** 张训练样本（**1.7M + 6M + 1M**），总训练为 **120k steps**，其中 **100k steps@512px**，**20k steps@1024px**。
- 质量层面，作者明确声称模型具有**较强的 prompt following**、**一致的整体美学风格**，且 **1024px 阶段主要提升细节锐度而不破坏构图**。
- 作者也明确指出局限：仍存在**纹理瑕疵、偶发人体结构异常、复杂 prompt 下不稳定**等问题，并将其归因为**训练不足和数据多样性有限**，而非配方本身存在结构性缺陷。
- 文中**没有提供明确的标准 benchmark 数字**（如 FID、CLIP score、GenEval、DrawBench 分数）或与具体 baseline 的量化对比；最强的实证主张是该组合配方在微预算条件下能得到“可用”的 1024 分辨率文生图模型，并可作为后续大规模训练配方基础。

## Link
- [https://huggingface.co/blog/Photoroom/prx-part3](https://huggingface.co/blog/Photoroom/prx-part3)
