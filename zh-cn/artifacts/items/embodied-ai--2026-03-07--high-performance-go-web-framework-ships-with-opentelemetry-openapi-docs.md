---
source: hn
url: https://github.com/rivaas-dev/rivaas
published_at: '2026-03-07T23:40:49'
authors:
- atkrad
topics:
- go-web-framework
- cloud-native
- opentelemetry
- openapi
- http-router
relevance_score: 0.01
run_id: materialize-outputs
language_code: zh-CN
---

# High-performance Go web framework; Ships with OpenTelemetry, OpenAPI docs

## Summary
这不是一篇机器人或基础模型论文，而是一个面向 Go 的高性能云原生 Web 框架 Rivaas。它主打高性能路由、内置可观测性、自动 OpenAPI 文档和模块化生产级能力。

## Problem
- 解决 Go 服务开发中“高性能路由、生产级中间件、可观测性、文档生成、配置管理”经常分散在多个库、集成成本高的问题。
- 这很重要，因为云原生 API 服务需要既快又稳定，还要易于监控、部署和维护。
- 该项目还试图避免开发者在“全功能框架”和“可独立复用组件”之间二选一。

## Approach
- 核心机制是提供一个 **batteries-included** 的 `app` 层，把路由、日志、指标、追踪、健康检查、校验、OpenAPI 等能力默认整合起来。
- 路由层使用 **radix tree router with Bloom filter optimization**，目标是在请求匹配上获得更高吞吐和更低开销。
- 可观测性原生接入 **OpenTelemetry**，并支持 Prometheus、OTLP、Jaeger 等后端，简化生产监控接入。
- 采用多模块仓库设计，每个子包可独立使用并单独版本化，从而兼顾“框架式易用性”和“库式灵活性”。
- 附带 12 个生产级中间件，以及优雅关闭、健康检查、panic recovery、mTLS 等运维能力。

## Results
- 文本声称该框架具备 **高性能**，并且“在每次路由器发布时都运行基准测试”，还与 **Gin、Echo、Chi、Fiber** 等进行比较，但此摘录**没有给出具体吞吐、延迟或内存数字**。
- 提供了 **12 个** 内置生产级中间件：accesslog、recovery、cors、requestid、timeout、ratelimit、basicauth、bodylimit、compression、security、methodoverride、trailingslash。
- 支持 **Go 1.25+**。
- 健康检查可配置就绪探针；指标默认可暴露到 **`:9090/metrics`**；追踪支持 **OTLP (`localhost:4317`)** 和 stdout 示例。
- 项目结构包含 **10+** 可独立使用的模块（如 app、router、binding、validation、logging、metrics、tracing、openapi 等），强调模块化复用和独立版本管理。
- 就给定用户关注方向而言，这项工作与 embodied/robot foundation model 主题**几乎无直接关系**。

## Link
- [https://github.com/rivaas-dev/rivaas](https://github.com/rivaas-dev/rivaas)
