---
source: arxiv
url: http://arxiv.org/abs/2603.10646v1
published_at: '2026-03-11T11:05:58'
authors:
- Thong Hoang
- Mykhailo Klymenko
- Xiwei Xu
- Shidong Pan
- Yi Ding
- Xushuo Tang
- Zhengyi Yang
- Jieke Shi
- David Lo
topics:
- llm-agents
- multi-agent-systems
- esg-reporting
- rag
- compliance-automation
relevance_score: 0.74
run_id: materialize-outputs
---

# ESG Reporting Lifecycle Management with Large Language Models and AI Agents

## Summary
本文提出一个面向ESG报告全生命周期的LLM与AI代理框架，把原本静态、人工密集的合规报告流程变成可自动化、可反馈迭代的系统。论文同时给出单模型、单代理和多代理三种实现思路，并以报告校验任务做原型验证。

## Problem
- ESG报告数据来源**非结构化且异构**，如表格、叙述、扫描件和图表，导致自动抽取与比对困难。
- 不同标准（如GRI、SASB、TCFD）对**同一指标有不同解释与要求**，多标准对齐复杂，人工成本高。
- 现有ESG生命周期框架**缺少自动化、跨领域适应性和持续反馈机制**，难以应对监管频繁变化与持续改进需求。

## Approach
- 提出一个**五阶段 agentic ESG lifecycle**：identification、measurement、reporting、engagement、improvement，用于覆盖从标准识别到持续优化的闭环流程。
- 为每个阶段设计专门代理：ESIA解释标准与识别指标，EDIA抽取/规范化/校验数据，ECA生成并对齐报告，ESEA处理利益相关方反馈，EPIA做风险评估与持续改进。
- 将**LLM提示策略**嵌入各阶段，结合角色提示、多步提示、比较提示、报告生成提示等，以最简单方式说，就是“让不同AI助手各自负责一类ESG工作，并把结果传给下一个助手”。
- 提出三种系统架构：**single-model**（一个LLM全做）、**single-agent**（一个代理+RAG+外部工具）、**multi-agent**（多个专职代理协作）；其中后两者以RAG支撑知识库、可解释性与忠实性。
- 定义四类核心任务：报告校验与合规检查、多报告比较、自动生成报告、ESG知识库维护，并给出质量属性，如准确性、可扩展性、容错性、可解释性和answer faithfulness。

## Results
- 论文进行了**13份ESG报告**的人工分析，并将其映射到**GRI、SASB、TCFD**三类标准，用于识别多标准对齐与异构格式两大核心挑战。
- 原型系统覆盖了**3种架构**（single-model、single-agent、multi-agent），并聚焦**1个案例任务**：ESG报告验证与合规检查。
- 评估声明比较了**3个指标**：accuracy、computational cost、energy consumption；**人工手动验证**被设为基线。
- 但在给定摘录中，**没有提供具体定量结果数值**，因此无法报告各架构相对基线的准确率提升、成本下降或能耗差异。
- 最强的具体主张是：该框架把ESG报告从静态披露流程转为**动态、可问责、可自适应**的治理系统，并通过多代理分工提升自动化、可解释性与持续改进能力。

## Link
- [http://arxiv.org/abs/2603.10646v1](http://arxiv.org/abs/2603.10646v1)
