---
source: hn
url: https://trashalert.io
published_at: '2026-03-05T23:23:29'
authors:
- hudtaylor
topics:
- civic-tech
- geospatial-data
- community-sourcing
- address-lookup
- notification-system
relevance_score: 0.18
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: I mapped 954K addresses because AI hallucinated my trash day

## Summary
这是一个面向居民的垃圾清运查询与提醒服务，核心是把市政开放数据与社区上报结合起来，提供按地址实时查询的收运日历。它并不是软件基础模型论文，但展示了一个由数据整合、地图可视化与社区校验驱动的实用型城市信息系统。

## Problem
- 解决居民不知道自家垃圾、回收与厨余收运日期的问题，尤其在节假日顺延规则存在时更容易混淆。
- 这个问题重要，因为错过清运会带来现实生活成本，而官方信息往往分散、难查，地址级查询体验不足。
- 文中还隐含指出，通用 AI 会在这类本地、细粒度、实时性强的信息上产生幻觉，因此需要可验证的数据系统替代纯生成式回答。

## Approach
- 以**地址查询**为入口：用户输入街道地址，系统从社区数据库中实时查找对应的垃圾、回收和厨余收运日期。
- 将**市政开放数据**与**社区报告**结合，并通过邻里验证来提升准确性，形成可持续扩展的地址级数据库。
- 提供**交互式地图**：把圣地亚哥地址按收运日着色，支持缩放、按日期过滤和按地址搜索。
- 内置**节假日顺延规则**，自动调整收运计划，而不是只返回静态日历。
- 用**提醒、排行榜、贡献激励**机制鼓励居民上报和维护数据，支持逐城市扩张。

## Results
- 系统声称已覆盖 **San Diego** 与 **Austin** 两个城市，并支持“city by city”持续扩展，但未给出更完整覆盖率指标。
- 页面标题声称作者“mapped **954K addresses**”，这是文中最强的量化规模信号，但摘录未提供数据来源、映射成功率或误差范围。
- 功能层面可查询 **3 类**收运：Trash、Organics、Recycling；其中 Trash/Organics 为**每周**收运，Recycling 为**隔周**收运（以 San Diego 三桶系统为例）。
- 支持 **2026 holiday schedule** 的顺延规则：从假日开始，该周后续收运**顺延 1 天**。
- 未提供标准研究型实验结果，如准确率、召回率、响应时间、与官方系统或其他工具的定量对比；最具体的结果是其已上线可用、具备实时查询、地图展示与邮件提醒能力。

## Link
- [https://trashalert.io](https://trashalert.io)
