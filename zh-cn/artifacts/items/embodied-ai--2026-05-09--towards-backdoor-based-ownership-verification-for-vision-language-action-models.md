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
GuardVLA 是一种用于视觉-语言-动作模型的水印方法，用来验证一个发布后的机器人策略是否在微调后被复制。它先在带有秘密隐写消息的图像上训练模型，再通过替换验证模块来检查水印，而不是改变机器人动作。

## 问题
- VLA 模型训练成本高，开源后又容易被复用，所以模型所有者需要证据证明部署中的模型来自自己的模型。
- 对 VLA 来说，常规的所有权测试效果较弱，因为不同的机器人策略可以用相似的动作轨迹完成同一任务。
- 验证方法必须保留正常任务成功率，并避免触发会导致不安全机器人动作的行为。

## 方法
- 在嵌入水印时，所有者用图像隐写编码器把固定的 6 比特秘密消息加入具身视觉观测，然后在这些输入上微调受保护的 VLA。
- 该方法还会在正常数据上训练一个干净模型，并在带随机消息的图像上训练一个噪声模型，这样验证器可以学习目标水印信号。
- 触发投影器和分类头用二元交叉熵和三元组损失联合训练；干净模型是锚点，噪声模型是正样本，带水印的模型作为负样本被分开。
- 审计时，验证器先在无害模式下检查任务成功率，再替换为触发投影器和分类头，计算水印识别置信度（WIC）。

## 结果
- 在 LIBERO 和 OpenVLA-OFT 上，带水印模型的 WIC 在 Spatial 上为 100.00%，Goal 上为 99.72%，Object 上为 100.00%，LIBERO-10 上为 99.99%；干净模型的 WIC 分别为 0.01%、0.00%、0.60% 和 0.00%。
- 在 LIBERO 和 VLA-Adapter 上，带水印模型在 Spatial、Goal、Object 和 LIBERO-10 上的 WIC 分别为 99.94%、99.85%、100.00% 和 99.90%；干净模型的 WIC 分别为 0.12%、0.50%、0.04% 和 0.01%。
- 在 pi_0.5 上，带水印模型达到 99.85% 的 WIC，而干净模型和噪声模型分别为 0.03% 和 0.01%。
- 无害任务成功率接近干净基线：OpenVLA-OFT 的 Object 从 98.2% 升到 99.4%，VLA-Adapter 的 LIBERO-10 从 89.8% 升到 93.4%，pi_0.5 的 LIBERO-10 从 90.8% 升到 94.2%。
- 从 LIBERO-10 迁移适配到 LIBERO-Spatial 后，SR 稳定在约 99%，WIC 仍接近 100%；把视觉输入减少到单视角后，SR 稳定在约 85% 到 87%，WIC 仍接近 100%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.09005v1](https://arxiv.org/abs/2605.09005v1)
