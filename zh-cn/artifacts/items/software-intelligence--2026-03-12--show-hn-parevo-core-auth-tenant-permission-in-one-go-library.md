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
- authorization
- developer-tooling
relevance_score: 0.54
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Parevo Core – Auth, tenant, permission in one Go library

## Summary
Parevo Core 是一个面向 Go 的框架无关库，把认证、多租户与权限管理整合到同一个组件中，目标是减少业务系统重复搭建基础安全与租户能力的成本。它更像工程基础设施库而非研究论文，强调可插拔、跨存储和跨 Web 框架复用。

## Problem
- 现代软件系统常需要同时处理认证、租户隔离和权限控制，但这些能力通常分散实现，增加了集成复杂度与维护成本。
- 多租户 SaaS 或平台型系统若缺少统一的 tenant context、权限模型和认证入口，容易出现安全漏洞、逻辑重复和框架绑定问题。
- 这件事重要，因为认证授权与租户隔离是生产系统的核心基础设施，直接影响安全性、开发速度与可扩展性。

## Approach
- 核心方法是把 **auth + tenant + permission** 三类常见基础能力封装进一个统一的 Go 库，让开发者通过少量配置即可接入。
- 认证层支持多种机制：JWT、OAuth2、SAML、LDAP、API keys、WebAuthn、magic link，以同一服务接口暴露。
- 多租户层提供 tenant context、tenant lifecycle 和 feature flags，帮助应用在请求处理中携带并管理租户状态。
- 权限层结合 RBAC、ABAC 和 cached checks，在角色规则与属性规则之间提供统一授权检查。
- 该库通过 storage-agnostic 与 framework-agnostic 设计适配 MySQL、Postgres、MongoDB、Redis、memory，以及 net/http、chi、gin、echo、fiber、GraphQL，核心机制就是“统一抽象 + 适配器”。

## Results
- 文本**没有提供定量实验结果**，没有论文式 benchmark、数据集、准确率、延迟或与基线方法的数字对比。
- 最强的具体主张是：单库同时覆盖 **3 类核心能力**（auth、multi-tenant、permission），减少分别选型和手工拼装的工作。
- 认证能力宣称支持 **7 种机制**：JWT、OAuth2、SAML、LDAP、API keys、WebAuthn、magic link。
- 存储适配宣称覆盖 **5 类后端**：MySQL、Postgres、MongoDB、Redis、memory。
- 框架适配宣称覆盖 **6 类接口/框架**：net/http、chi、gin、echo、fiber、GraphQL。
- 仓库给出多个可运行示例，包括 **nethttp-basic、gin-modular、notification、blob、admin-panel**，表明其重点是工程落地性而非研究突破。

## Link
- [https://github.com/parevo/core](https://github.com/parevo/core)
