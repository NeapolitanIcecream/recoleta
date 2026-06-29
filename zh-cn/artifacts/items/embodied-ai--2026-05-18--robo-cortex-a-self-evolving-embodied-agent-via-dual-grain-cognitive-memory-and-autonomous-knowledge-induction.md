---
source: arxiv
url: https://arxiv.org/abs/2605.18729v1
published_at: '2026-05-18T17:52:14'
authors:
- Nga Teng Chan
- Yi Zhang
- Yechi Liu
- Renwen Cui
- Fanhu Zeng
- Zeyuan Ding
- Xiancong Ren
- Zhang Zhang
- Qifeng Chen
- Jian Liu
- Yong Dai
- Xiaozhu Ju
topics:
- embodied-navigation
- world-model-planning
- robot-memory
- self-improving-agents
- vision-language-agents
- heuristic-induction
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# Robo-Cortex: A Self-Evolving Embodied Agent via Dual-Grain Cognitive Memory and Autonomous Knowledge Induction

## Summary
## 总结
Robo-Cortex 是一个具身导航智能体，它把过去的导航回合转成可复用的自然语言启发式，供后续规划使用。它结合了短时域世界模型规划、短期反思、长期记忆和在线启发式归纳。

## 问题
- 这篇论文针对未见过或部分可观测环境中的导航，这类环境要求智能体在不确定条件下使用视觉输入、目标、空间上下文和动作结果。
- 以往的导航智能体常常保留地图、轨迹或局部记忆，但论文认为它们没有可靠地把过去回合转成可复用的决策规则。
- 这对真实机器人很重要，因为重复失败、绕路和成功的搜索模式应该在不重新训练整个模型的情况下改善后续行为。

## 方法
- 在每一步，Robo-Cortex 先提出候选动作或子任务计划，再用世界模型预测短期未来的视觉结果，然后让视觉-语言评估器选择预期目标进展最好的候选项。
- 短期反思记忆会总结最近一个滑动窗口内的子任务，包括进展和失败模式，然后把这段总结反馈到下一轮规划中。
- 长期原则记忆会存储回合和子任务图，再通过以目标为条件的状态嵌入检索相关的过往经验以及成功或失败原则。
- Autonomous Knowledge Induction 会把存储轨迹中的反复出现的成功和失败模式提取到 Navigation Heuristic Library 中，条目包含模式 ID、问题描述、推荐策略、置信度分数以及成功/失败标签。
- Robo-Cortex++ 会在推理期间持续更新启发式库，而静态 Robo-Cortex 变体在评估时使用固定的记忆和启发式。

## 结果
- 在 IGNav 上，Robo-Cortex 的 SR 从 World-In-World 的 38.57 提高到 41.26，SPL 从 27.50 提高到 31.66。Robo-Cortex++ 达到 45.07 SR 和 35.06 SPL。
- 在 AR 上，Robo-Cortex 的 SR 从 World-In-World 的 20.68 提高到 22.39，Robo-Cortex++ 达到 23.88。平均轨迹长度方面，Robo-Cortex 为 6.97，World-In-World 为 7.09。
- 在 AEQA 上，Robo-Cortex 的回答分数从 World-In-World 的 27.19 提高到 29.78，Robo-Cortex++ 达到 30.59。Robo-Cortex++ 的 SPL 也达到 25.57，高于 WMNav 给出的最佳基线值 23.60。
- 在已见划分上的记忆累积研究中，到第 3 轮时，加入 LPM 和 SRM 后，IGNav 的 SR 从 Basic Pipeline 的 36.11、SPL 的 28.16 提高到 44.29 和 34.74。
- 在启发式迁移表中，迁移后的启发式把 IGNav 的 SPL 从 Basic Pipeline 的 24.03 提高到 39.33，增加 15.30，同时把 IGNav 的 SR 从 34.72 提高到 48.61。
- 摘要说初步的真实机器人实验支持这种方法，但没有给出真实场景下的成功率或轨迹指标。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.18729v1](https://arxiv.org/abs/2605.18729v1)
