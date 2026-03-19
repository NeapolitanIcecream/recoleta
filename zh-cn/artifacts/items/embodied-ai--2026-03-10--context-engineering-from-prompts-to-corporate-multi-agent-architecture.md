---
source: arxiv
url: http://arxiv.org/abs/2603.09619v1
published_at: '2026-03-10T12:58:31'
authors:
- Vera V. Vishnyakova
topics:
- context-engineering
- ai-agents
- multi-agent-systems
- enterprise-ai
- ai-governance
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# Context Engineering: From Prompts to Corporate Multi-Agent Architecture

## Summary
本文提出“上下文工程”作为面向企业级AI代理与多代理系统的独立工程学科，主张单靠提示工程无法支撑长链路、自主执行、可治理的生产级代理。作者进一步扩展到“意图工程”和“规范工程”，形成一个四层代理工程成熟度金字塔。

## Problem
- 论文要解决的是：当LLM从单轮问答组件变成可多步规划、调用工具、跨会话记忆的代理时，**如何设计代理在每一步所看到、记住、隔离和传递的信息环境**。
- 这很重要，因为企业正在快速尝试部署代理式AI，但生产落地会遇到长流程退化、跨步骤上下文污染、成本/时延失控、多代理权限与责任边界不清等问题；作者引用数据显示**75%企业计划两年内部署agentic AI**，但实际深度转型比例更低，且部署曾出现回撤。
- 提示工程只优化“怎么问”，无法解决第45步时模型“看到了什么、看错了什么、为什么还在带着脏上下文继续行动”这类系统级问题。

## Approach
- 核心方法是把**context（上下文）当成代理的“操作系统”**，而不是简单输入文本：它负责内存管理、资源分配、子代理隔离、对外系统接口，以及每一步的信息编排。
- 作者将上下文工程定义为对信息的**组成、时机、表示格式和生命周期**进行管理，即一种“JIT knowledge logistics（准时制知识物流）”：什么信息该给、何时给、以什么形式给、给多久、给哪个子代理。
- 论文提出5个生产级上下文质量标准：**relevance, sufficiency, isolation, economy, provenance**，用于判断上下文是否既够用又不过载、是否隔离污染、是否可追溯且经济可行。
- 在此基础上，作者提出两个更高层级：**Intent Engineering** 用于把组织目标、价值观、权衡次序编码进代理基础设施；**Specification Engineering** 用于把企业政策、质量标准、协议和指令整理为机器可读规范，以支撑大规模自治运行。
- 最终形成四层累积式成熟度模型：**prompt engineering → context engineering → intent engineering → specification engineering**，强调后层不是替代前层，而是建立在前层之上。

## Results
- 这篇论文主要是**概念框架/立场论文**，在所给摘录中**没有提供标准学术基准上的实验结果、消融实验或可复现实验数值**。
- 文中给出的最具体量化证据来自行业调查而非模型评测：**Deloitte 2026（N=3,235，24国）称约75%的组织计划在两年内部署agentic AI，但仅34%表示已用AI深度改造业务**。
- **KPMG 2026（N=130，美国C-suite）**显示代理部署比例从**2025年Q1的11%升至Q3的42%**，又在**Q4回落到26%**；作者将其解读为从试点转向生产级系统时暴露出上下文与治理复杂性。
- 同一调查中，企业**平均年度AI预算达到1.24亿美元**，被用来说明若缺乏上下文压缩、缓存与隔离设计，多步代理会因token与延迟成本而失去单位经济性。
- 文中还引用**Gartner 2025**预测：到**2030年**，半自主AI代理将编排**10%**关键生产运营/质量/维护用例，高于当前**2%**，用以支持企业级多代理与边缘-云混合架构的重要性。
- 最强的非量化主张是：**“谁控制代理的上下文，谁就控制它的行为；谁控制它的意图，谁就控制它的策略；谁控制它的规范，谁就控制它的规模。”**

## Link
- [http://arxiv.org/abs/2603.09619v1](http://arxiv.org/abs/2603.09619v1)
