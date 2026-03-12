---
source: hn
url: https://goldrush.dev/agents/
published_at: '2026-03-06T23:45:23'
authors:
- Ferns765
topics:
- blockchain-data
- agent-tools
- multi-chain
- portfolio-tracking
- pricing-api
relevance_score: 0.02
run_id: materialize-outputs
---

# GoldRush Agent Skills for blockchain data and pricing

## Summary
这不是一篇研究论文，而是一段关于 GoldRush Agent Skills 的产品/开发者文档摘录。它主要介绍如何把 GoldRush 集成到 AI 编码代理中，用于访问区块链数据与价格信息。

## Problem
- 要让 AI 代理处理区块链场景，通常需要统一获取**多链**资产余额、代币数据和价格信息，这对开发者来说集成成本较高。
- 不同链（如 Ethereum、Base、Polygon）数据接口分散，构建跨链投资组合追踪器等应用会比较麻烦。
- 这类能力之所以重要，是因为 AI 代理若不能稳定访问链上数据，就难以执行有用的区块链分析与自动化任务。

## Approach
- 核心方法很简单：提供一个可安装的 **GoldRush Agent Skills/SDK**，让 AI 编码代理直接调用 GoldRush 的区块链数据能力。
- 文本给出的典型用法是：用 GoldRush SDK 构建一个**多链投资组合追踪器**，统一拉取 Ethereum、Base 和 Polygon 上的代币余额。
- 集成方式被描述为开发者友好，示例安装命令为 `npx skills add covalenthq/goldrush-agent-skills`。
- 从机制上看，它更像是“把现成的数据 API 封装成 agent 可调用技能”，而不是提出新的学习算法或模型架构。

## Results
- 提供的文本**没有任何定量实验结果**，没有数据集、指标、基线或性能比较。
- 最强的具体声明是：可将 GoldRush 集成到你喜欢的 AI 编码代理中，并支持构建**多链 portfolio tracker**。
- 明确列出的链包括 **3 条**：Ethereum、Base、Polygon。
- 明确列出的安装方式有 **1 个**：`npx skills add covalenthq/goldrush-agent-skills`。
- 因为没有实验数字，无法判断其在准确率、延迟、覆盖率或价格数据质量上相对其他方案的提升幅度。

## Link
- [https://goldrush.dev/agents/](https://goldrush.dev/agents/)
