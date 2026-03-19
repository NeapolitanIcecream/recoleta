---
source: arxiv
url: http://arxiv.org/abs/2603.10864v1
published_at: '2026-03-11T15:16:58'
authors:
- Martin Obaidi
- Marc Herrmann
- Jendrik Martensen
- "Jil Kl\xFCnder"
- Kurt Schneider
topics:
- sentiment-analysis
- software-engineering
- developer-communication
- longitudinal-study
- human-factors
relevance_score: 0.28
run_id: materialize-outputs
language_code: zh-CN
---

# Exploring Indicators of Developers' Sentiment Perceptions in Student Software Projects

## Summary
这篇论文研究学生软件项目中，开发者为何会对同一条文本消息产生不同情绪判断，并考察这种判断如何随时间、情绪和团队因素变化。核心结论是：情绪感知在个体内部并不稳定，且更受具体语句歧义影响，而非明显受项目阶段驱动。

## Problem
- 软件团队中的文本沟通会影响协作氛围与情绪传播，但同一句话常被不同开发者、甚至同一开发者在不同时间，理解为正面、负面或中性。
- 现有软件工程中的情感分析研究多是静态、横截面标注，较少研究**同一人**的感知是否随时间变化，以及情绪、生活状态、冲突、项目阶段等因素是否相关。
- 这很重要，因为如果情绪感知本身高度主观且波动，自动情感分析工具的输出就可能被过度解读，进而误判团队氛围。

## Approach
- 作者进行了一项**四轮纵向问卷研究**，对象是 **81 名学生开发者**，来自团队式软件项目课程；课程整体涉及 **204 名学生、28 个项目团队**。
- 每轮中，参与者对 **30 条去上下文化的开发者语句**做三分类标注：positive / neutral / negative；这些语句来自 GitHub 与 Stack Overflow 数据集，且正/中/负类别做了均衡抽样。
- 同时收集多类解释变量：长期情绪特质（mood trait）、情绪反应性（reactivity）、短期情绪状态（PANAS）、生活满意度、团队关系/任务冲突、项目阶段，以及标注理由、置信度和不确定性原因。
- 分析上先看个体内稳定性与相关性，再使用**GEE 重复测量模型**在语句层面分析哪些因素会让参与者更可能把一条语句标成正面、负面或中性。

## Results
- 研究包含 **4 轮**调查、**81 名**参与者、每轮 **30 条**语句；这使其能够观察同一开发者随时间的标签变化。
- 作者明确报告：**个体内情绪感知只有中等稳定性**，且标签变化主要集中在**容易产生歧义的语句**上；说明“语句本身”是强影响因素。
- 相关性层面的信号总体**很小**，并且在做**全局多重检验校正后不再显著**；也就是说，很多表面相关并不稳健。
- 在 **GEE 语句级重复测量模型**中，**更高的 mood trait 和 reactivity**与**更偏向正面、较少标为中性**相关；而**负面标注的预测因素较弱**，最多只有趋势级证据，例如**task conflict**。
- 对外部情境因素，论文称**没有发现明确的系统性项目阶段效应**；即临近截止或项目后期并未显示出稳定改变感知的强证据。
- 论文摘要与引言**未提供具体效应大小、准确率、p 值或基线提升数字**；最强的定量事实主要是样本与设计规模（81 人、4 轮、30 句），以及“多重校正后不显著”“效应小”“中等稳定性”等结论性表述。

## Link
- [http://arxiv.org/abs/2603.10864v1](http://arxiv.org/abs/2603.10864v1)
