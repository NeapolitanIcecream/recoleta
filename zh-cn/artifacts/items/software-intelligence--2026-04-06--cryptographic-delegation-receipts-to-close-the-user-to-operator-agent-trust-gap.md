---
source: hn
url: https://github.com/Commonguy25/authproof-sdk
published_at: '2026-04-06T23:18:12'
authors:
- Commomguy
topics:
- agent-authentication
- delegation-protocols
- ai-agent-security
- auditability
- human-ai-interaction
relevance_score: 0.85
run_id: materialize-outputs
language_code: zh-CN
---

# Cryptographic delegation receipts to close the user-to-operator agent trust gap

## Summary
## 总结
AuthProof 提出一种加密委托回执，用来记录用户在 оператор 向 AI 代理发送指令之前实际授权了什么。目标是通过签名回执、追加式日志和按操作审计记录，让操作方改动、范围越界和未授权行为都能被发现。

## 问题
- 文中提到的现有 IETF 代理身份工作，包括 AIP、draft-klrc-aiagent-auth 和 WIMSE，覆盖的是服务到代理的授权，但没有给用户留下原始意图的加密记录。
- 在 User → Operator → Agent → Services 这条链路里，operator 可以在指令到达 agent 之前扩展、修改或删减指令，而用户之后无法证明自己批准了什么。
- 这个缺口会影响审计、合规、争议处理和代理安全，因为 agent 和服务缺少一份签名过的、关于用户批准范围和硬性限制的可信来源。

## 方法
- 核心机制是由用户用 WebAuthn/FIDO2 硬件支持密钥创建的签名 Delegation Receipt，并在任何代理动作开始前锚定到追加式日志。
- 回执包含结构化的允许操作清单、不可覆盖的明确禁止项、按日志时间校验的有效期，以及委托时 operator 指令文本的哈希。
- 对于可执行动作，回执指向 Safescript 程序静态 capability DAG 的哈希，这样如果哈希不匹配，批准后就不能换成另一段程序。
- 工具服务器可以发布签名的 capability manifest，回执引用的是 manifest 哈希，而不是 operator 提供的 schema，这样可以检查工具描述是否发生漂移。
- 每个代理动作都引用回执哈希，并写入签名的链式 Action Log；如果动作超出范围，系统会要求针对该具体动作重新生成用户签名的 micro-receipt。

## 结果
- 摘要没有报告基准测试结果、正式评估指标或与基线的数据集对比。
- 论文声称，用户可以证明自己授权了什么，因为回执是在任何代理动作之前签名并记录的，而之后若与 operator 指令不一致，可以通过比较哈希发现。
- 论文声称，超出范围的动作在按回执校验时在加密上无效，范围采用默认拒绝，并带有明确边界，例如阻止 `deletes` 或访问 `payment-methods`。
- Action Log 使用条目之间的 SHA-256 链接，并支持 `diff()` 来比较已授权范围和记录的动作；示例显示 2 条合规条目，随后 `Send email` 出现 1 次违规，`0% scope match` 和 `92% boundary overlap`。
- 论文还说明了一个实现限制：v1 时间戳使用客户端时钟，生产环境的合规部署应改用 RFC 3161 受信任时间戳机构。

## Problem

## Approach

## Results

## Link
- [https://github.com/Commonguy25/authproof-sdk](https://github.com/Commonguy25/authproof-sdk)
