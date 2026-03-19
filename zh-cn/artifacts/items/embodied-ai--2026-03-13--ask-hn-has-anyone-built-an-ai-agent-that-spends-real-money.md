---
source: hn
url: https://news.ycombinator.com/item?id=47371289
published_at: '2026-03-13T23:16:04'
authors:
- xodn348
topics:
- ai-agents
- autonomous-payments
- agentic-commerce
- browser-automation
- payment-infrastructure
relevance_score: 0.1
run_id: materialize-outputs
language_code: zh-CN
---

# Ask HN: Has anyone built an AI agent that spends real money?

## Summary
这不是一篇研究论文，而是一则 Hacker News 求助帖，讨论“让 AI 代理自主花真钱购物”是否已经有人真正做出来。核心价值在于它清晰暴露了支付、合规、反自动化与法律风险等现实落地障碍。

## Problem
- 要解决的问题是：让 AI 代理在用户授权后，能够自主完成浏览商品、选择商品并实际付款的闭环购买流程。
- 这件事重要，因为它是“AI 代理真正执行现实世界任务”的关键一步，涉及支付网络、商户网站、身份验证和责任归属。
- 帖子指出的主要障碍包括：发卡机构不理个人开发者、Stripe 的离线支付受 3D Secure 限制、电商平台封禁浏览器自动化，以及针对自动化购物的法律风险。

## Approach
- 作者已在做一个 MCP server，目的是把 AI 代理连接到支付提供商，如 Stripe、PayPal 和虚拟卡。
- 设想的机制很简单：用户先给代理一张卡或支付权限，代理随后自己完成“找商品—下单—支付”。
- 帖子并未提出新的算法或模型，而是聚焦系统集成层：支付 rails、浏览器自动化、电商结账流程和合规可行性。
- 文中还引用 Visa 的“Intelligent Commerce”和 Mastercard 的“Agent Pay”，说明大支付网络在推动 agentic commerce，但开发者工具链仍不成熟。

## Results
- 没有给出任何实验、基准、数据集或定量结果；这不是论文，而是问题征集帖。
- 最强的具体主张是当前落地卡点：**Stripe 离线支付需要 3D Secure**、**主要电商会拦截浏览器自动化**、**Amazon v. Perplexity（2025-03-09）显示存在真实法律风险**。
- 文中提到的行业信号包括：**Visa 发布“Intelligent Commerce”**，**Mastercard 推出“Agent Pay”**，表明支付网络认为该方向具有前景。
- 作者还提出一个产品可行性问题：用户是否愿意信任 AI 使用**500 美元预付卡**代为购物，但未报告任何用户实验或部署结果。

## Link
- [https://news.ycombinator.com/item?id=47371289](https://news.ycombinator.com/item?id=47371289)
