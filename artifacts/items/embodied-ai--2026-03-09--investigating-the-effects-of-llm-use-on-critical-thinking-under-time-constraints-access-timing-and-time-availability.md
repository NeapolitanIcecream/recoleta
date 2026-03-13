---
source: arxiv
url: http://arxiv.org/abs/2603.08849v1
published_at: '2026-03-09T19:05:25'
authors:
- Jiayin Zhi
- Harsh Kumar
- Mina Lee
topics:
- llm-evaluation
- critical-thinking
- human-ai-collaboration
- time-pressure
- hci-experiment
relevance_score: 0.02
run_id: materialize-outputs
---

# Investigating the Effects of LLM Use on Critical Thinking Under Time Constraints: Access Timing and Time Availability

## Summary
这篇论文研究LLM会在什么时间点帮助或损害批判性思维，而不是简单问“用不用LLM”。作者通过一项受控实验发现，LLM的效果与时间压力强烈交互：赶时间时越早用越有利，时间充足时反而先独立思考更好。

## Problem
- 论文要解决的问题是：**LLM究竟会提升还是削弱人的批判性思维表现**，以及这种影响是否取决于**时间压力**与**LLM接入时机**。
- 这很重要，因为现实中的推理与决策任务常常既有截止时间，又越来越多地嵌入LLM；如果忽略时间因素，就可能错误评估人机协作的利弊。
- 以往研究多依赖自我报告，或只比较“有/无LLM”，缺少对**真实表现**和**时间条件交互作用**的系统实验。

## Approach
- 作者进行了一个**4×2组间实验**（n=393），同时操纵两类时间因素：LLM接入时机（early、continuous、late、no-llm）和任务时间是否充足（10分钟 insufficient vs 30分钟 sufficient）。
- 任务采用iPAL批判性思维表现评估：参与者阅读一组关于现实公共决策场景的多源文档，写出有理有据的决策短文，而不是做简单选择题。
- 最核心机制可以用最简单的话概括为：**看人在赶时间或不赶时间时，是先自己想，还是一开始就让LLM介入，会不会改变最终推理质量**。
- 主要评估Essay表现，并补充测量Recall、Evaluation、Comprehension，以及任务后的自我评估，以观察LLM可能影响的认知环节。

## Results
- 论文声称出现了一个**“时间上的反转效应”**：在**时间不足**时，**early/continuous** LLM接入提升批判性思维Essay表现；但在**时间充足**时，模式反转，**late/no-llm** 更好。
- 在**sufficient time** 条件下，**从一开始就能用LLM（early/continuous）** 还会损害**Recall**，作者据此认为早期依赖LLM可能妨碍对文档内容的内化。
- 对同一接入方式比较时间长短时，**充足时间**显著提升了**late/no-llm** 组的Essay和Recall，但对**early/continuous** 组帮助很小，说明“更多时间”并不总能与“更早AI辅助”叠加。
- 任务后的**自我评估几乎不随条件变化**，表明人们未必能准确感知LLM对自己批判性思维的真实影响。
- 量化信息方面，摘要与给定摘录明确提供了**样本量 n=393**、**4×2设计**、**10分钟 vs 30分钟**、**4种接入时机**；但摘录**没有给出具体效应值、均值、p值或相对基线提升百分比**，因此无法报告更细的数值比较。

## Link
- [http://arxiv.org/abs/2603.08849v1](http://arxiv.org/abs/2603.08849v1)
