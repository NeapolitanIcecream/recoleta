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
- survey
- safety-critical-systems
relevance_score: 0.36
run_id: materialize-outputs
language_code: zh-CN
---

# Robotic Foundation Models for Industrial Control: A Comprehensive Survey and Readiness Assessment Framework

## Summary
这篇综述聚焦机器人基础模型（RFM）在工业控制中的可部署性，不是提出新模型，而是系统评估“当前RFM离工业可用还有多远”。作者给出一套面向工业落地的成熟度评估框架，并用它对大规模RFM文献与模型进行保守、可审计的比较。

## Problem
- 现有RFM研究常强调基准测试成功，但缺少针对**工业场景**的系统性评估，难以判断模型是否真的适合安全、实时、低成本的工厂部署。
- 工业机器人，尤其协作机器人，需要模型同时满足**安全性、低延迟、稳健感知、跨硬件适配、边缘计算约束**等多重要求；单点能力强并不等于可落地。
- RFM论文数量近年快速增长，若没有统一框架，领域容易出现**碎片化与夸大性结论**，不利于研究与产业对齐。

## Approach
- 作者从工业部署视角出发，先对机器人控制方法做分层，并给出RFM定义：必须具备**多模态输入、灵活输出、跨任务/跨具身适应性**的“generalist core”。
- 他们将工业需求综合为**11个相互依赖的deployment implications**，再细化为一个包含**149项具体标准**的评估目录，覆盖模型能力与生态系统要求。
- 为构建综述语料，作者使用自动化检索与LLM辅助筛选流程：两轮大规模检索共得到**10,728**与**12,027**条有效记录，合并后形成**6,497**篇唯一文章；经筛选后得到**1,025**篇高相关文献。
- 在模型评估上，作者用一个**保守的LLM辅助评审流程**，并以专家判断做校验，对**324个具操作能力的RFM**进行逐项打分，共形成**48,276**个criterion-level decisions。

## Results
- 论文的核心结论是：当前RFM的**工业成熟度有限且分布不均**；即使评分最高的模型，也只满足**149项标准中的一部分**，没有模型展现出对工业关键需求的全面覆盖。
- 评估规模方面，作者声称这是一次较大规模、可追踪的工业成熟度分析：**324**个manipulation-capable RFMs，**149**项标准，合计**48,276**次标准级判断。
- 文献综述规模上，最终主语料包含**1,025**篇高相关论文，其中包括**341**个control或integrated RFMs；其中**324**个聚焦manipulation / mobile manipulation / 通用机器人任务，另有**17**个面向其他具身或领域。
- 检索过滤流程显示领域增长很快：两次检索分别得到**10,728/12,027**条有效记录；合并去重后为**6,497**篇，先筛到**4,834**篇机器人相关，再筛到**1,408**篇RFM相关，最终人工整理为**1,025**篇。
- 文中**没有提供传统意义上单一模型SOTA准确率/成功率提升**这类实验数字；最强的实证主张是：现有模型通常只在少数工业含义维度上出现“局部峰值”，距离兼顾**安全、实时性、稳健感知、交互与成本集成**的industry-grade RFM仍有明显差距。

## Link
- [http://arxiv.org/abs/2603.06749v1](http://arxiv.org/abs/2603.06749v1)
