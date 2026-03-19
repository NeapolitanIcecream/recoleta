---
source: hn
url: https://arstechnica.com/gadgets/2026/03/amazon-appears-to-be-down-with-over-20000-reported-problems/
published_at: '2026-03-05T23:12:32'
authors:
- samizdis
topics:
- service-outage
- amazon
- incident-report
- web-reliability
relevance_score: 0.0
run_id: materialize-outputs
language_code: zh-CN
---

# Amazon Appears to Be Down

## Summary
这篇文章报道了 2026 年 3 月 Amazon 出现的一次大规模服务中断事件，主要影响网站购物流程、商品页面和移动端访问。文中基于 Downdetector 数据与 Amazon 官方回应，概述了故障发生、扩散与恢复过程。

## Problem
- 文章要解决的问题是：**Amazon 当时是否发生了大范围服务故障、影响了哪些功能，以及何时恢复**。
- 这很重要，因为 Amazon 是超大规模电商与云服务平台，宕机会直接影响用户购物、结账与平台可用性。
- 对外部观察者和用户而言，及时确认故障范围、时间线和原因，有助于判断是否为个体网络问题还是平台级事故。

## Approach
- 文章核心方法非常简单：**汇总第三方故障报告平台 Downdetector 的用户上报数据，结合记者实际访问验证，再补充 Amazon 官方社交账号与后续声明**。
- 它先用时间序列数据判断故障何时开始、何时达到峰值、何时回落。
- 再用问题分类占比说明受影响最严重的功能模块，例如结账、移动 App 和商品页面。
- 最后通过 Amazon 官方声明给出事故原因：与一次**软件代码部署**有关，并确认问题已经修复。

## Results
- Downdetector 显示，问题报告自 **1:41 p.m. ET** 开始上升，到 **2:26 p.m. ET** 达到 **18,320** 份报告。
- 故障报告在 **3:32 p.m. ET** 达到峰值 **20,804**，说明这是一次大范围、短时高强度的服务中断。
- 按问题类型划分，约 **50%** 的报告与**结账**有关，**21%** 来自**移动 App** 用户，**17%** 指向**商品页面**问题。
- Ars Technica 实测确认：部分商品页面**无法正常加载或完全无法加载**，Amazon 首页也会间歇性加载失败。
- 到 **4:10 p.m. ET** 后故障报告开始下降，至 **5:55 p.m. ET** 明显回落；到当晚 **9:05 p.m. ET**，Downdetector 报告数降至 **435**。
- Amazon 后续声明称问题已解决，并明确原因为一次**软件代码部署相关故障**；文中未提供更深入的技术修复细节或系统级性能指标。

## Link
- [https://arstechnica.com/gadgets/2026/03/amazon-appears-to-be-down-with-over-20000-reported-problems/](https://arstechnica.com/gadgets/2026/03/amazon-appears-to-be-down-with-over-20000-reported-problems/)
