---
source: arxiv
url: https://arxiv.org/abs/2606.09395v1
published_at: '2026-06-08T12:13:58'
authors:
- Yewei Song
- Prateek Rajput
- Tiezhu Sun
- Saad Ezzini
- "Tegawend\xE9 F. Bissyand\xE9"
- Jacques Klein
topics:
- structured-output
- code-intelligence
- llm-decoding
- software-engineering
- function-calling
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Empirical Study for Structured Output Control in LLMs for Software Engineering

## Summary
## 摘要
这篇论文研究了为什么大语言模型在软件工程中的结构化输出上会出错，比如 JSON、SQL、代码和函数调用。它的核心结论是：语法控制有帮助，但不能解决模式级和取值级的失败。

## 问题
- LLM 输出常常要接入解析器、API、部署工具和数据管道，所以即使思路正确，只要输出违反了 JSON 语法、SQL 语法、函数签名或局部模式，仍然会失败。
- 论文把失败分为语法错误、结构错误和值错误，因为每种错误都需要不同的修复方式。
- 这个问题会影响自动化软件流程：格式错误的 API 调用、配置或查询会中断流水线，或者把错误数据传给后续步骤。

## 方法
- 这项研究在 4 类软件工程任务上评估结构化输出行为：BigCodeBench 上的 text-to-code，Spider 上的 text-to-SQL，CallNavi 上的 text-to-JSON，以及 BFCL 上的函数调用。
- 它比较了 9 个 LLM：7 个通用模型和 2 个面向代码的模型，其中若干模型的规模从 7B 到 70B 不等。
- 它对 Python 和 SQL 任务使用 pass@1，对 JSON 和函数调用任务使用基于 AST 的评估。
- 它测试了解码器侧控制方法：语法约束解码、基于正则表达式的验证，以及 Template Token Match Generation，简称 TTMG。
- TTMG 通过匹配模板 token 来修复固定格式部分，然后只让模型生成可变内容，在模板复制和自由生成之间切换。

## 结果
- 给出的摘录没有包含最终的 pass@1 分数、AST 准确率分数或完整的错误率表，所以不能据此给出整体任务准确率的精确数值结论。
- 最强的结论是：TTMG 几乎消除了语法错误，但结构错误和值错误仍然存在。
- 评估覆盖 4 类任务和 4 个命名基准：BigCodeBench、Spider、CallNavi 和 BFCL。
- 模型集合包含 9 个模型：LLaMA-3.1-8B、Qwen-2.5-7B-it、Gemma2-9B-it、Qwen3-30B-A3B-IT、Mixtral-8x7B-Instruct-v0.1、LLaMA-3.1-70B GGUF、GPT-4.1-mini、Qwen2.5-Coder-7B-it 和 Seed-Coder-8B-it。
- 论文写到，提示词调优在主基准测试前使用了每个数据集 5% 的样本。
- 背景综述列出 8 个结构化输出工具，并提到一些系统成本或主张，例如 LLGuidance 在 128k 词表下每个 token 约 50 µs CPU 开销，以及 XGrammar 声称在负载下 token 生成速度最高可提升 5 倍。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.09395v1](https://arxiv.org/abs/2606.09395v1)
