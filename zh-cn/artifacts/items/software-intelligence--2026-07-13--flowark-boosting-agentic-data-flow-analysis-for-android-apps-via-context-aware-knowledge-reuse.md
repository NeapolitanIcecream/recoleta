---
source: arxiv
url: https://arxiv.org/abs/2607.11308v1
published_at: '2026-07-13T09:21:38'
authors:
- Yiming Zhang
- Jiangrong Wu
- Yuhong Nan
topics:
- code-intelligence
- agentic-software-engineering
- android-security
- data-flow-analysis
- agent-memory
- knowledge-reuse
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# FlowArk: Boosting Agentic Data-flow Analysis for Android Apps via Context-Aware Knowledge Reuse

## Summary
## 摘要
FlowArk 通过在原本彼此隔离的编码代理会话之间共享经过验证的知识，减少批量 Android 数据流任务中的重复代码分析。在 50 个开源 Android 应用的 4,685 个任务上，它将 API 成本降低了 26.83%，同时保持相近的分析质量。

## 问题
- 批量源到汇数据流分析会为不同污点源分配独立代理，但共享回调、分发器和跨文件逻辑会导致重复分析。
- 上下文隔离使后续代理无法使用先前的推理，增加了 token 用量和 API 成本，也减少了固定预算下能够完成的任务数量。
- 通用记忆系统可能存储不精确的信息，而且通常检索过晚，因为需要由当前代理主动请求这些信息。

## 方法
- FlowArk 将已完成的分析历史提炼为有证据支持、有边界且可执行的知识，用于描述反复出现的共享代码片段。
- 它为每条知识配置基于代码的匹配规则，包括精确符号、调用、符号后缀和包前缀。
- 在后续分析期间，FlowArk 监控工具输出，并在运行时上下文暴露相关代码锚点后立即注入匹配的知识块。
- 注入的知识块指出哪些共享步骤可以跳过，以及哪些依赖参数的下游处理器仍需检查。
- 准入检查会拒绝或修复证据不足、边界不清或匹配规则不可靠的条目。

## 结果
- 评估使用基于 OpenCode 的实现，覆盖了 50 个开源 Android 应用中的 4,685 个源到汇数据流分析任务。
- 与标准 OpenCode 相比，FlowArk 将端到端 LLM API 成本降低了 26.83%，同时保持相近的分析质量。
- 在 100 美元预算下，FlowArk 完成了 1,060 个任务，标准 OpenCode 完成了 776 个任务，任务数量增加了 36.66%。
- 与启用 Mem0 的 OpenCode 和 Analysis-Log RAG 相比，FlowArk 报告了更高的成本节省，同时保持相近的分析质量。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.11308v1](https://arxiv.org/abs/2607.11308v1)
