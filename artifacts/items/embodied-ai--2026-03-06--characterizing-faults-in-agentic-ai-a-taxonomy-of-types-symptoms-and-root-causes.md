---
source: arxiv
url: http://arxiv.org/abs/2603.06847v1
published_at: '2026-03-06T20:12:29'
authors:
- Mehil B Shah
- Mohammad Mehdi Morovati
- Mohammad Masudur Rahman
- Foutse Khomh
topics:
- agentic-ai
- fault-taxonomy
- failure-analysis
- software-debugging
- reliability-engineering
relevance_score: 0.18
run_id: materialize-outputs
---

# Characterizing Faults in Agentic AI: A Taxonomy of Types, Symptoms, and Root Causes

## Summary
这篇论文系统研究了 agentic AI 系统中的故障，提出了一个把**故障类型、可观察症状和根因**联系起来的实证 taxonomy。它的核心价值是说明这类失败并非随机杂乱，而是有结构、会跨组件传播，并可被系统化调试。

## Problem
- 论文要解决的问题是：**agentic AI** 把 LLM 推理、工具调用、长时程控制和外部环境交互组合在一起后，会出现不同于传统软件或单独 LLM 应用的新型故障，但目前缺少对这些故障**如何产生、如何表现、如何跨组件传播**的实证理解。
- 这件事重要，是因为 agentic AI 正被用于企业自动化、软件工程、机器人和决策支持等高风险场景；如果不理解故障模式，可能导致数据删除、安全漏洞、经济损失，甚至在安全关键领域带来物理风险。
- 现有研究多停留在任务失败或行为层面，缺少把失败与**具体系统组件**对应起来的分析，因此难以支撑可靠的调试、可观测性和可靠性工程。

## Approach
- 作者从 **40 个开源 agentic AI 仓库**中挖掘了 **13,602** 个已关闭 issue 和已合并 PR，作为真实世界故障语料来源。
- 他们采用**分层抽样**，从中选取 **385** 个故障做深度人工分析，以保持不同仓库类别的代表性。
- 然后使用**扎根理论（grounded theory）**做归纳式编码：先从 issue、日志、栈追踪和修复提交中提取细粒度现象，再逐步汇总成高层 taxonomy，最终形成故障类型、症状和根因的结构化分类。
- 为了理解“故障怎么传导”，他们把每个故障编码成“故障类别 + 症状 + 根因”的事务，并使用 **Apriori 关联规则挖掘**找出统计显著的传播关系。
- 最后通过 **145 名开发者**的问卷验证 taxonomy 是否符合实际开发经验。

## Results
- 论文产出了一套较完整的 taxonomy：**5 个架构级故障维度、13 个症状类别、12 个根因类别**。
- 在定量分布上，作者指出 **Runtime and Environment Grounding** 相关故障有 **87** 个实例；最主要的根因是 **Dependency and Integration Failures（19.5%）** 和 **Data and Type Handling Failures（17.6%）**。
- 关联规则挖掘显示故障常常跨组件传播，而不是停留在单点：例如**认证请求失败**与脆弱的 token refresh 机制强相关，报告的 **lift = 181.5**；**错误时间值**与不当 datetime 转换强相关，**lift = 121.0**。
- 开发者验证结果较强：taxonomy 的代表性平均评分为 **3.97/5**，内部一致性 **Cronbach's α = 0.904**（文中 RQ3 处约为 **0.91**），**83.8%** 的受访者表示该 taxonomy 覆盖了他们亲身遇到的故障，且 **74.5%** 的评分为 **4 分或以上**。
- 相比于“超过某个基线模型”的性能论文，这篇工作不是提出更高任务分数，而是声称一个**经大规模仓库挖掘和开发者验证支持的故障分类与传播框架**，可作为 agentic AI 调试和可靠性工程的基础。文中没有提供传统 ML 基准上的 accuracy / F1 / success-rate 对比数值。

## Link
- [http://arxiv.org/abs/2603.06847v1](http://arxiv.org/abs/2603.06847v1)
