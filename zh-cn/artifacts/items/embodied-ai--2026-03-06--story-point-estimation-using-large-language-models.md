---
source: arxiv
url: http://arxiv.org/abs/2603.06276v1
published_at: '2026-03-06T13:34:09'
authors:
- Pranam Prakash Shetty
- Adarsh Balakrishnan
- Mengqiao Xu
- Xiaoyin Xi
- Zhe Yu
topics:
- software-effort-estimation
- story-point-estimation
- large-language-models
- few-shot-learning
- software-engineering
relevance_score: 0.03
run_id: materialize-outputs
language_code: zh-CN
---

# Story Point Estimation Using Large Language Models

## Summary
本文研究大语言模型是否能在几乎没有项目标注数据时完成敏捷开发中的故事点评估。结论是：零样本LLM已经能超过需用80%训练数据的监督式深度学习基线，而少量示例还能进一步提升效果。

## Problem
- 要解决的是**敏捷软件开发中的故事点评估**自动化问题：根据任务标题和描述预测开发工作量。
- 这很重要，因为人工估点主观、耗时、难扩展；而现有监督模型通常需要**同一项目大量带标签历史数据**，在新项目或冷启动场景不实用。
- 论文还问了一个相关问题：相比直接给故事点，**成对比较哪个任务更费力**是否更容易让LLM学习，并能否作为更省人力的少样本监督信号。

## Approach
- 在 **16 个真实软件项目**上评测 **4 个现成LLM**（Kimi、DeepSeek、Gemini Flash Lite、OpenAI GPT-5 Nano），输入是 backlog item 的标题+描述。
- 设计四类实验：**零样本故事点预测**、**少样本故事点预测**、**零样本成对比较判断**、以及**用少量成对比较示例来辅助故事点预测**。
- 少样本设置每个项目只给 **5 个示例**，并比较两种选样策略：按高频故事点取样（Count）与按数值范围覆盖取样（Scale）。
- 评估指标主要是故事点预测与真值的 **Pearson 相关系数 ρ**、**Spearman 等级相关 rs**；成对比较任务用 **accuracy**。
- 输出端采用严格提示+JSON解析+正则回退，以稳定提取LLM返回的整数故事点或二元比较决策。

## Results
- **零样本已优于监督基线**：在 16 个项目平均上，监督基线 SBERT regression（用 **80%** 项目数据训练）的 **ρ=0.3175**；而零样本 **Kimi ρ=0.3735**、**DeepSeek ρ=0.4040**，均更高；Gemini 为 **0.2363**，OpenAI 为 **0.2712**。比较判断基线列出的 supervised comparative 为 **ρ=0.3337**，DeepSeek 和 Kimi 也超过它。
- 在 **Spearman rs** 上，论文给出的项目级结果同样显示 Kimi/DeepSeek 普遍强于传统监督基线；例如 **clover** 项目中，SBERT regression **rs=0.4166**，Kimi **0.5043**，DeepSeek **0.6358**。
- 若看单项目的 **Pearson ρ**，DeepSeek 在多个项目上明显领先，例如 **clover 0.8364 vs 监督回归 0.4403**，**bamboo 0.3479 vs 0.1768**，**titanium 0.4038 vs 0.1861**，说明某些项目里零样本LLM提升很大。
- 论文声称**少样本提示会进一步提升**零样本表现，只需极少示例即可更好地校准项目内故事点尺度；并且**比较判断示例也能提升故事点预测**。但在给定摘录中，RQ2/RQ4 的完整量化表格未提供，因此无法逐项列出平均提升数值。
- 对“比较判断是否更容易”这一点，作者的结论是**并不比直接估故事点更容易**；也就是说，LLM在pairwise判断上没有明显天然优势。
- 最强的整体结论是：**无需标注数据即可达到甚至超过传统监督方法，而只用少量示例还能更进一步**；这使LLM特别适合**数据稀缺/冷启动**的软件项目估算场景。

## Link
- [http://arxiv.org/abs/2603.06276v1](http://arxiv.org/abs/2603.06276v1)
