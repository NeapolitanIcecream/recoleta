---
kind: ideas
granularity: day
period_start: '2026-06-03T00:00:00'
period_end: '2026-06-04T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- LLM agents
- coding benchmarks
- software engineering
- MCP security
- LLM serving
- observability
- agent tooling
tags:
- recoleta/ideas
- topic/llm-agents
- topic/coding-benchmarks
- topic/software-engineering
- topic/mcp-security
- topic/llm-serving
- topic/observability
- topic/agent-tooling
language_code: zh-CN
---

# AI toolchain verification

## Summary
MCP 服务器团队可以在工具到达代理之前加入描述与代码一致性检查。SDK 文档团队可以给审查代理加一层检索，找到支持断言的跨文件证据。LLM 服务团队可以在输出质量下降但系统未崩溃时，加入比较中间模型状态的差分诊断流程。

## CI checks for MCP tool descriptions against implementation behavior
发布 MCP 服务器的团队应把工具描述当作可执行契约，并在工具变更时在 CI 中检查。检查可以抽取工具名称、schema、自然语言描述、入口函数、本地辅助调用和敏感 API 调用，然后把遗漏行为、夸大能力、状态变更、资源占用或数据泄露标出来，交给人工复核。

这个问题很具体，因为测得的失败率已经不是假设。DCIChecker 在 2,214 个真实 MCP 服务器上的 19,200 对工具中发现 9.93% 存在描述与代码不一致。这些不一致会误导工具选择，因为 LLM 依赖暴露出来的描述做规划，通常在调用时看不到实现代码。

一个可行的起点，是对变更过的 MCP 工具跑 CI 作业，并对文件系统、网络、认证、分析和状态变更类工具提高审查强度。输出应包含描述文本、触发标记的代码路径和不一致子类型，方便维护者在代理调用之前修正描述或实现。

### Evidence
- [Description-Code Inconsistency in Real-world MCP Servers: Measurement, Detection, and Security Implications](../Inbox/2026-06-03--description-code-inconsistency-in-real-world-mcp-servers-measurement-detection-and-security-implications.md): 定义了 MCP 工具的描述-代码不一致，介绍了 DCIChecker，并报告在来自 2,214 个服务器的 19,200 对工具中有 9.93% 不一致。
- [Description-Code Inconsistency in Real-world MCP Servers: Measurement, Detection, and Security Implications](../Inbox/2026-06-03--description-code-inconsistency-in-real-world-mcp-servers-measurement-detection-and-security-implications.md): 说明 LLM 通常根据工具描述进行规划而不会检查代码，并给出未披露状态和分析副作用的例子。

## Repository evidence retrieval for SDK documentation review agents
SDK 文档团队可以在每次 AI 辅助的 API 注释审查和教程验证流程里加入一个可被工具调用的检索步骤。这个检索层应索引源码文件、API 参考、测试、示例和上游文档，然后为代理想要验证的每个断言返回带文件元数据的排序片段。

Context-as-a-Service 提供了一个可用的模式。在两个生产 SDK 案例中，接入 CaaS 的代理找到了基线代理加常规仓库工具能找到的同样 5 个缺失公共成员文档，还多发现了 8 个问题，包括跨文件事实错误、API 注释过于笼统、可执行 URI 错误、API 使用改进和缺失前置条件。它也缩短了报告中的墙钟时间和输入 token 数，尽管调用 LLM 的次数更多。

最适合先落地的场景，是高风险的生成文档：公共方法的 API 参考、带可执行代码片段的教程，以及依赖生命周期行为或其他文件中创建对象的文档。审查时只保留能对应到具体证据片段和源路径的发现，这样文档负责人就可以在不重新跑代理搜索的情况下接受或拒绝修复。

### Evidence
- [Context-as-a-Service: Surfacing Cross-File Dependency Chains for LLM-Generated Developer Documentation](../Inbox/2026-06-03--context-as-a-service-surfacing-cross-file-dependency-chains-for-llm-generated-developer-documentation.md): 把 CaaS 描述为面向文档代理的检索层，并报告在两个生产 SDK 工作流中保留的发现从 5 个增至 13 个。
- [Context-as-a-Service: Surfacing Cross-File Dependency Chains for LLM-Generated Developer Documentation](../Inbox/2026-06-03--context-as-a-service-surfacing-cross-file-dependency-chains-for-llm-generated-developer-documentation.md): 列出了 CaaS 发现的额外问题，并报告两个任务的墙钟时间减少了 22% 到 34%。
- [Context-as-a-Service: Surfacing Cross-File Dependency Chains for LLM-Generated Developer Documentation](../Inbox/2026-06-03--context-as-a-service-surfacing-cross-file-dependency-chains-for-llm-generated-developer-documentation.md): 说明常规仓库工具为何会漏掉文档断言背后不明显的依赖链。

## Differential diagnosis runs for silent LLM serving errors
运行 vLLM、SGLang 或类似服务引擎的团队，应为不会崩溃的质量回退增加一条可复现的差分诊断路径。当已知的 prompt、模型和服务配置开始输出错误或更低准确率的结果时，系统应把目标引擎和 HuggingFace Transformers 之类的参考实现并排运行，收集中间激活值和调用序列，匹配对应组件，并标出输出开始明显分叉的第一个组件。

Ekka 说明，这个流程可以把静默错误排查推进到输出比较之外。它对真实 vLLM 和 SGLang 问题的研究报告了 80% 的 pass@1 和 88% 的 pass@5 诊断准确率。问题集也说明为什么需要组件级证据：根因分布在服务逻辑、模型实现、内核后端和数值精度上。

一个较小的运行版本可以从夜间哨兵 prompt 开始，针对启用自定义内核、量化、分页注意力或滑动窗口注意力的模型。准确率指标下降时，诊断产物应包含 prompt、模型版本、引擎版本、匹配后的组件路径、激活差异摘要，以及供服务工程师查看的候选故障层。

### Evidence
- [Ekka: Automated Diagnosis of Silent Errors in LLM Inference](../Inbox/2026-06-03--ekka-automated-diagnosis-of-silent-errors-in-llm-inference.md): 概述了 Ekka 的差分调试方法，并报告在真实静默服务错误上的 pass@1 为 80%、pass@5 为 88%。
- [Ekka: Automated Diagnosis of Silent Errors in LLM Inference](../Inbox/2026-06-03--ekka-automated-diagnosis-of-silent-errors-in-llm-inference.md): 解释了为什么优化过的 LLM 服务引擎可能在没有明确错误的情况下返回响应，而输出质量却下降。
