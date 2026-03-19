---
source: hn
url: https://reactdevelopment.substack.com/p/when-to-use-bff-and-should-it-replace
published_at: '2026-03-05T23:30:00'
authors:
- javatuts
topics:
- backend-for-frontend
- api-gateway
- microservices
- system-architecture
- client-specific-api
relevance_score: 0.01
run_id: materialize-outputs
language_code: zh-CN
---

# When to Use BFF and Should It Replace API Gateway?

## Summary
这篇文章讨论了 **BFF（Backend for Frontend）** 与 **API Gateway** 的职责区别，以及在什么情况下应该引入 BFF、何时可以与网关共存或暂时合并。核心结论是：BFF 适合处理面向特定客户端的数据聚合与接口定制，而 API Gateway 更适合处理路由、安全、限流等基础设施职责。

## Problem
- 文章要解决的问题是：在现代多客户端或复杂单前端系统中，**是否需要引入 BFF，以及它是否应该替代 API Gateway**。
- 这很重要，因为前端如果直接对接多个后端服务，就会承担请求编排、数据转换、错误处理、分页过滤等复杂逻辑，导致客户端变重、迭代变慢。
- 另一个关键问题是架构边界：如果把网关和 BFF 混在一起，短期上看似简单，但长期可能让单个组件承载过多职责，影响可维护性与扩展性。

## Approach
- 文章采用**架构模式分析**的方法，对比 BFF 与 API Gateway 的职责边界，而不是提出新的算法或系统实现。
- 它把 API Gateway 定义为**基础设施入口层**，负责路由、SSL 终止、鉴权令牌校验、限流、流量分发等，通常不承载业务逻辑。
- 它把 BFF 定义为**面向具体客户端的后端适配层**，负责从多个微服务聚合数据、裁剪字段、转换成 UI 友好的结构，并适配分页、排序等差异。
- 文中给出推荐组合方式：**Client → API Gateway → BFF → Microservices**，即网关管通用基础设施，BFF 管客户端定制逻辑。
- 文章还给出决策准则：多客户端、遗留/原始后端数据、多服务聚合、前后端独立迭代、性能敏感场景更适合 BFF；而单后端、简单系统、响应已匹配 UI、统一团队协作时则不一定需要。

## Results
- 这不是一篇实验型论文，**没有提供定量实验结果、基准数据集、指标提升或统计对比数字**。
- 文中最强的具体主张是：在成熟微服务架构中，推荐采用 **Client → API Gateway → BFF → Microservices** 的分层组合，而不是让 BFF 替代 API Gateway。
- 文章以 SoundCloud 作为案例背景，声称其将单一 API 拆分为多个面向客户端的 BFF 后，能够让不同团队**更快迭代**并更好地适配 Web 与移动端差异，但**没有给出速度提升百分比或性能数字**。
- 它明确指出移动端与 Web 端的需求差异示例：移动端可请求 **10 items/page**，而 Web 端可请求 **50 items/page**，说明 BFF 的价值在于按客户端需求定制接口，而不是统一暴露原始后端能力。
- 文章的结论性结果是：对小型、低负载、单客户端、低转换需求系统，可以临时合并 BFF 与网关职责；但随着系统增长，**职责分离通常会带来更清晰、更可扩展的架构**。

## Link
- [https://reactdevelopment.substack.com/p/when-to-use-bff-and-should-it-replace](https://reactdevelopment.substack.com/p/when-to-use-bff-and-should-it-replace)
