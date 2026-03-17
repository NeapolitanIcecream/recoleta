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
- multi-agent-systems
relevance_score: 0.91
run_id: materialize-outputs
---

# Show HN: Joy – Trust Network for AI Agents to Verify Each Other

## Summary
Joy 是一个面向 AI 代理与 MCP 服务器的去中心化发现与信任网络，让代理能够注册、搜索彼此，并通过相互担保建立可计算的信任分数。它试图解决开放代理生态中“如何找到可信代理”的基础设施问题。

## Problem
- 开放的 AI 代理生态需要一种机制来**发现**可用代理与 MCP 服务，否则代理协作和工具调用难以扩展。
- 仅靠目录或自报信息不够，系统还需要判断**哪些代理更可信**，因为低质量或伪造代理会影响自动化任务的安全性与可靠性。
- 这件事重要在于，多代理软件工程、代理网络和智能操作环境都依赖可验证的代理身份与可排序的信任信号。

## Approach
- Joy 提供一个去中心化风格的代理目录与 API：代理可注册，其他代理或客户端可按名称、描述、能力搜索发现目标代理。
- 核心机制非常简单：代理之间可以提交 **vouch**（担保）；每个担保给被担保代理增加 **0.3** 的信任分，最高 **3.0**。
- 系统还支持 **endpoint ownership proof**（端点所有权验证）；完成验证的代理在搜索发现中获得更高优先级。
- 它暴露标准化接口，包括 `/agents/register`、`/agents/discover`、`/vouches`、`/agents/:id`、`/stats`，以及供 AI 助手接入的 `/mcp` MCP 端点。

## Results
- 文本**没有提供正式实验、基准测试或论文式定量结果**，因此无法报告准确的性能提升、召回率、成功率或与基线方法的对比数字。
- 已给出的最具体机制性数字是：**每个 vouch 增加 0.3 信任分，最高 3.0**，说明其信任计算采用线性累积上限模型。
- 系统声称可实现对代理的**去中心化发现与信任**，并支持 Claude Code 通过 MCP 接入，但未给出数据集、用户规模、误报率或延迟指标。
- 另一个明确主张是：**完成端点所有权证明的代理会在发现排序中获得优先级**，但未量化这种排序策略带来的效果。

## Link
- [https://choosejoy.com.au](https://choosejoy.com.au)
