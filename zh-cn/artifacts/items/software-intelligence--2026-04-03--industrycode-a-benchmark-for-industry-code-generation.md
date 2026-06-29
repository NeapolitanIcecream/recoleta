---
source: arxiv
url: http://arxiv.org/abs/2604.02729v1
published_at: '2026-04-03T04:44:07'
authors:
- Puyu Zeng
- Zhaoxi Wang
- Zhixu Duan
- Liang Feng
- Shaobo Wang
- Cunxiang Wang
- Jinghang Wang
- Bing Zhao
- Hu Wei
- Linfeng Zhang
topics:
- code-generation-benchmark
- industrial-code
- multilingual-evaluation
- software-engineering
- llm-evaluation
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# IndustryCode: A Benchmark for Industry Code Generation

## Summary
## 总结
IndustryCode 是一个用于测试跨领域、跨语言真实工业任务代码生成能力的基准，覆盖了常见代码基准没有触及的场景。它同时衡量模块化子任务和完整项目级问题，而当前最强模型在可靠的工业级表现上仍有差距。

## 问题
- 现有代码基准主要关注通用软件任务、单一领域或单一语言，因此无法测试工业工作中常见的领域知识、数值精度和语言多样性。
- 真实的工业编码往往使用 MATLAB、Stata 这类专用语言，并且需要在更大的项目里解决彼此关联的子模块。
- 这很重要，因为面向消费场景或互联网风格编码任务的基准分数，不能说明模型是否能处理金融、自动化、航空航天或其他生产工程场景。

## 方法
- 论文构建了 **IndustryCode**，一个包含 **125 个主工业问题**、拆分为 **579 个子问题** 的基准。
- 任务来自行业从业者在生产环境中使用的真实代码，之后经过人工重建和修订，以减少预训练污染，并加入更难的数学、算法、工程和架构约束。
- 基准覆盖 **4 种语言**：**Python、C++、MATLAB 和 Stata**，涉及大约 **20 个子领域**，包括金融、自动化、航空航天、建筑、半导体和物流。
- 评测采用分层设置：模型先在主任务提供的累计上下文和前面生成的代码基础上解决子问题，再对完整主问题评分。
- 评分结合了 **基于执行的数值验证** 和 **LLM 裁判**，用于固定 I/O 测试难以单独判断功能或结构等价的情况。

## 结果
- 数据集规模：**125 个主问题**、**579 个子问题**；开发集划分为 **19 个主问题 / 80 个子问题**，测试集划分为 **106 个主问题 / 499 个子问题**。
- 最佳总体模型：**Claude 4.5 Opus**，在 **子问题** 上达到 **68.1% Pass@1**，在 **主问题** 上达到 **42.5%**。
- 其他表现较强的闭源模型：**Claude 4.5 Sonnet** 的总体成绩为 **64.4% / 33.8%**；**Gemini-3-pro** 为 **63.4% / 41.2%**；**GPT-5.2** 为 **53.4% / 32.4%**。
- 开源模型中，**Qwen3-Max** 在 **C++ 子问题** 上拿到 **70.4%**，高于该设置下的 **GPT-5.2（67.9%）** 和 **Gemini-3-pro（66.0%）**；它的总体成绩为 **55.9% / 32.5%**。
- 错误分析显示，失败主要来自 **语法错误（32.8%）**、**误解题意（30.2%）** 和 **幻觉（19.6%）**；**推理失败** 只占 **8.4%**。
- 对部分模型来说，思考模式平均让子问题成绩提升约 **+4.70%**，主问题提升约 **+7.65%**，但也在其他情况下增加了上下文混淆和语法问题。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.02729v1](http://arxiv.org/abs/2604.02729v1)
