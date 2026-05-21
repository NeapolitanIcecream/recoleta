---
source: arxiv
url: https://arxiv.org/abs/2605.15245v1
published_at: '2026-05-14T10:46:51'
authors:
- Spyridon Alvanakis Apostolou
- Jan Bosch
- "Helena Holmstr\xF6m Olsson"
topics:
- agentic-ai
- software-engineering
- systematic-review
- multi-agent-systems
- sdlc-automation
- code-intelligence
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# Assistance to Autonomy: A Systematic Literature Review of Agentic AI across the Software Development Life Cycle

## Summary
## 摘要
本文综述了软件开发生命周期中的代理式 AI，并发现：在输出能通过测试、编译器、日志或其他可执行信号检查的环节，采用程度最高。

## 问题
- 面向软件开发的代理式 AI 研究增长很快，但团队缺少一个综合视图，无法清楚了解这些系统在 SDLC 的哪些环节有效、哪些设计反复出现，以及工业使用中出现哪些限制。
- 这个问题很重要，因为自主代理可能影响代码、测试、发布和运维；证据薄弱或边界不清会带来可靠性和安全风险。
- 面对 ACM、IEEE、Scopus 和 Springer 中的 1,609 条初始候选记录，人工筛选无法扩展到这样的发表量。

## 方法
- 作者按照 Kitchenham 风格，对 2023 年以来经过同行评审的英文出版物进行了系统文献综述。
- 他们检索了四个来源，对记录进行标准化，去除重复项，补全缺失摘要，并通过质量控制、筛选、相关性选择和人工审查来过滤记录。
- 他们构建了一个与领域无关的多代理筛选流水线，包含 Assistant 和 Evaluator 代理、独立分类、最多三轮分歧对话，并在冲突仍然存在时默认纳入。
- 他们人工检查候选集，并提取 SDLC 阶段、评估语境、架构模式、限制和缓解策略。

## 结果
- 检索从 1,609 条记录开始，处理了 1,331 条，质量控制后保留 796 条，筛选 265 条，选出 127 条候选记录，最终得到 92 项经人工验证的主要研究。
- 在这 92 项研究中，13 项使用工业语境，79 项是学术概念验证研究，说明多数证据仍来自受控环境。
- 最大的 SDLC 类别是维护，有 20 项研究；测试与 QA 有 18 项；跨环节系统有 15 项；部署与运维有 14 项；编码与实现有 12 项。
- 工业研究集中在可验证的后期阶段：测试与 QA 有 5 项工业研究，部署与运维有 2 项，而编码与实现、需求分析各有 0 项工业研究。
- 主导架构是 Planner-Executor-Reviewer 角色专业化，常配有 Orchestrator；Reviewer 通过测试、编译器输出、日志、指标或 CI/CD 状态等可执行反馈来检查输出。
- 人工审查后，筛选流水线产生了 26 个假阳性；对 100 篇已排除论文的样本检查发现 1 个假阴性，其中筛选排除项为 0/50，相关性选择排除项为 1/50，据此作者估计在 669 条已排除记录中大约漏掉了 7 篇相关论文。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.15245v1](https://arxiv.org/abs/2605.15245v1)
