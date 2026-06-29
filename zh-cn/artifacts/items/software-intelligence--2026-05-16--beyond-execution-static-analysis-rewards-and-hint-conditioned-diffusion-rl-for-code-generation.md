---
source: arxiv
url: https://arxiv.org/abs/2605.17174v1
published_at: '2026-05-16T22:18:04'
authors:
- Shuyin Ouyang
- Zhaozhi Qian
- Faroq AL-Tam
- Muhammad AL-Qurishi
- Jie M. Zhang
topics:
- diffusion-code-models
- rl-for-code
- static-analysis-rewards
- hint-conditioned-sampling
- code-generation
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Beyond Execution: Static-Analysis Rewards and Hint-Conditioned Diffusion RL for Code Generation

## Summary
## 摘要
这篇论文研究了当单元测试奖励过于稀疏、难以指导学习时，如何对扩散式代码模型做 RL 后训练。结果显示，基于 Pylint 的静态检查和适度的训练时提示可以提升 DiffuCoder 在 HumanEval 和 LiveCodeBench 上的表现，同时降低 rollout 成本。

## 问题
- 面向代码的扩散语言模型在 RL 过程中可能进入低奖励区间：大多数采样程序无法通过单元测试，语义奖励接近于零，策略更新拿不到有用信号。
- 单元测试执行也会增加 rollout 成本，因为 RL 每个提示词要采样多个程序。
- 论文要回答的是，在 HumanEval、MBPP 和 LiveCodeBench 上，不同任务难度下，哪些奖励信号和训练提示最有效。

## 方法
- 研究比较了五种独立奖励：格式提取、语法解析、Pylint 静态检查、参考解相似度，以及语义单元测试通过率。
- 静态检查不运行代码，也能给出分级反馈，依据 Pylint 对错误、警告、未定义名称、不可达代码、未使用变量和相关问题的评分。
- 提示条件化的扩散采样只在 RL 训练时暴露部分参考解 token；评估时不使用提示。
- 论文测试了从左到右提示、随机 token 提示和基于 AST 的提示，提示比例包括 0.25、0.5 和 0.75。
- 实验使用 DiffuCoder 和 Dream-Coder 7B 的 SFT 检查点、用于 RL 训练的 AceCode-87K，以及 all-of-3 评估协议，也就是三个采样解都必须通过。

## 结果
- 在 DiffuCoder 上，静态检查相较语义奖励，在 HumanEval 上从 53.9 提升到 67.1，在 MBPP 上从 60.8 提升到 61.7，在 LiveCodeBench 上从 14.9 提升到 15.5。
- 静态检查把 DiffuCoder 的 rollout 时间从 29.3 秒降到 26.5 秒，减少 9.4%，因为它避免了重复执行测试。
- 在 Dream-Coder 上，静态检查在 HumanEval 上达到 70.9，高于语义奖励的 69.1；相似度在 MBPP 上达到 62.5，高于语义奖励的 61.9；LiveCodeBench 仍然较弱，语义奖励为 3.6，格式奖励为 8.1。
- 在 DiffuCoder 的语义奖励设置下，提示把 HumanEval 从没有提示时的 53.9 提升到左到右提示比例 0.5 时的 68.9；随机提示在 0.25 比例下把 LiveCodeBench 提升到 16.3，高于没有提示时的 14.9。
- 在静态检查下，AST 提示在表 4 中给出 LiveCodeBench 的最佳分数：提示比例 0.5 时为 16.5，高于没有提示时的 15.5。
- 更高的提示比例不总是更好：在静态检查加随机提示时，HumanEval 从 0.25 比例下的 67.7 降到 0.5 时的 40.4，再到 0.75 时的 32.1。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.17174v1](https://arxiv.org/abs/2605.17174v1)
