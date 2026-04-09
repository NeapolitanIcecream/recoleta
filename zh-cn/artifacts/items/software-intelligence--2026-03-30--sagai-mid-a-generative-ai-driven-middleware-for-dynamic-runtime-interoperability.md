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
SAGAI-MID 是一个由 LLM 驱动、基于 FastAPI 的中间件，可在运行时检测异构服务之间的 schema 不匹配，并重写请求以适配目标 schema。它把 API 和 payload 适配变成在线中间件功能，而不是为每一组 schema 手写一个适配器。

## 问题
- 分布式系统常常连接 REST API、GraphQL 服务和 IoT 设备，而它们的 payload 在字段名、类型、单位和嵌套结构上各不相同。
- 静态适配器和映射规则需要为每一组源 schema 与目标 schema 手工编写，运行时一旦出现新组合就会失效。
- 这很重要，因为 schema 演进和协议异构会在生产系统中持续带来维护成本和互操作失败。

## 方法
- 中间件会拦截 HTTP 请求，查找该路由对应的源和目标 JSON schema，并检查是否存在不匹配。
- 检测分为两部分：一是确定性的结构 diff，用于发现缺失字段、类型差异、嵌套差异和基数差异；二是由 LLM 执行的语义检查，用于识别命名和单位不匹配。
- 解决使用两种策略：**DIRECT**，由 LLM 对字段进行映射并转换每个请求；**CODEGEN**，由 LLM 编写 Python 适配器函数，再对其进行编译、验证并缓存以供复用。
- 可靠性来自三层保障：JSON Schema 和 Pydantic 验证；当验证失败时发起 3 次并行 LLM 调用并进行集成投票；以及面向已知重命名、单位转换、类型强制转换和数组/单值情况的规则回退。
- 缓存的 CODEGEN 适配器以源和目标 schema 的 SHA-256 哈希为键，因此同一组 schema 在首次编译后可在后续运行中做到零 LLM 调用。

## 结果
- 在涵盖 REST、GraphQL 和 IoT 的 10 个互操作场景中，并在来自 OpenAI 和 xAI 的 6 个 LLM 上测试，最佳配置达到 **0.90 pass@1**：**Grok 4.1 Fast（reasoning）+ CODEGEN**。
- 在全部 6 个模型上的平均结果中，**CODEGEN 的 pass@1 优于 DIRECT：0.83 对 0.77**。它还把 value accuracy 从 **0.95** 提高到 **0.97**。
- 跨模型结果：GPT-4o **0.70 -> 0.83**，GPT-5 **0.80 -> 0.80**，GPT-5.2 **0.83 -> 0.87**，GPT-5-nano **0.73 -> 0.73**，Grok 4.1 Fast non-reasoning **0.70 -> 0.87**，Grok 4.1 Fast reasoning **0.87 -> 0.90**，对应 DIRECT -> CODEGEN。
- 各模型的字段级映射质量都很高，**Field F1 >= 0.98**，因此大多数错误来自转换后的值错误，而不是字段对应关系缺失。
- 不同场景难度差异明显：股票代码大小写、nested-to-flat、缺失字段和数组-单值转换在各模型上都达到 **1.00 pass@1**；而传感器分析和指标归一化最难，平均 **pass@1** 约为 **0.50-0.56**。
- 各模型的成本和延迟差异很大。基准测试总成本范围为 **$0.18** 到 **$6.25**，平均延迟约为 **9 s** 到 **104 s**。论文称，在这组配置中，最准确的模型也是最便宜的：**Grok 4.1 Fast（reasoning），0.90 pass@1，成本 $0.18**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.28731v1](http://arxiv.org/abs/2603.28731v1)
