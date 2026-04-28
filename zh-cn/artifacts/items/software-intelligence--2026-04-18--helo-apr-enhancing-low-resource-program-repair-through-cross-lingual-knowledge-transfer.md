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
HELO-APR 通过已验证的跨语言数据和分阶段微调，把高资源语言中的修复知识迁移到低资源语言，从而提升低资源语言的自动程序修复能力。论文以 C++ 作为源语言，面向 Ruby 和 Rust 的修复任务，并报告了相对强基线的明显提升。

## 问题
- 基于 LLM 的程序修复在 C++ 这类高资源语言上的效果明显好于 Ruby 和 Rust 这类低资源语言，因为经过验证的 buggy-fixed 训练样本对很少。
- 直接从高资源语言迁移会带来语法干扰：如果模型只在 C++ 上训练，它可能会为 Ruby 生成带有 C++ 风格的补丁，而这些补丁无法通过编译。
- 简单的合成数据流程可能会生成低质量缺陷，或者无法判断某种缺陷在目标语言中是否真的可能存在。

## 方法
- HELO-APR 包含两部分：先从高资源语言样本对构建经过验证的低资源 buggy-fixed 样本对，再用三阶段课程学习进行训练。
- 在数据构建阶段，方法会过滤掉无法迁移的缺陷，把修复后的 C++ 代码翻译成目标语言，同时保留重建缺陷所需的代码结构，并用生成的测试对翻译后的代码进行验证，这些测试必须至少达到 90% 的行覆盖率和分支覆盖率。
- 然后，方法依据原始缺陷类型、根因和补丁注入目标语言中的缺陷，并选择那些在触发缺陷的输入上最接近原始缺陷行为、同时避免额外回归的候选样本。
- 在训练阶段，模型先学习 C++ 上的修复任务，再利用并行的 C++/目标语言 buggy-fixed 样本对学习跨语言对齐，最后适配为直接修复目标语言。骨干模型参数保持冻结，只训练修复适配器。

## 结果
- 在 xCodeEval 上，HELO-APR 将 DeepSeek-Coder-6.7B 的 Pass@1 从 31.32% 提高到 48.65%，相对 zero-shot 基线提升 55.33%。
- 在 xCodeEval 上，HELO-APR 将 CodeLlama-7B 的 Pass@1 从 1.67% 提高到 11.97%，超过 zero-shot 基线的 7 倍。
- 在语法有效性方面，CodeLlama 在目标语言上的平均编译通过率从 49.77% 提高到 91.98%。
- 在 Defects4Ruby 上，HELO-APR 将 CodeLlama-7B 的 BLEU-4 从 61.20 提高到 66.79，将 ROUGE-1 从 76.76 提高到 83.59。
- 论文还报告了数据集构建和课程学习阶段的消融实验，并声称每个核心组件都不可缺少，但给定摘录没有提供消融实验的具体数值。
- 训练数据使用了 xCodeEval 中 10,000 个 C++ buggy-fixed 样本对，用来为 Ruby 和 Rust 合成目标语言修复数据。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.17016v1](http://arxiv.org/abs/2604.17016v1)
