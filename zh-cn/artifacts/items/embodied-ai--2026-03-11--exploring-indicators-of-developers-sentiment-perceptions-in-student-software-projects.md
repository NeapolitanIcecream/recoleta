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
- team-dynamics
relevance_score: 0.01
run_id: materialize-outputs
language_code: zh-CN
---

# Exploring Indicators of Developers' Sentiment Perceptions in Student Software Projects

## Summary
这篇论文研究学生软件项目中，开发者对同一句文本情感是如何随时间和个人/团队因素变化的。结论是情感感知并不稳定，更多取决于语句本身的歧义，而非强而稳定的个体或项目阶段效应。

## Problem
- 它要解决的问题是：开发者为什么会把同一条书面消息看成积极、消极或中性，以及这种判断是否会随时间改变。
- 这很重要，因为沟通中的情感误读会影响协作、团队氛围和对软件工程情感分析工具输出的信任。
- 以往研究多是静态、横截面标注；缺少对同一人纵向变化，以及情绪、生活状态、冲突、项目阶段等因素的系统分析。

## Approach
- 作者进行了一个**四轮纵向问卷研究**，对象是 81 名参与团队软件项目的计算机专业学生；更大课程背景中共有 204 名学生、28 个团队项目。
- 在每一轮中，参与者对 **30 条去上下文化的开发者语句**标注为 positive / neutral / negative；语句来自 GitHub 和 Stack Overflow 数据集，且正中负大致均衡。
- 同时收集多类自报告变量：长期情绪特质、情绪反应性、短期情绪状态（PANAS）、生活满意度、团队关系冲突与任务冲突、以及项目阶段。
- 分析上既看个体内稳定性与相关性，也使用**GEE 重复测量模型**在语句层面分析哪些因素会推动更积极/更中性/更消极的标注。
- 还记录标注理由、信心与不确定性来源，用于解释哪些语句更容易引发感知变化。

## Results
- 研究基于 **81 名学生、4 轮调查、每轮 30 条语句** 的纵向设计；作者明确称情感感知在个体内只有**中等稳定性**，且标签变化主要集中在**歧义较高的语句**上。
- 相关性层面的信号总体**很小**，并且在进行**全局多重检验校正后均未保留显著性**；论文摘录未给出具体相关系数数值。
- 在语句级 **GEE 重复测量模型**中，**更高的情绪特质和更高的情绪反应性**与**更倾向于标为 positive、较少标为 neutral**相关。
- 对 **negative** 标注的预测因素更弱，最多只有**趋势级**发现；文中举例为**任务冲突**可能与更负面的标注有关，但证据不强。
- 作者称**没有清晰证据**表明项目阶段会系统性影响情感感知。
- 量化结果在摘录中较少：能明确提取的数字主要是**4 轮、81 名参与者、30 条语句**；未提供诸如准确率、效应量、p 值或相对基线提升等更详细指标。

## Link
- [http://arxiv.org/abs/2603.10864v1](http://arxiv.org/abs/2603.10864v1)
