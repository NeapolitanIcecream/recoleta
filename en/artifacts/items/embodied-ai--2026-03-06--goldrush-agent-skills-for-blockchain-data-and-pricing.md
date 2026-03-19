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
language_code: en
---

# GoldRush Agent Skills for blockchain data and pricing

## Summary
This is not a research paper, but rather an excerpt from product/developer documentation about GoldRush Agent Skills. It mainly explains how to integrate GoldRush into AI coding agents to access blockchain data and pricing information.

## Problem
- To enable AI agents to handle blockchain use cases, developers typically need a unified way to retrieve **multi-chain** asset balances, token data, and pricing information, which makes integration relatively costly.
- Data interfaces across different chains, such as Ethereum, Base, and Polygon, are fragmented, making it cumbersome to build applications like cross-chain portfolio trackers.
- This capability matters because if AI agents cannot reliably access on-chain data, it is difficult for them to perform useful blockchain analysis and automation tasks.

## Approach
- The core approach is simple: provide an installable **GoldRush Agent Skills/SDK** so AI coding agents can directly call GoldRush's blockchain data capabilities.
- The typical usage described in the text is to build a **multi-chain portfolio tracker** with the GoldRush SDK that fetches token balances across Ethereum, Base, and Polygon in a unified way.
- The integration is described as developer-friendly, with the example installation command `npx skills add covalenthq/goldrush-agent-skills`.
- Mechanistically, this is more like “packaging an existing data API into agent-callable skills” rather than proposing a new learning algorithm or model architecture.

## Results
- The provided text contains **no quantitative experimental results**—no datasets, metrics, baselines, or performance comparisons.
- The strongest concrete claim is that GoldRush can be integrated into your preferred AI coding agent and supports building a **multi-chain portfolio tracker**.
- The explicitly listed chains include **3**: Ethereum, Base, and Polygon.
- There is **1** explicitly listed installation method: `npx skills add covalenthq/goldrush-agent-skills`.
- Because there are no experimental figures, it is not possible to judge how much it improves over other solutions in accuracy, latency, coverage, or pricing data quality.

## Link
- [https://goldrush.dev/agents/](https://goldrush.dev/agents/)
