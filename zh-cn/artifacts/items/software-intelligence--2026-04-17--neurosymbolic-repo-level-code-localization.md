---
source: arxiv
url: http://arxiv.org/abs/2604.16021v2
published_at: '2026-04-17T12:49:18'
authors:
- Xiufeng Xu
- Xiufeng Wu
- Zejun Zhang
- Yi Li
topics:
- repo-level-code-localization
- neurosymbolic-reasoning
- datalog
- code-intelligence
- software-engineering-agents
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Neurosymbolic Repo-level Code Localization

## Summary
## 摘要
这篇论文认为，当前仓库级代码定位基准更奖励关键词匹配，而不是结构推理。论文提出了一个与关键词无关的基准，以及一个神经符号系统 LogicLoc。该系统把自然语言转换为针对已提取程序事实的 Datalog 查询。

## 问题
- 论文关注仓库级代码定位，尤其是在查询中不包含文件名、类名、函数名或其他词汇锚点的情况。
- 这一点很重要，因为自主软件工程代理需要仅根据意图找到正确代码，而像 SWE-bench 这类基于 issue 的基准，通常会让系统通过匹配堆栈跟踪或标识符中的关键词获胜。
- 作者把这种失效模式称为 **Keyword Shortcut**，并认为当前方法一旦必须基于仓库结构推理，而不是依赖表面文本，性能就会崩溃。

## 方法
- 作者定义了 **Keyword-Agnostic Logical Code Localization (KA-LCL)**，并构建了 **KA-LogicQuery**。这是一个诊断型基准，包含 **25** 个逻辑查询，带有真实位置标注，且没有命名提示。
- LogicLoc 先对代码仓库运行静态分析，提取**程序事实**，例如函数、类、包含关系、继承、导入、调用、引用，以及可选的控制流/数据流关系。
- LLM 读取自然语言查询，并编写一个 **Datalog** 程序，用这些事实表达需要匹配的结构条件。
- 系统使用 **parser-gated validation** 和 **synthesize-check-refine** 循环。它会修复简单语法问题，执行部分规则，检查为空的中间关系，并用基于变异的诊断帮助 LLM 修正约束过强的规则。
- 通过验证后的查询会在 **Soufflé** Datalog 引擎中运行，返回精确的代码位置；如果没有匹配项，也可以返回空结果。

## 结果
- 论文称，最先进的定位方法在 **KA-LogicQuery** 上出现了**灾难性**下滑，但摘录**没有**提供精确分数、按方法划分的数据集表格或绝对差值。
- 论文称 **LogicLoc significantly outperforms SOTA methods on KA-LogicQuery**，但摘录中没有给出具体指标值或具名基线数字。
- 论文还称，LogicLoc 在 **SWE-bench** 等**基于 issue 的基准**上仍保持**有竞争力的性能**，但提供的文本同样没有量化数值。
- 作者表示，LogicLoc 的 **token 使用更少**、运行**更快**，因为结构遍历由确定性的 Datalog 引擎处理，而不是依赖大量迭代式 LLM 推理；但摘录没有给出 token 数或延迟数据。
- 论文中的具体示例展示了一个查询：查找**参数超过 15 个**且排除 `__init__` 的函数。系统返回了 **2** 个匹配项：`astropy/convolution/convolve.py: convolve_fft`，有 **19** 个参数，位于第 **442** 行；以及 `astropy/io/fits/column.py: _verify_keywords`，有 **17** 个参数，位于第 **952** 行。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.16021v2](http://arxiv.org/abs/2604.16021v2)
