---
source: arxiv
url: https://arxiv.org/abs/2605.14950v1
published_at: '2026-05-14T15:21:36'
authors:
- Tao Lin
- Yuxin Du
- Jiting Liu
- Nuobei Zhu
- Yunhe Li
- Yuqian Fu
- Yinxinyu Chen
- Hongyi Cai
- Zewei Ye
- Bing Cheng
- Kai Ye
- Yiran Mao
- Yilei Zhong
- MingKang Dong
- Junchi Yan
- Gen Li
- Bo Zhao
topics:
- vision-language-action
- robot-manipulation
- implicit-depth
- multi-view-rgb
- generalist-robot-policy
- depth-enhanced-vla
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Evo-Depth: A Lightweight Depth-Enhanced Vision-Language-Action Model

## Summary
## 摘要
Evo-Depth 是一个 9 亿参数的 VLA 模型，它加入了由 RGB 推出的深度线索，用来提升需要精确空间控制的机器人操作。论文声称，它在仿真和真实世界中的成功率都高于更大的 VLA 基线，而且内存占用更低、推理更快。

## 问题
- 只依赖 2D 的 VLA 策略在抓取、放置和物体交互任务上容易失准，这些任务需要深度和相对位置。
- 深度相机、点云和大型几何模型会增加硬件、延迟、显存开销，还更容易受噪声影响。
- 论文要做的是，让现成的多视角 RGB 相机提供空间线索，同时保持策略可部署。

## 方法
- IDEM 读取多视角 RGB 图像，使用一个 1.3 亿参数的纯 Vision Transformer 提取紧凑的潜在深度特征；该模块从一个 any-view 深度编码器初始化。
- IDEM 的前几层在每个相机视角内做注意力，后几层同时混合视角内和跨视角注意力，让模型能把不同视角下的物体对应起来。
- 预训练的 InternVL3-1B 视觉语言骨干编码图像和指令；论文保留前 14 个语言层用于控制。
- SEM 把 IDEM 的深度特征转换成 FiLM 风格的缩放和偏移项，然后用它们调制视觉语言 token，而不是拼接大体积的 3D 特征。
- 一个基于 flow-matching 的 Diffusion Transformer 动作专家预测未来动作，训练分三阶段进行：先训练 SEM/动作专家，再做 IDEM 对齐，最后端到端微调。

## 结果
- Meta-World：Evo-Depth 在 9 亿参数下达到 84.4% 的平均成功率；Evo-1 报告为 80.6%（8 亿参数），RoboTron Mani 为 77.7%（40 亿参数）。
- VLA-Arena：Evo-Depth 达到 41.1% 的总成功率；OpenVLA-OFT 报告为 39.9%（70 亿参数），OpenVLA 为 39.6%（70 亿参数），UniVLA 为 38.7%（70 亿参数）。
- LIBERO：Evo-Depth 在没有机器人数据预训练的情况下达到 95.4% 的平均成功率；UniVLA 报告为 95.2%（70 亿参数），DepthVLA 为 94.9%（41 亿参数）。
- LIBERO-Plus：Evo-Depth 达到 69.6% 的平均成功率；下一个列出的基线 π0-Fast 为 53.6%。
- 真实世界测试：Evo-Depth 在三个任务上的平均成功率为 90%，GPU 显存占用 3.2 GB，推理速度 12.3 Hz，并且在对比方法中模型体积最小。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.14950v1](https://arxiv.org/abs/2605.14950v1)
