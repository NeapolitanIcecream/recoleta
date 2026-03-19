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
- llm-for-se
- repository-mining
relevance_score: 0.03
run_id: materialize-outputs
language_code: zh-CN
---

# Automating Detection and Root-Cause Analysis of Flaky Tests in Quantum Software

## Summary
本文提出一个面向量子软件的自动化流程，用于发现 flaky tests（无代码变化却随机通过/失败的测试）并分析其根因。它将仓库挖掘、向量相似度检索和多种大语言模型结合起来，以扩展数据集并自动完成缺陷分流。

## Problem
- 论文解决的是**量子软件中 flaky test 的自动检测与根因分析**问题；这很重要，因为量子程序天然具有概率性，测试结果更容易不稳定，从而掩盖真实缺陷并浪费开发者排查时间。
- 与经典软件相比，量子 flaky tests 还受到**随机性、量子噪声、真实硬件复现成本高**等因素影响；例如文中提到 IBM 量子平台可达 **96 美元/分钟**，反复重跑测试代价高。
- 现有量子 flaky test 数据主要依赖**关键词搜索和人工分析**，召回率有限、扩展慢，难以支撑大规模自动化维护。

## Approach
- 先从作者此前整理的量子 flaky test 数据出发，对 **12 个开源量子软件仓库**中的 GitHub issue/PR 文本做嵌入表示，并与已知 flaky 案例计算**余弦相似度**，从高相似候选中人工复核新案例。
- 嵌入模型比较了多个方案，最终选用 **mixedbread-ai/mxbai-embed-large-v1**，因为它对 flaky / non-flaky 的区分更清晰。
- 在检测与诊断阶段，作者评测了多家 FM/LLM（**OpenAI GPT、Meta LLaMA、Google Gemini、Anthropic Claude**），让模型基于 issue/PR 描述以及额外代码上下文判断：**是否为 flaky test**、以及**根因类别**。
- 方法本质上可以简单理解为：**先用“语义检索”找到像 flaky 的报告，再用 LLM 读懂文本和代码，判断是不是 flaky，并给出最可能原因。**

## Results
- 该流程新发现 **25 个**此前未知的量子 flaky tests，使原始数据集规模提升 **54%**；总计得到 **71 个 flaky tests**，来自 **12 个仓库**、**8,628 个关闭的 issue/PR**。
- 按仓库统计，观察到的 flaky 报告占比约为 **0.82%（71/8,628）**；不同仓库差异明显，例如 **qiskit: 29/4,533 = 0.55%**，**Microsoft Quantum: 4/111 = 3.60%**。
- 根因分析显示最常见原因是 **Randomness**，占 **19.2%（14/73 标签）**；最常见修复方式是 **Fix Seed**，占全部修复模式的 **16.4%（12/73）**。此外，多线程 **13.7%**，软件环境 **11.0%**，浮点问题 **9.6%**。
- 在自动分类上，最佳模型 **Google Gemini 2.5 Flash** 的 **flakiness detection F1 = 0.9420**。
- 在根因识别上，同一最佳模型达到 **root-cause identification F1 = 0.9643**。
- 论文的核心突破性主张是：**LLM 已能在量子软件中实用地支持 flaky 报告分流与根因定位**，同时产出一个扩展后的可复用数据集与自动化流程。

## Link
- [http://arxiv.org/abs/2603.09029v1](http://arxiv.org/abs/2603.09029v1)
