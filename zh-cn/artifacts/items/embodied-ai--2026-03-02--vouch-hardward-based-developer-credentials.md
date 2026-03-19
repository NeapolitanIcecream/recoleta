---
source: hn
url: https://vouch.sh
published_at: '2026-03-02T23:19:07'
authors:
- jplock
topics:
- developer-credentials
- hardware-authentication
- fido2
- credential-broker
- access-control
relevance_score: 0.03
run_id: materialize-outputs
language_code: zh-CN
---

# Vouch - Hardward based developer credentials

## Summary
Vouch 是一个基于 FIDO2 硬件验证的开发者凭证代理，用一次实体触碰换取多种短时、限权的开发凭证。它试图解决长期密钥泛滥、无法确认“人是否在场”、以及 AI 代理共享人类高权限凭证的问题。

## Problem
- 现代开发工作流存在**凭证蔓延**：SSH 密钥、AWS 长期访问密钥、GitHub PAT 等往往长期有效、分散存储且难以统一治理。
- 现有 MFA 往往只能验证设备，**不能确认真人在场**；一旦笔记本或缓存凭证被攻破，攻击者可被当作合法用户。
- AI 编码助手常直接继承开发者凭证，导致**权限过大、缺乏作用域限制、审计困难**，也难区分是人还是代理执行了操作。

## Approach
- 核心机制很简单：用户先**触碰 FIDO2 硬件密钥**并通过 PIN 完成一次硬件级验证，证明真人在场。
- 然后 Vouch 作为**凭证代理/经纪人**，为不同工具签发**短时、限权、带硬件证明、绑定设备**的凭证，而不是让用户长期保存静态密钥。
- 它可发放多类原生凭证：**SSH 证书、AWS 会话、GitHub token、Kubernetes 配置**等，并通过原生集成接入 SSH、AWS CLI、git、kubectl、docker、cargo 等，无需额外 wrapper。
- 对 AI 代理，Vouch 提供**作用域受限、时间受限**的凭证，并宣称可通过密码学审计轨迹区分**人类操作**与**代理操作**，支持快速撤销。
- 系统强调**可审计性与开源性**：CLI 和 agent 采用 Apache-2.0/MIT，服务器端代码为 BSL 1.1，并在 2 年后转为 Apache-2.0。

## Results
- 文本**没有提供标准学术实验、基准数据或量化指标**，因此没有可报告的准确率、成功率、吞吐或安全评测数字。
- 最强的具体能力声明是：用户通过**一次 FIDO2 硬件验证**，即可在“**all day**”范围内获取多类开发凭证。
- 其明确覆盖的凭证/系统包括：**SSH、AWS、GitHub、Kubernetes**，并支持 **AWS CLI、git、kubectl、docker、cargo、CodeArtifact、CodeCommit** 等原生集成。
- 安全性方面的核心主张是：凭证是**short-lived**、**scoped**、**hardware-attested**、**device-bound**，并且可对 AI 代理实现**即时撤销**与**人/代理区分审计**。
- 开源可审计方面的具体声明是：**CLI 和 agent 开源**，**server 源码可见**，服务器许可在 **2 年后**转为 Apache-2.0。

## Link
- [https://vouch.sh](https://vouch.sh)
