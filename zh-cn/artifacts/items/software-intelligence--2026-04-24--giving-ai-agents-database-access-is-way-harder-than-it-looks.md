---
source: hn
url: https://querybear.com/blog/architecture-of-querybear
published_at: '2026-04-24T23:06:19'
authors:
- dispencer
topics:
- ai-agents
- database-security
- sql-guardrails
- prompt-injection
- defense-in-depth
relevance_score: 0.87
run_id: materialize-outputs
language_code: zh-CN
---

# Giving AI Agents Database Access Is Way Harder Than It Looks

## Summary
## 摘要
这篇文章认为，要让 AI 代理安全访问数据库，需要多层防护，不能只靠一次只读检查。文章介绍了 QueryBear 的纵深防御设计，用来限制有害 SQL、数据泄露和资源滥用。

## 问题
- 具有数据库访问权限的 AI 代理，即使用的是名义上的只读账号，也可能发出破坏性、高成本或范围过大的查询。
- 简单控制在常见场景下会失效：基于正则的 SQL 过滤容易漏掉规避技巧，只读角色挡不住 `pg_sleep` 或超大连接查询，而合法的 join 仍可能暴露凭证或令牌等敏感列。
- 数据库内容本身也可能把对抗性文本注入代理的上下文，从而带来来自存储数据的提示注入风险。

## 方法
- 核心方法是分层的“洋葱”设计：先从默认拒绝访问开始，再只放开代理确实需要的表、列和查询能力。
- QueryBear 给出的防护层包括：严格的 SQL 解析器、表和列的允许列表、在 AST 层面对查询做重写以加入限制和超时、执行前成本检查、数据库层的只读事务、语句超时，以及完整的审计日志。
- 机制很直接：每一道防护都覆盖另一道防护可能漏掉的一类失效模式，因此系统不依赖某一个完美检查。
- 测试方法是对抗式的。文章主张测试提示注入载荷、多语句攻击，以及语法合法但在运行上不安全的查询。

## 结果
- 摘录中没有提供量化基准结果。
- 最明确的具体主张是架构层面的：QueryBear 表示，它已经运行了一套包含 SQL 解析、允许列表、AST 重写、成本检查、数据库只读约束、语句超时和审计日志的栈。
- 文章给出了这些防护层试图阻止的具体失效案例：用注释技巧隐藏的 `DELETE`、`SELECT pg_sleep(3600)` 导致连接耗尽、返回 5 亿行结果的 12 表笛卡尔连接，以及暴露 `oauth_tokens` 的 join。
- 文中声称的收益是，在提示注入、高成本查询和未授权读取等现实失效模式下，代理访问数据库会更安全；但摘录没有报告事件减少、延迟变化或攻击成功率下降等实测结果。

## Problem

## Approach

## Results

## Link
- [https://querybear.com/blog/architecture-of-querybear](https://querybear.com/blog/architecture-of-querybear)
