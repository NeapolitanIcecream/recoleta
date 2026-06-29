---
source: hn
url: https://stale-trace.vercel.app/
published_at: '2026-06-19T23:03:36'
authors:
- zahraarman
topics:
- agent-debugging
- temporal-ledger
- code-intelligence
- production-agents
- human-ai-interaction
relevance_score: 0.67
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: StaleTrace – A temporal ledger that catches stale-state agent bugs

## Summary
## 摘要
StaleTrace 是一种用于 Agent 的确定性事故调试工具，用来发现 Agent 何时使用了过时、冲突或无效状态。它基于现有工具调用和事实事件构建时间账本，然后写出一份通俗的事故报告。

## 问题
- 生产环境中的 Agent 故障可能来自事实在 Agent 观察后发生变化，例如账户关闭或客户记录变更。
- 团队需要知道 Agent 行动时哪些事实为真，因为当前数据库状态可能掩盖过去故障的原因。
- 目标痛点是生产 Agent 的可审计性，且无需让另一个 LLM 判断故障。

## 方法
- 系统读取用户系统已记录的 Agent 工具调用和事实事件。
- 它将事实事件重放到 ValidMemory 中。ValidMemory 是一个时间事实账本，其中每个值都有有效期窗口。
- 它把 Agent 使用的事实与当时有效的事实进行比较。
- 它标记过时事实、冲突事实和已关闭账户状态，然后生成根因、影响范围和可复制的事故报告。

## 结果
- 摘录未给出基准测试、数据集、准确率、延迟或生产规模数据。
- 它声称审计过程需要 0 次 LLM 调用、0 个嵌入，并且不使用图数据库。
- 它声称输出是确定性的：相同输入会产生相同判定。
- 它声称为 1 个重建示例 customer_123 生成报告，但没有展示与追踪、日志或基于 LLM 的评估器之间的实测对比。
- 摘录中唯一的时间数字是 20 分钟演示预约，这是销售流程细节，不是技术结果。

## Problem

## Approach

## Results

## Link
- [https://stale-trace.vercel.app/](https://stale-trace.vercel.app/)
