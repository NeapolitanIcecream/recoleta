---
source: arxiv
url: https://arxiv.org/abs/2605.02431v1
published_at: '2026-05-04T10:30:33'
authors:
- Minnan Wei
- Xiang Chen
- Xiaoshuai Niu
- Siyu Chen
topics:
- code-generation
- competitive-programming
- mcts
- llm-agents
- code-repair
- software-engineering
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# ARIADNE: Agentic Reward-Informed Adaptive Decision Exploration via Blackboard-Driven MCTS for Competitive Program Generation

## Summary
## 摘要
ARIADNE 是一个基于 LLM 的竞赛编程系统，在固定搜索预算下使用 MCTS 和共享黑板来规划、测试和修复代码。它在 APPS、CodeContests、CodeContests+、LiveCodeBench 以及两个近期比赛集合上的 Pass@1 高于智能体编码基线。

## 问题
- 它针对竞赛题中不可靠的一次性程序生成：模型必须选择正确算法，满足时间和内存限制，并处理隐藏边界情况。
- 这个问题很重要，因为很小的策略错误或遗漏的边界情况都可能让生成代码无法通过所有隐藏测试，即使代码看起来合理。
- 以往的智能体流水线、MCTS 代码搜索和黑板协调各自缺少所需循环的一部分：自适应规划、持续保留失败证据，以及预算分配。

## 方法
- ARIADNE 将程序生成视为状态 `(current code, blackboard evidence)` 上的序列决策过程。
- MCTS 在五类动作中选择：策略选择、代码生成、测试生成、质量评估和代码修复。
- 黑板存储解析后的约束、候选策略、生成的测试、反例、诊断信息和修复说明，使后续分支可以复用较早的证据。
- 评估返回标量奖励和结构化反馈。奖励权重为正确性 0.6、性能 0.2、代码结构 0.2。
- UCB 引导的选择和奖励反向传播会把搜索预算转向测试结果更好且修复更有用的分支。

## 结果
- 使用 GPT-4o 时，ARIADNE 报告在 APPS 上的 Pass@1 为 41.30，在 CodeContests 上为 46.67，在 CodeContests+ 上为 27.27，在 LiveCodeBench 上为 20.91。
- 论文称，ARIADNE 比列出的最强基线 CodeSim 最多高出 26.06 个 Pass@1 点。
- 在 2025 ICPC Asia Shenyang Regional Contest 集合上，ARIADNE 报告的 pass@1/3/5 为 3/13、6/13 和 7/13；最佳基准基线为 1/13、4/13 和 5/13。
- 在 2025 CCPC Fujian Invitational 集合上，ARIADNE 报告的 pass@1/3/5 为 4/13、5/13 和 7/13；对比结果为 2/13、2/13 和 5/13。
- 摘录还称 DeepSeek-V3.2 带来了进一步提升，但没有提供 DeepSeek-V3.2 的准确分数。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.02431v1](https://arxiv.org/abs/2605.02431v1)
