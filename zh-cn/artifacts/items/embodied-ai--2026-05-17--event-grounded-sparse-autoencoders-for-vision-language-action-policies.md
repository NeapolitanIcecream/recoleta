---
source: arxiv
url: https://arxiv.org/abs/2605.17204v1
published_at: '2026-05-17T00:20:17'
authors:
- Xinchen Jin
- Aditya Chatterjee
- Pranav Kumar
- Rohan Paleja
topics:
- vision-language-action
- mechanistic-interpretability
- sparse-autoencoders
- robot-policy
- closed-loop-evaluation
- libero
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Event-Grounded Sparse Autoencoders for Vision-Language-Action Policies

## Summary
## 概要
本文提出了一种事件锚定的 SAE 流水线，用来解释视觉-语言-动作（VLA）策略。它把 SAE 特征和反复出现的机器人事件对应起来，并通过闭环干预来测试这些特征。

## 问题
- VLA 的隐藏状态直接驱动机器人动作，因此内部特征不清楚时，轨迹、接触结果或失败模式都可能不同。
- LLM 和 VLM 的可解释工具无法直接迁移，因为 VLA 的输出是动作，不是可读 token。
- 进行因果验证的成本很高，因为对特征的编辑必须通过闭环机器人 rollout 来判断。

## 方法
- 在闭环 rollout 的逐 token residual stream 激活上训练 BatchTopK 稀疏自编码器。
- 使用 Automatic Waypoint Extraction 从末端执行器轨迹中找出关键帧，把它们当作行为锚点。
- 在每个任务内，结合视觉嵌入、机器人状态和时间进度对关键帧聚类；可选的 VLM 标签会给这些聚类提供简短语义名称。
- 按事件对齐的时间模板、事件窗口均值、任务均值和随机存活对照来给 SAE 特征排序。
- 用保留残差的潜变量编辑测试选出的特征，做法是在保持隐藏状态中 SAE 重建误差的同时，缩放选定的 SAE latent。

## 结果
- 在 LIBERO 上的 OpenVLA 中，原始成功率为 68.0±14.3%；SAE 重建钩子在第 0 层和第 16 层失败，Hooked SR 为 0.0%，在第 24 层达到 0.2±0.5%，在第 31 层达到 34.8±24.5%。
- 在 π_0.5 上，重建钩子保留了行为：PaliGemma backbone 的 Hooked SR 保持在 95.8% 到 97.8% 之间，action expert 保持在 95.8% 到 97.2% 之间。
- 关键帧提取在每次 rollout 中找到大约 3.86 到 6.91 个关键帧。按 50% episode 覆盖率过滤后，每个测试套件中重复出现的事件聚类数量为 35 到 61 个。
- OpenVLA 第 31 层的单特征置零中，事件对齐排序的因果效果最强：基线 SR 为 70.0%，事件对齐 SR 为 48.8%（-21.2 个百分点），窗口均值为 63.8%（-6.2），任务均值为 63.5%（-6.5），随机存活为 68.7%（-1.3）。
- π_0.5 的 PaliGemma backbone 编辑影响较小：列出的最大下降是第 11 层任务均值特征下降 -2.8 个百分点，相比之下该层随机存活只下降 -1.0。
- π_0.5 的 action expert 编辑不稳定：把排名靠前的特征置零时，SR 常常降到 0.0% 到 0.8%；而随机存活特征在更深层会带来较小但非零的下降，例如第 5 层下降 -23.4 个百分点、第 11 层下降 -8.1。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.17204v1](https://arxiv.org/abs/2605.17204v1)
