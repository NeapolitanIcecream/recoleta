---
kind: trend
trend_doc_id: 665
granularity: day
period_start: '2026-04-26T00:00:00'
period_end: '2026-04-27T00:00:00'
topics:
- coding-agents
- agent-evaluation
- benchmarks
- software-testing
- gpu-optimization
run_id: materialize-outputs
aliases:
- recoleta-trend-665
tags:
- recoleta/trend
- topic/coding-agents
- topic/agent-evaluation
- topic/benchmarks
- topic/software-testing
- topic/gpu-optimization
language_code: zh-CN
---

# 可执行证据正在决定编码与代理研究的进展速度

## Overview
这一时期最强的工作都在收紧生成与可执行证据之间的联系。KISS Sorcar、AgentEval 和 ClawMark 都按系统在真实工作流中能完成什么、追踪什么、承受什么来评分。SeGa 和 Optimas 把同样的思路扩展到基于需求的测试和分析器引导的优化，并在真实缺陷和实测速率提升上给出了具体结果。

## Clusters

### 编码代理中的执行约束
编码代理论文持续在长任务上加入执行约束。KISS Sorcar 用强制续写摘要、工具访问和 git worktree 隔离，让仓库修改更易审查，也更容易恢复。它在 Terminal Bench 2.0 上配合 Claude Opus 4.6 的通过率为 62.2%，略高于 Claude Code 的 58% 和 Cursor Composer 2 的 61.7%。细节很关键：只有 43.8% 的任务在五次试验中全部通过，另有 19 个任务始终失败。这说明仓库处理更好了，但离稳定自主还远。

#### Evidence
- [KISS Sorcar: A Stupidly-Simple General-Purpose and Software Engineering AI Assistant](../Inbox/2026-04-26--kiss-sorcar-a-stupidly-simple-general-purpose-and-software-engineering-ai-assistant.md): KISS Sorcar 的摘要与基准结果

### 基准测试正在检验失败路径，而不只看最终答案
评估工作变得更细，也更贴近实际运行。AgentEval 把规划、工具、参数、执行和综合步骤按依赖图打分，再把后续失败追溯到可能的源头步骤。在 150 个人工标注案例上，它的失败检测召回率达到 0.89，高于端到端检查的 0.41 和平铺步骤打分的 0.67。在一项为期四个月的试点中，它发现了 23 个发布前回归问题，并把根因识别时间中位数从 4.2 小时降到 22 分钟。ClawMark 把同样的要求带进基准测试：100 个跨多天的办公室任务、5 个有状态服务、1,072 个原始多模态材料，以及基于规则的评分。最高加权得分是 75.8，但严格任务成功率最高只有 20.0%，因此这个基准仍然要求完整工作流完成，而不只看部分进展。

#### Evidence
- [AgentEval: DAG-Structured Step-Level Evaluation for Agentic Workflows with Error Propagation Tracking](../Inbox/2026-04-26--agenteval-dag-structured-step-level-evaluation-for-agentic-workflows-with-error-propagation-tracking.md): 步骤级 DAG 评估指标和试点结果
- [ClawMark: A Living-World Benchmark for Multi-Turn, Multi-Day, Multimodal Coworker Agents](../Inbox/2026-04-26--clawmark-a-living-world-benchmark-for-multi-turn-multi-day-multimodal-coworker-agents.md): 面向动态协作代理的基准设计和任务成功结果

### 外部证据正在引导代码生成
在测试和优化中，生成都越来越依赖外部证据。SeGa 根据产品需求生成测试，而不只依赖代码上下文。在 4 个工业级 Go 项目、共 60 个业务逻辑缺陷上，它检测出 29 个缺陷；对比基线只找到 4 到 7 个。在 6 个生产仓库中，开发者确认并修复了系统发现的 16 个此前未知缺陷。Optimas 在 GPU 调优上用了同类方法。它把分析器输出压缩成紧凑的诊断摘要，然后要求代码修改直接针对测得的瓶颈。论文报告了 3,410 次实验、超过 98.82% 的性能提升运行，以及 8.02% 到 79.09% 的平均加速。按作者的设置，只看代码的基线没有产生任何有效优化。

#### Evidence
- [Uncovering Business Logic Bugs via Semantics-Driven Unit Test Generation](../Inbox/2026-04-26--uncovering-business-logic-bugs-via-semantics-driven-unit-test-generation.md): 基于需求的测试生成和工业缺陷发现结果
- [Optimas: An Intelligent Analytics-Informed Generative AI Framework for Performance Optimization](../Inbox/2026-04-26--optimas-an-intelligent-analytics-informed-generative-ai-framework-for-performance-optimization.md): 分析器引导的 GPU 优化流程和大规模实验结果
