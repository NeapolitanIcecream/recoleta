---
kind: ideas
granularity: day
period_start: '2026-07-04T00:00:00'
period_end: '2026-07-05T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- AI agents
- agent security
- LLM budgets
- browser testing
- local inference
- agentic desktops
tags:
- recoleta/ideas
- topic/ai-agents
- topic/agent-security
- topic/llm-budgets
- topic/browser-testing
- topic/local-inference
- topic/agentic-desktops
language_code: zh-CN
---

# 智能体执行边界

## Summary
智能体团队可以在故障会变贵的位置加入具体运行控制：为 LLM 请求做调用前成本预留，在 RAG chunk 或工具调用到达模型前做确定性授权，以及为消费级 GPU 硬件上的 out-of-core 本地推理设置一条范围明确的 Windows 基准测试。

## 自主智能体运行的调用前 LLM 支出预留
运行 LLM 网关的平台工程师，可以在一次智能体运行中的每个提供商请求之前加入预算决策。实际形态可以是网关钩子、sidecar 或 SDK 中间件：根据当前输入 token、有效输出上限和带版本的价格表估算最坏情况成本，然后在运行、用户、密钥等范围内原子性预留这笔金额。调用结束后，系统提交实际用量并释放未使用的预留金额。

这针对的是普通月度预算或按密钥预算容易漏掉的成本模式：智能体循环会反复发送累积上下文，到第 20 步时一次调用可能超过 50K 输入 token。智能体还需要机器可读的预算状态。Header 和 RFC 9457 problem-detail 错误可以告诉智能体何时选择更便宜的模型、裁剪上下文或干净停止。一个有用的初始测试，是用真实智能体 trace 回放并覆盖并行分支、缺失价格元数据和上下文增长，然后测量新增延迟、被阻止的调用，以及预留金额与实际花费金额。

### Evidence
- [RFC: Stopping runaway AI agent spend with atomic budget reservations](../Inbox/2026-07-04--rfc-stopping-runaway-ai-agent-spend-with-atomic-budget-reservations.md): 概述 RFC 设计：调用前估算支出、原子性预留、范围、预算状态 header，以及缺少评估结果。
- [RFC: Stopping runaway AI agent spend with atomic budget reservations](../Inbox/2026-07-04--rfc-stopping-runaway-ai-agent-spend-with-atomic-budget-reservations.md): 描述智能体循环的成本机制，包括累积上下文，以及第 20 步时一次调用达到 50K token。
- [RFC: Stopping runaway AI agent spend with atomic budget reservations](../Inbox/2026-07-04--rfc-stopping-runaway-ai-agent-spend-with-atomic-budget-reservations.md): 列出预算权限行为：在提供商调用前预留、遇到未知价格时关闭放行，并暴露预算状态供智能体调整。

## 面向 RAG 和工具工作流的人到智能体授权记录
在支持工作流中加入 RAG 和工具使用的团队，可以把身份路径做成每个请求的必需部分。检索器应给 chunk 附加访问元数据、认证用户、通过细粒度授权过滤检索到的 chunk，并只把已授权文本发送给模型。工具调用也需要同样处理：通过带 OAuth 2.1 的 MCP，或通过使用 token 和网关控制的普通 API。

智能体工作流需要分别记录人类用户、智能体参与者、委托范围和已执行动作。一个支持台流程可以把工作拆分给范围受限的子智能体，签发带委托声明的短期签名 JWT，并为每次操作记录参与者、委托者、人类用户、角色和范围。一个小型验证集应包含受限文档、过期凭证，以及试图调用范围外工具的委托智能体。

### Evidence
- [AI Authentication and Authorization](../Inbox/2026-07-04--ai-authentication-and-authorization.md): 概述文章中的模式：RAG 过滤、通过 MCP 或 API 访问工具、独立智能体身份、短期凭证和审计日志。
- [AI Authentication and Authorization](../Inbox/2026-07-04--ai-authentication-and-authorization.md): 解释为什么需要在授权人类与每个智能体动作之间维护身份链。
- [AI Authentication and Authorization](../Inbox/2026-07-04--ai-authentication-and-authorization.md): 说明 RAG 应在文档到达模型前进行过滤。
- [AI Authentication and Authorization](../Inbox/2026-07-04--ai-authentication-and-authorization.md): 给出具体的 RAG 实现模式：chunk 访问元数据、用户声明，以及通过细粒度授权过滤。

## 面向 out-of-core 70B 本地推理的 Windows 基准测试路径
在消费级 GPU 上评估本地推理的开发者，可以先为 Windows 11 上的 Kortex 增加一条专用基准测试路径，再为超大 GGUF 模型选择运行时。相关测试范围很窄：一台配有 20 GB GPU、足够 RAM、一块或两块 NVMe 硬盘的机器，以及一个超出 VRAM 的 70B 量化模型。在相同提示词、上下文大小和解码设置下，将 Kortex 与 llama.cpp 部分卸载进行比较，然后记录每秒 token 数、输出匹配情况、硬盘布局和 GPU 驻留计划。

Kortex 报告称，在 Radeon RX 7900 XT 20 GB 系统上，Llama-3.3-70B Q4_K_M 达到每秒 1.95 token；相比之下，同一硬件上使用 llama.cpp b9860 Vulkan 并卸载 80 层中的 30 层时，每秒为 0.21 token。当前采用边界很明确：流式路径仅支持 Windows，没有 HTTP 服务器或多轮 REPL，Linux 流式尚未测试。这意味着应先走评估和批量推理路径，服务集成留到后续构建。

### Evidence
- [Out-of-core LLM inference engine written from scratch in Rust](../Inbox/2026-07-04--out-of-core-llm-inference-engine-written-from-scratch-in-rust.md): 概述 Kortex 的 out-of-core 设计、报告的 70B 结果、与 llama.cpp 的比较、正确性检查和当前限制。
- [Out-of-core LLM inference engine written from scratch in Rust](../Inbox/2026-07-04--out-of-core-llm-inference-engine-written-from-scratch-in-rust.md): 说明仅 Windows 支持流式路径，以及在 20 GB 消费级 GPU 上报告的 70B 性能。
- [Out-of-core LLM inference engine written from scratch in Rust](../Inbox/2026-07-04--out-of-core-llm-inference-engine-written-from-scratch-in-rust.md): 解释测得的 1.95 tok/s 结果、llama.cpp 部分卸载瓶颈，以及 Kortex 使用流式权重进行仅 GPU 计算。
