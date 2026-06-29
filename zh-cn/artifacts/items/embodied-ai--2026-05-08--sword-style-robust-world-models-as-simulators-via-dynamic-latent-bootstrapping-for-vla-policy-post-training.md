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
Sword 训练了一个基于 Wan、带动作条件的世界模型，用于 LIBERO 操作回放，在风格变化和长时间自回归使用下保持稳定。它面向 VLA 策略后训练，让想象中的回放更接近真实数据集里的视觉和动作条件行为。

## 问题
- 现有的学习型模拟器，比如 WoVR，在 LIBERO 中遇到初始状态的视觉变化时会失效，包括光照、饱和度、背景、桌面和机械臂颜色变化。
- 教师强制训练使用真实上下文帧，而推理时使用模型自己生成的帧；这种不匹配会在长回放中造成误差累积。
- 这个问题很重要，因为 VLA 策略的强化学习后训练需要大量交互，而真实机器人交互成本很高。

## 方法
- Sword 使用结构引导的风格增强：Cosmos-Transfer 2.5 改变视觉风格，同时用深度图、分割掩码和任务提示保留场景几何和任务语义。
- 这个世界模型以 Wan 2.2 TI2V 扩散 Transformer 作为骨干，根据当前观测和动作预测未来观测。
- 动态潜变量 bootstrapping 会把模型预测的 VAE 潜变量存入动态缓存，并在训练中逐步用缓存预测替换真实上下文潜变量。
- 这个潜变量缓存避免了像素空间展开存储；论文报告把上下文帧存储从数百 GB 降到 20 GB 以下，在潜空间里压缩约 60 倍。
- 在推理时，模型使用 4 帧上下文并预测接下来的 8 帧；首个回合帧也会作为全局条件，用于保持时间一致性。

## 结果
- 在 LIBERO-Original 上，Sword 在所有报告的生成指标上都优于 WoVR：LPIPS 0.11 对 0.13，FID 18.39 对 22.01，FVD 35.61 对 61.26，FloLPIPS 0.23 对 0.26。
- 在 LIBERO-Mixed 上，使用原始数据加上分布外风格偏移数据时，Sword 相比 WoVR 的结果是 LPIPS 0.20 对 0.39，FID 32.59 对 119.62，FVD 111.19 对 198.84，FloLPIPS 0.30 对 0.46。
- DLB 消融实验显示，Sword 在 LIBERO 上有提升；完整 Sword 达到 LPIPS 0.12、FID 18.51、FVD 32.17、FloLPIPS 0.23，而去掉 DLB 后分别是 0.13、20.80、48.46、0.25。
- 在 Mixed 消融设置下，完整 Sword 达到 LPIPS 0.17、FID 28.09、FVD 86.84、FloLPIPS 0.26，而去掉 DLB 后分别是 0.22、37.84、110.71、0.32。
- 论文报告了在 LIBERO-Spatial 上对 OpenVLA-OFT 进行 GRPO 后训练时，Sword 在各训练步的策略成功率高于 WoVR，但摘录里没有给出成功率数值。
- 实验使用了 1,600 个 512 帧的回放 episode，其中 1,500 个用于训练、100 个用于评估，并报告了大约 13,000 个 A100 GPU 小时的计算量。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.07288v1](https://arxiv.org/abs/2605.07288v1)
