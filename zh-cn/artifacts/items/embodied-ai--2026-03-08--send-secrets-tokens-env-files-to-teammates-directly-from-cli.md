---
source: hn
url: https://github.com/rel-s/stringphone
published_at: '2026-03-08T22:54:26'
authors:
- rel0s
topics:
- cli-security
- end-to-end-encryption
- secure-messaging
- ssh-keys
- metadata-blind-relay
relevance_score: 0.02
run_id: materialize-outputs
language_code: zh-CN
---

# Send secrets/tokens/env-files to teammates directly from CLI

## Summary
这项工作介绍了 **stringphone**：一个命令行工具，用现有 SSH ed25519 密钥在终端里直接向队友发送消息、密钥和小文件。它强调端到端加密、短暂存储和“元数据盲”中继，让服务器几乎只负责转发密文。

## Problem
- 解决的问题是：开发者需要一种**从 CLI 直接发送 secrets/tokens/env 文件**给同事的简单方式，而不想依赖聊天软件、手工加密或长期存储服务。
- 这很重要，因为凭据和配置文件通常敏感；若服务器能读取内容、识别通信双方或长期保存数据，就会带来泄露和运维风险。
- 现有终端工作流里，安全传输往往要额外管理密钥或基础设施，门槛高、流程不顺。

## Approach
- 核心机制很简单：双方各自使用**已有的 SSH ed25519 密钥**，通过 **X25519 Diffie-Hellman** 独立算出同一个共享密钥，不传输私钥。
- 基于该共享密钥，再用 **BLAKE3** 生成方向相关的 mailbox ID，用 **HKDF-SHA256** 导出加密密钥，并用 **ChaCha20-Poly1305** 对消息进行机密性与完整性保护。
- 中继服务器只看到**不透明的 mailbox ID 和密文**；由于 mailbox ID 混入 DH shared secret，即使知道双方公钥，第三方也难以推断通信邮箱，从而降低参与者关联和覆盖写入风险。
- 消息是**短暂性的**：默认最大 5 KiB、TTL 为 5 分钟；客户端保存已见消息哈希并检查时间戳，以抵抗重放攻击。
- 交互上做成 Unix 风格 CLI：支持 `pair` 配对、stdin 自动判断发送/接收，并可从 GitHub 公钥导入对方 ed25519 key。

## Results
- 文本**没有提供正式论文式定量实验**，没有 benchmark、数据集、成功率或与基线方法的数值比较。
- 提出的最具体结果/能力声明包括：服务器默认**最大消息大小 5 KiB**，消息在服务器上默认只保留**5 分钟 TTL**。
- 协议开销被明确给出为**每条消息 37 字节**（1 字节版本号 + 12 字节 nonce + 8 字节时间戳 + 16 字节认证标签）。
- mailbox ID 为**64 字符十六进制字符串**，服务端响应包含 **201 / 413 / 429 / 400** 等状态码，用于表示写入成功、过大、邮箱满或 bad ID。
- 设计上声称的突破点不是精度指标，而是安全与易用性的结合：**服务器不能读取消息、不能识别参与者、也不能确定谁在和谁通信**，同时直接复用现有 SSH ed25519 身份。

## Link
- [https://github.com/rel-s/stringphone](https://github.com/rel-s/stringphone)
