---
source: arxiv
url: http://arxiv.org/abs/2603.09467v1
published_at: '2026-03-10T10:20:02'
authors:
- Oleksandr Kosenkov
- Konstantin Blaschke
- Tony Gorschek
- Michael Unterkalmsteiner
- Oleksandr Adamov
- Davide Fucci
topics:
- requirements-engineering
- software-engineering-education
- professional-curriculum
- curriculum-alignment
- learning-path-design
relevance_score: 0.18
run_id: materialize-outputs
language_code: zh-CN
---

# Experience Report on the Adaptable Integration of Requirements Engineering Courses into Curricula for Professionals

## Summary
本文是一篇经验报告，讨论如何把需求工程课程更灵活地嵌入面向在职专业人士的软件工程课程体系中。作者基于三个真实项目，总结了此类课程体系的特点，并提出了一种轻量级、以内容项映射为核心的集成方法。

## Problem
- 论文要解决的问题是：如何在面向专业人士的动态、模块化软件工程课程体系中，系统而有效地整合需求工程（RE）课程。
- 这很重要，因为传统大学课程常把RE作为“事后补充”，更强调知识广度而非深度和行业就绪能力，导致教学内容与产业需求之间长期存在落差。
- 面向专业人士的课程体系（CfP）比传统学历课程更动态、更松耦合、教师自主性更高，缺少适合持续对齐和协同开发的框架。

## Approach
- 作者基于三个案例（PROMIS、Software4KMU、TASTE）提炼出CfP的关键特征：高模块化、高动态性、实践导向、较少前置集中式对齐、教师自主性强，以及更适合按学习路径而非全局统一课程结构来组织。
- 核心方法是**基于内容项（content items, CI）的课程对齐**：把课程拆成约10–15分钟的细粒度内容单元，每个单元记录标题和涵盖的主题/概念。
- 然后由RE课程教师与相关课程教师协作，找出不同课程内容项之间的交集、依赖与合适顺序，把它们重新编排成统一序列。
- 在统一序列基础上，进一步形成模块和学习路径，再补充教学材料，并据此制定或校验学习目标。
- 简单说，这个机制就是：**先把多门课拆成小知识块，再像拼图一样把相关知识块重新排顺序，形成更贴近职业角色和实践需求的学习路径**。

## Results
- 作者声称该方法在 **3 个项目/案例** 中都成功支持了RE课程集成：PROMIS、Software4KMU、TASTE。
- 在 **PROMIS** 中，按该方法初版开发的RE课程已教学 **3年**，并获得学生**正面反馈**；但文中未给出量化评分、样本量或与基线课程的对比数据。
- 在 **TASTE** 中，作者构建了一个包含 **35 个内容项（CIs）** 的学习路径：RE课程 **11个CI**（**4个必修 + 7个可选**）、MBSE课程 **13个CI**（**7个必修 + 6个可选**）、QA课程 **11个CI**（**8个必修 + 3个可选**）。
- 该TASTE学习路径包含 **3个必修模块** 和 **5个可选模块**；其中 **2个必修模块** 混合了三门课程内容，**1个必修模块** 来自单一课程。
- 在 TASTE 中，学习路径迭代到了 **4 个版本**，说明该方法支持渐进式、协同式调整。
- 论文**没有提供严格的定量效果评测**（如学习成绩提升、完成率提升、与其他课程设计方法的实验对比）；最强的具体证据主要是跨案例可落地实施、长期教学使用，以及项目经理和学生的正向主观反馈。

## Link
- [http://arxiv.org/abs/2603.09467v1](http://arxiv.org/abs/2603.09467v1)
