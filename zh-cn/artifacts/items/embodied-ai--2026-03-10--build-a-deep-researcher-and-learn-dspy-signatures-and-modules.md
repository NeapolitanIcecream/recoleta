---
source: hn
url: https://www.cmpnd.ai/blog/learn-dspy-deep-research.html
published_at: '2026-03-10T23:25:11'
authors:
- dbreunig
topics:
- dspy
- research-agent
- react
- tool-using-llm
- workflow-decomposition
relevance_score: 0.12
run_id: materialize-outputs
language_code: zh-CN
---

# Build a deep researcher and learn DSPy Signatures and Modules

## Summary
这是一篇实践型技术文章，演示如何用 DSPy 从零构建“深度研究”代理，并逐步把简单的单步问答扩展为带检索、澄清、规划与合成的多阶段系统。核心价值不在提出新算法，而在用 Signatures 与 Modules 说明如何更快原型化、更易控制和提升可靠性。

## Problem
- 文章要解决的是：如何把一个依赖大模型的“深度研究代理”从简单提示调用，做成可用、可扩展、可维护的研究系统。
- 这很重要，因为单体式长上下文代理容易出现上下文膨胀、引用管理差、漏掉子主题、来源不可审计、成本和时延难控制等问题。
- 对开发者而言，还存在工程难题：手工写提示、解析输出、接工具、做评测与优化都很脆弱且迭代慢。

## Approach
- 用 DSPy **Signature** 先声明“输入是什么、输出是什么”，例如 `research_request -> report`，把任务目标从具体提示词中抽离出来。
- 用 DSPy **Module** 执行这些声明：先用 `Predict` 做最小可用版本，再用 `ReAct` 让模型调用网页搜索与网页读取工具，实现带外部知识的研究代理。
- 增加一个澄清环节：先生成 clarifying questions，再把用户回答作为额外输入传给研究代理，以减少对用户意图的误解。
- 进一步把工作流拆成多步程序，如澄清、规划、收集来源、处理网页、综合写作与注释，从而换取更好的预算控制、评测、并行化、模型路由和可审计性。
- 强调 DSPy 的机制是“声明 what，不手写 how”：靠字段名、类型、docstring、field description 和模块组合来约束 LLM 行为，而不是手工维护脆弱 prompt。

## Results
- 文章没有给出标准学术实验、基准数据集或定量指标，因此**没有可报告的量化结果**。
- 给出的最具体工程结果是：加入网页工具后，报告“更详细、通常更准确、也更及时”，但未提供 accuracy、citation quality 或 task success rate 数字。
- 加入澄清问题后，作者声称系统“更不容易误解用户意图，更可能聚焦用户关心的部分”；实现该版本“不到 50 行代码（含注释）”。
- 文中展示了一个最小例子：`Predict` 版本只依赖模型参数；`ReAct + internet_search + read_webpage` 版本可执行多轮工具调用并最终合成报告。
- 对分解式架构的收益，文章给出的是定性主张：可设置子主题数、每个子主题 URL 数、最大搜索次数；可并行 Gatherer/Processor；可按步骤写 eval；可追踪事实到 URL 来源，但均无量化对比。

## Link
- [https://www.cmpnd.ai/blog/learn-dspy-deep-research.html](https://www.cmpnd.ai/blog/learn-dspy-deep-research.html)
