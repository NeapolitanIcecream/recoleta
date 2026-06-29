---
source: hn
url: https://capframe.ai
published_at: '2026-05-19T23:46:47'
authors:
- euan21
topics:
- ai-agent-security
- mcp
- capability-tokens
- tool-use
- policy-enforcement
- prompt-injection
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Capframe – capability tokens for AI agent tool calls

## Summary
## 摘要
Capframe 是一个本地 Rust 工具包，用于映射 MCP 工具访问、发放范围受限的能力令牌，并对 AI 代理的工具调用执行确定性策略。它面向代理连接外部工具时的间接提示注入和过高权限风险。

## 问题
- 通过 MCP 连接的 AI 代理可以访问很多工具、端点和参数，因此它们的真实权限很难检查。
- 未受约束的工具输入和间接注入面会让恶意内容影响工具调用，或者推动代理越过预期权限。
- 安全团队需要能映射到 OWASP LLM Top 10、NIST AI RMF 和 MITRE ATLAS 的审计证据。

## 方法
- `find` 会遍历 MCP 服务器和工具端点，记录参数，标记未受约束的输入和间接注入面，并写出 `capframe.findings.json`。
- `bind` 发放范围受限、可撤销的能力令牌，带有类似 macaroon 的权限收缩、ed25519 持有者密钥绑定、`max_refund=50` 这样的限制，以及使用 HMAC-SHA256 的签名拒绝回执。
- `guard` 在运行时用确定性的 Rust 代码评估每次工具调用对应的 YAML 策略，因此允许和拒绝判断不依赖 LLM。
- `report` 导出 HTML 或 PDF 证据，并映射到 OWASP LLM、NIST AI RMF 和 MITRE ATLAS 控制项。

## 结果
- 示例扫描映射了 2 个 MCP 服务器上的 14 个工具，并发现 3 个工具存在与 OWASP LLM01 相关的未受约束输入。
- 另一个示例还发现了 1 个与 OWASP LLM01 和 MITRE ATLAS T0051 相关的间接注入面。
- 示例令牌将 `shopify-bot` 限定为 2 个工具、2 个限制项和 24 小时 TTL；具体限制包括 `max_refund≤50` 和 `region=eu`。
- Guard 回测报告显示，默认语料库的 247/247 个案例通过了 14 条规则和 3 个类别，假阳性率为 0.0%。
- 报告示例显示 OWASP LLM Top 10 覆盖了 10 项中的 4 项，存在 2 个未解决发现，标记了 2 个 MITRE 技术项，没有活跃利用。
- 运行时策略评估据称可在个位数微秒内完成。

## Problem

## Approach

## Results

## Link
- [https://capframe.ai](https://capframe.ai)
