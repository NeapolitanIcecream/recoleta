---
source: hn
url: https://thenewstack.io/risk-mitigation-agentic-ai/
published_at: '2026-03-12T22:58:27'
authors:
- chhum
topics:
- agentic-ai
- api-mocking
- contract-testing
- enterprise-risk
- ai-agents
- mcp
relevance_score: 0.89
run_id: materialize-outputs
language_code: zh-CN
---

# Before you let AI agents loose, you'd better know what they're capable of

## Summary
这篇文章讨论企业在部署具备行动能力的 AI agents 前，为什么必须先用**契约测试、沙箱和高保真 mock**来理解并约束其行为。核心观点是：对于 agentic AI，系统真实能力应由其可观察、可测试的行为来定义，而不是仅靠设计意图。

## Problem
- 企业级 agent 不是只生成文本，而是会**浏览网页、调用 API、执行代码、修改文件**，因此早期错误可能级联放大，且难以及时审计和追责。
- 这类系统暴露于**提示注入、安全越权、数据泄露、不可逆操作**等风险；在缺少成熟实践的情况下，直接上线代价很高。
- 如果企业没有清晰的 API 目录、沙箱和共享 mock，团队就难以知道“系统到底能做什么”，更难安全评估 agent 的真实能力边界。

## Approach
- 核心方法是把**测试与 mocking 当作 agent 风险缓解基础设施**：先在沙箱中观察和塑造行为，再逐步接近生产环境。
- 采用**contract-first**思路：以 OpenAPI 等正式规范作为主工件，自动生成 mock endpoint，并用示例数据、录制流量或 YAML 补充高保真场景。
- 通过**契约测试**让 API 提供方与消费方共享同一行为预期，确保 mock 与真实服务结构一致，减少“假 mock”导致的错误安全感。
- 借助 Microcks、OpenAPI、Bruno 等开源工具，企业可在 REST、gRPC、GraphQL、Kafka、MQTT 等多协议环境中建立统一的“sandbox as a service”。
- 新增的 MCP 接口还让 mock API 可直接作为 **LLM/agent 工具**使用，从而在生产前测试 agent 如何调用企业能力。

## Results
- BNP Paribas 在法国零售银行部门中，**32 个 squad、500+ 开发与测试人员**使用 Microcks，平台每周处理**250 万+ API 调用**。
- 根据公开案例，借助主机 API mocking，BNP 的**开发与测试周期缩短了三分之二（约 66%）**，并减少了对昂贵核心主机的直接访问。
- Microcks 轻量本地二进制启动时间**低于 200 毫秒**，支持 Java、Node、Go、.NET 的 Testcontainers 集成，帮助缩小“works on my laptop”差距。
- 大型采用者（如 Amadeus）被描述为获得了**显著开发速度提升**，但文中未提供更细的可比基线数值。
- 对 agentic AI 本身，文章**没有给出标准基准数据或模型性能指标**；最强的具体主张是：高保真 mock + 契约测试 + 共享沙箱可在上线前更安全地暴露并约束 agent 行为。

## Link
- [https://thenewstack.io/risk-mitigation-agentic-ai/](https://thenewstack.io/risk-mitigation-agentic-ai/)
