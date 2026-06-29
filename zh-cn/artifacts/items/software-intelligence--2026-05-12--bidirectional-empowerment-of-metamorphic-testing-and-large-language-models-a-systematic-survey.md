---
source: arxiv
url: https://arxiv.org/abs/2605.13898v1
published_at: '2026-05-12T13:47:26'
authors:
- Zheng Zheng
- Zenghui Zhou
- Yinwang Xu
- Daixu Ren
- Tsong Yueh Chen
topics:
- metamorphic-testing
- llm-testing
- software-quality-assurance
- code-intelligence
- test-automation
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# Bidirectional Empowerment of Metamorphic Testing and Large Language Models: A Systematic Survey

## Summary
## 摘要
这篇综述梳理了如何用变形测试来测试 LLM 系统，以及如何用 LLM 自动化变形测试的部分环节。它回顾了 93 篇主要研究，并把这一领域归纳为两个主要方向。

## 问题
- LLM 的输出是概率性的、开放式的，而且常常没有唯一正确答案，所以精确测试预言在问答、对话、代码生成、RAG 和智能体等任务上效果不好。
- 变形测试检查相关输入和输出之间的关系，适合正确性取决于语义或比较结果的场景。
- 变形测试仍然需要人工去发现变形关系、构造输入变换，并实现可执行测试。

## 方法
- 这篇综述遵循 Kitchenham 风格的系统综述方法，检索了 ACM Digital Library、IEEE Xplore、SpringerLink、ScienceDirect、arXiv，并用 Google Scholar 做补充。
- 它使用一个元数据检索式，把变形测试相关术语与 LLM、GPT、Claude、Gemini、DeepSeek、代码模型、RAG 和智能体等术语组合起来。
- 它纳入使用变形测试来研究 LLM，或使用 LLM 支持变形测试的研究，同时排除了与“MR”无关的用法，以及不涉及 LLM 的通用机器学习测试。
- 它把文献分成两个方向：面向 LLM 的 MT 和面向 MT 的 LLM。
- 面向 LLM 的 MT 覆盖幻觉、公平性、鲁棒性、代码可靠性、RAG、对话和自主智能体；面向 MT 的 LLM 覆盖关系发现、输入变换、测试实现和闭环测试。

## 结果
- 这篇论文回顾了截至 2026 年 4 月 30 日可获得文献中的 93 篇主要研究。
- 覆盖的发表时间主要是 2019 年 1 月到 2026 年 4 月，在 2022 年末 ChatGPT 发布后增长更快，2024 年后增长更明显。
- 检索使用了 5 个主要学术来源，并在每个查询下检查了 Google Scholar 的前 250 条结果作为补充覆盖。
- 作者主张的主要贡献是一个两部分分类法：面向 LLM 的 MT 和面向 MT 的 LLM。
- 这篇综述没有报告基准式的模型性能提升，比如准确率、通过率，或相对基线的缺陷检测改进；它的量化内容主要是语料规模、检索范围、时间窗口，以及综述图中给出的类别数量。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.13898v1](https://arxiv.org/abs/2605.13898v1)
