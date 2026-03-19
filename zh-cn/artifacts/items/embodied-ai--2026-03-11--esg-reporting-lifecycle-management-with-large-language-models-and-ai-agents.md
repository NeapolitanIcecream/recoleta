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
- esg-reporting
- llm-agents
- multi-agent-systems
- retrieval-augmented-generation
- compliance-checking
relevance_score: 0.01
run_id: materialize-outputs
language_code: zh-CN
---

# ESG Reporting Lifecycle Management with Large Language Models and AI Agents

## Summary
本文提出一个面向ESG报告全生命周期的LLM/AI代理框架，把原本静态、人工主导的ESG披露流程改造成可自动化、可解释、可持续迭代的系统。论文还给出单模型、单代理和多代理三种实现架构，并用报告合规校验原型进行案例评估。

## Problem
- ESG报告数据来源高度异构，常见于表格、叙述、扫描文档、图表等形式，自动抽取和统一处理困难。
- 同一ESG指标在GRI、SASB、TCFD等多标准中的定义和披露要求不同，导致跨标准对齐与合规验证复杂。
- 现有ESG生命周期框架多为特定领域设计，缺少自动化与持续反馈机制，难以支持频繁更新的监管要求和持续改进。

## Approach
- 提出一个**五阶段**的agentic ESG lifecycle：identification、measurement、reporting、engagement、improvement，使ESG流程形成闭环反馈。
- 为每个阶段设计专门代理：ESIA负责标准/指标识别，EDIA负责数据抽取与规范化，ECA负责报告生成与可视化，ESEA负责利益相关方沟通，EPIA负责风险评估与持续改进。
- 将LLM作为核心推理组件，并结合角色提示、多步提示、比较提示等机制，把复杂任务拆成更易执行的子任务。
- 定义四类关键任务：报告验证与合规检查、多报告比较、自动报告生成、ESG知识库维护；并提出准确性、可解释性、faithfulness、模块化、容错等质量属性。
- 给出三种系统架构：single-model（一个LLM包办全部任务）、single-agent（LLM+RAG+外部工具）、multi-agent（每个任务一个专门代理，代理间交换结果）。

## Results
- 论文完成了**13份ESG报告**的人工结构化分析，并将披露内容映射到**GRI、SASB、TCFD**三类标准，用于发现多标准对齐和异构格式两大核心难点。
- 案例研究实现了**3种原型架构**（single-model、single-agent、multi-agent），聚焦**报告验证与合规检查**任务，并以**人工核验**作为基线。
- 论文明确说明比较维度包括**accuracy、computational cost、energy consumption**三项指标。
- 但在给定摘录中，**没有提供这三种架构的具体定量结果**，因此无法报告准确率、成本或能耗的数值对比。
- 最强的实证性主张是：作者不仅提出概念框架，还落地了可运行原型，并公开了**source code and data**以支持复现。

## Link
- [http://arxiv.org/abs/2603.10646v1](http://arxiv.org/abs/2603.10646v1)
