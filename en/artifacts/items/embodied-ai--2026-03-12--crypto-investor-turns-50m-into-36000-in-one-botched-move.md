---
source: hn
url: https://www.coindesk.com/markets/2026/03/12/crypto-investor-turns-usd50-million-into-usd36-000-in-one-botched-move
published_at: '2026-03-12T23:03:28'
authors:
- scrlk
topics:
- defi
- slippage
- amm-liquidity
- mev
- arbitrage
relevance_score: 0.0
run_id: materialize-outputs
language_code: en
---

# Crypto investor turns $50M into $36,000 in one botched move

## Summary
This is a news report about a DeFi trading incident, not an academic paper. It describes how a user swapped roughly $50 million in assets on Aave/CoW Protocol into tokens worth only about $36,000 due to an extremely large trade and extreme slippage.

## Problem
- The issue discussed in the article is that, in decentralized finance, unusually large orders routed into very shallow liquidity pools can produce **extreme slippage**, causing catastrophic losses for traders.
- This matters because once an on-chain transaction is executed, it is usually irreversible, and any price dislocation can be captured instantly by arbitrage bots and block builders, allowing an ordinary user to lose a huge amount of money in a single action.
- The article also implicitly highlights a product and risk-control issue: even when the interface provides risk warnings, users may still confirm high-risk transactions on mobile devices.

## Approach
- The article does not propose any new algorithm, model, or research method; it is mainly an **after-the-fact analysis and mechanism explanation** of an on-chain incident.
- The core mechanism, in the simplest terms, is that the user attempted to use about $50 million of aEthUSDT to buy aEthAAVE, but the corresponding market liquidity was too thin, so the execution price was effectively crushed by the order itself, resulting in **more than 99% slippage**.
- Once the price was severely distorted by this large order, arbitrage bots and network intermediaries immediately captured the spread within the same block, turning most of the loss into their own profit.
- According to the Aave founder, the interface had already issued multiple warnings about “extraordinary slippage risk” before the trade and required the user to explicitly check a confirmation box, indicating that the system followed normal procedures but did not prevent the user from proceeding.

## Results
- The user attempted to swap **$50,432,688** of **aEthUSDT** for **aEthAAVE**.
- The transaction actually incurred **more than 99% slippage**, ultimately yielding only about **327 aEthAAVE**, worth about **$36,000**.
- By the article’s framing, the loss from this single transaction was on the order of **$50 million**.
- BlockSec said that, within the **same block**, arbitrageurs extracted **more than $43 million** in profit, of which **$32.6 million** went to the block builder.
- Aave said it planned to return about **$600,000** in transaction fees to the affected user.
- The article does not provide experimental data, baseline models, or dataset comparisons; the strongest concrete takeaway is that this incident shows how executing extremely large DeFi trades in shallow liquidity pools can lead to devastating consequences from slippage and MEV/arbitrage extraction.

## Link
- [https://www.coindesk.com/markets/2026/03/12/crypto-investor-turns-usd50-million-into-usd36-000-in-one-botched-move](https://www.coindesk.com/markets/2026/03/12/crypto-investor-turns-usd50-million-into-usd36-000-in-one-botched-move)
