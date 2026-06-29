---
source: arxiv
url: https://arxiv.org/abs/2605.17957v1
published_at: '2026-05-18T07:12:14'
authors:
- Chen Liu
- Qingyuan Liang
- Hanwen Zhang
- Zeyu Sun
- Yakun Zhang
- Lu Zhang
topics:
- code-generation
- code-pretraining
- caller-context
- repository-level-code
- static-analysis
- code-benchmarks
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Contextualized Code Pretraining for Code Generation

## Summary
## 摘要
CallerGen 训练代码模型在生成缺失的 Python 函数时使用已经调用它们的调用方代码。论文认为，这种以调用方为条件的预训练能提高真实仓库生成任务的 pass@1，尤其对小模型更明显。

## 问题
- 在真实项目里，常常需要在调用方代码已经存在后再补实现一个缺失函数，因此调用点可以提供预期输入、返回形状、错误处理和副作用信息。
- 常见代码模型主要用代码或自然语言描述进行训练，函数签名信息不足时，可能会忽略调用方的用法。
- 基于检索的仓库方法在找不到相似示例或检索不到时会失效，这在新模块、小仓库和早期代码阶段都很常见。

## 方法
- 该方法用基于 AST 的静态分析、符号表、导入别名解析和函数级调用图，从 800 个 Python GitHub 仓库中抽取 caller-callee 对。
- 每个训练样本把一个目标 callee 与其直接调用方函数体和可选的 docstring 配对，然后让模型生成缺失的 callee 实现。
- CallerGen 在 60M、220M 和 0.5B 参数规模上用 invocation-aware 目标进行训练。
- 论文把这个思路同时用于 encoder-decoder 的 CodeT5 风格模型和 decoder-only 的 Qwen2.5-Coder 风格模型。
- 论文引入 CallerEval，作为一个包含真实 caller-callee 案例的基准，并用与调用方约束行为相关的执行测试进行评估。

## 结果
- 在 CallerEval 上，CallerGen-220M 达到 16.58% pass@1，CallerGen-0.5B 达到 22.81% pass@1。
- 在带调用上下文的 CoderEval 上，CallerGen-220M 的 pass@1 为 21.22%，而 CodeGen-350M 为 8.78%。
- CallerGen-0.5B 在 CallerEval 上达到 22.81% pass@1，论文报告它比 Qwen2.5-Coder-32B-Instruct 高近 2 个百分点。
- 没有调用上下文时，CallerGen-220M 在 CoderEval 上仅用函数头生成时达到 10.00% pass@1，而 CodeGen-350M 为 7.39%。
- 评估将 CallerGen 与 9 个开源代码模型在 CoderEval 和 CallerEval 上进行比较。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.17957v1](https://arxiv.org/abs/2605.17957v1)
