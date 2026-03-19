---
source: hn
url: https://snapfair.pages.dev/
published_at: '2026-03-04T23:17:12'
authors:
- Herliken
topics:
- bill-splitting
- receipt-scanning
- ocr
- consumer-web-app
relevance_score: 0.0
run_id: materialize-outputs
language_code: zh-CN
---

# I made a website where you can: Scan a bill. Split it fairly. No app needed

## Summary
这不是一篇研究论文，而是一个用于扫描账单并公平分摊费用的网页产品说明。它描述了从扫描小票、校正条目到给多人分配消费项并发起付款请求的基本流程。

## Problem
- 解决多人聚餐后**手动拆分账单麻烦、易出错、效率低**的问题。
- 重要性在于现实生活中账单分摊是高频需求，若没有工具，常需人工计算每个人应付金额。
- 提供“无需安装 App”的网页方式，降低使用门槛。

## Approach
- 通过网页端**扫描账单/小票**，让用户将收据对准取景框完成读取。
- 系统似乎会先自动提取商品和价格，再允许用户**编辑姓名或价格、删除识别错误**，说明存在基础 OCR/结构化录入流程，但文中未给出技术细节。
- 用户可**添加同桌所有人**，然后通过点击人物把每个消费项分配给对应的人。
- 最后生成**共享分账结果**，并支持“有人与你共享账单”或“有人请求付款”这类后续结算流程。

## Results
- 文本**没有提供任何定量实验结果**，没有数据集、准确率、召回率、时延、基线比较或用户研究数字。
- 最强的具体产品性声明是：**“No app needed”**，即无需安装 App 即可使用。
- 还声明**“This may take a few seconds”**，暗示扫描/处理耗时为几秒，但未给出精确数值或测试条件。
- 另一个明确声明是**“It's free forever”**，表示产品永久免费，但这不是研究性能指标。

## Link
- [https://snapfair.pages.dev/](https://snapfair.pages.dev/)
