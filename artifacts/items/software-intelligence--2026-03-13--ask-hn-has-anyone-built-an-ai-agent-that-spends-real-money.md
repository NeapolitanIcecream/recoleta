---
source: hn
url: https://news.ycombinator.com/item?id=47371289
published_at: '2026-03-13T23:16:04'
authors:
- xodn348
topics:
- ai-agents
- autonomous-commerce
- payments-infrastructure
- browser-automation
- agentic-transactions
relevance_score: 0.81
run_id: materialize-outputs
---

# Ask HN: Has anyone built an AI agent that spends real money?

## Summary
这不是一篇正式论文，而是一则关于“能自主花真钱的 AI 代理”可行性的实践求助帖。核心价值在于清晰暴露了支付、风控、合规与平台封锁等现实瓶颈，说明该方向虽被卡组织看好，但开发者基础设施仍明显缺失。

## Problem
- 要解决的问题是：让 AI 代理在用户授权后，能够自主完成浏览商品、选择下单和真实支付的闭环。
- 这很重要，因为它是从“会建议”走向“会执行”的关键一步，直接关系到代理型电商、自动采购和更广义的可执行 AI 助手落地。
- 当前主要障碍包括发卡机构不配合个人开发者、Stripe 的 3D Secure 离线支付限制、电商网站封禁浏览器自动化，以及大型平台上自动化操作的法律风险。

## Approach
- 作者正在构建一个 MCP server，把 AI 代理连接到支付通道，如 Stripe、PayPal 和虚拟卡。
- 目标机制很简单：用户先提供一次支付凭证，之后代理自行完成“找商品—做决策—付款”。
- 该方案依赖现有支付 rail 与浏览器自动化，而不是新型支付协议，因此会直接受到支付认证、反欺诈和网站策略限制。
- 文中还把 Visa 的 **Intelligent Commerce** 和 Mastercard 的 **Agent Pay** 作为行业信号，说明卡组织正在为“代理消费”铺路，但开发者可用工具还不成熟。

## Results
- 没有提供正式实验、基准数据或量化结果；没有数据集、准确率、成功率、交易转化率等数字。
- 最强的具体进展是作者“已经在做”一个连接 Stripe、PayPal、虚拟卡的 MCP 支付服务，并公开了仓库：`clawpay`。
- 文中列出的关键现实结论是：**Stripe 需要 3D Secure 处理 off-session payments**，这使“代理自行付款”在现有电商支付流程中难以无缝完成。
- 另一项具体结论是：主流电商平台会拦截浏览器自动化，而 **Amazon v. Perplexity（文中称 3 月 9 日）** 被作者视为浏览器自动化存在真实法律风险的佐证。
- 行业层面的积极信号是 **Visa Intelligent Commerce** 和 **Mastercard Agent Pay** 已发布，但文中没有给出其可用性、覆盖率或开发者接入数据。

## Link
- [https://news.ycombinator.com/item?id=47371289](https://news.ycombinator.com/item?id=47371289)
