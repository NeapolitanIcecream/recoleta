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

# 可执行证据正在为编码和代理研究定节奏

## Overview
这一时期最强的工作收紧了生成与可执行证据之间的联系。KISS Sorcar、AgentEval 和 ClawMark 都按系统能完成什么、能追踪什么、能在真实工作流中承受什么来评分。SeGa 和 Optimas 把同样的思路扩展到基于需求的测试和基于性能分析器的优化，并在真实漏洞和测得的加速上取得了具体收益。

## Clusters

### 编码代理中的执行约束
面向编码代理的论文正在为长任务增加执行约束。KISS Sorcar 使用强制续接摘要、工具访问和 git worktree 隔离，让仓库修改便于审查和恢复。它在 Terminal Bench 2.0 上用 Claude Opus 4.6 报告了 62.2% 的通过率，略高于 Claude Code 的 58% 和 Cursor Composer 2 的 61.7%。细节很重要：只有 43.8% 的任务在全部五次试验中都通过，19 个任务始终失败。结果是更好的仓库处理能力，而不是稳定的自主性。

#### Evidence
- [KISS Sorcar: A Stupidly-Simple General-Purpose and Software Engineering AI Assistant](../Inbox/2026-04-26--kiss-sorcar-a-stupidly-simple-general-purpose-and-software-engineering-ai-assistant.md): Summary and benchmark results for KISS Sorcar

### 基准测试在考失败路径，不只是最终答案
评估工作正在变得更细，也更贴近实际流程。AgentEval 把计划、工具、参数、执行和综合步骤按依赖图打分，再把后续失败追溯到可能的源头步骤。在 150 个人工标注案例上，它的失败检测召回率达到 0.89，高于端到端检查的 0.41 和平面步骤评分的 0.67。在为期四个月的试点中，它发现了 23 个发布前回归，并把根因识别的中位时间从 4.2 小时降到 22 分钟。ClawMark 把同样的压力带到基准测试里：100 个跨多天的办公任务、5 个有状态服务、1,072 个原始多模态工件，以及基于规则的评分。最高加权分是 75.8，但严格的任务成功率最高只有 20.0%，这让基准测试仍然绑定在完整工作流完成上，而不只是部分进展。

#### Evidence
- [AgentEval: DAG-Structured Step-Level Evaluation for Agentic Workflows with Error Propagation Tracking](../Inbox/2026-04-26--agenteval-dag-structured-step-level-evaluation-for-agentic-workflows-with-error-propagation-tracking.md): Step-level DAG evaluation metrics and pilot results
- [ClawMark: A Living-World Benchmark for Multi-Turn, Multi-Day, Multimodal Coworker Agents](../Inbox/2026-04-26--clawmark-a-living-world-benchmark-for-multi-turn-multi-day-multimodal-coworker-agents.md): Benchmark design and task-success results for dynamic coworker agents

### 外部证据正在引导代码生成
把生成过程建立在外部证据上，既出现在测试里，也出现在优化里。SeGa 根据产品需求生成测试，而不只看代码上下文。在 4 个工业 Go 项目、60 个业务逻辑漏洞上，它检测到 29 个漏洞；对比基线只找到 4 到 7 个。在 6 个生产仓库里，开发者确认并修复了系统发现的 16 个此前未知漏洞。Optimas 把同样的思路用于 GPU 调优。它把性能分析器输出压缩成紧凑的诊断摘要，然后要求修改直接指向测得的瓶颈。论文报告了 3,410 次实验、超过 98.82% 的性能提升运行，以及 8.02% 到 79.09% 的平均加速。只看代码的基线在作者的设置中没有产生有效优化。

#### Evidence
- [Uncovering Business Logic Bugs via Semantics-Driven Unit Test Generation](../Inbox/2026-04-26--uncovering-business-logic-bugs-via-semantics-driven-unit-test-generation.md): Requirement-grounded test generation and industrial bug-finding results
- [Optimas: An Intelligent Analytics-Informed Generative AI Framework for Performance Optimization](../Inbox/2026-04-26--optimas-an-intelligent-analytics-informed-generative-ai-framework-for-performance-optimization.md): Profiler-guided GPU optimization pipeline and large-scale experiment results
