---
source: arxiv
url: https://arxiv.org/abs/2605.29438v1
published_at: '2026-05-28T06:33:05'
authors:
- Ye Li
- Huanan Liu
- Kangye Ji
- Yuan Meng
- Jiajun Fan
- Yuansong Wang
- Shiyu Qin
- Chenglei Wu
- Shu-Tao Xia
- Zhi Wang
topics:
- vision-language-action
- robot-policy-acceleration
- dynamic-compute
- temporal-caching
- reinforcement-learning
- real-time-manipulation
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# ElegantVLA: Learning When to Think for Efficient Vision-Language-Action Models

## Summary
## 摘要
ElegantVLA 通过学习哪些控制步骤需要完整计算、哪些可以复用缓存结果，来加速视觉-语言-行动机器人策略。它保持基础 VLA 模型冻结，只为视觉编码器、LLM 和动作头添加一个小型调度器。

## 问题
- GR00T 和 CogACT 这类 VLA 策略会在每个机器人控制步运行视觉编码器、LLM 和动作生成器，这限制了实时操作。
- 固定的加速规则会在稳定运动时浪费计算，在接触、对齐、抓取、插入或放置等接近关键动作时损害精度。
- 这很重要，因为较低的控制频率会让机器人错过移动中的物体，或在精细操作中反应过慢。

## 方法
- ElegantVLA 在冻结的 VLA 策略上加入了一个学习型调度器。调度器在每一步选择计算模式，而不是修改基础模型权重。
- 对视觉编码器和 LLM，它使用五级模式：完整重算、部分 LLM 重算，或复用缓存的视觉-语言表示若干步。
- 它用来自第一层 LLM 的 CKA 相似度来估计视觉-语言稳定性，将当前隐藏状态与最近一次完整计算的锚点进行比较。
- 对动作头，它使用三级模式：重算全部去噪或精炼步骤、复用中间步骤，或在第一次精炼后复用全部步骤。
- 调度器用 Maskable PPO 训练，输入包括 CKA 相似度、夹爪速度、末端执行器平移速度、末端执行器旋转速度和回合进度。

## 结果
- 在 SimplerEnv 上的 GR00T 中，ElegantVLA 将总体成功率从 64.00% 提高到 65.88%，并报告平均 FLOPs 加速最高达 2.55×。
- 在 SimplerEnv 的 GR00T Google Robot 任务中，平均成功率为 75.00%，加速为 2.35×；GR00T 的对应结果是 71.08% 和 1.00×。
- 在 SimplerEnv 的 GR00T WidowX 任务中，平均成功率为 58.07%，加速为 2.55×；GR00T 的对应结果是 57.93% 和 1.00×。
- 在 SimplerEnv 的 CogACT Visual Matching 中，平均成功率为 77.59%，加速为 3.72×；CogACT 的对应结果是 74.80% 和 1.00×。
- 在 SimplerEnv 的 CogACT Variant Aggregation 中，平均成功率为 72.54%，加速为 3.77×；CogACT 的对应结果是 61.30% 和 1.00×。
- 在基于 GR00T 的六项真实世界测试中，它报告计算量减少 2.18×，控制频率从 13.8 Hz 提高到 26.3 Hz，平均成功率从 61.67% 提高到 65.00%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.29438v1](https://arxiv.org/abs/2605.29438v1)
