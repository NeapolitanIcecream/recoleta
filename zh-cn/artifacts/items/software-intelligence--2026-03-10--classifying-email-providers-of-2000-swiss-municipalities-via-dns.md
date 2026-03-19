---
source: hn
url: https://mxmap.ch/
published_at: '2026-03-10T23:08:13'
authors:
- notmine1337
topics:
- dns-analysis
- digital-sovereignty
- email-infrastructure
- public-sector-tech
relevance_score: 0.18
run_id: materialize-outputs
language_code: zh-CN
---

# Classifying email providers of 2000 Swiss municipalities via DNS

## Summary
该项目通过公开 DNS 记录，对约 2,100 个瑞士市镇的官方邮箱服务商进行分类并可视化，以提升对公共部门邮件基础设施的透明度。其核心价值在于支持围绕数字主权与数据管辖风险的公共讨论。

## Problem
- 许多市镇使用哪类邮件服务商并不透明，公众难以了解公共通信基础设施的实际依赖关系。
- 这件事之所以重要，是因为美国服务商可能受 **US CLOUD Act** 约束，带来跨境数据访问与数字主权担忧。
- 仅凭直观观察很难系统识别全国范围内各市镇的邮件提供商分布，因此需要一种可扩展、可复核的方法。

## Approach
- 项目抓取每个瑞士市镇官方域名的公开 **DNS** 信息，重点检查 **MX** 和 **SPF** 记录。
- 根据这些记录推断邮件由谁路由、哪些发送方被授权，并据此将市镇归类到不同的 provider type。
- 结果被按辖区分组展示在一张覆盖全国市镇的地图上，便于观察服务商格局。
- 方法尽量依赖公开、可验证的数据源；同时明确声明：DNS 只能反映邮件路由和授权发送者，**不能直接证明数据实际存储位置**。
- 代码和数据已开源在 GitHub，支持外部审查和错误反馈。

## Results
- 覆盖范围：展示了约 **2,100** 个瑞士市镇的官方邮箱提供商分类地图。
- 数据来源：对每个市镇官方域名检查公开 **MX + SPF** 记录后进行分类。
- 论文摘录中**没有提供**准确率、召回率、F1、人工标注对比或基线方法等定量评测结果。
- 最强的具体主张是：该系统让瑞士市镇邮件服务商版图“可见化”，从而为数字主权讨论提供可操作的证据基础。
- 另一个明确主张是：分类依据是公开 DNS 信号，因此具有可复核性，但结论受限于 DNS 不能直接揭示数据存储地点。

## Link
- [https://mxmap.ch/](https://mxmap.ch/)
