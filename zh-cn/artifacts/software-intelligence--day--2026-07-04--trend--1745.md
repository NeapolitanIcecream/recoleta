---
kind: trend
trend_doc_id: 1745
granularity: day
period_start: '2026-07-04T00:00:00'
period_end: '2026-07-05T00:00:00'
topics:
- AI agents
- agent security
- LLM budgets
- browser testing
- local inference
- agentic desktops
run_id: materialize-outputs
aliases:
- recoleta-trend-1745
tags:
- recoleta/trend
- topic/ai-agents
- topic/agent-security
- topic/llm-budgets
- topic/browser-testing
- topic/local-inference
- topic/agentic-desktops
language_code: zh-CN
---

# 代理部署需要支出门禁、身份链和经过测量的本地运行路径

## Overview
今天最强的信号在运行层面：大型语言模型（LLM）代理需要针对资金、身份和执行的硬门禁。Donobu、Kortex 和 Aion 显示了测试、本地推理和桌面领域的分布。证据主要来自 RFC、软件包和产品报告；Kortex 给出了最清楚的数字。

## Clusters

### 用于代理调用的运行级预算
这份代理预算 RFC 把成本当作调用前的授权决定。它建议在每次请求提供商之前估算最坏情况支出，在运行、用户、密钥和其他作用域中以原子方式预留该金额，然后在调用后提交实际用量。该设计针对会反复发送不断增长上下文的循环；RFC 称，一个运行到第 20 步时输入 token 可能超过 50K。

有用的细节在失败路径上。代理通过标头和 RFC 9457 problem-detail 错误接收预算状态，因此可以选择更便宜的模型、缩短上下文，或干净地停止。RFC 引用了已报告的成本事件，包括一笔 $4,200 的周末账单和一笔 $87K 的团队月账单，但没有报告延迟、节省金额、误拦截或采用结果。

#### Evidence
- [RFC: Stopping runaway AI agent spend with atomic budget reservations](../Inbox/2026-07-04--rfc-stopping-runaway-ai-agent-spend-with-atomic-budget-reservations.md): 运行级预算预留设计及其已报告证据限制的摘要。

### 用于 RAG、工具和代理的确定性身份
这篇认证文章给出了一条实用的 AI 访问规则：每个动作都应继承自人类用户的权限，并经过确定性授权。对于检索增强生成（RAG），chunk 携带访问元数据，检索结果在模型看到之前先被过滤。对于工具，文章指向使用 OAuth 2.1 的 Model Context Protocol（MCP），或使用令牌和网关控制的普通 API。

代理部分增加了子代理的独立身份、短期凭据、签名 JSON Web Tokens（JWTs）、委托声明和审计日志。银行示例把工作拆分给四个代理，并使用 300 秒的 JWT 生命周期。这篇文章是指导，不是经过评估的安全研究，因此它的价值在于具体的访问模式。

#### Evidence
- [AI Authentication and Authorization](../Inbox/2026-07-04--ai-authentication-and-authorization.md): 身份继承、RAG 过滤、工具访问、代理身份和证据限制的摘要。

### 带修复轨迹的 AI 辅助浏览器测试
Donobu 把 AI 浏览器动作打包进 Playwright 测试。测试可以用自然语言指令调用 `page.ai()`，用 schema 和工具允许列表约束它，并把生成的工具调用缓存到 spec 旁边。该包还记录失败产物，包括截图、DOM dump、GPT 摘要和处理计划。

自动修复路径是主要的运行主张。使用 `--auto-heal` 时，Donobu 可以重新运行一个自主修复流程，并附加重新生成的 `fixed-test.ts`。语料没有给出通过率、成本、延迟或基线比较，因此稳妥的解读更窄：该工具把 AI 测试变成带有缓存动作和失败证据的可追踪工作流。

#### Evidence
- [Freedom from NPM. Happy 4th](../Inbox/2026-07-04--freedom-from-npm-happy-4th.md): Donobu 的 Playwright fixture、Page.AI 调用、缓存、分诊和缺少基准的摘要。

### 通过权重流式传输在消费级 GPU 上推理
Kortex 是这一时期测量最充分的项目。它通过在 NVMe、RAM、VRAM 和 GPU 计算之间流式传输权重，运行大于 GPU 内存的模型。在一台配备 Radeon RX 7900 XT 20 GB、32 GB RAM 和两块 NVMe 驱动器的 Windows 11 机器上，它报告 Llama-3.3-70B Q4_K_M 的速度为每秒 1.95 tokens。

比较对象是在同一硬件上的 llama.cpp b9860 Vulkan，其中 80 层有 30 层被卸载，报告速度为每秒 0.21 tokens。Kortex 将差距归因于在通过 PCIe 流式传输权重的同时，让所有计算都留在 GPU 上。它的限制也很明确：目前流式传输仅支持 Windows，没有 HTTP 服务器或多轮 REPL，也还没有经过测试的 Linux 路径。

#### Evidence
- [Out-of-core LLM inference engine written from scratch in Rust](../Inbox/2026-07-04--out-of-core-llm-inference-engine-written-from-scratch-in-rust.md): 流式传输方法、硬件配置、基准数字和当前限制的摘要。
