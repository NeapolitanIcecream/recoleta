---
source: hn
url: https://reactdevelopment.substack.com/p/when-to-use-bff-and-should-it-replace
published_at: '2026-03-05T23:30:00'
authors:
- javatuts
topics:
- backend-for-frontend
- api-gateway
- software-architecture
- microservices
- frontend-backend-integration
relevance_score: 0.28
run_id: materialize-outputs
---

# When to Use BFF and Should It Replace API Gateway?

## Summary
这篇文章解释了 BFF（Backend for Frontend）与 API Gateway 的职责差异，并给出何时引入、何时避免、以及何时两者应协同工作的架构判断。核心观点是：BFF 负责面向客户端的数据整形与聚合，API Gateway 负责通用基础设施入口，两者通常不应互相替代。

## Problem
- 文章要解决的问题是：在现代后端架构中，团队何时需要 BFF、它是否应取代 API Gateway，以及在单前端或多前端场景下如何避免过度设计或职责混乱。
- 这很重要，因为前端若直接对接多个后端服务，会承担请求编排、响应转换、错误处理、分页过滤等复杂逻辑，导致客户端复杂、演进缓慢。
- 若把 API Gateway 与 BFF 混为一体，系统早期看似简单，但随着业务增长会把路由、安全、限流、聚合、转换、缓存等职责堆到同一组件中，增加维护成本。

## Approach
- 文章采用架构模式对比的方法，先定义 BFF 的来源与目标，再对比 API Gateway 的典型职责，澄清二者不是同一种组件。
- 用最简单的话说：API Gateway 像“总入口门卫”，负责把请求安全地转发到正确服务；BFF 像“为某个前端定制的服务员”，负责把多个后端的数据整理成该客户端最需要的样子。
- 给出推荐链路：**Client → API Gateway → BFF → Microservices**，其中 Gateway 处理 SSL、认证、限流、路由等基础设施问题，BFF 处理聚合、裁剪字段、适配分页/排序、补充界面专用字段等客户端逻辑。
- 通过场景化准则说明何时使用：当存在多客户端、遗留或原始后端数据、页面需跨服务聚合、前端团队需要独立迭代、或需减少客户端请求时，BFF 更有价值；系统简单、单后端服务、返回已匹配 UI 时则可不引入。
- 文章还从组织协作角度讨论 BFF 归属，指出其可由前端团队维护，但运行上仍属于后端组件。

## Results
- 文章**没有提供实验、基准测试或正式量化指标**，因此没有可报告的准确数据、数据集或数值提升。
- 最强的具体结论是：在成熟架构中，推荐将 API Gateway 与 BFF 分层协作，而不是让 BFF 替代 Gateway；典型请求路径为 **Client → API Gateway → BFF → Microservices**。
- 文中给出的明确经验性收益包括：BFF 可为不同客户端返回不同形态的数据，例如移动端返回更小 payload、Web 端返回更丰富数据、管理后台暴露运维信息。
- 文章引用 SoundCloud 的实践作为案例，声称将单一 API 拆分为按客户端定制的多个 BFF 后，团队能更快迭代，并减少统一后端 API 成为瓶颈的问题，但**未给出具体速度、延迟或成本数字**。
- 对是否合并 BFF 与 API Gateway 的结论是：在“小型内部应用 + 单客户端 + 简单后端 + 低负载 + 最少数据转换”场景下可以接受；一旦进入持续增长的微服务环境，职责分离通常更易维护且更具扩展性。

## Link
- [https://reactdevelopment.substack.com/p/when-to-use-bff-and-should-it-replace](https://reactdevelopment.substack.com/p/when-to-use-bff-and-should-it-replace)
