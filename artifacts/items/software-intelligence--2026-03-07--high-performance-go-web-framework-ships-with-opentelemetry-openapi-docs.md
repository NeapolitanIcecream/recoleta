---
source: hn
url: https://github.com/rivaas-dev/rivaas
published_at: '2026-03-07T23:40:49'
authors:
- atkrad
topics:
- go-web-framework
- cloud-native
- observability
- openapi
- high-performance-routing
relevance_score: 0.49
run_id: materialize-outputs
---

# High-performance Go web framework; Ships with OpenTelemetry, OpenAPI docs

## Summary
Rivaas 是一个面向云原生场景的 Go Web 框架，主打高性能路由、开箱即用的可观测性、自动 OpenAPI 文档，以及模块化可独立使用的组件设计。它试图把生产环境常见能力整合到一个轻量但完整的开发栈中。

## Problem
- 解决 Go Web 服务开发中“能力分散、集成成本高”的问题：开发者通常需要手动拼装路由、日志、指标、追踪、校验和文档生成。
- 解决生产级 API 服务从开发到上线之间的落差：很多轻量框架缺少优雅关闭、健康检查、panic 恢复、mTLS、可观测性等关键能力。
- 这很重要，因为云原生服务需要既快又稳定，还要便于监控、治理和维护，否则会增加工程复杂度和运维成本。

## Approach
- 核心方法是提供一个 **batteries-included** 的 `app` 层，把路由、日志、指标、追踪、配置、校验、错误处理、OpenAPI 等能力统一装配起来，开发者用少量代码即可启动服务。
- 底层使用独立的高性能 `router` 模块，采用 **radix tree router with Bloom filter optimization**，目标是在保持 API 易用性的同时提升路由性能。
- 采用模块化架构：`router`、`binding`、`validation`、`openapi`、`logging`、`metrics`、`tracing` 等每个包都可单独使用，并且各自有独立 `go.mod`，支持独立版本演进。
- 内置 OpenTelemetry 原生可观测性，支持 Prometheus、OTLP、Jaeger，并自动传播服务元数据与生命周期管理。
- 提供 12 个生产级中间件，以及健康检查、优雅关闭、请求绑定与验证、自动 OpenAPI 生成等常见后端能力，降低工程拼装工作量。

## Results
- 文中明确声称具备 **高性能路由**，并说明“每个 router release 都会运行 benchmarks”，且比较对象包括 **Gin、Echo、Chi、Fiber** 等框架。
- 但本摘录 **没有给出具体 benchmark 数字**，因此无法确认吞吐、延迟、内存占用或相对提升百分比。
- 可量化的具体功能声明包括：内置 **12 个** production-ready middleware；支持 Prometheus 指标暴露在 **`:9090/metrics`**；要求 **Go 1.25+**。
- 架构上包含 **11 个** 主要模块/包（如 `app`、`router`、`binding`、`validation`、`logging`、`metrics`、`tracing`、`openapi` 等），并采用 multi-module repository 以支持独立复用。
- 最强的实际主张是：相比只提供基础路由的框架，Rivaas 将性能、可观测性、文档、验证和生产运维能力统一打包，强调“生产可用 + 云原生 + 模块化”的综合工程价值，而非单点算法突破。

## Link
- [https://github.com/rivaas-dev/rivaas](https://github.com/rivaas-dev/rivaas)
