---
source: arxiv
url: https://arxiv.org/abs/2606.30610v1
published_at: '2026-06-29T17:45:36'
authors:
- Chuyue Li
- Ziqi Tang
- Jingyi Wang
- Yu Wu
- Kazuma Hashimoto
- Lingyu Gao
topics:
- code-intelligence
- software-foundation-models
- code-error-classification
- programming-education
- llm-benchmarking
relevance_score: 0.76
run_id: materialize-outputs
language_code: zh-CN
---

# PyMETA: A Benchmark Dataset for Hierarchical Student Code Error Classification with Python-Interpreter-Based Labels

## Summary
## 摘要
PyMETA 是一个 Python 学生代码错误分类基准，包含 48,646 份提交和由解释器生成的标签。它在三级错误分类体系上测试微调代码模型和提示式 LLM，并包含一个小规模专家标注的多错误子集。

## 问题
- 教育调试工具需要与 Python 执行行为一致的错误标签，但公开数据集通常规模小、范围窄，且分类体系不一致。
- 单一运行时标签可能掩盖同时存在的多个错误，降低反馈质量和模型评估效果。
- 在低资源或免训练设置下，提示式 LLM 需要一个共享基准来诊断学生代码。

## 方法
- 作者从 Circle Cat 平台上 579 名用户、155 道题的 Moodle CodeRunner 输出中收集了 48,646 份 Python 提交。
- 他们根据在线评测执行结果和 Python 异常类型生成单错误标签；能运行但未通过测试的代码被标为 Logic Error。
- 他们将标签组织为三个任务：二分类 Error/No Error，三分类 No Error/Explicit Error/Logic Error，以及 14 类细粒度分类体系。
- 他们对 97 个可能包含多错误的样本进行专家标注，这些样本来自 CodeBERT 误分类和高熵预测，平均每个样本有 1.91 种错误类型。
- 他们评估了微调后的 CodeBERT 和 CodeLlama-7B，以及提示式 GPT-3.5、GPT-4o、Gemini 2.5 Pro 和 DeepSeek-V3。

## 结果
- PyMETA 包含 48,646 份提交：23,207 个 No Error、11,387 个 Logic Error、5,618 个 Syntax Error、2,565 个 Name Error、2,074 个 Type Error；合并稀有标签后，另外 9 个类别的数量更少。
- 在按题目划分的测试集上，CodeLlama-7B 在二分类中达到 96.3% macro F1，在三分类中达到 93.5% macro F1，在 14 类分类中达到 80.6% macro F1。
- CodeBERT 在细粒度任务上弱得多，在 Task C 上的 macro F1 为 45.2%，weighted F1 为 71.0%。
- 在单错误提示中，Gemini 2.5 Pro 是表现最好的提示式模型，accuracy 为 85.9%，macro F1 为 71.9%；GPT-4o 的 macro F1 为 28.0%，DeepSeek-V3 为 29.1%，GPT-3.5 为 8.8%。
- 提示式 LLM 会过度预测 Logic Error：报告的 Logic Error Overprediction Rate 从 Gemini 2.5 Pro 的 17.6% 到 GPT-3.5 的 92.8% 不等。
- 在多错误提示中，Gemini 2.5 Pro 在 97 个样本的专家子集上按 contains 判据达到 81.8% macro F1。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.30610v1](https://arxiv.org/abs/2606.30610v1)
