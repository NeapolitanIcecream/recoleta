---
kind: trend
trend_doc_id: 180
granularity: day
period_start: '2026-04-06T00:00:00'
period_end: '2026-04-07T00:00:00'
topics:
- coding-agents
- reinforcement-learning
- software-testing
- program-repair
- verification
- workflow-automation
run_id: materialize-outputs
aliases:
- recoleta-trend-180
tags:
- recoleta/trend
- topic/coding-agents
- topic/reinforcement-learning
- topic/software-testing
- topic/program-repair
- topic/verification
- topic/workflow-automation
language_code: zh-CN
---

# 软件代理研究正收敛到可验证的训练回路和硬性控制闸门

## Overview
这一天最清晰的一批工作，让软件代理更容易评分、更容易重跑，也更容易在未通过检查时被拦下。Atomic-skill RL、Agent-CoEvo 和 Nidus 分别在不同位置收紧了控制回路：训练目标、仓库修复和工程治理。与前几天相比，重点更少放在证明代理能在真实环境中行动，更多放在建立训练和验证设置，让这些行动始终可测量。

## Clusters

### 面向工程代理的执行评分 RL
强化学习正变得更易用，因为训练目标更窄，环境运行也更快。*Scaling Coding Agents via Atomic Skills* 将软件工作拆成五个可验证技能，并报告在十个任务上平均提升 18.7%，其中 SWE-bench Verified 从 0.507 提高到 0.585。*SandMLE* 把同样的“先执行再评分”逻辑用到机器学习工程：合成任务把运行时间从约 200 秒降到 15 秒以下，并将 MLE-bench-lite 上的 Any Medal rate 提高 20.3% 到 66.9%。共同模式很直接：让每一步都便宜、易评分，再扩展 on-policy RL。

#### Evidence
- [Scaling Coding Agents via Atomic Skills](../Inbox/2026-04-06--scaling-coding-agents-via-atomic-skills.md): 面向编码代理的原子技能 RL 设置与跨任务收益
- [Synthetic Sandbox for Training Machine Learning Engineering Agents](../Inbox/2026-04-06--synthetic-sandbox-for-training-machine-learning-engineering-agents.md): 合成沙箱设计、13 倍加速，以及 MLE 性能提升

### 仓库和服务层面的行为优先评估
仓库代理现在看的是它们能不能修复行为，而不只是打补丁。*Agent-CoEvo* 同时搜索代码补丁和测试补丁，再用通过/失败矩阵给结果打分。它在 SWE-bench Lite 上报告 41.33% resolved，在 SWT-bench Lite 上报告 46.4%，测试质量也高于文中列出的基线。在微服务场景中，*Mirage* 在测试期间把模型保留在依赖调用环路里，在 110 个场景上达到 99% status-code fidelity 和 99% response-shape fidelity。这两篇论文都把模型放进可执行的反馈环里，在行为展开时直接检查结果。

#### Evidence
- [Beyond Fixed Tests: Repository-Level Issue Resolution as Coevolution of Code and Behavioral Constraints](../Inbox/2026-04-06--beyond-fixed-tests-repository-level-issue-resolution-as-coevolution-of-code-and-behavioral-constraints.md): 代码与测试联合搜索，以及在 SWE-bench Lite 和 SWT-bench Lite 上的基准结果
- [MIRAGE: Online LLM Simulation for Microservice Dependency Testing](../Inbox/2026-04-06--mirage-online-llm-simulation-for-microservice-dependency-testing.md): 用于微服务测试的运行时依赖模拟与保真度指标

### 确定性与求解器校验的控制层
另一条路线是在任务已经清楚到可以编译或验证时，收紧模型在运行时的自由度。*Compiled AI* 先生成一次小型代码产物，验证后再以确定性方式运行。在 BFCL 上，它达到 96% task completion，约 17 次事务后达到盈亏平衡，中位延迟为 4.5 ms，复现率为 100%。*Nidus* 在治理上更进一步：每次变更都要对照由求解器支撑的动态规范进行检查，论文还报告了一个自托管的 100,000 行系统，并且每次提交都有 proof obligations。当天最强的系统都不把“谨慎行事”交给模型自己。它们用代码、测试或形式化检查来约束模型。

#### Evidence
- [Compiled AI: Deterministic Code Generation for LLM-Based Workflow Automation](../Inbox/2026-04-06--compiled-ai-deterministic-code-generation-for-llm-based-workflow-automation.md): 编译式工作流生成、验证流程，以及成本/延迟结果
- [Nidus: Externalized Reasoning for AI-Assisted Engineering](../Inbox/2026-04-06--nidus-externalized-reasoning-for-ai-assisted-engineering.md): 经求解器检查的动态规范与自托管证据
