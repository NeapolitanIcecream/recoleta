---
source: hn
url: https://writings.stephenwolfram.com/2013/06/there-was-a-time-before-mathematica/
published_at: '2026-03-06T23:19:28'
authors:
- masfuerte
topics:
- symbolic-computation
- programming-language-design
- computer-algebra
- mathematica-history
- software-systems
relevance_score: 0.44
run_id: materialize-outputs
language_code: zh-CN
---

# There Was a Time before Mathematica (2013)

## Summary
这是一篇回顾性文章，讲述 Mathematica 诞生前的前身系统 SMP 的设计、实现与商业化历程，以及这些经验如何塑造了 Mathematica。它的重要性在于揭示了现代符号计算与计算语言设计的一套核心思想是如何逐步形成并被验证的。

## Problem
- 要解决的是**如何让计算机可靠地处理大规模符号数学与通用计算**，避免研究者在复杂代数推导中反复“追 minus sign 和系数”。
- 当时已有的系统（如 Reduce、Macsyma、Schoonschip）要么过于专用、要么交互性差、要么在规模与表达能力上碰到边界，难以支持更广泛的科学计算与程序构造。
- 这件事重要，因为理论物理、工程和科研需要的不只是数值计算，还需要可交互、可编程、可扩展的符号计算环境；作者进一步认为，这类环境还能成为长期的科学研究与技术产品基础。

## Approach
- 核心机制是把**计算统一表示为符号表达式上的变换**：用户写出长得像某种形式的表达式，系统用模式和规则把它改写成另一种形式。
- 作者先构建了前身系统 **SMP (Symbolic Manipulation Program)**，以此探索语言设计，包括模式匹配、规则替换、列表/函数表示、代码生成、并行处理等能力。
- 在 Mathematica 设计中，保留了 SMP 中被验证有效的主线：**symbolic expressions + transformation rules**，同时去掉了难以理解或不实用的设计，如“chameleonic symbols”、过度统一的符号索引列表、过强的语义匹配、复杂递归控制和用户自定义语法陷阱。
- 方法论上，作者强调**从语言原语层做最小而强大的抽象**，并通过边设计边写文档来逼迫接口与语义保持清晰。
- 从工程实现看，SMP 于 1980 年开始用 C 实现，Mathematica 于 1986 年重新从零开始，以覆盖代数、数值、图形、编程与界面等更广范围，而非只做代数系统。

## Results
- 文中**没有给出标准学术实验或基准测试的定量结果**，因此不存在精确的 metric/dataset/baseline 比较数字。
- 文章给出的最强具体结果是时间线与系统里程碑：SMP 于 **1980 年**开始编码，**1981 年 6 月**运行 Version 1；Mathematica 首批代码写于 **1986 年 10 月**，**1988 年 6 月 23 日**正式发布 1.0。
- 作者声称其设计原则具有很强持久性：到文章写作时 Mathematica 已有 **25 年**发展，而“**大多数 Mathematica 1.0 代码今天仍可不变运行**”。
- SMP 在当时已是“大型软件系统”，但可执行文件仍**不到 1 MB**；作者自述在开发中曾达到约 **1000 行代码/天** 的编写速度。
- 商业与平台方面，Mathematica 发布前已获得多家厂商合作，首先是 **NeXT**，随后包括 **Sun、Silicon Graphics、IBM** 等；作者将此作为系统市场可行性与影响力的证据。
- 文章的核心突破主张不是单点性能提升，而是：通过前身系统 SMP 的试错，最终确立了 Mathematica 的通用计算范式，使其能长期支撑后续产品与研究（包括作者提到的 **A New Kind of Science** 与 **Wolfram|Alpha**）。

## Link
- [https://writings.stephenwolfram.com/2013/06/there-was-a-time-before-mathematica/](https://writings.stephenwolfram.com/2013/06/there-was-a-time-before-mathematica/)
