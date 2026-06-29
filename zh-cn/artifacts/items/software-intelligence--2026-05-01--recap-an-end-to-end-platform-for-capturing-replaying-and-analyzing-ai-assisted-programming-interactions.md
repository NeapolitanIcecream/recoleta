---
source: arxiv
url: https://arxiv.org/abs/2605.01104v1
published_at: '2026-05-01T21:20:38'
authors:
- Keyu He
- Qianou Ma
- Valerie Chen
- Wayne Chi
- Tongshuang Wu
topics:
- ai-assisted-programming
- code-intelligence
- developer-telemetry
- human-ai-interaction
- programming-education
- session-replay
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# RECAP: An End-to-End Platform for Capturing, Replaying, and Analyzing AI-Assisted Programming Interactions

## Summary
## 摘要
RECAP 是一个开源的 VS Code 平台，用于记录、回放和分析 AI 辅助编程会话。它把 GitHub Copilot 的聊天提示与细粒度代码编辑关联起来，方便研究者查看开发者在真实项目中如何使用 AI。

## 问题
- 仅靠聊天日志和 git 历史，无法看出哪个提示导致了哪次编辑、开发者拒绝了什么、以及工作过程如何随时间变化。
- 现代编码代理可以在长会话中修改多个文件，而普通提交和短期实验会丢掉很多细节。
- 这对需要证据来判断 AI 依赖、调试行为和 AI 辅助对代码影响的教育者和研究者很重要。

## 方法
- 一个 VS Code 扩展记录 Copilot 聊天 JSON 文件和工作区变更的影子 git 历史。
- 影子 git 存储会提交文件保存、创建、删除、重命名，以及未保存的 dirty 快照，采用 5 秒去抖和最长 30 秒间隔。
- 系统在 5 分钟窗口内，用模糊的行级比较，把 Copilot 文本编辑组与后续 git diff 进行匹配，然后把编辑标记为 Copilot、人工、部分匹配、未匹配，或可能来自外部来源。
- 一个网页回放查看器把聊天事件和代码提交合并到一条时间线中，包含文件树、diff 视图、聊天面板和按颜色区分的事件标记。
- 分析模块把提示分成 6 个类别下的 17 个行为编码，按工作会话计算 AI 编辑占比，并对提示嵌入进行聚类。

## 结果
- 在 2026 年春季的一门大学课程部署中，RECAP 从 29 名学生那里捕获了 2,034 个提示，从 41 名学生那里捕获了 8,239 次影子 git 提交，覆盖 406 个工作会话。
- 作业持续 2 周，要求学生扩展 Zulip 中两个基于 LLM 的功能。
- 提示分类结果显示 Explain 占 44%，其中 explain-error 提示单独占 29%；Plan 和 Code 各占 14%，Converse 占 13%，Setup 占 8%，Eval 占 6%。
- 随着后续工作会话推进，AI 编辑占比下降，带权线性拟合 r = -0.222，p < 0.001。
- 回放暴露了具体行为模式，包括一个持续 11 分钟的 TypeError 循环，其中提示 17、20 和 23 反复触发同一个错误，Copilot 生成的修复又把问题带回原处。
- 论文把这次部署作为平台演示，而不是受控结果研究，所以没有声称开发速度、代码质量或学习结果有改善。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.01104v1](https://arxiv.org/abs/2605.01104v1)
