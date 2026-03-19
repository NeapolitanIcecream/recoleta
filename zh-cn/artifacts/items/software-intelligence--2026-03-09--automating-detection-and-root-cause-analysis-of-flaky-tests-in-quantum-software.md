---
source: arxiv
url: http://arxiv.org/abs/2603.09029v1
published_at: '2026-03-09T23:57:55'
authors:
- Janakan Sivaloganathan
- Ainaz Jamshidi
- Andriy Miranskyy
- Lei Zhang
topics:
- quantum-software
- flaky-test-detection
- root-cause-analysis
- large-language-models
- software-maintenance
relevance_score: 0.71
run_id: materialize-outputs
language_code: zh-CN
---

# Automating Detection and Root-Cause Analysis of Flaky Tests in Quantum Software

## Summary
本文提出一个面向量子软件的自动化流水线，用于从仓库中的 issue/PR 检测 flaky test，并进一步用大语言模型做根因分析。它的重要性在于量子程序天然具有概率性，传统测试更容易出现“同样代码、结果时好时坏”的问题，影响质量保障与维护效率。

## Problem
- 论文解决的是**量子软件中的 flaky test 自动检测与根因定位**问题：测试在代码未变化时仍会随机通过或失败，容易掩盖真实缺陷并误导开发者。
- 这一问题在量子场景更重要，因为量子程序本身具有概率性，且真实硬件重跑成本高、噪声大、复现困难。
- 现有量子 flaky test 数据集小、发现方式依赖关键词和人工分析，召回率与可扩展性有限。

## Approach
- 先以已有量子 flaky test 数据集为种子，把 GitHub issue/PR 文本编码成向量，用**embedding + cosine similarity** 检索与已知 flaky case 语义相近的新候选报告。
- 对高相似候选进行人工交叉核验，迭代两轮，扩展出新的 flaky test，并补充其**根因类别、缺陷代码和修复信息**。
- 再评估多种基础模型/大语言模型（OpenAI GPT、Meta LLaMA、Google Gemini、Anthropic Claude）完成两类任务：**是否为 flaky test 相关报告的分类**，以及**根因识别**。
- 方法核心可以简单理解为：先用语义相似度“找像 flaky 的报告”，再让 LLM 读 issue 描述和代码上下文，判断“是不是 flaky”以及“为什么 flaky”。

## Results
- 流水线共发现 **25 个此前未知的 flaky tests**，使原始数据集规模提升 **54%**；数据集从先前 **46** 个扩展到 **71** 个 flaky tests。
- 最终数据覆盖 **12 个开源量子软件仓库**、**8,628** 个已关闭 issue/PR；观测到的 flaky 报告占比约为 **0.82%（71/8,628）**。
- 在根因统计上，最常见原因是 **Randomness**，占 **19.2%（14/73 标注）**；最常见修复模式是 **Fix Seed**，占 **16.4%（12/73）**。
- 最优模型为 **Google Gemini 2.5 Flash**：flakiness detection 的 **F1-score = 0.9420**，root-cause identification 的 **F1-score = 0.9643**。
- 论文声称该结果表明 LLM 已能为量子软件中的 flaky 报告分诊和根因理解提供**实用支持**，并提供可复用的扩展数据集与自动化流水线。

## Link
- [http://arxiv.org/abs/2603.09029v1](http://arxiv.org/abs/2603.09029v1)
