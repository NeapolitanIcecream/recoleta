---
source: hn
url: https://daniel.haxx.se/blog/2026/03/09/10k-curl-downloads-per-year/
published_at: '2026-03-09T23:02:13'
authors:
- donutshop
topics:
- open-source-metrics
- software-measurement
- curl
- ecosystem-analytics
relevance_score: 0.31
run_id: materialize-outputs
language_code: zh-CN
---

# 10K Curl Downloads per Year

## Summary
这篇文章批评 Linux Foundation “Insights” 对开源项目影响力的度量方法，指出其对 curl 年下载量的统计严重失真。作者用多个实际分发渠道的数据说明，单一聚合指标会显著低估真实使用规模。

## Problem
- 文章要解决的问题是：**开源项目平台给出的“下载量”指标是否可信，以及这种指标失真为何危险**。
- 这很重要，因为基金会或评分平台的数字会被用来“评级”项目健康度、影响力和资源分配，但错误指标会误导社区、用户和决策者。
- 文中以 curl 为例，指出所谓年下载量 **10,467** 与实际传播方式完全不符。

## Approach
- 作者不是提出新算法，而是用**反例审计**的方法，抓住 Linux Foundation Insights 中一个具体指标进行拆解。
- 核心机制很简单：把平台声称的 curl 年下载量，与 curl 在多个真实分发渠道上的公开/已知规模做直接对比。
- 对比的渠道包括：官网 release tarball 下载、Docker 镜像拉取、quay.io 镜像拉取、git 仓库克隆，以及操作系统预装、Linux/BSD 包管理分发、libcurl 被嵌入到应用和设备中的间接分发。
- 论点是：如果一个“下载量”定义无法覆盖这些主要分发路径，那么它并不代表项目真实采用度，只是某个狭窄来源的片面计数。

## Results
- Linux Foundation Insights 声称：curl 过去一年下载量为 **10,467**。
- 作者给出的官网数据是：curl release tarball 从 curl.se 的下载约为 **250,000/月**，折合约 **3,000,000/年**，已经远高于 10,467。
- Docker 渠道中，curl 镜像拉取约 **400,000–700,000/天**；quay.io “大致相同”，意味着两者合计约 **800,000–1,400,000/天**，折合约 **2.92亿–5.11亿/年**。
- curl 的 git 仓库被克隆约 **32,000/天**，折合约 **1,168万/年**。
- 另外还有未量化但重要的分发：Linux/BSD 发行版安装、Windows 与 macOS 默认预装、以及 libcurl 被大量应用、游戏、设备、汽车、电视、打印机和服务嵌入。文章没有给出统一总量，但最强结论是：**10,467 这一数字与 curl 的真实分发规模相比低估了多个数量级**。

## Link
- [https://daniel.haxx.se/blog/2026/03/09/10k-curl-downloads-per-year/](https://daniel.haxx.se/blog/2026/03/09/10k-curl-downloads-per-year/)
