---
source: arxiv
url: http://arxiv.org/abs/2603.11150v1
published_at: '2026-03-11T17:45:06'
authors:
- Marek Horvath
- Emilia Pietrikova
- Diomidis Spinellis
topics:
- programmer-attribution
- code-stylometry
- behavioral-biometrics
- systematic-survey
- software-forensics
relevance_score: 0.02
run_id: materialize-outputs
language_code: zh-CN
---

# Bridging Behavioral Biometrics and Source Code Stylometry: A Survey of Programmer Attribution

## Summary
这是一篇关于程序员归因（programmer attribution）的系统性映射综述，梳理了2012到2025年间基于源代码风格与行为特征识别作者的研究。论文的核心贡献不是提出新模型，而是统一整理任务、特征、模型、数据集与评测实践，并指出该领域的主要空白。

## Problem
- 要解决的问题是：如何根据源代码制品中的**风格、结构或行为特征**识别或验证程序员身份，以及现有研究到底用了哪些特征、模型、数据和评测方式。
- 这很重要，因为程序员归因涉及**软件取证、抄袭检测、教育分析、开发者画像与安全场景**，但现有研究分散在多个社区，方法口径不统一。
- 论文指出该领域当前存在明显失衡：研究**过度集中于封闭世界作者归因与静态代码风格特征**，而**行为信号、作者验证、可复现性**探索不足。

## Approach
- 采用**systematic mapping study**方法，对程序员归因文献进行系统筛选与分类，而不是训练新的归因模型。
- 检索范围覆盖**2012–2025**，使用三类关键词组合：作者任务、源代码对象、分析方法，并在**IEEE Xplore、ACM DL、Scopus**中检索，再辅以**Google Scholar**滚雪球。
- 从**135**篇候选论文中，经纳入/排除标准筛选，最终保留**47**篇实证研究进行分析。
- 按多个维度建立统一分类框架：**作者任务（attribution/verification）**、**特征类型（stylistic/behavioral/hybrid）**、**学习模型**、**数据集来源**、**评测方法**。
- 提出一个**taxonomy**，把**风格特征与行为特征**同常见机器学习技术对应起来，并补充发表趋势、基准数据集、编程语言和主题聚类的描述性分析。

## Results
- 论文的主要“结果”是综述性发现，而非新的模型性能提升；文中给出的核心数量包括：从**135**篇候选出版物中筛选出**47**篇研究，时间跨度为**2012–2025**。
- 研究发现该领域**强烈偏向 closed-world authorship attribution**，说明大多数工作假设作者集合已知，而不是更贴近现实的开放环境或验证任务。
- 特征层面，现有文献主要依赖**stylometric features**（如词法、句法、结构特征）；相较之下，**behavioral signals** 的研究明显较少。
- 数据层面，论文指出研究**严重依赖少数几个 benchmark datasets**，意味着结论可能受限于数据分布，跨数据集泛化与生态覆盖不足。
- 方法学层面，作者明确指出**reproducibility remain less explored**，即许多研究在数据、预处理和评测协议上缺乏足够可复现性。
- 摘要与节选中**没有提供具体的准确率/F1/Top-k等跨论文汇总数值**；最强的具体主张是：该综述给出了一个统一框架与分类法，并系统识别出行为特征、作者验证、数据与评测规范化方面的研究空白。

## Link
- [http://arxiv.org/abs/2603.11150v1](http://arxiv.org/abs/2603.11150v1)
