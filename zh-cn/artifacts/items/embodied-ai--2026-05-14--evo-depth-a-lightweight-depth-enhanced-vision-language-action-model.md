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
## 概要
Evo-Depth 是一个 0.9B 参数的 VLA 模型，它加入从 RGB 提取的深度线索，用于改进需要精确空间控制的机器人操作。论文声称，相比更大的 VLA 基线方法，它在仿真和真实世界中的成功率更高，显存占用更低，推理更快。

## 问题
- 仅使用 2D 表示的 VLA 策略在抓取、放置和物体间交互任务上准确率下降，这些任务需要深度和相对位置。
- 深度相机、点云和大型几何模型会增加硬件、延迟、内存成本，并且对噪声更敏感。
- 论文目标是构建可部署的操作策略，从现有多视角 RGB 相机获取空间线索。

## 方法
- IDEM 读取多视角 RGB 图像，并使用一个 0.13B 的普通 Vision Transformer 提取紧凑的潜在深度特征；该模型初始化自一个任意视角深度编码器。
- IDEM 的早期层在每个相机视角内部做注意力计算；后期层混合同视角和跨视角注意力，使模型能够关联不同视角中的物体。
- 预训练的 InternVL3-1B 视觉语言主干编码图像和指令；论文保留前 14 个语言层用于控制。
- SEM 将 IDEM 深度特征转换为 FiLM 风格的缩放项和偏移项，然后调制视觉语言 token，而不是拼接大型 3D 特征。
- 一个基于流匹配的 Diffusion Transformer 动作专家预测未来动作，并通过三个阶段训练：先训练 SEM/动作专家，再做 IDEM 对齐，最后进行端到端调优。

## 结果
- Meta-World：Evo-Depth 以 0.9B 参数达到 84.4% 平均成功率；Evo-1 报告 0.8B 参数下为 80.6%，RoboTron Mani 报告 4B 参数下为 77.7%。
- VLA-Arena：Evo-Depth 达到 41.1% 总成功率；OpenVLA-OFT 报告 7B 参数下为 39.9%，OpenVLA 报告 7B 参数下为 39.6%，UniVLA 报告 7B 参数下为 38.7%。
- LIBERO：Evo-Depth 在未使用机器人数据预训练的情况下达到 95.4% 平均成功率；UniVLA 报告 7B 参数下为 95.2%，DepthVLA 报告 4.1B 参数下为 94.9%。
- LIBERO-Plus：Evo-Depth 达到 69.6% 平均成功率；列表中排名下一位的基线方法 π0-Fast 报告为 53.6%。
- 真实世界测试：Evo-Depth 报告三个任务的平均成功率为 90%，GPU 显存占用为 3.2 GB，推理频率为 12.3 Hz，并且在对比方法中模型尺寸最小。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.14950v1](https://arxiv.org/abs/2605.14950v1)
