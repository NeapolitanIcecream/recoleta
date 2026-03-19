---
source: arxiv
url: http://arxiv.org/abs/2603.09134v1
published_at: '2026-03-10T03:15:36'
authors:
- Shaswata Mitra
- Raj Patel
- Sudip Mittal
- Md Rayhanur Rahman
- Shahram Rahimi
topics:
- multi-agent-security
- cyber-operations
- llm-agents
- trust-boundaries
- tool-orchestration
- memory-security
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# AgenticCyOps: Securing Multi-Agentic AI Integration in Enterprise Cyber Operations

## Summary
本文提出 AgenticCyOps，一个面向企业网络安全运营中多智能体 AI 集成的安全架构框架。核心观点是：多数已知攻击最终都会落到两个关键集成面——工具编排与记忆管理，因此应把它们当作主要信任边界来设计防御。

## Problem
- 论文要解决的是：企业把具备自主调用工具、共享记忆、互相通信能力的多智能体系统接入实际业务后，会暴露出传统确定性流水线没有的新型攻击面。
- 这件事重要，因为在 SOC/CyberOps 这类高对抗场景里，一旦代理被误导或被攻陷，不只是“出错”，还可能帮助攻击者规避检测；文中还指出攻击者横向移动可少于 **30 分钟**，而组织平均要 **181 天** 识别入侵、再花 **60 天** 遏制。
- 现有研究多聚焦提示注入或单点漏洞，缺少一个能把多层攻击面系统化映射到可执行企业防御原则的整体架构模型。

## Approach
- 作者先把 MAS 威胁按 **component / coordination / protocol** 三层拆解，发现不同攻击虽然表现各异，但结构上大多收敛到两个可利用面：**tool orchestration** 和 **memory management**。
- 基于这一观察，框架把这两个面定义为主要信任边界，并提出五条防御原则：**authorized interfaces**、**capability scoping**、**verified execution**、**memory integrity & synchronization**、**access-controlled data isolation**。
- 对工具侧，简单说就是：先确认工具是真的且被授权，再把代理权限收得很小，最后任何高风险动作都要先验证后执行，可配合共识校验、审计、签名清单、注册表和策略控制。
- 对记忆侧，简单说就是：写入前过滤和验证，读取时做一致性/共识校验，并把不同组织或不同任务的记忆隔离开，避免投毒、泄露和横向污染。
- 在落地上，作者把该框架应用到一个基于 **MCP** 的 SOC/SOAR 架构中，采用阶段划分代理、共识验证回路和按组织划分的记忆边界来实现纵深防御。

## Results
- 论文声称其 **coverage analysis、attack path tracing、trust boundary assessment** 表明，该设计能够覆盖文中整理的已记录攻击向量，并形成 defense-in-depth；但摘录未给出更细粒度逐项指标表。
- 对 **4** 条代表性攻击链中的 **3** 条，系统可在前 **2** 个步骤内拦截。
- 相比扁平化的多智能体系统（flat MAS），该设计将可被利用的信任边界数至少减少 **72%**。
- 论文将此结果定位为企业级多智能体 AI 集成安全的基础框架，但从提供文本看，结果主要来自架构分析与案例评估，而非大规模基准数据集上的实验分数比较。

## Link
- [http://arxiv.org/abs/2603.09134v1](http://arxiv.org/abs/2603.09134v1)
