---
source: hn
url: https://choosejoy.com.au
published_at: '2026-03-14T23:38:44'
authors:
- savvyllm
topics:
- ai-agents
- trust-network
- agent-discovery
- mcp
- decentralized-systems
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Joy – Trust Network for AI Agents to Verify Each Other

## Summary
Joy 是一个面向 AI agents 与 MCP servers 的去中心化发现与信任网络，让代理可以注册、搜索并相互背书。其核心目标是为代理生态提供一种简单的可验证信任层，以提升发现质量与协作安全性。

## Problem
- AI agents 和 MCP servers 缺少统一的去中心化发现与信任机制，用户很难判断某个代理是否可信。
- 仅靠名称或描述搜索容易被低质量、伪装或身份不明的代理干扰，影响代理间协作与工具调用安全。
- 如果不能证明端点归属或累积来自其他代理的信誉，代理生态很难形成可扩展的信任网络。

## Approach
- 提供一个网络服务层，支持代理注册、搜索发现、查看详情、统计信息，以及供 AI 助手接入的 MCP endpoint。
- 采用“代理互相担保”的机制：一个代理可以对另一个代理发起 vouch，作为信任信号累积到 trust score。
- 信任分数规则非常直接：每个 vouch 增加 0.3 分，最高 3.0 分，形成简单可解释的信誉上限机制。
- 对完成 endpoint ownership proof 的 verified agents，在搜索发现中给予更高优先级，把身份验证与社交背书结合起来。

## Results
- 文本未提供标准学术实验、基准数据集或与 baseline 的定量对比结果。
- 给出了明确的机制性数字：每个 vouch 为目标代理增加 **0.3** 信任分，trust score 上限为 **3.0**。
- 系统已公开多个可用接口：`/agents/discover`、`/agents/register`、`/vouches`、`/agents/:id`、`/stats`、`/mcp`，表明其已具备可部署的原型能力。
- 其 strongest claim 是：通过去中心化注册 + 代理互相背书 + 端点所有权验证，可提升代理发现排序中的可信度与优先级，但 excerpt 中没有给出提升幅度。

## Link
- [https://choosejoy.com.au](https://choosejoy.com.au)
