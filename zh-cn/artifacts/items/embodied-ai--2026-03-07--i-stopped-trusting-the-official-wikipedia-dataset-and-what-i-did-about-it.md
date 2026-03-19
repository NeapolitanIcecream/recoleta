---
source: hn
url: https://omarkamali.com/blog/wikipedia-monthly-pipeline
published_at: '2026-03-07T22:52:41'
authors:
- omneity
topics:
- wikipedia-dataset
- data-pipeline
- multilingual-corpus
- data-cleaning
- low-resource-languages
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# I stopped trusting the official Wikipedia dataset, and what I did about it

## Summary
这篇文章指出官方 HuggingFace Wikipedia 数据集长期未更新，导致许多语言尤其低资源语言的数据严重缺失。作者构建了一个可每月更新、覆盖 340+ 语言版本的 Wikipedia 清洗与发布流水线，以提供更完整、更干净的文本语料。

## Problem
- 官方 Wikipedia 数据集快照过旧；例如作者在 2025 年发现摩洛哥阿拉伯语仍停留在 2023 快照，数据集仅 **8,000** 篇，而线上已有 **11,000+** 篇，约 **30%** 内容缺失。
- MediaWiki 标记语言和模板系统非常复杂，直接清洗容易产生错误文本；不同语言的命名空间标签也本地化，若不识别会把无关标签混入训练语料。
- 将流程扩展到全语言时，会遇到 API 访问脆弱、磁盘空间不足、内存瓶颈和大规模上传不稳定等工程问题，这会阻碍研究者获得新鲜且高质量的 Wikipedia 语料。

## Approach
- 采用折中方案：先用 **mwparserfromhell** 做结构解析，再通过**确定性规则**处理模板、条件逻辑和语言特定标签，目标是从原始 dump 中提取干净纯文本。
- 自动收集各 Wikipedia 语言版本的 MediaWiki 命名空间标签，并发布为独立数据集 **wikipedia-labels**，用于识别并剥离诸如 Category/تصنيف/Catégorie 等本地化标签。
- 将单语言原型泛化为面向所有语言版本的参数化流水线，定期从 Wikimedia 月度 dump 下载、解析、清洗并发布数据集。
- 为解决资源瓶颈，作者加入了断点续传、内存监控调度和更动态的并行控制，以避免复杂模板处理阶段引发的内存爆炸与 swap/磁盘崩溃。
- 发布时还提供 **10k / 5k / 1k** 文章子集，降低用户在下载和处理语料时的存储与内存门槛。

## Results
- 最终数据集 **omarkamali/wikipedia-monthly** 实现**每月更新**，覆盖 **340+** 个 Wikipedia 语言版本。
- 相比原先流程，处理时间从 **12–14 天** 缩短到作者笔记本上的 **3 天**，在服务器上可做到 **<24 小时**。
- 最新版本基于 **2026** 年快照，比多数研究者默认使用的官方 HuggingFace Wikipedia 数据集**新 3 年**。
- 数据增量方面：摩洛哥阿拉伯语从 **8,000** 篇提升到 **11,000+**；英语相较官方版本缺失约 **700,000** 篇；阿拉伯语缺失约 **100,000** 篇。
- 整体上，语料规模相对官方版本的**中位增长为 6.8%**，部分语言增长更高；另有 **31** 种语言是在 2023 年后才加入 Wikipedia，因此此前官方语料中**完全没有文本语料**。
- 文章还给出采用与影响的具体信号：例如 **Nous Research** 用其训练 **Hermes 4**，并已有来自 **INRIA HAL lab** 等论文引用；但没有提供标准 NLP 基准上的模型精度对比。

## Link
- [https://omarkamali.com/blog/wikipedia-monthly-pipeline](https://omarkamali.com/blog/wikipedia-monthly-pipeline)
