---
source: hn
url: https://github.com/xraymemory/vibetheory
published_at: '2026-03-02T23:13:57'
authors:
- idempotent_
topics:
- computational-aesthetics
- text-analysis
- vae
- diffusion-models
- manifold-learning
relevance_score: 0.01
run_id: materialize-outputs
---

# Vibe Theory: Mathematical Derivation of Aesthetic Vibe from Text

## Summary
本文提出一个把文学批评中的“vibe（氛围/审美统一性）”形式化为可计算指标的工具，分别用 VAE 与扩散/流形模型从文本中提取“共享生成结构”。它更像概念验证型研究与软件实现，而非经过标准基准验证的机器学习论文。

## Problem
- 试图回答：文本或作者作品中的“审美氛围”能否被**数学化、可操作化**，而不只停留在主观文学描述。
- 这很重要，因为作者认为人们感知到的“Kafkaesque”等风格统一性，本质上是**多样现象可由少量共同结构近似生成**。
- 现有单一全局潜空间方法（如 VAE）可能无法刻画“表面差异很大但仍 vibe 一致”的数据，因此需要局部流形视角。

## Approach
- 将原始文本切成重叠滑动窗口（phenomena），再用 **TF-IDF + 标准化** 表示成向量。
- **VAE '17 模型**：训练一个自编码器，把文本窗口压缩到低维潜空间；用重建误差定义“canon（最符合 vibe 的核心现象）”，并计算 vibe density、aesthetic unity、vibe strength、excess of reality 等指标。
- **Diffusion '25 模型**：训练一个基于去噪 score matching 的小型 score network，把 vibe 看作隐式低维流形；用 **score norm** 做 on-manifold 判定。
- 在扩散版本中，再对 **score Jacobian 做 SVD** 提取局部切空间，并以邻域投影后的余弦相似度定义 **local comparability**，把“意义”从全局坐标改成局部邻域结构。
- 作者明确说明：2025 版的大部分数学定义是其对 Grietzer 概念文本的**自行 operationalization**，不是原文已有定理或标准公式。

## Results
- 对 **Kafka《The Trial》** 的 **VAE '17** 示例：23 个文本窗口、69 维 TF-IDF，训练在 **epoch 330** 提前停止，**final loss=0.085626**，有效潜维 **5**，压缩比 **0.0725**。
- 同一示例下，VAE 指标为：**Vibe Density=0.261**、**Aesthetic Unity=-0.058**、**Full-Text Comparability=-0.027**、**Vibe Strength=-0.031**、**Mean Reconstruction Error=1.9768**、**Excess of Reality=2.1996**；canon 大小 **6/23**。
- 对同一文本的 **Diffusion '25** 示例：训练在 **epoch 141** 提前停止，**final loss=0.927987**；判定 **on-manifold 17/23**，即 **0.739**，**Mean anomaly score=1.4527**。
- 扩散版本还报告：**Mean local comparability=0.414**、**Local comparability variability=0.126**、**Global comparability=-0.044**；前 8 个切空间奇异值均值从 **0.8814** 递减到 **0.4045**。
- 两文本比较（Kafka vs. Stein）示例中：Kafka 的 **Aesthetic Unity=0.061**，Stein 为 **-0.026**；交叉重建误差为 **1.4727** 与 **1.3953**，系统给出 **Vibe Similarity=1.000**，声称两者有“strong vibe affinity”。
- 但全文**没有标准数据集、消融实验、统计显著性或外部基线对比**；最强结论是作者展示了一个可运行框架，并用若干单例文本分析说明这些指标能够产出可解释的风格/氛围报告。

## Link
- [https://github.com/xraymemory/vibetheory](https://github.com/xraymemory/vibetheory)
