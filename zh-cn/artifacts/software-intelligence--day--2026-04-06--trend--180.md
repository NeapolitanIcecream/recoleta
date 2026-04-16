---
kind: trend
trend_doc_id: 180
granularity: day
period_start: '2026-04-06T00:00:00'
period_end: '2026-04-07T00:00:00'
topics:
- coding-agents
- reinforcement-learning
- verification
- repository-repair
- workflow-automation
run_id: materialize-outputs
aliases:
- recoleta-trend-180
tags:
- recoleta/trend
- topic/coding-agents
- topic/reinforcement-learning
- topic/verification
- topic/repository-repair
- topic/workflow-automation
language_code: zh-CN
---

# 软件智能体研究正收敛到显式奖励和严格验证关卡

## Overview
这一天最强的一批工作，让软件智能体更容易训练、更容易检查，也更容易审计。最清楚的证据来自原子技能强化学习、仓库修复中的可编辑测试闭环，以及编译式或求解器检查的执行路径。共同标准是具体反馈：单元测试、隐藏评估器、证明义务，或确定性的代码路径。

## Clusters

### 奖励设计正在成为核心研究对象
强化学习研究开始更具体地规定智能体因什么得到奖励，以及奖励来自哪里。最强的代码方向结果是在五种可复用技能上训练一个共享策略，然后展示它向更难的仓库任务迁移：SWE-bench Verified 从 0.507 提升到 0.585，SWE-bench Multilingual 从 0.300 提升到 0.389。SandMLE 把同样的思路用于机器学习工程，把完整流水线缩成可验证的微任务。这将执行时间从约 200 秒降到 15 秒以内，并将 MLE-bench-lite 上的 Any Medal rate 相对提升 20.3% 到 66.9%，在 MLE-Dojo 上的 HumanRank 最高提升 32.4%。

#### Evidence
- [Scaling Coding Agents via Atomic Skills](../Inbox/2026-04-06--scaling-coding-agents-via-atomic-skills.md): 基于原子技能的强化学习，在多个代码基准上得到迁移结果。
- [Synthetic Sandbox for Training Machine Learning Engineering Agents](../Inbox/2026-04-06--synthetic-sandbox-for-training-machine-learning-engineering-agents.md): 面向 MLE 智能体的合成沙箱强化学习，在速度和基准表现上都有较大提升。

### 验证闭环现在覆盖规范、测试和模拟器
仓库修复论文开始把测试当作可编辑的证据，而不只是最后一道关卡。Agent-CoEvo 同时维护代码补丁和测试补丁的候选群体，让它们彼此评分，并报告在 SWE-bench Lite 上解决 41.33%，在 SWT-bench Lite 上解决 46.4%。同时，测试质量的 ΔC 达到 56.0%。StatsClaw 也体现出同样重视控制的做法，它把规划、编码、测试和模拟拆成彼此隔离的角色。在它构建 probit 包的流程里，系统以 10^-6 到 10^-8 的容差将 MLE 输出与 R `glm` 对照检查，并报告 7 项 Monte Carlo 验收检查全部通过。

#### Evidence
- [Beyond Fixed Tests: Repository-Level Issue Resolution as Coevolution of Code and Behavioral Constraints](../Inbox/2026-04-06--beyond-fixed-tests-repository-level-issue-resolution-as-coevolution-of-code-and-behavioral-constraints.md): 代码与测试的协同进化，并在 SWE-bench Lite 和 SWT-bench Lite 上给出基准结果。
- [StatsClaw: An AI-Collaborative Workflow for Statistical Software Development](../Inbox/2026-04-06--statsclaw-an-ai-collaborative-workflow-for-statistical-software-development.md): 统计软件生成中的隔离式工作流和独立验证。

### 外部验证正在进入产品执行路径
第二条主线是对智能体可交付内容施加更严格的外部控制。Nidus 把需求、架构、可追踪性和证明义务放进一个经过求解器检查的工件中，并报告一个 10 万行的自托管系统在每次提交时都接受检查。Compiled AI 则把这种控制进一步推进到重复性工作流中：模型只写一次小函数，之后生产环境以确定性代码运行。在 BFCL 上，它报告 96% 的任务完成率、4.5 ms 的中位延迟，以及与直接使用 LLM 相比在约 17 次事务时达到盈亏平衡。在 DocILE 上，它受限的 Code Factory 变体以低于直接运行时推理的延迟达到 80.4% 的行项目识别率。

#### Evidence
- [Nidus: Externalized Reasoning for AI-Assisted Engineering](../Inbox/2026-04-06--nidus-externalized-reasoning-for-ai-assisted-engineering.md): 经过求解器检查的工程治理，对每次变更都做验证。
- [Compiled AI: Deterministic Code Generation for LLM-Based Workflow Automation](../Inbox/2026-04-06--compiled-ai-deterministic-code-generation-for-llm-based-workflow-automation.md): 确定性的编译式工作流，提供成本、延迟和准确率数据。

### 人工监督正在被做进界面，而不是留给提示词技巧
面向开发者的系统也在尝试让人在智能体承担更多工作时仍然保持对系统的理解。Aporia 把明确的设计决策记录到 Decision Bank 中，并把这些决策转成测试；在一项 14 人研究中，参与者心智模型与代码发生分歧的概率比使用 Claude Code 时低 5 倍。Tonone 走的是另一条路，用基于角色的智能体组合包：为工程、产品、安全和运维提供 23 个专家角色和 125 项技能。这里的证据来自实际运行描述，而不是基准测试，但它显示出多角色编排正在多快地变成一种产品模式。

#### Evidence
- [Decision-Oriented Programming with Aporia](../Inbox/2026-04-06--decision-oriented-programming-with-aporia.md): 关于显式设计决策和理解准确性的用户研究。
- [Inspired by gstack: I stopped prompting Claude and gave it job titles instead](../Inbox/2026-04-06--inspired-by-gstack-i-stopped-prompting-claude-and-gave-it-job-titles-instead.md): 开源的多角色编排系统，给出了具体范围说明，但没有基准测试。
