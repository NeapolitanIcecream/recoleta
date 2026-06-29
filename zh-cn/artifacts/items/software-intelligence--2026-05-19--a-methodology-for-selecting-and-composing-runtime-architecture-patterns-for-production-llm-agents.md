---
source: arxiv
url: https://arxiv.org/abs/2605.20173v1
published_at: '2026-05-19T17:54:21'
authors:
- Vasundra Srinivasan
topics:
- llm-agents
- runtime-architecture
- multi-agent-systems
- software-engineering
- agent-reliability
- human-ai-interaction
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# A Methodology for Selecting and Composing Runtime Architecture Patterns for Production LLM Agents

## Summary
## 摘要
本文认为，生产环境中的 LLM 代理需要在模型输出和系统动作之间有一个明确契约。作者把这个契约命名为随机-确定性边界，并给出了一套面向运行时架构的模式选择方法。

## 问题
- 生产环境中的 LLM 代理常常在模型提议变成数据库写入、工具调用或外部副作用时出错。
- 这些错误很重要，因为更好的模型会降低单次调用的波动，但不会决定状态归属、重试、门控、持久化提交或人工审批。
- 团队已经在代理动作外层加入检查和提交，但本文认为他们缺少一个共享契约来设计和审查这个边界。

## 方法
- 核心机制是随机-确定性边界：LLM 提议一个动作，确定性代码验证它，系统将被接受的动作持久化提交，而当验证失败时，带类型的拒绝信号会返回给 LLM。
- 论文把运行时设计分成 3 个关注点：协调、状态和控制。
- 论文定义了 6 种运行时模式：分层委派、散射-聚合加 Saga、事件驱动排序、共享状态机、监督者加门控、以及人工介入。
- 论文给出了一套 5 步选择方法：先分类运行时，再选择状态主干，然后加入协调、加入控制，最后记录决定。
- 论文还给出了一套生产故障诊断流程，包括 replay divergence，即把同一个事件日志通过一个已更换的 LLM 或提示词重放后，生成了不同的下游事件。

## 结果
- 对 5 个开源代理项目的审计发现，在 21 个 LLM 到动作的调用点中，有 19 个显式包含验证器和提交逻辑。
- 对 21 篇已发表的代理故障事后分析进行分类后发现，21 个案例中有 15 个，也就是 71.4%，问题定位到边界薄弱处。
- 同一分类还发现，21 个修复中有 17 个，也就是 81%，强化了验证、提交语义或拒绝信号。
- 文中引用的一个 Promptfoo 案例报告称，在模型更换后，提示注入抵抗率下降了 23 个百分点，从使用 GPT-4o 时的 94% 降到使用 GPT-4.1 时的 71%；修复方案加入了输出分类器和更严格的工具门控。
- 论文把这套方法应用到 5 个工作负载上，并用公开的 IBM Telco Customer Churn 数据集构建了 1 个可运行的参考实现。
- 论文没有报告已部署生产系统在准确率、延迟、成本或事故减少方面的基准提升。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.20173v1](https://arxiv.org/abs/2605.20173v1)
