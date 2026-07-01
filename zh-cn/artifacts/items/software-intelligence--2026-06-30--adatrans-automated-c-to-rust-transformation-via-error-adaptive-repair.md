---
source: arxiv
url: https://arxiv.org/abs/2606.31706v1
published_at: '2026-06-30T14:11:54'
authors:
- Xiaofan Liu
- Zecan Li
- Zhuang Zhao
- Ziqi Shuai
- Yanming Yang
- Qi Xin
- Jifeng Xuan
topics:
- c-to-rust
- code-transformation
- llm-code-repair
- compiler-feedback
- rust-ownership
- software-migration
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# AdaTrans: Automated C to Rust Transformation via Error-Adaptive Repair

## Summary
## 摘要
AdaTrans 将自包含 C 文件转换为大多安全的 Rust 代码，方法是用编译器错误和测试失败来指导大语言模型反复修复。它针对所有权和借用错误，这些错误会让直接的 C 到 Rust 转换失败，或退回到使用 unsafe Rust。

## 问题
- C 到 Rust 迁移有实际价值，因为 C 代码常包含内存风险模式，而 Rust 可以在编译时强制执行所有权、借用和生命周期规则。
- 通用大语言模型经常生成无法通过借用检查器的 Rust 代码，改变程序行为，或使用 `unsafe` 块绕过 Rust 的安全检查。
- 现有修复循环常把原始编译器错误直接反馈给模型，没有把错误映射到具体修复动作。

## 方法
- AdaTrans 对具有标准输入/输出行为的文件级自包含 C 模块使用生成-验证-修复循环。
- 验证流水线先运行 `cargo build`，再执行测试，并将 Rust 输出与原始 C 输出进行比较。
- 它的策略驱动 RAG 将编译器错误代码映射到修复模板和 Rust 文档片段，使模型获得有针对性的指导，而不只看到原始诊断信息。
- 它的错误分层转换策略将失败分为语法-链接、内存语义、逻辑行为和模糊回退类别。
- 修复循环会按错误类型调整采样温度：语法修复使用较低温度，所有权修复使用中等温度，行为失败使用较高温度。

## 结果
- 在 104 个 LeetCode Weekly Contest 算法题上，AdaTrans 报告三次独立运行的平均编译通过率为 95.51%，波动为 ±1.11%。
- 在基于模糊测试的测试 oracle 下，它报告平均解题率为 81.09%，波动为 ±3.09%。
- 它报告平均 unsafe 文件率为 1.19%。
- 相比对照中最强的现有 LLM C 到 Rust 工具，它的解题率提高了 59.94 个百分点。
- 论文还报告了零样本 `gpt-4o-mini` 的 pass@100 估计值为 70.58%，该估计基于每题 200 个样本，用作高预算暴力搜索参考。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.31706v1](https://arxiv.org/abs/2606.31706v1)
