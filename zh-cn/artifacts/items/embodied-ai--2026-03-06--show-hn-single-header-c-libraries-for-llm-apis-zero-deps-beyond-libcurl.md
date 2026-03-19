---
source: hn
url: https://news.ycombinator.com/item?id=47282433
published_at: '2026-03-06T23:23:17'
authors:
- Shmungus
topics:
- llm-api
- c-plus-plus
- single-header-library
- inference-infrastructure
- structured-output
relevance_score: 0.1
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Single-header C++ libraries for LLM APIs – zero deps beyond libcurl

## Summary
这不是一篇机器人或基础模型论文，而是一组面向 LLM API 的单头文件 C++ 工具库，主打除 `libcurl` 外零额外依赖。它试图用极简集成方式解决流式调用、缓存、成本估算、重试容错和结构化输出等工程问题。

## Problem
- 解决的问题是：C++ 开发者接入 OpenAI/Anthropic 等 LLM API 时，常需要引入大量第三方依赖，增加编译、部署和维护复杂度。
- 这很重要，因为生产环境中的 LLM 应用不仅要“能调用”，还要处理流式返回、缓存、成本控制、失败重试和结构化输出等实际工程需求。
- 对给定用户关注方向而言，它与 embodied/robot foundation model 关系较弱，但可作为底层推理服务接入的工程配套组件。

## Approach
- 核心方法很简单：把常见 LLM API 工程能力拆成多个独立的单头文件 `.hpp` 库，做到“拷贝文件、链接 `libcurl`、即可使用”。
- `llm-stream` 提供 OpenAI 和 Anthropic 的流式输出，采用 callback 方式处理增量 token/文本。
- `llm-cache` 提供文件后端的语义缓存，并带 LRU 淘汰，用于减少重复请求。
- `llm-cost` 在离线场景做 token 计数和费用估算，帮助开发者控制预算。
- `llm-retry` 与 `llm-format` 分别处理指数退避/熔断/供应商切换，以及结构化输出约束与手写 JSON 解析，避免依赖如 nlohmann、boost 或 Python。

## Results
- 文本未提供标准论文式定量实验结果，**没有**给出数据集、基线模型、准确率、延迟、吞吐或成本节省百分比。
- 最强的具体工程声明是：每个组件都可“drop in one `.hpp`, link `libcurl`, done”，即除 `libcurl` 外零额外依赖。
- 功能覆盖上，明确声称支持 **2 个**主流提供商的流式调用：OpenAI 与 Anthropic。
- 组件数量上，共列出 **5 个**独立库：`llm-stream`、`llm-cache`、`llm-cost`、`llm-retry`、`llm-format`。
- 容错机制上，`llm-retry` 明确包含 **3 类**能力：exponential backoff、circuit breaker、provider failover。
- 结构化输出方面，`llm-format` 明确采用手写 JSON parser，但文中未提供其正确率、性能或与现有解析器对比数字。

## Link
- [https://news.ycombinator.com/item?id=47282433](https://news.ycombinator.com/item?id=47282433)
