---
source: hn
url: https://github.com/AltimateAI/claude-consensus
published_at: '2026-03-05T23:38:46'
authors:
- aaur0
topics:
- code-review
- multi-model-consensus
- claude-code
- plan-review
- developer-tools
relevance_score: 0.91
run_id: materialize-outputs
---

# Multi-model code review and plan review for Claude Code

## Summary
这是一个面向 Claude Code 的多模型代码审查与方案审查插件，让多个 AI 模型先独立评审，再通过结构化综合与最多两轮收敛形成共识。它试图提升单一模型审查的不稳定性与偏差问题，并以较低配置门槛支持实际开发工作流。

## Problem
- 解决代码审查和实施方案审查中过度依赖单一模型的问题；单模型可能遗漏缺陷、判断片面或输出不稳定，这会影响软件工程质量。
- 该问题重要，因为代码审查和设计审查直接影响缺陷发现、实现方案质量以及团队对 AI 辅助开发的信任。
- 还要解决多模型协作的工程落地问题：如何在 Claude Code 中以可配置、可降级、可操作的方式组织多个模型共同完成审查。

## Approach
- 核心机制很简单：让 Claude 和多个外部模型**并行独立**审查同一份代码或计划，避免模型彼此污染意见。
- 然后进入**结构化综合**阶段，汇总共识点、冲突点和比较表，形成统一视图。
- 最后进行**收敛/审批**阶段，输出 `APPROVE` 或 `CHANGES NEEDED`，最多进行 2 轮。
- 系统支持可配置仲裁条件，包括启用哪些模型、最小法定人数（quorum）、命令行接入方式，以及运行时不可用模型的优雅降级。
- 最小配置下只需 Claude + 1 个外部模型即可工作，完整配置中 README 提到可从 7 个外部模型中选择启用。

## Results
- 文本**没有提供标准基准测试或定量实验结果**，没有报告在具体数据集、缺陷发现率、准确率、召回率或人工评审时间上的数值提升。
- 给出的最具体机制性结果是：审查流程分为 **3 个阶段**（独立评审、综合、收敛），并且收敛阶段**最多 2 轮**。
- 默认法定人数为 **5**，要求参与者中达到**严格多数响应**才算有效审查；同时支持运行时跳过不可用模型，只要仍满足 quorum。
- 最小可用设置是 **Claude + 1 个外部模型**；配置界面中说明可从 **7 个外部模型**中选择启用。
- 论文/README 的 strongest claim 是：通过多模型独立审查 + 共识综合，能比单模型方式提供更稳健的代码审查与方案审查，但文中未给出量化对比证据。

## Link
- [https://github.com/AltimateAI/claude-consensus](https://github.com/AltimateAI/claude-consensus)
