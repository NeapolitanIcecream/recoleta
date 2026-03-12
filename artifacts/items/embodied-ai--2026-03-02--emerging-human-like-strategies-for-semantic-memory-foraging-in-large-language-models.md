---
source: arxiv
url: http://arxiv.org/abs/2603.01822v1
published_at: '2026-03-02T12:55:51'
authors:
- Eric Lacosse
- Mariana Duarte
- Peter M. Todd
- Daniel C. McNamee
topics:
- mechanistic-interpretability
- large-language-models
- semantic-memory
- cognitive-alignment
- logit-lens
relevance_score: 0.03
run_id: materialize-outputs
---

# Emerging Human-like Strategies for Semantic Memory Foraging in Large Language Models

## Summary
本文研究大语言模型在语义流畅性任务中的“语义记忆觅食”是否呈现类似人类的聚类与切换策略。作者用机制可解释性方法发现，这些收敛/发散模式不仅出现在模型输出中，也能在中后层内部表征中被读出。

## Problem
- 论文要解决的问题是：**LLM 在从语义记忆中检索概念时，是否使用了可识别的、类似人类的搜索策略**，尤其是语义流畅性任务中的“聚类（convergent）”与“切换（divergent）”。
- 这很重要，因为如果能定位这些机制，就能更严谨地理解 LLM 与人类认知是“对齐”还是“表面相似但机制不同”，并为后续行为引导与表示工程提供基础。
- 这也关联到机制可解释性中的核心问题：模型内部哪些层和表征真正支持了这类看似“认知式”的行为。

## Approach
- 作者采用经典的 **Semantic Fluency Task (SFT)**：让人或模型连续说出尽可能多的动物名，并用类别规范把连续词对标注为“同类延续”（non-switch / convergent）或“跨类切换”（switch / divergent）。
- 数据上，比较 **699 条人类序列** 与 **Llama-3 系列（1B/3B/8B/70B）生成的等量任务序列**；过滤后分析了 **681 条人类序列** 和 **2285 条 LLM 序列**。
- 在输出层面，作者把词表划分为“当前类别内 token 集”和“跨类别 token 集”，观察切换事件前后两类 token 概率质量如何变化，并用 **logit lens** 追踪这种差异在各层何时出现。
- 在表示层面，作者对残差流做 **PCA + logistic regression probe**，测试是否能从中间层激活直接判别 switch vs. non-switch；同时构造中性、收敛、发散三类对比提示数据以增强机制读出。

## Results
- 人类与 LLM 的类别转移矩阵高度相关：**Spearman ρ = 0.701, p < 0.001**，说明两者在总体语义搜索模式上相似。
- 但 LLM 比人类更少切换类别：人类平均 **switch ratio = 0.55**，LLM 平均 **0.40**，且差异显著（**Mann-Whitney p < 0.0001**）；作者据此认为 LLM 更倾向于更彻底地“榨干”同一语义簇。
- 在 70B 模型上，切换点附近的输出分布显著变化：从相对位置 -1 到 0，**within-category d = -0.158**、**between-category d = 0.144**、**actual sequence d = -0.184**，**均 p < 0.001**，说明切换发生时模型对“跨类词”的相对偏好上升。
- logit lens 显示区分 switch / non-switch 的信号在**中后层（约 layer > 40）**明显出现；晚层中，非切换时 **within-category prob = 0.0035**、**between-category prob = 0.0005**，而切换时变为 **0.0008 vs. 0.0007**，仍有显著差异（**Mann-Whitney, p < 0.001**）。
- 仅用真实人类序列的残差流表示做线性探针时，效果较弱：**AUROC = 0.57**（Llama-3.3-70B）；而用输出分布做分类可达 **AUROC = 0.751**。
- 在作者构造的对比式提示数据上，残差流中的切换机制可被强力读出：70B 模型在线性探针下达到 **AUROC = 0.96（neutral）/ 0.98（convergent）/ 0.97（divergent）**；同时，模型越大，读出性能总体越高。

## Link
- [http://arxiv.org/abs/2603.01822v1](http://arxiv.org/abs/2603.01822v1)
