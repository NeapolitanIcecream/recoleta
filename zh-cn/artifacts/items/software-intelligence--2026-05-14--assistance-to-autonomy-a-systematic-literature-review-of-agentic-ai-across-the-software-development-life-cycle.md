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
## 总结
本文回顾了软件开发生命周期中的代理式 AI，发现当输出可以通过测试、编译器、日志或其他可执行信号来检查时，采用最强。

## 问题
- 面向软件开发的代理式 AI 研究增长很快，但团队缺少一份统一视图，来说明系统在 SDLC 的哪些环节有效、哪些设计模式反复出现、以及工业使用中会出现哪些限制。
- 这个问题很重要，因为自主代理会影响代码、测试、发布和运维；证据不足或边界不清会带来可靠性和安全风险。
- 人工筛选无法应对论文数量，ACM、IEEE、Scopus 和 Springer 的初始候选记录共有 1,609 条。

## 方法
- 作者按照 Kitchenham 风格，对 2023 年以来的英文同行评审出版物做了系统性文献综述。
- 他们检索了四个来源，标准化记录，去重，补全缺失摘要，并通过质量控制、筛选、相关性选择和人工复核进行过滤。
- 他们构建了一个与领域无关的多智能体筛选流程，包含 Assistant 和 Evaluator 智能体、独立分类、最多三轮分歧对话，以及在冲突仍未解决时默认纳入。
- 他们人工检查候选集，并提取 SDLC 阶段、评估场景、架构模式、限制和缓解策略。

## 结果
- 检索从 1,609 条记录开始，处理了 1,331 条，质量控制后保留 796 条，筛选 265 条，选出 127 条候选，最后得到 92 篇人工验证的主要研究。
- 在这 92 篇研究中，13 篇使用工业场景，79 篇是学术概念验证研究，说明大多数证据仍来自受控环境。
- 最大的 SDLC 类别是维护 20 篇、测试与 QA 18 篇、跨阶段系统 15 篇、部署与运维 14 篇，以及编码与实现 12 篇。
- 工业研究集中在可验证的后期阶段：测试与 QA 有 5 篇工业研究，部署与运维有 2 篇，而编码与实现和需求分析都没有工业研究。
- 主导架构是 Planner-Executor-Reviewer 角色分工，常带有 Orchestrator；Reviewer 通过测试、编译器输出、日志、指标或 CI/CD 状态等可执行反馈检查输出。
- 筛选流程在人工复核后产生了 26 个假阳性；一个包含 100 篇被排除文献的样本发现 1 个假阴性，其中筛选排除阶段为 0/50，相关性选择排除阶段为 1/50。作者据此估计，在 669 条被排除记录中大约漏掉了 7 篇相关论文。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.15245v1](https://arxiv.org/abs/2605.15245v1)
