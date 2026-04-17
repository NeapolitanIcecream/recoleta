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
## 摘要
AuthProof 提出一种加密委托回执，用来记录用户在操作员向 AI 代理发送指令之前实际授权了什么。目标是用签名回执、仅追加日志和逐动作审计记录，让操作员改动、越权和未授权操作都能被发现。

## 问题
- 论文中提到的现有 IETF 代理身份方案，包括 AIP、draft-klrc-aiagent-auth 和 WIMSE，覆盖的是服务到代理的授权，但没有给用户提供其原始意图的加密记录。
- 在 User → Operator → Agent → Services 这条链路中，操作员可以在指令到达代理之前扩展、更改或删除内容，用户事后也无法证明自己批准过什么。
- 这个缺口会影响审计、合规、争议处理和代理安全，因为代理和服务缺少一个经过签名的真实依据，无法确认哪些范围和硬性限制是用户批准过的。

## 方法
- 核心机制是用户使用 WebAuthn/FIDO2 硬件支持密钥创建并签名的 Delegation Receipt，并在任何代理动作开始前写入仅追加日志。
- 回执包含一份结构化的允许操作白名单、明确且不可覆盖的禁止项、一个基于日志时间检查的有效时间窗口，以及委托时操作员指令文本的哈希值。
- 对于可执行操作，回执指向 Safescript 程序静态 capability DAG 的哈希，因此如果哈希不匹配，批准后就不能替换成另一个程序。
- 工具服务器可以发布已签名的 capability manifest，而回执引用的是 manifest 哈希，不是操作员提供的 schema，这样可以检查工具描述是否发生漂移。
- 每个代理动作都会引用回执哈希，并写入带签名链式结构的 Action Log；如果某个动作超出授权范围，系统要求用户为该特定动作重新签署一个 micro-receipt。

## 结果
- 摘录中没有报告基准测试结果、正式评估指标，或与基线的数据集对比。
- 论文称，用户可以证明自己授权了什么，因为回执在任何代理动作发生前就已经签名并写入日志，之后如果操作员指令与之不一致，可以通过比较哈希发现。
- 论文称，在根据回执进行验证时，超出范围的动作在加密意义上无效，因为作用域默认拒绝，边界也被明确写出，例如禁止 `deletes` 或访问 `payment-methods`。
- Action Log 在条目之间使用 SHA-256 链接，并支持用 `diff()` 比较已授权范围和已记录动作；示例显示先有 2 条合规记录，随后 1 条违规记录，内容是 `Send email`，其 `0% scope match` 和 `92% boundary overlap`。
- 论文还提到一个实现限制：v1 时间戳使用客户端时钟，生产环境中的合规部署应改用 RFC 3161 可信时间戳机构。

## Problem

## Approach

## Results

## Link
- [https://github.com/Commonguy25/authproof-sdk](https://github.com/Commonguy25/authproof-sdk)
