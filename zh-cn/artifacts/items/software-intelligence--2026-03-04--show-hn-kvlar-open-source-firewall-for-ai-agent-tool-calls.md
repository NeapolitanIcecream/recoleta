---
source: hn
url: https://github.com/kvlar-io/kvlar
published_at: '2026-03-04T23:16:30'
authors:
- kvlar
topics:
- ai-agent-security
- mcp
- policy-engine
- runtime-guardrails
- tool-call-firewall
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Kvlar – Open-source firewall for AI agent tool calls

## Summary
Kvlar 是一个面向 AI 代理工具调用的开源安全层，在执行前用 YAML 策略检查每一次工具调用、数据访问和操作。它试图为 MCP 生态补上一个默认拒绝、可审计、可测试的运行时防火墙。

## Problem
- AI 代理已经能执行代码、发邮件、查数据库、操作生产系统，但代理与工具之间缺少统一的安全隔离层。
- 没有标准化的策略执行点，意味着越权调用、误操作和不可审计行为更容易发生，这对自动化软件生产和智能体系统很重要。
- 需要一种可预测、可验证的机制，在工具真正执行前决定“允许还是拒绝”。

## Approach
- Kvlar 在代理与 MCP 工具服务器之间插入一个代理层，对每个 tool call / data access / operation 先做策略评估，再决定是否放行。
- 核心机制很简单：把安全规则写成可读的 YAML；如果某个动作没有命中允许规则，就按 **fail-closed** 默认拒绝。
- 系统强调确定性：相同动作加相同策略，总是得到相同决策，便于测试、复现与审计。
- 它是 MCP 协议原生的，支持 stdio 和 TCP，采用 JSON-RPC 2.0 over newline-delimited JSON，并提供 `wrap`/`unwrap` 将客户端接入现有 MCP 配置。
- 除运行时拦截外，还提供策略测试与结构化审计日志，支持用 CLI 和 JSON 输出接入 CI。

## Results
- 文本没有提供基准数据、拦截率、性能开销或与其他方案的定量对比结果。
- 明确声称的能力包括：**默认拒绝**（无匹配规则即 deny）、**可审计**（每次决策记录完整上下文）、**确定性决策**（同动作+同策略=同结果）。
- 工程验证方面，项目给出了 **80 tests**（`cargo test --workspace`）作为当前实现的测试覆盖信号，但未报告通过率以外的进一步指标。
- 兼容性声明包括：基于 **MCP spec 2024-11-05**，支持 **stdio** 和 **TCP**，并已测试 **Claude Desktop** 与 `@modelcontextprotocol/server-filesystem`。
- 相比“无安全层直接调用工具”，其主要突破性主张不是更高任务性能，而是为 AI 代理增加一个开源、策略化、运行时强制执行的安全控制面。

## Link
- [https://github.com/kvlar-io/kvlar](https://github.com/kvlar-io/kvlar)
