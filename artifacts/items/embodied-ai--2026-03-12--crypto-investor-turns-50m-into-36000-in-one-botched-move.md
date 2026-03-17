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
---

# Crypto investor turns $50M into $36,000 in one botched move

## Summary
这是一则关于DeFi交易事故的新闻，而非学术论文。它描述了一名用户在Aave/CoW Protocol上因超大额换币与极端滑点，约将5000万美元资产换成了仅约3.6万美元的代币。

## Problem
- 文章讨论的问题是：在去中心化金融中，超大额订单若打入流动性很浅的池子，会产生**极端滑点**，导致交易者遭受灾难性损失。
- 这很重要，因为链上交易一旦执行通常不可逆，价格错位会被套利机器人和区块构建者瞬间捕获，普通用户可能在一次操作中损失巨额资金。
- 文中也隐含了一个产品与风控问题：即使界面给出风险提示，用户仍可能在移动端确认高风险交易。

## Approach
- 这篇文章没有提出新的算法、模型或研究方法；它主要是对一笔链上事件的**事后分析与机制解释**。
- 核心机制可以用最简单的话说：用户试图用约5000万美元的aEthUSDT去买aEthAAVE，但市场里对应流动性太薄，结果成交价格被自己“砸穿”，出现了**超过99%的滑点**。
- 当价格被这笔大单严重扭曲后，套利机器人和网络中介立即在同一区块内吃掉价差，把大部分损失转化为自己的利润。
- Aave创始人称，界面在交易前已多次提示“异常滑点风险”，并要求用户显式勾选确认，说明系统按常规流程运行，但没有阻止用户继续执行。

## Results
- 用户尝试交换 **$50,432,688** 的 **aEthUSDT** 为 **aEthAAVE**。
- 交易实际发生了 **超过99%滑点**，最终只得到约 **327 aEthAAVE**，价值约 **$36,000**。
- 以文中口径，单笔交易损失大约 **$50 million** 量级。
- BlockSec称，在**同一区块**内，套利者共提取了 **超过$43 million** 的利润，其中 **$32.6 million** 归于区块构建者（block builder）。
- Aave方面表示计划向受影响用户返还约 **$600,000** 的交易手续费。
- 文中没有提供实验数据、基准模型或数据集对比；最强的具体结论是，这次事故显示了在浅流动性池中执行超大额DeFi交易时，滑点与MEV/套利提取会造成毁灭性后果。

## Link
- [https://www.coindesk.com/markets/2026/03/12/crypto-investor-turns-usd50-million-into-usd36-000-in-one-botched-move](https://www.coindesk.com/markets/2026/03/12/crypto-investor-turns-usd50-million-into-usd36-000-in-one-botched-move)
