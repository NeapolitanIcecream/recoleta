---
kind: ideas
granularity: day
period_start: '2026-05-04T00:00:00'
period_end: '2026-05-05T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- repository repair
- tool calling
- program generation
- software quality
tags:
- recoleta/ideas
- topic/coding-agents
- topic/repository-repair
- topic/tool-calling
- topic/program-generation
- topic/software-quality
language_code: zh-CN
---

# 受约束的编码代理接口

## Summary
编码代理团队可以通过把终端输出、工具 schema 和仓库证据放到更小、可测试的接口后面，拿到具体收益。最清楚的落地方向是有边界的命令执行、用于长工具目录的编译式工具描述，以及在代理改代码前暴露定义-使用证据的仓库上下文工具。生成式仓库工作流也应包含静态 API 和类型检查，因为很多失败在运行测试前就能被发现。

## 用于构建和测试运行的有边界终端执行子代理
编码代理团队应把构建、测试、安装和诊断命令交给一个有边界的终端执行子代理处理，前提是原始日志正在占用主代理的上下文。具体做法很简单：主代理发送自然语言请求，子代理每轮执行一个同步终端命令并设置超时，然后返回一份结构化摘要，包含命令状态、警告、失败测试和下一步可能动作。

Terminus-4B 给出了这个接口的可用模板。在报告的 Serilog 示例中，主代理的运行从 246 万 tokens 和 40 轮降到 74 万 tokens 和 32 轮，而子代理在内部运行了 9 个命令。返回给主代理的摘要大约有 200 个 token，仍然包含 `dotnet build` 的结果、769 个通过的单元测试，以及 1 个失败的审批测试和可能的修复办法。团队可以用自己的问题队列做测试，回放最近的代理运行，对比主代理 token 数、直接终端调用次数，以及在有无子代理时的修复成功率。

### Evidence
- [Terminus-4B: Can a Smaller Model Replace Frontier LLMs at Agentic Execution Tasks?](../Inbox/2026-05-04--terminus-4b-can-a-smaller-model-replace-frontier-llms-at-agentic-execution-tasks.md): 总结了 Terminus-4B 的执行子代理设计、token 降低主张，以及包含命令和测试细节的 Serilog 示例。
- [Terminus-4B: Can a Smaller Model Replace Frontier LLMs at Agentic Execution Tasks?](../Inbox/2026-05-04--terminus-4b-can-a-smaller-model-replace-frontier-llms-at-agentic-execution-tasks.md): 描述了终端输出带来的上下文窗口问题，以及需要简洁摘要而不是原始 shell 日志。

## 面向长工具目录的代理工具 schema 编译
面对编码代理暴露 20 个或更多工具的团队，应在 API 边界测试一个工具 schema 编译器。这个构建步骤会在模型看到工具之前，把现有的 JSON 工具 schema 确定性地转换成紧凑的结构化文本，然后保持下游工具执行器不变。第一次评估应使用团队现有的工具调用回归集，并按模型规模报告工具选择准确率、参数准确率、输入 token 和失败情况。

TSCG 是具体参考案例。论文报告了大约 19,000 次调用，覆盖 12 个模型，并声称当工具目录变长时收益很大。摘要里，保守版 TSCG 让 Mistral 7B 在 20 个工具时准确率从 35.0% 提升到 80.0%，在 50 个工具时从 30.0% 提升到 75.3%；Gemma 3 4B 在 50 个工具时从 24.3% 提升到 87.5%。同一工作还报告了在较重的 MCP schema 上节省 52–57% 的 token。对想运行更小本地模型，或减少生产代理调用里重复 schema token 的团队，这个方法更直接相关。

### Evidence
- [TSCG: Deterministic Tool-Schema Compilation for Agentic LLM Deployments](../Inbox/2026-05-04--tscg-deterministic-tool-schema-compilation-for-agentic-llm-deployments.md): 报告了 TSCG 的问题陈述、确定性 schema 编译方法、基准规模、模型结果和 token 节省。
- [TSCG: Deterministic Tool-Schema Compilation for Agentic LLM Deployments](../Inbox/2026-05-04--tscg-deterministic-tool-schema-compilation-for-agentic-llm-deployments.md): 说明 TSCG 以零依赖 TypeScript 包形式发布，并报告了生产风格的 MCP schema 节省。
- [TSCG: Deterministic Tool-Schema Compilation for Agentic LLM Deployments](../Inbox/2026-05-04--tscg-deterministic-tool-schema-compilation-for-agentic-llm-deployments.md): 解释了 API 边界问题：JSON schema 会消耗数千个重复 token，并削弱小模型的工具调用能力。

## 仓库修复代理中的定义-使用切片
仓库修复代理需要一个上下文工具，能在代理写补丁前回答一个值在哪里定义、在哪里使用、在哪里变更。具体做法是把 Python 仓库索引成带有语句节点和过程内定义-使用边的图，然后把后向、前向和双向切片作为一次工具调用暴露出来。代理可以对某个变量和语句请求切片，查看返回的代码上下文，并更少依赖对相关函数或行的猜测来打补丁。

ARISE 说明了这值得测试。在 SWE-bench Lite 上，配合 SWE-agent 和 Qwen2.5-Coder-32B-Instruct，它比未修改的基线在 Function Recall@1 上提高了 17.0 个点，在 Line Recall@1 上提高了 15.0 个点。它达到 22.0% 的 Pass@1，修复了 300 个问题中的 66 个，提升了 4.7 个百分点。消融结果对实现有直接意义：提升来自数据流图，而且模型可以直接消费结构化切片输出，不需要自然语言摘要层。

### Evidence
- [ARISE: A Repository-level Graph Representation and Toolset for Agentic Fault Localization and Program Repair](../Inbox/2026-05-04--arise-a-repository-level-graph-representation-and-toolset-for-agentic-fault-localization-and-program-repair.md): 总结了 ARISE 的图设计、切片 API、SWE-bench Lite 设置、定位提升和 Pass@1 结果。
- [ARISE: A Repository-level Graph Representation and Toolset for Agentic Fault Localization and Program Repair](../Inbox/2026-05-04--arise-a-repository-level-graph-representation-and-toolset-for-agentic-fault-localization-and-program-repair.md): 给出了论文文本中的 Function Recall@1、Line Recall@1、Pass@1、消融和结构化输出结果。
