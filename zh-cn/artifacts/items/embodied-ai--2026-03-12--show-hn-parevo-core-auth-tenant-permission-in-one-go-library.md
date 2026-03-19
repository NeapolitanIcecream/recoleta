---
source: hn
url: https://github.com/parevo/core
published_at: '2026-03-12T23:53:15'
authors:
- parevo
topics:
- go-library
- authentication
- multi-tenancy
- access-control
- backend-infrastructure
relevance_score: 0.01
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Parevo Core – Auth, tenant, permission in one Go library

## Summary
Parevo Core 是一个与框架和存储无关的 Go 库，把认证、多租户和权限管理整合到同一套组件中，目标是减少应用后端重复建设。它主要面向工程集成与产品开发效率，而不是机器人或基础模型研究问题。

## Problem
- 它要解决的是后端系统中**认证、租户隔离、权限控制**通常分散实现、重复开发、难以统一维护的问题。
- 这很重要，因为这些能力几乎是 SaaS 和企业应用的基础设施；若集成碎片化，会增加安全风险、开发成本和迁移难度。
- 文本中强调还要兼顾不同 Web 框架和不同数据库/缓存后端，避免被单一技术栈绑定。

## Approach
- 核心方法是提供**一个统一的 Go 库**，把 auth、tenant、permission 三类能力放进同一个可组合的服务层中。
- 在认证上，它内置多种常见机制：JWT、OAuth2、SAML、LDAP、API keys、WebAuthn、magic link。
- 在多租户上，它提供 tenant context、tenant lifecycle、feature flags，帮助应用在请求和业务层处理中携带租户信息。
- 在权限上，它支持 RBAC、ABAC 和 cached checks，用统一方式做角色/属性访问控制与权限校验加速。
- 为了易集成，它同时宣称 framework-agnostic 和 storage-agnostic，可接入 net/http、chi、gin、echo、fiber、GraphQL，以及 MySQL、Postgres、MongoDB、Redis、memory。

## Results
- 提供的文本**没有给出论文式定量结果**，没有准确的 benchmark、数据集、延迟、吞吐、安全性提升百分比或与基线方法的数值比较。
- 最具体的工程性结果是功能覆盖：**7 类认证方式**（JWT、OAuth2、SAML、LDAP、API keys、WebAuthn、magic link）。
- 最具体的兼容性结果是支持 **6 类框架/接口**（net/http、chi、gin、echo、fiber、GraphQL）。
- 最具体的存储覆盖是支持 **6 类后端**（MySQL、Postgres、MongoDB、Redis、memory，再加上 storage-agnostic 的适配思路）。
- 文本还给出了多个可运行示例：**5 个示例入口**（nethttp-basic、gin-modular、notification、blob、admin-panel），说明其可用性主张偏向实际工程落地而非研究突破。

## Link
- [https://github.com/parevo/core](https://github.com/parevo/core)
