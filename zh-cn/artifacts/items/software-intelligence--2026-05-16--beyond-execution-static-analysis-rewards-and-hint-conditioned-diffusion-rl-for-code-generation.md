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
本文研究在单元测试奖励过于稀疏、难以指导学习时，扩散代码模型的 RL 后训练。研究发现，基于 Pylint 的静态检查和适度的训练期提示可以提升 DiffuCoder 在 HumanEval 和 LiveCodeBench 上的表现，同时降低 rollout 成本。

## 问题
- 用于代码生成的扩散语言模型在 RL 期间可能进入低奖励区间：大多数采样程序无法通过单元测试，因此语义奖励接近零，策略更新得到的有用信号很少。
- 单元测试执行也会增加 rollout 成本；RL 会为每个提示采样多个程序，因此这一成本很重要。
- 论文研究在 HumanEval、MBPP 和 LiveCodeBench 上，哪些奖励信号和训练提示在不同任务难度下效果最好。

## 方法
- 研究比较了五种独立奖励：格式提取、语法解析、Pylint 静态检查、参考解相似度，以及语义单元测试通过率。
- 静态检查不运行代码也能给出分级反馈，使用 Pylint 对错误、警告、未定义名称、不可达代码、未使用变量及相关问题的评分。
- 提示条件扩散采样只在 RL 训练期间展示部分参考解 token；评估时不使用提示。
- 研究测试了从左到右提示、随机 token 提示和基于 AST 的提示，提示比例包括 0.25、0.5 和 0.75。
- 实验使用 DiffuCoder 和 Dream-Coder 7B SFT checkpoint、AceCode-87K 进行 RL 训练，并采用 all-of-3 评估协议，即三个采样解都必须通过。

## 结果
- 在 DiffuCoder 上，静态检查相较语义奖励将 HumanEval 从 53.9 提升到 67.1，将 MBPP 从 60.8 提升到 61.7，将 LiveCodeBench 从 14.9 提升到 15.5。
- 静态检查将 DiffuCoder 的 rollout 时间从 29.3 秒降到 26.5 秒，减少 9.4%，原因是避免了重复执行测试。
- 在 Dream-Coder 上，静态检查在 HumanEval 上达到 70.9，语义奖励为 69.1；相似度奖励在 MBPP 上达到 62.5，语义奖励为 61.9；LiveCodeBench 仍然较弱，语义奖励为 3.6，格式奖励为 8.1。
- 在 DiffuCoder 的语义奖励下，提示将 HumanEval 从无提示的 53.9 提升到 0.5 比例从左到右提示的 68.9；0.25 比例的随机提示在 LiveCodeBench 上达到 16.3，无提示为 14.9。
- 在静态检查下，AST 提示给出了表 4 中最好的 LiveCodeBench 分数：0.5 提示比例下为 16.5，无提示为 15.5。
- 更高的提示比例不一定有帮助：在静态检查配合随机提示时，HumanEval 从 0.25 比例的 67.7 降至 0.5 比例的 40.4 和 0.75 比例的 32.1。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.17174v1](https://arxiv.org/abs/2605.17174v1)
