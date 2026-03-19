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
- code-language-models
- human-attention
relevance_score: 0.03
run_id: materialize-outputs
language_code: zh-CN
---

# Semantic Neighborhood Density and Eye Gaze Time in Human Programmer Attention

## Summary
本文研究源代码词元的语义邻域密度（SND）是否与程序员眼动停留时间相关，并在 C 与 Java 两个眼动数据集上进行统计与预测分析。结论是：高 SND 词通常获得更长注视时间，尤其是低频词，但其预测力总体较弱。

## Problem
- 论文要解决的问题是：**源代码中的词语“语义上是否拥挤”（SND 高低）会不会影响程序员看代码时的注视时长**，以及这种关系是否能帮助解释或预测程序员注意力。
- 这很重要，因为眼动时间常被当作**认知负担、困惑程度和注意力分配**的代理指标；若能理解其驱动因素，就能改进程序理解研究、工具设计和注意力建模。
- 在心理语言学里，SND 已被证明与自然语言阅读有关，但**在软件工程/代码阅读场景中基本未被研究**，其含义可能不同。

## Approach
- 使用两个既有眼动实验数据：**C 缺陷定位**数据集（21 名程序员，约 **31 小时**）和 **Java 代码摘要/文档编写**数据集（10 名程序员，约 **60 小时**）。
- 从代码仓库提取词元；Java 额外进行 **camelCase/下划线拆分** 与小写化，构建语言特定词表。
- 用两类语言模型生成词向量：**GPT2（按 C/Java 分别训练的 350M 模型）** 和 **CodeLLaMA 7B**；再按 Shaoul & Westbury 的 ARC 思路计算 SND：先用 **10k 随机词对**估计全局距离阈值，再对每个词取阈值内邻居的平均余弦相似度作为 SND。
- 同时计算词频（TF），并做两类分析：一是**无模型统计分析**，把词分成高/低 SND、高/低频以及“高 SND 且低频”组，比较四种眼动指标（SFD、FFD、GD、RPD）；二是**有模型分析**，检查 SND 与频率对注视时长的预测区分能力。

## Results
- 数据规模方面，研究覆盖 **2 个编程语言/任务场景**：C 数据集 **21 人、31 小时**，Java 数据集 **10 人、60 小时**；表明分析基于较长时段真实代码阅读。
- 论文核心发现是：**高 SND 词比低 SND 词往往有更高 gaze time**，并且这种现象在 **C 数据集**上更明显；摘要中未给出具体显著性数值、效应量或每项指标的完整统计表。
- 另一项明确结论是：**SND 与词频存在交互**，其中**低频且高 SND**的词更容易获得更高视觉注意力；作者用这点回应了心理语言学中“高 SND × 低频”效应。
- 在模型选择上，作者声称使用**定制 GPT2 计算 SND**时，这种关联更强；但摘要摘录未提供与 **CodeLLaMA** 的定量对比数值。
- 预测方面，作者称 **SND 和频率对 gaze time 仅有轻微（minor）预测能力**，说明它们虽与注意力相关，但在高噪声眼动数据上并不足以强力预测注视时长。
- **未提供明确量化结果**：给定摘录没有报告具体的 p 值、FDR 校正结果、Hedges' g、准确率/AUC，或相对任何基线模型的提升幅度。

## Link
- [http://arxiv.org/abs/2603.03566v1](http://arxiv.org/abs/2603.03566v1)
