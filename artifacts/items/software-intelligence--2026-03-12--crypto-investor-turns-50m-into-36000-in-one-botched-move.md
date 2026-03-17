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
---

# Crypto investor turns $50M into $36,000 in one botched move

## Summary
这不是一篇研究论文，而是一则关于 DeFi 大额交易滑点事故的案例报道。它说明了在浅流动性池中执行超大额兑换时，即使界面给出警告，用户仍可能因滑点而遭受几乎全部资金损失。

## Problem
- 文章讨论的问题是：在去中心化金融中，超大额代币兑换如果直接打入浅流动性池，会因**极端滑点**导致成交价格严重偏离预期。
- 这很重要，因为单笔用户操作就可能造成数千万美元损失，而且价值会被套利机器人、区块构建者等市场参与者迅速抽走。
- 该案例还暴露出：即使前端界面提供风险提示，用户确认机制也未必足以防止灾难性执行结果。

## Approach
- 这篇文章没有提出新的研究方法，而是基于**链上数据**和相关方说明，对一次失败交易进行事后分析。
- 核心机制可以用最简单的话说：用户试图把约 **5043 万美元** 的 aEthUSDT 一次性换成 aEthAAVE，但目标池子太浅，导致成交价格被自己砸穿。
- 当价格在交易过程中剧烈偏移时，**套利机器人**会立刻吃掉价差，把本应属于用户的价值转走。
- Aave 创始人表示，界面曾多次提示异常滑点，并要求用户在移动设备上手动确认风险，交易路由本身按预期执行。

## Results
- 用户尝试兑换 **$50,432,688** 的 aEthUSDT，最终只得到约 **327 枚 aEthAAVE**，价值约 **$36,000**。
- 该交易的滑点超过 **99%**，意味着用户在单笔操作中损失了几乎全部价值。
- BlockSec 表示，同一区块中的套利者共提取了超过 **$43 million** 的利润。
- 其中约 **$32.6 million** 流向了区块构建者（block builder）。
- Aave 方面称计划向受影响用户返还约 **$600,000** 的交易手续费。
- 文中没有给出实验数据、基准模型或数据集对比；最强的具体结论是，该事件证明了 DeFi 中大额交易对浅流动性和 MEV/套利机制极其敏感。

## Link
- [https://www.coindesk.com/markets/2026/03/12/crypto-investor-turns-usd50-million-into-usd36-000-in-one-botched-move](https://www.coindesk.com/markets/2026/03/12/crypto-investor-turns-usd50-million-into-usd36-000-in-one-botched-move)
