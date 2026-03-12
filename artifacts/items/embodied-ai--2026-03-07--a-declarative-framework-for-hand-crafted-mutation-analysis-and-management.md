---
source: arxiv
url: http://arxiv.org/abs/2603.07065v1
published_at: '2026-03-07T06:46:16'
authors:
- Alperen Keles
topics:
- mutation-testing
- fuzzing-evaluation
- property-based-testing
- program-analysis
- developer-tools
relevance_score: 0.02
run_id: materialize-outputs
---

# A Declarative Framework for Hand-Crafted Mutation Analysis and Management

## Summary
本文提出一个用于**手工构造变异体**的声明式框架，统一描述、转换和管理多种变异表示，并实现了原型工具 Marauder。核心价值在于减少现有手工变异工具在可读性、可保留性与执行效率之间的割裂权衡。

## Problem
- 现有手工变异分析工具分散，常在**可读性、是否保留变异结构、执行/编译成本**之间被迫取舍。
- 手工变异在 fuzzing 和 property-based testing 评测中越来越重要，因为它们更贴近真实缺陷、可控且可复现。
- 传统注释式方案往往需要**每个变异重新编译**，且有些实现不是 mutation-preserving，激活后会丢失变异边界，影响后续分析与管理。

## Approach
- 将手工变异系统归纳为五类表示：**comment-based、preprocessor-based、patch-based、match-and-replace、in-ast**，并分析各自优缺点。
- 提出一个**mutation algebra**：用 `+` 表示顺序测试、`*` 表示组合激活，支持基于 tag 的展开与高阶组合，方便选择子集或同时测试多个变异。
- 设计一个**共同中间表示**与**无损转换管线**，通过“先提取成统一结构，再渲染到目标表示”的方式实现跨表示转换。
- 针对 in-AST 变异，提出提取与规范化策略：寻找能容纳所有候选变体的**最小语法单元**，从而把原本跨语法边界的变异安全转换为 AST 内嵌形式。
- 实现原型系统 **Marauder**，支持注入、激活、重置、组合、测试和跨表示转换，并提供 CLI 与 VS Code/ETNA 插件接口。

## Results
- 论文的主要突破是**提出统一框架、变异代数和无损转换思路**，并给出可运行原型 Marauder；不是在追求新的测试准确率指标。
- 在 ETNA Rust 工作负载上比较 **comment-based vs. in-AST**：总计 **31** 个变异，comment-based 总时间 **146.07s**，in-AST 总时间 **102.72s**，整体约 **1.42×** 总体加速。
- **BST**：`n=8`，comment-based 总时间 **37.51s**，in-AST **20.40s**；编译加速 **1.84×**，执行减速 **1.30×**。
- **RBT**：`n=13`，comment-based 总时间 **41.39s**，in-AST **22.74s**；编译加速 **1.82×**，执行减速 **1.12×**。
- **STLC**：`n=10`，comment-based 总时间 **67.17s**，in-AST **59.57s**；编译加速 **1.13×**，执行减速 **1.07×**。
- 结论上，作者声称 in-AST 方案在仅带来较小运行时开销（**1.07×–1.30×** slowdown）的同时，能显著降低重复编译开销，从而更高效地进行手工变异实验。

## Link
- [http://arxiv.org/abs/2603.07065v1](http://arxiv.org/abs/2603.07065v1)
