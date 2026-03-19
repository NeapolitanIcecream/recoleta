---
source: hn
url: https://qualitymax.io/vibe-check
published_at: '2026-03-13T23:58:41'
authors:
- qualitymax
topics:
- application-security
- ai-generated-code
- vibe-coding
- security-testing
- playwright
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# What Did You Forget to Prompt? $87,500 in Fraud from Vibe-Coded Startup

## Summary
这篇文章用一个公开案例说明：把 AI 生成的原型代码直接上线、却不做安全审计，会迅速演变成真实欺诈与数据泄露风险。核心主张是用自动化安全爬虫加生成式测试，在上线前像攻击者一样扫描并拦截“vibe-coded”应用中的常见漏洞。

## Problem
- 文章要解决的问题是：创始人使用生成式编程工具快速搭建并上线产品，但常常遗漏最基础的安全设计与审计，导致密钥暴露、认证缺失、XSS、CSRF 等漏洞直接进入生产环境。
- 这很重要，因为问题并非高难度攻击，而是前端明文密钥、开放管理面板、未鉴权 API 这类“低门槛高损失”失误，能直接造成欺诈收费、PII 泄露、合规事故和长期重构成本。
- 文中强调 AI 会回答“你问的问题”，但不会自动完成系统级安全架构思考；因此仅靠提示式开发容易把可运行原型误当成可安全运营的产品。

## Approach
- 核心方法很简单：让 QualityMax 像攻击者一样自动爬取网站、接口和前端 JS 包，寻找暴露密钥、失效鉴权、缺失安全头和 OWASP Top 10 漏洞。
- 系统在发现问题后，不只给报告，还会输出漏洞严重级别、修复说明以及对应 OWASP 参考，帮助开发者快速补救。
- 它还能自动生成 Playwright 安全测试脚本，把这些检查放进 CI/CD，让每次部署都重复验证相同风险。
- 文章通过复刻真实被攻破的“vibe-coded”创业应用模式，展示工具如何在上线前发现这些常见但致命的错误配置与实现缺陷。

## Results
- 文中案例声称，一名创始人因把 **Stripe secret key** 放在前端，被攻击者直接从 DevTools 复制后滥用，导致 **175 名客户各被扣 $500**，创始人报告损失 **$2,500 in Stripe fees**。
- 文章还给出更广泛的损失描述：类似事故可带来 **$200K+** 的重建成本，以及 **4–8 个月** 的系统重构周期；但这些是案例性陈述，不是受控实验结果。
- 在其复刻的演示应用中，作者声称包含 **24 vulnerabilities**，扫描结果为 **6 CRITICAL, 8 HIGH, 5 MEDIUM, 3 LOW**，覆盖暴露密钥、开放管理面板、未鉴权接口、XSS、无 CSRF 等问题。
- 对自动化测试，文中给出的预期结果是 **25 tests, 25 failures**，并称这意味着“every vulnerability caught”；但注意这里是厂商自建 demo 与自述结果，没有独立基准或第三方评测。
- 文章还举例称开放管理面板可返回 **340 user records**，包括姓名、邮箱、电话、地址和部分 SSN，且 **zero authentication required**，用来说明风险严重性。
- 没有提供学术论文常见的标准数据集、对比基线或统计显著性；最强证据是多个公开事故案例与一个可复现实验性演示环境。

## Link
- [https://qualitymax.io/vibe-check](https://qualitymax.io/vibe-check)
