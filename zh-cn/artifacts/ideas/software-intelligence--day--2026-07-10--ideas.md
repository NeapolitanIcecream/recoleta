---
kind: ideas
granularity: day
period_start: '2026-07-10T00:00:00'
period_end: '2026-07-11T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- software testing
- formal verification
- agent memory
- reusable skills
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-testing
- topic/formal-verification
- topic/agent-memory
- topic/reusable-skills
language_code: zh-CN
---

# 编码代理可靠性系统

## Summary
编码代理团队可以通过将问题接收转换为失败后通过的测试、将反复出现的正确性断言编码为共享证明和基于属性的测试模板，以及在重复任务之间保留获批准的仓库上下文来提高可靠性。每项改动都可以先在少量真实维护任务上测试，再扩大采用范围。

## 生成已验证失败后通过测试的问题接收流程
增加一个自动分流步骤，将每个新问题转换为一个测试：测试在报告所针对的版本上失败，在已接受的修复之后通过。该流程应检索仓库结构，运行候选测试，并将疑似文件或函数以及建议的修复方向返回给维护者审核。ReProAgent 在 SWT-bench-verified 中复现了 70.30% 的问题，平均每个问题的成本为 $0.14；另一项 SWE-bench Verified 研究发现，受影响代码的位置和建议修复与代理修复成功率之间的正相关最明显。可以使用最近关闭的 50 个缺陷进行试验：隐藏最终补丁，生成测试和定位提示，然后测量有效复现率、维护者审核时间以及后续补丁通过率。

### Evidence
- [ReProAgent: Tool-Augmented Multi-Stage Agentic Generation of Bug Reproduction Tests from Issue Reports](../Inbox/2026-07-10--reproagent-tool-augmented-multi-stage-agentic-generation-of-bug-reproduction-tests-from-issue-reports.md): 报告了 ReProAgent 的复现率、每个问题的成本以及对后续修复的改进。
- [ReProAgent: Tool-Augmented Multi-Stage Agentic Generation of Bug Reproduction Tests from Issue Reports](../Inbox/2026-07-10--reproagent-tool-augmented-multi-stage-agentic-generation-of-bug-reproduction-tests-from-issue-reports.md): 将失败后通过的测试定义为可执行规范，用于补丁验证和自动修复。
- [Writing Bug Reports for Software Repair Agents: What Information Matters Most?](../Inbox/2026-07-10--writing-bug-reports-for-software-repair-agents-what-information-matters-most.md): 研究发现，定位线索和建议修复可以缩小搜索与修复范围，并且与成功修复呈正相关。

## 用于证明和运行时测试的共享属性模板
维护查询引擎、编译器、数据类库或优化规则的团队，可以将反复出现的正确性断言保存为参数化模板，并为其配套 Lean 4 证明义务和基于属性的测试。编码代理填写特定属性的空缺，CI 则将机器检查过的模型与实际实现进行比较。DualVeri 使证明合成成功率平均提高了 1.6×，将证明幻觉减少了 59%，并在 400 个候选属性中将基于属性的测试意图不匹配数量从 22 降至 1。可以先选择一个重复出现的属性族，例如优化器等价性或聚合分解，在 20 到 30 个属性上跟踪模板完成情况、证明失败、运行时反例以及模型与实现之间的不一致。

### Evidence
- [Agentic Proof and Property-Based Testing via Property-Templates in Data-Intensive Computing](../Inbox/2026-07-10--agentic-proof-and-property-based-testing-via-property-templates-in-data-intensive-computing.md): 介绍了共享证明模板和基于属性的测试模板、评估设计，以及在 400 个属性上测得的改进。
- [Agentic Proof and Property-Based Testing via Property-Templates in Data-Intensive Computing](../Inbox/2026-07-10--agentic-proof-and-property-based-testing-via-property-templates-in-data-intensive-computing.md): 解释了形式化证明和针对实际实现的基于属性测试各自覆盖的范围。
- [Agentic Proof and Property-Based Testing via Property-Templates in Data-Intensive Computing](../Inbox/2026-07-10--agentic-proof-and-property-based-testing-via-property-templates-in-data-intensive-computing.md): 说明了为什么可以将数据系统中反复出现的属性族编码一次，再用于不同 API。

## 用于重复性维护任务的版本化仓库上下文
将获批准的任务规范、模式、工具设置和输出约束保存在带版本控制的工作区中，用于依赖更新、发布准备和定期报告生成等重复性编码代理任务。排除推理轨迹、失败的恢复路径、原始数据和临时工具日志；通过稳定的运行时接口刷新兼容输入。在对 24 个重复性企业任务的评估中，选择性记忆的完成率达到 96%，无状态会话为 79%，保留完整历史记录的记忆为 71%。公开的软件工程技能仓库也显示出打包不足：11,497 个技能中有 63.8% 只包含说明，13.6% 包含可执行代码资产。团队可以在一个月度维护流程上测试这种方法，连续运行三个周期，测量完成率、纠正轮次、令牌用量以及由过时上下文导致的失败。

### Evidence
- [Shared Selective Persistent Memory for Agentic LLM Systems](../Inbox/2026-07-10--shared-selective-persistent-memory-for-agentic-llm-systems.md): 说明了可复用的上下文类别、排除的临时材料、完成率结果和零令牌刷新机制。
- [Shared Selective Persistent Memory for Agentic LLM Systems](../Inbox/2026-07-10--shared-selective-persistent-memory-for-agentic-llm-systems.md): 报告了对比完成率，并解释了带版本控制的工件和兼容数据刷新。
- [Inside the Skill Market: From Software Engineering Activities to Reusable Agent Skills](../Inbox/2026-07-10--inside-the-skill-market-from-software-engineering-activities-to-reusable-agent-skills.md): 量化了 11,497 个软件工程技能中仅含说明的技能比例，以及包含可执行资产的技能比例。
