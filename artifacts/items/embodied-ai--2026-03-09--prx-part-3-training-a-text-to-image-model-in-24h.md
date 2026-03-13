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
- token-routing
- perceptual-loss
- low-cost-training
relevance_score: 0.03
run_id: materialize-outputs
---

# PRX Part 3 – Training a Text-to-Image Model in 24h

## Summary
这篇文章展示了一套将多种已验证技巧组合起来的文本到图像扩散训练配方，可在**24小时、32张H200、约1500美元**预算内训练出一个“可用”的512/1024分辨率模型。核心贡献不在提出全新单一算法，而在于证明通过精心工程整合，低成本快速训练高质量扩散模型已经变得可行。

## Problem
- 论文要解决的问题是：**在严格算力和成本约束下，如何从零开始快速训练一个有竞争力的文本到图像模型**。
- 这很重要，因为早期扩散模型训练往往需要极高成本；若能把成本降到**单日、千美元级**，研究和产品迭代门槛会大幅下降。
- 作者还想验证：把此前分开测试过的技巧一起使用时，是否能在**吞吐、收敛速度和最终图像质量**之间得到实际可用的平衡。

## Approach
- 采用**pixel-space x-prediction**，直接在像素空间训练而**不使用VAE**；通过patch size 32和256维初始瓶颈控制token数量，并直接从**512px训练后再微调到1024px**。
- 在标准扩散/flow matching目标之外，加入两种轻量**感知损失**：**LPIPS（权重0.1）**和**DINOv2 perceptual loss（权重0.01）**，并在**所有噪声级别**、基于**整图池化特征**施加监督，以提升视觉质量与收敛。
- 使用**TREAD token routing**降低计算：让**50% token**从第2个block绕过到倒数第二个block，再重新注入；并用**self-guidance**缓解稀疏路由模型在CFG下的质量下降。
- 使用**REPA + DINOv3**做表征对齐，在**第8个transformer block**施加一次对齐损失，权重**0.5**，且只对**未路由token**计算，以保持监督一致性。
- 优化器使用**Muon**（针对2D参数）+ **Adam**（其余参数）；训练数据为约**8.7M**公开合成图文样本，训练日程为**512px 100k steps, batch 1024**，再**1024px 20k steps, batch 512**，并使用**EMA=0.999**进行采样和评估。

## Results
- 最明确的结果是成本与速度：作者在**32×H200**上完成**24小时**训练，总成本约**$1500（按$2/小时/GPU）**。
- 数据规模上，训练使用了约**8.7M**样本：**1.7M Flux generated + 6M FLUX-Reason-6M + 1M midjourney-v6-llava**。
- 分辨率训练策略为**512px阶段100k steps**后接**1024px阶段20k steps**；作者声称1024阶段主要作用是**提升细节锐度而不破坏构图**。
- 文中**没有给出具体定量指标**（如FID/CLIP score/GenEval、明确基线数值对比曲线读数等），因此无法报告严格的数值SOTA或百分比提升。
- 最强的定性结论是：在仅一天训练后，模型已经“**clearly usable**”，具备**较强的prompt following**、**一致的审美表现**，但仍存在**纹理瑕疵、偶发人体结构异常、困难提示词稳定性不足**等问题。
- 作者的核心主张是，当前剩余缺陷更像是**训练不足和数据多样性有限**，而不是训练配方存在根本性结构问题；因此在**更多算力和更广数据覆盖**下，这套方案应能继续稳定提升。

## Link
- [https://huggingface.co/blog/Photoroom/prx-part3](https://huggingface.co/blog/Photoroom/prx-part3)
