---
source: arxiv
url: https://arxiv.org/abs/2605.09005v1
published_at: '2026-05-09T15:44:19'
authors:
- Ming Sun
- Rui Wang
- Xingrui Yu
- Lihua Jing
- Hangyu Du
- Zhenglin Wan
- Xu Pan
- Ivor Tsang
topics:
- vision-language-action
- model-watermarking
- ownership-verification
- robot-policy-security
- libero-benchmark
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# Towards Backdoor-Based Ownership Verification for Vision-Language-Action Models

## Summary
## 摘要
GuardVLA 是一种面向视觉-语言-动作模型的水印方法，用于验证发布后的机器人策略在微调后是否被复制。它用带有秘密隐写消息的图像训练模型，然后通过替换后的验证模块检查该水印，而不是通过改变机器人动作来验证。

## 问题
- VLA 模型训练成本高，开源发布后容易被复用，因此所有者需要证据证明某个已部署模型来自其模型。
- 标准所有权测试对 VLA 较弱，因为不同机器人策略可以用相似的动作轨迹完成同一任务。
- 验证方法必须保留正常任务成功率，并避免触发会导致不安全机器人动作的行为。

## 方法
- 在嵌入水印期间，所有者使用图像隐写编码器向具身视觉观测中加入固定的 6 位秘密消息，然后在这些输入上微调受保护的 VLA。
- 该方法还在正常数据上训练一个干净模型，并在带有随机消息的图像上训练一个噪声模型，使验证器能够学习目标水印信号。
- 触发投影器和分类头通过二元交叉熵和三元组损失共同训练；干净模型是锚点，噪声模型是正样本，带水印模型作为负样本被拉开距离。
- 审计时，验证器先在正常模式下检查任务成功率，然后换入触发投影器和分类头来计算水印识别置信度（WIC）。

## 结果
- 在使用 OpenVLA-OFT 的 LIBERO 上，带水印模型的 WIC 在 Spatial、Goal、Object 和 LIBERO-10 上分别为 100.00%、99.72%、100.00% 和 99.99%；干净模型的 WIC 分别为 0.01%、0.00%、0.60% 和 0.00%。
- 在使用 VLA-Adapter 的 LIBERO 上，带水印模型在 Spatial、Goal、Object 和 LIBERO-10 上的 WIC 分别为 99.94%、99.85%、100.00% 和 99.90%；干净模型的 WIC 保持在 0.12%、0.50%、0.04% 和 0.01%。
- 在 pi_0.5 上，带水印模型达到 99.85% WIC，而干净模型和噪声模型分别为 0.03% 和 0.01%。
- 正常成功率接近干净基线：OpenVLA-OFT Object 从 98.2% 升至 99.4%，VLA-Adapter LIBERO-10 从 89.8% 升至 93.4%，pi_0.5 LIBERO-10 从 90.8% 升至 94.2%。
- 从 LIBERO-10 下游适配到 LIBERO-Spatial 后，SR 稳定在约 99%，WIC 保持接近 100%；将视觉输入减少到一个视角后，SR 稳定在约 85%-87%，WIC 保持接近 100%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.09005v1](https://arxiv.org/abs/2605.09005v1)
