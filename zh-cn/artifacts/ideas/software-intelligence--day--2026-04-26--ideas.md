---
kind: ideas
granularity: day
period_start: '2026-04-26T00:00:00'
period_end: '2026-04-27T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding-agents
- agent-evaluation
- benchmarks
- software-testing
- gpu-optimization
tags:
- recoleta/ideas
- topic/coding-agents
- topic/agent-evaluation
- topic/benchmarks
- topic/software-testing
- topic/gpu-optimization
language_code: zh-CN
---

# 可执行验证闭环

## Summary
可执行证据正在进入日常工程工作流。这里最明确的机会是：能指出失败步骤的 agent CI、面向业务逻辑的需求驱动测试生成，以及通过运行代码验证每次修改的 profiler 引导式 GPU 优化闭环。

## 面向 agent CI 的步骤级回归追踪
给 agent CI 运行加上步骤级故障图。直接用户是已经在交付带工具调用的多步骤 agent 的团队，因为端到端检查失败后，工程师往往还得手动翻 trace。AgentEval 给出了一个具体模板：分别给规划、工具选择、参数生成、执行和综合打分，再沿依赖关系把下游失败追溯回去。在论文报告的试点中，这把根因定位时间的中位数从 4.2 小时降到 22 分钟，并在四个月里发现了 23 个发布前回归。低成本的第一版不需要完整分类体系。可以先从一个工作流开始，记录每一步及其父步骤，为最常见的失败点加上类型化的通过/失败检查，并在运行出错时标出上游得分最低的步骤。如果这个视图能缩短某一类重复故障的分诊时间，就值得把它扩展到更多工作流。

### Evidence
- [AgentEval: DAG-Structured Step-Level Evaluation for Agentic Workflows with Error Propagation Tracking](../Inbox/2026-04-26--agenteval-dag-structured-step-level-evaluation-for-agentic-workflows-with-error-propagation-tracking.md): 提供了失败检测召回率、根因定位准确率、传播错误，以及为期四个月的 CI/CD 试点（发现 23 个回归并加快调试）的主要结果。
- [AgentEval: DAG-Structured Step-Level Evaluation for Agentic Workflows with Error Propagation Tracking](../Inbox/2026-04-26--agenteval-dag-structured-step-level-evaluation-for-agentic-workflows-with-error-propagation-tracking.md): 确认了论文把 agent 运行建模为评估 DAG 的方法，其中包含步骤级指标和自动根因归因。

## 面向业务逻辑缺陷、以需求为依据的单元测试生成
为承载业务规则的代码从产品需求生成测试。这适合维护企业服务的团队，因为这类系统的正确性常常取决于审批规则、策略检查、定价条件或工作流约束，而这些内容更多写在 PRD 和内部文档里，不在代码本身里。SeGa 说明了这件事现在为什么可行：它把需求文档转成结构化的功能条目，为目标方法检索相关部分，把这些内容转成明确的业务场景，再用这些场景驱动单元测试生成。在 4 个工业 Go 项目的 60 个业务逻辑缺陷上，它找到了 29 个，而对比基线只找到了 4 到 7 个。在 6 个生产代码库中，开发者确认并修复了 16 个此前未知的缺陷。一个合适的首次部署目标是需求文档稳定、且积压了线上遗漏逻辑缺陷的某个服务。衡量指标应是每批生成测试确认出的缺陷数，而不只是覆盖率或编译通过率。

### Evidence
- [Uncovering Business Logic Bugs via Semantics-Driven Unit Test Generation](../Inbox/2026-04-26--uncovering-business-logic-bugs-via-semantics-driven-unit-test-generation.md): 概述了由需求驱动的测试生成方法，并报告了缺陷检测和生产环境发现结果。
- [Uncovering Business Logic Bugs via Semantics-Driven Unit Test Generation](../Inbox/2026-04-26--uncovering-business-logic-bugs-via-semantics-driven-unit-test-generation.md): 说明了业务逻辑缺陷这一核心问题，以及基于需求文档的语义驱动测试生成方法。

## 带执行校验的 profiler 引导式 GPU 补丁生成
为 GPU kernel 建立一个从 profiler 到补丁的闭环，只针对已测得的瓶颈提出修改，并通过执行验证结果。第一批用户是性能工程师和 HPC 开发者，他们已经有 profiler 报告，但仍然需要手动把计数器和停顿 trace 翻译成代码修改。Optimas 给出了一个具体操作模式：把 profiler 输出压缩成小型诊断摘要，把编辑范围限制在受影响区域，要求每次修改都注明它处理的是哪条证据，然后编译、运行、检查正确性并记录加速效果。论文报告了 3,410 次实验，其中性能得到提升的运行占比超过 98.82%，平均加速幅度在 8.02% 到 79.09% 之间。论文还报告，在作者的设置里，只看代码的基线没有产生任何有效优化。一个低成本试点做法是选取一类有可重复基准测试的 kernel，把最热点的 kernel 和主要停顿信号总结成简洁提示词，再把实测收益与当前人工调优队列做对比。

### Evidence
- [Optimas: An Intelligent Analytics-Informed Generative AI Framework for Performance Optimization](../Inbox/2026-04-26--optimas-an-intelligent-analytics-informed-generative-ai-framework-for-performance-optimization.md): 包含了诊断引导优化、基于执行的验证、实验数量、成功率和加速效果的主要结论。
- [Optimas: An Intelligent Analytics-Informed Generative AI Framework for Performance Optimization](../Inbox/2026-04-26--optimas-an-intelligent-analytics-informed-generative-ai-framework-for-performance-optimization.md): 说明了实际痛点：profiler 只能暴露瓶颈，不能生成具体的代码修改。
