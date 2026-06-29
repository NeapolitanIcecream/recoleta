---
kind: ideas
granularity: day
period_start: '2026-05-06T00:00:00'
period_end: '2026-05-07T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- software agents
- executable verification
- program synthesis
- agent security
- coding productivity
- repository mining
tags:
- recoleta/ideas
- topic/software-agents
- topic/executable-verification
- topic/program-synthesis
- topic/agent-security
- topic/coding-productivity
- topic/repository-mining
language_code: zh-CN
---

# 有边界的代理执行

## Summary
三个实用变化很突出：在共享企业代理的检索和工具循环里强制授权；把新服务创建导向已批准的 Backstage 模板；把重复的程序综合工作编译成可复用的符号求解器。每一种都给代理加了明确边界和可测检查。

## ABAC 门控检索与服务端工具执行，用于多租户代理
正在测试共享 RAG 代理的企业团队，应把授权放进检索和工具调用循环。具体做法是在摄取阶段为每个 chunk 标注租户和访问元数据，在检索阶段做资源级和 chunk 级检查，再把工具执行、会话状态、审计日志和策略检查放到服务端代理循环里。

实际问题很明确：语义搜索会返回其他租户的机密数据，因为相关性评分本身没有访问检查。在 OGX 的评估中，没有门控的检索在 98–100% 的跨租户探测中泄露了跨租户数据。ABAC 门控把报告中的跨租户泄露率和授权违规率都降到了 0%，而且客户端编排和服务端编排两种模式下都一样。

在大规模上线前，可以先做一个成本低的试验。用三个租户建立测试语料，运行授权查询、跨租户探测和提示注入探测，然后测泄露、授权违规和延迟。元数据缺失或含糊时，系统应该直接拒绝。

### Evidence
- [Securing the Agent: Vendor-Neutral, Multitenant Enterprise Retrieval and Tool Use](../Inbox/2026-05-06--securing-the-agent-vendor-neutral-multitenant-enterprise-retrieval-and-tool-use.md): 描述了 OGX、在摄取阶段添加租户和访问元数据、ABAC 检索门控、服务端工具执行，以及报告中的泄露下降。
- [Securing the Agent: Vendor-Neutral, Multitenant Enterprise Retrieval and Tool Use](../Inbox/2026-05-06--securing-the-agent-vendor-neutral-multitenant-enterprise-retrieval-and-tool-use.md): 说明了企业问题：检索按相关性排序，所以一个租户的查询可能暴露另一个租户的机密数据。
- [Securing the Agent: Vendor-Neutral, Multitenant Enterprise Retrieval and Tool Use](../Inbox/2026-05-06--securing-the-agent-vendor-neutral-multitenant-enterprise-retrieval-and-tool-use.md): 确认了服务端编排设计，以及 ABAC 门控在评估中消除了跨租户泄露的说法。

## 通过澄清式聊天为新服务脚手架选择 Backstage 模板
平台工程团队可以通过在已批准的 Backstage 模板上加一层检索来减少服务启动失败。流程很窄：先问几个关于服务用途、技术栈、数据库、API 风格、CI/CD 需求和安全要求的问题；把答案和模板目录匹配；再用选中的、已批准的脚手架生成服务起步代码。

价值在于部署适配。服务脚手架论文指出，开放式编码辅助经常漏掉公司特定的 CI/CD、Kubernetes、安全和平台规则。在它的小规模评估里，模板选择系统 10 次都选中了正确的真实模板。7 个 Copilot 用户里只有 2 个通过了所有部署质量门，而模板选择系统通过这些门的中位交互次数是 3 次，且用时不到 5 分钟。

第一次内部测试应该直接用现有的平台质量门，而不是只看开发者感受。在最近的服务需求上运行选择器，把选出的模板和平台团队预期的模板对比，再检查生成项目是否能通过 CI/CD、安全、部署和 pod 日志检查，而不用人工修复。

### Evidence
- [Architectural Constraints Alignment in AI-assisted, Platform-based Service Development](../Inbox/2026-05-06--architectural-constraints-alignment-in-ai-assisted-platform-based-service-development.md): 概述了在已批准 Backstage 模板上做 RAG、澄清式对话，以及报告中的模板选择和质量门结果。
- [Architectural Constraints Alignment in AI-assisted, Platform-based Service Development](../Inbox/2026-05-06--architectural-constraints-alignment-in-ai-assisted-platform-based-service-development.md): 说明评估绑定在一家大型德国软件公司的部署工作流上。
- [Architectural Constraints Alignment in AI-assisted, Platform-based Service Development](../Inbox/2026-05-06--architectural-constraints-alignment-in-ai-assisted-platform-based-service-development.md): 列出了生产约束：CI/CD、安全策略、基础设施服务和既有架构模式。
- [A meta-analysis of the effect of generative AI on productivity and learning in programming](../Inbox/2026-05-06--a-meta-analysis-of-the-effect-of-generative-ai-on-productivity-and-learning-in-programming.md): 提供了一个提醒：企业里 GenAI 编码助手的生产率影响在调节分析中很小，而且不显著。

## 基于 LLM 推理轨迹构建可复用符号求解器，用于重复程序综合任务
面对很多相似程序综合任务的团队，可以先做一个离线的求解器构建步骤。收集某类任务中成功和失败的 LLM 推理轨迹，让编码代理写一个独立的 Python 求解器，针对允许的 DSL 或转换语言实现规则，然后先运行求解器，只在求解器无法满足验证器时再调用 LLM。

ReaComp 就是具体案例。它根据每个基准大约 100 条推理轨迹构建符号程序综合器。在 PBEBench-Hard 上，符号集成在测试时不使用 LLM token 的情况下达到了 84.7% 的准确率，而 Best-of-K 是 68.4%。混合方案达到了 85.8% 的准确率，并把报告中的 token 用量从 332.1M 降到了 71.6M。

这种工作流适合能通过执行或验证器检查正确性的领域，比如基于示例的程序转换、数据整理规则和受约束的代码转换。一个实用试点可以先选一个重复任务族，只构建一次求解器，然后跟踪已解决案例、验证器失败、回退率和 token 开销，并与当前只用 LLM 的路径对比。

### Evidence
- [ReaComp: Compiling LLM Reasoning into Symbolic Solvers for Efficient Program Synthesis](../Inbox/2026-05-06--reacomp-compiling-llm-reasoning-into-symbolic-solvers-for-efficient-program-synthesis.md): 概述了 ReaComp 的轨迹到求解器方法，以及 PBEBench-Hard 的准确率和 token 降低结果。
- [ReaComp: Compiling LLM Reasoning into Symbolic Solvers for Efficient Program Synthesis](../Inbox/2026-05-06--reacomp-compiling-llm-reasoning-into-symbolic-solvers-for-efficient-program-synthesis.md): 说明 ReaComp 把推理轨迹编译成可复用的、基于受限 DSL 的符号程序综合器。
- [ReaComp: Compiling LLM Reasoning into Symbolic Solvers for Efficient Program Synthesis](../Inbox/2026-05-06--reacomp-compiling-llm-reasoning-into-symbolic-solvers-for-efficient-program-synthesis.md): 解释了更难的组合综合任务中，基于 LLM 搜索的成本和可靠性问题。
