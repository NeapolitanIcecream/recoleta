---
source: hn
url: https://topicqueue.substack.com/p/xiaomi-opens-a-38b-world-model-built
published_at: '2026-07-16T23:41:36'
authors:
- DISCURSIVE
topics:
- world-model
- robot-data
- robot-foundation-model
- sim2real
- generalist-robot-policy
relevance_score: 0.98
run_id: materialize-outputs
language_code: zh-CN
---

# Xiaomi Opens a 38B World Model Built to Generate Robot Data

## Summary
## 摘要
Xiaomi-Robotics-U0 是一个拥有 380 亿参数的开放式机器人世界模型，用于生成机器人训练数据，而不是直接控制机器人。小米报告称，使用 U0 生成的数据后，π0.5 在陌生真实世界操作任务中的成功率从 36.9% 提升至 63.2%；但这一结果由厂商报告，且基于小米自己的评测。

## 问题
- 机器人策略需要大量且多样化的训练数据，但采集真实世界中的操作示范成本高，这限制了策略在陌生场景和物体上的表现。
- 该论文探讨世界模型能否作为机器人策略的数据生成引擎，而不是直接充当控制器。

## 方法
- Xiaomi-Robotics-U0 是一个单一的 38B 参数模型，用类似图像和视频生成的方法生成机器人场景与视频。
- 生成的场景和视频被用作 π0.5（一种机器人策略）的额外训练数据。
- 小米通过 World Arena 排行榜评估 U0 的具身视频质量，并将其生成场景获得的人类偏好与 GPT-Image-2.0 进行比较。
- 模型权重和代码均已开放，外部用户可以复现这一数据生成流程，并测试其对其他策略或设置的影响。

## 结果
- 在陌生真实世界操作任务中，使用 U0 生成的数据训练后，π0.5 报告的成功率从 36.9% 提升至 63.2%，增加了 26.3 个百分点。
- 小米报告称，U0 在 World Arena 具身视频排行榜上排名第一。
- 据报告，人类评审者更偏好 U0 生成的场景，而不是 GPT-Image-2.0 生成的场景。
- 这些比较结果来自小米自己的评测；摘录没有提供独立复现结果或单独的数据集细节。

## Problem

## Approach

## Results

## Link
- [https://topicqueue.substack.com/p/xiaomi-opens-a-38b-world-model-built](https://topicqueue.substack.com/p/xiaomi-opens-a-38b-world-model-built)
