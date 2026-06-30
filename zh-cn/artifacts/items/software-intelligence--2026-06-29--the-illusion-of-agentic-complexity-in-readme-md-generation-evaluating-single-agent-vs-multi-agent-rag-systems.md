---
source: arxiv
url: https://arxiv.org/abs/2606.30524v1
published_at: '2026-06-29T16:29:31'
authors:
- Abu Saleh
- Tesfay Welegebreal Tesfay
- Phuong T. Nguyen
- Juri Di Rocco
- Muhammad Umar Zeshan
- Davide Di Ruscio
topics:
- readme-generation
- multi-agent-systems
- rag
- software-documentation
- code-intelligence
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# The Illusion of Agentic Complexity in README.md Generation: Evaluating Single-Agent vs. Multi-Agent RAG Systems

## Summary
## 摘要
这篇论文测试多智能体 RAG 用于生成 GitHub README 文件时是否值得付出相应成本。论文发现，单智能体 RAG 系统在词汇指标上与自主 MAS 相当，成本低得多；由人工提供计划时，质量最好。

## 问题
- README 文件通常由人工编写，容易不完整或过时，并影响用户理解和采用代码库。
- 多智能体软件工程系统通常假设把工作拆分给多个智能体会提升输出质量，但论文测试了这类额外成本对 README 生成是否有帮助。
- 这项任务重要，因为代码库级文档需要基于源代码，包含正确命令、清晰章节和一致格式。

## 方法
- 研究比较四类输出：Single-Agent RAG、自主 MAS RAG、Dev-Plan MAS 和 LARCH，并使用原始 README 文件作为参考。
- 数据集包含 180 个 2025 年 8 月之后创建的 GitHub 代码库：118 个 Python、49 个 JavaScript 和 13 个 Go。Dev-Plan 在一个包含 20 个代码库的子集上测试。
- 流水线会移除现有 Markdown 文件，用语法感知分块对源文件和配置文件建索引，使用 `text-embedding-3-small` 嵌入分块，将其存储在 ChromaDB 中，并使用 `gpt-5.1` 生成内容。
- Single-Agent 系统检索与章节相关的代码分块，并在一个提示中写完整个 README。MAS 使用 profiler、planner、section writers、reviewer 和 aggregator。Dev-Plan 用人工编写的 JSON 计划替代 MAS planner。
- 评估使用 ROUGE、BERTScore、token 数、运行时间、基于 12 章节 README 分类法的人工覆盖率检查，以及按 10 分制打分的 LLM judge。

## 结果
- 在 180 个代码库上，Single-Agent 的 ROUGE-L F1 略高于自主 MAS：0.2007 对 0.1964。两者都高于 LARCH，后者的 ROUGE-L F1 为 0.1022。
- Single-Agent 平均每个 README 使用 7,840 个 token，耗时 40 秒。MAS 使用 56,242 个 token，耗时 78 秒，token 数约为前者的 7.1 倍。论文将其报告为 Single-Agent 相比 MAS 减少 86% token。
- Dev-Plan 报告的词汇指标最好：ROUGE-L F1 为 0.2323，BERTScore F1 为 0.8230，但平均每个 README 需要 79,196 个 token 和 148 秒。
- 在 20 个代码库的结构评估中，MAS 的人工精确率最高，为 0.982，召回率为 0.696，F1 为 0.814。Single-Agent 的精确率为 0.776，召回率为 0.492，F1 为 0.602。
- Dev-Plan 的评审有用性最好：LLM-judge 平均得分 8.60，第一名胜率 53.75%，失败率 1.25%。MAS 得分 7.55，胜率 16.25%，失败率 2.50%。Single-Agent 得分 7.25，胜率 10.00%，失败率 6.25%。
- 在结构研究中，原始 README 文件得分低于 Dev-Plan：精确率 0.724，召回率 0.667，F1 为 0.694，平均评审得分 7.36，失败率 17.50%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.30524v1](https://arxiv.org/abs/2606.30524v1)
