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
- software-debugging
- reliability-engineering
- empirical-study
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Characterizing Faults in Agentic AI: A Taxonomy of Types, Symptoms, and Root Causes

## Summary
这篇论文通过分析开源 Agentic AI 项目的真实缺陷，提出了一个关于故障类型、症状和根因的经验性分类体系，并研究这些故障如何跨组件传播。其价值在于为面向智能体系统的调试、可观测性与可靠性工程提供了更系统的基础。

## Problem
- Agentic AI 结合了 **LLM 推理、工具调用和长时程控制**，其故障模式不同于传统软件或单纯聊天式 LLM，但目前缺少系统性的实证理解。
- 这类系统已进入自动化、软件工程、机器人等关键场景；若不了解故障如何产生、表现和传播，就会带来可靠性、安全性和经济损失风险。
- 现有研究多停留在任务失败或高层行为错误，较少把故障与**具体系统组件、可观察症状和根因**建立清晰映射。

## Approach
- 作者从 **40 个开源 agentic AI 仓库**中收集了 **13,602** 个已关闭 issue 和合并 PR，并通过分层抽样选出 **385** 个故障做深入人工分析。
- 使用 **扎根理论（grounded theory）**，从真实问题描述、日志、堆栈和修复提交中，归纳出三套分类：**5 个架构级故障维度、13 个症状类、12 个根因类**。
- 用 **Apriori 关联规则挖掘**分析“故障类型—症状—根因”之间的高强度共现关系，以发现故障跨组件传播路径。
- 再通过 **145 名开发者**的问卷验证该分类是否贴近真实开发经验，并根据反馈检查其完整性与实用性。

## Results
- 论文产出了一个结构化 taxonomy：**5 个故障维度、13 个症状类别、12 个根因类别**，说明 agentic AI 的失败并非随机，而是可被系统归纳。
- 在样本中，**Runtime and Environment Grounding** 相关故障出现 **87** 次；主要根因包括 **Dependency and Integration Failures（19.5%）** 和 **Data and Type Handling Failures（17.6%）**。
- 关联规则显示明显的跨层传播：例如 **认证请求失败 ↔ 脆弱的 token refresh 机制** 的关联强度 **lift = 181.5**；**错误时间值 ↔ 不当 datetime 转换** 的 **lift = 121.0**。
- 开发者验证结果较强：taxonomy 的代表性平均评分为 **3.97/5**，内部一致性 **Cronbach's α = 0.904**（文中另一处约为 **0.91**），且 **83.8%** 的受访者表示其覆盖了自己遇到的故障。
- 调查中 **74.5%** 的评分达到 **4 分及以上**，表明大多数类别被认为具有现实相关性。
- 论文没有报告与既有方法在统一基准上的“性能提升”式结果；其最强主张是：首次以大规模开源证据和开发者验证，建立了可用于诊断 agentic AI 故障的组件化分类与传播模式。

## Link
- [http://arxiv.org/abs/2603.06847v1](http://arxiv.org/abs/2603.06847v1)
