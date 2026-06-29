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
ARIADNE 是一个基于大语言模型的竞技编程系统，使用 MCTS 和共享黑板，在固定搜索预算下规划、测试并修复代码。它在 APPS、CodeContests、CodeContests+、LiveCodeBench 以及两个最近的竞赛数据集上，Pass@1 都高于现有的 agentic 编码基线。

## 问题
- 它解决的是竞赛题中不稳定的一次性程序生成问题。在这类任务里，模型必须选对算法，满足时间和内存限制，还要处理隐藏边界情况。
- 这个问题很重要，因为哪怕策略有一点偏差，或者漏掉一个边界情况，生成的代码也会在所有隐藏测试上失败，即使表面上看起来可行。
- 以前的 agent 流水线、用于代码搜索的 MCTS，以及黑板式协调，各自都缺了必要闭环中的一部分：自适应规划、持续积累失败证据、以及预算分配。

## 方法
- ARIADNE 把程序生成看作一个关于状态 `(current code, blackboard evidence)` 的顺序决策过程。
- MCTS 在五类动作之间选择：策略选择、代码生成、测试生成、质量评估和代码修复。
- 黑板保存解析后的约束、候选策略、生成的测试、反例、诊断信息和修复记录，后续分支可以复用这些早先证据。
- 评估会返回一个标量奖励和结构化反馈。奖励的权重是：正确性 0.6，性能 0.2，代码结构 0.2。
- 由 UCB 引导的选择和奖励回传，会把搜索预算分配给测试结果更好、修复更有用的分支。

## 结果
- 使用 GPT-4o 时，ARIADNE 在 APPS 上的 Pass@1 为 41.30，在 CodeContests 上为 46.67，在 CodeContests+ 上为 27.27，在 LiveCodeBench 上为 20.91。
- 论文称，ARIADNE 比列出的最强基线 CodeSim 最高高出 26.06 个 Pass@1 点。
- 在 2025 ICPC Asia Shenyang Regional Contest 数据集上，ARIADNE 的 pass@1/3/5 为 3/13、6/13 和 7/13；最佳基线分别为 1/13、4/13 和 5/13。
- 在 2025 CCPC Fujian Invitational 数据集上，ARIADNE 的 pass@1/3/5 为 4/13、5/13 和 7/13；对应的基线为 2/13、2/13 和 5/13。
- 摘要还提到 DeepSeek-V3.2 有进一步提升，但没有给出 DeepSeek-V3.2 的具体分数。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.02431v1](https://arxiv.org/abs/2605.02431v1)
