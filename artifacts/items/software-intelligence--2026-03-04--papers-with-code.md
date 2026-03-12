---
source: hn
url: https://papers.app.nz
published_at: '2026-03-04T23:05:00'
authors:
- horsebatterysta
topics:
- scientific-search
- paper-code-linking
- semantic-search
- research-discovery
- benchmark-tracking
relevance_score: 0.46
run_id: materialize-outputs
---

# Papers with Code

## Summary
这不是一篇研究论文正文，而更像是 **Papers with Code** 的站点简介。它介绍了一个将论文、代码、方法和数据集统一索引并支持语义搜索的科研发现平台。

## Problem
- 研究人员很难高效地在海量论文中同时找到**论文、可复现代码、方法和数据集**之间的对应关系。
- 如果缺少统一检索入口，模型比较、基准跟踪和实验复现都会变得低效。
- 这件事重要，因为科研与工程落地都依赖快速发现可用方法与实现。

## Approach
- 构建一个聚合平台，统一收录论文、代码仓库、方法和数据集。
- 提供**语义搜索**能力，文本中说明其由 **gobed** 驱动，以提升检索相关性。
- 通过结构化目录把研究对象分成多个实体类型，如 papers、code repos、methods、datasets。
- 展示 recent evals，暗示平台还支持结果/评测信息的浏览与追踪。

## Results
- 文本给出的最具体结果是平台规模：**577K papers**。
- 收录 **600K code repos**。
- 收录 **9K methods**。
- 收录 **15K datasets**。
- 未提供论文式实验指标，**没有给出**检索精度、召回率、速度或相对基线比较结果。

## Link
- [https://papers.app.nz](https://papers.app.nz)
