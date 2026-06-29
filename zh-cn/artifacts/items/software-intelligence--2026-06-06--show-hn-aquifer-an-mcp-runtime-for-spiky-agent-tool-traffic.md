---
source: hn
url: https://github.com/rjpruitt16/aquifer
published_at: '2026-06-06T23:08:44'
authors:
- rjpruitt16
topics:
- mcp-runtime
- agent-tooling
- rate-limiting
- durable-queues
- webhooks
- traffic-control
relevance_score: 0.62
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Aquifer – an MCP runtime for spiky agent tool traffic

## Summary
## 摘要
Aquifer 是一个自托管的 MCP 和 HTTP 运行时，把突发的 agent 工具调用转成持久、限速的任务。它适合那些会压垮本地后端，或从外部 API 收到 429 的 agent 系统。

## 问题
- 分布式 agent 会成批发送工具和 API 请求，导致入站流量过载、出站 429，以及某个依赖变慢后连带失败。
- agent 团队需要一层协调，方便后端或上游 API 决定安全的请求速度。
- 这个工具面向单机 sidecar 部署，团队想要持久化，又不想加外部数据库。

## 方法
- agent 通过 MCP 工具或 HTTP 端点提交任务；Aquifer 返回 job ID，把任务存到 SQLite，之后再分发。
- 每个上游都有独立 worker，按配置的 RPS 和并发上限发送请求，并根据 `X-Aquifer-*` 响应头里的抖动和实时降速信号调整速度。
- 结果通过 webhook 发送，Server-Sent Events 提供实时任务状态、队列位置，以及给晚订阅者的补发事件。
- 运行时核心处理幂等性、持久化、分发、SSE 事件、L8 签名、webhook 投递和指标；适配器通过 MCP stdio、HTTP 或自定义 Go 集成把这个核心暴露出去。
- L8 v0.1 在一次性的公钥挑战之后用 Ed25519 给 webhook 签名，避免保存共享的 HMAC 密钥。

## 结果
- 摘要没有给出吞吐量、延迟、队列持久性或故障恢复的基准，因此不能支持有实测性能突破的说法。
- 配置示例显示了按上游设置的限制，例如 `api.openai.com` 为 10 RPS、最多 3 个并发请求，`api.stripe.com` 为 20 RPS、最多 5 个并发请求，以及一个内部后端为 50 RPS、最多 10 个并发请求。
- webhook 投递会重试 4 次，退避间隔分别是 1 秒、2 秒、4 秒和 8 秒。
- 任务等待时，每 2 秒发出一次队列位置事件。
- 运行中的任务如果超过 5 分钟，会被重置为 `queued`；重启后，队列中的任务会从 SQLite 重新分发。
- L8 协议版本是 0.1；摘要称 webhook 验证只需要一次本地 Ed25519 `verify()` 调用，使用缓存的公钥。

## Problem

## Approach

## Results

## Link
- [https://github.com/rjpruitt16/aquifer](https://github.com/rjpruitt16/aquifer)
