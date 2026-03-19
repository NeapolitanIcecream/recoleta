---
source: hn
url: https://snapfair.pages.dev/
published_at: '2026-03-04T23:17:12'
authors:
- Herliken
topics:
- receipt-scanning
- bill-splitting
- web-app
- ocr
- payment-request
relevance_score: 0.18
run_id: materialize-outputs
language_code: zh-CN
---

# I made a website where you can: Scan a bill. Split it fairly. No app needed

## Summary
SnapFair 是一个无需安装应用的网页工具，用于扫描账单并在多人之间公平分摊费用。它试图把线下餐饮结账中的手工计算、逐项分配和催款流程简化为一个可分享的轻量体验。

## Problem
- 解决多人聚餐后**账单扫描、项目分配、费用公平分摊**繁琐且容易出错的问题。
- 传统做法常需要手动录入、心算分账，或者要求所有人安装同一个应用，使用门槛高。
- 该问题重要在于它是高频生活场景，影响付款效率、社交体验和收款准确性。

## Approach
- 用手机网页直接**扫描账单**，不需要下载 App。
- 系统先从账单中提取条目与价格，随后允许用户**编辑名字或价格、删除识别错误**，说明其流程是“自动识别 + 人工校正”。
- 用户可**添加同桌人员**，并通过点击人员把每个菜品/项目分配给对应的人。
- 支持**分享分账结果**，并显示“someone shared a bill split with you / someone is requesting payment”，表明其还覆盖分享与收款请求环节。

## Results
- 文本**没有提供任何定量结果**，未给出准确率、处理时延、用户数、转化率或与竞品/基线的比较。
- 最强的具体产品声明是：**“No app needed”**，即无需安装应用即可完成分账流程。
- 还声明扫描过程**“may take a few seconds”**，只给出了模糊的速度预期，没有具体秒数。
- 产品能力层面的明确功能包括：扫描账单、编辑识别结果、添加人员、逐项分配、分享分账、发起付款请求。

## Link
- [https://snapfair.pages.dev/](https://snapfair.pages.dev/)
