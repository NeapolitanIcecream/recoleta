---
source: hn
url: https://writings.stephenwolfram.com/2013/06/there-was-a-time-before-mathematica/
published_at: '2026-03-06T23:19:28'
authors:
- masfuerte
topics:
- symbolic-computation
- programming-languages
- mathematica
- computer-algebra
- software-history
relevance_score: 0.02
run_id: materialize-outputs
language_code: zh-CN
---

# There Was a Time before Mathematica (2013)

## Summary
这不是一篇科研论文，而是一篇Stephen Wolfram回顾Mathematica诞生前史的历史性文章，核心讲述其前身SMP的设计、商业化与经验教训。文章的价值主要在于揭示符号计算语言与系统设计理念如何逐步演化为Mathematica。

## Problem
- 早期理论物理与数学计算中存在大量繁琐且易错的代数推导，人工处理会陷入“追负号和系数”的低效工作。
- 当时已有的代数系统（如Reduce、Macsyma等）功能有限、交互性差、难以扩展，无法满足作者对通用高层计算系统的需求。
- 这件事之所以重要，是因为它说明了现代计算数学平台为何需要把**符号、数值、图形、编程与交互**统一在同一个系统里。

## Approach
- 作者先为自己的物理研究需求设计并实现了SMP（Symbolic Manipulation Program），把**符号表达式**作为统一表示。
- SMP/Mathematica的核心机制是：把计算看成对符号表达式应用**模式匹配与变换规则**；简单说，就是“如果一个式子长得像这样，就把它改写成那样”。
- 在此基础上，作者追求“用尽可能少的原语表达尽可能大的能力”，逐步形成了后来Mathematica的语言哲学。
- Mathematica在1986年重新从零设计，吸收SMP经验，保留符号表达式与规则变换的主线，同时扩展到数值计算、图形、接口与更易理解的语言设计。
- 文章还总结了若干失败设计（如符号索引列表、语义模式匹配、过强递归控制、用户自定义语法等），说明Mathematica如何通过删繁就简获得更强可用性。

## Results
- 文章**没有提供标准科研实验、数据集或基准测试上的定量结果**。
- 明确的时间节点包括：SMP于**1980年初**开始写C代码，**1981年6月**运行SMP Version 1；Mathematica首批代码写于**1986年10月**，并于**1988年6月23日**发布1.0。
- 作者称SMP在当时已是“大型软件系统”，其可执行文件“**略低于1 MB**”。
- 文中给出的规模性事实包括：作者自述一度以约“**1000行代码/天**”速度编写SMP；早期ARPANET只有“**256 hosts**”；Mathematica发布时距离写作已过去“**25年**”。
- 文章的最强结论性主张是：Mathematica的基础设计原则经受了长期检验，甚至“**大多数Mathematica 1.0代码今天仍可不改运行**”；同时SMP虽未复用代码，却为Mathematica提供了关键设计先验。

## Link
- [https://writings.stephenwolfram.com/2013/06/there-was-a-time-before-mathematica/](https://writings.stephenwolfram.com/2013/06/there-was-a-time-before-mathematica/)
