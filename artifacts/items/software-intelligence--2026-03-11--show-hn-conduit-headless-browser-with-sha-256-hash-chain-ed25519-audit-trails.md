---
source: hn
url: https://news.ycombinator.com/item?id=47343785
published_at: '2026-03-11T23:15:53'
authors:
- TaxFix
topics:
- agent-auditing
- headless-browser
- cryptographic-provenance
- mcp-tools
- ai-agents
relevance_score: 0.92
run_id: materialize-outputs
---

# Show HN:Conduit–Headless browser with SHA-256 hash chain - Ed25519 audit trails

## Summary
Conduit 是一个面向 AI 代理的无头浏览器审计工具，把网页操作记录成可验证的加密证据链。它试图解决代理执行浏览、点击、填表和抓取时“事后无法证明发生了什么”的可信性问题。

## Problem
- AI 代理在网页上的操作通常只有截图或普通日志，**容易伪造、篡改或事后编辑**，出问题时难以追责。
- 在合规、数据采集、诉讼取证等场景中，**需要可独立验证的执行证据**，而不是仅依赖工具提供方的口头或平台信任。
- 对软件代理/LLM 工具调用来说，缺少**原生可审计性**会限制其在高风险自动化流程中的落地。

## Approach
- 基于 **Playwright** 构建无头浏览器，记录每一步操作，如 browse、click、fill、screenshot。
- 将每个动作与前一条记录一起做 **SHA-256 哈希**，形成串联的防篡改哈希链；若中间任一步被改动，后续链条都会失效。
- 在会话结束时，用 **Ed25519** 对整个结果签名，生成 proof bundle，其中包含动作日志、哈希链、签名和公钥。
- 任意第三方都可以在**不信任生成方**的情况下独立验证该 bundle 的完整性与来源。
- 工具还作为 **MCP server** 暴露，使 Claude、GPT 等 LLM 代理能直接通过工具调用使用浏览器，并自动生成审计证据。

## Results
- 文本**没有提供标准基准、公开数据集或定量实验结果**，因此无法报告准确的性能提升或对比数字。
- 论文式主张的核心结果是：每次浏览会话结束后可产出 **1 个 proof bundle（JSON）**，其中至少包含 **4 类内容**：action log、hash chain、signature、public key。
- 声称任何人都能对 bundle 做**独立验证**，无需信任日志生成者；这相对普通截图/日志提供了更强的防篡改保证。
- 支持的目标场景包括 **4 类**：AI agent auditing、compliance automation、web scraping provenance、litigation support。
- 工程落地层面给出了较强可用性信号：**MIT 许可、纯 Python、无需账号/API key/遥测**，并提供 `pip install conduit-browser` 和 MCP 集成。

## Link
- [https://news.ycombinator.com/item?id=47343785](https://news.ycombinator.com/item?id=47343785)
