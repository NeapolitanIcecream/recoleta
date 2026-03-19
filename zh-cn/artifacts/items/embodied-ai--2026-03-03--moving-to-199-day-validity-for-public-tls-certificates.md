---
source: hn
url: https://knowledge.digicert.com/alerts/public-tls-certificates-199-day-validity
published_at: '2026-03-03T23:54:39'
authors:
- thread_id
topics:
- tls-certificates
- certificate-lifecycle-management
- pkis
- acme
- security-operations
relevance_score: 0.01
run_id: materialize-outputs
language_code: zh-CN
---

# Moving to 199-day validity for public TLS certificates

## Summary
这是一则关于公有 TLS 证书有效期缩短的行业变更通知，而非学术研究论文。DigiCert 将从 2026 年 2 月 24 日起把公有 TLS 证书最大有效期从 397 天降至 199 天，并提示未来将进一步过渡到约 47/46 天。

## Problem
- 它要解决的问题是：行业正在收紧公有 TLS 证书的最长有效期，组织若不提前调整采购、续期和运维流程，可能会在证书签发、续期和重签发时遇到中断。
- 这件事重要，因为 TLS 证书是网站与在线服务建立信任和加密通信的基础；有效期变短会显著增加证书生命周期管理频率。
- 文中明确指出，到 2029 年最大有效期将缩短到 **46 天**，届时手工证书生命周期管理将“不切实际”，因此需要自动化。

## Approach
- 核心机制很简单：从 **2026-02-24** 起，DigiCert 对新签发的公有 TLS 证书实施 **199 天最大有效期** 限制，替代当前的 **397 天** 上限。
- 在 CertCentral 下单时，只提供三类选择：**199 天**、**不超过 199 天的自定义到期日**、以及 **不超过 199 天的自定义时长**。
- 对于 CertCentral Services API，请求中原本按 **1 年** 申请的公有 TLS 证书会被**自动调整为 199 天**，以避免请求报错并保持流程成功。
- 现有已在截止日前签发、且有效期大于 199 天的证书**不受影响**，仍可一直被信任到自然过期；但在截止日后续期、重签发或 duplicate issue 时，将受 **199 天** 上限约束。
- 为应对后续更短周期，文中建议采用自动化方案，如 **ACME**、CertCentral 自动化能力和 Trust Lifecycle Manager。

## Results
- 关键变更数字：公有 TLS 证书最大有效期将从 **397 天** 降到 **199 天**，生效日期为 **2026-02-24**。
- 这是多阶段过渡的第一步；文中称未来将走向 **47 天** TLS 证书，而“Prepare for the future”部分写明到 **2029 年** 最大有效期将缩短到 **46 天**。
- API 层面的直接结果：自 **2026-02-24** 起，经 CertCentral Services API 提交的 **1 年期** 公有 TLS 证书请求将被**自动改写为 199 天**，以减少“unexpected errors”。
- 续期窗口未变：证书仍可在到期前 **90 天** 进行续期，但自 **2026-02-24** 起新签发的续期证书最长也只有 **199 天**。
- 重签发/副本影响：**2026-02-24 之前**，365/397 天证书重签发或 duplicate issue 仍可达 **397 天**；**当日及之后**，上限变为 **199 天**。
- 文中**没有提供实验、基准数据集或性能指标**；最强的具体主张是该策略可帮助避免 API 请求失败，并表明未来短周期将使手工 CLM 不再可行。

## Link
- [https://knowledge.digicert.com/alerts/public-tls-certificates-199-day-validity](https://knowledge.digicert.com/alerts/public-tls-certificates-199-day-validity)
