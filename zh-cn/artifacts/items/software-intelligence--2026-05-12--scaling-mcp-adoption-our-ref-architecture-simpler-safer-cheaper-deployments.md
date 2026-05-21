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
Cloudflare 描述了一种受治理的企业 MCP 部署方式：把 MCP 服务器从员工电脑迁移到共享访问、日志、DLP 和成本控制之后。文中声称最明显的收益来自 Code Mode：在一个内部门户配置中，工具定义上下文从约 9,400 个 token 降到 600 个 token。

## 问题
- 企业采用 MCP 会带来风险：授权扩散、提示注入、未经审查的本地服务器、工具注入、供应链暴露和数据泄露。
- 本地 MCP 服务器把版本选择、更新和来源信任交给单个员工处理，审计和策略执行会变得困难。
- 大规模 MCP 部署还会浪费上下文，因为客户端可能在知道需要哪些工具之前就收到所有工具 schema。

## 方法
- Cloudflare 在其开发者平台上把 MCP 服务器作为远程服务运行，由一个中心团队管理模板、CI/CD、密钥、审计日志和默认拒绝的写入控制。
- Cloudflare Access 提供基于 OAuth 的身份认证，并在私有 MCP 服务器可用之前检查 SSO、MFA、IP、位置和设备属性。
- MCP 服务器门户为每名员工提供一个客户端端点，只暴露已授权的内部和第三方 MCP 服务器，并配有日志、策略执行和 DLP 规则。
- Code Mode 把许多上游 MCP 工具收敛为两个门户工具：search 按需查找工具定义，execute 运行沙箱化 JavaScript 来调用选定工具。
- AI Gateway 位于 MCP 客户端和 LLM 提供商之间，用于提供商切换和 token 限制；Cloudflare Gateway 则使用 URL 和 JSON-RPC 正文模式扫描流量，以发现影子 MCP 服务器。

## 结果
- Cloudflare 的一个 MCP 服务器设计通过 2 个工具暴露数千个 Cloudflare API 端点，并声称与把所有端点作为独立工具暴露相比，token 使用量减少 99.9%。
- 在一个连接 4 台 MCP 服务器的内部门户中，52 个工具的定义使用了约 9,400 个上下文 token；Code Mode 把这一数字降到 2 个门户工具共约 600 个 token，减少 94%。
- Jira 加 Google Drive 的示例在 Code Mode 下需要 2 次工具调用：1 次 search 调用和 1 次 execute 调用。非 Code Mode 版本需要预先提供完整 schema，并进行 3 次独立工具调用。
- 文中提出的影子 MCP 检测使用 /mcp 和 /mcp/sse 等 URL 路径，并匹配 JSON-RPC 正文中的方法，包括 initialize、tools/call、tools/list、resources/read、resources/list、prompts/list 和 sampling/createMessage。
- 摘录提供了产品和部署层面的主张，没有包含外部基准测试，也没有包含与其他 MCP 安全产品的受控评估。

## Problem

## Approach

## Results

## Link
- [https://blog.cloudflare.com/enterprise-mcp/](https://blog.cloudflare.com/enterprise-mcp/)
