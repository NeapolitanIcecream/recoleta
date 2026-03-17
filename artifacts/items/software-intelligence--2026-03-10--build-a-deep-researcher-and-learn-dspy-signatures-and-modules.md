---
source: hn
url: https://www.cmpnd.ai/blog/learn-dspy-deep-research.html
published_at: '2026-03-10T23:25:11'
authors:
- dbreunig
topics:
- dspy
- deep-research-agent
- llm-orchestration
- tool-use
- agent-workflow
relevance_score: 0.85
run_id: materialize-outputs
---

# Build a deep researcher and learn DSPy Signatures and Modules

## Summary
这是一篇教学型文章，展示如何用 DSPy 从零构建一个“深度研究”代理，并逐步把简单的单步调用演化成更可靠、可控的多阶段研究流水线。核心价值不在提出新算法，而在用 DSPy 的 Signature 与 Module 机制说明如何更快原型化、组合和约束 LLM 代理。

## Problem
- 文章要解决的问题是：如何构建一个能进行网页检索、澄清需求、汇总来源并产出研究报告的深度研究代理，以及如何让这种代理比“单次提示 + 单模型回答”更可靠。
- 这很重要，因为真实研究型代理常会遇到上下文膨胀、引用混乱、遗漏用户关心子主题、事实来源不可审计、成本和时延不可控等工程问题。
- 对面向产品化的 AI 软件开发而言，作者强调仅靠长上下文和强模型不够，需要可分解、可评测、可优化的结构化工作流。

## Approach
- 用 DSPy Signature 声明任务的输入输出，例如 `research_request: str -> report: str`，把“想要什么”与“怎么做”分离，让模型从字段名、类型、文档字符串中推断目标。
- 用 DSPy Module 执行任务：基础版使用 `Predict` 把 Signature 转成提示并抽取结构化输出；增强版使用 `ReAct`，结合 `internet_search` 和 `read_webpage` 两个工具完成“推理 + 工具调用”的网页研究。
- 在研究前加入澄清步骤：先用单独的 Signature/Module 生成澄清问题，再收集用户回答，将问答对作为研究器的新输入，减少对用户意图的误解。
- 将大任务拆成多程序流水线，例如澄清、规划、搜集来源、处理网页、综合写作、标注来源等，以换取预算控制、可并行化、可审计、易评测和易优化等工程收益。
- 文章还强调通过类型约束（如 `list[str]`、定长 `tuple`）和 class-based Signature 的 docstring/字段描述，来更稳地引导模型行为并减少脆弱的手写提示与输出解析。

## Results
- 文中展示了一个最小研究代理可在**2 行核心程序**下工作：定义 Signature 并用 `dspy.Predict` 执行；随后在加入工具后变成可联网的深度研究代理。
- 加入澄清问题的版本据称只需**不到 50 行代码（含注释）**，就能让代理在研究前先询问用户，从而“更不容易误解意图，更可能聚焦用户关心内容”。
- 文中明确给出若需固定澄清问题数量，可用 `tuple[str, str, str]` 生成**3 个**问题；也可把问题数量作为 `int` 输入参数控制输出规模。
- 对工具化研究，作者声称 `ReAct` + 网页搜索/阅读后，报告会“**更详细**、往往也“**更准确**”、并且“**更及时**”，但未提供标准数据集、评价指标或与基线的定量对比。
- 对分解式架构，文章提出可设置**最大子主题数、每个子主题 URL 数、最大搜索次数**等控制项，并支持不同阶段使用不同模型、对 Gatherer/Processor 做并行调用，但这些收益均为设计主张，**没有给出实验数字**。
- 总体上，本文**没有提供正式定量实验结果**；最强的具体结论是：通过 DSPy 的 Signature + Module + 分解式工作流，可以把一个单体研究代理演化为更可靠、可控、可评估、可审计的研究系统。

## Link
- [https://www.cmpnd.ai/blog/learn-dspy-deep-research.html](https://www.cmpnd.ai/blog/learn-dspy-deep-research.html)
