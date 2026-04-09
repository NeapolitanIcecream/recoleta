---
source: hn
url: https://specterops.io/blog/2026/03/26/leveling-up-secure-code-reviews-with-claude-code/
published_at: '2026-03-30T23:51:40'
authors:
- vinhnx
topics:
- secure-code-review
- llm-assisted-analysis
- code-intelligence
- application-security
- prompt-engineering
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Leveling Up Secure Code Reviews with Claude Code

## Summary
## 摘要
这篇文章认为，在提示词提供充分的应用上下文和明确的输出规则时，Claude Code 能让以人为主导的安全代码审查在面对陌生代码库时更快推进。作者把它当作帮助理解代码的助手，而不是自主发现漏洞的工具，这样可以减少误报，并产出可读性更好的、聚焦安全的代码流程说明。

## 问题
- 在渗透测试中，当测试人员进入一个使用陌生语言、框架或架构构建的应用时，手动安全代码审查推进缓慢。
- 使用泛化的“寻找漏洞”提示词会产生大量质量不高的发现和误报，仍然需要人工筛选。
- 异步工作流水线和多阶段请求处理这类复杂路径很难靠手工追踪，容易掩盖与安全相关的输入流。

## 方法
- 这套方法以一条详细的系统提示词为中心，其中提供应用描述、授权模型、API 参考、组件路径、期望输出格式，以及一个安全审查角色设定。
- 审查者会为每条调查线索启动一个新的交互式 Claude 会话，然后提出范围很窄的问题，例如枚举守护进程，或端到端追踪某个 HTTP 端点。
- Claude 需要产出易于理解的代码流程说明，其中包括代码片段、source 和 sink 映射、正面的安全观察、需要检查的控制缺口，以及置信度。
- 这个流程由人工主导：审查者接收或否决 Claude 的注释，在 Claude 事实出错时更新提示词上下文，并使用单独的 `[TeachMe]` 模式来定向解释某种语言或框架的行为。
- 文章还建议，对私有代码使用自托管或本地部署，避免把客户 IP 发送到公开托管模型。

## 结果
- 文章没有提供正式基准、全数据集指标或受控对比。
- 在 BloodHound Community Edition 中，Claude 识别出异步守护进程，按功能进行了分组，并报告这些工作进程会从 **3 张 PostgreSQL 表** 中消费任务，作者据此优先分析篡改风险。
- 对于 `POST /api/v2/graphs/cypher` 路径，Claude 重建了从路由注册到解析和查询生成的端到端流程；作者说，这让他看到提交的 Cypher 会先用 **ANTLR** 分词，随后过滤修改操作和被阻止的过程，再被转换为 PostgreSQL 查询。
- 基于这份流程说明，作者认为该实现“有效消除了传统 SQL 注入”在该路径上的风险，同时仍有必要继续检查过程过滤是否有遗漏，以及访问控制方面的问题。
- 在分析过程中，Claude 至少出现过一次事实错误，声称 Neo4j 是数据库；作者随后更正并记录了 BloodHound 使用 **PostgreSQL**，且 DAWGS 负责将 Cypher 转换为 PostgreSQL 这一事实。
- 在 BadWindowsService 上，Claude 判断该服务是刻意设计成带漏洞的，并生成了一张与安全相关特性的表格，以及后续的概念验证 PowerShell 脚本，但作者表示那份漏洞列表并不完整。

## Problem

## Approach

## Results

## Link
- [https://specterops.io/blog/2026/03/26/leveling-up-secure-code-reviews-with-claude-code/](https://specterops.io/blog/2026/03/26/leveling-up-secure-code-reviews-with-claude-code/)
