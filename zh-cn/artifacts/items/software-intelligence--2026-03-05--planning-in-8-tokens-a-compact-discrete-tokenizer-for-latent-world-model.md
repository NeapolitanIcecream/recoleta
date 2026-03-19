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
- world-models
- discrete-tokenizer
- model-predictive-control
- visual-planning
- latent-representation
relevance_score: 0.35
run_id: materialize-outputs
language_code: zh-CN
---

# Planning in 8 Tokens: A Compact Discrete Tokenizer for Latent World Model

## Summary
CompACT提出一种面向世界模型规划的极致压缩离散图像tokenizer，把每帧观测压到最少8个token，以显著降低决策时规划开销。核心主张是：规划不需要保留照片级细节，只需保留与动作和空间关系相关的语义信息。

## Problem
- 现有世界模型常把一张图编码成数百个token，注意力计算随token数近似二次增长，导致规划过慢、难以实时控制。
- 这很重要，因为世界模型虽然能提升样本效率并支持MPC/决策时规划，但若每次规划都耗时很长，就难以用于机器人、导航等真实系统。
- 论文特别指出，现有导航世界模型可在单个RTX 6000 ADA上每个episode规划耗时**最高约3分钟**，成为部署瓶颈。

## Approach
- 用**CompACT**把每张图压缩到**16或8个离散token**；其中8-token版本约为**128 bits/图像**（8个16-bit token），相比NWM中SD-VAE的**784个token**大幅缩短序列长度。
- 编码端不再为像素重建训练一个普通编码器，而是使用**冻结的DINOv3视觉基础模型**提取语义特征，再用少量可学习query通过**cross-attention resampler**蒸馏出规划关键语义（物体、布局、空间关系）。
- 为避免从极少token直接还原像素的困难，解码端改为**条件生成**：先预测预训练**VQGAN/MaskGIT**目标token（通常**196个token@224×224**），再由其decoder生成图像，把“解压”变成更可行的语义条件生成任务。
- 世界模型直接在这个**极小离散潜空间**中学习动作条件转移，使用**masked generative modeling**预测下一时刻token，从而让MPC rollout只在8/16-token级别进行。
- 由于采用离散token和MaskGIT式并行/非自回归生成，未来状态预测避免了扩散模型常见的数百步去噪，进一步降低规划延迟。

## Results
- 在**RECON**导航规划上，使用CompACT tokenizer训练的动作条件世界模型与使用**784个连续token**的模型相比，达到**可比的规划精度**，同时带来约**40× planning latency加速**。
- 论文声称其**8-token模型优于此前64-token tokenizer**，说明“精心设计的极端压缩”不仅更快，也可能带来更好的规划表现；但摘录中**未给出具体ATE/RPE数值**。
- 在**RoboNet**动作条件视频预测上，CompACT表示可实现与使用**16×更多token**的先前tokenizer**相当的动作回归性能**，并保持较强的动作一致性；但摘录中**未提供具体L1/R²/APE数值**。
- 在表示压缩层面，论文给出最直观的规模对比：**8 token vs 784 token**，以及中间目标tokenizer通常为**196 token**；其核心结论是，规划关键语义可在远少于传统方法的token数中保留。
- 对实时可用性的最强具体主张是：相比现有可达**3分钟/episode**的规划代价，CompACT把世界模型规划推进到更接近实际部署的速度范围。

## Link
- [http://arxiv.org/abs/2603.05438v1](http://arxiv.org/abs/2603.05438v1)
