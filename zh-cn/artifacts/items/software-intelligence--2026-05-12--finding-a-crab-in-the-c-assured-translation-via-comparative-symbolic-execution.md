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
cozy 检查一个 C 二进制和一个 Rust 二进制在已探索的符号路径上是否表现一致，然后把剩下的差异展示给开发者。论文把这个现有工具用于 C 到 Rust 的翻译保证，包括手写 Rust 移植和 C2Rust 输出。

## 问题
- 旧的 C 和 C++ 代码有内存安全风险，但把整个代码库重写成 Rust 代价太高，也有风险。
- 手工移植、转换器和基于 ML 的翻译器会改变程序行为；有些改动修复了 bug，有些会引入错误。
- 开发者需要路径级别的语义差异证据，而不只是一个通过/失败的等价结果。

## 方法
- cozy 把两个程序都编译成二进制，然后用相同的符号输入在 angr 中运行。
- 只有当终止状态的路径约束可以同时满足时，它才比较这些状态，这意味着某个具体输入可以到达这两个状态。
- 它用 Z3 证明选定的输出、内存位置和其他状态元素相等，或者生成能暴露差异的具体输入。
- 它缓存不可满足核心，避免在朴素的 n^2 终止状态兼容性检查中重复调用 SMT。
- 它用注解和 Rust 互操作选项，例如 repr(C)、extern "C" 和 DWARF 布局数据，对齐 C 和 Rust 的数据位置。

## 结果
- 作者报告了 3 个 C/Rust 比较实验：插入排序、日期时间手表更新函数和 box blur 图像滤波器。
- 在插入排序实验中，cozy 验证了手写 C、手写 Rust 和 C2Rust 版本之间的等价性；它还验证了在有界输入长度下，C 插入排序和 Rust 冒泡排序的排序输出等价。
- 在手表实验中，C 和 Rust 先因为溢出语义出现分歧；在加入合理的年份范围等输入边界后，Z3 证明了输出相等。
- 在 box blur 实验中，cozy 验证了小尺寸图像和核大小下的等价输出，包括通过 array2d crate 建模的 Rust 数据。
- GUI 包含 3 种聚焦机制：高亮、剪枝和压缩；压缩有 2 个级别。
- 论文没有给出时间、内存、基准规模或求解器查询减少的数值，所以最明确的结果是这 3 个从玩具到小规模实验中的功能验证，而不是测得的可扩展性提升。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.12731v1](https://arxiv.org/abs/2605.12731v1)
