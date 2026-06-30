---
source: arxiv
url: https://arxiv.org/abs/2606.30317v1
published_at: '2026-06-29T13:59:41'
authors:
- Carson Rodrigues
- Oysturn Vas
topics:
- model-context-protocol
- llm-tools
- agent-infrastructure
- software-architecture
- tool-use
- human-ai-interaction
relevance_score: 0.76
run_id: materialize-outputs
language_code: zh-CN
---

# MCP Server Architecture Patterns for LLM-Integrated Applications

## Summary
## 摘要
这篇论文为 MCP 服务器作者提供了一个模式目录，用于构建连接 LLM 的工具、资源和服务包装器。论文的核心主张是：LLM 客户端会改变 API 设计，因为它们通过名称、描述和 schema 来选择工具。

## 问题
- MCP 被快速采用后，短时间内出现了许多服务器，但开发者缺少已发表的指导，来判断如何拆分工具、管理状态、聚合服务器，以及包装复杂 API。
- 这一点很重要，因为 LLM 会阅读自然语言描述和 schema 来选择工具。糟糕的服务器设计可能降低工具选择准确率、暴露提示注入路径，或造成脆弱的集成。
- 论文关注 MCP 服务器的维护和演进，尤其是连接数据库、API、工作流和基于会话的工具的生产级 LLM 应用。

## 方法
- 作者研究了 15 个 MCP 服务器：5 个生产环境中的 ANSYR 语音 AI 服务器，以及 10 个来自官方 MCP registry 的公开服务器。
- 他们从每个服务器中提取了工具、资源和提示注册信息；传输设置；会话处理；上游委派；以及特定领域校验。
- 他们把反复出现的结构编码为 5 种模式：Resource Gateway、Tool Orchestrator、Stateful Session Server、Proxy Aggregator 和 Domain-Specific Adapter。
- 他们还描述了 4 种反模式：God Tool、Unsanitized Resource Content、Synchronous Long-Running Operations 和 Missing or Vague Tool Descriptions。
- 最简单的机制是模式挖掘：检查真实的 MCP 服务器，把重复出现的设计选择分组，然后测试独立评分者能否应用这些标签。

## 结果
- 该目录来自 15 个服务器：5 个生产服务器和 10 个公开服务器。论文报告了 5 种架构模式和 4 种反模式。
- 在 54 个留出的 MCP 服务器上，两个独立的 LLM 评分者达到 Cohen’s κ = 0.76，95% CI 为 [0.62, 0.88]，原始一致率为 81.5%。与作者标签的一致率为：Claude Haiku 4.5 为 68.5%，Claude Sonnet 4 为 75.9%。
- 一项使用作者撰写的标准描述的试点测试得分为 97%，但作者认为这是更容易的测试，因为这些描述过于直接地暴露了架构。
- 环回上的传输延迟为：stdio 的 p50 为 0.01 ms，streamable-http 的 p50 为 0.39 ms。跨主机同区域路径被建模为约 30 ms p50 基线加协议开销。
- 对 Claude Haiku 4.5，每个上下文中的工具数量在 10 到 15 个之间时，工具选择准确率降至 90% 以下；对 Claude Sonnet 4，则在 20 到 30 个之间降至 90% 以下。
- 最强的实践性主张是：当可见工具集超过这些因模型而异的范围后，静态工具聚合可能损害 LLM 的选择效果。因此，对大型 MCP 部署来说，限定范围的聚合或对工具进行检索更安全。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.30317v1](https://arxiv.org/abs/2606.30317v1)
