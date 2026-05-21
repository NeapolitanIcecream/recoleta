---
source: arxiv
url: https://arxiv.org/abs/2605.12160v1
published_at: '2026-05-12T14:10:54'
authors:
- Joonha Park
- Jiseung Jeong
- Taesik Gong
topics:
- vision-language-action
- generalist-robot-policy
- streaming-instructions
- visual-grounding
- robot-latency
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Premover: Fast Vision-Language-Action Control by Acting Before Instructions Are Complete

## Summary
## 摘要
Premover 让冻结的 VLA 策略在用户仍在输入或说出指令时开始做有用的工作。它加入焦点图和就绪门控，使机器人能够提前行动，同时避免朴素提前执行中出现的成功率崩塌。

## 问题
- 标准 VLA 评测假设完整指令在控制开始前已经可用，因此忽略了用户输入时间。
- 在 LIBERO 上，以 52.24 WPM 输入指令时，输入时间平均占总交互时间的 39%；其中 LIBERO-Spatial 估计为 31.05s 中的 17.69s。
- 过早行动可能会在前缀尚未确定目标时移动到错误物体。

## 方法
- 骨干是冻结的 π₀.₅；可训练部分包括两个 2 层 MLP 投影头和一个标量就绪阈值，参数量不到骨干参数的 1%。
- 图像头和语言头把中间图像 patch 状态与流式前缀 token 状态映射到同一个归一化空间。
- patch-token 余弦得分形成逐 patch 焦点图，并使用模拟器渲染的目标物体分割掩码，通过类别平衡 BCE 进行监督。
- 步骤 t 的焦点图用 floor scale α=0.2 对步骤 t+1 的图像 token 重新加权，使目标 patch 获得更高权重，同时不屏蔽全部上下文。
- 就绪得分等于焦点图 top-10 均值减去全局均值；该得分超过学习到的阈值后，策略开始执行。

## 结果
- 在 LIBERO 上，Premover 将所有 episode 的平均墙钟时间从 34.0s 降至 29.4s，为完整提示基线的 86.4%；成功率为 95.1%，完整提示为 95.0%。
- LIBERO 上的朴素提前移动成功率为 66.4%，平均墙钟时间为 34.5s，因此没有门控的提前执行相比完整提示损失 28.6 个百分点的成功率。
- 使用 Premover 时，LIBERO 各套件墙钟时间分别为 Spatial 22.7s、Object 24.4s、Goal 21.9s、LIBERO-10 48.6s；完整提示分别为 31.0s、30.7s、23.8s、50.8s。
- 在 VLA-arena Level-1 上，Premover 将所有 episode 的墙钟时间从 85.4s 降至 76.6s，为完整提示的 89.7%；平均成功率为 30.9%，完整提示为 33.0%。
- VLA-arena 上各方法成功率都偏弱，包括完整提示和 Premover 在 Long-horizon 上均为 0.0%，因此主要主张的收益是降低延迟，同时平均成功率有小幅损失。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.12160v1](https://arxiv.org/abs/2605.12160v1)
