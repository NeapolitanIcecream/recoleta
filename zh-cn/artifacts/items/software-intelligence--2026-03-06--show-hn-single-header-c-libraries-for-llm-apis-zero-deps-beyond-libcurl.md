---
source: hn
url: https://news.ycombinator.com/item?id=47282433
published_at: '2026-03-06T23:23:17'
authors:
- Shmungus
topics:
- c-plus-plus
- llm-api
- single-header-library
- code-infrastructure
- structured-output
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Single-header C++ libraries for LLM APIs – zero deps beyond libcurl

## Summary
这是一组面向 C++ 的单头文件 LLM API 库，主打除 `libcurl` 外几乎零依赖，并覆盖流式调用、缓存、成本估算、重试容错和结构化输出。它的价值在于让原生 C++ 项目更容易接入和工程化使用大模型，而不必引入庞大依赖栈。

## Problem
- 许多 LLM 工具链偏向 Python 或重依赖生态，不适合依赖敏感、部署受限或原生系统软件场景的 C++ 项目。
- 直接调用 LLM API 往往缺少工程化能力，如流式处理、语义缓存、成本控制、失败重试和结构化输出约束。
- 这很重要，因为在软件基础设施、代码智能和自动化工程中，低依赖、可嵌入、可控的 LLM 接入层能显著降低集成与运维成本。

## Approach
- 提供多个可独立引入的单头文件库：`llm-stream`、`llm-cache`、`llm-cost`、`llm-retry`、`llm-format`，用户只需引入一个 `.hpp` 并链接 `libcurl`。
- `llm-stream` 用回调方式支持 OpenAI 和 Anthropic 的流式输出，简化增量生成的接入。
- `llm-cache` 提供文件后端的语义缓存，并带 LRU 淘汰，用于减少重复请求和延迟。
- `llm-cost` 做离线 token 计数与成本估算；`llm-retry` 提供指数退避、熔断器和供应商故障切换；`llm-format` 用手写 JSON 解析器做结构化输出约束。
- 整体机制可以理解为：把调用大模型时最常见的“工程胶水”拆成几个极轻量 C++ 组件，尽量避免外部依赖如 nlohmann、boost 或 Python。

## Results
- 文本没有提供基准实验、公开数据集或定量指标，因此**没有可报告的数值结果**。
- 最强的具体声明是工程属性：除 `libcurl` 外“零额外依赖”，以单头文件形式交付，支持直接 drop-in 集成。
- 功能覆盖 5 个方面：流式调用、文件型语义缓存（含 LRU）、离线 token/成本估算、指数退避+熔断+故障切换、结构化输出约束。
- 支持至少 2 家模型提供商：OpenAI 和 Anthropic（在 `llm-stream` 描述中明确提到）。

## Link
- [https://news.ycombinator.com/item?id=47282433](https://news.ycombinator.com/item?id=47282433)
