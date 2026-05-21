---
source: arxiv
url: https://arxiv.org/abs/2605.12731v1
published_at: '2026-05-12T20:33:33'
authors:
- Caleb Helbling
- Graham Leach-Krouse
- Michael Crystal
topics:
- code-translation
- symbolic-execution
- program-equivalence
- rust-migration
- software-assurance
relevance_score: 0.76
run_id: materialize-outputs
language_code: zh-CN
---

# Finding a Crab in the C: Assured Translation via Comparative Symbolic Execution

## Summary
## 摘要
cozy 检查一个 C 二进制文件和一个 Rust 二进制文件在已探索的符号路径上是否行为相同，然后向开发者展示剩余差异。论文将这个已有工具用于 C 到 Rust 翻译保障，包括手写 Rust 移植版本和 C2Rust 输出。

## 问题
- 遗留 C 和 C++ 代码有内存安全风险，但把整个代码库改写成 Rust 的成本和风险可能过高。
- 手工移植、转译器和基于机器学习的翻译器都可能改变程序行为；有些改动会修复 bug，有些会引入错误。
- 开发者需要关于语义差异的路径级证据，不能只依赖通过/失败式的等价性结果。

## 方法
- cozy 将两个程序都编译成二进制文件，并在 angr 中用相同的符号输入运行它们。
- 它只在两个终止状态的路径约束可联合满足时比较这些状态，也就是存在一个具体输入可以到达两个状态。
- 它使用 Z3 证明选定的输出、内存位置和其他状态元素相等，或生成能暴露差异的具体输入。
- 它缓存 unsat core，以避免在朴素的 n^2 终止状态兼容性检查中反复调用 SMT。
- 它使用注解，以及 repr(C)、extern "C" 和 DWARF 布局数据等 Rust 互操作选择，来对齐 C 和 Rust 的数据位置。

## 结果
- 作者报告了 3 个 C/Rust 对比实验：插入排序、datetime 手表更新函数，以及 box blur 图像滤波器。
- 在插入排序实验中，cozy 验证了手写 C、手写 Rust 和 C2Rust 版本之间的等价性；它还在有界输入长度下验证了 C 插入排序和 Rust 冒泡排序的排序输出等价。
- 在手表实验中，C 和 Rust 起初因溢出语义而出现分歧；加入合理年份范围等输入边界后，Z3 证明了输出相等。
- 在 box-blur 实验中，cozy 验证了小图像和小核尺寸下的输出等价，包括通过 array2d crate 建模的 Rust 数据。
- GUI 包含 3 种聚焦机制：高亮、剪枝和压缩；压缩有 2 个级别。
- 论文没有给出时间、内存、基准规模或 solver 查询减少量等数字，所以最强的具体结果是在 3 个玩具到小规模实验上的功能验证，而非经过测量的可扩展性提升。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.12731v1](https://arxiv.org/abs/2605.12731v1)
