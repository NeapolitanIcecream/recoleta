---
source: hn
url: https://nlp.elvissaravia.com/p/state-of-the-art-prompting-for-ai
published_at: '2026-03-08T23:52:42'
authors:
- walterbell
topics:
- prompt-engineering
- ai-agents
- agent-workflows
- evals
- meta-prompting
relevance_score: 0.88
run_id: materialize-outputs
---

# State-of-the-Art Prompting for AI Agents (2025)

## Summary
这篇文章不是严格意义上的学术论文，而是一份面向构建 AI agent 的提示工程最佳实践总结。它整理了多种可操作的 prompting 技巧，核心目标是提升 agent 的可靠性、可控性与可调试性。

## Problem
- 要让 AI agent 在真实工作流中稳定执行任务并不容易；如果提示不清晰，模型容易输出不一致、幻觉或错误调用工具。
- 多步骤、工具使用、结构化输出等 agent 场景比普通问答更复杂，因此需要更系统的提示设计方法。
- 这个问题之所以重要，是因为高质量 prompting 直接影响软件自动化、代码智能体和生产级 agent 系统的效果、成本与可信度。

## Approach
- 提倡把 LLM 当作“新员工”来管理：给出**超具体、超详细**的长提示，明确角色、任务、约束和输出格式。
- 使用**角色设定**、**任务拆解**、**分步计划**和**结构化格式**（如 Markdown/XML 标签）来增强模型对指令的理解和输出一致性。
- 借助**few-shot 示例**和**meta-prompting**，让模型基于好/坏案例帮助改写提示，从而迭代优化行为。
- 在多阶段 agent 工作流中使用**动态 prompt folding** 生成更专门的子提示，并加入 **escape hatch**（如“不知道就明确说明”）来减少幻觉。
- 强调**debug 信息/思维痕迹**与**evals**的重要性：前者帮助排查提示问题，后者用于系统性衡量提示质量；同时考虑不同模型“个性”，并通过大模型优化、小模型部署来做蒸馏与成本权衡。

## Results
- 文中**没有提供正式实验、基准数据集或可复现的定量指标**，因此没有可报告的 accuracy、success rate、latency 或成本对比数字。
- 最具体的工程性例子包括：Parahelp 的客服 agent 提示词长度达到 **6+ pages**，并使用 XML 风格标签（如 `<manager_verify>accept</manager_verify>`）约束结构化输出。
- 文中声称这些方法可带来更高的**可靠性**、更好的**可调试性**、更一致的**机器可读输出**，并降低 hallucination 风险，但这些结论主要来自经验总结而非严格实验验证。
- 文章还提出“**evals are your crown jewels**”这一核心主张：相比单条 prompt，本地评测集被认为是 prompt 迭代和 agent 产品化的关键资产。

## Link
- [https://nlp.elvissaravia.com/p/state-of-the-art-prompting-for-ai](https://nlp.elvissaravia.com/p/state-of-the-art-prompting-for-ai)
