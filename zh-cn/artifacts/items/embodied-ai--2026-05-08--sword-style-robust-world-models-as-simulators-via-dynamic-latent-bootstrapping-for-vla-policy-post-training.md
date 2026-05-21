---
source: arxiv
url: https://arxiv.org/abs/2605.07288v1
published_at: '2026-05-08T05:54:33'
authors:
- Jiaxuan Gao
- Yongjian Guo
- Zhong Guan
- Wen Huang
- Wanlun Ma
- Xi Xiao
- Junwu Xiong
- Sheng Wen
topics:
- vision-language-action
- world-model
- robot-policy-post-training
- sim2real
- robot-data-scaling
- libero
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Sword: Style-Robust World Models as Simulators via Dynamic Latent Bootstrapping for VLA Policy Post-Training

## Summary
## 摘要
Sword 训练了一个基于 Wan、以动作为条件的世界模型，用于 LIBERO 操作 rollout；在风格变化和长时间自回归使用下仍能保持稳定。它面向 VLA 策略后训练，使想象 rollout 更接近真实数据集中的视觉表现和动作条件行为。

## 问题
- WoVR 等现有学习型模拟器在 LIBERO 的初始状态视觉变化下会失效，包括光照、饱和度、背景、桌面和机器人手臂颜色变化。
- Teacher forcing 在训练时使用真实上下文帧，而推理时使用模型自己生成的帧；这种不匹配会在长 rollout 中造成误差累积。
- 这个问题很重要，因为 VLA 策略的 RL 后训练需要大量交互，而实体机器人交互成本高。

## 方法
- Sword 使用 Structure-Guided Style Augmentation：Cosmos-Transfer 2.5 改变视觉风格，同时用深度图、分割掩码和任务提示保留场景几何结构和任务语义。
- 世界模型使用 Wan 2.2 TI2V diffusion Transformer 骨干网络，根据当前观测和动作预测未来观测。
- Dynamic Latent Bootstrapping 将模型预测的 VAE latent 存入动态缓存，并在训练过程中逐步用缓存预测替换真实上下文 latent。
- latent 缓存避免存储像素空间展开结果；论文报告称，它将上下文帧存储量从数百 GB 降到 20 GB 以下，在 latent 空间约有 60 倍压缩。
- 推理时，模型使用 4 个上下文帧并预测接下来的 8 帧；每个 episode 的第一帧也作为全局条件，用于保持时间一致性。

## 结果
- 在 LIBERO-Original 上，Sword 在所有报告的生成指标上都优于 WoVR：LPIPS 0.11 对 0.13，FID 18.39 对 22.01，FVD 35.61 对 61.26，FloLPIPS 0.23 对 0.26。
- 在 LIBERO-Mixed 上，使用原始数据加 OOD 风格迁移数据时，Sword 相比 WoVR 的结果为：LPIPS 0.20 对 0.39，FID 32.59 对 119.62，FVD 111.19 对 198.84，FloLPIPS 0.30 对 0.46。
- DLB 消融实验显示 Sword 在 LIBERO 上带来提升：完整 Sword 达到 LPIPS 0.12、FID 18.51、FVD 32.17、FloLPIPS 0.23；不使用 DLB 时为 0.13、20.80、48.46、0.25。
- 在 Mixed 消融设置下，完整 Sword 达到 LPIPS 0.17、FID 28.09、FVD 86.84、FloLPIPS 0.26；不使用 DLB 时为 0.22、37.84、110.71、0.32。
- 论文报告了在 LIBERO-Spatial 上对 OpenVLA-OFT 进行 GRPO 后训练，策略成功率在各训练步数上高于 WoVR，但摘录中没有给出成功率数值。
- 实验使用 1,600 个 rollout episode，每个 512 帧，其中 1,500 个用于训练，100 个用于评估，并报告约 13,000 个 A100 GPU 小时的计算量。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.07288v1](https://arxiv.org/abs/2605.07288v1)
