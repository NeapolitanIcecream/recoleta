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

# Executable validation loops

## Summary
可执行证据正在进入日常工程流程。这里最清楚的切口是：agent CI 直接指向失败步骤、基于需求的业务逻辑测试生成，以及用执行结果验证每次修改的 profiler 引导 GPU 优化循环。

## Step-level regression tracing for agent CI
为 agent 的 CI 运行添加逐步失败图。最直接的用户是已经上线带工具调用的多步 agent 团队，这类团队即使端到端检查失败，工程师还是要手动翻 traces。AgentEval 给出一个具体做法：分别给 planning、tool selection、parameter generation、execution 和 synthesis 打分，再沿依赖关系追踪下游失败。在报告的试点中，这把根因定位中位时间从 4.2 小时降到 22 分钟，并在四个月内发现了 23 个发布前回归。第一版不需要完整分类体系。先从一个 workflow 开始，记录每一步和它的父步骤，为最常见的失败点加上类型化的通过/失败检查，在运行出错时显示得分最低的上游步骤。如果这种视图能缩短某一类反复出现故障的排查时间，就值得扩展到下一个 workflow。

### Evidence
- [AgentEval: DAG-Structured Step-Level Evaluation for Agentic Workflows with Error Propagation Tracking](../Inbox/2026-04-26--agenteval-dag-structured-step-level-evaluation-for-agentic-workflows-with-error-propagation-tracking.md): Provides the main results on failure-detection recall, root-cause accuracy, propagated errors, and the four-month CI/CD pilot with 23 regressions and faster debugging.
- [AgentEval: DAG-Structured Step-Level Evaluation for Agentic Workflows with Error Propagation Tracking](../Inbox/2026-04-26--agenteval-dag-structured-step-level-evaluation-for-agentic-workflows-with-error-propagation-tracking.md): Confirms the paper's framing of agent runs as evaluation DAGs with step-level metrics and automated root-cause attribution.

## Requirements-grounded unit test generation for business logic bugs
根据产品需求为带业务规则的代码生成测试。这适合维护企业服务的团队，因为正确性取决于审批规则、策略检查、定价条件或工作流约束，而这些内容更多写在 PRD 和内部文档里，而不是代码本身。SeGa 说明这件事现在可行：它把需求文档转成结构化的功能条目，检索目标方法相关的部分，再把这些部分转成明确的业务场景，用这些场景驱动单元测试生成。在 4 个工业 Go 项目、60 个业务逻辑 bug 上，它找到了 29 个，而对比基线只找到 4 到 7 个。在 6 个生产仓库中，开发者确认并修复了 16 个此前未知的 bug。一个合适的首个落地对象是某个需求文档稳定、且有一批漏出的逻辑 bug 的服务。衡量指标应是每批生成测试确认的 bug 数量，而不只是覆盖率或编译通过率。

### Evidence
- [Uncovering Business Logic Bugs via Semantics-Driven Unit Test Generation](../Inbox/2026-04-26--uncovering-business-logic-bugs-via-semantics-driven-unit-test-generation.md): Summarizes the requirements-driven test generation method and reports bug detection and production findings.
- [Uncovering Business Logic Bugs via Semantics-Driven Unit Test Generation](../Inbox/2026-04-26--uncovering-business-logic-bugs-via-semantics-driven-unit-test-generation.md): States the core problem of business logic bugs and the semantics-driven test generation approach from requirement documents.

## Profiler-guided GPU patch generation with execution checks
为 GPU kernel 建一个从 profiler 到 patch 的循环，只对测到的瓶颈提出修改，并通过执行验证。最先的用户是已经有 profiler 报告，但仍要把 counters 和 stall traces 手工翻成代码改动的性能工程师和 HPC 开发者。Optimas 给出了一个明确流程：把 profiler 输出压缩成小的诊断摘要，把修改限制在相关区域，要求每个修改都引用它对应的证据，然后编译、运行、检查正确性并记录加速比。论文报告了 3,410 次实验，其中性能提升运行占比超过 98.82%，平均加速比在 8.02% 到 79.09% 之间。它还报告，在作者的设置里，只用代码、不带诊断的基线没有产生有效优化。一个低成本试点是选一类可重复基准测试的 kernel，把最热的 kernel 和主要 stall 信号整理成紧凑 prompt，再把实测收益和当前的人工调优队列对比。

### Evidence
- [Optimas: An Intelligent Analytics-Informed Generative AI Framework for Performance Optimization](../Inbox/2026-04-26--optimas-an-intelligent-analytics-informed-generative-ai-framework-for-performance-optimization.md): Contains the main claims on diagnostic-guided optimization, execution-based validation, experiment count, success rate, and speedups.
- [Optimas: An Intelligent Analytics-Informed Generative AI Framework for Performance Optimization](../Inbox/2026-04-26--optimas-an-intelligent-analytics-informed-generative-ai-framework-for-performance-optimization.md): Establishes the operational pain that profilers expose bottlenecks but do not generate concrete code changes.
