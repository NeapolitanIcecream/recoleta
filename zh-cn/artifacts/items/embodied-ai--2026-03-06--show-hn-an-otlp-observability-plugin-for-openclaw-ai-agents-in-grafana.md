---
source: hn
url: https://github.com/awsome-o/grafana-lens
published_at: '2026-03-06T23:37:50'
authors:
- AwesomeO3000
topics:
- observability
- grafana
- otlp
- ai-agents
- sre
- tracing
relevance_score: 0.03
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: An OTLP observability plugin for OpenClaw AI agents in Grafana

## Summary
这不是一篇机器人/基础模型论文，而是一个面向 OpenClaw AI agent 的 Grafana 可观测性插件。它把指标、日志、链路追踪、告警和安全巡检封装成可由代理通过自然语言调用的工具，用于运维与监控。

## Problem
- 解决 AI agent 平台在**指标、日志、追踪、告警与安全信号**上分散、难统一排障的问题。
- 传统 OpenClaw 内置 diagnostics-otel 只提供基础计数/直方图，缺少**生命周期级 tracing、日志转发、会话级追踪和安全监测**，因此难以定位复杂故障或异常行为。
- 这很重要，因为 agent 系统一旦接入工具、Webhook、多轮会话和外部数据源，问题往往跨越 metrics/logs/traces，多信号联查是实际运维的核心需求。

## Approach
- 通过一个自包含的 OpenClaw 插件，把 **17 个 Grafana 相关工具**注册给 agent，让用户直接用自然语言完成查询 PromQL/LogQL/TraceQL、建 dashboard、设 alert、分享图表、调查 incident 等操作。
- 使用 **OTLP HTTP push** 将指标发送到 Prometheus、日志发送到 Loki、追踪发送到 Tempo；不依赖 Prometheus scraping，因此数据“立即可用”。
- 在 OpenClaw 中注册 **16 个生命周期 hooks**（如 `session_start`、`llm_input`、`before_tool_call`、`after_tool_call` 等），构建会话级 trace tree，并把日志与 `trace_id` 关联，实现 Loki 到 Tempo 的点击跳转。
- 提供面向 SRE 的分析逻辑：如 `grafana_investigate` 并行聚合 metrics/logs/traces/context；异常检测用**相对 7 天基线的 z-score**；告警疲劳分析识别 always-firing、flapping、error/nodata 规则。
- 提供检测型安全监控：**6 类检查**（提示注入、成本异常、工具循环、会话枚举、webhook 错误、卡住会话），以及 **12 条正则**扫描 prompt injection 信号，并支持敏感 token 自动脱敏导出。

## Results
- 文本**没有给出正式实验、基准数据集或对比论文式量化结果**，因此没有可核验的 SOTA/提升百分比。
- 具体功能性结果声明包括：提供 **17 个 composable tools**、**12 个预置 dashboard 模板**、**16 个生命周期 hooks**、**6 项安全检查**、**15+ 个消息渠道**分享能力。
- 异常分析方面，声明支持基于**7 天基线**的 z-score 严重度分级：`normal`（<1.5σ）、`mild`（1.5–2σ）、`significant`（2–3σ）、`critical`（>3σ）。
- 追踪检索方面，声明可直接查询慢 trace，例如阈值 **>10s** 的慢追踪，并支持基于 TraceQL 的错误状态与属性过滤。
- OTLP 导出默认周期给出为 **15000 ms**，内容字段默认截断长度 **2000** 字符；自定义指标默认支持最多 **100** 个 metric 定义、每个 metric 最多 **5** 个 label key、最多 **50** 个唯一 label 组合。
- 安全/隐私方面，声明默认开启 `redactSecrets`，可识别多类 token（如 `ghp_`、`xoxb-`、`sk-`、`glsa_` 等）并将其脱敏为 `${first6}...${last4}` 格式。

## Link
- [https://github.com/awsome-o/grafana-lens](https://github.com/awsome-o/grafana-lens)
