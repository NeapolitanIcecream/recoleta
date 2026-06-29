---
source: arxiv
url: http://arxiv.org/abs/2603.28731v1
published_at: '2026-03-30T17:46:41'
authors:
- Oliver Aleksander Larsen
- Mahyar T. Moghaddam
topics:
- llm-middleware
- runtime-interoperability
- schema-matching
- code-generation
- distributed-systems
relevance_score: 0.77
run_id: materialize-outputs
language_code: zh-CN
---

# SAGAI-MID: A Generative AI-Driven Middleware for Dynamic Runtime Interoperability

## Summary
## 摘要
SAGAI-MID 是一个由 LLM 驱动的 FastAPI 中间件，用于在运行时检测异构服务之间的 schema 不匹配，并改写请求以符合目标 schema。它把 API 和 payload 适配变成一个在线中间件功能，而不是为每一对 schema 手工编写适配器。

## 问题
- 分布式系统常常连接 REST API、GraphQL 服务和 IoT 设备，而它们的 payload 在字段名、类型、单位和嵌套结构上不同。
- 静态适配器和映射规则需要为每一对源/目标 schema 单独手工处理，而且当运行时出现新组合时就会失效。
- 这会带来持续的维护成本，也会在生产系统里造成 schema 演进和协议异构带来的互操作失败。

## 方法
- 该中间件拦截 HTTP 请求，查找路由对应的源和目标 JSON schema，并检查不匹配项。
- 检测分为两部分：一部分是确定性的结构差异分析，用于找出缺失字段、类型差异、嵌套差异和基数差异；另一部分是 LLM 语义检查，用于发现命名和单位不匹配。
- 解决方式有两种：**DIRECT** 让 LLM 映射字段并逐个请求转换；**CODEGEN** 让 LLM 编写一个 Python 适配器函数，然后对其编译、验证并缓存以便复用。
- 可靠性来自三层保护：JSON Schema 和 Pydantic 验证；当验证失败时使用 3 个并行 LLM 调用进行集成投票；以及一个基于规则的回退机制，用于已知的重命名、单位换算、类型强制转换和数组/单值情况。
- 缓存的 CODEGEN 适配器用源和目标 schema 的 SHA-256 哈希作为键，因此同一对 schema 在首次编译后可以在不调用 LLM 的情况下重复运行。

## 结果
- 在 10 个互操作场景中，覆盖 REST、GraphQL 和 IoT，并使用来自 OpenAI 和 xAI 的 6 个 LLM，最佳配置达到 **0.90 pass@1**：**Grok 4.1 Fast (reasoning) + CODEGEN**。
- 对 6 个模型取平均后，**CODEGEN 的 pass@1 高于 DIRECT：0.83 对 0.77**。它也把数值准确率从 **0.95** 提高到 **0.97**。
- 跨模型结果：GPT-4o **0.70 -> 0.83**，GPT-5 **0.80 -> 0.80**，GPT-5.2 **0.83 -> 0.87**，GPT-5-nano **0.73 -> 0.73**，Grok 4.1 Fast non-reasoning **0.70 -> 0.87**，Grok 4.1 Fast reasoning **0.87 -> 0.90**，对应 DIRECT -> CODEGEN。
- 各模型的字段级映射质量都很高，**Field F1 >= 0.98**，所以大多数错误来自转换后的值错误，而不是字段对应关系缺失。
- 场景难度有明显差异：库存大小写、嵌套到扁平、缺失字段、数组与单值转换都达到跨模型 **1.00 pass@1**，而传感器分析和指标归一化最难，平均 pass@1 约为 **0.50-0.56**。
- 成本和延迟在不同模型之间差异很大。总基准成本从 **$0.18** 到 **$6.25**，平均延迟从约 **9 s** 到 **104 s**。论文声称，在这个设置里，准确率最高的模型也是最便宜的：**Grok 4.1 Fast (reasoning)，0.90 pass@1，成本 $0.18**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.28731v1](http://arxiv.org/abs/2603.28731v1)
