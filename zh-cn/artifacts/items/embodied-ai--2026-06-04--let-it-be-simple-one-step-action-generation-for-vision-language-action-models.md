---
source: arxiv
url: https://arxiv.org/abs/2606.05737v1
published_at: '2026-06-04T05:58:30'
authors:
- Yitong Chen
- Shiduo Zhang
- Jingjing Gong
- Xipeng Qiu
topics:
- vision-language-action
- generalist-robot-policy
- diffusion-policy
- robot-data-scaling
- sim2real
- action-generation
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# Let It Be Simple: One-Step Action Generation for Vision-Language-Action Models

## Summary
## 总结
本文认为，当观测、语言和状态条件已经把动作确定得很清楚时，VLA 扩散策略可以在一次推理中生成动作块。把训练时程向高噪声端偏移后，标准流匹配在 LIBERO 系列基准和一个小规模真实机器人检验中，与 10 步解码相当。

## 问题
- 扩散 VLA 策略通常每次动作查询要做 10 步或更多去噪，这会增加机器人控制的延迟。
- 图像生成里的单步扩散方法常常需要教师模型、蒸馏、一致性损失或额外训练阶段；本文认为，紧凑的机器人动作块可能不需要这些机制。
- 这个问题很重要，因为更快的动作解码可以减少控制延迟，同时保留连续动作并避免动作标记化。

## 方法
- 该模型使用条件流匹配和速度预测：采样噪声和一个干净的动作块，在两者之间插值，并训练解码器从带噪动作、时间、图像、语言和机器人状态中预测速度。
- 主要变化是训练时的时间分布：按 t = u / (1 + (alpha - 1)(1 - u)) 把样本移向高噪声端，这样模型能更多在单步解码所用的点附近练习。
- 架构把 SigLIP/PaliGemma 视觉-语言编码器和一个小型 Transformer 动作头配在一起；动作保持连续。
- MNIST 网格到序列任务测试同样的条件-目标形状：一个丰富的视觉条件映射到一个紧凑的序列目标。
- 消融实验改变噪声偏移、动作时域、输入通道和动作损失掩码，测试单步解码在什么条件下成立。

## 结果
- 在标准 LIBERO H10 上，使用小模型时，alpha=4 的单步达到 96.4% 的 Spatial、99.6% 的 Object、96.8% 的 Goal 和 85.2% 的 Long；均匀采样的单步分别是 88.8%、92.8%、90.2% 和 70.2%。
- 在同一标准 LIBERO H10 设置下，均匀的 10 步得到 96.6% 的 Spatial、96.2% 的 Object、93.2% 的 Goal 和 80.8% 的 Long，所以 alpha=4 的单步在 Object、Goal 和 Long 上超过这个基线，在 Spatial 上接近。
- 使用完整编码器时，单步 mask7 达到 97.4% 的 Spatial、98.4% 的 Object、97.8% 的 Goal 和 92.8% 的 Long；完整32的单步达到 98.4%、100.0%、97.0% 和 95.6%。
- 在 LIBERO-Plus 上，18 个可比配置里，单步结果都达到或超过 10 步解码，平均优势是 5.4 个成功百分点。
- 在 LIBERO-Pro 的零样本扰动上，基于标准 LIBERO 检查点，单步平均 44.2%，10 步平均 43.5%；16 个单元里有 14 个的差异不超过 5 个百分点。
- 在真实双臂 YAM RSS 任务上，使用微调后的 pi_0.5 检查点，单步与 10 步基线持平或更好：插入鼠标电池是 80% 对 80%，封住水瓶盖是 60% 对 35%，汉诺塔是 100% 对 50%，每个任务做了 5 次单步试验。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.05737v1](https://arxiv.org/abs/2606.05737v1)
