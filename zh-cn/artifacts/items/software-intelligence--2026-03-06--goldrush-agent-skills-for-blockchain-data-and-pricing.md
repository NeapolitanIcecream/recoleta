---
source: hn
url: https://goldrush.dev/agents/
published_at: '2026-03-06T23:45:23'
authors:
- Ferns765
topics:
- blockchain-data
- ai-coding-agents
- multi-chain
- portfolio-tracking
- sdk-integration
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# GoldRush Agent Skills for blockchain data and pricing

## Summary
这不是一篇传统研究论文，而是 GoldRush 面向 AI 编码代理提供的区块链数据与定价技能集。它旨在让代理更容易接入多链资产余额和定价数据，用于构建如投资组合追踪器之类的应用。

## Problem
- 需要让 AI coding agents 方便地访问区块链数据与价格信息，否则构建链上应用要分别处理多链数据源与集成复杂性。
- 多链场景下，像 Ethereum、Base、Polygon 这类网络的数据获取与统一查询会增加开发门槛。
- 这件事重要，因为它直接影响自动化软件生产和代理驱动开发能否快速落地到真实 Web3 应用。

## Approach
- 提供可被 AI coding agents 集成的 **GoldRush Agent Skills**，作为区块链数据和定价能力的封装接口。
- 通过 `npx skills add covalenthq/goldrush-agent-skills` 进行安装，把能力接入开发者常用的 AI 编码代理工作流。
- 用 GoldRush SDK 支持构建多链 portfolio tracker，示例中可拉取 Ethereum、Base、Polygon 上的 token balances。
- 核心机制可以简单理解为：把复杂的多链链上数据查询与价格访问，打包成代理可直接调用的“技能”。

## Results
- 提供的文字**没有给出正式定量实验结果**，没有论文式指标、数据集、基线或消融对比。
- 最具体的能力声明是：可让开发者“Integrate GoldRush with your favorite AI coding agents”。
- 最具体的应用声明是：可“Build a multi-chain portfolio tracker”并获取 **3 条链** 的 token balances：**Ethereum、Base、Polygon**。
- 最具体的落地信号是提供了可执行安装命令：`npx skills add covalenthq/goldrush-agent-skills`。以下结论更像产品能力说明，而非经验证的研究突破。

## Link
- [https://goldrush.dev/agents/](https://goldrush.dev/agents/)
