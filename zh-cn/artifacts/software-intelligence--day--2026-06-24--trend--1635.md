---
kind: trend
trend_doc_id: 1635
granularity: day
period_start: '2026-06-24T00:00:00'
period_end: '2026-06-25T00:00:00'
topics:
- coding agents
- software engineering
- agent harnesses
- tool reliability
- code benchmarks
- test migration
- agent governance
run_id: materialize-outputs
aliases:
- recoleta-trend-1635
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-engineering
- topic/agent-harnesses
- topic/tool-reliability
- topic/code-benchmarks
- topic/test-migration
- topic/agent-governance
language_code: zh-CN
---

# 编码 agent 正在按状态、恢复和回归控制来衡量

## Overview
这一时期把编码 agent 视为带有状态、测试、故障恢复和可追踪控制的软件系统。i cat-agent 提供了最强的正向结果；ToolBench-X 和 CodeChat-Eval 暴露了 agent 在工具故障和后续编辑下的脆弱行为。

## Clusters

### Agent harness 与分离的编码角色
最强的工程结果来自 i cat-agent。它把 GitHub issue 解决流程拆给 Explorer、Patch Editor 和 Validator 三个角色。各 agent 交换结构化事件，Validator 对 Patch Editor 隐藏测试和断言，以减少补丁过拟合。在 SWE-bench Pro 上，使用 GPT-5.4-xhigh 的 i cat-agent 解决了 67.4% 的任务，比使用同一骨干模型的 mini-SWE-agent 高 8.3 个百分点。同一篇论文报告称，在 SWE-bench Pro 上，它的平均成本低于 Claude Code。

更大的设计主题出现在 Code as Agent Harness 这篇综述中。该综述把代码视为 agent 保存状态、调用工具、规划和验证工作的地方。MCPlexer 给出了这个思路在 Model Context Protocol (MCP) 上的具体产品版本：一个小型共享工具面，配有路由、审批、审计日志、记忆、浏览器控制和工作区策略。MCPlexer 这一项没有基准证据，因此它的价值在于运营设计，而不是已测得的性能。

#### Evidence
- [Unlocking Model Potentials Through Adaptive Multi-Agent Scaffolding for Efficient Issue Resolution](../Inbox/2026-06-24--unlocking-model-potentials-through-adaptive-multi-agent-scaffolding-for-efficient-issue-resolution.md): i cat-agent 架构、SWE-bench 结果和成本主张的摘要。
- [Code as Agent Harness](../Inbox/2026-06-24--code-as-agent-harness.md): 关于代码作为 agent harness，用于状态、工具、规划和验证的综述摘要。
- [Show HN: Mcplexer.com](../Inbox/2026-06-24--show-hn-mcplexer-com.md): MCPlexer 摘要，涵盖跨 harness 路由、审批、审计、记忆和工作区控制。

### 基准更强调恢复和保持正确性，而不是干净环境下的调用
ToolBench-X 用 1,106 个可执行多步骤任务、4,956 个 Python 工具和五类可恢复故障类型测试 agent。没有被评测的模型达到 0.60 的总体准确率。报告中的最高分是 Doubao-Seed-2.0-Lite 的 0.513。论文的诊断子集显示，定向恢复提示可挽回 25.5 到 35.5 个准确率点，而增加交互轮次的帮助较小。薄弱点在于故障诊断和恢复选择。

CodeChat-Eval 为编码模型增加了另一项压力测试：它们能否在 10 轮细化对话中保持代码正确？在 542 个编程任务中，所有被评测模型的功能正确性都下降。经过多轮细化后，GPT-5 Nano 下降 19.2%，Llama 3.1 8B 下降 69.2%。SWE-Pro 对性能优化提出了同样的问责要求。专家补丁带来较大的运行时间和内存收益，而当前大语言模型经常能应用补丁，却很少交付可测得的速度或内存改进。

#### Evidence
- [Beyond Function Calling: Benchmarking Tool-Using Agents under Tool-Environment Unreliability](../Inbox/2026-06-24--beyond-function-calling-benchmarking-tool-using-agents-under-tool-environment-unreliability.md): ToolBench-X 的任务数量、故障设计、模型分数和诊断恢复结果。
- [CodeChat-Eval: Evaluating Large Language Models in Multi-Turn Code Refinement Dialogues](../Inbox/2026-06-24--codechat-eval-evaluating-large-language-models-in-multi-turn-code-refinement-dialogues.md): CodeChat-Eval 设置，以及多轮代码细化中的正确性下降。
- [Evaluating LLMs on Real-World Software Performance Optimization](../Inbox/2026-06-24--evaluating-llms-on-real-world-software-performance-optimization.md): SWE-Pro 基准设计，以及专家优化补丁与 LLM 补丁之间的实测差距。

### 测试迁移使用意图和仓库上下文
IntentTester 展示了多 agent 编码在生成补丁之外的实际用途。它把源测试转换为与语言无关的 Test Description Language，将这些意图映射到目标仓库图上，然后通过验证反馈生成可执行测试。这可以处理 API 签名和直接代码模式不对应的情况，包括 Java-Python 迁移。

评测覆盖 JSON、HTML 和 Time 库中的九个开源项目。流水线从 2,058 个源测试创建 5,536 个子测试，并在过滤后保留 3,257 个。IntentTester 生成 2,776 个语法正确的测试，正确率为 85%，相比之下 MUT 为 51%，METALLICUS 为 43%。生成的测试暴露了 25 个真实缺陷，包括栈溢出和空指针解引用 bug。

#### Evidence
- [IntentTester: Intent-Driven Multi-agent Framework for Cross-Library Test Migration](../Inbox/2026-06-24--intenttester-intent-driven-multi-agent-framework-for-cross-library-test-migration.md): IntentTester 的方法、评测规模、正确性提升、可执行测试和真实缺陷。

### Agent 指令正在成为带版本的工程工件
语料还包括关于团队如何维护编码 agent 指令的早期工作。Agent Context File 研究把 CLAUDE.md、AGENTS.md 和 copilot-instructions.md 等文件作为带有提交历史的仓库工件来检查。该研究计划对变更分类，将它们与之后 agent 生成代码的质量关联起来，并测量不同开发窗口中的时间关系。

这篇论文报告的是研究设计和可行性，而不是已完成结果。规模仍有助于界定问题：作者引用 AIDev，其中包含 116,211 个仓库和 932,791 个涉及 agent 生成代码的 pull request，另有来自 1,925 个仓库的 2,303 个上下文文件。一个初步流水线生成了 10,763 个上下文文件快照，以及 8,600 个同时包含指令文件和 agent 代码信息的提交。

#### Evidence
- [How Do Developers Maintain and Evolve Their Agents' Instructions? An Empirical Study](../Inbox/2026-06-24--how-do-developers-maintain-and-evolve-their-agents-instructions-an-empirical-study.md): Agent Context Files 的研究设计、数据集、计划指标和可行性数量。
