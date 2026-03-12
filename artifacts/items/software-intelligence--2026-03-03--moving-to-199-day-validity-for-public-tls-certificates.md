---
source: hn
url: https://knowledge.digicert.com/alerts/public-tls-certificates-199-day-validity
published_at: '2026-03-03T23:54:39'
authors:
- thread_id
topics:
- tls-certificates
- certificate-lifecycle
- pki-operations
- security-automation
relevance_score: 0.18
run_id: materialize-outputs
---

# Moving to 199-day validity for public TLS certificates

## Summary
这是一份关于公有 TLS 证书有效期缩短的行业变更通知，而不是学术论文。它说明 DigiCert 将在 2026 年 2 月 24 日把最大证书有效期从 397 天降到 199 天，并提示企业尽快转向自动化证书生命周期管理。

## Problem
- 公有 TLS 证书的最长有效期将从 **397 天**缩短到 **199 天**，并且这是后续迈向约 **47/46 天**有效期的第一阶段。
- 更短有效期会显著增加续签、重签发、重复签发和校验维护频率，使**手工证书生命周期管理**越来越不可行。
- 如果企业的域名验证、组织验证或 API 调用逻辑未提前适配，可能导致证书申请时长不足、续签流程中断或运维负担上升。

## Approach
- DigiCert 计划自 **2026-02-24** 起，将新签发公有 TLS 证书的最大有效期统一限制为 **199 天**。
- 在 **CertCentral** 中，届时可选有效期变为：**199 天**、**不超过 199 天的自定义到期日**、以及**不超过 199 天的自定义时长**。
- 对 **CertCentral Services API**，如果请求仍按 **1 年**等更长期限提交，系统会**自动调整为 199 天**，以避免请求报错。
- 已在截止日前签发且有效期超过 199 天的证书**继续有效直到到期**；但在截止日后进行**续签、重签发、重复签发**时，都要遵守新的 **199 天上限**。
- 文档明确建议组织提前完成域名/组织验证，并采用 **ACME**、**Trust Lifecycle Manager** 等自动化方案，为未来进一步缩短到 **46 天**做准备。

## Results
- 关键变更时间点：自 **2026-02-24** 起，DigiCert 公有 TLS 证书最大有效期从 **397 天降至 199 天**。
- 长期路线图：这是迈向 **47 天**证书有效期过渡的第一阶段；到 **2029 年**，最大有效期将缩短到 **46 天**。
- 对现有已签发证书的影响：**2026-02-24 之前**签发且有效期大于 **199 天**的证书，**不会被提前失效**，而是持续受信任至自然到期。
- 对重签发/重复签发的影响：**2026-02-24 之前**，365/397 天证书的 reissue/duplicate 仍可到 **397 天**；**当日及之后**，上限变为 **199 天**。
- 对续签的影响：仍可在到期前 **90 天**开始 renew，但 **2026-02-24** 起实际签发的新证书最长只有 **199 天**。
- 文本未提供实验、基准测试或性能指标；最强的具体主张是：API 请求会被**自动改写为 199 天**以减少错误，并且未来 **46 天**有效期将使手工 CLM“不可行”。

## Link
- [https://knowledge.digicert.com/alerts/public-tls-certificates-199-day-validity](https://knowledge.digicert.com/alerts/public-tls-certificates-199-day-validity)
