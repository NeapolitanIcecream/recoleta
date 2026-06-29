---
source: arxiv
url: https://arxiv.org/abs/2605.29490v1
published_at: '2026-05-28T07:17:53'
authors:
- Puzhuo Liu
- Yuhan Huang
- Jianlei Chi
- Peng Di
- Yu Jiang
topics:
- binary-decompilation
- code-intelligence
- llm-evaluation
- automated-repair
- software-security
- program-analysis
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# CODEFUSE-DEBENCH: An Empirical Study on Readability, Recompilability, and Functionality

## Summary
## 总结
CODEFUSE-DeBench 通过判断二进制反编译结果是否可读、能否在有限修复后重新编译，以及是否保持与原始二进制一致的行为，来评估反编译器。研究发现，能编译通过的代码和能保留行为的代码之间差距很大。

## 问题
- 二进制反编译器常用表面指标来评估，例如行数、字符匹配或可读性评分，但这些指标看不出恢复出的代码是否可复用。
- 这对逆向工程、安全分析、自动补丁、跨架构迁移，以及在缺少或不可靠源代码时对二进制做静态分析都很重要。
- 可读的反编译代码仍然可能是错的，难看的代码也可能保留行为，因此单一指标对用户的工具选择帮助很小。

## 方法
- DeBench 使用 240 个原子测试函数，覆盖 8 个源代码维度，并编译成 640 个二进制文件，涉及编译器、优化级别、调试符号设置、架构和相关构建选项。
- 它评估 5 个整程序反编译器：IDA、Ghidra、RetDec、Angr 和 BinaryAI。
- 可读性使用 URAF 评分，这是一个由 LLM 评判的量表，包含 18 个子维度，覆盖命名、结构、类型、语义清晰度和上下文。
- 可重新编译性通过迭代式编译与修复来测量，在固定的 50 次迭代预算下使用 3 个独立的修复 LLM。
- 功能性通过基于 Frida 的差分动态跟踪来检查，粒度包括程序、函数和指令级。

## 结果
- 最好的反编译器加修复 LLM 组合在程序级行为重叠上达到 22.3% 的 Exact+Partial，但精确 stdout 匹配只有 1.2%。
- 论文报告从可重新编译性到功能等价性大约下降 50 个百分点，说明编译成功往往并不保留运行时行为。
- 优化和编译器选择会改变结果：O3 的可读性最低，但功能性最高；Clang 的可读性低于 GCC，但功能性是 GCC 的 2.6 倍。
- 反编译器选择比修复 LLM 选择更重要：跨反编译器的功能性波动是 20 倍，而跨 LLM 的波动是 1.6 倍。
- 失败分析发现，语法噪声通常可以通过修复处理；类型系统崩溃约占所有修复错误的 19%；上游损失，例如 ARM64 重定位习惯用法和 C++ ABI 特性，修复 LLM 无法恢复。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.29490v1](https://arxiv.org/abs/2605.29490v1)
