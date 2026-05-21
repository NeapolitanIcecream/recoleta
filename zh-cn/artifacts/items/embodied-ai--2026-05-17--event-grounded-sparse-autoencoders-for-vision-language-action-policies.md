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
## 摘要
本文提出一种基于事件的 SAE 流程，用于解释 Vision-Language-Action 策略。该流程把 SAE 特征关联到重复出现的机器人事件，并通过闭环干预测试这些特征。

## 问题
- VLA 隐藏状态会驱动机器人动作，因此不清楚的内部特征可能导致不同的轨迹、接触或失败。
- LLM 和 VLM 的可解释性工具不能直接迁移到 VLA，因为 VLA 输出的是动作，而不是可读 token。
- 因果验证成本高，因为特征编辑必须通过闭环机器人 rollout 来评估。

## 方法
- 在闭环 rollout 产生的逐 token residual-stream 激活上训练 BatchTopK 稀疏自编码器。
- 对末端执行器轨迹使用 Automatic Waypoint Extraction，找出可作为行为锚点的关键帧。
- 在每个任务内使用视觉嵌入、机器人状态和时间进度对关键帧聚类；可选的 VLM 标签为聚类提供简短语义名称。
- 按事件对齐的时间模板、事件窗口均值、任务均值和 random-alive 对照来排序 SAE 特征。
- 用保留残差的潜变量编辑测试选定特征：缩放所选 SAE 潜变量，同时在隐藏状态中保留 SAE 重构误差。

## 结果
- 在 LIBERO 上的 OpenVLA 中，原始成功率为 68.0±14.3%；SAE 重构 hook 在第 0 层和第 16 层失败，Hooked SR 为 0.0%，在第 24 层达到 0.2±0.5%，在第 31 层达到 34.8±24.5%。
- 在 π_0.5 上，重构 hook 保留了行为：PaliGemma backbone 的 Hooked SR 保持在 95.8% 到 97.8% 之间，action expert 保持在 95.8% 到 97.2% 之间。
- 关键帧提取在每个 rollout 中找到约 3.86 到 6.91 个关键帧。经过 50% episode 覆盖率过滤后，每个 suite 的重复事件聚类数量为 35 到 61 个。
- OpenVLA 第 31 层单特征置零显示，事件对齐排序产生最强因果效应：baseline SR 70.0%，event-aligned SR 48.8%（-21.2 个百分点），window-mean 63.8%（-6.2），task-mean 63.5%（-6.5），random-alive 68.7%（-1.3）。
- π_0.5 PaliGemma backbone 编辑影响较小：列出的最大下降是在第 11 层 task-mean 特征上的 -2.8 个百分点，而该层 random-alive 为 -1.0。
- π_0.5 action expert 编辑不稳定：将排名最高的特征置零时，SR 经常降到 0.0% 到 0.8%；random-alive 特征在较深层导致较小但非零的下降，例如第 5 层下降 -23.4 个百分点，第 11 层下降 -8.1 个百分点。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.17204v1](https://arxiv.org/abs/2605.17204v1)
