---
source: hn
url: https://github.com/Beam-directory/beam-protocol
published_at: '2026-03-07T23:16:30'
authors:
- alfridus
topics:
- agent-communication
- decentralized-identity
- intent-protocol
- trust-and-verification
- multi-agent-systems
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Beam Protocol – SMTP for AI Agents (natural language agent-to-agent)

## Summary
Beam Protocol提出一个面向AI智能体的开放通信层，试图像SMTP之于电子邮件一样，为跨公司、跨框架、跨机器的智能体交互提供统一的身份、发现、验证与消息传递机制。它的核心卖点是让智能体通过可验证身份和结构化意图直接对话，而不需要传统API集成、OAuth或人工中介。

## Problem
- 现有AI智能体虽然能浏览网页、写代码、分析数据，但**无法可靠地与其他智能体互通**，尤其是在不同公司、不同框架、不同机器之间。
- 缺少智能体通信所需的基础设施：**地址体系、身份标识、信任验证、能力发现**，导致真实业务场景中仍需繁琐的API对接。
- 这很重要，因为跨组织的自动化服务协作（如订票、配送、客服转接、支付）若没有统一协议，就难以规模化落地。

## Approach
- 用 **Beam-ID + DID** 为每个智能体建立可解析身份：Beam-ID类似邮箱地址，映射到W3C兼容的DID文档，并绑定**Ed25519**密钥对进行加密身份认证。
- 通信不采用自由文本聊天，而采用**结构化、签名的intents**：发送方声明意图类型和JSON负载，接收方验证签名、DID和目录中的验证信息后响应。
- 提供一个**目录服务（directory）**，支持按能力搜索智能体、解析DID、查看验证等级和信任分数，从而完成“找谁、能做什么、是否可信”的发现流程。
- 引入**信任与安全机制**：信任分数基于验证等级、账号年龄、成功历史、社区报告、域名验证等因素；接收方还可配置白名单或最低信任阈值。
- 工程上通过 **WebSocket relay + HTTP API + TypeScript/Python SDK** 实现跨语言接入，并支持自托管目录、恢复短语、加密导出等身份管理功能。

## Results
- 文中给出一个航班预订示例：个人代理向 Lufthansa 代理发送 `booking.flight` intent，**总耗时 1.8 秒**，返回航班 `LH1132`、价格 `€149`、确认号 `BK-839271`；但这是演示案例，不是基准实验。
- 另一个配送示例中，餐厅代理向配送代理发送 `delivery.request`，**2.1 秒后** 返回骑手 `Max`、预计送达 `22min`、追踪号 `SPD-8291`；同样属于场景展示而非严格评测。
- 速度方面，协议宣称 intents 可通过WebSocket实现**sub-second**通信；安全方面宣称**所有intents都进行Ed25519签名验证**，并经过五层安全检查，但未提供误报率、吞吐、可用性等系统评测数据。
- 具体实现规模上，项目列出 **48+ API routes**、**21 database tables**，支持TypeScript、Python与HTTP/WS接入，表明其已具备较完整原型系统而不仅是概念设计。
- 信任分数示例：新的未验证代理默认 **0.3**，有历史记录的企业验证代理可达 **0.9+**；这是规则设定，不是实验结果。
- 总体而言，提供文本**没有给出标准数据集、对比基线或正式量化实验**；最强的具体主张是：无需API key、无需OAuth、无需人工参与，即可在秒级完成跨组织智能体调用。

## Link
- [https://github.com/Beam-directory/beam-protocol](https://github.com/Beam-directory/beam-protocol)
