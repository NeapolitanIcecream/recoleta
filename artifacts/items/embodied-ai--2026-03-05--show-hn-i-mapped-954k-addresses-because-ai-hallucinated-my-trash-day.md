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
relevance_score: 0.02
run_id: materialize-outputs
---

# Show HN: I mapped 954K addresses because AI hallucinated my trash day

## Summary
TrashAlert 是一个面向居民的垃圾收运查询与提醒网站，帮助用户快速查到垃圾、回收和厨余收运日，并用社区共建补全数据。其核心价值在于把分散的市政开放数据与邻里上报整合成可搜索、可提醒、可视化的地址级服务。

## Problem
- 解决居民不知道自家垃圾收运日期、节假日顺延规则复杂、容易错过倒垃圾时间的问题。
- 市政信息往往分散、难查或不够细到地址级，导致实际使用门槛高。
- 通过社区报告补足缺失区域与更新信息，对覆盖扩张和数据准确性都重要。

## Approach
- 用户输入街道地址，系统基于**municipal open data**和**community reports**实时查询该地址的收运安排。
- 提供地址级结果，展示垃圾、回收、厨余的收运日，并自动考虑节假日顺延。
- 用交互式地图按收运日给地址着色，支持缩放、按天过滤和地址搜索，便于整街/社区查看。
- 采用社区共建机制：用户可以上报自己的收运日、帮助邻居补全数据库，并通过排行榜激励参与。
- 声称地址查询实时处理且**不存储**用户搜索内容，以降低隐私顾虑。

## Results
- 覆盖规模的最具体数字是标题声称“mapped **954K addresses**”，表明其已建立大规模地址级映射。
- 当前明确支持 **2** 个城市：**San Diego** 与 **Austin**，并声称将逐城扩展。
- 在 San Diego，说明了 **three-bin system**：黑桶与绿桶为**每周**收运，蓝桶为**每两周一次**；黑/绿桶收运日覆盖 **Mon-Fri**。
- 提供 **2026 holiday schedule** 规则：逢指定假日停收，且从假日起该周后续收运**顺延 1 天**。
- 文本未提供严格论文式评测指标、对比基线或精度/F1/召回等定量实验结果；最强的具体主张是大规模地址映射、实时查询、节假日自动调整以及社区验证的数据构建流程。

## Link
- [https://trashalert.io](https://trashalert.io)
