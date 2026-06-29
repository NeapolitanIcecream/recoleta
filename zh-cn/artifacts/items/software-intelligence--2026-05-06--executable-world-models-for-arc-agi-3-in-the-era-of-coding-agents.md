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
本文测试了一个用于 ARC-AGI-3 的编码代理基线：它会先为每个游戏编写并检查一个可执行的 Python 模型，再采取行动。结果显示它在公开测试集上有一定效果，但表现波动很大，私有验证集还没有测试。

## 问题
- ARC-AGI-3 代理必须在没有自然语言说明的新交互式游戏中推断目标和动态，而每一次真实动作都可能消耗预算或结束关卡。
- 直接试错成本很高，因此代理需要一种在花费环境动作前测试假设和计划的方法。
- 这个基准很重要，因为人类可以解出这些游戏，而前沿 AI 系统据称在 2026 年 3 月时得分低于 1%。

## 方法
- 代理维护一个 Python 世界模型，包含状态重建、转移预测、目标检查和规划等函数。
- 每得到一次新观察后，验证程序会检查模型是否能复现之前的转移，以及规划器是否能解出已经建模的关卡。
- 代理会被提示将代码重构为更简单的共享规则，这被用作 MDL 风格简单性偏好的实用近似。
- 计划执行器先在模型中模拟一串动作，再在真实游戏中执行，并在每一步后检查预测帧与观察帧是否一致。
- 控制器是脚本化且通用的：它提供提示、在 GAME_OVER 后处理 RESET，并提供模板，但没有手工编写的游戏专用逻辑。

## 结果
- 在 25 个公开 ARC-AGI-3 游戏上，代理完整解出 7 个游戏，按游戏平均的 RHAE 均值为 32.58%，中位数为 14.65%。
- 它在 25 个游戏中的 6 个上达到超过 75% 的平均游戏 RHAE，在 9 个游戏上低于 5%。
- 在 29 次记录运行中，包括部分游戏的重复全新运行，它共解出 209 个尝试关卡中的 106 个。
- 表现最好的运行包括 ar25 的 8/8 关卡和 100.00% RHAE，lp85 的 8/8 和 100.00%，tr87 的 6/6 和 100.00%，sb26 的 8/8 和 92.70%，cd82 的 6/6 和 86.51%，以及 tu93 的 9/9 和 78.33%。
- 不同运行之间的差异很大：cn04 在一次全新运行中的 RHAE 为 62.15%，另一次只有 0.01%；g50t 分别为 21.43% 和 34.03%。
- 公开游戏运行使用 Codex CLI 0.122.0 和 GPT-5.4；估算 API 成本在每次记录运行 34.08 美元到 620.33 美元之间，且有几次运行因中断提前结束。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.05138v1](https://arxiv.org/abs/2605.05138v1)
