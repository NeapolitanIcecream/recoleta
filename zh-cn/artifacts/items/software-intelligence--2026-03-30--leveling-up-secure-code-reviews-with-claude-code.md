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
这篇文章认为，在应用上下文和响应规则足够明确时，Claude Code 能让人工主导的安全代码审查在陌生代码库上更快完成。作者把它当作代码理解助手，而不是自动漏洞发现器，这样可以减少误报，并产出更易读的安全分析过程。

## 问题
- 在渗透测试中，如果测试人员接触到陌生的语言、框架或架构，手工安全代码审查会很慢。
- 直接用“查找漏洞”这类通用提示，会产生很多质量不高的发现和误报，最后还是要人工筛选。
- 异步工作流和多阶段请求处理这类复杂路径很难靠人工逐步追踪，容易漏掉与安全相关的输入流。

## 方法
- 这个方法的核心是一份详细的系统提示词，其中包含应用描述、授权模型、API 参考、组件路径、期望输出格式和安全审查角色设定。
- 审查者会针对每条调查线程新开一个 Claude 交互会话，然后提出范围很窄的问题，比如枚举守护进程，或从头到尾追踪某个 HTTP 端点。
- 系统要求 Claude 输出易读的代码流分析，包括代码片段、源与汇的映射、正向安全观察、需要检查的控制缺口，以及置信度等级。
- 这个流程仍由人工掌控：审查者可以接受或拒绝 Claude 的注释，在 Claude 事实出错时更新提示上下文，并使用单独的 `[TeachMe]` 模式来针对性解释语言或框架行为。
- 文章还建议，对私有代码应使用自托管或本地部署，避免把客户 IP 发送给公共托管模型。

## 结果
- 文章没有提供正式基准、全数据集指标或受控对比。
- 在 BloodHound Community Edition 中，Claude 识别出异步守护进程，并按功能分组，还报告说工作进程从 **3 个 PostgreSQL 表** 中获取任务，作者据此优先分析篡改风险。
- 对于 `POST /api/v2/graphs/cypher` 路径，Claude 从路由注册开始，一直到解析和查询生成，重建了端到端流程；作者说，这暴露出提交的 Cypher 会先用 **ANTLR** 分词，再过滤变更操作和被阻止的过程，最后转换为 PostgreSQL 查询。
- 基于这段分析，作者得出结论：该实现对这条路径“有效消除了传统 SQL 注入”，但仍有必要检查过程过滤的遗漏和访问控制问题。
- Claude 在分析中至少有一次事实错误，把 Neo4j 说成了数据库；作者更正为 BloodHound 使用的是 **PostgreSQL**，而且 DAWGS 负责 Cypher 到 PostgreSQL 的转换。
- 在 BadWindowsService 上，Claude 判断该服务是故意设计成可被利用的，并输出了一张包含安全相关特性的信息表和后续的概念验证 PowerShell 脚本，但作者说漏洞列表并不完整。

## Problem

## Approach

## Results

## Link
- [https://specterops.io/blog/2026/03/26/leveling-up-secure-code-reviews-with-claude-code/](https://specterops.io/blog/2026/03/26/leveling-up-secure-code-reviews-with-claude-code/)
