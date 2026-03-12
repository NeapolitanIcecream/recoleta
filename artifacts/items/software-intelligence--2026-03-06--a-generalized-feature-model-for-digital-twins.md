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
- digital-twins
- feature-modeling
- systematic-literature-review
- model-driven-engineering
- design-science-research
relevance_score: 0.18
run_id: materialize-outputs
---

# A Generalized Feature Model for Digital Twins

## Summary
本文提出一个面向数字孪生的广义特征模型（GFM），试图统一描述数字模型、数字影子和数字孪生的必选与可选特征。其意义在于为数字孪生的设计、开发以及验证提供一个跨领域、可复用的结构化基础。

## Problem
- 现有数字孪生研究很多，但缺少一个**通用且系统化**的特征模型，无法清楚区分哪些能力是必需的、哪些是可选的。
- 数字孪生跨制造、车辆、应急等多个领域，术语和能力边界不统一，导致设计决策、能力分级和系统比较都很困难。
- 这很重要，因为如果没有统一特征框架，就难以进行模型驱动开发、成熟度评估、以及后续验证与测试用例推导。

## Approach
- 作者基于**系统性文献映射/综述**，从既有数字孪生文献中抽取问题空间、设计空间以及解决空间中的关键特征。
- 在此基础上构建一个**广义特征模型（GFM）**，统一覆盖三类对象：Digital Model、Digital Shadow、Digital Twin。
- 模型显式区分**必选特征**与**可选特征**；文中指出监测（monitoring）与状态表示（state）属于核心必选能力，而可视化、意图、情境检测、决策支持、行为、仿真、自适应、控制等按能力层级扩展。
- 作者将这些特征与**Wagg 的数字孪生成熟度模型**对齐：从监测/可视化到仿真、学习、自主控制，形成渐进式能力路径。
- 研究方法采用**设计科学研究（DSR）**，并通过三个领域用例（应急、车辆、制造）对模型适用性进行验证。

## Results
- 论文的核心成果是提出了一个**跨六个应用领域文献归纳**得到的数字孪生广义特征模型，但摘要与节选中**没有给出标准实验指标、精度、召回率或性能提升百分比**。
- 文中明确声称该模型可统一分类**Digital Model / Digital Shadow / Digital Twin**，并提升语义清晰度，帮助区分必选与可选特征。
- 该模型与**5级数字孪生成熟度框架**相衔接：从 Level 1 的测量，到 Level 3 的仿真与决策支持，再到 Level 5 的自主控制。
- 有效性验证来自**3个用例**：应急服务、车辆系统、制造领域，作者据此声称模型具有跨领域适用性与实用性。
- 论文还提出较强的工程性主张：GFM 可支持**模型驱动工程（MDE）**中的模型映射，并为**验证与确认（V&V）/测试用例推导**提供基础，但节选未提供量化对比实验。
- 背景中给出市场动机数据：数字孪生市场规模据引文预计将从**2022年的 70 亿美元**增长到**2031年的 1830 亿美元**，用以说明该类系统化工程方法的现实价值。

## Link
- [http://arxiv.org/abs/2603.06308v1](http://arxiv.org/abs/2603.06308v1)
