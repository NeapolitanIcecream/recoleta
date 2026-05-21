---
source: arxiv
url: https://arxiv.org/abs/2605.05138v1
published_at: '2026-05-06T17:12:36'
authors:
- Sergey Rodionov
topics:
- coding-agents
- executable-world-models
- arc-agi-3
- model-based-planning
- agent-verification
- code-intelligence
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Executable World Models for ARC-AGI-3 in the Era of Coding Agents

## Summary
## 摘要
这篇论文测试了一个用于 ARC-AGI-3 的编码智能体基线：智能体先为每个游戏编写并检查可执行的 Python 模型，再采取行动。论文报告了有用的公开集结果，但性能差异很大，私有验证集仍未测试。

## 问题
- ARC-AGI-3 智能体必须在没有自然语言说明的新交互式游戏中推断目标和动态规则，而且每个真实动作都可能消耗预算或导致关卡结束。
- 直接试错成本很高，因此智能体需要在消耗环境动作之前测试假设和计划。
- 这个基准有意义，因为人类可以解出这些游戏，而据报告，截至 2026 年 3 月，前沿 AI 系统的得分低于 1%。

## 方法
- 智能体维护一个 Python 世界模型，其中包含状态重建、转移预测、目标检查和规划函数。
- 每次获得新观测后，验证器程序会测试该模型是否能复现先前的状态转移，以及规划器是否能解出已经建模的关卡。
- 提示会要求智能体将代码重构为更简单的共享规则，用作 MDL 式简洁性偏置的实用替代指标。
- 计划执行器先在模型中模拟动作序列，然后在真实游戏中执行，并在每一步后对照观测帧检查预测帧。
- 控制器是脚本化且游戏通用的：它提供提示，处理 GAME_OVER 后的 RESET，并提供模板，但不包含手写的游戏专用逻辑。

## 结果
- 在 25 个公开 ARC-AGI-3 游戏上，智能体完全解出 7 个游戏，按游戏计算的平均 RHAE 为 32.58%，中位数 RHAE 为 14.65%。
- 在 25 个游戏中，它有 6 个游戏的平均游戏 RHAE 超过 75%，有 9 个游戏低于 5%。
- 在 29 次记录运行中，包括对部分游戏的重复全新运行，它在 209 个尝试关卡中解出 106 个。
- 最好的一批运行包括：ar25 为 8/8 关且 RHAE 为 100.00%，lp85 为 8/8 且 100.00%，tr87 为 6/6 且 100.00%，sb26 为 8/8 且 92.70%，cd82 为 6/6 且 86.51%，tu93 为 9/9 且 78.33%。
- 不同运行之间的方差很大：cn04 在一次全新运行中得到 62.15% RHAE，在另一次中为 0.01%；g50t 分别得到 21.43% 和 34.03%。
- 公开游戏运行使用 Codex CLI 0.122.0 和 GPT-5.4；每次记录运行的估算 API 成本在 34.08 美元到 620.33 美元之间，且有几次运行因中断而提前结束。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.05138v1](https://arxiv.org/abs/2605.05138v1)
