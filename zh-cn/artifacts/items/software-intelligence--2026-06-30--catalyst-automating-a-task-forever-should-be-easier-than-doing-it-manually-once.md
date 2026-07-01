---
source: hn
url: https://www.serval.com/serval-news/introducing-catalyst-automating-a-task-forever-should-be-easier-than-doing-it-manually-once
published_at: '2026-06-30T23:05:57'
authors:
- emot
topics:
- ai-agents
- it-automation
- workflow-generation
- human-in-the-loop
- code-generation
- enterprise-it
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# Catalyst: Automating a task forever should be easier than doing it manually once

## Summary
## 摘要
Catalyst 是 Serval 的产品代理，可将自然语言自动化请求转换为 Serval 设置草案，覆盖集成、权限、触发器、工作流、技能和仪表盘。主要观点是：当创建自动化比手动处理一次任务更省力时，IT 团队会自动化更多任务。

## 问题
- IT 团队经常跳过自动化，因为构建自动化可能比处理一张工单耗时更久，例如手动添加电子邮件别名。
- Serval 表示，Workflow Builder 减少了编写工作流的工作量，但设置仍需要在集成、权限、触发器和路由上分别处理。
- 这一点很重要，因为重复的 IT 请求会增加手动工作量，而不安全的代理变更可能影响服务台行为、访问权限和第三方系统。

## 方法
- Catalyst 使用与对话用户相同的公开文档、面向用户的端点和权限，因此它可以配置该用户有权访问的同一批 Serval 资源。
- 基于文件系统的代理将 Serval 资源视为可编辑文件：工作流是 TypeScript，技能是 Markdown，集成或策略是类似 JSON 的数据。
- 该代理在沙盒中运行，可以搜索文档、执行命令、生成文件，并编写用于读取或拟议变更的临时工作流。
- Catalyst 会暂存拟议变更，而不直接应用；用户在标签页中查看已变更的资源，并发布已批准的变更。
- 团队可以要求第二人审批流程，对第三方系统的变更操作也必须先获批才能执行。

## 结果
- 文章没有给出基准评估、准确率指标、延迟指标，也没有与其他自动化代理做受控比较。
- Serval 表示，Workflow Builder 在 Catalyst 之前已投入生产运行 1 年，并让创建工作流比手动处理某些任务一次更容易。
- 在别名请求示例中，Catalyst 同时处理 4 个设置步骤：集成连接、权限、工作流创建，以及技能/路由设置。
- Catalyst Beta 会暂存 3 类资源的变更：Workflows、Skills 和 Dashboards。
- 暂存设计支持第二人审批，即必须由另一名团队成员在发布前批准。
- Serval 称，由于 Catalyst 能在介绍电话后构建常见自动化，一些客户交易在不到 1 周内完成。

## Problem

## Approach

## Results

## Link
- [https://www.serval.com/serval-news/introducing-catalyst-automating-a-task-forever-should-be-easier-than-doing-it-manually-once](https://www.serval.com/serval-news/introducing-catalyst-automating-a-task-forever-should-be-easier-than-doing-it-manually-once)
