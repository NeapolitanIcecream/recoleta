---
source: arxiv
url: http://arxiv.org/abs/2603.10808v1
published_at: '2026-03-11T14:14:53'
authors:
- Linghao Zhang
topics:
- agent-development
- human-ai-interaction
- memory-augmented-agents
- knowledge-crystallization
- domain-expert-agents
relevance_score: 0.87
run_id: materialize-outputs
language_code: zh-CN
---

# Nurture-First Agent Development: Building Domain-Expert AI Agents Through Conversational Knowledge Crystallization

## Summary
本文提出一种“先养成、后固化”的智能体开发范式：不是先把专家知识一次性写进代码或提示词，而是在真实对话中逐步培养智能体，再把零散经验周期性沉淀为结构化知识。其核心贡献是把“开发”和“使用”合并为持续共演化过程，面向高度隐性、个性化且持续变化的领域知识。

## Problem
- 论文要解决的是**领域专家知识如何被有效编码进 AI 智能体**的问题，尤其是那些难以预先形式化的隐性知识、情境判断和个人化经验。
- 传统 **code-first** 依赖工程师把知识写成规则/流程，可靠但难捕捉专家判断，且更新成本高；**prompt-first** 依赖静态提示词，易上手但会遇到上下文窗口和静态失效问题。
- 这很重要，因为当前基础模型的通用能力已不再是主要瓶颈，真正限制高价值行业智能体的是从“会做任务”到“输出值得专家信任”的**configuration gap**。

## Approach
- 提出 **Nurture-First Development (NFD)**：智能体先以最小脚手架启动，在实际工作对话中由领域专家持续“养成”，而不是先完整开发再部署。
- 核心机制是 **Knowledge Crystallization Cycle**：先通过日常对话获得碎片化经验，再周期性地把这些经验提炼成可复用的结构化知识资产。
- 设计了 **Three-Layer Cognitive Architecture**，把知识分成三层：**Constitutional**（长期原则/身份）、**Skill**（任务化技能与参考知识）、**Experiential**（高频增长的交互经验）。
- 配套提出 **Dual-Workspace Pattern** 与 **Spiral Development Model**：一个工作区用于日常“养成”互动，另一个用于“外科手术式”知识结晶与整理，整体按螺旋式循环持续提升。
- 论文还给出形式化定义，包括知识状态、结晶操作、效率指标与算法化描述，并用美国股票研究智能体案例说明方法适用性。

## Results
- 论文**没有提供标准基准数据集上的定量实验结果**，也没有报告如准确率、F1、胜率或与现有框架的数值对比。
- 明确的定性主张包括：NFD 相比 code-first / prompt-first，将开发-部署关系从“顺序式”改为“并发交织式”，并把主要开发者从工程师/提示词工程师转移为**领域实践者本人**。
- 表 1 中给出的非实验性对比声称：NFD 的 **time to first value** 可达 **minutes (scaffold)**，而 code-first 为 **weeks–months**，prompt-first 为 **hours–days**。
- 架构层面给出一个具体容量主张：**Constitutional Layer** 因每次会话都加载，通常占可用上下文的 **10–15%**，因此应只保存原则与索引，而非大段细节知识。
- 可扩展性方面，论文主张三类范式的上限不同：code-first 受**工程能力**限制，prompt-first 受**上下文窗口**限制，而 NFD 主要受**记忆检索质量**限制。
- 实证部分仅为**金融研究代理（美国股票分析）案例说明**，用于展示框架如何落地，而非证明在公开 benchmark 上取得突破性数值提升。

## Link
- [http://arxiv.org/abs/2603.10808v1](http://arxiv.org/abs/2603.10808v1)
