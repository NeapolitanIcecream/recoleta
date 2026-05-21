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
## 概要
RECAP 是一个开源 VS Code 平台，用于记录、回放和分析 AI 辅助编程会话。它把 GitHub Copilot 聊天提示与细粒度代码编辑关联起来，使研究人员可以查看开发者在真实项目中如何使用 AI。

## 问题
- 仅靠聊天日志和 git 历史，无法显示哪个提示导致了哪次编辑、开发者拒绝了什么，或工作如何随时间变化。
- 现代编程代理可以在长会话中编辑多个文件，而普通提交和短期实验室研究会丢失大量细节。
- 这关系到教育者和研究人员，他们需要关于 AI 依赖、调试行为以及 AI 辅助对代码影响的证据。

## 方法
- 一个 VS Code 扩展记录 Copilot 聊天 JSON 文件，以及工作区变更的影子 git 历史。
- 影子 git 存储会提交文件保存、创建、删除、重命名，以及未保存的脏快照；采用 5 秒防抖和 30 秒最大间隔。
- 系统使用模糊的行级比较，在 5 分钟窗口内将 Copilot 文本编辑组与后续 git diff 匹配，然后把编辑标注为 Copilot、人类、部分匹配、未匹配或可能来自外部来源。
- 一个网页回放查看器把聊天事件和代码提交合并到同一条时间线中，包含文件树、diff 视图、聊天面板和按颜色编码的事件标记。
- 分析模块将提示分类为 6 个类别下的 17 种行为代码，按工作会话计算 AI 编辑占比，并对提示嵌入进行聚类。

## 结果
- 在 2026 年春季一门大学课程的部署中，RECAP 从 29 名学生处捕获了 2,034 条提示，并从 41 名学生处捕获了 8,239 次影子 git 提交，覆盖 406 个工作会话。
- 作业持续 2 周，要求学生扩展 Zulip 中两个基于 LLM 的功能。
- 提示分类结果显示，Explain 占 44%，其中仅 explain-error 提示就占 29%；Plan 和 Code 各占 14%，Converse 占 13%，Setup 占 8%，Eval 占 6%。
- AI 编辑占比在连续工作会话中下降，加权线性拟合结果为 r = -0.222，p < 0.001。
- 回放显示了具体行为模式，包括一个 11 分钟的 TypeError 循环：第 17、20 和 23 条提示重复同一错误，Copilot 生成的修复又回到了原始问题。
- 论文把这次部署作为平台演示，而非受控结果研究，因此没有声称它能提升开发者速度、代码质量或学习结果。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.01104v1](https://arxiv.org/abs/2605.01104v1)
