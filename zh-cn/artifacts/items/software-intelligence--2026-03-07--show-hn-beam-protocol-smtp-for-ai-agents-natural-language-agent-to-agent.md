---
source: hn
url: https://github.com/Beam-directory/beam-protocol
published_at: '2026-03-07T23:16:30'
authors:
- alfridus
topics:
- agent-communication
- multi-agent-systems
- decentralized-identity
- protocol-design
- ai-infrastructure
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Beam Protocol – SMTP for AI Agents (natural language agent-to-agent)

## Summary
Beam Protocol提出了一个面向AI代理的开放通信层，试图像SMTP之于电子邮件一样，让不同公司、不同框架、不同机器上的代理能够相互发现、验证身份并安全通信。其核心价值是把代理间协作从定制API集成转为基于身份、意图和信任分数的标准化交互。

## Problem
- 现有AI代理即使能浏览网页、写代码、分析数据，也**无法跨组织直接与其他代理通信**，缺少统一地址、身份与信任机制。
- 企业间代理协作通常需要**API密钥、OAuth、Webhook和长期集成工程**，导致自动化服务编排成本高、扩展慢。
- 缺乏可验证身份与权限控制会带来**冒充、滥用和低可信交互**问题，这对真实商业流程很关键。

## Approach
- 用类似邮箱的 **Beam-ID**（如 `booking@lufthansa.beam.directory`）作为代理地址，并映射到 **Ed25519 密钥对** 与 **W3C DID**，实现无密码、可验证身份。
- 代理不发送自由聊天消息，而是发送**结构化 intent**：带有 intent 类型和 JSON payload 的签名请求，接收方先验签、解析身份，再返回结构化结果。
- 提供一个**目录/注册中心**，支持按 capability 搜索代理、解析 DID 文档、查看验证等级与 trust score，从而先“发现”再“通信”。
- 用**可验证凭证、邮箱/DNS/企业验证、历史成功交互、社区报告**等信号计算 trust score，并配合 whitelist/open 等安全策略控制谁可联系代理。
- 通过 **WebSocket relay + HTTP API + TS/Python SDK** 形成跨语言实现，目标是把代理互联从专用集成变成通用协议层。

## Results
- 文中给出两个端到端示例时延：航班预订代理请求在 **1.8 秒**完成，餐饮到配送代理请求在 **2.1 秒**完成；但这些是演示案例，不是系统化基准评测。
- 声称通信过程**无需 API keys、无需 OAuth、无需人工介入**，并在所有 intent 上执行 **Ed25519 签名校验**。
- 给出实现规模指标：**48+ API routes、21 个数据库表**，支持 **WebSocket 实时转发**、DID 解析、验证、信任评分与多目录联邦。
- trust score 例子：新建未验证代理起始分数约 **0.3**，有历史记录的 business-verified 代理可达到 **0.9+**。
- 提供可运行生态：**TypeScript SDK、Python SDK、CLI、Docker/self-hosted directory**，并支持 Stripe 付费升级；这说明项目更偏协议与产品化基础设施，而非论文式实验结果。
- **没有提供标准数据集、对照基线或正式定量实验**，因此最强的具体主张是：以标准身份+目录+签名 intent 机制，把跨组织代理对接时间从“数月API集成”缩短为即插即用式互通。

## Link
- [https://github.com/Beam-directory/beam-protocol](https://github.com/Beam-directory/beam-protocol)
