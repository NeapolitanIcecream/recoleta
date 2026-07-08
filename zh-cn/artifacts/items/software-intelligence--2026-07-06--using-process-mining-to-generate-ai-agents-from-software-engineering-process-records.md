---
source: arxiv
url: https://arxiv.org/abs/2607.04948v1
published_at: '2026-07-06T11:22:25'
authors:
- Saimir Bala
- Fabiana Fournier
- Lior Limonad
- Andreas Metzger
topics:
- multi-agent-software-engineering
- process-mining
- software-agents
- repository-mining
- langgraph
- human-ai-interaction
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Using Process Mining to Generate AI Agents from Software Engineering Process Records

## Summary
## 摘要
pm4aa 从代码库流程记录生成面向具体项目的软件工程代理。它挖掘 GitHub 事件日志来推导角色、约束和 LangGraph 代理实现，而不是从固定代理角色开始。

## 问题
- 论文讨论如何为人机混合的软件工程团队定义 AI 代理角色，同时避免单个大型代理带来的复杂性，或大量小型代理带来的高协调成本。
- 现有多代理软件工程系统常使用程序员、评审者和测试人员等固定角色，因此会遗漏项目特定的工作模式。
- 这很重要，因为团队希望代理遵循其代码库工作流、议题生命周期和贡献规则。

## 方法
- 该流水线使用 PyStack’t 从 GitHub 代码库提取对象中心事件日志，将用户、议题、提交以及后续任务作为对象类型。
- 它解析 Conventional Commit 消息，将提交映射到软件工程任务类别，例如功能开发、缺陷修复、文档和质量保证。
- 它使用基于规则的画像为每个贡献者分配一个角色，画像由活动分布、提交数量和任务类别分布构建。
- 它按角色拆分日志，然后挖掘 OC-DFGs、BPMN 模型和 DECLARE 约束，以捕获角色范围、工作序列、对象交互和行为护栏。
- 它使用 GPT-4-mini 生成角色流程描述，并使用 IBM BOB 生成 LangGraph 应用，其中包含特定角色的代理节点、共享状态、提示词和路由逻辑。

## 结果
- 在 Commitizen 代码库上，原始日志覆盖了约 8 年历史，从 2017 年 11 月到 2025 年 11 月，包含 21,488 个事件和 4,813 个对象。
- 数据集包括 1,459 个议题、2,765 次提交和 589 个用户账户；经过任务补充后，它在提交、任务、议题和用户四类对象中共包含 6,534 个对象。
- 提交解析器匹配了 2,765 次提交中的 1,721 次，占 62.2%，并从 Conventional Commit 消息创建了 1,721 个任务对象。
- 角色分类器将 589 个用户分配到 8 个角色：425 个 issue_reporters、66 个 contributors、37 个 quality_engineers、23 个 technical_writers、20 个 feature_developers、8 个 maintainers、6 个 bots 和 4 个 devops_engineers。
- 各角色的事件量不均衡：issue_reporter 有 16,037 个事件，bot 有 3,394 个，maintainer 有 2,149 个，devops_engineer 有 15 个，因此部分生成的角色规格仍带有探索性质。
- 该概念验证生成了一个以议题为中心的 LangGraph 应用，包含 5 个特定角色代理，并通过功能测试和一项 10 人参与的探索性用户研究进行评估，但摘录未提供测试通过率、用户研究分数或基准比较。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.04948v1](https://arxiv.org/abs/2607.04948v1)
