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
- source-code-stylometry
- behavioral-biometrics
- systematic-survey
- software-forensics
relevance_score: 0.68
run_id: materialize-outputs
---

# Bridging Behavioral Biometrics and Source Code Stylometry: A Survey of Programmer Attribution

## Summary
这篇论文是一项关于程序员归属识别（programmer attribution）的系统性映射综述，梳理了2012-2025年间基于源代码风格与行为特征识别作者的研究。它的主要贡献是给出统一分类框架，指出当前领域在行为信号、作者验证和可复现性方面仍存在明显空白。

## Problem
- 论文要解决的问题是：如何系统整理“通过源代码及相关行为特征识别程序作者”的研究现状，并澄清不同特征、模型、数据集和评测方式之间的关系。
- 这很重要，因为程序员归属可用于软件取证、抄袭检测、教育分析、开发者画像与招聘等场景，但现有研究分散在软件工程、安全和数字取证等领域，方法和术语不统一。
- 作者特别指出，现有工作大多只看静态代码风格，较少研究编程行为信号，导致领域全貌和方法学缺口尚不清晰。

## Approach
- 核心方法是**系统性映射研究**：不是提出一个新的识别模型，而是按照预定义流程检索、筛选、编码并比较已有论文。
- 作者从 **135** 篇候选文献出发，通过结构化筛选最终纳入 **47** 篇、发表于 **2012-2025** 年的研究。
- 分析维度包括：作者归属任务（attribution / verification）、特征类型（风格、行为、混合）、学习模型、数据集来源、预处理流程和评估方法。
- 在最简单层面上，这篇论文做的事就是：把过去研究按“用了什么信号、配了什么模型、在哪些数据上测、怎么评估”整理成一个统一 taxonomy，并总结趋势与缺口。
- 研究还结合内容层面的主题分析，归纳该领域的主要研究簇，并公开了提取属性与统计脚本的可复现资源（Zenodo 链接给出）。

## Results
- 文献覆盖方面：从 **135** 篇候选文献中筛出 **47** 篇实证研究，时间范围为 **2012-2025**。
- 论文的核心发现之一是：现有研究**强烈偏向 closed-world authorship attribution**，而不是更困难也更贴近现实的 authorship verification/open-world 设置。
- 特征使用方面：综述称该领域**主要集中于 stylometric features**（词法、句法、结构等静态代码风格特征），而**behavioral signals** 研究明显不足。
- 数据与评测方面：作者指出研究**严重依赖少数 benchmark datasets**，并且**reproducibility 仍较弱**；这意味着不同方法之间的比较可能受数据与协议选择影响较大。
- 贡献层面：论文声称提出了一个把**风格特征/行为特征**与**常见机器学习技术**对应起来的统一 taxonomy，并提供了关于发表趋势、基准数据集和编程语言分布的描述性综述。
- 定量性能结果方面：给定摘要与节选**没有提供具体任务性能数字**（如 accuracy/F1 提升、相对某个基线的百分比增益）；最强的可量化结论主要是文献规模与筛选结果（135→47，2012-2025）。

## Link
- [http://arxiv.org/abs/2603.11150v1](http://arxiv.org/abs/2603.11150v1)
