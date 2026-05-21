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
编码代理团队可以把终端输出、工具 schema 和仓库证据放到更小、可测试的接口之后，以获得具体收益。最明确的采用点是有边界的命令执行、面向长目录的已编译工具描述，以及在代理编辑代码前暴露定义-使用证据的仓库上下文工具。静态 API 检查和类型检查也应纳入生成式仓库工作流，因为许多失败在运行时测试之前就能被发现。

## 用于构建和测试运行的有边界终端执行子代理
当原始日志占用主代理上下文时，编码代理团队应把构建、测试、安装和诊断命令交给一个有边界的终端执行子代理。具体实现很小：主代理发送自然语言请求，子代理每轮运行一个带超时的同步终端命令，然后返回结构化摘要，其中包含命令状态、警告、失败测试和可能的下一步操作。

Terminus-4B 为这个接口提供了可直接参考的模板。在报告的 Serilog 示例中，主代理运行从 2.46M tokens 和 40 轮降到 740k tokens 和 32 轮，同时子代理在内部运行了 9 条命令。发回主代理的摘要约为 200 tokens，但仍包含 `dotnet build` 结果、769 个通过的单元测试，以及 1 个失败的 approval test 和可能的修复方式。团队可以在自己的 issue 队列上测试这一做法：重放近期代理运行，对比有无子代理时的主代理 token 数、直接终端调用次数和补丁成功率。

### Evidence
- [Terminus-4B: Can a Smaller Model Replace Frontier LLMs at Agentic Execution Tasks?](../Inbox/2026-05-04--terminus-4b-can-a-smaller-model-replace-frontier-llms-at-agentic-execution-tasks.md): 总结了 Terminus-4B 的执行子代理设计、token 减少主张，以及带有命令和测试细节的 Serilog 示例。
- [Terminus-4B: Can a Smaller Model Replace Frontier LLMs at Agentic Execution Tasks?](../Inbox/2026-05-04--terminus-4b-can-a-smaller-model-replace-frontier-llms-at-agentic-execution-tasks.md): 描述了终端输出造成的上下文窗口问题，以及相比原始 shell 日志更需要简明摘要。

## 面向长工具目录代理的工具 schema 编译
向编码代理暴露 20 个或更多工具的团队应在 API 边界测试工具 schema 编译器。实现方式是一个确定性的转换步骤：在模型看到工具定义之前，把现有 JSON 工具 schema 转成紧凑的结构化文本，同时保持下游工具执行器不变。第一次评估应使用团队当前的工具调用回归集，并按模型大小报告工具选择准确率、参数准确率、输入 token 数和失败情况。

TSCG 是具体参考案例。论文报告了覆盖 12 个模型的约 19,000 次调用，并声称当目录变长时收益很大。摘要中，保守版 TSCG 在 20 个工具时将 Mistral 7B 的准确率从 35.0% 提高到 80.0%，在 50 个工具时从 30.0% 提高到 75.3%；Gemma 3 4B 在 50 个工具时从 24.3% 提高到 87.5%。同一工作还报告，在重型 MCP schema 上节省 52–57% token。这对试图运行较小本地模型，或减少生产代理调用中重复 schema token 的团队最相关。

### Evidence
- [TSCG: Deterministic Tool-Schema Compilation for Agentic LLM Deployments](../Inbox/2026-05-04--tscg-deterministic-tool-schema-compilation-for-agentic-llm-deployments.md): 报告了 TSCG 的问题陈述、确定性 schema 编译方法、基准规模、模型结果和 token 节省。
- [TSCG: Deterministic Tool-Schema Compilation for Agentic LLM Deployments](../Inbox/2026-05-04--tscg-deterministic-tool-schema-compilation-for-agentic-llm-deployments.md): 说明 TSCG 以零依赖 TypeScript 包形式发布，并报告了生产风格 MCP schema 的节省情况。
- [TSCG: Deterministic Tool-Schema Compilation for Agentic LLM Deployments](../Inbox/2026-05-04--tscg-deterministic-tool-schema-compilation-for-agentic-llm-deployments.md): 解释了 API 边界问题：JSON schema 会消耗数千个重复 token，并损害小模型的工具使用能力。

## 仓库修复代理中的定义-使用切片
仓库修复代理在写补丁前，需要一个上下文工具来回答某个值在哪里被定义、使用和更改。具体流程是把 Python 仓库索引成带有语句节点和过程内定义-使用边的图，然后把后向、前向和双向切片作为工具调用暴露出来。代理可以请求某个变量和语句的切片，查看返回的代码上下文，再围绕相关函数或行减少猜测并写补丁。

ARISE 说明了为什么值得测试这一点。在 SWE-bench Lite 上，使用 SWE-agent 和 Qwen2.5-Coder-32B-Instruct 时，相比未修改的基线，它将 Function Recall@1 提高了 17.0 个点，将 Line Recall@1 提高了 15.0 个点。它达到 22.0% Pass@1，修复了 300 个 issue 中的 66 个，提升 4.7 个百分点。消融结果对实现有用：改进来自数据流图，模型可以直接消费结构化切片输出，不需要自然语言摘要层。

### Evidence
- [ARISE: A Repository-level Graph Representation and Toolset for Agentic Fault Localization and Program Repair](../Inbox/2026-05-04--arise-a-repository-level-graph-representation-and-toolset-for-agentic-fault-localization-and-program-repair.md): 总结了 ARISE 的图设计、切片 API、SWE-bench Lite 设置、定位收益和 Pass@1 结果。
- [ARISE: A Repository-level Graph Representation and Toolset for Agentic Fault Localization and Program Repair](../Inbox/2026-05-04--arise-a-repository-level-graph-representation-and-toolset-for-agentic-fault-localization-and-program-repair.md): 给出了论文文本中报告的 Function Recall@1、Line Recall@1、Pass@1、消融和结构化输出发现。
