---
source: arxiv
url: https://arxiv.org/abs/2605.06388v1
published_at: '2026-05-07T15:05:26'
authors:
- Nilaksh
- Saurav Jha
- Artem Zholus
- Sarath Chandar
topics:
- robot-world-models
- latent-diffusion
- semantic-latents
- policy-evaluation
- robot-planning
- bridgev2
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# Reconstruction or Semantics? What Makes a Latent Space Useful for Robotic World Models

## Summary
## 摘要
论文发现，用 V-JEPA 2.1、Web-DINO 和 SigLIP 2 的语义潜变量训练机器人扩散世界模型，在规划和策略评估上优于用于像素重建的潜变量。重建型 VAE 能生成较好的像素结果，但对控制有用的信号是潜空间中与动作和任务相关的结构。

## 问题
- 机器人世界模型用于在真实硬件执行前测试动作序列和策略，因此预测需要保留物体状态、接触、几何关系和任务进度。
- 潜扩散世界模型常使用为图像重建训练的 VAE 类潜变量，这类潜变量可能在像素指标上得分较高，却丢失控制所需的信号。
- 论文研究在真实机器人操作数据上，哪种潜空间最适合动作条件潜扩散世界模型。

## 方法
- 作者在 BridgeV2 上训练动作条件 DiT 潜扩散世界模型。BridgeV2 包含约 60K 条 WidowX 250 示范，覆盖 13 个任务族，并带有 RGB 观测、7-DoF 动作和语言指令。
- 他们固定数据集、转移模型、优化器、历史长度和动作条件，只改变编码器、可选适配器和解码器路径。
- 他们将重建编码器 SD3 VAE (D=16)、VA-VAE (D=32) 和 Cosmos (D=16) 与语义编码器 V-JEPA 2.1 (D=1024)、Web-DINO (D=1024) 和 SigLIP 2 (D=1152) 进行比较。
- 对于语义编码器，他们测试原生高维潜变量和使用 S-VAE 压缩到 d=96 的潜变量，并在需要时使用更宽的 DDT 头和按维度调整的噪声调度偏移。
- 评估覆盖视觉保真度、CEM 规划误差、世界模型内的 OpenVLA-7B rollout、OOD 物体和指令测试、逆动力学动作恢复，以及 SOAR 成功分类。

## 结果
- 在 DiT-S 策略 rollout 中，V-JEPA 2.1_96 达到最高的共识成功率 0.362 ± 0.038，高于 VAE 的 0.169 ± 0.030、VA-VAE 的 0.175 ± 0.030 和 Cosmos 的 0.244 ± 0.034。
- SigLIP 2_96 在 OOD 子集中的同分布成功率最高，为 0.625 ± 0.054；干扰物 OOD 成功率也最高，为 0.588 ± 0.055。VAE 在相同指标上分别为 0.375 ± 0.054 和 0.287 ± 0.051。
- CEM 动作恢复更偏向语义潜变量：SigLIP 2 的 k=1 误差最低，为 0.082 ± 0.006；V-JEPA 2.1 的 k=4 误差最低，为 0.424 ± 0.014。VAE 报告的对应数值为 0.111 ± 0.009 和 0.612 ± 0.023。
- 在编码器潜变量上的逆动力学动作恢复中，V-JEPA 2.1 在 k=1 时达到 Pearson r=0.829，在 k=4 时达到 r=0.865；VAE 分别为 r=0.507 和 r=0.478。
- 在生成的世界模型潜变量上，V-JEPA 2.1 在列出的 DiT-S 编码器中保持最高 IDM 相关性，k=1 时 r=0.781，k=4 时 r=0.840；VAE 报告值为 r=0.476 和 r=0.464。
- 在 SOAR 整段视频成功分类上，SigLIP 2 的世界模型潜变量准确率最高，为 0.823，高于 V-JEPA 2.1 的 0.789、Web-DINO 的 0.788、VA-VAE 的 0.744、Cosmos 的 0.723 和 VAE 的 0.716。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.06388v1](https://arxiv.org/abs/2605.06388v1)
