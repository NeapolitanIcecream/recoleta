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
- llm-code-generation
- multi-turn-interaction
- human-llm-collaboration
- evaluation-benchmarking
- multi-agent-framework
relevance_score: 0.03
run_id: materialize-outputs
---

# An Empirical Study of Interaction Smells in Multi-Turn Human-LLM Collaborative Code Generation

## Summary
本文研究多轮人机协作代码生成中的“交互异味”，即那些不会直接体现在最终功能正确性上、却会破坏协作过程的隐性问题。作者基于真实对话数据提出首个异味分类体系，并用一个轻量多智能体框架来减少这类问题。

## Problem
- 现有代码生成评测更关注最终代码是否正确，但忽略了多轮协作过程中常见的上下文丢失、历史约束违背和回应退化等过程性问题。
- 这些“交互异味”会让模型在长对话里偏离用户真实意图、破坏之前已实现的功能，导致开发者频繁返工，影响效率与体验。
- 论文要回答：这类异味有哪些、在不同主流LLM上是否普遍存在、以及能否被系统性缓解。

## Approach
- 从 **WildChat** 和 **LMSYS-Chat-1M** 中抽取真实编程相关对话，合并得到 **60,949** 条记录；经解耦与筛选后得到 **66,371** 条编程会话，其中 **19,507** 条为多轮对话。
- 通过对 **378** 个多轮样本进行人工开放式卡片分类，建立“交互异味” taxonomy；论文文字中最终给出 **3** 个一级类别、**9** 个二级类别：**user-intent-quality、historical-instruction-compliance、historical-response-violation**，包括 ambiguous instruction、incomplete instruction、must-do omission、must-not violate、signature mismatch、cross-turn inconsistency、partial functionality breakdown、code rollback、repetitive response。
- 在 **WildBench** 上评估 **6** 个主流模型：GPT-4o、DeepSeek-Chat、Gemini 2.5、Qwen2.5-32B、Qwen2.5-72B、Qwen3-235B-a22b，分析不同异味的分布与普遍性。
- 提出 **InCE (Invariant-aware Constraint Evolution)**：先用 **IEM** 从历史对话中提取“全局不变量/必须持续满足的约束”，再用 **PSD** 在生成前做质量审计，提前检查是否会违反这些约束。
- 用最简单的话说，核心机制就是：**先把整段对话里一直不能变的规则整理出来，再在每次回答前检查新回答会不会破坏这些规则。**

## Results
- 作者声称这是**首个**针对多轮人机协作代码生成“交互异味”的系统化分类研究，基于真实用户-LLM日志而非纯模拟任务。
- 在人工标注中，用户意图类异味中：**Ambiguous Instruction 3.84%**，**Incomplete Instruction 4.39%**。
- 历史指令遵循类中：**Must-Do Omission 38.35%**，**Must-Not Violate 3.22%**；文中明确指出 **Must-Do Omission** 是跨模型普遍存在的高频问题之一。
- 论文还定性指出 **Partial Functionality Breakdown** 同样在不同模型中普遍存在，而 **Ambiguous Instruction** 与 **Incomplete Instruction** 相对较少见；但给定摘录未提供所有类别/所有模型的完整分布数字。
- 在扩展的 **WildBench** 上，**InCE** 将 **Task Success Rate** 最多提升 **6.67%**。
- **InCE** 还能将关键交互异味（如 **Repetitive Response** 和 **Must-Do Omission**）的发生率压低约 **13.5%**。

## Link
- [http://arxiv.org/abs/2603.09701v1](http://arxiv.org/abs/2603.09701v1)
