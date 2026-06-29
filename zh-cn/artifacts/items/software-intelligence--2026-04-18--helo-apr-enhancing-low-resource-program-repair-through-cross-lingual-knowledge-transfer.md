---
source: arxiv
url: http://arxiv.org/abs/2604.17016v1
published_at: '2026-04-18T14:55:11'
authors:
- Zhipeng Wang
- Boyang Yang
- Yidong Wan
- Liuye Guo
- You Lv
- Tao Zheng
- Zhuowei Wang
- Tieke He
topics:
- automatic-program-repair
- cross-lingual-transfer
- code-llms
- low-resource-languages
- software-engineering
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# HELO-APR: Enhancing Low-Resource Program Repair through Cross-Lingual Knowledge Transfer

## Summary
## 摘要
HELO-APR 通过经过验证的跨语言数据和分阶段微调，把修复知识从高资源语言迁移到低资源语言，从而提升低资源语言的自动程序修复效果。论文以 C++ 作为源语言，面向 Ruby 和 Rust 修复，报告了相对强基线的明显提升。

## 问题
- 基于 LLM 的程序修复在 C++ 这类高资源语言上的效果远好于 Ruby 和 Rust 这类低资源语言，因为经过验证的 buggy-fixed 训练对太少。
- 从高资源语言直接迁移会带来语法干扰：只用 C++ 训练的模型可能为 Ruby 生成 C++ 风格补丁，这些补丁无法编译。
- 朴素的合成数据流程可能生成质量较差的 bug，或者无法判断某个缺陷是否真的能在目标语言中出现。

## 方法
- HELO-APR 分两部分：先从高资源语言对构建经过验证的低资源 buggy-fixed 对，再用三阶段课程学习进行训练。
- 在数据构建阶段，它先过滤掉不可迁移的缺陷，再把修复后的 C++ 代码翻译成目标语言，同时保留重现 bug 所需的代码结构，并用生成测试验证译文，测试必须达到至少 90% 的行覆盖率和分支覆盖率。
- 随后，它根据原始缺陷类型、根因和补丁注入目标语言 bug，再挑选与原始 bug 在触发输入上的行为最接近、且不会引入额外回归的候选样本。
- 在训练阶段，模型先学习 C++ 修复，再用平行的 C++/目标语言 buggy-fixed 对学习跨语言对齐，最后适应目标语言中的直接修复。主干模型被冻结，只调整修复适配器。

## 结果
- 在 xCodeEval 上，HELO-APR 将 DeepSeek-Coder-6.7B 的 Pass@1 从 31.32% 提升到 48.65%，相对零样本基线提升 55.33%。
- 在 xCodeEval 上，HELO-APR 将 CodeLlama-7B 的 Pass@1 从 1.67% 提升到 11.97%，是零样本基线的 7 倍多。
- 在语法有效性方面，CodeLlama 的目标编译率平均值从 49.77% 提升到 91.98%。
- 在 Defects4Ruby 上，HELO-APR 将 CodeLlama-7B 的 BLEU-4 从 61.20 提升到 66.79，将 ROUGE-1 从 76.76 提升到 83.59。
- 论文还报告了数据集构建和课程阶段的消融研究，并给出“每个核心组件都必要”的结论，但摘要片段没有提供消融数值。
- 训练数据使用 xCodeEval 中的 10,000 对 C++ buggy-fixed 样本，合成 Ruby 和 Rust 的目标语言修复数据。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.17016v1](http://arxiv.org/abs/2604.17016v1)
