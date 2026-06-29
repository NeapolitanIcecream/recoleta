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
## 总结
这篇文章的观点是，给 AI agent 安全地访问数据库，需要多层防护，而不是只做一次只读检查。文章介绍了 QueryBear 的纵深防御设计，用来限制有害 SQL、数据泄露和资源滥用。

## 问题
- 即使使用名义上的只读账号，能访问数据库的 AI agent 也可能发出破坏性、代价高或范围过大的查询。
- 简单控制在常见场景下会失效：正则 SQL 过滤会漏掉技巧性写法，只读角色挡不住 `pg_sleep` 或超大连接，合法的连接查询也可能暴露凭证或 token 等敏感列。
- 数据库内容还会把对抗性文本注入 agent 的上下文，从而带来来自存储数据的提示注入风险。

## 方法
- 核心方法是分层的“洋葱”设计：先默认拒绝访问，再只放行 agent 需要的精确表、列和查询能力。
- QueryBear 说明的层包括严格的 SQL 解析器、表和列白名单、在 AST 层重写查询以加入限制和超时、执行前成本检查、数据库级只读事务、语句超时和完整审计日志。
- 机制很直接：每一道防护都覆盖另一道防护可能漏掉的失败模式，这样系统就不依赖某一个完美检查。
- 测试方法是对抗式的。文章要求测试提示注入载荷、多语句攻击，以及语法合法但运行上不安全的查询。

## 结果
- 这段摘录没有提供定量基准结果。
- 最明确的具体说法是架构层面的：QueryBear 说它已经运行一套包含 SQL 解析、白名单、AST 重写、成本检查、数据库只读强制、语句超时和审计日志的栈。
- 文章给出了这些层要拦住的具体失败例子：用注释技巧隐藏的 `DELETE`、耗尽连接的 `SELECT pg_sleep(3600)`、返回五亿行的 12 表笛卡尔连接，以及暴露 `oauth_tokens` 的连接查询。
- 文章声称的收益是在提示注入、昂贵查询和未授权读取等现实失败模式下，让 agent 的数据库访问更安全，但这段摘录没有报告事故、延迟或攻击成功率的实际下降。

## Problem

## Approach

## Results

## Link
- [https://querybear.com/blog/architecture-of-querybear](https://querybear.com/blog/architecture-of-querybear)
