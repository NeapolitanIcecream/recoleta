---
source: hn
url: https://github.com/kvlar-io/kvlar
published_at: '2026-03-04T23:16:30'
authors:
- kvlar
topics:
- ai-agent-security
- tool-call-firewall
- policy-engine
- mcp
- runtime-guard
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Kvlar – Open-source firewall for AI agent tool calls

## Summary
Kvlar 是一个面向 AI 代理工具调用的开源安全层与策略引擎，在执行前对每次工具调用、数据访问和操作做基于策略的检查。它要解决的是代理可直接接触代码、数据库和生产系统时缺少统一安全防火墙的问题。

## Problem
- AI 代理正在获得执行代码、发邮件、访问数据库和操作生产系统的能力，但代理与工具之间**缺少标准化安全层**。
- 如果没有统一的策略检查，代理可能执行越权操作；这很重要，因为一旦接入真实系统，错误或恶意调用会直接带来安全与合规风险。
- 需要一种默认安全、可审计、可测试的机制，在每次工具调用前做确定性的允许/拒绝决策。

## Approach
- Kvlar 在代理与 MCP 工具服务器之间插入一个运行时代理层，拦截每个 tool call，并在执行前用策略引擎评估。
- 核心机制很简单：把安全规则写成**人类可读的 YAML 策略**；每个动作都拿去和策略匹配，命中允许规则就放行，否则默认拒绝（fail-closed）。
- 它是 **MCP 协议原生** 的，针对 Model Context Protocol（spec 2024-11-05）设计，支持 stdio 和 TCP，并通过 JSON-RPC 2.0 / newline-delimited JSON 通信。
- 系统由几个部分组成：`kvlar-proxy` 负责转发与拦截，`kvlar-core` 负责策略评估，`kvlar-audit` 负责结构化审计日志。
- 它还提供策略测试工具，可写 YAML 测试用例验证某个操作应被 allow 或 deny，并支持 CLI、verbose 和 JSON 输出用于 CI。

## Results
- 文本**没有提供学术基准或性能指标**，没有延迟、吞吐、误报率、拦截率等量化结果。
- 给出的最具体数字是工程验证信息：项目声明支持 **MCP spec 2024-11-05**、协议为 **JSON-RPC 2.0**，传输支持 **2 种**（stdio 为主、TCP）。
- 仓库层面的验证信息包括：工作区有 **80 tests**，并提供 `cargo test --workspace` 进行测试。
- 已明确测试兼容的环境包括 **Claude Desktop** 和 **@modelcontextprotocol/server-filesystem**。
- 主要声称的突破是工程与安全属性：**默认拒绝（fail-closed）**、**确定性决策**（相同动作+相同策略=相同结果）、**可审计**（每次决策带完整上下文日志）、以及**策略即代码**的可维护性。

## Link
- [https://github.com/kvlar-io/kvlar](https://github.com/kvlar-io/kvlar)
