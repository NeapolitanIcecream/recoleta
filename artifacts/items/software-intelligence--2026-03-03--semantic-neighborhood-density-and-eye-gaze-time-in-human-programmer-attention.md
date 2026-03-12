---
source: arxiv
url: http://arxiv.org/abs/2603.03566v1
published_at: '2026-03-03T22:51:04'
authors:
- Robert Wallace
- Emory Michaels
- Yu Huang
- Collin McMillan
topics:
- program-comprehension
- eye-tracking
- semantic-neighborhood-density
- code-embeddings
- human-attention
relevance_score: 0.64
run_id: materialize-outputs
---

# Semantic Neighborhood Density and Eye Gaze Time in Human Programmer Attention

## Summary
本文研究源代码词元的语义邻域密度（SND）是否与程序员眼动停留时间相关，并在 C 与 Java 两个真实眼动数据集上做统计与预测分析。结论是：高 SND 词，尤其是低频词，通常会获得更长的注视时间，但这种信息对预测注视时间的增益较小。

## Problem
- 论文要解决的问题是：**源代码中的词语“语义邻居是否拥挤”是否会影响程序员阅读时的视觉注意与认知负担**，并且这种影响能否用于预测眼动时间。
- 这很重要，因为眼动时间常被用作程序理解难度与注意力分配的代理信号；若能解释哪些代码词更“吸睛”或更费解，就有助于改进程序理解、代码展示和面向人的软件设计。
- 现有 SND 研究主要在自然语言阅读中，软件工程里其含义未知，尤其代码词往往抽象但缺少自然语言中的情绪因素，可能呈现不同规律。

## Approach
- 使用两个既有眼动实验数据集：**C 缺陷定位**（21 名程序员，约 **31 小时**）和 **Java 代码总结/文档编写**（10 名程序员，约 **60 小时**）。
- 从代码仓库提取词元；对 Java 进一步做驼峰/下划线切分与小写化。随后用两种代码语言模型生成词向量：面向 C/Java 分别训练的 **GPT2-like 350M**，以及多语言代码模型 **CodeLLaMA 7B**。
- 按 Shaoul & Westbury 的 ARC 思路计算每个词的 **SND**：先在嵌入空间中用随机采样的 10k 词对估计全局距离阈值，再对阈值内邻居的余弦相似度取平均；同时计算语料级 **term frequency (TF)**。
- 进行两类分析：一是**无模型统计分析**，把词按高/低 SND、频率及“高 SND 且低频”分组，比较 **SFD/FFD/GD/RPD** 四类眼动指标；二是**有模型分析**，检验 SND 与频率对注视时间是否具有预测力。

## Results
- 主要结论：**高 SND 词比低 SND 词更容易获得更长的眼动时间**，这一趋势在 **C 数据集**中更明显，并且在使用**定制 GPT2**计算 SND 时更强。
- 交互效应上，**低频且高 SND 的词**最容易得到更多视觉注意；作者明确总结为：**较稀有但语义邻域更密集的词往往注视更久**。
- 数据规模方面，实验基于两个真实任务：C 数据集 **21 人 / 31 小时 / 8 个 bug report**，Java 数据集 **10 人 / 60 小时 / 40 个方法**；C 的回视率约 **43.0%–67.0%**，Java 约 **49.8%–56.6%**。
- 模型方面，SND 由 **GPT2 350M（1024 维嵌入）** 和 **CodeLLaMA 7B（4096 维嵌入）** 计算；论文声称 GPT2 派生的 SND 在关联性上表现更好，暗示语言专用嵌入比跨语言大模型嵌入更适合该分析。
- 预测结论上，作者指出 **SND 与频率对 gaze time 只有“minor predictive power”**；给定摘录中**未提供具体预测指标数值**（如 AUC、R²、F1 或误差下降幅度），因此无法报告定量优于何种基线多少。

## Link
- [http://arxiv.org/abs/2603.03566v1](http://arxiv.org/abs/2603.03566v1)
