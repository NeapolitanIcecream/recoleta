---
source: arxiv
url: https://arxiv.org/abs/2606.24453v1
published_at: '2026-06-23T11:41:32'
authors:
- Theodore Papamarkou
- Vladislav Smirnov
- Viktor Mazanov
- Artem Vazhentsev
- Preslav Nakov
- Timothy Baldwin
- Artem Shelmanov
topics:
- coding-agents
- bayesian-control
- code-intelligence
- tool-orchestration
- uncertainty-quantification
- automated-program-repair
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Bayesian control for coding agents

## Summary
## 摘要
本文把编码智能体的编排建模为一个贝叶斯控制问题，核心是判断候选程序是否正确。主要结论是：当验证成本高、较便宜的评审器能提供有用但不完美的信号时，基于后验概率的工具使用最有帮助。

## 问题
- 编码智能体必须选择何时生成代码、运行低成本诊断、细化代码、调用高成本验证器，或停止。
- 固定策略例如始终验证、best-of-N 采样、单一评审器门控，以及固定的生成-评审-再生成循环，不会跟踪候选代码正确性的 uncertainty。
- 这个问题很重要，因为在 CI、SWE-Bench 式设置或其他慢速测试环境中，验证器调用可能占据主要成本。

## 方法
- 该方法维护一个信念分数 b = P(Y = 1 | evidence)，其中 Y 表示当前候选代码会通过 oracle 验证器。
- 语法检查、公开测试和 LLM judge 等低成本评审器使用校准后的似然 P(z | Y)，通过贝叶斯规则更新信念。
- 生成器调用会根据测得的修复概率和破坏概率移动信念，即 P(fix | broken) 和 P(break | correct)。
- 控制器比较各个动作的期望效用：调用评审器、重新生成、验证，或停止。效用等于正确解的奖励减去工具成本。
- 论文实现了一个单步贝叶斯贪心控制器，以及一个有限时域动态规划控制器；后者在 51 点信念网格上使用 horizon H = 3。

## 结果
- 评估覆盖 6 个生成器和 9 个编码基准，任务包括函数级合成、仓库级补丁生成和缺陷修复。
- 在不同的生成器-基准组合中，初始通过率先验从 0.05 到 0.96，覆盖低成功率和高成功率设置。
- 机制分析汇总了 P(Y = 1) 和 C_ver/R 上的 7,020 个扫描点。结果显示，贝叶斯策略主要在验证成本高时胜出，尤其是在 C_ver/R ≳ 1 附近。
- 在论文报告的成本设置中，慢 oracle 机制使用 C_ver = 90、C_syn = 1、C_test = 2、C_llm = 5、C_gen = 10、R = 100。快 oracle 机制使用 C_ver = 5，评审器成本为 1。
- 摘录没有提供完整的数值效用增益表。最强的具体结论是：在低先验、高验证器成本且评审器信息有效的机制下，贝叶斯控制优于固定策略；当公开测试能很好预测隐藏测试、先验较高或验证成本较低时，public-test gating 或 always_verify 会胜出。
- 论文还声称，后验信念比 token probability 和原始工具成功率基线更适合作为 uncertainty score，但摘录没有包含校准指标。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.24453v1](https://arxiv.org/abs/2606.24453v1)
