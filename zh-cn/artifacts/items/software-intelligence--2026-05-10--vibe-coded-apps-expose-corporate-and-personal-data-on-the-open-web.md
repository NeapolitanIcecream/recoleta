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
RedAccess 在 Lovable、Replit、Base44 和 Netlify 域名上发现了 5,000 多个由 AI 生成的 Web 应用，这些应用可被公开访问，且没有真正的访问控制。这个发现很重要，因为员工可能在正常安全审查之外发布带有企业或个人数据的工具。

## 问题
- AI 编码平台让用户能够快速创建并托管 Web 应用，而用户往往没有接受过安全培训。
- 缺失身份验证或薄弱的登录规则，可能让任何拥有或找到 URL 的人看到私有数据。
- 安全团队可能不知道这些应用存在，因此数据可能脱离已批准的软件开发和审查流程。

## 方法
- RedAccess 在 Google 和 Bing 上搜索由 Lovable、Replit、Base44 和 Netlify 托管的域名，并搭配可能暴露 AI 构建应用的关键词。
- 团队手动检查了暴露的应用，确认它们是否有身份验证、访问控制，或看起来属于私有的数据。
- WIRED 查看了截图，并核实有几个暴露的应用仍然在线。
- RedAccess 联系了一些疑似应用所有者；几名用户确认存在暴露问题，随后保护或移除了应用。

## 结果
- RedAccess 称其发现了 5,000 多个几乎没有安全措施或完全没有安全措施、可被公开访问的 AI 编码应用。
- 这些应用中约 40%，接近 2,000 个，似乎暴露了敏感数据。
- 报告称暴露的数据包括带有医生标识符的医院排班、广告购买记录、上市推广幻灯片、含客户姓名和联系方式的聊天机器人日志、货运记录、销售记录和财务记录。
- RedAccess 称，在一些案例中，暴露的应用可能允许管理访问，或允许移除其他管理员。
- RedAccess 还报告称，Lovable 上存在冒充 Bank of America、Costco、FedEx、Trader Joe’s 和 McDonald’s 的钓鱼网站。
- 相关公司对报告的部分内容提出异议，并指出可见性设置由用户控制；但摘录称，它们没有否认部分公开应用可在开放 Web 上访问。

## Problem

## Approach

## Results

## Link
- [https://www.wired.com/story/thousands-of-vibe-coded-apps-expose-corporate-and-personal-data-on-the-open-web/](https://www.wired.com/story/thousands-of-vibe-coded-apps-expose-corporate-and-personal-data-on-the-open-web/)
