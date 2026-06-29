---
source: arxiv
url: http://arxiv.org/abs/2604.12881v1
published_at: '2026-04-14T15:32:07'
authors:
- Changshu Liu
topics:
- code-reasoning
- benchmarking
- software-evaluation
- python-repositories
- llm-for-code
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Evaluating LLMs Code Reasoning Under Real-World Context

## Summary
## 总结
R²Eval 是一个从真实 Python 项目构建的代码推理基准，而不是由简短独立代码片段组成。它测试 LLM 能否在代码依赖真实仓库上下文和复杂数据类型时，预测程序输入和输出。

## 问题
- 现有代码推理基准大多使用简短的生成代码片段或编程题解答，因此看不到真实仓库的结构、依赖关系和以对象为主的数据。
- 许多先前基准把输入和输出限制为基本类型，这去掉了生产代码里常见的一类难点。
- 这很重要，因为在简化基准上的高分会高估模型在真实项目中的软件任务表现，比如程序修复、翻译和生成。

## 方法
- 论文提出了 **R²Eval**，这是一个包含 **135** 个代码推理问题的基准，题目来自 **10** 个常用 Python 项目：scikit-learn、django、requests、seaborn、sphinx、pytest、astropy、xarray、matplotlib 和 sympy。
- 每个问题都是一个三元组 **(P, I, O)**：包含相关方法、依赖和类上下文的代码；序列化输入；以及序列化输出。
- 核心机制是程序分析，把复杂、复合和自定义运行时对象拆成可 JSON 序列化的部分，这样模型看到的是更接近真实情况的输入和输出，而不只是基本值。
- 评分时，基准会把模型输出反序列化回对象，再通过运行测试检查正确性，这样可以避免把纯字符串匹配当成错误来源。
- 评估把 R²Eval 和从 CRUXEval 中抽取的、规模匹配的 **135 题**样本进行对比，在六个 LLM 上同时测试输入预测和输出预测任务。

## 结果
- 在六个模型上，输入预测的平均准确率从 **81.23% 降到 16.91%**，从 CRUXEval 到 R²Eval 下降了 **64.32** 个百分点。
- 在六个模型上，输出预测的平均准确率从 **80.37% 降到 28.15%**，下降了 **52.22** 个百分点。
- **o4-mini** 在输入预测上从 **92.59%** 降到 **20.00%**，在输出预测上从 **91.85%** 降到 **28.15%**。
- **Gemini-2.5-Pro** 在输入预测上从 **91.85%** 降到 **15.56%**，在输出预测上从 **88.89%** 降到 **34.07%**。
- **DeepSeek-R1** 在输入预测上从 **94.81%** 降到 **21.48%**，在输出预测上从 **87.41%** 降到 **31.85%**。
- 以推理为重点的模型在输入预测上平均比非推理模型高 **13.95** 个百分点，在输出预测上高 **12.22** 个百分点，但所有模型在这个更接近真实场景的基准上都明显退化。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.12881v1](http://arxiv.org/abs/2604.12881v1)
