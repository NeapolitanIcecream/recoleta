---
source: hn
url: https://qualitymax.io/vibe-check
published_at: '2026-03-13T23:58:41'
authors:
- qualitymax
topics:
- application-security
- ai-code-generation
- vibe-coding
- security-testing
- owasp
relevance_score: 0.01
run_id: materialize-outputs
---

# What Did You Forget to Prompt? $87,500 in Fraud from Vibe-Coded Startup

## Summary
这篇文章不是学术论文，而是一篇围绕“vibe-coded”创业应用安全失误的案例与产品宣传材料。核心观点是：仅靠提示驱动的 AI 编码会遗漏系统安全设计，导致真实资金损失、数据泄露和高昂重构成本。

## Problem
- 文章要解决的问题是：创始人使用 AI 快速生成并上线产品时，常把原型直接当生产系统，遗漏安全审计、架构审查和基础防护，导致前端暴露密钥、鉴权缺失、XSS、CSRF 等漏洞。
- 这很重要，因为后果是直接的财务损失和合规风险：文中案例包括 **$87,500 欺诈交易**、**$2,500 Stripe 费用损失**、**175 名客户被错误收取 $500**、以及医疗数据泄露后被迫关停。
- 文章强调 AI 会写“能运行的代码”，但不会主动思考攻击面；如果开发者没有明确要求安全性，系统就可能带着致命漏洞上线。

## Approach
- 核心方法很简单：用一个名为 **QualityMax** 的 AI 爬虫把应用当作攻击者来浏览，自动扫描页面、API 端点和 JavaScript bundle，寻找暴露密钥、认证缺失、安全头缺失和 OWASP Top 10 漏洞。
- 工具不仅报告问题，还会给出漏洞严重级别、修复说明和 OWASP 参考，目的是让非安全专家也能定位和修补问题。
- 它还会自动生成 **Playwright** 安全测试脚本，把这些检查变成可在 CI/CD 中重复运行的测试，从而在每次部署时检测是否重新引入漏洞。
- 文中通过一个“仿真的脆弱 fintech SaaS”演示该机制：复刻现实中 vibe-coded 初创公司被攻破后常见的同类漏洞，再验证扫描器和测试能否全部发现。

## Results
- 文中最突出的真实案例数字是：创始人把 **Stripe secret key** 放在前端后，攻击者直接从源码复制密钥，导致 **175 名客户各被收取 $500**，总计约 **$87,500** 欺诈交易；创始人称自己承担了 **$2,500** 费用后才轮换密钥。
- 对于清理代价，文中给出的经验性数字是：安全债修复往往需要 **4–8 个月重构**，还有 **$200K+** 的重建成本，以及客户流失后难以挽回。
- 在其演示应用中，作者声称共复现了 **24 个漏洞**，扫描结果为 **6 CRITICAL / 8 HIGH / 5 MEDIUM / 3 LOW**，覆盖暴露密钥、开放管理后台、泄露 API、XSS、无 CSRF 等问题。
- 生成的 Playwright 测试据称达到 **25 个测试、25 个失败**，即“每个漏洞都被捕获”；文中列举了 Stripe key、Supabase service role key、OpenAI key、管理员面板未鉴权、缺失 CSP 等失败项。
- 文章还给出若干轶事性案例：发现 **3 个** ProductHunt 上线项目暴露的 Stripe key；有人 2 天做出 MVP，却花 **3 个月** 清理安全债；这些都用于支持“vibe coding 正在系统性制造生产安全问题”的论点。
- 但需要注意：文本没有提供正式实验设计、公开基准、对照方法或同行评审结果，因此这些结果更像案例证据和产品宣称，而非严格学术评测。

## Link
- [https://qualitymax.io/vibe-check](https://qualitymax.io/vibe-check)
