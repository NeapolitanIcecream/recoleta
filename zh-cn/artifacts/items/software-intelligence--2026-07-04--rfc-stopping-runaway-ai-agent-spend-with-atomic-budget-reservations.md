---
source: hn
url: https://github.com/iamapsrajput/agent-budget-protocol/blob/main/RFC.md
published_at: '2026-07-04T22:42:00'
authors:
- iamapsrajput
topics:
- agent-budgeting
- llm-gateway
- cost-control
- agent-runtime
- software-agents
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# RFC: Stopping runaway AI agent spend with atomic budget reservations

## Summary
## 摘要
这份 RFC 提出一种面向 AI agent 单次运行的预算权限机制，在每次调用 LLM 提供商之前先预留估算费用。它针对的是 agent 循环导致的失控成本：agent 会反复发送不断增长的上下文，并在一次会话中发起大量调用。

## 问题
- Agent 运行的成本可能快速增长，因为每次循环都可能重新发送累积上下文；摘录称，到第 20 步时，单次调用的输入 token 可能超过 50K。
- 现有网关预算通常绑定到 API key、用户或团队，并按天或月统计，而一次 agent 运行可能在数小时内耗尽配额。
- 目前的预算失败通常只给 agent 返回不透明的错误，因此 agent 无法切换到更便宜的模型、缩短上下文，或干净地停止。

## 方法
- 以网关 hook、sidecar 或 SDK middleware 的形式加入预算决策层。
- 在调用提供商之前，根据实际输入 token、有效的最大输出 token 和带版本的价格表，计算最坏情况的估算成本。
- 使用一个 Redis Lua 脚本或一个 SQL 事务，在所有适用范围内原子化预留该估算金额，例如 run、user、team、key 和 feature。
- 调用结束后，提交实际用量并释放未使用的预留；如果提供商调用失败，则释放预留；如果结果缺失，则让预留过期并稍后对账。
- 通过 header 和 RFC 9457 problem-detail 错误返回预算状态，其中包括满足工具、JSON、上下文、模态和租户策略需求的可用替代选项。

## 结果
- 这份 RFC 报告的是用于说明问题的成本事件，不是新的实验：据报告，一名开发者在一个周末的 API 费用达到 $4,200，一个 35 人工程团队收到了 $87K 的月度账单。
- 它引用了一次覆盖 30 个团队的审计：同一工具下，每名开发者成本的 p10 到 p90 相差 20x；摘录称这些数据来自行业文章，而非一手事故报告。
- 在 hard-gate 模式下，它声称只有当估算费用已针对每个适用上限完成预留后，请求才会被转发，这会关闭一个竞态：10 个并行调用各自看到还有剩余预算并全部通过。
- v1 范围包括可执行的 run、user 和 key 上限；feature 和 team 在 v1 中是归因标签，v1 之后才会有可执行的 feature/team 上限。
- 它没有给出延迟、吞吐量、误拦截、成本节省或生产采用情况的基准结果。

## Problem

## Approach

## Results

## Link
- [https://github.com/iamapsrajput/agent-budget-protocol/blob/main/RFC.md](https://github.com/iamapsrajput/agent-budget-protocol/blob/main/RFC.md)
