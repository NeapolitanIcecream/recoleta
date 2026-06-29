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
## 总结
本文认为，当前仓库级代码定位基准更奖励关键词匹配，而不是结构推理。文中提出了一个关键词无关的基准，以及一个神经符号系统 LogicLoc，它把自然语言转换成针对抽取出的程序事实的 Datalog 查询。

## 问题
- 论文关注的是仓库级代码定位，查询里没有文件名、类名、函数名或其他词汇锚点。
- 这很重要，因为自治软件工程智能体需要只根据意图找到正确代码，而像 SWE-bench 这样的基于 issue 的基准，常常让系统通过匹配堆栈跟踪或标识符里的关键词取胜。
- 作者把这种失败模式称为 **Keyword Shortcut**，并认为现有方法一旦必须围绕仓库结构而不是表面文本推理，就会失效。

## 方法
- 作者定义了 **Keyword-Agnostic Logical Code Localization (KA-LCL)**，并构建了 **KA-LogicQuery**，这是一个包含 **25** 个逻辑查询的诊断基准，带有真实位置且没有命名提示。
- LogicLoc 先对仓库做静态分析，提取 **program facts**，包括函数、类、包含关系、继承、导入、调用、引用，以及可选的控制流/数据流关系。
- LLM 读取自然语言查询，并写出一个 **Datalog** 程序，用这些事实表达需要匹配的结构条件。
- 系统使用 **parser-gated validation** 和 **synthesize-check-refine** 循环。它会修复简单语法问题，执行部分规则，检查空的中间关系，并用基于变异的诊断信息帮助 LLM 修正规则过于严格的问题。
- 通过验证的查询会在 **Soufflé** Datalog 引擎中运行，返回精确的代码位置；如果没有匹配项，也可以返回空结果。

## 结果
- 论文称，**KA-LogicQuery** 上的最先进定位方法出现了 **灾难性** 下降，但摘要里没有给出具体分数、各方法对应的数据集表，或绝对差值。
- 论文还称 **LogicLoc significantly outperforms SOTA methods on KA-LogicQuery**，但提供的摘要没有具体指标值或基线数值。
- 文中也说，LogicLoc 在像 **SWE-bench** 这样的 **issue-driven benchmarks** 上保持了有竞争力的表现，不过同样没有给出定量数值。
- 作者表示，LogicLoc 比依赖迭代式 LLM 的方法使用 **更少的 token**、运行 **更快**，因为结构遍历由确定性的 Datalog 引擎处理，但摘要没有给出 token 数或延迟数值。
- 论文里的一个具体例子查询的是参数 **超过 15 个** 且排除 `__init__` 的函数，系统返回 **2** 个匹配项：`astropy/convolution/convolve.py: convolve_fft`，它在第 **442** 行有 **19** 个参数；以及 `astropy/io/fits/column.py: _verify_keywords`，它在第 **952** 行有 **17** 个参数。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.16021v2](http://arxiv.org/abs/2604.16021v2)
