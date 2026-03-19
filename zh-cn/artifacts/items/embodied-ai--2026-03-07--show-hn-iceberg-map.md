---
source: hn
url: https://icebergmap.com/
published_at: '2026-03-07T23:45:19'
authors:
- aosmith
topics:
- p2p-networking
- webrtc
- anonymous-reporting
- privacy-preserving
relevance_score: 0.01
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Iceberg Map

## Summary
Iceberg Map 是一个基于浏览器的点对点匿名目击报告网络，强调无账号、无服务器、无追踪。它主要是一个隐私优先的 WebRTC 应用，而不是一篇机器人或基础模型研究论文。

## Problem
- 试图解决匿名事件/目击上报中的**中心化依赖**问题：传统平台通常需要账号、服务器和日志，带来审查、单点故障与隐私泄露风险。
- 试图解决**用户可追踪性**问题：若上报系统收集身份、设备或网络元数据，匿名性会被削弱。
- 这很重要，因为对敏感事件的上报场景中，用户往往最在意隐私保护、抗审查和最小化信任假设。

## Approach
- 核心机制很简单：让浏览器之间**直接通信**，用 WebRTC 在对等节点间共享报告，而不是先发到中心服务器。
- 系统设计原则是**无账号、无服务器、无追踪**，从产品层面尽量减少身份绑定与集中式数据留存。
- 页面显示网络层指标，如 connected peers、sightings received/sent、syncs completed、dedup cache、blocked connections，说明其采用了**P2P 同步与去重**机制。
- 明确声明“**No data passes through a central server**”以及“**No identifying information is collected or transmitted**”，其匿名性主要依赖于去中心化传输与最小数据收集。

## Results
- 提供的内容**没有论文式定量实验结果**，没有数据集、基线方法、准确率、延迟、吞吐或匿名性评测数字。
- 唯一可见数字是产品页面状态：版本为 **v0.1.0**，示例界面中 **Connected Peers = 0**、**Sightings Received = 0**、**Sightings Sent = 0**、**Syncs Completed = 0**，这些不是性能结果。
- 最强的具体主张是：**所有连接都通过 WebRTC 直接点对点建立**，并且**没有数据经过中心服务器**。
- 另一项核心主张是：**不上账号，不收集或传输可识别信息**，因此目标是实现匿名上报。

## Link
- [https://icebergmap.com/](https://icebergmap.com/)
