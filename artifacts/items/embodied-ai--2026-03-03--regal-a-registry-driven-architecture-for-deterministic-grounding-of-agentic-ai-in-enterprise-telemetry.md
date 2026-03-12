---
source: arxiv
url: http://arxiv.org/abs/2603.03018v1
published_at: '2026-03-03T14:13:39'
authors:
- Yuvraj Agrawal
topics:
- llm-systems
- enterprise-telemetry
- mcp-tools
- deterministic-grounding
- data-governance
relevance_score: 0.07
run_id: materialize-outputs
---

# REGAL: A Registry-Driven Architecture for Deterministic Grounding of Agentic AI in Enterprise Telemetry

## Summary
REGAL提出一种面向企业遥测数据的架构，用确定性数据计算和注册表驱动的工具编译来约束LLM代理，而不是让模型直接处理原始日志。其重点不是新学习算法，而是把“语义接口”和“治理”做成可版本化、可审计的系统基础设施。

## Problem
- 企业工程系统会产生海量、异构且不断变化的遥测数据，直接交给LLM会遇到**上下文超限与高token成本**。
- 许多关键语义是组织内部定义的（如P1、release-candidate、regression），如果没有确定性绑定，LLM容易**语义歧义和幻觉**。
- 手写工具/API会随着schema和指标定义演化而**工具漂移**，带来错误解释、审计困难与治理风险。

## Approach
- 用**Medallion ELT**把来自版本控制、CI/CD、问题跟踪和可观测性系统的原始数据，确定性地转换为可回放、版本化的Gold语义工件，而不是把原始事件流暴露给模型。
- 引入一个**metrics registry**作为单一事实来源：在其中声明指标语义、检索逻辑、作用域、缓存策略和访问控制元数据。
- 通过**registry-driven compilation**自动把这些声明式指标编译为MCP工具，让工具描述、实现、ACL和缓存策略来自同一份定义，从而减少tool drift。
- 强制**deterministic → probabilistic**分层：LLM只能消费Gold工件和编译出的有限工具集合，不能反过来影响数据计算；文中用非干扰性质表述为 \(\partial \mathcal{D} / \partial \mathcal{P} = 0\)。
- 在交互上同时支持**pull**（历史查询）和**push**（基于Gold工件更新的事件驱动触发），但两者都共享同一语义接口，避免主动/被动流程的语义分叉。

## Results
- 论文声明的是**原型验证与案例研究**，核心结论是该架构在实践中可行，但**摘录中没有给出系统性的基准表格或完整定量对比数据集结果**。
- 文中最明确的定量说法是：在原型部署中，当Gold工件可放入内存时，**聚合指标检索在中等并发下保持sub-second（小于1秒）**，而**缓存命中时接近即时**；此时整体交互延迟主要由**模型推理**而非数据检索主导。
- 论文声称该设计可带来**更低token消耗**，因为模型处理的是预聚合、语义压缩后的Gold工件，而不是原始日志；但摘录中**未提供具体token节省百分比或绝对数值**。
- 论文声称能改善**治理与审计性**：访问控制、TTL/缓存和工具定义在编译边界统一施加；同时由于动作空间被限制为有限的注册表工具集，**幻觉面和运维风险降低**，但摘录中**未提供定量幻觉率下降数据**。
- 新颖性主张不是算法SOTA，而是系统化提出：把**注册表作为单一事实来源**、把**语义编译作为约束代理动作空间的执行机制**、并与**端到端确定性摄取/版本化Gold工件**结合起来。作者称这是首个对该模式的系统化正式化与端到端落地。

## Link
- [http://arxiv.org/abs/2603.03018v1](http://arxiv.org/abs/2603.03018v1)
