---
source: arxiv
url: http://arxiv.org/abs/2604.08224v1
published_at: '2026-04-09T13:19:41'
authors:
- Chenyu Zhou
- Huacan Chai
- Wenteng Chen
- Zihan Guo
- Rong Shan
- Yuanyi Song
- Tianyi Xu
- Yingxuan Yang
- Aofan Yu
- Weiming Zhang
- Congming Zheng
- Jiachen Zhu
- Zeyu Zheng
- Zhuosheng Zhang
- Xingyu Lou
- Changwang Zhang
- Zhihui Fu
- Jun Wang
- Weiwen Liu
- Jianghao Lin
- Weinan Zhang
topics:
- llm-agents
- agent-infrastructure
- memory-systems
- tool-protocols
- multi-agent-systems
- software-engineering-agents
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Externalization in LLM Agents: A Unified Review of Memory, Skills, Protocols and Harness Engineering

## Summary
## 摘要
这篇论文是一篇综述，主张当前 LLM agent 的进展来自把关键负担从模型权重移到运行时基础设施中。它把这种转移统一为四个部分：记忆、技能、协议，以及负责协调它们的 harness。

## 问题
- 当长期状态、可重复流程和与工具或其他 agent 的可靠协同仍留在提示词和模型权重里时，LLM agent 在这些方面表现较弱。
- 现有工作常把记忆、工具使用、agent 协议或架构分开研究，这让人很难解释这些方向为什么会在实际系统中汇合。
- 这很重要，因为很多已部署 agent 的收益来自围绕模型的系统设计，尤其是在软件工程、工作流自动化和多 agent 执行等长周期任务中。

## 方法
- 论文用 **外化** 这个概念做统一综述：把认知负担移到显式的外部工件中，让模型可以查询或遵循这些工件。
- 它把外化分成三部分：**记忆** 负责跨时间保存状态，**技能** 负责可复用的流程，**协议** 负责与工具、服务、用户和其他 agent 的结构化交互。
- 它把 **harness 工程** 定义为运行时层，用控制逻辑、约束、可观测性、审批环路和恢复机制来编排这些部分。
- 它把这个领域的历史概括为从 **weights -> context -> harness** 的转变，能力从模型参数转向提示词/上下文设计，再转向持久基础设施。
- 它用 RAG、ReAct、AutoGen、MetaGPT、SWE-agent 和 OpenHands 等先前系统的例子说明外部模块如何改变模型要解决的任务。

## 结果
- 这是一篇调查/综述论文。摘要没有提供**新的基准数值或实验指标**。
- 主要结论是概念性的：可靠的 agent 行为更少来自改动模型权重，更来自把三类负担外化出去，即把连续性放进记忆，把流程放进技能，把协同放进协议。
- 论文认为 harness 是整合这些模块的运行时层，通过排序、验证、沙箱隔离、可观测性和反馈环路让它们在实践中可用。
- 论文认为，agent 系统里最强的实际收益往往来自基础设施改动，比如持久记忆、工具注册表、协议化接口和多步编排，而不只是换一个新的基础模型。
- 论文还指出了评估、治理、参数化能力与外化能力之间的权衡，以及自演化 harness 和共享 agent 基础设施等未来方向。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.08224v1](http://arxiv.org/abs/2604.08224v1)
