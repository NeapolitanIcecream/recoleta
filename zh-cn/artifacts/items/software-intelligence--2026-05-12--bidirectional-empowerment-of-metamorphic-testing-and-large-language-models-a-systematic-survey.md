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
这篇综述梳理了变形测试如何测试大语言模型（LLM）系统，以及 LLM 如何自动化变形测试的部分环节。它回顾了 93 篇主要研究，并将该领域分为两个主要方向。

## 问题
- LLM 输出具有概率性和开放性，且常常没有唯一正确答案，因此精确测试预言在问答、对话、代码生成、RAG 和智能体等任务中效果较差。
- 变形测试检查相关输入和输出之间的关系，适合正确性依赖语义或比较判断的场景。
- 变形测试仍需要人工投入，用于发现变形关系、构建输入转换，并实现可执行测试。

## 方法
- 这篇综述采用 Kitchenham 风格的系统性综述方法，检索 ACM Digital Library、IEEE Xplore、SpringerLink、ScienceDirect、arXiv，并使用 Google Scholar 作为补充。
- 它使用元数据检索查询，将变形测试相关术语与 LLM、GPT、Claude、Gemini、DeepSeek、代码模型、RAG 和智能体相关术语组合。
- 它纳入将变形测试用于 LLM 的研究，或使用 LLM 支持变形测试的研究；同时排除与“MR”无关的用法，以及没有 LLM 参与的一般机器学习测试研究。
- 它将文献组织为 2 个方向：用于 LLM 的 MT，以及用于 MT 的 LLM。
- 用于 LLM 的 MT 涵盖幻觉、公平性、鲁棒性、代码可靠性、RAG、对话和自主智能体；用于 MT 的 LLM 涵盖关系发现、输入转换、测试实现和闭环测试。

## 结果
- 论文回顾了截至 2026 年 4 月 30 日可获得文献中筛选出的 93 篇主要研究。
- 覆盖的发表时间主要为 2019 年 1 月至 2026 年 4 月；在 2022 年底 ChatGPT 发布后增长加快，2024 年后增长更明显。
- 检索使用了 5 个主要学术来源，并检查每个查询在 Google Scholar 中的前 250 条结果，以补充覆盖范围。
- 论文声称的主要贡献是一个两部分分类法：用于 LLM 的 MT，以及用于 MT 的 LLM。
- 这篇综述没有报告基准式模型性能提升，例如相对于基线的准确率、通过率或缺陷检测改进；它的定量主张是语料规模、检索范围、时间窗口，以及综述图表中描述的类别计数。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.13898v1](https://arxiv.org/abs/2605.13898v1)
