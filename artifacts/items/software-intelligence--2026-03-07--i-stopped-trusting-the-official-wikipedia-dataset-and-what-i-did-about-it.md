---
source: hn
url: https://omarkamali.com/blog/wikipedia-monthly-pipeline
published_at: '2026-03-07T22:52:41'
authors:
- omneity
topics:
- dataset-pipeline
- wikipedia-corpus
- data-engineering
- multilingual-nlp
- low-resource-languages
relevance_score: 0.77
run_id: materialize-outputs
---

# I stopped trusting the official Wikipedia dataset, and what I did about it

## Summary
这篇文章提出并实现了一个按月更新的多语言 Wikipedia 语料构建流水线，用来替代长期停滞的官方 HuggingFace Wikipedia 数据集。其核心价值在于补齐过时快照遗漏的大量文章，尤其改善低资源语言和新近建立语言版本的训练数据可用性。

## Problem
- 官方 HuggingFace Wikipedia 数据集长期未更新，作者发现 2025 年仍在使用 2023 快照，导致明显数据缺失；例如摩洛哥阿拉伯语数据集中约 **8,000** 篇，而网站已有 **11,000+** 篇，约 **30%** 知识缺失。
- 直接使用 Wikimedia 原始 dump 并不容易：MediaWiki 标记、模板嵌套、条件逻辑和语言本地化命名空间会让朴素清洗产生错误文本，污染训练语料。
- 在 340+ 语言规模上运行时，还面临 API 不稳定、磁盘/内存瓶颈和大规模上传失败等工程问题，这使得持续更新的数据生产十分困难。

## Approach
- 核心方法是走“务实折中”路线：先用 **mwparserfromhell** 解析结构，再用**确定性规则**处理模板、条件和清洗细节，而不是运行完整 MediaWiki 引擎。
- 为解决各语言命名空间本地化问题，作者自动收集并人工清洗所有语言版本的 MediaWiki namespace labels，发布为独立数据集 **omarkamali/wikipedia-labels**，用于跨语言正确剥离如 Category/تصنيف/Catégorie 等标签。
- 将单语言清洗流程参数化，扩展为覆盖 **340+ Wikipedia editions** 的通用月度流水线，并提供 **10k / 5k / 1k** 子集，降低下游用户的存储与内存门槛。
- 为解决资源瓶颈，作者定位到复杂嵌套模板是主要内存热点，随后用**内存监控调度**替代简单互斥锁：只有当内存低于阈值时才调度新任务，从而动态控制并行度。

## Results
- 处理效率显著提升：全量多语言处理时间从 **12–14 天** 降到作者笔记本上的 **3 天**，在服务器上可做到 **<24 小时**。
- 数据覆盖明显优于官方版本：最新构建基于 **2026 snapshot**，比大多数研究者默认使用的官方 HuggingFace Wikipedia 数据集**新 3 年**。
- 文章规模提升具体可观：摩洛哥阿拉伯语从 **8,000** 提升到 **11,000+**；英语相比官方版本**多出约 700,000 篇**；阿拉伯语**多出约 100,000 篇**。
- 全局数据增量上，作者声称总体语料规模的**中位数增长为 6.8%**，且部分语言出现“爆发式增长”。
- 覆盖新增语言方面，有 **31 种语言**是在 2023 年后才加入 Wikipedia，因此在作者发布前**从未有可用文本语料**。
- 影响力方面，作者声称该数据集已被 **Nous Research 用于训练 Hermes 4**，并被 **INRIA HAL lab** 等论文引用；不过文中未提供更标准的基准任务分数或模型性能对比。

## Link
- [https://omarkamali.com/blog/wikipedia-monthly-pipeline](https://omarkamali.com/blog/wikipedia-monthly-pipeline)
