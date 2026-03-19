---
source: arxiv
url: http://arxiv.org/abs/2603.09701v1
published_at: '2026-03-10T14:12:18'
authors:
- Binquan Zhang
- Li Zhang
- Lin Shi
- Song Wang
- Yuwei Qian
- Linhui Zhao
- Fang Liu
- An Fu
- Yida Ye
topics:
- multi-turn-code-generation
- human-llm-collaboration
- interaction-smells
- multi-agent-framework
- code-intelligence
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# An Empirical Study of Interaction Smells in Multi-Turn Human-LLM Collaborative Code Generation

## Summary
本文研究多轮人机协作编程中的“交互异味”，即虽然最终代码可能可用，但对话过程本身会不断丢上下文、漏要求、破坏已有功能。作者基于真实聊天数据建立首个异味分类体系，并提出一个轻量多智能体缓解框架 InCE。

## Problem
- 现有代码生成评测大多只看最终功能正确性，忽略了多轮协作过程中导致反复返工、打断开发流的隐藏交互问题。
- LLM 在长对话中常出现历史约束遗忘、前后不一致、回滚已完成功能等现象，影响人机协作效率与满意度。
- 缺少基于真实用户日志的系统性研究：到底有哪些典型交互异味、它们有多常见、不同模型是否仍普遍存在。

## Approach
- 从 WildChat 与 LMSYS-Chat-1M 中抽取代码相关对话，合并得到 60,949 条交互；经 LLM 解耦与筛选后得到 66,371 条编程日志，其中 19,507 条为多轮对话。
- 对 378 个多轮真实样本做人工开放式卡片分类，构建交互异味 taxonomy；最终定义 3 个一级类、9 个子类：如 ambiguous-instruction、must-do-omission、partial-functionality-breakdown、code-rollback 等。
- 用 6 个主流 LLM（GPT-4o、DeepSeek-Chat、Gemini 2.5、Qwen2.5-32B、Qwen2.5-72B、Qwen3-235B）在 WildBench 上做定量分析，比较各类异味分布。
- 提出 InCE（Invariant-aware Constraint Evolution）多智能体框架：一个模块提取跨轮“全局不变量/约束”，另一个模块在生成前做异味审计，尽量提前阻止违反历史要求或破坏已有实现。

## Results
- 作者声称建立了首个面向人机协作代码生成的交互异味分类体系，包含 **3** 个一级类别和 **9** 个细分类别。
- 在人工标注样本中，已给出的异味占比包括：**Must-Do Omission 38.35%**、**Incomplete Instruction 4.39%**、**Ambiguous Instruction 3.84%**、**Must-Not Violate 3.22%**；文中还指出 **Must-Do Omit** 与 **Partial Functionality Breakdown** 在各模型中最普遍。
- 数据处理验证方面：对解耦后的 **383** 条样本检查，标注者一致性 **Cohen’s Kappa = 0.87**，总体准确率 **92%**；开放式卡片分类阶段专家平均 **Kappa ≥ 0.78**，学生标注阶段平均 **Kappa = 0.82**。
- 在扩展 WildBench 上，InCE 使 **Task Success Rate 最多提升 6.67%**。
- InCE 还能将关键交互异味（如 **Repetitive Response** 和 **Must-Do Omission**）的发生抑制约 **13.5%**。
- 论文摘要未提供更细的逐模型、逐基准分数表或与某个明确 baseline 的完整数值对比，但核心量化主张是：轻量 InCE 可同时提升任务成功率并显著降低交互异味。

## Link
- [http://arxiv.org/abs/2603.09701v1](http://arxiv.org/abs/2603.09701v1)
