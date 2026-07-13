---
source: hn
url: https://github.com/shehryarsaroya/agenttransfer
published_at: '2026-07-11T22:52:52'
authors:
- tomatoes2026
topics:
- agent-infrastructure
- file-transfer
- multi-agent-coordination
- mcp
- agent-identity
- self-hosting
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: AgentTransfer – open-source file transfer for AI agents (one Go binary)

## Summary
## 摘要
AgentTransfer 让 AI 代理在一个可自行托管的 Go 静态二进制中拥有自己的身份、收件箱、存储空间和经过验证的文件传输流程。它把文件交付、完整性检查、代理发现、协作、MCP、电子邮件和可选的应用托管整合起来，每次交接都无需人工参与。

## 问题
- 现有文件工具通常要求人工创建账户、管理凭据、分享链接并确认交付。
- 大文件通过电子邮件或 AI 模型的上下文窗口传输时，操作不便，也可能带来安全风险。
- 代理需要收件人身份、交付状态、完整性元数据、访问控制和审计证据，单纯的存储空间无法满足这些要求。

## 方案
- 代理通过一次 `POST /v1/agents` 请求注册，并获得电子邮件地址、API 密钥、收件箱、文件夹和 400 MB 临时存储配额。在所有者验证邮箱之前，文件默认 24 小时后过期。
- 代理向指定姓名的收件人发送结构化文件交接信息，其中包含下载链接、文件大小、SHA-256 哈希、过期时间和消息元数据。HTTPS 在客户端与服务器之间直接传输文件字节，CLI 和 MCP 桥接程序会验证下载内容。
- 经过 Ed25519 签名并通过哈希串联的收据记录文件传输和应用生命周期事件。运营者和客户端可以离线验证单个代理的记录，或验证整个实例的链。
- 同一个 Go 静态二进制提供服务器、CLI、本地 MCP 桥接程序、REST API、可选的电子邮件和 webhook 交付、发现卡片、共享空间、客户端加密，以及独立的面向 Docker 的应用运行器。
- 人工完成邮箱验证后，代理可以使用外发电子邮件，获得一个永久 20 GB 文件夹，单文件上限为 5 GB，并可选择托管静态应用或容器应用。配额、收件人数量限制、隔离区、速率限制和 SSRF 检查用于限制滥用。

## 结果
- 离线演示无需账户或网络，即可完成 `alice` 到 `bob` 的 1 MiB 文件交接，流程包括上传、发送、长轮询、下载、SHA-256 验证和签名收据链验证。
- 新代理可以立即使用 400 MB 临时存储，文件有效期为 24 小时；完成验证的代理可获得 20 GB 永久存储，并能上传单个不超过 5 GB 的文件。
- 项目声称本地 MCP 桥接程序支持传输 5 GB 文件，文件内容不会进入模型上下文窗口。摘录没有提供吞吐量、延迟、可靠性数据，也没有与现有工具进行基准比较。
- AgentTransfer v0.6.0 包含开放注册、收件箱交付、发现、共享空间、本地和托管 MCP、客户端对称加密与封装加密、签名收据、webhook、已验证代理的静态站点、容器应用，以及基于隧道的 Connect 托管。
- 自行托管需要 Linux VPS、域名、外发中继密钥，以及 Go 1.25+ 或 Docker；核心部署无需单独的数据库、对象存储或反向代理。

## Problem

## Approach

## Results

## Link
- [https://github.com/shehryarsaroya/agenttransfer](https://github.com/shehryarsaroya/agenttransfer)
