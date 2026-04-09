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
## 摘要
IndustryCode 是一个用于测试真实工业任务代码生成的基准，覆盖多个领域和编程语言，弥补了常见代码基准的空白。它同时衡量模块化子任务和完整项目级问题，而当前最强模型离可靠的工业级表现仍有差距。

## 问题
- 现有代码基准主要关注通用软件任务、单一领域或单一语言，因此无法测试工业工作中常见的领域知识、数值精度和语言多样性。
- 真实工业编程经常使用 MATLAB 和 Stata 这类专用语言，还需要在更大项目中解决彼此关联的子模块。
- 这一点很重要，因为在面向消费者或互联网风格编码任务上的基准分数，并不能说明模型是否能处理金融、自动化、航空航天或其他生产工程场景。

## 方法
- 论文构建了 **IndustryCode**，这是一个包含 **125 个主要工业问题** 并拆分为 **579 个子问题** 的基准。
- 这些任务来自行业从业者使用的真实生产代码，之后经过人工重构和修订，以减少预训练污染，并加入更高难度的数学、算法、工程和架构约束。
- 该基准覆盖 **4 种语言**：**Python、C++、MATLAB 和 Stata**，涵盖大约 **20 个子领域**，包括金融、自动化、航空航天、建筑、半导体和物流。
- 评测采用分层设置：模型在主任务和先前生成代码提供的累积上下文下解决子问题，同时也会在完整的主要问题上评分。
- 评分结合了**基于执行的数值验证**和 **LLM judge**，用于处理那些仅靠固定输入输出测试难以检查功能或结构等价性的情况。

## 结果
- 数据集规模：**125 个主要问题**、**579 个子问题**；其中开发集为 **19 个主要问题 / 80 个子问题**，测试集为 **106 个主要问题 / 499 个子问题**。
- 总体最佳模型：**Claude 4.5 Opus**，在**子问题**上达到 **68.1% Pass@1**，在**主要问题**上达到 **42.5%**。
- 其他表现较强的闭源模型：**Claude 4.5 Sonnet** 总体达到 **64.4% / 33.8%**；**Gemini-3-pro** 达到 **63.4% / 41.2%**；**GPT-5.2** 达到 **53.4% / 32.4%**。
- 较强的开源模型结果：**Qwen3-Max** 在 **C++ 子问题**上得到 **70.4%**，超过该设置下的 **GPT-5.2 (67.9%)** 和 **Gemini-3-pro (66.0%)**；其总体分数为 **55.9% / 32.5%**。
- 错误分析显示，失败主要来自 **语法错误 (32.8%)**、**误解题目 (30.2%)** 和 **幻觉 (19.6%)**；**推理失败**较低，为 **8.4%**。
- Thinking mode 对部分模型有帮助，对那些从中受益的模型来说，子问题平均提升约 **+4.70%**，主要问题平均提升约 **+7.65%**；但在其他情况下，它也增加了上下文混淆和语法问题。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.02729v1](http://arxiv.org/abs/2604.02729v1)
