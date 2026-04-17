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
这篇论文是一篇综述，核心观点是：当前 LLM 智能体的进展，主要来自把关键负担从模型权重转移到运行时基础设施中。论文用一个统一视角概括了这一转变的四个部分：记忆、技能、协议，以及协调它们的 harness。

## 问题
- 当长期状态、可重复执行的流程，以及与工具或其他智能体的可靠协作仍然留在提示词和模型权重内部时，LLM 智能体在这些方面能力较弱。
- 现有研究常常分别讨论记忆、工具使用、智能体协议或系统架构，这使得人们难以解释为什么这些方向会在实际系统中逐渐汇合。
- 这一点很重要，因为许多已部署智能体的性能提升来自模型外围的系统设计，尤其是在软件工程、工作流自动化和多智能体执行这类长时程任务中。

## 方法
- 论文通过 **externalization（外化）** 这一概念给出统一综述：把认知负担转移到模型可以查询或遵循的外部显式构件中。
- 它将外化分为三部分：用于跨时间保存状态的 **memory（记忆）**、用于复用流程的 **skills（技能）**，以及用于与工具、服务、用户和其他智能体进行结构化交互的 **protocols（协议）**。
- 论文将 **harness engineering** 定义为运行时层，用控制逻辑、约束、可观测性、审批回路和恢复机制来编排这些部分。
- 它把该领域的历史概括为 **weights -> context -> harness** 的转变，即能力先体现在模型参数中，随后转向提示词/上下文设计，再转向持久化基础设施。
- 它用 RAG、ReAct、AutoGen、MetaGPT、SWE-agent 和 OpenHands 等已有系统作为例子，说明外部模块如何改变模型实际需要解决的任务。

## 结果
- 这是一篇综述论文。给出的摘录 **没有提供新的基准结果或实验指标**。
- 论文的主要主张是概念性的：可靠的智能体行为，越来越少依赖修改模型权重，越来越多依赖将三类负担外化，即把连续性放到记忆中、把流程放到技能中、把协调放到协议中。
- 它认为，harness 是把这些模块整合起来的运行时层，并通过编排、验证、沙箱、可观测性和反馈回路让它们在实际中可用。
- 它认为，智能体系统中最强的实际收益往往来自基础设施层面的变化，例如持久记忆、工具注册表、协议化接口和多步编排，而不只是更换一个新的基础模型。
- 它指出了一些开放问题，包括评估、治理、参数化能力与外化能力之间的权衡，以及未来方向，如自演化 harness 和共享智能体基础设施。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.08224v1](http://arxiv.org/abs/2604.08224v1)
