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
- decentralized-systems
relevance_score: 0.15
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Iceberg Map

## Summary
Iceberg Map 是一个基于浏览器的点对点匿名目击报告网络，强调**无账号、无服务器、无追踪**。它把报告直接通过 WebRTC 在浏览器之间传播，目标是提供更私密、去中心化的信息共享方式。

## Problem
- 现有上报/地图类系统通常依赖中心化服务器，容易形成**单点控制、审查、日志留存和隐私泄露**风险。
- 用户若要提交敏感目击信息，常被要求注册账号或暴露可追踪元数据，这会降低参与意愿。
- 需要一种**无需信任中心平台**、可在普通浏览器中直接运行的匿名共享机制。

## Approach
- 使用 **WebRTC** 在浏览器之间建立**直接点对点连接**，让数据不经过中心服务器转发。
- 系统设计原则是**no accounts, no servers, no tracking**，即不要求身份注册，也不收集或传输可识别个人信息。
- 通过对等网络在浏览器节点间同步“sighting reports”，把每个用户浏览器同时作为客户端和网络参与者。
- 界面展示网络运行指标，如已连接节点数、收到/发送的报告数、同步次数、去重缓存和被阻止连接数，说明其核心是轻量 P2P 同步网络。

## Results
- 提供文本中**没有论文式定量实验结果**，未给出数据集、基线方法、准确率、时延、吞吐或匿名性评测数字。
- 最强的具体实现性声明是：**所有连接均通过 WebRTC 直接点对点建立，数据不经过中心服务器**。
- 原型页面显示系统版本为 **v0.1.0**，采用 **AGPL-3.0** 许可证，表明这是一个早期可运行原型而非成熟评测论文系统。
- 页面列出了可观测运行指标（如 Connected Peers、Sightings Received/Sent、Syncs Completed、Dedup Cache），但摘录中对应数值基本为 **0 或未连接状态**，因此无法据此证明实际性能突破。

## Link
- [https://icebergmap.com/](https://icebergmap.com/)
