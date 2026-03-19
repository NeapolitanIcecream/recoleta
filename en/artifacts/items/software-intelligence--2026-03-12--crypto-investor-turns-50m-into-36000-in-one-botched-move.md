---
source: hn
url: https://www.coindesk.com/markets/2026/03/12/crypto-investor-turns-usd50-million-into-usd36-000-in-one-botched-move
published_at: '2026-03-12T23:03:28'
authors:
- scrlk
topics:
- defi
- slippage
- mev
- arbitrage
- liquidity-risk
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Crypto investor turns $50M into $36,000 in one botched move

## Summary
This is not a research paper, but a case report about a large DeFi trade slippage incident. It shows that when executing an unusually large swap against a shallow liquidity pool, a user can still lose nearly all funds to slippage even if the interface provides warnings.

## Problem
- The issue discussed in the article is that, in decentralized finance, if an unusually large token swap is sent directly into a shallow liquidity pool, **extreme slippage** can cause the execution price to deviate severely from expectations.
- This matters because a single user action can cause losses of tens of millions of dollars, while the value can be rapidly extracted by market participants such as arbitrage bots and block builders.
- The case also reveals that even if the frontend interface provides risk warnings, the user confirmation mechanism may still be insufficient to prevent catastrophic execution outcomes.

## Approach
- The article does not propose a new research method; instead, it provides an after-the-fact analysis of a failed trade based on **on-chain data** and statements from relevant parties.
- The core mechanism, put simply, is that the user attempted to swap about **$50.43 million** of aEthUSDT for aEthAAVE in a single transaction, but the target pool was too shallow, causing the execution price to collapse under the trade's own impact.
- When the price shifts sharply during execution, **arbitrage bots** immediately capture the spread and extract value that would otherwise have remained with the user.
- The Aave founder said the interface repeatedly warned about abnormal slippage and required the user to manually confirm the risk on a mobile device, and that the trade routing itself executed as intended.

## Results
- The user attempted to swap **$50,432,688** of aEthUSDT and ultimately received only about **327 aEthAAVE**, worth roughly **$36,000**.
- The trade incurred more than **99%** slippage, meaning the user lost nearly all value in a single transaction.
- BlockSec said arbitrageurs in the same block extracted more than **$43 million** in profit.
- Of that, about **$32.6 million** went to the block builder.
- Aave said it planned to return about **$600,000** in transaction fees to the affected user.
- The article does not provide experimental data, baseline models, or dataset comparisons; its strongest concrete conclusion is that this event demonstrates how highly sensitive large DeFi trades are to shallow liquidity and MEV/arbitrage mechanisms.

## Link
- [https://www.coindesk.com/markets/2026/03/12/crypto-investor-turns-usd50-million-into-usd36-000-in-one-botched-move](https://www.coindesk.com/markets/2026/03/12/crypto-investor-turns-usd50-million-into-usd36-000-in-one-botched-move)
