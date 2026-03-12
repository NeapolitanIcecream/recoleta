---
source: arxiv
url: http://arxiv.org/abs/2603.05438v1
published_at: '2026-03-05T18:00:02'
authors:
- Dongwon Kim
- Gawon Seo
- Jinsung Lee
- Minsu Cho
- Suha Kwak
topics:
- world-model
- latent-tokenizer
- planning
- model-predictive-control
- robotics
- discrete-latents
relevance_score: 0.94
run_id: materialize-outputs
---

# Planning in 8 Tokens: A Compact Discrete Tokenizer for Latent World Model

## Summary
本文提出 CompACT，一种把每张图像压缩到仅 8 个离散 token 的紧凑 tokenizer，用于加速潜在世界模型中的规划。核心主张是：规划不需要高保真像素细节，只需保留与动作决策相关的语义与空间信息。

## Problem
- 现有世界模型常把单帧编码成数百个 token，导致基于注意力的规划计算量随 token 数平方增长，难以实时控制。
- 许多生成式世界模型追求照片级重建，保留了纹理、光照等对规划并不关键的高频细节，造成不必要的表示冗余。
- 这很重要，因为若规划延迟过高，世界模型即使预测能力强，也难以用于真实机器人或导航系统的在线决策。

## Approach
- 提出 **CompACT**：将每张图像编码为 **16 或 8 个离散 token**，其中 8-token 设定约为 **128 bits/image**（8 个 token × 16 bits）。
- 编码器不再端到端为重建训练，而是建立在**冻结的 DINOv3 视觉编码器**之上；用少量可学习 query 通过 cross-attention 从其特征中提取对象级语义和空间关系，再经离散量化得到紧凑 token。
- 解码器不直接从 8/16 个 token 重建像素，而是把它们作为条件，去**生成预训练 VQGAN/MaskGIT 的高维 target token**，再由目标解码器恢复图像；简单说，就是“紧凑 token 保留语义，生成式解码补全外观细节”。
- 在世界模型训练中，作者直接在这组超紧凑离散 token 上学习 **动作条件下一步预测**，并采用 masked generative modeling；规划时结合 MPC/CEM 在潜空间 rollout 搜索动作序列。
- 由于离散 token 可通过 MaskGIT 风格 unmasking 快速预测，避免连续潜变量常见的多步扩散去噪，因此进一步降低推理开销。

## Results
- 在 **RECON** 导航规划中，使用 CompACT 的动作条件世界模型在规划精度上与使用 **784 个连续 token** 的模型**相当**，但**规划延迟约快 40×**。
- 作者声称其 **8-token** 模型优于先前使用 **64-token** 的 tokenizer，说明极端压缩在精心设计下不仅更快，还可能带来更好的规划表现。
- 论文指出 **NWM** 一类现有方法规划一次 episode 最高需 **约 3 分钟**（单张 RTX 6000 ADA GPU），而 CompACT 旨在把这类延迟降到更接近实时可用的水平。
- 在 **RoboNet** 动作条件视频预测中，CompACT 的潜变量可支持**与使用 16× 更多 token 的先前 tokenizer 相当的动作回归性能**，并保持较强动作一致性。
- 文段未给出更完整的表格数值（如 ATE/RPE、APE、IDM 具体绝对值），但最强定量结论是：**8 token vs 784 token 达到相近规划性能，且规划速度提升约 40 倍**。

## Link
- [http://arxiv.org/abs/2603.05438v1](http://arxiv.org/abs/2603.05438v1)
