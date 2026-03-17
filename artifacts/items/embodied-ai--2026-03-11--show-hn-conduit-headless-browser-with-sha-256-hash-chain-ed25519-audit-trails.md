---
source: hn
url: https://news.ycombinator.com/item?id=47343785
published_at: '2026-03-11T23:15:53'
authors:
- TaxFix
topics:
- ai-agent-auditing
- headless-browser
- cryptographic-provenance
- sha-256-hash-chain
- ed25519-signatures
- mcp-tools
relevance_score: 0.11
run_id: materialize-outputs
---

# Show HN:Conduit–Headless browser with SHA-256 hash chain - Ed25519 audit trails

## Summary
Conduit 是一个面向 AI 代理的无头浏览器审计工具，用密码学方式为网页操作生成可验证的证据链。它试图解决“代理到底做了什么无法证明”的可信审计问题，并通过 MCP 集成让 LLM 代理可直接调用。

## Problem
- AI 代理在网页中浏览、点击、填表、抓取数据时，传统截图和日志都可能被伪造或篡改，事后难以证明真实发生过什么。
- 在合规、数据来源追踪、诉讼取证等场景中，缺少可独立验证的操作证据会带来责任不清和信任问题。
- 这很重要，因为随着代理自动执行真实世界网页任务，审计性和可追责性会成为部署与合规落地的基础要求。

## Approach
- 核心机制很简单：把每一步浏览器动作与前一步的哈希连接起来，形成 SHA-256 哈希链；如果中间任何一步被改动，整条链就会失效。
- 会话结束后，再用 Ed25519 对结果签名，生成一个 proof bundle，里面包含完整操作日志、哈希链、签名和公钥。
- 任何人都可以拿这个 JSON 证据包独立验证，不需要信任生成证据的一方。
- 实现上基于 Playwright 的无头浏览器，并封装为纯 Python 工具。
- 同时提供 MCP 服务器接口，使 Claude、GPT 等 LLM 代理能通过工具调用直接使用 browse、click、fill、screenshot 等能力，并在后台自动构建证据包。

## Results
- 文本没有提供标准论文式定量实验结果，**没有**给出基准数据集、成功率、延迟、开销或与其他审计方案的数值比较。
- 最强的具体主张是：每个动作都进入 **SHA-256** 哈希链，并在会话结束时用 **Ed25519** 签名，从而得到“tamper-evident” 的可审计记录。
- 产出物是一个可独立验证的 **JSON proof bundle**，包含 **action log、hash chain、signature、public key** 四类核心内容。
- 支持的代理能力包括 **browse / click / fill / screenshot**，并宣称可用于 **AI agent auditing、compliance automation、web scraping provenance、litigation support**。
- 工程属性上的具体信息包括：**MIT 许可证**、**纯 Python**、**无账号 / 无 API key / 无遥测**，以及通过 `pip install conduit-browser` 安装。

## Link
- [https://news.ycombinator.com/item?id=47343785](https://news.ycombinator.com/item?id=47343785)
