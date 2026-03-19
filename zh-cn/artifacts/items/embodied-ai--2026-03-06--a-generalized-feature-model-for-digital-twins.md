---
source: arxiv
url: http://arxiv.org/abs/2603.06308v1
published_at: '2026-03-06T14:12:32'
authors:
- Philipp Zech
- Yanis Mair
- Michael Vierhauser
- Pablo Oliveira Antonino
- Frank Schnicke
- Tony Clark
topics:
- digital-twin
- feature-model
- systematic-literature-review
- model-driven-engineering
- design-science-research
relevance_score: 0.16
run_id: materialize-outputs
language_code: zh-CN
---

# A Generalized Feature Model for Digital Twins

## Summary
本文提出一个面向数字孪生的通用特征模型（GFM），试图统一描述数字模型、数字影子和数字孪生的必选与可选特征。其价值在于为数字孪生的设计、开发以及验证提供更清晰的结构化依据，但论文摘录中主要给出方法与概念框架，量化结果有限。

## Problem
- 论文要解决的问题是：目前数字孪生领域缺少一个**跨领域、系统化**的通用特征模型，无法清楚区分哪些能力是必需的、哪些是可选的。
- 这很重要，因为数字孪生已扩展到制造、车辆、应急、医疗等多个场景；没有统一特征框架，设计决策、能力分级、开发路线和测试验证都会缺乏依据。
- 作者还指出现有研究对数字模型（DM）、数字影子（DS）和数字孪生（DT）的边界不清，影响术语一致性与成熟度评估。

## Approach
- 核心方法很简单：作者先做**系统性文献映射/文献综述**，从已有数字孪生研究中抽取共同特征，再整理成一个通用特征模型。
- 该模型把数字系统分成 **Digital Model、Digital Shadow、Digital Twin**，并区分**mandatory** 与 **optional** 特征，形成结构化分类。
- 模型覆盖从低到高的能力链条，包括监测、状态表示、可视化、目标、情境检测、决策支持、行为、仿真、自适应和控制。
- 作者将这些概念与 **Wagg 的数字孪生成熟度模型（Level 1–5）** 对齐，用来说明不同特征如何支撑从监控到自主控制的渐进能力。
- 方法论上采用 **Design Science Research (DSR)**，并声称该特征模型可支持模型驱动工程（MDE），帮助推导开发路线和测试用例。

## Results
- 论文的主要成果是提出了一个**广义特征模型（GFM）**，并声明它来源于覆盖**6个应用领域**的系统文献分析。
- 论文摘录未提供常见机器学习式的定量指标结果（如准确率、F1、提升百分比等），因此**没有可报告的标准量化性能数字**。
- 文中给出的最具体验证主张是：该模型被应用到**3个用例/领域**进行有效性检查，分别来自**应急、车辆、制造**领域，用于展示可适用性与实用性。
- 作者声称该模型能够更清晰地区分 **DM / DS / DT** 三类系统，并把特征与 **Level 1–5 成熟度**对应起来，支持从“监测/可视化”到“仿真/自适应/自主控制”的能力演进。
- 论文还给出一个市场背景数字：数字孪生市场规模据引文从 **2022 年 70 亿美元** 预计增长到 **2031 年 1830 亿美元**，用来说明建立系统化工程方法的现实意义，但这不是模型本身的实验结果。

## Link
- [http://arxiv.org/abs/2603.06308v1](http://arxiv.org/abs/2603.06308v1)
