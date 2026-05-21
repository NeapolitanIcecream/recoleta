---
source: hn
url: https://1password.com/blog/what-we-learned-using-ai-agents-to-refactor-a-monolith
published_at: '2026-05-13T23:33:13'
authors:
- cdrnsf
topics:
- agentic-refactoring
- code-intelligence
- software-engineering-agents
- monolith-decomposition
- production-migration
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# What we learned using AI agents to refactor a monolith

## Summary
## 摘要
1Password 报告称，在规格明确、分析工具具备确定性，并由人工审查排序风险时，AI agent 帮助重构了一个数百万行 Go 单体应用的部分代码。

## 问题
- 1Password 需要在大型 Go 单体应用 B5 内拆分服务边界，同时在生产流量下保持隐私、性能、可靠性和安全性。
- 提取顺序很关键，因为共享 schema、写入路径或所有权边界中的错误排序可能导致隐蔽的生产故障。
- 另一项清理工作需要修改 3,000 多个 `MustBegin` 事务调用点，单靠人工清理难以处理这类范围过大的积压任务。

## 方法
- 团队构建了一套 agent 工具链，使用 Go SSA 分析、SQL 解析和 DataDog MCP 运行时数据来映射领域所有权、耦合关系和提取顺序。
- Agent 帮助编写确定性分析器和 manifest；工程师随后审查稳定产物，而不是依赖模型反复解释。
- 对于 `MustBegin` 迁移，团队生成了调用点 manifest，将它们按模式分组，编写模板，并给 agent 提供了包含停止并上报规则的操作手册。
- 多个 agent 通过 git worktree 并行运行，使每个变更集保持隔离。
- 在服务提取中，工程师发现 agent 需要明确的不变量、schema 排序规则、部署顺序和共享数据所有权约束。

## 结果
- 提取分析覆盖了数百万行 Go 代码，并产出了与资深工程判断一致的顺序：先是 Vault，然后是 Billing，再是 AuthN 和 AuthZ，同时将 Identity 保留为核心。
- `MustBegin` 迁移覆盖了 3,000 多个生产和测试调用点；团队构建工具和规格后，agent 执行只用了数小时。
- 服务提取任务只带来了约 20-30% 的生产率提升，因为 agent 会犯排序错误，并且需要人工协调。
- 一个失败案例在修改插入代码前回填了 UUID 列，这可能导致静默数据丢失。
- 另一个失败案例推断某个标识符是 ULID，并将这一假设扩散到多个变更中，导致该会话必须回滚。
- 为分析添加的 instrumentation 也改善了 DataDog 中端到端事务的可见性，作用超出了这次重构项目。

## Problem

## Approach

## Results

## Link
- [https://1password.com/blog/what-we-learned-using-ai-agents-to-refactor-a-monolith](https://1password.com/blog/what-we-learned-using-ai-agents-to-refactor-a-monolith)
