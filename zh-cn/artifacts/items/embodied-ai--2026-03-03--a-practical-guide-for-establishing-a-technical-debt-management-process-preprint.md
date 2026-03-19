---
source: arxiv
url: http://arxiv.org/abs/2603.03085v1
published_at: '2026-03-03T15:28:50'
authors:
- Marion Wiese
- Kamila Serwa
- Eva Bittner
topics:
- technical-debt
- software-engineering
- process-guideline
- action-research
- backlog-management
relevance_score: 0.01
run_id: materialize-outputs
language_code: zh-CN
---

# A Practical Guide for Establishing a Technical Debt Management Process (Preprint)

## Summary
本文通过跨3个团队的行动研究，总结了如何在企业中落地技术债务管理（TDM）流程，并提炼出可复用的最佳实践起点。核心价值不在提出新算法，而在把分散的TDM研究方法转化为可执行的组织流程与实施指南。

## Problem
- 软件团队常会采用短期有利、长期增加维护成本的技术债务做法；若没有系统化管理，后续改动会更慢、更贵、更风险化。
- 现有TDM研究很多，但缺少跨公司可迁移的统一落地指南，实践团队难以知道该先做什么、用哪些方法、如何持续执行。
- 论文还关注一个关键问题：建立TDM流程后，团队对技术债务的“意识”是否真的提升，因为这直接影响日常决策质量。

## Approach
- 采用**行动研究 + 5步工作坊**方法，在3个团队中复制和比较TDM落地过程；团队可从研究文献中给出的候选做法里自行选择要采用的方案。
- 全研究覆盖**15次工作坊 + 4次回顾**，观察**108场会议、96小时**，周期**30个月**；共分析**1132个被讨论的事项**，并收集**240份TD-SAGAT意识测量数据**。
- 方法上围绕多个TDM活动展开：技术债务识别、记录、优先级、偿还、预防与可视化，并比较哪些做法在不同公司里都被接受。
- 提炼出的共通机制很简单：给团队设定**TD champion/manager**，在现有backlog里加入专门的TD条目类型，记录如**interest、contagiousness、resubmission date**等属性，并在决策时强制讨论**备选方案、缺点和风险**。
- 同时用TD-SAGAT和观察法跟踪“技术债务意识”变化，判断流程建立是否真正改变了团队的讨论与决策习惯。

## Results
- 论文声称识别出一组跨团队都采用的TDM最佳实践起点：**(1)** 设立TD champion/manager，**(2)** 用带具体属性的TD backlog项记录债务，**(3)** 在决策时评估替代方案及其缺点/风险，**(4)** TD优先级主要与其他TD项比较而不是直接和功能需求比较，**(5)** 使用**resubmission date**做延期复查。
- 三个团队在记录与预防策略上高度相似：都复用了各自现有backlog，并新增TD issue type；共同使用的属性包括**interest、contagiousness、resubmission date**及提醒讨论缺点/风险等字段。
- 研究规模上的主要量化结果是：覆盖**3个团队**、**30个月净研究期（43个月毛跨度）**、**108场会议 / 96小时**、**1132个讨论事项**、**28次TD-SAGAT中断测量**、**240份回答**，用于支撑其流程建议的可行性结论。
- 关于效果，作者给出的最强具体结论是：**技术债务意识总体只会在相关属性被加入issue type并作为持续提醒时上升**。但摘录中**没有提供明确的前后提升百分比、统计显著性或基线对比数值**。
- 论文还总结了多团队重复出现的落地难点：团队需要更具体的操作支持、简单的backlog识别方法、启动流程的指导、初期的外部提醒机制，以及帮助成员更好表述TD后果的支持。
- 最终产出除了研究结论，还包括一个面向实践者的**白皮书/指南**，并建议issue tracking工具厂商原生支持TD issue type及其属性。

## Link
- [http://arxiv.org/abs/2603.03085v1](http://arxiv.org/abs/2603.03085v1)
