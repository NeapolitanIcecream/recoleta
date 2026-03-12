---
source: hn
url: https://github.com/rel-s/stringphone
published_at: '2026-03-08T22:54:26'
authors:
- rel0s
topics:
- cli-security
- end-to-end-encryption
- secret-sharing
- developer-tooling
- metadata-privacy
relevance_score: 0.39
run_id: materialize-outputs
---

# Send secrets/tokens/env-files to teammates directly from CLI

## Summary
stringphone 是一个命令行工具，用现有 SSH ed25519 密钥在终端里直接向队友发送消息、密钥和小文件，并通过端到端加密与短期存储的中继减少泄露风险。它强调元数据盲化与极简 CLI 体验，让临时共享敏感信息更方便。

## Problem
- 解决团队在 CLI/开发流程中安全传递 secrets、tokens、env 文件和小型配置文件的问题；传统聊天、邮件或手工复制粘贴更容易泄露或留下长期痕迹。
- 仅做内容加密还不够，服务端若能识别通信双方、消息路由或长期保存数据，仍会暴露敏感协作关系与操作痕迹。
- 开发者需要一个几乎零额外基础设施、可直接复用现有 SSH 密钥的方案，否则安全工具往往因使用门槛高而不被采用。

## Approach
- 核心机制很简单：双方各自用自己的 SSH ed25519 密钥和对方公钥做 X25519 Diffie-Hellman，独立算出同一个共享密钥，无需传输私钥。
- 再用 `mailbox_id = BLAKE3(shared_secret || sender_pubkey || recipient_pubkey)` 生成定向邮箱 ID，使 `alice→bob` 与 `bob→alice` 不同；因为邮箱 ID 含共享密钥，第三方即使知道双方公钥也难以推断路由。
- 消息加密使用 HKDF-SHA256 从共享密钥派生方向绑定的加密键，再用 ChaCha20-Poly1305 对 `[timestamp][plaintext]` 加密，获得机密性和完整性保护。
- 为抗重放，客户端记录最近见过的消息哈希并检查时间戳，拒绝旧消息和重复消息；服务端只看到不透明邮箱 ID、密文、时间、大小和 IP。
- 工程上提供极简 CLI：支持 `pair`、自动识别 send/recv、从 GitHub 导入公钥，默认使用在线 relay，消息默认上限 5 KiB、TTL 5 分钟。

## Results
- 文本未提供标准基准测试、公开数据集或与其他工具的定量对比结果。
- 给出的明确系统参数包括：消息最大大小默认 **5 KiB**，服务端保留时间默认 **5 分钟**。
- 协议层消息总开销为 **37 字节**，由 **1-byte version + 12-byte nonce + 8-byte timestamp + 16-byte auth tag** 组成；服务端看到的密文长度约为明文长度 + **29 字节**。
- 共享密钥长度为 **32 字节**；邮箱 ID 为 **64 个十六进制字符**；消息认证依赖 Poly1305 的 **16 字节**标签。
- 具体可验证的安全性主张是：服务端**不能读取消息内容**、**不能直接识别参与者**、**不能确定谁在与谁通信**，且消息是**短暂存储**与**端到端加密**的。
- 实用性主张是：直接复用现有 **SSH ed25519** 密钥，无需额外认证头；若用户只有 RSA/ECDSA，则当前方案**不支持**，需另生成 ed25519 密钥。

## Link
- [https://github.com/rel-s/stringphone](https://github.com/rel-s/stringphone)
