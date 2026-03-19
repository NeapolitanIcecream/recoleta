---
source: hn
url: https://github.com/AltimateAI/claude-consensus
published_at: '2026-03-05T23:38:46'
authors:
- aaur0
topics:
- multi-agent-review
- code-review
- llm-orchestration
- consensus-synthesis
- developer-tools
relevance_score: 0.04
run_id: materialize-outputs
language_code: zh-CN
---

# Multi-model code review and plan review for Claude Code

## Summary
这是一个为 Claude Code 提供**多模型代码审查与方案审查**的插件：让多个 AI 模型先独立评审，再通过结构化综合与最多两轮收敛形成结论。其价值在于用“多视角 + 共识”替代单模型判断，提升审查稳健性与可解释性。

## Problem
- 该工具要解决的问题是：**单个模型做代码审查或实施方案审查时，容易遗漏问题、判断偏颇或不稳定**。
- 这很重要，因为代码评审和计划评审直接影响**软件质量、缺陷发现、实现风险和开发效率**。
- 它还试图解决多模型协作的工程问题：如何在**不同模型、不同可用性、不同意见**之间得到一个可执行的统一结论。

## Approach
- 核心机制很简单：**让 Claude 和若干外部模型并行、彼此隔离地独立审查同一段代码或同一实现计划**，避免互相污染判断。
- 然后系统进入**结构化综合**阶段，汇总共识点、冲突点和比较表，形成中间结论。
- 接着进行**收敛/审批**阶段，输出 `APPROVE` 或 `CHANGES NEEDED`，最多进行 **2 轮**。
- 工程上支持**可配置 quorum（法定人数）**，默认 **5**；只要达到严格多数响应，就能产出有效结果；若部分模型不可用，只要仍满足 quorum，就会**优雅降级**继续运行。
- 最小可用配置是**Claude + 1 个外部模型**；配置可通过 OpenRouter 或原生 CLI，最多可启用文中提到的 **7 个外部模型**。

## Results
- 文本**没有提供标准基准数据集上的定量实验结果**，也没有报告准确率、缺陷发现率、人工偏好胜率等指标。
- 明确的系统性声明包括：支持**代码审查**与**计划审查**两类任务，并采用 **3 个阶段**流程：独立评审、综合、收敛。
- 收敛机制给出了明确上限：审批阶段**最多 2 轮**，最终输出带归因的结果。
- 鲁棒性方面，默认 **quorum=5**，并要求**严格多数**参与者响应；若部分模型失效，只要 quorum 满足，系统仍可运行。
- 易用性方面，作者声称多数用户只需一句指令即可完成安装；最小配置要求为 **Claude + 1 个外部模型**。
- 从创新点看，最强的具体主张不是性能数字，而是**把多模型独立评审、结构化冲突综合、法定人数机制和审批式收敛**组合成一个可落地的 Claude Code 插件工作流。

## Link
- [https://github.com/AltimateAI/claude-consensus](https://github.com/AltimateAI/claude-consensus)
