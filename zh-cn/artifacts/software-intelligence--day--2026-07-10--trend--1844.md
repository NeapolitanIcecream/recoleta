---
kind: trend
trend_doc_id: 1844
granularity: day
period_start: '2026-07-10T00:00:00'
period_end: '2026-07-11T00:00:00'
topics:
- coding agents
- software testing
- formal verification
- agent memory
- reusable skills
run_id: materialize-outputs
aliases:
- recoleta-trend-1844
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-testing
- topic/formal-verification
- topic/agent-memory
- topic/reusable-skills
language_code: zh-CN
---

# 当规范变得可执行且可复用时，编码代理的表现会提升

## Overview
当天最有价值的工作将大语言模型（LLM）编码作为受控的工程流程。ReProAgent和TestAgent把仓库上下文与运行时反馈连接起来，DualVeri则将机器检查的证明与针对实际实现的测试结合起来。可复用的任务上下文也成为降低成本、提高完成率的实际手段。

## Clusters

### 可执行测试与适配代理的缺陷报告
ReProAgent通过仓库探索、代码图检索和运行时验证，将问题报告转换为从失败到通过的测试。它在SWT-bench-lite问题集上复现了58.43%的问题，在SWT-bench-verified问题集上复现了70.30%，平均每个问题的成本为$0.14。TestAgent围绕测试专用仓库图使用规划器、生成器和审查器。在六个Java项目上，它达到了92.34%的代码行覆盖率和83.69%的变异分数；它还以92.22%的精确率检测出154个真实缺陷。

输入报告与执行循环同样重要。对441份SWE-bench Verified缺陷报告的分析发现，受影响代码的位置和建议修复方案与修复成功的正相关性最强。这说明简洁的报告有助于缩小搜索和修复范围。

#### Evidence
- [ReProAgent: Tool-Augmented Multi-Stage Agentic Generation of Bug Reproduction Tests from Issue Reports](../Inbox/2026-07-10--reproagent-tool-augmented-multi-stage-agentic-generation-of-bug-reproduction-tests-from-issue-reports.md): 介绍ReProAgent的分阶段方法、基准复现率和成本。
- [Multi-Agent LLM Collaboration for Unit Test Generation via Human-Testing-Inspired Workflows](../Inbox/2026-07-10--multi-agent-llm-collaboration-for-unit-test-generation-via-human-testing-inspired-workflows.md): 提供TestAgent的工作流、覆盖率、变异分数和缺陷检测结果。
- [Writing Bug Reports for Software Repair Agents: What Information Matters Most?](../Inbox/2026-07-10--writing-bug-reports-for-software-repair-agents-what-information-matters-most.md): 支持定位线索和建议修复方案有助于修复代理这一发现。

### 证明与测试作为互补检查
DualVeri使用共享属性模板进行Lean 4证明，并针对PySpark开展基于属性的测试。在400个候选属性上，模板使证明合成成功率平均提高1.6倍，将证明幻觉减少59%，并将测试意图不匹配的数量从22降至1。证明结果与执行结果之间的不一致暴露了形式化模型与运行时行为之间的缺口。

Diversify2Verify增加了另一种有效控制：在固定契约下生成多个实现。数组、列表、递归式和命令式变体在73个任务中的49个任务上至少生成了一个通过验证的产物，任务成功率为67.1%。因此，即使不同变体针对同一任务，验证成功率也部分取决于实现结构。

#### Evidence
- [Agentic Proof and Property-Based Testing via Property-Templates in Data-Intensive Computing](../Inbox/2026-07-10--agentic-proof-and-property-based-testing-via-property-templates-in-data-intensive-computing.md): 详细说明DualVeri结合证明与测试的设计及测得的收益。
- [Diversifying to Verify: When Task-Equivalent Programs Differ in Verifiability](../Inbox/2026-07-10--diversifying-to-verify-when-task-equivalent-programs-differ-in-verifiability.md): 报告多种表示形式和控制流变体下的验证率。

### 面向重复代理工作的选择性复用
选择性持久记忆保存任务规范、数据模式、工具设置和输出约束，同时排除临时轨迹。在24个反复执行的企业任务上，它的完成率达到96%，无状态会话为79%，完整历史记忆为71%。对于兼容的数据刷新，18个任务全部无需再次调用LLM即可完成。

公开技能仓库显示，复用程度仍不均衡。在11,497个软件工程技能中，实现、测试和代码审查占65.4%。只有13.6%包含可执行代码资产，需求、发布和部署合计占10.7%。大多数已发布技能仍以说明文档为主，经过测试的可执行组件仍有很大补充空间。

#### Evidence
- [Shared Selective Persistent Memory for Agentic LLM Systems](../Inbox/2026-07-10--shared-selective-persistent-memory-for-agentic-llm-systems.md): 提供选择性记忆的设计、完成率、令牌数据和零令牌刷新结果。
- [Inside the Skill Market: From Software Engineering Activities to Reusable Agent Skills](../Inbox/2026-07-10--inside-the-skill-market-from-software-engineering-activities-to-reusable-agent-skills.md): 提供11,497个代理技能的生命周期覆盖率和可执行资产统计数据。
