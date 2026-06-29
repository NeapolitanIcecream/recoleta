---
source: hn
url: https://blog.cloudflare.com/enterprise-mcp/
published_at: '2026-05-12T23:46:13'
authors:
- Daviey
topics:
- mcp
- agentic-workflows
- enterprise-ai-security
- ai-governance
- tool-use
- token-efficiency
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Scaling MCP adoption: Our ref architecture – simpler,safer&cheaper deployments

## Summary
## 摘要
Cloudflare 描述了一种受治理的企业 MCP 部署方式：把 MCP 服务器从员工机器上移到共享的访问、日志、DLP 和成本控制之后。它声称最强的收益是 Code Mode，在一个内部门户场景里，把工具定义上下文从约 9,400 个 token 降到 600 个 token。

## 问题
- 企业采用 MCP 会带来风险，包括授权扩散、提示注入、未审核的本地服务器、工具注入、供应链暴露和数据泄露。
- 本地 MCP 服务器把版本选择、更新和源信任交给单个员工，这让审计和策略执行变得困难。
- 大规模 MCP 部署也会浪费上下文，因为客户端在知道自己需要哪些工具之前，可能先拿到所有工具的 schema。

## 方法
- Cloudflare 在其开发者平台上把 MCP 服务器作为远程服务运行，由中央团队管理模板、CI/CD、密钥、审计日志和默认拒绝写入控制。
- Cloudflare Access 在私有 MCP 服务器可用之前，提供基于 OAuth 的身份验证，并检查 SSO、MFA、IP、位置和设备属性。
- MCP 服务器门户给每位员工提供一个客户端端点，只暴露已授权的内部和第三方 MCP 服务器，并带有日志、策略执行和 DLP 规则。
- Code Mode 把许多上游 MCP 工具压缩成两个门户工具：search 按需查找工具定义，execute 运行受沙箱保护的 JavaScript 来调用选定工具。
- AI Gateway 位于 MCP 客户端和 LLM 提供商之间，用于切换提供商和限制 token；Cloudflare Gateway 则通过 URL 和 JSON-RPC 请求体模式扫描流量，寻找影子 MCP 服务器。

## 结果
- Cloudflare 的 MCP 服务器设计通过 2 个工具暴露了数千个 Cloudflare API 端点，并声称相比把所有端点都作为独立工具暴露，token 使用量减少了 99.9%。
- 在一个连接 4 个 MCP 服务器的内部门户中，52 个工具的定义大约占用 9,400 个上下文 token；Code Mode 把它降到大约 600 个 token，分布在 2 个门户工具上，减少了 94%。
- Jira 加 Google Drive 的示例在 Code Mode 下需要 2 次工具调用：1 次 search 调用和 1 次 execute 调用。非 Code Mode 版本则需要先提供完整 schema，再进行 3 次独立的工具调用。
- 提议的影子 MCP 检测使用 /mcp 和 /mcp/sse 之类的 URL 路径，以及对 initialize、tools/call、tools/list、resources/read、resources/list、prompts/list 和 sampling/createMessage 等方法的 JSON-RPC 请求体匹配。
- 这段内容给出的是产品和部署层面的主张，没有提供外部基准，也没有和其他 MCP 安全产品做受控评估。

## Problem

## Approach

## Results

## Link
- [https://blog.cloudflare.com/enterprise-mcp/](https://blog.cloudflare.com/enterprise-mcp/)
