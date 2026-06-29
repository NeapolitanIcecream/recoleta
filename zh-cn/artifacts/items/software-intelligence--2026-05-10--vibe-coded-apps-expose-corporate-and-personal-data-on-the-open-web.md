---
source: hn
url: https://www.wired.com/story/thousands-of-vibe-coded-apps-expose-corporate-and-personal-data-on-the-open-web/
published_at: '2026-05-10T22:05:48'
authors:
- abdelhousni
topics:
- ai-code-generation
- vibe-coding
- software-security
- data-exposure
- web-app-security
- human-ai-interaction
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Vibe-Coded Apps Expose Corporate and Personal Data on the Open Web

## Summary
## 摘要
RedAccess 在 Lovable、Replit、Base44 和 Netlify 的域名上发现了 5000 多个 AI 生成的网页应用，这些应用可以直接访问，几乎没有真正的访问控制。这个发现之所以重要，是因为员工可能在没有经过正常安全审查的情况下发布包含公司或个人数据的工具。

## 问题
- AI 编程平台让用户快速创建和托管网页应用，但用户往往没有接受过安全培训。
- 缺少身份验证或只用很弱的登录规则，会让拿到或找到网址的人看到私密数据。
- 安全团队可能不知道这些应用存在，数据就会绕开获批的软件开发和审查流程。

## 方法
- RedAccess 在 Google 和 Bing 上搜索了托管在 Lovable、Replit、Base44 和 Netlify 域名下的网页，使用了可能暴露 AI 构建应用的检索词。
- 团队手动检查了这些暴露的应用，查看它们是否有身份验证、访问控制或看起来像私密数据的内容。
- WIRED 查看了截图，并确认其中几个暴露的应用仍在运行。
- RedAccess 联系了部分看起来像应用所有者的人；几位用户确认了暴露情况，随后保护了应用或将其移除。

## 结果
- RedAccess 称，它发现了 5000 多个公开可访问、几乎没有安全措施的 AI 编码应用。
- 这些应用中约 40%，接近 2000 个，似乎暴露了敏感数据。
- 报告中提到的暴露数据包括带有医生标识符的医院排班、广告投放记录、上市营销演示文稿、包含客户姓名和联系方式的聊天机器人日志、运输货物记录、销售记录和财务记录。
- 在某些情况下，RedAccess 说这些暴露的应用可能允许管理访问，或者删除其他管理员。
- RedAccess 还报告了 Lovable 上的钓鱼网站，这些网站冒充 Bank of America、Costco、FedEx、Trader Joe’s 和 McDonald’s。
- 这些公司对报告的部分内容提出异议，并提到由用户控制的可见性设置，但摘录中说，它们没有否认有些公开应用可以在开放网络上访问。

## Problem

## Approach

## Results

## Link
- [https://www.wired.com/story/thousands-of-vibe-coded-apps-expose-corporate-and-personal-data-on-the-open-web/](https://www.wired.com/story/thousands-of-vibe-coded-apps-expose-corporate-and-personal-data-on-the-open-web/)
