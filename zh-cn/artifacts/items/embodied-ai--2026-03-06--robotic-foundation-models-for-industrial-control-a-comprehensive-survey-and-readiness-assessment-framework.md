---
source: arxiv
url: http://arxiv.org/abs/2603.06749v1
published_at: '2026-03-06T11:23:00'
authors:
- David Kube
- Simon Hadwiger
- Tobias Meisen
topics:
- robotic-foundation-models
- industrial-robotics
- readiness-assessment
- vision-language-action
- manipulation
- survey
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# Robotic Foundation Models for Industrial Control: A Comprehensive Survey and Readiness Assessment Framework

## Summary
这是一篇面向工业控制场景的机器人基础模型（RFM）综述，不是提出新模型，而是系统评估现有RFM距离工业落地还有多远。论文的核心价值在于把“工业可部署性”具体化为可审计的评估框架，并据此大规模分析当前模型生态。

## Problem
- 现有RFM/VLA研究常强调基准成绩，但缺少从**工业部署**视角出发的系统性审查，尤其是安全、实时性、异构硬件、边缘计算和系统集成等要求。
- 工业机器人，特别是协作机器人，需要可指令、可迁移、低工程成本的通用控制能力；但学术进展不等于可直接进入工厂。
- 文献增长极快，容易出现碎片化与夸大结论，因此需要一个可复用、可追踪的成熟度评估框架来判断RFM是否真正具备产业准备度。

## Approach
- 论文先从工业需求出发，重新界定RFM：要求具备**通用核心能力**，能跨任务/跨 embodiment 适配，并具备多模态输入与灵活输出，而不仅是单一感知或单一控制模块。
- 作者将工业部署需求归纳为**11个相互依赖的影响维度**，并把这些维度操作化为一个包含**149项具体标准**的评估目录，覆盖模型能力与生态系统要求。
- 他们建立了标准化文献获取与筛选流程：通过自动化数据库检索、LLM辅助过滤和人工复核，整理RFM相关文献与模型谱系。
- 在评估阶段，作者使用一个**保守的LLM辅助判定流程**，并用专家判断进行验证，对**324个具备操作能力的RFM**进行逐条标准打分。
- 最终形成一个大规模、面向工业成熟度的横向比较，而不是仅按模型架构或单一benchmark分类。

## Results
- 论文声称完成了对**324个 manipulation-capable RFMs**的工业成熟度评估，总计产生了**48,276条 criterion-level decisions**。
- 评估框架本身包含**11个工业部署影响维度**和**149项具体标准**，覆盖的不只是模型能力，也包括部署生态要求。
- 文献构建方面，主语料最终整理出**1,025篇**高相关论文，其中包括**341个 control/integrated RFMs**；其中**324个**聚焦操作、移动操作或通用机器人场景。
- 两轮大规模检索共得到**10,728**和**12,027**条有效文章记录，合并去重后得到**6,497**篇唯一条目；经两阶段过滤后保留**1,408**篇，再经人工精炼得到最终语料。
- 核心结论是：**工业成熟度整体“有限且不均衡”**；即便评分最高的模型也只满足**一部分**标准，通常只在少数维度上突出，而非全面覆盖工业所需能力。
- 文中未在给定摘录中提供各模型的具体平均分、榜单数值或相对某个baseline的百分比提升；最强的定量主张是其评估规模（324模型、149标准、48,276次判定）以及“当前尚无真正 industry-grade RFM”的总体结论。

## Link
- [http://arxiv.org/abs/2603.06749v1](http://arxiv.org/abs/2603.06749v1)
