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
Premover 让冻结的 VLA 策略在用户还在输入或说出指令时就开始做有用的工作。它加入了一个关注图和一个就绪门控，使机器人可以提前行动，同时避免天真早执行带来的成功率崩塌。

## 问题
- 标准 VLA 评估假定控制开始前完整指令已经可用，因此忽略了用户输入时间。
- 在 LIBERO 上，以 52.24 WPM 的输入速度计算，输入指令平均占总交互时间的 39%，其中 LIBERO-Spatial 估计为 31.05s 中的 17.69s。
- 过早行动会在前缀还没有指明目标对象时朝错误对象移动。

## 方法
- 主干网络是冻结的 π₀.₅；可训练部分是两个两层 MLP 投影头和一个标量就绪阈值，占主干参数不到 1%。
- 图像头和语言头把中间图像 patch 状态和流式前缀 token 状态映射到同一个归一化空间。
- patch-token 余弦分数形成按 patch 的关注图，并使用类别平衡 BCE 监督，标签来自仿真器生成的目标对象分割掩码。
- 第 t 步的关注图会在第 t+1 步重加权图像 token，底限缩放 α=0.2，因此目标 patch 会得到更高权重，同时不会压掉所有上下文。
- 就绪分数等于 top-10 关注图均值减去全局均值；当这个分数超过学到的阈值时，策略开始执行。

## 结果
- 在 LIBERO 上，Premover 将所有 episode 的平均墙钟时间从 34.0s 降到 29.4s，相当于完整提示基线的 86.4%，同时成功率保持在 95.1%，完整提示基线为 95.0%。
- LIBERO 上的天真 premoving 成功率只有 66.4%，平均墙钟时间为 34.5s，所以没有门控的提前执行比完整提示少了 28.6 个百分点的成功率。
- Premover 在 LIBERO 各套件上的墙钟时间分别是 Spatial 22.7s、Object 24.4s、Goal 21.9s、LIBERO-10 48.6s；完整提示分别是 31.0s、30.7s、23.8s、50.8s。
- 在 VLA-arena Level-1 上，Premover 将所有 episode 的墙钟时间从 85.4s 降到 76.6s，相当于完整提示的 89.7%，平均成功率为 30.9%，完整提示为 33.0%。
- VLA-arena 上各方法的成功率都不高，包括完整提示和 Premover 在 Long-horizon 上都是 0.0%，所以这里的主要收益是降低延迟，代价是平均成功率小幅下降。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.12160v1](https://arxiv.org/abs/2605.12160v1)
