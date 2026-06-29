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
## 总结
1Password 表示，在工作有清晰规格、确定性分析工具，以及用于排序风险的人类复核时，AI 代理帮助重构了多百万行 Go 单体应用的部分代码。

## 问题
- 1Password 需要在保留生产流量下的隐私、性能、可靠性和安全性的同时，拆分 B5 这个大型 Go 单体应用中的服务边界。
- 提取顺序很重要，因为共享 schema、写入路径或所有权边界上的错误排序会引发隐蔽的生产故障。
- 另一个清理任务需要修改 3,000 多个 `MustBegin` 事务调用点，这个待办项范围太大，不能只靠人工清理。

## 方法
- 团队使用 Go SSA 分析、SQL 解析和 DataDog MCP 运行时数据构建了一套代理式工具链，用来映射领域所有权、耦合关系和提取顺序。
- 代理帮助编写了确定性的分析器和清单；工程师随后审核稳定的产物，而不是反复依赖模型解释。
- 对于 `MustBegin` 迁移，团队生成了调用点清单，把它们按模式分组，编写了模板，并给代理提供了带有停止和上报规则的操作手册。
- 多个代理通过 git worktree 并行运行，这样每个变更集都能保持隔离。
- 在服务提取任务中，工程师发现代理需要明确的不变量、schema 排序规则、部署顺序和共享数据所有权约束。

## 结果
- 提取分析覆盖了数百万行 Go 代码，并给出了与资深工程判断一致的顺序：先 Vault，再 Billing，然后是 AuthN 和 AuthZ，同时保留 Identity 作为核心。
- `MustBegin` 迁移覆盖了 3,000 多个生产和测试调用点；在团队完成工具和规格之后，代理执行用了几个小时。
- 服务提取任务只带来了大约 20-30% 的生产力提升，因为代理会犯顺序错误，还需要人工协调。
- 一个失败案例是在修改插入代码之前回填 UUID 列，这本来可能导致静默数据丢失。
- 另一个失败案例把某个标识符推断成 ULID，并把这个假设扩散到后续修改中，迫使团队回滚该会话。
- 为分析新增的仪表化也改善了 DataDog 中端到端事务可见性，超出了重构项目本身。

## Problem

## Approach

## Results

## Link
- [https://1password.com/blog/what-we-learned-using-ai-agents-to-refactor-a-monolith](https://1password.com/blog/what-we-learned-using-ai-agents-to-refactor-a-monolith)
